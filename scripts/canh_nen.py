"""Cảnh nền cho video 1:1 — vẽ vector, tự làm nên không lo bản quyền.

Nguyên tắc bố cục (quan trọng, đừng phá):

    0   ─────────────────────────────  VÙNG HÌNH
        cảnh nền + nhân vật bên phải
    690 ─────────────────────────────  VÙNG CHỮ (VUNG_CHU)
        chỉ có chữ, không vẽ gì vào đây
    1080 ────────────────────────────

- Chi tiết cảnh dồn ở **nửa trên và bên trái** (x < 620) vì bên phải là nhân vật.
- Chân trời khoảng y=600, sàn kết thúc ở 690 — không vẽ tràn xuống vùng chữ.
- Có lớp xa (mờ, nhạt) → lớp giữa → lớp gần (đậm, nét) để hình có chiều sâu.
"""

from __future__ import annotations

KEM = "#F7FAF5"
VANG = "#E9C46A"
LA_NHAT = "#A9D4A6"

VUNG_CHU = 690      # từ đây xuống dành cho chữ
CHAN_TROI = 600     # chân trời / mặt sàn


def _may(x: int, y: int, s: float, mo: str) -> str:
    """Đám mây mềm: ba khối tròn mờ chồng nhau."""
    return (
        f'<g transform="translate({x} {y}) scale({s})" filter="url(#{mo})" opacity="0.5">'
        f'<ellipse cx="-46" cy="6" rx="52" ry="24" fill="{KEM}"/>'
        f'<ellipse cx="10" cy="-10" rx="60" ry="32" fill="{KEM}"/>'
        f'<ellipse cx="58" cy="8" rx="46" ry="22" fill="{KEM}"/></g>'
    )


def _bong(cx: int, cy: int, rx: int, ry: int, mo: str, op: float = 0.3) -> str:
    """Bóng đổ mềm dưới vật — thứ làm hình đỡ 'dán phẳng' nhất."""
    return f'<ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}" fill="#0B1F17" opacity="{op}" filter="url(#{mo})"/>'


def _cay(x: int, y: int, s: float, mo: str, xa: bool = False) -> str:
    """Cây: thân cong nhẹ, ba khối lá lệch nhau, có bóng dưới gốc."""
    la1, la2, la3 = ("#4E8B70", "#3F7A61", "#5C9B7C") if not xa else ("#7FAE95", "#719F87", "#8CBAA1")
    return (
        f'{_bong(x, y + 4, int(70 * s), int(14 * s), mo, 0.28 if not xa else 0.12)}'
        f'<g transform="translate({x} {y}) scale({s})">'
        f'<path d="M-7,0 C-4,-40 -10,-70 -4,-104 L10,-104 C6,-70 10,-40 9,0 Z" fill="#4A382C"/>'
        f'<ellipse cx="-2" cy="-140" rx="66" ry="56" fill="{la1}"/>'
        f'<ellipse cx="-42" cy="-112" rx="44" ry="38" fill="{la2}"/>'
        f'<ellipse cx="40" cy="-118" rx="48" ry="40" fill="{la3}"/>'
        f'<ellipse cx="-6" cy="-166" rx="38" ry="30" fill="{la3}" opacity="0.9"/>'
        f"</g>"
    )


