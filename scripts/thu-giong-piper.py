#!/usr/bin/env python3
"""Nghe thử các giọng Piper tiếng Anh trên cùng một đoạn chữ.

Bản tiếng Anh của `thu-giong-vieneu.py`. Chạy bằng Python của môi trường TTS:

    .venv-tts/bin/python scripts/thu-giong-piper.py                 # nghe các giọng đã tải
    .venv-tts/bin/python scripts/thu-giong-piper.py --liet-ke       # xem giọng đang có
    .venv-tts/bin/python scripts/thu-giong-piper.py --cham 1.0 1.12 1.25   # so tốc độ đọc
    .venv-tts/bin/python scripts/thu-giong-piper.py --file content/scripts/loi-doc/VD-003-loi-doc-en.txt

File ra nằm ở video/thu-giong-en/ (thư mục video không lên GitHub).
Tải thêm giọng:
    .venv-tts/bin/python -m piper.download_voices --data-dir .piper-voices en_GB-alba-medium
"""

from __future__ import annotations

import argparse
import subprocess
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import giong_piper as gp  # noqa: E402

REPO = Path(__file__).resolve().parent.parent
RA = REPO / "video" / "thu-giong-en"

# Bốn khối đầu của VD-003 — nghe thử trên chữ thật của kênh, không phải câu mẫu vu vơ.
DOAN_MAU = (
    "You're lying there, looking at the ceiling, phone still in your hand. "
    "The day hasn't started yet, and you already feel behind. "
    "Some days are just like that. Your body is awake. Nothing else is. "
    "A tired day isn't a wasted day. Everyone has them."
)


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--giong", nargs="*", help="Tên giọng cần nghe (mặc định: tất cả đã tải)")
    p.add_argument("--cham", nargs="*", type=float, default=[gp.DO_CHAM_MAC_DINH],
                   help="Tốc độ đọc, >1 là chậm lại (mặc định %(default)s)")
    p.add_argument("--chu", help="Đoạn chữ muốn nghe")
    p.add_argument("--file", type=Path, help="Đọc chữ từ file thay vì --chu")
    p.add_argument("--liet-ke", action="store_true", help="Chỉ in giọng đã tải rồi thoát")
    a = p.parse_args()

    co_san = gp.liet_ke()
    if a.liet_ke:
        if not co_san:
            print("Chưa tải giọng nào. Tải về:")
            print("  .venv-tts/bin/python -m piper.download_voices "
                  "--data-dir .piper-voices en_US-ryan-high")
            return 1
        for g in co_san:
            print(f"  {g}")
        return 0

    if not co_san:
        sys.exit("❌ Chưa có giọng nào trong .piper-voices/ — xem --liet-ke để biết cách tải.")

    giong_can = a.giong or co_san
    chu = a.file.read_text(encoding="utf-8").strip() if a.file else (a.chu or DOAN_MAU)

    RA.mkdir(parents=True, exist_ok=True)
    da_lam: list[Path] = []

    for ten in giong_can:
        if ten not in co_san:
            print(f"⚠️  Chưa tải giọng {ten!r} — bỏ qua.")
            continue
        for cham in a.cham:
            nhan = f"{ten}-cham{cham:g}".replace(".", "_")
            tho = RA / f"{nhan}-tho.wav"
            ra = RA / f"{nhan}.wav"

            t0 = time.time()
            g = gp.Giong(ten, cham)
            giay = g.doc(chu, tho)

            # Hậu kỳ đúng chuỗi dùng khi render, để nghe thử sát bản thật
            subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(tho),
                            "-af", f"{gp.LOC_TUNG_THE},{gp.LOC_TOAN_BAI}",
                            "-ar", "48000", "-ac", "1", str(ra)], check=True)
            tho.unlink(missing_ok=True)

            so_tu = len(chu.split())
            print(f"  ✅ {nhan:38s} {giay:5.1f}s  "
                  f"({so_tu / giay:.2f} từ/giây)  máy chạy {time.time() - t0:.1f}s")
            da_lam.append(ra)

    if not da_lam:
        return 1

    print(f"\n🎧 Nghe thử: open {RA.relative_to(REPO)}")
    print("   Chấm theo ba thứ: có ấm không · nghe kịp không · chữ 's' cuối từ có rõ không.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
