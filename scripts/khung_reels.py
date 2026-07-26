"""Dựng lớp chữ trong suốt phủ lên ảnh thật — khung dọc 9:16 cho Reels.

Khác bản cũ ở chỗ: không vẽ nhân vật, không vẽ cảnh. Nền là **ảnh chụp thật**
(tải bằng `tai-anh-pexels.py`), còn file này chỉ lo phần chữ + logo + lớp tối
làm cho chữ đọc được trên ảnh.

Xuất ra SVG nền trong suốt, `render-video-v2.py` sẽ đè lên ảnh bằng ffmpeg.

Vùng an toàn tính theo nơi che nhiều nhất trong ba nền tảng, để **một file đăng
được cả ba chỗ** (Facebook Reels · Instagram Reels · YouTube Shorts):

    | Nền tảng          | đáy che  | phải che | đỉnh che |
    |-------------------|----------|----------|----------|
    | Facebook Reels    | ~320px   | ~120px   | ~110px   |
    | Instagram Reels   | ~400px   | ~120px   | ~110px   |  ← che nhiều nhất ở đáy
    | YouTube Shorts    | ~330px   | ~140px   | ~130px   |  ← che nhiều nhất ở phải/đỉnh

Nên lấy mức khắt khe nhất: đáy 470px, phải 140px, đỉnh 130px. Khối chữ vì thế nằm
trong khoảng y 980–1450 (trước chỉ tính riêng Facebook nên để tới 1520 — Instagram
sẽ che mất dòng cuối).
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
CTA_EN = "subscribe for one small thing a day"

# Vùng an toàn — lấy mức khắt khe nhất của cả ba nền tảng (xem bảng ở đầu file)
LE_DAY = 470          # Instagram che đáy nhiều nhất
LE_PHAI = 140         # YouTube Shorts che phải nhiều nhất
LE_DINH = 130         # YouTube Shorts che đỉnh nhiều nhất
CHU_DAY = 1450        # đáy khối chữ
CHU_DINH = 980        # đỉnh khối chữ

LOGO = f"""  <g transform="translate(64 168)">
    <g transform="scale(0.30)">
      <path d="M0,60 C -48,30 -48,-75 -7,-116 C -3,-95 -9,-35 0,60 Z" fill="{KEM}" transform="rotate(-16)"/>
      <path d="M0,60 C 48,30 48,-75 7,-116 C 3,-95 9,-35 0,60 Z" fill="{LA_NHAT}" transform="rotate(16)"/>
    </g>
    <text x="56" y="20" font-family="{FONT}" font-size="46" font-weight="800" fill="{KEM}">Sống Tốt</text>
  </g>"""

# Logo kênh tiếng Anh: ba việc, một xong hai để đấy. Cùng vị trí và cỡ chữ với logo
# Sống Tốt để hai kênh nhìn ra là cùng một tay làm.
LOGO_EN = f"""  <g transform="translate(70 168)">
    <circle cx="0" cy="0" r="15" fill="{VANG}"/>
    <circle cx="40" cy="0" r="15" fill="none" stroke="{KEM}" stroke-width="4" opacity="0.45"/>
    <circle cx="80" cy="0" r="15" fill="none" stroke="{KEM}" stroke-width="4" opacity="0.45"/>
    <text x="114" y="16" font-family="{FONT}" font-size="46" font-weight="800" fill="{KEM}">One Small Thing</text>
  </g>"""

# Màu lớp phủ tối — ám cả khung hình, nên phải theo nền của từng kênh:
# Sống Tốt xanh lá, One Small Thing xanh đá. Dùng chung thì video tiếng Anh bị ám
# xanh lá, lệch hẳn với icon và banner của kênh đó.
NHAN_DIEN = {
    "vi": (LOGO, CTA, "#0B1F18", "#06120D"),
    "en": (LOGO_EN, CTA_EN, "#0B1219", "#050A0F"),
}


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


def tao_lop_chu(chu: str, dau_video: bool = False, cta: bool = False,
                kenh: str = "vi") -> str:
    """Lớp phủ trong suốt: mờ tối phía dưới + khối chữ + logo.

    chu        : nội dung thẻ
    dau_video  : thẻ mở đầu — chữ to hơn một nấc cho câu hook đập vào mắt
    cta        : có in dòng kêu gọi theo dõi ở đáy không (dùng cho thẻ cuối)
    kenh       : "vi" (Sống Tốt) hoặc "en" (One Small Thing) — đổi logo và lời kêu gọi
    """
    logo_kenh, cta_kenh, mau_toi, mau_bong = NHAN_DIEN[kenh]
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
            f'opacity="0.86" letter-spacing="1.2">{html.escape(cta_kenh)}</text>'
        )

    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{RONG}" height="{CAO}"
     viewBox="0 0 {RONG} {CAO}">
  <defs>
    <linearGradient id="toi_duoi" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%"   stop-color="{mau_toi}" stop-opacity="0"/>
      <stop offset="38%"  stop-color="{mau_toi}" stop-opacity="0.42"/>
      <stop offset="70%"  stop-color="{mau_toi}" stop-opacity="0.78"/>
      <stop offset="100%" stop-color="{mau_toi}" stop-opacity="0.92"/>
    </linearGradient>
    <linearGradient id="toi_tren" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%"   stop-color="{mau_toi}" stop-opacity="0.55"/>
      <stop offset="100%" stop-color="{mau_toi}" stop-opacity="0"/>
    </linearGradient>
    <filter id="bong" x="-12%" y="-12%" width="124%" height="124%">
      <feDropShadow dx="0" dy="3" stdDeviation="7" flood-color="{mau_bong}" flood-opacity="0.75"/>
    </filter>
  </defs>

  <!-- tối đỉnh khung cho logo nổi, tối đáy khung cho chữ đọc được -->
  <rect x="0" y="0" width="{RONG}" height="360" fill="url(#toi_tren)"/>
  <rect x="0" y="{CAO - 1180}" width="{RONG}" height="1180" fill="url(#toi_duoi)"/>

{logo_kenh}
{chr(10).join(dong_svg)}
{gach}
{dong_cta}
</svg>
"""