def canh_sang_cua_so() -> str:
    """Buổi sáng trong phòng, nắng qua cửa sổ — cho nội dung khởi đầu ngày."""
    return f"""
  <defs>
    <linearGradient id="s1tuong" x1="0%" y1="0%" x2="20%" y2="100%">
      <stop offset="0%" stop-color="#5AA487"/><stop offset="100%" stop-color="#407F66"/>
    </linearGradient>
    <linearGradient id="s1troi" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="#D9EDDF"/><stop offset="60%" stop-color="#F1E6C4"/>
      <stop offset="100%" stop-color="#EBD9A9"/>
    </linearGradient>
    <linearGradient id="s1san" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="#AD8B62"/><stop offset="100%" stop-color="#8C6C4C"/>
    </linearGradient>
    <linearGradient id="s1nang" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="{VANG}" stop-opacity="0.5"/>
      <stop offset="100%" stop-color="{VANG}" stop-opacity="0"/>
    </linearGradient>
    <filter id="s1mo" x="-60%" y="-60%" width="220%" height="220%"><feGaussianBlur stdDeviation="18"/></filter>
    <filter id="s1mo2" x="-60%" y="-60%" width="220%" height="220%"><feGaussianBlur stdDeviation="7"/></filter>
  </defs>
  <rect width="1080" height="1080" fill="url(#s1tuong)"/>
  <rect x="0" y="{CHAN_TROI}" width="1080" height="{VUNG_CHU - CHAN_TROI}" fill="url(#s1san)"/>

  <!-- vệt nắng loang trên tường -->
  <ellipse cx="700" cy="250" rx="300" ry="220" fill="{VANG}" opacity="0.12" filter="url(#s1mo)"/>

  <!-- cửa sổ: khung ngoài, trời, nắng hắt vào -->
  <rect x="96" y="118" width="470" height="440" rx="10" fill="#C8B79A"/>
  <rect x="112" y="134" width="438" height="408" rx="6" fill="url(#s1troi)"/>
  <circle cx="430" cy="250" r="52" fill="#FBF0C8"/>
  <circle cx="430" cy="250" r="96" fill="{VANG}" opacity="0.35" filter="url(#s1mo)"/>
  {_may(210, 210, 0.8, "s1mo2")}
  {_may(360, 330, 0.6, "s1mo2")}
  <g stroke="#C8B79A" stroke-width="16">
    <path d="M331,134 V542"/><path d="M112,338 H550"/>
  </g>
  <!-- nắng đổ xuống sàn -->
  <path d="M130,558 L86,{VUNG_CHU} L640,{VUNG_CHU} L520,558 Z" fill="url(#s1nang)"/>

  <!-- rèm buông bên phải cửa sổ, có nếp gấp cho đỡ phẳng -->
  <path d="M566,108 C600,190 584,320 596,{CHAN_TROI} L664,{CHAN_TROI} C646,420 654,220 622,108 Z"
        fill="#CBD6C9" opacity="0.75"/>
  <g fill="none" stroke="#9FB09C" stroke-width="5" opacity="0.55">
    <path d="M600,150 C618,270 606,430 608,{CHAN_TROI - 10}"/>
    <path d="M628,150 C644,270 634,430 636,{CHAN_TROI - 10}"/>
  </g>

  <!-- bệ cửa + chậu cây -->
  <rect x="88" y="556" width="486" height="18" rx="6" fill="#D6C6A8"/>
  {_bong(206, 578, 46, 10, "s1mo2", 0.35)}
  <g transform="translate(206 556)">
    <path d="M-30,0 L-24,-44 L24,-44 L30,0 Z" fill="#C98A5B"/>
    <path d="M-24,-44 L24,-44 L22,-34 L-22,-34 Z" fill="#B0764B"/>
    <path d="M0,-44 C-34,-64 -38,-104 -10,-114 C-2,-90 -6,-64 0,-44 Z" fill="#4E8B70"/>
    <path d="M0,-44 C30,-60 36,-98 12,-108 C6,-86 4,-62 0,-44 Z" fill="{LA_NHAT}"/>
  </g>
"""


