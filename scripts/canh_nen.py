"""Cảnh nền minh hoạ cho video 1:1 — vẽ vector, tự làm nên không lo bản quyền.

Mỗi cảnh vẽ trong khung 1080x1080, chi tiết dồn ở nửa trên (vì nửa dưới bị
dải chữ che). Đường sàn nằm ở y≈660 để nhân vật đứng cho có chân đế.

Danh sách cảnh: xem CANH.keys() — hoặc chạy `python3 scripts/xem-cach-nen.py`.
"""

from __future__ import annotations

KEM = "#F7FAF5"
VANG = "#E9C46A"
LA_NHAT = "#A9D4A6"

SAN = 660  # cao độ đường sàn / chân trời


def _rem(x: int, y: int, dai: int = 90, nghieng: int = 14) -> str:
    return f'<path d="M{x},{y} l{nghieng},{dai}" stroke="#CFE6DA" stroke-width="4" stroke-linecap="round" opacity="0.55"/>'


def _sao(x: int, y: int, r: float = 3) -> str:
    return f'<circle cx="{x}" cy="{y}" r="{r}" fill="{KEM}" opacity="0.85"/>'


def _cay(x: int, y: int, s: float = 1.0) -> str:
    """Cây đơn giản: thân + hai tán lá."""
    return (
        f'<g transform="translate({x} {y}) scale({s})">'
        f'<rect x="-9" y="-90" width="18" height="90" rx="6" fill="#3A2E28"/>'
        f'<circle cx="0" cy="-120" r="62" fill="#2E5D4B"/>'
        f'<circle cx="-34" cy="-96" r="44" fill="#376E56"/>'
        f'<circle cx="36" cy="-100" r="46" fill="#376E56"/>'
        f"</g>"
    )


def canh_sang_cua_so() -> str:
    """Buổi sáng trong phòng, nắng qua cửa sổ — dùng cho nội dung khởi đầu ngày."""
    return f"""
  <defs>
    <linearGradient id="c1tuong" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="#3C7A62"/><stop offset="100%" stop-color="#2A5544"/>
    </linearGradient>
    <linearGradient id="c1troi" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="#CFE9DA"/><stop offset="100%" stop-color="#F3E3BC"/>
    </linearGradient>
  </defs>
  <rect width="1080" height="1080" fill="url(#c1tuong)"/>
  <rect x="0" y="{SAN}" width="1080" height="{1080 - SAN}" fill="#24473A"/>

  <!-- cửa sổ -->
  <rect x="120" y="164" width="440" height="400" rx="14" fill="url(#c1troi)"/>
  <circle cx="440" cy="276" r="58" fill="{VANG}" opacity="0.95"/>
  <g stroke="{KEM}" stroke-width="14">
    <path d="M340,164 V564"/><path d="M120,364 H560"/>
  </g>
  <rect x="106" y="150" width="468" height="428" rx="18" fill="none" stroke="{KEM}" stroke-width="16"/>
  <!-- nắng đổ xuống sàn -->
  <path d="M150,578 L110,{SAN + 120} L660,{SAN + 120} L520,578 Z" fill="{VANG}" opacity="0.22"/>

  <!-- chậu cây trên bệ -->
  <rect x="106" y="570" width="468" height="20" rx="8" fill="{KEM}" opacity="0.9"/>
  <g transform="translate(200 570)">
    <path d="M-26,0 L-20,-40 L20,-40 L26,0 Z" fill="{VANG}"/>
    <path d="M0,-40 C -30,-58 -34,-96 -8,-104 C -2,-80 -4,-58 0,-40 Z" fill="{LA_NHAT}"/>
    <path d="M0,-40 C 28,-56 34,-92 10,-100 C 4,-78 4,-58 0,-40 Z" fill="#7BAE7F"/>
  </g>
"""


