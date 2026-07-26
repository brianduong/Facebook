#!/usr/bin/env python3
"""Tải ảnh thật từ Pexels về làm cảnh nền cho video.

Thay cho nhân vật vẽ tay + cảnh SVG: mỗi thẻ chữ trong video nằm trên một
tấm ảnh chụp thật, nhìn đỡ "rẻ tiền" hơn hẳn.

Cần `PEXELS_API_KEY` trong file `.env`. Lấy key miễn phí ở
https://www.pexels.com/api/ (đăng ký ~2 phút, 200 lượt/giờ — thừa dùng).

    # tải theo từ khoá ghi sẵn trong kịch bản
    python3 scripts/tai-anh-pexels.py VD-001

    # tự chọn từ khoá
    python3 scripts/tai-anh-pexels.py VD-001 --tu-khoa "morning sunlight window" "pouring warm water"

Ảnh về nằm ở `assets/images/canh/VD-001/01.jpg, 02.jpg…` (thư mục này
KHÔNG lên GitHub — xem .gitignore).

Giấy phép Pexels: dùng thương mại được, không bắt ghi nguồn, không được
bán lại ảnh gốc nguyên trạng. Đưa vào video có chữ đè lên là hợp lệ.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
THU_MUC_ANH = REPO / "assets" / "images" / "canh"
API = "https://api.pexels.com/v1/search"

# Chỉ lấy ảnh dọc cho Reels 9:16; ảnh ngang bị cắt mất hai bên thành ra
# nhân vật/vật thể chính hay rơi ra ngoài khung.
HUONG_MAC_DINH = "portrait"


def doc_env() -> dict[str, str]:
    """Đọc .env đơn giản (KEY=VALUE, bỏ qua dòng trống và dòng #)."""
    f = REPO / ".env"
    ra: dict[str, str] = {}
    if not f.exists():
        return ra
    for dong in f.read_text(encoding="utf-8").splitlines():
        dong = dong.strip()
        if not dong or dong.startswith("#") or "=" not in dong:
            continue
        k, _, v = dong.partition("=")
        ra[k.strip()] = v.strip().strip('"').strip("'")
    return ra


def tu_khoa_tu_kich_ban(ma: str) -> list[str]:
    """Đọc dòng '**Hình ảnh/B-roll:**' trong file kịch bản để lấy từ khoá.

    Trong kịch bản viết tiếng Việt, ngăn nhau bằng dấu '·'. Pexels tìm bằng
    tiếng Anh cho ra ảnh tốt hơn nhiều, nên phần dịch nằm ở bảng TU_DIEN dưới.
    """
    ds = sorted((REPO / "content" / "scripts").glob(f"{ma}-*.md"))
    if not ds:
        return []
    for dong in ds[0].read_text(encoding="utf-8").splitlines():
        if "B-roll" in dong:
            phan = dong.split(":", 1)[1] if ":" in dong else ""
            phan = re.sub(r"\*\*|_", "", phan)
            return [x.strip() for x in phan.split("·") if x.strip()]
    return []


# Cụm tiếng Việt hay gặp trong ghi chú B-roll → cụm tìm tiếng Anh cho Pexels.
# Thiếu chữ nào thì cứ thêm vào đây, hoặc truyền thẳng --tu-khoa.
TU_DIEN = {
    "ánh nắng qua cửa sổ": "morning sunlight through window",
    "tay rót nước": "hands pouring water glass",
    "giường vừa dọn": "made bed morning light",
    "người ngồi bên bàn viết": "person writing notebook desk",
    "bàn trà": "tea cup table calm",
    "đường cây": "tree lined path walking",
    "bến mưa": "rain bus stop street",
    "quán cà phê": "vietnamese coffee shop",
    "buổi sáng": "quiet morning light",
}


def dich_tu_khoa(tv: str) -> str:
    thuong = tv.lower().strip()
    for k, v in TU_DIEN.items():
        if k in thuong:
            return v
    return tv          # không có trong từ điển thì cứ để nguyên, Pexels vẫn tìm được


def tim(key: str, tu_khoa: str, huong: str, so_luong: int = 5) -> list[dict]:
    q = urllib.parse.urlencode(
        {"query": tu_khoa, "orientation": huong, "per_page": so_luong, "locale": "en-US"}
    )
    req = urllib.request.Request(f"{API}?{q}", headers={"Authorization": key})
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            return json.load(r).get("photos", [])
    except urllib.error.HTTPError as e:
        if e.code == 401:
            sys.exit("❌ PEXELS_API_KEY sai hoặc hết hạn. Lấy key mới ở https://www.pexels.com/api/")
        if e.code == 429:
            sys.exit("❌ Quá 200 lượt/giờ của Pexels. Chờ một lát rồi chạy lại.")
        raise


def tai(url: str, ra: Path) -> None:
    req = urllib.request.Request(url, headers={"User-Agent": "song-tot/1.0"})
    with urllib.request.urlopen(req, timeout=60) as r, ra.open("wb") as f:
        f.write(r.read())


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("ma", help="Mã video, ví dụ VD-001")
    p.add_argument("--tu-khoa", nargs="*",
                   help="Tự chọn từ khoá (tiếng Anh cho kết quả tốt nhất). "
                        "Bỏ trống thì lấy từ dòng B-roll trong kịch bản.")
    p.add_argument("--huong", default=HUONG_MAC_DINH,
                   choices=["portrait", "landscape", "square"],
                   help="Hướng ảnh (mặc định portrait cho Reels 9:16)")
    p.add_argument("--so-anh", type=int, default=1,
                   help="Số ảnh lấy cho mỗi từ khoá (mặc định 1)")
    a = p.parse_args()

    key = doc_env().get("PEXELS_API_KEY") or os.environ.get("PEXELS_API_KEY")
    if not key:
        sys.exit(
            "❌ Chưa có PEXELS_API_KEY.\n"
            "   1. Vào https://www.pexels.com/api/ → đăng ký → copy key\n"
            "   2. Mở file .env, thêm dòng:  PEXELS_API_KEY=key_vua_copy"
        )

    tu_khoa = a.tu_khoa or [dich_tu_khoa(t) for t in tu_khoa_tu_kich_ban(a.ma)]
    if not tu_khoa:
        sys.exit(f"❌ Không tìm được từ khoá cho {a.ma}. "
                 f"Thêm dòng '**Hình ảnh/B-roll:**' vào kịch bản, hoặc dùng --tu-khoa")

    ra = THU_MUC_ANH / a.ma
    ra.mkdir(parents=True, exist_ok=True)
    print(f"🔎 {len(tu_khoa)} từ khoá · hướng {a.huong} → {ra.relative_to(REPO)}")

    dem = 0
    for tk in tu_khoa:
        anh = tim(key, tk, a.huong, so_luong=max(a.so_anh, 3))
        if not anh:
            print(f"   ⚠️  không có ảnh nào cho {tk!r}")
            continue
        for ct in anh[: a.so_anh]:
            dem += 1
            f = ra / f"{dem:02d}.jpg"
            tai(ct["src"]["large2x"], f)
            print(f"   {dem:2d}. {f.name}  ← {tk!r}  · chụp bởi {ct['photographer']}")

    if dem:
        # Ghi lại nguồn để sau này cần đối chiếu bản quyền thì có chỗ tra
        (ra / "nguon.txt").write_text(
            f"Ảnh tải từ Pexels (pexels.com) — giấy phép dùng thương mại tự do.\n"
            f"Từ khoá: {', '.join(tu_khoa)}\n", encoding="utf-8"
        )
    print(f"\n✅ Xong {dem} ảnh.  Xem thử:  open {ra.relative_to(REPO)}")


if __name__ == "__main__":
    main()