def canh_ban_tra() -> str:
    """Góc bàn với ly nước ấm — cho nội dung biết ơn, ngồi lại với mình."""
    return f"""
  <defs>
    <linearGradient id="s2tuong" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="#549C7E"/><stop offset="100%" stop-color="#3C765D"/>
    </linearGradient>
    <linearGradient id="s2ban" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="#BA8F66"/><stop offset="100%" stop-color="#93704E"/>
    </linearGradient>
    <radialGradient id="s2den" cx="50%" cy="50%" r="50%">
      <stop offset="0%" stop-color="{VANG}" stop-opacity="0.55"/>
      <stop offset="100%" stop-color="{VANG}" stop-opacity="0"/>
    </radialGradient>
    <filter id="s2mo" x="-60%" y="-60%" width="220%" height="220%"><feGaussianBlur stdDeviation="16"/></filter>
    <filter id="s2mo2" x="-60%" y="-60%" width="220%" height="220%"><feGaussianBlur stdDeviation="6"/></filter>
  </defs>
  <rect width="1080" height="1080" fill="url(#s2tuong)"/>

  <!-- đèn thả + vùng sáng ấm (đặt lệch phải cho khỏi chạm ô logo góc trên trái) -->
  <path d="M440,0 V104" stroke="#C8B79A" stroke-width="6"/>
  <path d="M388,104 L492,104 L466,176 L414,176 Z" fill="#D8C7A4"/>
  <circle cx="440" cy="250" r="190" fill="url(#s2den)"/>

  <!-- mặt bàn -->
  <rect x="0" y="{CHAN_TROI - 30}" width="1080" height="{VUNG_CHU - CHAN_TROI + 30}" fill="url(#s2ban)"/>
  <rect x="0" y="{CHAN_TROI - 30}" width="1080" height="10" fill="#B08A63" opacity="0.8"/>

  <!-- ly nước ấm + khói -->
  {_bong(258, CHAN_TROI - 18, 74, 14, "s2mo2", 0.4)}
  <g transform="translate(250 {CHAN_TROI - 24})">
    <path d="M-52,0 C-56,-58 -50,-104 -46,-118 L46,-118 C50,-104 56,-58 52,0 Z" fill="#EFF3EC"/>
    <path d="M-46,-118 L46,-118 C48,-110 48,-104 46,-100 L-46,-100 C-48,-104 -48,-110 -46,-118 Z" fill="#D7DED3"/>
    <path d="M46,-96 C92,-92 92,-40 44,-34" fill="none" stroke="#EFF3EC" stroke-width="13"/>
    <ellipse cx="-18" cy="-108" rx="26" ry="7" fill="#C7A277" opacity="0.9"/>
    <g stroke="#EFF3EC" stroke-width="7" fill="none" opacity="0.45" stroke-linecap="round" filter="url(#s2mo2)">
      <path d="M-16,-134 C-34,-160 -2,-176 -18,-208"/>
      <path d="M18,-138 C0,-164 32,-180 16,-212"/>
    </g>
  </g>

  <!-- sổ tay + bút -->
  {_bong(500, CHAN_TROI - 16, 88, 10, "s2mo2", 0.35)}
  <g transform="translate(500 {CHAN_TROI - 24})">
    <path d="M-92,0 L-84,-30 L92,-30 L84,0 Z" fill="#5E8F74"/>
    <path d="M-84,-30 L84,-30 L80,-40 L-80,-40 Z" fill="#EFF3EC"/>
    <path d="M-40,-46 L64,-64" stroke="#C8B79A" stroke-width="8" stroke-linecap="round"/>
  </g>
"""


