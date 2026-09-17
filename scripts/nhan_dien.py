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
    "sang": ("#57A184", "#3C765D", "#16382A", 0.55),   # tươi — nội dung nhẹ nhàng
    "vua": ("#3C765D", "#8FC293", "#16382A", 0.58),    # mặc định
    "tram": ("#2A5B49", "#3C765D", "#123326", 0.55),   # dịu — nội dung an ủi
}
KEM = "#F7FAF5"       # trắng ngà — chữ chính
VANG = "#E9C46A"      # vàng nắng — điểm nhấn
LA_NHAT = "#A9D4A6"   # xanh lá nhạt — nửa lá logo

# ── Nền SÁNG — riêng cho ảnh chữ đăng Facebook ────────────────────────────────
# Vì sao có bảng này: đọc API 18/09 thấy Page thời 2019 đăng **ảnh chữ nền sáng,
# chữ đen, từ khoá tô màu** thì được 419 thích/bài (bài top 4.429 thích · 390 chia
# sẻ). Từ 2026 đổi sang video dọc thì còn 1,5 thích/bài. Bảng này lấy lại lối trình
# bày đã chạy với chính tệp người theo dõi đó, nhưng **giữ logo và giọng chữ của dự
# án** — không bắt chước giọng self-help của mấy trang châm ngôn.
#
# Mỗi mục: (nền trên, nền dưới, màu chữ, màu nhấn)
TONES_SANG = {
    "kem":     ("#FCF7EC", "#F4E9D4", "#2B2B2B", "#C0392B"),
    "hong":    ("#FDF1F1", "#F7DFDF", "#2B2B2B", "#C0392B"),
    "xanh":    ("#EEF4FB", "#DCE8F5", "#22303F", "#2E5FA3"),
    "bac_ha":  ("#EEF7F2", "#DAEDE3", "#1F3A2E", "#1B7A55"),
}
# Logo trên nền sáng phải đổi màu, không thì mất hút.
XANH_DAM = "#1E5140"
FONT = "'Be Vietnam Pro','Montserrat',Arial,sans-serif"
CTA = "theo dõi để sống tốt mỗi ngày"

LOGO = f"""  <g transform="translate(60 70)">
    <g transform="scale(0.28)">
      <path d="M0,60 C -48,30 -48,-75 -7,-116 C -3,-95 -9,-35 0,60 Z" fill="{KEM}" transform="rotate(-16)"/>
      <path d="M0,60 C 48,30 48,-75 7,-116 C 3,-95 9,-35 0,60 Z" fill="{LA_NHAT}" transform="rotate(16)"/>
    </g>
    <text x="52" y="18" font-family="{FONT}" font-size="42" font-weight="800" fill="{KEM}">Sống Tốt</text>
  </g>"""


def logo_sang(mau_chu: str) -> str:
    """Logo cho nền sáng — cùng hình, đổi màu để không mất hút trên nền nhạt."""
    return f"""  <g transform="translate(60 70)">
    <g transform="scale(0.28)">
      <path d="M0,60 C -48,30 -48,-75 -7,-116 C -3,-95 -9,-35 0,60 Z" fill="{XANH_DAM}" transform="rotate(-16)"/>
      <path d="M0,60 C 48,30 48,-75 7,-116 C 3,-95 9,-35 0,60 Z" fill="#6FA97F" transform="rotate(16)"/>
    </g>
    <text x="52" y="18" font-family="{FONT}" font-size="42" font-weight="800" fill="{mau_chu}">Sống Tốt</text>
  </g>"""


def tach_nhan(dong: str) -> list[tuple[str, bool]]:
    """Tách một dòng thành các mảnh (chữ, có_tô_màu_không).

    Đánh dấu từ khoá bằng dấu sao: "cái bạn *sợ nhất*" → phần trong sao được tô.
    Lối này chép từ ảnh 2019 của Page: câu chữ màu đen, chỉ vài từ khoá tô đỏ hoặc
    xanh — mắt bắt được ý chính trong một giây khi lướt.
    """
    mieng: list[tuple[str, bool]] = []
    for i, phan in enumerate(dong.split("*")):
        if phan:
            mieng.append((phan, i % 2 == 1))
    return mieng or [("", False)]


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


