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

⚠️ GHI NGUỒN LÀ BẮT BUỘC. Giấy phép ảnh Pexels thì không bắt, nhưng điều khoản
API thì có: *"Whenever you are doing an API request make sure to show a prominent
link to Pexels."* Mình lấy ảnh qua API nên phải theo. Cách làm: thêm một dòng ở
cuối caption Facebook, ví dụ

    Ảnh: Pexels.com

Script tự ghi tên người chụp vào `nguon.txt` cạnh ảnh để anh ghi tên họ nếu muốn.
Ngoài ra: dùng thương mại được, không được bán lại ảnh gốc nguyên trạng — đưa vào
video có chữ đè lên là hợp lệ.

Hạn mức miễn phí: 200 lượt/giờ, 20.000 lượt/tháng.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
THU_MUC_ANH = REPO / "assets" / "images" / "canh"
API = "https://api.pexels.com/v1/search"

# Pexels chặn User-Agent mặc định của urllib ("Python-urllib/3.x") → trả 403.
# Đã thử: cùng key, đổi User-Agent thì 403 thành 200. Nên phải gắn cho MỌI request.
USER_AGENT = "song-tot/1.0 (+https://www.facebook.com/songtot.in)"

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
    # VD-001
    "ánh nắng qua cửa sổ": "morning sunlight through window",
    "tay rót nước": "hands pouring water glass",
    "giường vừa dọn": "made bed morning light",
    "người ngồi bên bàn viết": "person writing notebook desk",
    # VD-002
    "mưa trên mái hiên": "rain dripping from roof eaves",
    "hai người dưới một cái áo mưa": "two people sharing umbrella rain",
    "bàn tay đưa": "hands giving receiving gesture",
    "người bước vào toà nhà": "person entering office building",
    # dùng chung
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
    req = urllib.request.Request(
        f"{API}?{q}", headers={"Authorization": key, "User-Agent": USER_AGENT}
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            return json.load(r).get("photos", [])
    except urllib.error.HTTPError as e:
        if e.code == 401:
            sys.exit("❌ PEXELS_API_KEY sai hoặc hết hạn. Lấy key mới ở https://www.pexels.com/api/")
        if e.code == 403:
            sys.exit("❌ Pexels trả 403 Forbidden. Thường là do key bị dán kèm dấu cách/dấu nháy "
                     "trong .env, hoặc User-Agent bị chặn. Kiểm tra lại dòng PEXELS_API_KEY.")
        if e.code == 429:
            sys.exit("❌ Quá 200 lượt/giờ của Pexels. Chờ một lát rồi chạy lại.")
        raise


def tai(url: str, ra: Path) -> None:
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(req, timeout=60) as r, ra.open("wb") as f:
        f.write(r.read())


def ghi_file_nguon(ra: Path, tu_khoa: list[str], dong: list[str]) -> None:
    """Điều khoản API bắt phải dẫn nguồn Pexels → giữ danh sách để dán vào caption."""
    (ra / "nguon.txt").write_text(
        "Ảnh tải qua Pexels API. Điều khoản API BẮT BUỘC dẫn nguồn:\n"
        "  → thêm dòng 'Ảnh: Pexels.com' vào cuối caption Facebook.\n\n"
        f"Từ khoá: {', '.join(dict.fromkeys(tu_khoa))}\n\n"
        "Người chụp từng ảnh (ghi tên nếu muốn ghi đầy đủ hơn):\n"
        + "\n".join(f"  {d}" for d in dong) + "\n",
        encoding="utf-8"
    )


# ---------------------------------------------------------------- chế độ chọn

def _duong_dan_chon(ma: str) -> tuple[Path, Path, Path]:
    """Thư mục tạm giữ ứng viên, file ghi thông tin, và bảng ảnh để xem."""
    thu_muc = REPO / "video" / "thu-anh" / ma          # trong video/ nên không lên GitHub
    return thu_muc, thu_muc / "ung-vien.json", thu_muc.parent / f"{ma}-chon.png"


def gom_ung_vien(key: str, tu_khoa: list[str], huong: str, moi_tu_khoa: int,
                 ma: str) -> list[dict]:
    """Tải ảnh nhỏ của nhiều ứng viên về, ghi lại thông tin để bước --lay dùng."""
    thu_muc, f_json, _ = _duong_dan_chon(ma)
    if thu_muc.exists():
        shutil.rmtree(thu_muc)
    thu_muc.mkdir(parents=True)

    ung_vien: list[dict] = []
    for tk in tu_khoa:
        for ct in tim(key, tk, huong, so_luong=moi_tu_khoa):
            so = len(ung_vien) + 1
            nho = thu_muc / f"{so:02d}.jpg"
            tai(ct["src"]["medium"], nho)       # bản nhỏ, chỉ để xem cho nhanh
            ung_vien.append({
                "so": so, "tu_khoa": tk, "xem": str(nho),
                "tai_ve": ct["src"]["large2x"],
                "nguoi_chup": ct["photographer"], "trang": ct["url"],
            })
            print(f"   {so:2d}. {tk}")
    f_json.write_text(json.dumps(ung_vien, ensure_ascii=False, indent=1), encoding="utf-8")
    return ung_vien


def dung_bang_chon(ung_vien: list[dict], ra: Path, moi_hang: int = 6) -> None:
    """Ghép ứng viên thành một bảng ảnh có số thứ tự để xem một lượt."""
    if not shutil.which("rsvg-convert"):
        sys.exit("❌ Thiếu rsvg-convert (brew install librsvg) — cần để dựng bảng chọn.")

    o, cao_o, le = 300, 440, 12                        # cỡ mỗi ô và khoảng cách
    hang = (len(ung_vien) + moi_hang - 1) // moi_hang
    rong = moi_hang * (o + le) + le
    cao = hang * (cao_o + le) + le

    phan: list[str] = []
    for i, uv in enumerate(ung_vien):
        x = le + (i % moi_hang) * (o + le)
        y = le + (i // moi_hang) * (cao_o + le)
        phan.append(
            f'  <image xlink:href="file://{uv["xem"]}" x="{x}" y="{y}" '
            f'width="{o}" height="{cao_o}" preserveAspectRatio="xMidYMid slice"/>\n'
            f'  <rect x="{x}" y="{y}" width="66" height="52" fill="#0B1F18" opacity="0.85"/>\n'
            f'  <text x="{x + 33}" y="{y + 38}" text-anchor="middle" font-family="Arial" '
            f'font-size="34" font-weight="bold" fill="#E9C46A">{uv["so"]}</text>'
        )

    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" '
           f'xmlns:xlink="http://www.w3.org/1999/xlink" width="{rong}" height="{cao}">\n'
           f'  <rect width="{rong}" height="{cao}" fill="#16382A"/>\n'
           + "\n".join(phan) + "\n</svg>\n")

    f_svg = ra.with_suffix(".svg")
    f_svg.write_text(svg, encoding="utf-8")
    subprocess.run(["rsvg-convert", "-w", str(rong), "-h", str(cao), "-o", str(ra), str(f_svg)],
                   check=True)
    f_svg.unlink()


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
    p.add_argument("--chon", type=int, metavar="N",
                   help="Chế độ CHỌN: lấy N ứng viên mỗi từ khoá, ghép thành một bảng "
                        "ảnh có số thứ tự để anh xem rồi tự chọn. Không ghi vào thư mục ảnh.")
    p.add_argument("--lay", metavar="1,4,7",
                   help="Sau khi xem bảng ở --chon, lấy đúng những số này làm ảnh nền "
                        "(theo thứ tự anh gõ = thứ tự xuất hiện trong video).")
    a = p.parse_args()

    key = doc_env().get("PEXELS_API_KEY") or os.environ.get("PEXELS_API_KEY")
    if not key:
        sys.exit(
            "❌ Chưa có PEXELS_API_KEY.\n"
            "   1. Vào https://www.pexels.com/api/ → bấm 'Get Started' → đăng nhập\n"
            "      (có thể dùng 'Continue with Google') → điền mô tả → key hiện ra ngay\n"
            "   2. Mở file .env, dán vào dòng:  PEXELS_API_KEY=key_vua_copy\n"
            "   → Hướng dẫn đầy đủ từng bước: docs/lay-pexels-api-key.md"
        )

    ra = THU_MUC_ANH / a.ma
    _, f_json, f_bang = _duong_dan_chon(a.ma)

    # ---- Bước 2 của chế độ chọn: lấy đúng những số anh đã chấm ----
    if a.lay:
        if not f_json.exists():
            sys.exit(f"❌ Chưa có danh sách ứng viên cho {a.ma}.\n"
                     f"   Chạy trước:  python3 scripts/tai-anh-pexels.py {a.ma} --chon 6")
        ung_vien = {uv["so"]: uv for uv in json.loads(f_json.read_text(encoding="utf-8"))}
        try:
            so_chon = [int(s) for s in a.lay.replace(" ", "").split(",") if s]
        except ValueError:
            sys.exit("❌ --lay phải là các số cách nhau bởi dấu phẩy, ví dụ --lay 2,5,9")
        thieu = [s for s in so_chon if s not in ung_vien]
        if thieu:
            sys.exit(f"❌ Không có ứng viên số {thieu}. Bảng chọn chỉ có 1–{max(ung_vien)}.")

        ra.mkdir(parents=True, exist_ok=True)
        for f in ra.glob("*.jpg"):
            f.unlink()
        print(f"⬇️  Lấy {len(so_chon)} ảnh đã chọn → {ra.relative_to(REPO)}")
        ghi_nguon = []
        for i, s in enumerate(so_chon, 1):
            uv = ung_vien[s]
            f = ra / f"{i:02d}.jpg"
            tai(uv["tai_ve"], f)
            print(f"   {i:2d}. {f.name}  ← ứng viên #{s}  · chụp bởi {uv['nguoi_chup']}")
            ghi_nguon.append(f"{f.name}  —  {uv['nguoi_chup']}  —  {uv['trang']}")
        ghi_file_nguon(ra, [ung_vien[s]["tu_khoa"] for s in so_chon], ghi_nguon)
        print(f"\n✅ Xong. Render được rồi:\n"
              f"   .venv-tts/bin/python scripts/render-video-v2.py {a.ma} "
              f"--nhac assets/music/nen-am-ap.m4a")
        print("📌 Nhớ dòng 'Ảnh: Pexels.com' ở cuối caption — điều khoản API bắt buộc.")
        return

    tu_khoa = a.tu_khoa or [dich_tu_khoa(t) for t in tu_khoa_tu_kich_ban(a.ma)]
    if not tu_khoa:
        sys.exit(f"❌ Không tìm được từ khoá cho {a.ma}. "
                 f"Thêm dòng '**Hình ảnh/B-roll:**' vào kịch bản, hoặc dùng --tu-khoa")

    # ---- Bước 1 của chế độ chọn: gom ứng viên và dựng bảng để xem ----
    if a.chon:
        print(f"🔎 {len(tu_khoa)} từ khoá × {a.chon} ứng viên · hướng {a.huong}")
        ung_vien = gom_ung_vien(key, tu_khoa, a.huong, a.chon, a.ma)
        if not ung_vien:
            sys.exit("❌ Không tìm được ảnh nào.")
        f_bang.parent.mkdir(parents=True, exist_ok=True)
        dung_bang_chon(ung_vien, f_bang)
        print(f"\n🖼  Bảng chọn: {f_bang.relative_to(REPO)}  ({len(ung_vien)} ứng viên)")
        print(f"   Mở xem:   open {f_bang.relative_to(REPO)}")
        print(f"   Chọn xong thì lấy đúng những số đó, theo thứ tự muốn xuất hiện:")
        print(f"   python3 scripts/tai-anh-pexels.py {a.ma} --lay 2,5,9,11")
        return

    ra.mkdir(parents=True, exist_ok=True)
    print(f"🔎 {len(tu_khoa)} từ khoá · hướng {a.huong} → {ra.relative_to(REPO)}")

    dem = 0
    ghi_nguon: list[str] = []
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
            ghi_nguon.append(f"{f.name}  —  {ct['photographer']}  —  {ct['url']}")

    if dem:
        ghi_file_nguon(ra, tu_khoa, ghi_nguon)
    print(f"\n✅ Xong {dem} ảnh.  Xem thử:  open {ra.relative_to(REPO)}")
    if dem:
        print("📌 Nhớ thêm dòng 'Ảnh: Pexels.com' vào cuối caption — điều khoản API bắt buộc.")


if __name__ == "__main__":
    main()
