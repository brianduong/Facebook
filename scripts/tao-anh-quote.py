#!/usr/bin/env python3
"""Tạo ảnh quote 1:1 (1080x1080) đúng nhận diện kênh Sống Tốt.

Dùng:
    python3 scripts/tao-anh-quote.py VD-007 "Dòng thứ nhất" "Dòng thứ hai"
    python3 scripts/tao-anh-quote.py VD-007 "Một dòng thôi" --tone tram --kicker "MỘT VIỆC"

Kết quả: assets/templates/quotes/VD-007-quote.svg + .png
Cần `rsvg-convert` để xuất PNG (brew install librsvg). Không có thì vẫn ra file SVG.
"""

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import nhan_dien as nd  # noqa: E402

OUT_DIR = nd.REPO / "assets" / "templates" / "quotes"


def main() -> int:
    p = argparse.ArgumentParser(description="Tạo ảnh quote 1:1 cho kênh Sống Tốt")
    p.add_argument("ma_so", help="Mã video, vd VD-007")
    p.add_argument("dong", nargs="+", help="Mỗi tham số là một dòng chữ trên ảnh")
    p.add_argument("--tone", default="vua",
                   help="Sắc nền. Nền tối: " + " · ".join(sorted(nd.TONES))
                        + " — Nền sáng (--sang): " + " · ".join(sorted(nd.TONES_SANG)))
    p.add_argument("--kicker", help="Chữ cỡ lớn phía trên, vd MỘT VIỆC")
    p.add_argument("--sang", action="store_true",
                   help="Nền sáng, chữ đen, từ khoá tô màu — bản dành cho Facebook. "
                        "Đánh dấu từ khoá bằng dấu sao: \"cái bạn *sợ nhất*\"")
    p.add_argument("--hau-to", default="quote",
                   help="Hậu tố tên file (mặc định quote → VD-007-quote.png)")
    a = p.parse_args()

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    svg = OUT_DIR / f"{a.ma_so}-{a.hau_to}.svg"
    png = OUT_DIR / f"{a.ma_so}-{a.hau_to}.png"

    if a.sang:
        tone = a.tone if a.tone in nd.TONES_SANG else "kem"
        noi_dung = nd.tao_svg_sang(a.dong, tone=tone, kicker=a.kicker)
    else:
        tone = a.tone if a.tone in nd.TONES else "vua"
        noi_dung = nd.tao_svg(a.dong, tone=tone, kicker=a.kicker)
    svg.write_text(noi_dung, encoding="utf-8")
    print(f"✅ {svg.relative_to(nd.REPO)}")

    if nd.xuat_png(svg, png):
        print(f"✅ {png.relative_to(nd.REPO)}")
    else:
        print("⚠️  Chưa có rsvg-convert nên chưa xuất PNG. Cài: brew install librsvg")
    return 0


if __name__ == "__main__":
    sys.exit(main())