def tao_the_video(
    dong: list[str],
    canh: str,
    nhan_vat: str | None = None,
    mieng_mo: bool = False,
) -> str:
    """Dựng một thẻ chữ cho video — khung chia làm hai vùng, không lộn xộn vào nhau:

        0    → 690   VÙNG HÌNH: cảnh nền + nhân vật (chân dung, lệch phải)
        690  → 1080  VÙNG CHỮ : chỉ có chữ, nền phủ đều, lề trái phải 90px

    dong      : các dòng chữ (đã ngắt sẵn, tối đa 4 dòng)
    canh      : tên cảnh trong canh_nen.CANH
    nhan_vat  : 'anh' | 'chi' | 'chu' | 'co' | None (không có người)
    mieng_mo  : True/False — hai trạng thái đổi qua lại tạo động tác đang nói
    """
    import canh_nen
    import nhan_vat as nv

    vc = canh_nen.VUNG_CHU
    nen = canh_nen.ve_canh(canh)

    nguoi = ""
    if nhan_vat:
        # Chân dung nửa người, đáy thân trùng đúng mép vùng chữ → không cắt lửng lơ
        nguoi = (
            f'  <g clip-path="url(#vung-hinh)">'
            f'<g transform="translate(830 {vc}) scale(0.98)">'
            f"{nv.ve_nhan_vat(nhan_vat, mieng_mo)}</g></g>"
        )

    co = co_chu(dong)
    buoc = int(co * 1.32)
    tam = vc + (1080 - vc) // 2 + 6      # giữa vùng chữ, nhích xuống một chút cho cân mắt
    dau_khoi = tam - (len(dong) - 1) * buoc // 2
    khoi_chu = "\n".join(
        f'  <text x="540" y="{dau_khoi + i * buoc}" text-anchor="middle" '
        f'font-family="{FONT}" font-size="{co}" font-weight="800" fill="{KEM}">{escape(d)}</text>'
        for i, d in enumerate(dong)
    )

    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="1080" height="1080" viewBox="0 0 1080 1080">
  <defs>
    <clipPath id="vung-hinh"><rect x="0" y="0" width="1080" height="{vc}"/></clipPath>
    <linearGradient id="chuyen-vung" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="#1E5140" stop-opacity="0"/>
      <stop offset="100%" stop-color="#1E5140" stop-opacity="0.9"/>
    </linearGradient>
  </defs>

  <g clip-path="url(#vung-hinh)">
{nen}
  </g>
{nguoi}

  <!-- chuyển tiếp mềm giữa hai vùng, cho khỏi thành đường cắt gắt -->
  <rect x="0" y="{vc - 90}" width="1080" height="90" fill="url(#chuyen-vung)"/>
  <!-- VÙNG CHỮ: nền phủ kín, không có chi tiết cảnh nào lọt vào -->
  <rect x="0" y="{vc}" width="1080" height="{1080 - vc}" fill="#1E5140"/>
  <rect x="0" y="{vc}" width="1080" height="4" fill="{VANG}" opacity="0.75"/>

  <!-- nền mờ sau logo để đọc được cả trên cảnh trời sáng -->
  <rect x="34" y="34" width="300" height="76" rx="38" fill="#1E5140" opacity="0.45"/>
{LOGO}

{khoi_chu}
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


def tao_svg_sang(
    dong: list[str],
    tone: str = "kem",
    kicker: str | None = None,
    cta: bool = True,
) -> str:
    """Ảnh chữ 1:1 nền SÁNG — dành riêng cho Facebook.

    Khác `tao_svg` ở ba chỗ, và cả ba đều là chỗ ảnh 2019 của Page làm được:
      1. Nền sáng, chữ đen — dễ đọc trên nền trắng của bảng tin Facebook.
      2. **Từ khoá tô màu** — đánh dấu bằng dấu sao trong chuỗi, xem `tach_nhan`.
      3. Khối chữ nằm giữa khung, không dồn xuống đáy như ảnh quote nền tối.

    Vẫn giữ logo và dòng CTA của dự án để người xem nhận ra cùng một kênh.
    """
    nen_tren, nen_duoi, mau_chu, mau_nhan = TONES_SANG[tone]
    # Đo cỡ chữ trên chuỗi ĐÃ BỎ dấu sao — dấu sao chỉ là ký hiệu đánh dấu, không
    # hiện trên ảnh. Tính cả nó thì câu có nhiều từ tô màu bị co chữ nhỏ vô cớ.
    co = co_chu([d.replace("*", "") for d in dong])
    buoc = int(co * 1.42)
    dau_khoi = 592 - (len(dong) - 1) * buoc // 2
    if kicker:
        dau_khoi += 40

    hang = []
    for i, d in enumerate(dong):
        mieng = "".join(
            f'<tspan fill="{mau_nhan if to else mau_chu}"'
            f'{" font-weight=\"800\"" if to else ""}>{escape(chu)}</tspan>'
            for chu, to in tach_nhan(d)
        )
        hang.append(
            # xml:space="preserve" — thiếu nó thì SVG nuốt dấu cách đứng ngay trước
            # <tspan>, ra "cáibạn sợ nhất". Đã dính đúng lỗi này lần dựng đầu tiên.
            f'  <text x="540" y="{dau_khoi + i * buoc}" text-anchor="middle" '
            f'xml:space="preserve" font-family="{FONT}" font-size="{co}" '
            f'font-weight="600" fill="{mau_chu}">{mieng}</text>'
        )
    khoi_chu = "\n".join(hang)

    tren = ""
    if kicker:
        tren = (
            f'  <text x="540" y="{dau_khoi - buoc - 40}" text-anchor="middle" '
            f'font-family="{FONT}" font-size="86" font-weight="800" '
            f'fill="{mau_nhan}" letter-spacing="4">{escape(kicker)}</text>'
        )

    y_vach = dau_khoi + (len(dong) - 1) * buoc + int(co * 1.05)
    vach = f'  <rect x="495" y="{y_vach}" width="90" height="6" rx="3" fill="{mau_nhan}" opacity="0.75"/>'

    dong_cta = (
        f'  <text x="540" y="1004" text-anchor="middle" font-family="{FONT}" font-size="32" '
        f'font-weight="600" fill="{mau_chu}" opacity="0.55" letter-spacing="3">{CTA}</text>'
        if cta
        else ""
    )

    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="1080" height="1080" viewBox="0 0 1080 1080">
  <defs>
    <linearGradient id="bg" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="{nen_tren}"/>
      <stop offset="100%" stop-color="{nen_duoi}"/>
    </linearGradient>
  </defs>

  <rect width="1080" height="1080" fill="url(#bg)"/>
  <rect x="44" y="44" width="992" height="992" fill="none" stroke="{mau_nhan}" stroke-opacity="0.28" stroke-width="3" rx="10"/>

{logo_sang(mau_chu)}

{tren}

{khoi_chu}

{vach}

{dong_cta}
</svg>
"""
