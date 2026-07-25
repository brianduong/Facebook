#!/usr/bin/env python3
"""Tự tổng hợp nhạc nền GỐC cho kênh Sống Tốt — không dùng nhạc của ai cả.

Vì sao tự làm: nhạc lấy trên mạng (kể cả nhạc "free") là rủi ro bản quyền lớn
nhất khi Page bật kiếm tiền. Nhạc do script này tạo ra là của kênh, dùng vĩnh
viễn, không ai đòi được.

Đây là nhạc nền tối giản: đệm dây kéo dài (pad) + vài tiếng gõ nhẹ như chuông,
âm lượng thấp, để chảy dưới giọng đọc. Không phải nhạc có nhạc cụ thật.

    python3 scripts/tao-nhac-nen.py                    # tạo cả 3 kiểu
    python3 scripts/tao-nhac-nen.py --kieu am-ap       # chỉ một kiểu

Ra file trong assets/music/ (đoạn 32 giây, script render tự lặp lại cho đủ video):
    nen-am-ap.m4a      ấm áp, hy vọng — cho nội dung biết ơn, tử tế
    nen-lang.m4a       lặng, dịu — cho nội dung an ủi, nghỉ ngơi
    nen-trong-sang.m4a trong sáng, nhẹ nhõm — cho nội dung bước tiếp
"""

from __future__ import annotations

import argparse
import math
import subprocess
import sys
import wave
from array import array
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import nhan_dien as nd  # noqa: E402

SR = 22050          # tổng hợp ở tần số thấp cho nhanh, ffmpeg nâng lại 44100
DAI = 32.0          # giây — một đoạn lặp
RA_DIR = nd.REPO / "assets" / "music"


def nốt(ten: str) -> float:
    """Tên nốt kiểu 'C4', 'A3' → tần số Hz (A4 = 440)."""
    bang = {"C": -9, "D": -7, "E": -5, "F": -4, "G": -2, "A": 0, "B": 2}
    ten_not, quang = ten[0], int(ten[1:])
    nua_cung = bang[ten_not] + (quang - 4) * 12
    return 440.0 * (2 ** (nua_cung / 12))


# Mỗi kiểu: (hợp âm đệm, chuỗi nốt gõ, độ trong của tiếng gõ)
KIEU = {
    "am-ap": {
        "hop_am": [["C3", "E3", "G3", "D4"], ["A2", "C3", "E3", "G3"],
                   ["F2", "A2", "C3", "E3"], ["G2", "B2", "D3", "A3"]],
        "go": ["E5", "G5", "D5", "E5", "A4", "C5", "G4", "E5"],
        "sang": 0.35,
    },
    "lang": {
        "hop_am": [["A2", "C3", "E3"], ["F2", "A2", "C3"],
                   ["D2", "F2", "A2"], ["E2", "G2", "B2"]],
        "go": ["A4", "C5", "A4", "E4", "G4", "A4", "E4", "C5"],
        "sang": 0.18,
    },
    "trong-sang": {
        "hop_am": [["G3", "B3", "D4"], ["D3", "F3", "A3"],
                   ["C3", "E3", "G3"], ["G3", "B3", "E4"]],
        "go": ["D5", "G5", "B5", "A5", "G5", "D5", "E5", "G5"],
        "sang": 0.5,
    },
}


def _dao_dong(buf: array, t0: float, freq: float, dai: float, bien: float,
              tan: float, nha: float, lech: float = 0.0) -> None:
    """Cộng một dao động hình sin có bao âm vào buffer.

    Dùng công thức truy hồi s[n] = 2cos(w)·s[n-1] − s[n-2] thay cho math.sin
    từng mẫu — nhanh hơn nhiều lần, đủ để chạy bằng Python thuần.

    tan  : giây để âm lên hết (0 = gõ, vào ngay rồi tắt dần)
    nha  : giây để âm tắt còn ~37%
    lech : lệch tần số vài phần Hz cho tiếng dày hơn (hiệu ứng chorus)
    """
    i0 = int(t0 * SR)
    n = int(dai * SR)
    if i0 + n > len(buf):
        n = len(buf) - i0
    if n <= 0:
        return

    w = 2 * math.pi * (freq + lech) / SR
    c = 2 * math.cos(w)
    s1, s2 = math.sin(w), 0.0          # s[n-1], s[n-2]

    if tan > 0:                         # pad: lên dần rồi tắt dần
        buoc_len = 1.0 / (tan * SR)
        env = 0.0
    else:                               # gõ: vào ngay
        buoc_len = 0.0
        env = 1.0
    k_tat = math.exp(-1.0 / max(nha * SR, 1.0))
    dinh = int(tan * SR)

    for i in range(n):
        s0 = c * s1 - s2
        s2, s1 = s1, s0
        if i < dinh:
            env += buoc_len
            if env > 1.0:
                env = 1.0
        else:
            env *= k_tat
        buf[i0 + i] += s0 * env * bien


