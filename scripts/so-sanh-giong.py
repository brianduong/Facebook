#!/usr/bin/env python3
"""Tạo hai file tiếng để nghe so sánh giọng đọc trước/sau khi thêm ngữ điệu.

    python3 scripts/so-sanh-giong.py VD-001

Ra hai file trong video/raw/ (ngoài GitHub):
    VD-001-giong-A-phang.wav      đọc đều, không lọc âm  (bản cũ)
    VD-001-giong-B-truyen-cam.wav có ngữ điệu + hậu kỳ tiếng (bản mới)

Nghe cả hai rồi quyết định giữ bản nào.
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import giong_doc as gd  # noqa: E402
import nhan_dien as nd  # noqa: E402

TOC_DO = 155


def chay(cmd: list[str]) -> None:
    kq = subprocess.run(cmd, capture_output=True, text=True)
    if kq.returncode != 0:
        sys.exit(f"❌ {' '.join(cmd[:3])}...\n{kq.stderr.strip()[-800:]}")


def do_dai(f: Path) -> str:
    r = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                        "-of", "csv=p=0", str(f)], capture_output=True, text=True)
    return f"{float(r.stdout.strip()):.1f}s"


def main() -> int:
    ma = sys.argv[1] if len(sys.argv) > 1 else "VD-001"
    nguon = nd.REPO / "content" / "scripts" / "loi-doc" / f"{ma}-loi-doc.txt"
    if not nguon.exists():
        sys.exit(f"❌ Không thấy {nguon.relative_to(nd.REPO)}")

    ra_dir = nd.REPO / "video" / "raw"
    ra_dir.mkdir(parents=True, exist_ok=True)
    tam = ra_dir / "_tam"
    tam.mkdir(exist_ok=True)

    # Chỉ lấy 3 đoạn đầu cho đủ nghe, khỏi phải ngồi hết một phút
    doan = [d.strip() for d in nguon.read_text(encoding="utf-8").split("\n\n") if d.strip()][:3]
    text = " ".join(doan)

    for ten, co_ngu_dieu in (("A-phang", False), ("B-truyen-cam", True)):
        txt = tam / f"{ten}.txt"
        aiff = tam / f"{ten}.aiff"
        wav = ra_dir / f"{ma}-giong-{ten}.wav"
        txt.write_text(
            gd.soan_ngu_dieu(text, TOC_DO, la_the_dau=True, la_the_cuoi=True) if co_ngu_dieu else text,
            encoding="utf-8",
        )
        chay(["say", "-v", "Linh", "-r", str(TOC_DO), "-f", str(txt), "-o", str(aiff)])
        loc = ["-af", gd.LOC_AM] if co_ngu_dieu else []
        chay(["ffmpeg", "-y", "-loglevel", "error", "-i", str(aiff), *loc,
              "-ar", "44100", "-ac", "1", str(wav)])
        print(f"✅ {wav.relative_to(nd.REPO)}  ({do_dai(wav)})")

    print("👉 Mở hai file, nghe lần lượt A rồi B.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
