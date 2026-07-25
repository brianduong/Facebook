#!/usr/bin/env python3
"""Tạo ảnh quote 1:1 (1080x1080) đúng nhận diện kênh Sống Tốt.

Dùng:
    python3 scripts/tao-anh-quote.py VD-007 "Dòng thứ nhất" "Dòng thứ hai"
    python3 scripts/tao-anh-quote.py VD-007 "Một dòng thôi" --tone tram --kicker "MỘT VIỆC"

Kết quả: assets/templates/quotes/VD-007-quote.svg + .png

Cần `rsvg-convert` để xuất PNG (brew install librsvg). Không có thì vẫn ra file SVG.
"""

import argparse
import shutil
import subprocess
import sys
from pathlib import Path
from xml.sax.saxutils import escape

REPO = Path(__file__).resolve().parent.parent
OUT_DIR = REPO / "assets" / "templates" / "quotes"

# Bảng màu chốt trong docs/dinh-huong-kenh.md
TONES = {
    "sang": ("#3C7A62", "#2E5D4B", "#123326", 0.62),   # tươi, dùng cho nội dung nhẹ
    "vua": ("#2E5D4B", "#7BAE7F", "#123326", 0.68),    # mặc định
    "tram": ("#1E4437", "#2E5D4B", "#0E2A1F", 0.60),   # dịu, dùng cho nội dung an ủi
}
KEM = "#F7FAF5"       # trắng ngà — chữ chính
VANG = "#E9C46A"      # vàng nắng — điểm nhấn
FONT = "'Be Vietnam Pro','Montserrat',Arial,sans-serif"
CTA = "theo dõi để sống tốt mỗi ngày"


def co_chu(dong: list[str]) -> int:
    """Chọn cỡ chữ để dòng dài nhất không tràn khỏi lề an toàn (~960px)."""
    dai_nhat = max(len(d) for d in dong)
    for co, gioi_han in ((80, 18), (76, 20), (70, 23), (64, 26), (58, 30), (52, 34)):
        if dai_nhat <= gioi_han:
            return co
    return 46


def dung_svg(dong: list[str], tone: str, kicker: str | None) -> str:
    dau, cuoi, toi, mo = TONES[tone]
    co = co_chu(dong)
    buoc = int(co * 1.28)

    # Khối chữ căn giữa quanh y=720 (vùng dưới, nơi mắt người xem dừng lại)
    tam = 720
    dau_khoi = tam - (len(dong) - 1) * buoc // 2
    dong_svg = "\n".join(
        f'  <text x="540" y="{dau_khoi + i * buoc}" text-anchor="middle" '
        f'font-family="{FONT}" font-size="{co}" font-weight="800" fill="{KEM}">{escape(d)}</text>'
        for i, d in enumerate(dong)
    )
    y_vach = dau_khoi + (len(dong) - 1) * buoc + int(co * 0.95)

    if kicker:
        tren = (
            f'  <text x="540" y="470" text-anchor="middle" font-family="{FONT}" '
            f'font-size="120" font-weight="800" fill="{VANG}" letter-spacing="6">{escape(kicker)}</text>'
        )
    else:
        tren = (
            f'  <text x="540" y="490" text-anchor="middle" font-family="Georgia,serif" '
            f'font-size="200" fill="{VANG}" opacity="0.35">“</text>'
        )

    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="1080" height="1080" viewBox="0 0 1080 1080">
  <defs>
    <linearGradient id="bg" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="{dau}"/>
      <stop offset="100%" stop-color="{cuoi}"/>
    </linearGradient>
    <linearGradient id="fade" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="{toi}" stop-opacity="0"/>
      <stop offset="100%" stop-color="{toi}" stop-opacity="{mo}"/>
    </linearGradient>
  </defs>

  <rect width="1080" height="1080" fill="url(#bg)"/>
  <rect x="0" y="520" width="1080" height="560" fill="url(#fade)"/>

  <!-- Logo mầm cây + tên kênh -->
  <g transform="translate(60 70)">
    <g transform="scale(0.28)">
      <path d="M0,60 C -48,30 -48,-75 -7,-116 C -3,-95 -9,-35 0,60 Z" fill="{KEM}" transform="rotate(-16)"/>
      <path d="M0,60 C 48,30 48,-75 7,-116 C 3,-95 9,-35 0,60 Z" fill="#A9D4A6" transform="rotate(16)"/>
    </g>
    <text x="52" y="18" font-family="{FONT}" font-size="42" font-weight="800" fill="{KEM}">Sống Tốt</text>
  </g>

{tren}

{dong_svg}

  <rect x="480" y="{y_vach}" width="120" height="8" rx="4" fill="{VANG}"/>

  <text x="540" y="1000" text-anchor="middle" font-family="{FONT}"
        font-size="34" font-weight="500" fill="{VANG}" letter-spacing="4">{CTA}</text>
</svg>
"""


def main() -> int:
    p = argparse.ArgumentParser(description="Tạo ảnh quote 1:1 cho kênh Sống Tốt")
    p.add_argument("ma_so", help="Mã video, vd VD-007")
    p.add_argument("dong", nargs="+", help="Mỗi tham số là một dòng chữ trên ảnh")
    p.add_argument("--tone", choices=sorted(TONES), default="vua", help="Sắc nền (mặc định: vua)")
    p.add_argument("--kicker", help="Chữ vàng cỡ lớn phía trên, vd MỘT VIỆC")
    a = p.parse_args()

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    svg = OUT_DIR / f"{a.ma_so}-quote.svg"
    png = OUT_DIR / f"{a.ma_so}-quote.png"
    svg.write_text(dung_svg(a.dong, a.tone, a.kicker), encoding="utf-8")
    print(f"✅ {svg.relative_to(REPO)}")

    if shutil.which("rsvg-convert"):
        subprocess.run(
            ["rsvg-convert", "-w", "1080", "-h", "1080", str(svg), "-o", str(png)],
            check=True,
        )
        print(f"✅ {png.relative_to(REPO)}")
    else:
        print("⚠️  Chưa có rsvg-convert nên chưa xuất PNG. Cài: brew install librsvg")
    return 0


if __name__ == "__main__":
    sys.exit(main())