def tong_hop(kieu: str) -> array:
    cf = KIEU[kieu]
    buf = array("d", [0.0]) * int(DAI * SR)
    so_hop_am = len(cf["hop_am"])
    dai_hop_am = DAI / so_hop_am

    # Lớp đệm: mỗi hợp âm gối lên hợp âm sau cho khỏi giật khúc
    for i, hop_am in enumerate(cf["hop_am"]):
        t0 = i * dai_hop_am
        for j, ten in enumerate(hop_am):
            f = nốt(ten)
            bien = 0.20 if j == 0 else 0.13
            _dao_dong(buf, t0, f, dai_hop_am + 2.4, bien, tan=1.3, nha=2.2)
            _dao_dong(buf, t0, f, dai_hop_am + 2.4, bien * 0.5, tan=1.3, nha=2.2, lech=0.4)
            _dao_dong(buf, t0, f * 2, dai_hop_am + 2.0, bien * 0.16, tan=1.5, nha=1.8)

    # Lớp gõ: một nốt mỗi 2 giây, có hài âm nên nghe như chuông gỗ
    go = cf["go"]
    for i in range(int(DAI // 2)):
        t0 = 1.0 + i * 2.0
        f = nốt(go[i % len(go)])
        bien = 0.16 * (1.0 if i % 4 else 0.7)      # nhấn nhẹ theo nhịp
        _dao_dong(buf, t0, f, 2.6, bien, tan=0.0, nha=0.85)
        _dao_dong(buf, t0, f * 2, 1.8, bien * cf["sang"], tan=0.0, nha=0.45)
        _dao_dong(buf, t0, f * 3, 1.2, bien * cf["sang"] * 0.35, tan=0.0, nha=0.28)

    # Chuẩn hoá về đỉnh 0.9 để khỏi vỡ tiếng khi ghi ra file
    dinh = max(abs(x) for x in buf) or 1.0
    he_so = 0.9 / dinh
    for i in range(len(buf)):
        buf[i] *= he_so
    return buf


def ghi_wav(buf: array, f: Path) -> None:
    mau = array("h", [int(max(-1.0, min(1.0, x)) * 32000) for x in buf])
    with wave.open(str(f), "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes(mau.tobytes())


def hau_ky(vao: Path, ra: Path) -> None:
    """Làm mềm và mở rộng tiếng: cắt cao, vang phòng, tách stereo nhẹ, hạ độ to."""
    loc = (
        "aresample=44100,"
        "lowpass=f=4200,"                                  # bớt gắt
        "aecho=0.8:0.85:180|420:0.3|0.18,"                 # vang, nghe rộng
        f"afade=t=in:st=0:d=0.6,afade=t=out:st={DAI - 0.6:.1f}:d=0.6,"
        "loudnorm=I=-23:TP=-6:LRA=7,"                      # mức nhạc nền, còn dư đầu
        "aresample=44100"                                  # loudnorm đẩy lên 192k, kéo về lại
    )
    # Kênh phải trễ 16ms so với kênh trái → tiếng nghe rộng ra hai bên tai
    subprocess.run(
        ["ffmpeg", "-y", "-loglevel", "error", "-i", str(vao),
         "-filter_complex", f"[0:a]{loc},asplit=2[l][r];[r]adelay=16[rd];"
                            "[l][rd]join=inputs=2:channel_layout=stereo[out]",
         "-map", "[out]", "-c:a", "aac", "-b:a", "128k", str(ra)],
        check=True,
    )


def main() -> int:
    p = argparse.ArgumentParser(description="Tạo nhạc nền gốc cho kênh Sống Tốt")
    p.add_argument("--kieu", choices=sorted(KIEU), help="Chỉ tạo một kiểu (mặc định: cả 3)")
    a = p.parse_args()

    RA_DIR.mkdir(parents=True, exist_ok=True)
    tam = RA_DIR / "_tam.wav"
    for kieu in ([a.kieu] if a.kieu else sorted(KIEU)):
        print(f"🎵 đang tổng hợp {kieu}...")
        ghi_wav(tong_hop(kieu), tam)
        ra = RA_DIR / f"nen-{kieu}.m4a"
        hau_ky(tam, ra)
        print(f"✅ {ra.relative_to(nd.REPO)}  ({ra.stat().st_size / 1e6:.2f} MB, {DAI:.0f}s lặp được)")
    tam.unlink(missing_ok=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
