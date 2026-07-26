"""Dựng lớp chữ trong suốt phủ lên ảnh thật — khung dọc 9:16 cho Reels.

Khác bản cũ ở chỗ: không vẽ nhân vật, không vẽ cảnh. Nền là **ảnh chụp thật**
(tải bằng `tai-anh-pexels.py`), còn file này chỉ lo phần chữ + logo + lớp tối
làm cho chữ đọc được trên ảnh.

Xuất ra SVG nền trong suốt, `render-video-v2.py` sẽ đè lên ảnh bằng ffmpeg.

Vùng an toàn của Reels (Facebook che mất):
    - đáy  320px  (nút thích/bình luận/chia sẻ + tên trang)
    - phải 120px  (cột nút dọc)
Nên khối chữ nằm gọn trong khoảng y 980–1520.
"""

from __future__ import annotations

import html
import textwrap

RONG, CAO = 1080, 1920

KEM = "#F7FAF5"       # trắng ngà — chữ chính
VANG = "#E9C46A"      # vàng nắng — gạch nhấn
LA_NHAT = "#A9D4A6"
FONT = "'Be Vietnam Pro','Montserrat','Helvetica Neue',Arial,sans-serif"
CTA = "theo dõi để sống tốt mỗi ngày"

# Vùng an toàn Reels
LE_DAY = 320
LE_PHAI = 120
CHU_DAY = 1520        # đáy khối chữ, nằm trên vùng nút của Facebook
CHU_DINH = 980        # đỉnh khối chữ

LOGO = f"""  <g transform="translate(64 96)">
    <g transform="scale(0.30)">
      <path d="M0,60 C -48,30 -48,-75 -7,-116 C -3,-95 -9,-35 0,60 Z" fill="{KEM}" transform="rotate(-16)"/>
      <path d="M0,60 C 48,30 48,-75 7,-116 C 3,-95 9,-35 0,60 Z" fill="{LA_NHAT}" transform="rotate(16)"/>
    </g>
    <text x="56" y="20" font-family="{FONT}" font-size="46" font-weight="800" fill="{KEM}">Sống Tốt</text>
  </g>"""


def boc_dong(chu: str, moi_dong: int = 22) -> list[str]:
    """Ngắt đoạn thành dòng ngắn. Khung dọc hẹp hơn khung vuông nên ít chữ hơn."""
    return textwrap.wrap(" ".join(chu.split()), width=moi_dong) or [""]


def co_chu(dong: list[str]) -> int:
    """Cỡ chữ lớn nhất mà dòng dài nhất vẫn nằm trong lề an toàn (~880px)."""
    dai_nhat = max(len(d) for d in dong)
    for co, gioi_han in ((84, 14), (78, 16), (72, 19), (66, 22), (60, 25), (54, 29), (48, 34)):
        if dai_nhat <= gioi_han:
            return co
    return 44


def tao_lop_chu(chu: str, dau_video: bool = False, cta: bool = False) -> str:
    """Lớp phủ trong suốt: mờ tối phía dưới + khối chữ + logo.

    chu        : nội dung thẻ
    dau_video  : thẻ mở đầu — chữ to hơn một nấc cho câu hook đập vào mắt
    cta        : có in dòng kêu gọi theo dõi ở đáy không (dùng cho thẻ cuối)
    """
    dong = boc_dong(chu, moi_dong=20 if dau_video else 22)
    co = co_chu(dong) + (6 if dau_video else 0)
    buoc = int(co * 1.36)

    cao_khoi = (len(dong) - 1) * buoc
    # Neo khối chữ vào đáy vùng an toàn, nhưng không trèo quá cao lên đỉnh.
    # Thẻ có dòng kêu gọi thì phải nhấc lên, chừa chỗ cho dòng đó nằm trong vùng an toàn.
    day = CHU_DAY - (110 if cta else 0)
    dau_khoi = max(day - cao_khoi, CHU_DINH)

    dong_svg = []
    for i, d in enumerate(dong):
        y = dau_khoi + i * buoc
        dong_svg.append(
            f'    <text x="{RONG // 2}" y="{y}" text-anchor="middle" font-family="{FONT}" '
            f'font-size="{co}" font-weight="700" fill="{KEM}" '
            f'filter="url(#bong)">{html.escape(d)}</text>'
        )

    # Gạch nhấn vàng ngay dưới khối chữ
    gach_y = dau_khoi + cao_khoi + int(co * 0.72)
    gach = (f'    <rect x="{RONG // 2 - 44}" y="{gach_y}" width="88" height="6" rx="3" '
            f'fill="{VANG}" opacity="0.9"/>')

    dong_cta = ""
    if cta:
        dong_cta = (
            f'    <text x="{RONG // 2}" y="{gach_y + 62}" text-anchor="middle" '
            f'font-family="{FONT}" font-size="34" font-weight="600" fill="{KEM}" '
            f'opacity="0.86" letter-spacing="1.2">{html.escape(CTA)}</text>'
        )

    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{RONG}" height="{CAO}"
     viewBox="0 0 {RONG} {CAO}">
  <defs>
    <linearGradient id="toi_duoi" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%"   stop-color="#0B1F18" stop-opacity="0"/>
      <stop offset="38%"  stop-color="#0B1F18" stop-opacity="0.42"/>
      <stop offset="70%"  stop-color="#0B1F18" stop-opacity="0.78"/>
      <stop offset="100%" stop-color="#0B1F18" stop-opacity="0.92"/>
    </linearGradient>
    <linearGradient id="toi_tren" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%"   stop-color="#0B1F18" stop-opacity="0.55"/>
      <stop offset="100%" stop-color="#0B1F18" stop-opacity="0"/>
    </linearGradient>
    <filter id="bong" x="-12%" y="-12%" width="124%" height="124%">
      <feDropShadow dx="0" dy="3" stdDeviation="7" flood-color="#06120D" flood-opacity="0.75"/>
    </filter>
  </defs>

  <!-- tối đỉnh khung cho logo nổi, tối đáy khung cho chữ đọc được -->
  <rect x="0" y="0" width="{RONG}" height="360" fill="url(#toi_tren)"/>
  <rect x="0" y="{CAO - 1180}" width="{RONG}" height="1180" fill="url(#toi_duoi)"/>

{LOGO}
{chr(10).join(dong_svg)}
{gach}
{dong_cta}
</svg>
"""