def canh_duong_cay() -> str:
    """Đường đi bộ buổi sáng — cho nội dung bước tiếp, đi tiếp."""
    return f"""
  <defs>
    <linearGradient id="s3troi" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="#A8D4E0"/><stop offset="55%" stop-color="#DCEBDA"/>
      <stop offset="100%" stop-color="#F0E4BE"/>
    </linearGradient>
    <linearGradient id="s3xa" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="#8FBBA2"/><stop offset="100%" stop-color="#7BAE93"/>
    </linearGradient>
    <linearGradient id="s3co" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="#72AE8B"/><stop offset="100%" stop-color="#528C6E"/>
    </linearGradient>
    <linearGradient id="s3loi" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="#E2D3AE"/><stop offset="100%" stop-color="#C9B58C"/>
    </linearGradient>
    <filter id="s3mo" x="-60%" y="-60%" width="220%" height="220%"><feGaussianBlur stdDeviation="18"/></filter>
    <filter id="s3mo2" x="-60%" y="-60%" width="220%" height="220%"><feGaussianBlur stdDeviation="7"/></filter>
  </defs>
  <rect width="1080" height="1080" fill="url(#s3troi)"/>

  <!-- mặt trời + mây -->
  <circle cx="236" cy="176" r="62" fill="#FBF0C8"/>
  <circle cx="236" cy="176" r="120" fill="{VANG}" opacity="0.3" filter="url(#s3mo)"/>
  {_may(470, 150, 1.0, "s3mo2")}
  {_may(840, 226, 0.75, "s3mo2")}

  <!-- lớp xa: đồi mờ -->
  <path d="M0,506 C180,452 330,510 520,486 C700,464 900,504 1080,478 L1080,{CHAN_TROI} L0,{CHAN_TROI} Z"
        fill="url(#s3xa)" opacity="0.75"/>
  <ellipse cx="540" cy="{CHAN_TROI - 10}" rx="620" ry="60" fill="{KEM}" opacity="0.25" filter="url(#s3mo)"/>

  <!-- lớp gần: cỏ + lối đi -->
  <rect x="0" y="{CHAN_TROI}" width="1080" height="{VUNG_CHU - CHAN_TROI}" fill="url(#s3co)"/>
  <path d="M436,{CHAN_TROI} L612,{CHAN_TROI} L742,{VUNG_CHU} L300,{VUNG_CHU} Z" fill="url(#s3loi)"/>

  {_cay(146, CHAN_TROI + 16, 1.15, "s3mo")}
  {_cay(392, CHAN_TROI - 6, 0.5, "s3mo2", xa=True)}
  {_cay(1020, CHAN_TROI + 24, 1.0, "s3mo")}

  <!-- chim -->
  <g stroke="#4B6B60" stroke-width="4" fill="none" opacity="0.7" stroke-linecap="round">
    <path d="M640,150 C650,140 658,140 668,150"/>
    <path d="M676,124 C684,116 691,116 699,124"/>
  </g>
"""


