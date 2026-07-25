"""Nhận diện hình ảnh kênh Sống Tốt — dùng chung cho các script khác.

Giữ một nơi duy nhất định nghĩa màu, font, logo, cách dựng khung 1:1.
Đổi màu/font ở đây là mọi ảnh và video nháp đổi theo.
Bảng màu gốc: docs/dinh-huong-kenh.md
"""

from __future__ import annotations

import shutil
import subprocess
import textwrap
from pathlib import Path
from xml.sax.saxutils import escape

REPO = Path(__file__).resolve().parent.parent

# Bảng màu chốt trong docs/dinh-huong-kenh.md
TONES = {
    "sang": ("#3C7A62", "#2E5D4B", "#123326", 0.62),   # tươi — nội dung nhẹ nhàng
    "vua": ("#2E5D4B", "#7BAE7F", "#123326", 0.68),    # mặc định
    "tram": ("#1E4437", "#2E5D4B", "#0E2A1F", 0.60),   # dịu — nội dung an ủi
}
KEM = "#F7FAF5"       # trắng ngà — chữ chính
VANG = "#E9C46A"      # vàng nắng — điểm nhấn
LA_NHAT = "#A9D4A6"   # xanh lá nhạt — nửa lá logo
FONT = "'Be Vietnam Pro','Montserrat',Arial,sans-serif"
CTA = "theo dõi để sống tốt mỗi ngày"

LOGO = f"""  <g transform="translate(60 70)">
    <g transform="scale(0.28)">
      <path d="M0,60 C -48,30 -48,-75 -7,-116 C -3,-95 -9,-35 0,60 Z" fill="{KEM}" transform="rotate(-16)"/>
      <path d="M0,60 C 48,30 48,-75 7,-116 C 3,-95 9,-35 0,60 Z" fill="{LA_NHAT}" transform="rotate(16)"/>
    </g>
    <text x="52" y="18" font-family="{FONT}" font-size="42" font-weight="800" fill="{KEM}">Sống Tốt</text>
  </g>"""


def co_chu(dong: list[str]) -> int:
    """Cỡ chữ lớn nhất mà dòng dài nhất vẫn nằm trong lề an toàn (~960px)."""
    dai_nhat = max(len(d) for d in dong)
    for co, gioi_han in ((80, 18), (76, 20), (70, 23), (64, 26), (58, 30), (52, 34), (46, 40)):
        if dai_nhat <= gioi_han:
            return co
    return 40


def boc_dong(text: str, moi_dong: int = 26) -> list[str]:
    """Ngắt một đoạn văn thành các dòng ngắn để đọc trên màn hình vuông."""
    return textwrap.wrap(" ".join(text.split()), width=moi_dong) or [""]


def tao_svg(
    dong: list[str],
    tone: str = "vua",
    kicker: str | None = None,
    cta: bool = True,
    giua: bool = False,
    dau_ngoac: bool = True,
) -> str:
    """Dựng một khung 1:1.

    dong        : các dòng chữ (đã ngắt sẵn)
    tone        : 'sang' | 'vua' | 'tram'
    kicker      : chữ vàng cỡ lớn phía trên (vd 'MỘT VIỆC')
    cta         : có in dòng 'theo dõi để sống tốt mỗi ngày' ở đáy không
    giua        : True = khối chữ giữa khung (thẻ lời đọc), False = vùng dưới (ảnh quote)
    dau_ngoac   : hiện dấu ngoặc kép trang trí (chỉ khi không có kicker)
    """
    dau, cuoi, toi, mo = TONES[tone]
    co = co_chu(dong)
    buoc = int(co * 1.34)
    tam = 540 if giua else 720
    dau_khoi = tam - (len(dong) - 1) * buoc // 2

    khoi_chu = "\n".join(
        f'  <text x="540" y="{dau_khoi + i * buoc}" text-anchor="middle" '
        f'font-family="{FONT}" font-size="{co}" font-weight="800" fill="{KEM}">{escape(d)}</text>'
        for i, d in enumerate(dong)
    )

    tren = ""
    if kicker:
        tren = (
            f'  <text x="540" y="470" text-anchor="middle" font-family="{FONT}" '
            f'font-size="120" font-weight="800" fill="{VANG}" letter-spacing="6">{escape(kicker)}</text>'
        )
    elif dau_ngoac and not giua:
        tren = (
            f'  <text x="540" y="490" text-anchor="middle" font-family="Georgia,serif" '
            f'font-size="200" fill="{VANG}" opacity="0.35">“</text>'
        )

    y_vach = dau_khoi + (len(dong) - 1) * buoc + int(co * 0.95)
    vach = f'  <rect x="480" y="{y_vach}" width="120" height="8" rx="4" fill="{VANG}"/>' if not giua else ""

    dong_cta = (
        f'  <text x="540" y="1000" text-anchor="middle" font-family="{FONT}" font-size="34" '
        f'font-weight="500" fill="{VANG}" letter-spacing="4">{CTA}</text>'
        if cta
        else ""
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

{LOGO}

{tren}

{khoi_chu}

{vach}

{dong_cta}
</svg>
"""


def xuat_png(svg: Path, png: Path) -> bool:
    """Xuất PNG 1080x1080 từ SVG. Trả về False nếu máy chưa có rsvg-convert."""
    if not shutil.which("rsvg-convert"):
        return False
    png.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run(
        ["rsvg-convert", "-w", "1080", "-h", "1080", str(svg), "-o", str(png)],
        check=True,
    )
    return True