def canh_ban_tra() -> str:
    """Bàn với ly nước ấm bốc khói — dùng cho nội dung nhẹ, biết ơn, sáng sớm."""
    return f"""
  <defs>
    <linearGradient id="c2tuong" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="#35705B"/><stop offset="100%" stop-color="#28513F"/>
    </linearGradient>
  </defs>
  <rect width="1080" height="1080" fill="url(#c2tuong)"/>
  <circle cx="300" cy="190" r="150" fill="{VANG}" opacity="0.14"/>
  <circle cx="300" cy="190" r="86" fill="{VANG}" opacity="0.2"/>
  <rect x="0" y="{SAN}" width="1080" height="{1080 - SAN}" fill="#3A2E28"/>
  <rect x="0" y="{SAN - 16}" width="1080" height="22" rx="8" fill="#4A3B32"/>

  <!-- ly nước + khói -->
  <g transform="translate(250 {SAN - 16})">
    <path d="M-52,0 L-44,-104 L44,-104 L52,0 Z" fill="{KEM}"/>
    <path d="M44,-88 C 84,-84 84,-40 44,-36" fill="none" stroke="{KEM}" stroke-width="12"/>
    <g stroke="{KEM}" stroke-width="7" fill="none" opacity="0.5" stroke-linecap="round">
      <path d="M-18,-120 C -34,-146 -2,-160 -18,-190"/>
      <path d="M16,-124 C 0,-150 32,-164 16,-194"/>
    </g>
  </g>
  <!-- quyển sổ -->
  <g transform="translate(520 {SAN - 16})">
    <rect x="-70" y="-24" width="140" height="24" rx="6" fill="{LA_NHAT}"/>
    <rect x="-62" y="-32" width="124" height="14" rx="5" fill="{KEM}"/>
  </g>
"""


def canh_duong_cay() -> str:
    """Đường đi bộ có cây, trời sáng — dùng cho nội dung bước tiếp, đi tiếp."""
    return f"""
  <defs>
    <linearGradient id="c3troi" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="#BFE3D0"/><stop offset="100%" stop-color="#EFE0BA"/>
    </linearGradient>
  </defs>
  <rect width="1080" height="1080" fill="url(#c3troi)"/>
  <circle cx="230" cy="190" r="72" fill="{VANG}"/>
  <path d="M0,540 C 220,470 380,560 620,510 C 800,472 960,520 1080,492 L1080,{SAN} L0,{SAN} Z" fill="#48876C"/>
  <rect x="0" y="{SAN}" width="1080" height="{1080 - SAN}" fill="#2E5D4B"/>
  <!-- lối đi -->
  <path d="M430,{SAN} L640,{SAN} L780,1080 L250,1080 Z" fill="#D9C9A8" opacity="0.92"/>
  {_cay(150, SAN + 6, 1.15)}
  {_cay(1030, SAN + 10, 0.95)}
  {_cay(430, SAN - 6, 0.55)}
"""


def canh_ben_mua() -> str:
    """Trạm chờ xe, trời mưa — dùng cho câu chuyện che mưa, giúp người lạ."""
    return f"""
  <defs>
    <linearGradient id="c4troi" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="#2A4A55"/><stop offset="100%" stop-color="#3E6B63"/>
    </linearGradient>
  </defs>
  <rect width="1080" height="1080" fill="url(#c4troi)"/>
  <rect x="0" y="{SAN}" width="1080" height="{1080 - SAN}" fill="#27453E"/>

  <!-- mái trạm chờ -->
  <path d="M120,300 L860,300 L900,352 L80,352 Z" fill="#2E5D4B"/>
  <rect x="150" y="352" width="18" height="{SAN - 352}" fill="#456F5E"/>
  <rect x="820" y="352" width="18" height="{SAN - 352}" fill="#456F5E"/>
  <rect x="196" y="392" width="180" height="120" rx="10" fill="{KEM}" opacity="0.22"/>

  <!-- mưa -->
  {"".join(_rem(x, y, 110) for x, y in ((60, 60), (240, 20), (420, 90), (600, 30), (760, 80), (940, 40), (1010, 150), (140, 200), (330, 240), (520, 190), (690, 230), (880, 200)))}
  <!-- vũng nước -->
  <ellipse cx="400" cy="{SAN + 70}" rx="180" ry="26" fill="{KEM}" opacity="0.14"/>
  <ellipse cx="820" cy="{SAN + 130}" rx="130" ry="20" fill="{KEM}" opacity="0.12"/>
"""


