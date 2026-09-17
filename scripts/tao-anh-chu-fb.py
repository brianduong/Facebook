#!/usr/bin/env python3
"""Dựng ảnh chữ 1:1 cho Facebook, đọc thẳng từ file caption.

Vì sao có tuyến ảnh chữ riêng cho Facebook: đọc API 18/09/2026 thấy Page thời
2019 đăng **ảnh chữ nền sáng** thì được 419 thích/bài (bài top 4.429 thích ·
390 chia sẻ); từ 2026 đổi sang video dọc thì còn 1,5 thích/bài. Tuyến này thử
lại đúng định dạng đã chạy với chính tệp người theo dõi đó. Video **giữ nguyên**,
không đụng gì tới.

Nguồn sự thật là `content/captions/AC-XX-caption.md` — cả chữ trên ảnh lẫn màu nền
đều nằm trong đó, nên sửa chữ thì sửa ở file rồi chạy lại, đừng sửa tay file ảnh.

    python3 scripts/tao-anh-chu-fb.py AC-01
    python3 scripts/tao-anh-chu-fb.py --tat-ca

Cần `rsvg-convert` để xuất PNG (brew install librsvg).
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import nhan_dien as nd  # noqa: E402

DIR_CAPTION = nd.REPO / "content" / "captions"
DIR_ANH = nd.REPO / "assets" / "templates" / "quotes"


def doc_bai(ma: str) -> tuple[list[str], str]:
    """Trả về (các dòng chữ trên ảnh, tên màu nền) đọc từ file caption."""
    f = DIR_CAPTION / f"{ma}-caption.md"
    if not f.exists():
        sys.exit(f"❌ Không thấy {f.relative_to(nd.REPO)}")
    noi_dung = f.read_text(encoding="utf-8")

    m_tone = re.search(r"nền `([a-z_]+)`", noi_dung)
    if not m_tone:
        sys.exit(f"❌ {f.name} thiếu tên màu nền — cần một dòng dạng: nền `kem`")
    tone = m_tone.group(1)
    if tone not in nd.TONES_SANG:
        sys.exit(f"❌ {f.name} ghi nền `{tone}`, chỉ có: {' · '.join(sorted(nd.TONES_SANG))}")

    m_chu = re.search(r"##\s*Chữ trên ảnh.*?```\s*\n(.*?)\n```", noi_dung, re.S)
    if not m_chu:
        sys.exit(f"❌ {f.name} thiếu mục '## Chữ trên ảnh' có khối ```")
    dong = [d.rstrip() for d in m_chu.group(1).splitlines() if d.strip()]
    if not dong:
        sys.exit(f"❌ {f.name} có mục 'Chữ trên ảnh' nhưng khối rỗng")
    return dong, tone


def dung_anh(ma: str) -> bool:
    dong, tone = doc_bai(ma)
    DIR_ANH.mkdir(parents=True, exist_ok=True)
    svg = DIR_ANH / f"{ma}-fb.svg"
    png = DIR_ANH / f"{ma}-fb.png"
    svg.write_text(nd.tao_svg_sang(dong, tone=tone), encoding="utf-8")
    xong = nd.xuat_png(svg, png)
    # Chữ không tô màu vẫn giữ dấu sao trong file nguồn — bỏ đi khi in ra cho dễ đọc.
    xem = " / ".join(d.replace("*", "") for d in dong)
    print(f"{'✅' if xong else '⚠️ '} {ma}  nền {tone:<7} {xem[:62]}")
    if not xong:
        print("    Chưa có rsvg-convert nên mới ra SVG. Cài: brew install librsvg")
    return xong


def main() -> int:
    p = argparse.ArgumentParser(description="Dựng ảnh chữ 1:1 cho Facebook")
    p.add_argument("ma", nargs="*", help="Mã bài ảnh, vd AC-01")
    p.add_argument("--tat-ca", action="store_true", help="Dựng lại toàn bộ AC-*")
    a = p.parse_args()

    ma_list = a.ma
    if a.tat_ca:
        ma_list = sorted(f.name[:5] for f in DIR_CAPTION.glob("AC-*-caption.md"))
    if not ma_list:
        sys.exit("❌ Thiếu mã bài. Vd: tao-anh-chu-fb.py AC-01 — hoặc thêm --tat-ca")

    loi = [ma for ma in ma_list if not dung_anh(ma)]
    print(f"\nXong {len(ma_list) - len(loi)}/{len(ma_list)} ảnh.")
    return 1 if loi else 0


if __name__ == "__main__":
    sys.exit(main())
