#!/usr/bin/env python3
"""Nghe thử các giọng VieNeu-TTS trên cùng một đoạn chữ.

Chạy bằng Python riêng của môi trường TTS:

    .venv-tts/bin/python scripts/thu-giong-vieneu.py
    .venv-tts/bin/python scripts/thu-giong-vieneu.py --giong "Phạm Tuyên" "Trúc Ly"

File ra nằm ở video/thu-giong/ (thư mục video không lên GitHub).
"""

from __future__ import annotations

import argparse
import sys
import time
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
RA = REPO / "video" / "thu-giong"

DOAN_MAU = (
    "Sáng nay mở mắt ra, cái đầu tiên bạn nghĩ tới là gì? "
    "Chắc là việc chưa xong, đúng không. Tin nhắn chưa trả lời. Khoản chưa trả. "
    "Mình bắt đầu một ngày bằng danh sách những thứ mình còn thiếu. "
    "Rồi cả ngày cứ thế, đi tìm cái thiếu."
)


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--giong", nargs="*", default=["Phạm Tuyên", "Trúc Ly", "Đoan Trang"],
                   help="Tên giọng cần nghe thử")
    p.add_argument("--kieu", default="tu_nhien",
                   choices=["tu_nhien", "tin_tuc", "doc_truyen"],
                   help="Kiểu đọc (mặc định tu_nhien — giọng nói đời thường)")
    p.add_argument("--chu", help="Đoạn chữ muốn nghe (mặc định dùng đoạn mẫu VD-001)")
    p.add_argument("--file", type=Path, help="Đọc chữ từ file thay vì --chu")
    p.add_argument("--liet-ke", action="store_true", help="Chỉ in danh sách giọng rồi thoát")
    a = p.parse_args()

    from vieneu import Vieneu

    print("⏳ Đang nạp model VieNeu-TTS v3 Turbo...")
    v = Vieneu()

    if a.liet_ke:
        for mo_ta, ten in v.list_preset_voices():
            print(f"  {ten:12s}  {mo_ta}")
        return

    chu = a.file.read_text(encoding="utf-8").strip() if a.file else (a.chu or DOAN_MAU)
    co_san = {ten for _, ten in v.list_preset_voices()}

    RA.mkdir(parents=True, exist_ok=True)
    for giong in a.giong:
        if giong not in co_san:
            print(f"⚠️  Không có giọng {giong!r} — bỏ qua. Xem danh sách: --liet-ke")
            continue
        t0 = time.time()
        am = v.infer(chu, voice=giong, style=a.kieu)
        ten_file = RA / f"{giong.replace(' ', '-')}-{a.kieu}.wav"
        v.save(am, str(ten_file))
        giay = len(am) / v.sample_rate
        print(f"✅ {ten_file.relative_to(REPO)}  ({giay:.1f}s tiếng, "
              f"mất {time.time() - t0:.0f}s để tổng hợp)")

    print(f"\n🎧 Nghe bằng:  open {RA.relative_to(REPO)}")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        sys.exit(130)
