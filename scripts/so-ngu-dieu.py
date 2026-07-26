#!/usr/bin/env python3
"""Đo ngữ điệu của giọng đọc — để chọn tham số bằng số thay vì bằng cảm giác.

Anh chê "giọng đọc chứ không phải giọng nói". Cái làm nên khác biệt đó chủ yếu là
**cao độ có nhấp nhô hay không**: người đọc thuộc lòng thì câu nào cũng một đường
cao độ như nhau; người nói thì lên xuống theo ý.

Script này tổng hợp cùng một đoạn chữ qua nhiều cấu hình, rồi đo:

  F0 std   — độ lệch chuẩn cao độ (Hz). **Càng cao càng nhiều ngữ điệu.**
  F0 range — khoảng cao độ giữa bách phân vị 10 và 90, bỏ đuôi nhiễu
  lặng      — tỉ lệ thời gian im lặng, tức là có ngắt nghỉ để lấy hơi hay không

    .venv-tts/bin/python scripts/so-ngu-dieu.py
    .venv-tts/bin/python scripts/so-ngu-dieu.py --giong "Phạm Tuyên" "Trúc Ly"

File nghe thử ra ở video/thu-ngu-dieu/. Số cao chưa chắc đã hay — nhiệt cao quá thì
model bắt đầu vấp và đọc sai chữ, nên vẫn phải nghe lại vài bản đứng đầu.
"""

from __future__ import annotations

import argparse
import subprocess
import sys
import wave
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
import giong_vieneu as gv  # noqa: E402

REPO = Path(__file__).resolve().parent.parent
RA = REPO / "video" / "thu-ngu-dieu"

# Đoạn mẫu: hook VD-001 — có câu hỏi, có câu ngắn, có liệt kê. Ba thứ này bộc lộ
# ngữ điệu rõ nhất; đoạn văn xuôi đều đều thì cấu hình nào nghe cũng như nhau.
DOAN_MAU = (
    "Sáng nay mở mắt ra, cái đầu tiên bạn nghĩ tới là gì? "
    "Chắc là việc chưa xong, đúng không. Tin nhắn chưa trả lời. Khoản chưa trả. "
    "Không phải riêng bạn đâu, ai cũng thế cả."
)


def doc_wav(f: Path) -> tuple[np.ndarray, int]:
    with wave.open(str(f), "rb") as w:
        tan = w.getframerate()
        x = np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16)
    return x.astype(np.float32) / 32768.0, tan


def cao_do(x: np.ndarray, tan: int, f_min: int = 70, f_max: int = 350) -> np.ndarray:
    """Bám cao độ bằng tự tương quan từng khung 40 ms.

    Đủ dùng để **so sánh** các cấu hình với nhau — không nhằm đo chính xác tuyệt đối.
    Khung nào quá nhỏ tiếng hoặc tự tương quan yếu thì coi như vô thanh, bỏ qua.
    """
    khung = int(0.04 * tan)
    buoc = int(0.01 * tan)
    lo, hi = int(tan / f_max), int(tan / f_min)
    nguong = 0.02 * np.abs(x).max()

    ra = []
    for i in range(0, len(x) - khung, buoc):
        k = x[i:i + khung]
        if np.sqrt(np.mean(k ** 2)) < nguong:
            continue
        k = k - k.mean()
        tt = np.correlate(k, k, mode="full")[khung - 1:]
        if tt[0] <= 0:
            continue
        vung = tt[lo:hi]
        if len(vung) == 0:
            continue
        dinh = int(np.argmax(vung)) + lo
        if tt[dinh] / tt[0] < 0.3:        # tự tương quan yếu → vô thanh
            continue
        ra.append(tan / dinh)
    return np.array(ra)


def ti_le_lang(x: np.ndarray) -> float:
    khung = 1024
    nguong = 0.02 * np.abs(x).max()
    nl = np.array([np.sqrt(np.mean(x[i:i + khung] ** 2))
                   for i in range(0, len(x) - khung, khung)])
    return float((nl < nguong).mean()) if len(nl) else 0.0


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--giong", nargs="*", default=["Phạm Tuyên"])
    p.add_argument("--kieu", nargs="*", default=["tu_nhien", "doc_truyen"])
    p.add_argument("--nhiet", nargs="*", type=float, default=[0.7, 0.8, 0.95, 1.1])
    p.add_argument("--im-lang", nargs="*", type=float, default=[0.15, 0.28])
    p.add_argument("--chu", help="Đoạn chữ muốn thử")
    a = p.parse_args()

    chu = a.chu or DOAN_MAU
    RA.mkdir(parents=True, exist_ok=True)
    ket: list[tuple] = []

    print(f"Đo trên {len(chu.split())} chữ · "
          f"{len(a.giong) * len(a.kieu) * len(a.nhiet) * len(a.im_lang)} cấu hình\n")

    for giong in a.giong:
        for kieu in a.kieu:
            for nhiet in a.nhiet:
                for im in a.im_lang:
                    nhan = f"{giong}-{kieu}-n{nhiet:g}-l{im:g}".replace(" ", "_")
                    tho = RA / f"{nhan}-tho.wav"
                    ra = RA / f"{nhan}.wav"
                    try:
                        g = gv.Giong(giong, kieu, nhiet, im)
                        g.doc(chu, tho)
                    except Exception as e:
                        print(f"  ⚠️  {nhan}: {e}")
                        continue

                    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(tho),
                                    "-af", f"{gv.LOC_TUNG_THE},{gv.LOC_TOAN_BAI}",
                                    "-ar", "48000", "-ac", "1", str(ra)], check=True)
                    tho.unlink(missing_ok=True)

                    x, tan = doc_wav(ra)
                    f0 = cao_do(x, tan)
                    if len(f0) < 20:
                        print(f"  ⚠️  {nhan}: không bám được cao độ")
                        continue
                    std = float(np.std(f0))
                    khoang = float(np.percentile(f0, 90) - np.percentile(f0, 10))
                    ket.append((std, khoang, ti_le_lang(x), len(x) / tan, nhan))

    if not ket:
        return 1

    ket.sort(reverse=True)
    print(f"{'F0 std':>7} {'F0 range':>9} {'lặng':>6} {'giây':>6}  cấu hình")
    print("─" * 62)
    for std, khoang, lang, giay, nhan in ket:
        print(f"{std:7.1f} {khoang:9.1f} {lang:5.0%} {giay:6.1f}  {nhan}")

    print(f"\nNghe thử: open {RA.relative_to(REPO)}")
    print("F0 std cao = cao độ nhấp nhô = nghe ra giọng nói.")
    print("Nhưng nhiệt cao quá thì model vấp và đọc sai chữ — phải nghe lại vài bản đầu bảng.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
