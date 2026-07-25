"""Bộ nhân vật minh hoạ của kênh Sống Tốt — vẽ vector, không dùng ảnh người thật.

Vì sao vẽ: ảnh/video người thật lấy trên mạng là rủi ro bản quyền lớn nhất với
một Page đang chuẩn bị bật kiếm tiền. Nhân vật vẽ là của kênh, dùng mãi được.

Khung là **chân dung nửa người** (đầu + vai) chứ không phải người tí hon đứng xa
— để mặt đủ lớn mà thấy được mắt, miệng, nếp nhăn, tức là trông "thật" hơn.

Bốn nhân vật:
    anh — đàn ông trẻ · chi — phụ nữ trẻ · chu — đàn ông lớn tuổi · co — phụ nữ lớn tuổi

Toạ độ nội bộ: gốc (0,0) là đáy phần thân thấy được; nhân vật cao lên phía y âm,
đỉnh đầu khoảng y = -440. Ghép vào khung bằng translate + scale.
"""

from __future__ import annotations

MAT_TRANG = "#F6F1EA"
TRONG_MAT = "#3A2A22"
MOI = "#B4675F"
MOI_TOI = "#8E4A45"
VIEN = "#00000022"

KIEU = {
    "anh": {
        "da": ("#F2CDA7", "#D9A478"), "toc": "#241A15", "kieu_toc": "ngan",
        "ao": ("#EEF3EA", "#C9D6C7"), "co_ao": "so-mi", "gia": False, "kinh": False,
    },
    "chi": {
        "da": ("#F6D3B0", "#DDA980"), "toc": "#2A1C16", "kieu_toc": "dai",
        "ao": ("#A9D4A6", "#7BAE7F"), "co_ao": "tron", "gia": False, "kinh": False,
    },
    "chu": {
        "da": ("#EDC8A4", "#CE9E76"), "toc": "#C7CDC8", "kieu_toc": "ngan",
        "ao": ("#9EC7A2", "#74A279"), "co_ao": "so-mi", "gia": True, "kinh": True,
    },
    "co": {
        "da": ("#F2CFAE", "#D4A47D"), "toc": "#D3D8D3", "kieu_toc": "bui",
        "ao": ("#F2F5F0", "#CFDACD"), "co_ao": "tron", "gia": True, "kinh": True,
    },
}


def _mat(x: int, mo: float = 1.0) -> str:
    """Một con mắt: lòng trắng hình hạt, con ngươi, đốm sáng, mi trên."""
    return f"""
    <g transform="translate({x} -360)">
      <path d="M-19,0 C-13,-13 13,-13 19,0 C13,11 -13,11 -19,0 Z" fill="{MAT_TRANG}"/>
      <circle cx="0" cy="-1" r="9.5" fill="{TRONG_MAT}"/>
      <circle cx="0" cy="-1" r="4.2" fill="#140D0A"/>
      <circle cx="-3.4" cy="-4.4" r="2.8" fill="#FFFFFF" opacity="0.9"/>
      <path d="M-19,0 C-13,-13 13,-13 19,0" fill="none" stroke="#3A2A22" stroke-width="3.4"
            stroke-linecap="round" opacity="{mo}"/>
    </g>"""


def _mieng(mo: bool, gia: bool) -> str:
    """Miệng đóng (nét môi) hoặc mở (đang nói) — hai trạng thái đổi qua lại tạo động tác nói."""
    y = -292 if not gia else -288
    if not mo:
        return f"""
    <g transform="translate(0 {y})">
      <path d="M-25,0 C-16,-7 -6,-4 0,-3 C6,-4 16,-7 25,0 C16,8 -16,8 -25,0 Z" fill="{MOI}"/>
      <path d="M-25,0 C-14,2 14,2 25,0" fill="none" stroke="{MOI_TOI}" stroke-width="2.4" opacity="0.7"/>
    </g>"""
    return f"""
    <g transform="translate(0 {y})">
      <path d="M-23,-2 C-14,-11 14,-11 23,-2 C16,14 -16,14 -23,-2 Z" fill="#6E3230"/>
      <path d="M-18,-3 C-10,-8 10,-8 18,-3 C10,-1 -10,-1 -18,-3 Z" fill="{MAT_TRANG}" opacity="0.92"/>
      <path d="M-23,-2 C-14,-11 14,-11 23,-2" fill="none" stroke="{MOI_TOI}" stroke-width="2.6"/>
    </g>"""


