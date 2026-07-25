#!/usr/bin/env python3
"""Xem thử nhân vật và cảnh nền trước khi render cả video.

    python3 scripts/xem-thu.py

Tạo ra:
    assets/images/nhan-vat-mau.png     — bảng 4 nhân vật để anh chọn
    video/edit/xem-thu/canh-*.png      — mỗi cảnh nền một khung mẫu (ngoài GitHub)
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import canh_nen  # noqa: E402
import nhan_dien as nd  # noqa: E402
import nhan_vat as nv  # noqa: E402

TEN_GOI = {
    "anh": "anh — đàn ông trẻ",
    "chi": "chị — phụ nữ trẻ",
    "chu": "chú — đàn ông lớn tuổi",
    "co": "cô — phụ nữ lớn tuổi",
}


def bang_nhan_vat() -> str:
    """Bảng 2x2 bốn nhân vật kèm tên gọi."""
    o = []
    for i, (loai, ten) in enumerate(TEN_GOI.items()):
        cx = 270 + (i % 2) * 540
        cy = 530 + (i // 2) * 450
        o.append(
            f'<g transform="translate({cx} {cy}) scale(0.72)">{nv.ve_nhan_vat(loai)}</g>'
            f'<text x="{cx}" y="{cy + 56}" text-anchor="middle" font-family="{nd.FONT}" '
            f'font-size="34" font-weight="800" fill="{nd.KEM}">{ten}</text>'
        )
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="1080" height="1080" viewBox="0 0 1080 1080">
  <defs>
    <linearGradient id="bg" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#2E5D4B"/><stop offset="100%" stop-color="#1E4437"/>
    </linearGradient>
  </defs>
  <rect width="1080" height="1080" fill="url(#bg)"/>
  <text x="540" y="110" text-anchor="middle" font-family="{nd.FONT}" font-size="52"
        font-weight="800" fill="{nd.KEM}">Nhân vật kênh Sống Tốt</text>
  <text x="540" y="162" text-anchor="middle" font-family="{nd.FONT}" font-size="30"
        font-weight="500" fill="{nd.VANG}">vẽ vector — không lo bản quyền hình người thật</text>
  {"".join(o)}
</svg>
"""


def main() -> int:
    anh_dir = nd.REPO / "assets" / "images"
    thu_dir = nd.REPO / "video" / "edit" / "xem-thu"
    thu_dir.mkdir(parents=True, exist_ok=True)

    svg = anh_dir / "nhan-vat-mau.svg"
    svg.write_text(bang_nhan_vat(), encoding="utf-8")
    nd.xuat_png(svg, anh_dir / "nhan-vat-mau.png")
    print(f"✅ {(anh_dir / 'nhan-vat-mau.png').relative_to(nd.REPO)}")

    mau = "Câu mẫu để xem chữ có dễ đọc trên cảnh này không."
    for ten in canh_nen.CANH:
        s = thu_dir / f"canh-{ten}.svg"
        s.write_text(
            nd.tao_the_video(nd.boc_dong(f"[{ten}] {mau}", 28), ten, nhan_vat="chi"),
            encoding="utf-8",
        )
        nd.xuat_png(s, thu_dir / f"canh-{ten}.png")
        print(f"✅ {(thu_dir / f'canh-{ten}.png').relative_to(nd.REPO)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