def canh_ben_mua() -> str:
    """Trạm chờ xe trời mưa — cho câu chuyện che mưa, giúp người lạ."""
    rem = "".join(
        f'<path d="M{x},{y} l16,{d}" stroke="#D7E7E2" stroke-width="3.5" stroke-linecap="round" opacity="{o}"/>'
        for x, y, d, o in (
            (70, 40, 120, 0.5), (250, 10, 150, 0.35), (420, 80, 110, 0.5), (600, 20, 140, 0.3),
            (770, 70, 120, 0.45), (940, 30, 150, 0.35), (1020, 180, 110, 0.5), (150, 210, 130, 0.4),
            (330, 250, 110, 0.3), (520, 190, 140, 0.45), (690, 240, 120, 0.35), (880, 210, 130, 0.4),
            (40, 380, 120, 0.3), (400, 420, 110, 0.3), (760, 400, 120, 0.28),
        )
    )
    return f"""
  <defs>
    <linearGradient id="s4troi" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="#446A78"/><stop offset="100%" stop-color="#43706A"/>
    </linearGradient>
    <linearGradient id="s4duong" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="#52736C"/><stop offset="100%" stop-color="#3D5A54"/>
    </linearGradient>
    <filter id="s4mo" x="-60%" y="-60%" width="220%" height="220%"><feGaussianBlur stdDeviation="16"/></filter>
    <filter id="s4mo2" x="-60%" y="-60%" width="220%" height="220%"><feGaussianBlur stdDeviation="6"/></filter>
  </defs>
  <rect width="1080" height="1080" fill="url(#s4troi)"/>

  <!-- nhà xa mờ trong mưa -->
  <g opacity="0.35" filter="url(#s4mo2)">
    <rect x="60" y="360" width="150" height="240" fill="#20423E"/>
    <rect x="230" y="410" width="120" height="190" fill="#1C3B37"/>
    <rect x="900" y="390" width="140" height="210" fill="#20423E"/>
  </g>

  <!-- trạm chờ -->
  <path d="M96,286 L700,286 L742,336 L58,336 Z" fill="#2C5648"/>
  <path d="M96,286 L700,286 L694,300 L104,300 Z" fill="#3B6D5B"/>
  <rect x="126" y="336" width="16" height="{CHAN_TROI - 336}" fill="#43705F"/>
  <rect x="660" y="336" width="16" height="{CHAN_TROI - 336}" fill="#43705F"/>
  <rect x="186" y="382" width="220" height="150" rx="8" fill="#DCE9E4" opacity="0.16"/>
  <rect x="186" y="382" width="220" height="150" rx="8" fill="none" stroke="#DCE9E4" stroke-width="4" opacity="0.3"/>
  <!-- ghế chờ -->
  <rect x="196" y="546" width="230" height="14" rx="6" fill="#5A8272"/>
  <rect x="212" y="560" width="12" height="40" fill="#4A6E60"/>
  <rect x="400" y="560" width="12" height="40" fill="#4A6E60"/>

  <!-- đường ướt + vũng nước phản chiếu -->
  <rect x="0" y="{CHAN_TROI}" width="1080" height="{VUNG_CHU - CHAN_TROI}" fill="url(#s4duong)"/>
  <ellipse cx="330" cy="{CHAN_TROI + 46}" rx="210" ry="28" fill="#CFE3DE" opacity="0.16" filter="url(#s4mo2)"/>
  <ellipse cx="820" cy="{CHAN_TROI + 66}" rx="150" ry="20" fill="#CFE3DE" opacity="0.12" filter="url(#s4mo2)"/>

  {rem}
"""


def canh_bep() -> str:
    """Bồn rửa trong bếp — cho nội dung 'làm một việc nhỏ'."""
    gach = "".join(
        f'<rect x="{x}" y="{y}" width="122" height="82" rx="6" fill="{KEM}" opacity="0.07"/>'
        for y in (150, 242, 334)
        for x in range(40, 1040, 132)
    )
    return f"""
  <defs>
    <linearGradient id="s5tuong" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="#51937A"/><stop offset="100%" stop-color="#28533F"/>
    </linearGradient>
    <linearGradient id="s5ban" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="#E6E1D4"/><stop offset="100%" stop-color="#C9C3B4"/>
    </linearGradient>
    <filter id="s5mo" x="-60%" y="-60%" width="220%" height="220%"><feGaussianBlur stdDeviation="16"/></filter>
    <filter id="s5mo2" x="-60%" y="-60%" width="220%" height="220%"><feGaussianBlur stdDeviation="6"/></filter>
  </defs>
  <rect width="1080" height="1080" fill="url(#s5tuong)"/>
  {gach}
  <ellipse cx="240" cy="200" rx="260" ry="200" fill="{KEM}" opacity="0.1" filter="url(#s5mo)"/>

  <!-- mặt bếp -->
  <rect x="0" y="{CHAN_TROI - 60}" width="1080" height="{VUNG_CHU - CHAN_TROI + 60}" fill="url(#s5ban)"/>
  <rect x="0" y="{CHAN_TROI - 60}" width="1080" height="12" fill="{KEM}" opacity="0.9"/>

  <!-- bồn rửa chìm + vòi -->
  <rect x="150" y="{CHAN_TROI - 40}" width="330" height="120" rx="14" fill="#9AA39B"/>
  <rect x="166" y="{CHAN_TROI - 28}" width="298" height="96" rx="10" fill="#79857D"/>
  <ellipse cx="315" cy="{CHAN_TROI + 30}" rx="120" ry="26" fill="#5F6C64" opacity="0.6"/>
  <path d="M300,{CHAN_TROI - 60} V 468 C300,430 392,430 392,470 V 516" fill="none"
        stroke="#DDE3DA" stroke-width="15" stroke-linecap="round"/>
  <circle cx="392" cy="524" r="9" fill="#DDE3DA"/>

  <!-- chồng bát + khăn -->
  {_bong(650, CHAN_TROI - 52, 76, 12, "s5mo2", 0.3)}
  <g transform="translate(650 {CHAN_TROI - 58})">
    <ellipse cx="0" cy="0" rx="70" ry="18" fill="#EFF3EC"/>
    <ellipse cx="0" cy="-24" rx="62" ry="16" fill="{LA_NHAT}"/>
    <ellipse cx="0" cy="-46" rx="54" ry="14" fill="#EFF3EC"/>
    <ellipse cx="0" cy="-64" rx="44" ry="12" fill="#D9E3D6"/>
  </g>
  <path d="M40,{CHAN_TROI - 60} C70,{CHAN_TROI - 20} 30,{CHAN_TROI + 20} 60,{VUNG_CHU - 10} L0,{VUNG_CHU - 10} Z"
        fill="#8FBBA2" opacity="0.85"/>
"""