def _toc(kieu: str, mau: str) -> tuple[str, str]:
    """Trả về (lớp tóc phía sau đầu, lớp tóc phía trước)."""
    # Tóc phải trùm cao hơn và rộng hơn hộp sọ (đỉnh đầu ở y=-452, hai bên x=±80)
    # nếu không sẽ trông như đội mũ chật / hói.
    if kieu == "dai":
        sau = (
            f'<path d="M-92,-356 C-110,-250 -104,-160 -88,-124 L88,-124 '
            f'C104,-160 110,-250 92,-356 Z" fill="{mau}"/>'
        )
        # Chân tóc nằm TRÊN đường mày (mày ở y≈-396), không thì tóc che mất mắt
        truoc = (
            f'<path d="M-90,-344 C-112,-528 112,-528 90,-344 '
            f'C78,-402 40,-418 8,-416 C-26,-412 -66,-390 -90,-344 Z" fill="{mau}"/>'
            f'<path d="M8,-416 C-32,-410 -70,-386 -86,-340 C-96,-378 -84,-414 -56,-432 Z" fill="{mau}"/>'
        )
        return sau, truoc
    if kieu == "bui":
        sau = f'<ellipse cx="4" cy="-462" rx="42" ry="36" fill="{mau}"/>'
        truoc = (
            f'<path d="M-88,-346 C-108,-524 108,-524 88,-346 '
            f'C70,-410 -70,-410 -88,-346 Z" fill="{mau}"/>'
            f'<path d="M-88,-346 C-84,-390 -70,-414 -44,-428" fill="none" stroke="{mau}" '
            f'stroke-width="14" stroke-linecap="round"/>'
        )
        return sau, truoc
    # tóc ngắn
    sau = ""
    truoc = (
        f'<path d="M-88,-340 C-110,-526 110,-526 88,-340 '
        f'C70,-400 32,-416 0,-414 C-32,-414 -70,-392 -88,-340 Z" fill="{mau}"/>'
        f'<path d="M0,-414 C-28,-410 -60,-390 -80,-344 C-88,-382 -64,-410 -30,-422 Z" fill="{mau}"/>'
    )
    return sau, truoc


