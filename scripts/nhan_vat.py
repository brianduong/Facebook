"""Bộ nhân vật minh hoạ của kênh Sống Tốt — vẽ bằng vector, không dùng ảnh người thật.

Vì sao vẽ vector: ảnh/video người thật lấy trên mạng là rủi ro bản quyền lớn nhất
với một Page đang chuẩn bị bật kiếm tiền. Nhân vật vẽ là của mình, dùng mãi được.

Bốn nhân vật (gọi theo cách người Việt gọi nhau):
    anh  — đàn ông trẻ
    chi  — phụ nữ trẻ
    chu  — đàn ông lớn tuổi
    co   — phụ nữ lớn tuổi

Toạ độ: gốc (0,0) là chỗ chân đứng, người cao khoảng 400px hướng lên (y âm).
Ghép vào khung bằng transform translate(x y) scale(s).
"""

from __future__ import annotations

DA = "#E9BE97"        # màu da
DA_TOI = "#D9A87F"    # bóng da
MAT = "#2B3A33"
MOI = "#8A4A44"

# ao = áo, quan = quần, toc = tóc, kinh = có đeo kính không
KIEU = {
    "anh": {"ao": "#F7FAF5", "quan": "#2B4A3C", "toc": "#2B2B2B", "kinh": False, "toc_dai": False, "bun": False},
    "chi": {"ao": "#A9D4A6", "quan": "#2B4A3C", "toc": "#3A2E28", "kinh": False, "toc_dai": True, "bun": False},
    "chu": {"ao": "#A9D4A6", "quan": "#3A3A3A", "toc": "#C9CFCB", "kinh": True, "toc_dai": False, "bun": False},
    "co": {"ao": "#F7FAF5", "quan": "#3A3A3A", "toc": "#C9CFCB", "kinh": True, "toc_dai": False, "bun": True},
}


def ve_nhan_vat(loai: str, mieng_mo: bool = False) -> str:
    """Trả về một nhóm <g> SVG vẽ nhân vật. mieng_mo=True để làm động tác đang nói."""
    if loai not in KIEU:
        raise ValueError(f"Không có nhân vật '{loai}'. Chọn: {', '.join(KIEU)}")
    k = KIEU[loai]
    ao, quan, toc = k["ao"], k["quan"], k["toc"]

    # Tóc dài vẽ TRƯỚC đầu để nằm phía sau
    toc_sau = ""
    if k["toc_dai"]:
        toc_sau = f'<path d="M-52,-330 C -60,-250 -50,-215 -40,-205 L 40,-205 C 50,-215 60,-250 52,-330 Z" fill="{toc}"/>'
    if k["bun"]:
        toc_sau = f'<circle cx="0" cy="-378" r="22" fill="{toc}"/>'

    mieng = (
        f'<ellipse cx="0" cy="-298" rx="10" ry="9" fill="{MOI}"/>'
        if mieng_mo
        else f'<path d="M-11,-301 Q0,-293 11,-301" stroke="{MOI}" stroke-width="5" fill="none" stroke-linecap="round"/>'
    )

    kinh = ""
    if k["kinh"]:
        kinh = (
            f'<g stroke="{MAT}" stroke-width="4" fill="none">'
            f'<circle cx="-17" cy="-329" r="15"/><circle cx="17" cy="-329" r="15"/>'
            f'<path d="M-2,-329 H2"/><path d="M-32,-332 H-42"/><path d="M32,-332 H42"/></g>'
        )

    # Tóc trước (phần trên đầu) — mỗi kiểu một dáng
    if k["toc_dai"]:
        toc_truoc = f'<path d="M-47,-336 C -44,-382 44,-382 47,-336 C 30,-360 -30,-360 -47,-336 Z" fill="{toc}"/>'
    elif k["bun"]:
        toc_truoc = f'<path d="M-46,-338 C -42,-378 42,-378 46,-338 C 26,-356 -26,-356 -46,-338 Z" fill="{toc}"/>'
    else:
        toc_truoc = f'<path d="M-47,-334 C -46,-384 46,-384 47,-334 C 24,-352 -24,-352 -47,-334 Z" fill="{toc}"/>'

    return f"""<g>
    {toc_sau}
    <!-- chân -->
    <rect x="-34" y="-124" width="27" height="124" rx="13" fill="{quan}"/>
    <rect x="7" y="-124" width="27" height="124" rx="13" fill="{quan}"/>
    <!-- thân -->
    <path d="M-54,-240 C -54,-268 -30,-284 0,-284 C 30,-284 54,-268 54,-240 L 54,-118 L -54,-118 Z" fill="{ao}"/>
    <!-- tay -->
    <rect x="-76" y="-248" width="25" height="112" rx="12" fill="{ao}" transform="rotate(7 -63 -248)"/>
    <rect x="51" y="-248" width="25" height="112" rx="12" fill="{ao}" transform="rotate(-7 63 -248)"/>
    <circle cx="-70" cy="-134" r="13" fill="{DA}"/>
    <circle cx="70" cy="-134" r="13" fill="{DA}"/>
    <!-- cổ + đầu -->
    <rect x="-14" y="-292" width="28" height="26" fill="{DA_TOI}"/>
    <circle cx="0" cy="-330" r="47" fill="{DA}"/>
    {toc_truoc}
    <circle cx="-17" cy="-332" r="5" fill="{MAT}"/>
    <circle cx="17" cy="-332" r="5" fill="{MAT}"/>
    {kinh}
    {mieng}
  </g>"""