def canh_dem_sao() -> str:
    """Trời đêm nhiều sao — cho nội dung nghỉ ngơi, dịu lại, tha thứ."""
    sao = "".join(
        f'<circle cx="{x}" cy="{y}" r="{r}" fill="{KEM}" opacity="{o}"/>'
        for x, y, r, o in (
            (120, 110, 3.4, 0.9), (260, 200, 2.6, 0.7), (398, 84, 3.2, 0.85), (520, 250, 2.2, 0.6),
            (640, 130, 3.6, 0.9), (780, 230, 2.8, 0.7), (930, 100, 3.2, 0.85), (1010, 290, 2.4, 0.6),
            (180, 320, 2.8, 0.7), (700, 350, 2.2, 0.55), (330, 400, 2.4, 0.5), (860, 400, 2.6, 0.55),
        )
    )
    return f"""
  <defs>
    <linearGradient id="s6troi" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="#1B3F55"/><stop offset="60%" stop-color="#255460"/>
      <stop offset="100%" stop-color="#316552"/>
    </linearGradient>
    <filter id="s6mo" x="-60%" y="-60%" width="220%" height="220%"><feGaussianBlur stdDeviation="20"/></filter>
    <filter id="s6mo2" x="-60%" y="-60%" width="220%" height="220%"><feGaussianBlur stdDeviation="7"/></filter>
  </defs>
  <rect width="1080" height="1080" fill="url(#s6troi)"/>
  {sao}

  <!-- trăng khuyết + hào quang -->
  <circle cx="250" cy="180" r="130" fill="{VANG}" opacity="0.16" filter="url(#s6mo)"/>
  <path d="M292,214 A 64,64 0 1,1 232,146 A 52,52 0 1,0 292,214 Z" fill="#F6E7B4"/>

  <!-- mái nhà lớp xa rồi lớp gần -->
  <g opacity="0.5">
    <path d="M0,520 L120,452 L240,520 L240,{CHAN_TROI} L0,{CHAN_TROI} Z" fill="#1D4451"/>
    <path d="M860,540 L980,470 L1080,540 L1080,{CHAN_TROI} L860,{CHAN_TROI} Z" fill="#1D4451"/>
  </g>
  <path d="M60,570 L230,470 L400,570 L400,{CHAN_TROI} L60,{CHAN_TROI} Z" fill="#1E4239"/>
  <rect x="150" y="524" width="52" height="44" rx="6" fill="{VANG}" opacity="0.8"/>
  <rect x="0" y="{CHAN_TROI}" width="1080" height="{VUNG_CHU - CHAN_TROI}" fill="#1B3E34"/>
  <ellipse cx="200" cy="{CHAN_TROI + 30}" rx="230" ry="30" fill="{VANG}" opacity="0.1" filter="url(#s6mo2)"/>
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