def ve_nhan_vat(loai: str, mieng_mo: bool = False) -> str:
    """Trả về nhóm <g> SVG vẽ nhân vật. mieng_mo=True cho khung 'đang nói'."""
    if loai not in KIEU:
        raise ValueError(f"Không có nhân vật '{loai}'. Chọn: {', '.join(KIEU)}")
    k = KIEU[loai]
    da_sang, da_toi = k["da"]
    ao_sang, ao_toi = k["ao"]
    toc_sau, toc_truoc = _toc(k["kieu_toc"], k["toc"])
    p = f"nv{loai}"   # tiền tố id cho khỏi trùng với id của cảnh nền

    # Cổ áo
    if k["co_ao"] == "so-mi":
        co_ao = f"""
    <path d="M-30,-208 L0,-150 L30,-208 L54,-196 L0,-120 L-54,-196 Z" fill="{da_toi}" opacity="0.35"/>
    <path d="M-30,-208 L-2,-152 L-26,-140 L-62,-186 Z" fill="{ao_sang}"/>
    <path d="M30,-208 L2,-152 L26,-140 L62,-186 Z" fill="{ao_sang}"/>
    <path d="M-2,-150 L2,-150 L6,0 L-6,0 Z" fill="{ao_toi}" opacity="0.45"/>
    <circle cx="0" cy="-96" r="5" fill="{ao_toi}"/>
    <circle cx="0" cy="-40" r="5" fill="{ao_toi}"/>"""
    else:
        co_ao = f"""
    <path d="M-44,-196 C-30,-160 30,-160 44,-196 C30,-176 -30,-176 -44,-196 Z" fill="{da_toi}" opacity="0.4"/>
    <path d="M-52,-192 C-34,-148 34,-148 52,-192" fill="none" stroke="{ao_toi}" stroke-width="6" opacity="0.5"/>"""

    # Nếp nhăn cho nhân vật lớn tuổi
    nep_nhan = ""
    if k["gia"]:
        nep_nhan = f"""
    <g fill="none" stroke="{da_toi}" stroke-width="3" opacity="0.55" stroke-linecap="round">
      <path d="M-34,-404 C-20,-412 -6,-412 4,-406"/>
      <path d="M-30,-390 C-16,-398 -2,-398 8,-392"/>
      <path d="M-52,-344 C-58,-336 -58,-330 -54,-324"/>
      <path d="M52,-344 C58,-336 58,-330 54,-324"/>
      <path d="M-30,-318 C-38,-306 -40,-296 -34,-286"/>
      <path d="M30,-318 C38,-306 40,-296 34,-286"/>
    </g>"""

    kinh = ""
    if k["kinh"]:
        kinh = f"""
    <g fill="#FFFFFF" fill-opacity="0.1" stroke="#3B3B3B" stroke-width="4.6" stroke-linejoin="round">
      <rect x="-62" y="-382" width="60" height="46" rx="18"/>
      <rect x="2" y="-382" width="60" height="46" rx="18"/>
    </g>
    <g fill="none" stroke="#3B3B3B" stroke-width="4.6" stroke-linecap="round">
      <path d="M-2,-364 H2"/><path d="M-62,-368 L-80,-360"/><path d="M62,-368 L80,-360"/>
    </g>"""

    return f"""<g>
  <defs>
    <radialGradient id="{p}da" cx="34%" cy="26%" r="78%">
      <stop offset="0%" stop-color="{da_sang}"/><stop offset="100%" stop-color="{da_toi}"/>
    </radialGradient>
    <linearGradient id="{p}ao" x1="0%" y1="0%" x2="90%" y2="100%">
      <stop offset="0%" stop-color="{ao_sang}"/><stop offset="100%" stop-color="{ao_toi}"/>
    </linearGradient>
    <filter id="{p}mo" x="-60%" y="-60%" width="220%" height="220%">
      <feGaussianBlur stdDeviation="12"/>
    </filter>
    <!-- Bóng mờ phải bị cắt theo hình thân và hình đầu, không thì tràn ra ngoài thành viền sáng -->
    <clipPath id="{p}than">
      <path d="M-152,0 C-148,-104 -104,-168 -58,-196 L58,-196 C104,-168 148,-104 152,0 Z"/>
    </clipPath>
    <clipPath id="{p}dau">
      <path d="M-80,-368 C-80,-436 -46,-452 0,-452 C46,-452 80,-436 80,-368
               C80,-306 44,-250 0,-250 C-44,-250 -80,-306 -80,-368 Z"/>
    </clipPath>
  </defs>

  {toc_sau}

  <!-- vai và thân -->
  <path d="M-152,0 C-148,-104 -104,-168 -58,-196 L58,-196 C104,-168 148,-104 152,0 Z" fill="url(#{p}ao)"/>
  <g clip-path="url(#{p}than)">
    <ellipse cx="-124" cy="-40" rx="46" ry="90" fill="{ao_toi}" opacity="0.4" filter="url(#{p}mo)"/>
    <ellipse cx="128" cy="-30" rx="40" ry="90" fill="{ao_toi}" opacity="0.3" filter="url(#{p}mo)"/>
  </g>

  <!-- cổ -->
  <path d="M-28,-200 L28,-200 L34,-244 L-34,-244 Z" fill="{da_toi}"/>
  <ellipse cx="0" cy="-244" rx="44" ry="20" fill="#000000" opacity="0.2" filter="url(#{p}mo)"/>

  {co_ao}

  <!-- tai -->
  <ellipse cx="-79" cy="-344" rx="13" ry="21" fill="{da_toi}"/>
  <ellipse cx="79" cy="-344" rx="13" ry="21" fill="{da_toi}"/>

  <!-- đầu -->
  <path d="M-80,-368 C-80,-436 -46,-452 0,-452 C46,-452 80,-436 80,-368
           C80,-306 44,-250 0,-250 C-44,-250 -80,-306 -80,-368 Z" fill="url(#{p}da)"/>
  <!-- má hồng + bóng hai bên mặt (cắt trong hình đầu) -->
  <g clip-path="url(#{p}dau)">
    <ellipse cx="-50" cy="-318" rx="24" ry="13" fill="#E08D7A" opacity="0.32" filter="url(#{p}mo)"/>
    <ellipse cx="50" cy="-318" rx="24" ry="13" fill="#E08D7A" opacity="0.32" filter="url(#{p}mo)"/>
    <ellipse cx="-86" cy="-350" rx="26" ry="60" fill="{da_toi}" opacity="0.45" filter="url(#{p}mo)"/>
  </g>

  <!-- mày -->
  <g fill="none" stroke="{k['toc']}" stroke-width="7" stroke-linecap="round" opacity="0.95">
    <path d="M-48,-392 C-38,-400 -20,-400 -12,-394"/>
    <path d="M12,-394 C20,-400 38,-400 48,-392"/>
  </g>

  {_mat(-32)}{_mat(32)}

  <!-- mũi -->
  <path d="M0,-352 C-6,-330 -10,-320 -2,-314 C4,-311 10,-314 12,-320" fill="none"
        stroke="{da_toi}" stroke-width="4" stroke-linecap="round" opacity="0.85"/>

  {_mieng(mieng_mo, k['gia'])}
  {nep_nhan}
  {toc_truoc}
  {kinh}
</g>"""