def canh_bep() -> str:
    """Bồn rửa trong bếp — dùng cho nội dung 'làm một việc nhỏ'."""
    return f"""
  <defs>
    <linearGradient id="c5tuong" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="#33705A"/><stop offset="100%" stop-color="#26503F"/>
    </linearGradient>
  </defs>
  <rect width="1080" height="1080" fill="url(#c5tuong)"/>
  <!-- gạch tường -->
  <g fill="{KEM}" opacity="0.08">
    {"".join(f'<rect x="{x}" y="{y}" width="118" height="78" rx="8"/>' for y in (150, 240, 330) for x in range(60, 1020, 130))}
  </g>
  <rect x="0" y="{SAN - 40}" width="1080" height="{1080 - SAN + 40}" fill="#3F6957"/>
  <rect x="0" y="{SAN - 52}" width="1080" height="20" rx="8" fill="{KEM}" opacity="0.85"/>

  <!-- bồn rửa + vòi -->
  <rect x="180" y="{SAN - 40}" width="330" height="120" rx="16" fill="#2A5544"/>
  <rect x="206" y="{SAN - 26}" width="278" height="92" rx="12" fill="#204033" opacity="0.35"/>
  <path d="M330,{SAN - 52} V 470 C 330,430 420,430 420,470 V {SAN - 90}" fill="none" stroke="{KEM}" stroke-width="16" stroke-linecap="round"/>
  <!-- chồng bát -->
  <g transform="translate(620 {SAN - 52})">
    <ellipse cx="0" cy="-8" rx="62" ry="16" fill="{KEM}"/>
    <ellipse cx="0" cy="-34" rx="56" ry="14" fill="{LA_NHAT}"/>
    <ellipse cx="0" cy="-58" rx="48" ry="13" fill="{KEM}"/>
  </g>
"""


def canh_dem_sao() -> str:
    """Trời đêm nhiều sao — dùng cho nội dung nghỉ ngơi, dịu lại, tha thứ."""
    return f"""
  <defs>
    <linearGradient id="c6troi" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="#12303F"/><stop offset="100%" stop-color="#1E4437"/>
    </linearGradient>
  </defs>
  <rect width="1080" height="1080" fill="url(#c6troi)"/>
  {"".join(_sao(x, y, r) for x, y, r in ((120, 120, 4), (260, 210, 3), (400, 90, 3.5), (520, 260, 2.5), (660, 140, 4), (800, 240, 3), (940, 110, 3.5), (1000, 300, 2.5), (180, 330, 3), (700, 360, 2.5)))}
  <path d="M860,180 A 62,62 0 1,1 800,120 A 50,50 0 1,0 860,180 Z" fill="{VANG}" opacity="0.9"/>
  <!-- mái nhà -->
  <path d="M0,560 L160,470 L320,560 L320,{SAN} L0,{SAN} Z" fill="#183A2E"/>
  <path d="M760,600 L900,510 L1040,600 L1040,{SAN} L760,{SAN} Z" fill="#183A2E"/>
  <rect x="0" y="{SAN}" width="1080" height="{1080 - SAN}" fill="#14322A"/>
  <rect x="120" y="530" width="46" height="40" rx="6" fill="{VANG}" opacity="0.75"/>
  <rect x="856" y="566" width="46" height="40" rx="6" fill="{VANG}" opacity="0.6"/>
"""


CANH = {
    "sang-cua-so": canh_sang_cua_so,
    "ban-tra": canh_ban_tra,
    "duong-cay": canh_duong_cay,
    "ben-mua": canh_ben_mua,
    "bep": canh_bep,
    "dem-sao": canh_dem_sao,
}


def ve_canh(ten: str) -> str:
    if ten not in CANH:
        raise ValueError(f"Không có cảnh '{ten}'. Chọn: {', '.join(CANH)}")
    return CANH[ten]()
