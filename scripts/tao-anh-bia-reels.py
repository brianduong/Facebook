#!/usr/bin/env python3
"""Tạo ảnh bìa 9:16 cho Reels — lấy một ảnh nền của video + câu quote đè lên.

Ảnh quote cũ trong `assets/templates/quotes/` là khung vuông 1:1, lên Reels bị
cắt hai đầu. File này dựng bản dọc 1080×1920 đúng khung Reels, dùng cùng lớp chữ
với video nên bìa và video trông liền một bộ.

    python3 scripts/tao-anh-bia-reels.py VD-002 "Tử tế không bao giờ là lãng phí."
    python3 scripts/tao-anh-bia-reels.py VD-002 "..." --anh 5

Kết quả: video/thumbnails/VD-002-bia.png (ngoài GitHub)
Cần: ffmpeg, rsvg-convert.
"""

from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import khung_reels as kr  # noqa: E402

REPO = Path(__file__).resolve().parent.parent


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("ma", help="Mã video, vd VD-002")
    p.add_argument("quote", help="Câu chữ in trên bìa")
    p.add_argument("--anh", type=int, default=2,
                   help="Dùng ảnh nền thứ mấy của video (mặc định 2 — thường là ảnh đẹp nhất)")
    a = p.parse_args()

    thieu = [t for t in ("ffmpeg", "rsvg-convert") if not shutil.which(t)]
    if thieu:
        sys.exit(f"❌ Máy thiếu: {', '.join(thieu)}")

    thu_muc_anh = REPO / "assets" / "images" / "canh" / a.ma
    anh_ds = sorted(thu_muc_anh.glob("*.jpg"))
    if not anh_ds:
        sys.exit(f"❌ Chưa có ảnh nền ở {thu_muc_anh.relative_to(REPO)}\n"
                 f"   Tải về bằng: python3 scripts/tai-anh-pexels.py {a.ma} --chon 6")
    if not 1 <= a.anh <= len(anh_ds):
        sys.exit(f"❌ --anh phải trong khoảng 1–{len(anh_ds)}")
    nen = anh_ds[a.anh - 1]

    ra = REPO / "video" / "thumbnails" / f"{a.ma}-bia.png"
    ra.parent.mkdir(parents=True, exist_ok=True)
    tam = ra.parent / f".{a.ma}-lop.svg"
    lop_png = ra.parent / f".{a.ma}-lop.png"

    # Bìa dùng cỡ chữ to như thẻ mở đầu, kèm dòng kêu gọi theo dõi ở đáy
    tam.write_text(kr.tao_lop_chu(a.quote, dau_video=True, cta=True), encoding="utf-8")
    subprocess.run(["rsvg-convert", "-w", str(kr.RONG), "-h", str(kr.CAO),
                    "-o", str(lop_png), str(tam)], check=True)
    subprocess.run(
        ["ffmpeg", "-y", "-loglevel", "error", "-i", str(nen), "-i", str(lop_png),
         "-filter_complex",
         f"[0:v]scale={kr.RONG}:{kr.CAO}:force_original_aspect_ratio=increase,"
         f"crop={kr.RONG}:{kr.CAO},eq=brightness=0.02:contrast=1.06:saturation=1.05[nen];"
         "[nen][1:v]overlay=0:0:format=auto,format=rgb24[ra]",
         "-map", "[ra]", "-frames:v", "1", str(ra)], check=True)
    tam.unlink()
    lop_png.unlink()

    print(f"✅ {ra.relative_to(REPO)}  (1080×1920, nền = {nen.name})")
    print(f"   Xem thử:  open {ra.relative_to(REPO)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
