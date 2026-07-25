#!/usr/bin/env python3
"""Render VIDEO NHÁP 1:1 từ lời đọc — chữ chạy theo giọng, không cần quay gì.

Video ra sẽ đăng được ngay, nhưng đây là bản NHÁP:
  - giọng là giọng máy (Linh của macOS) → nên thu lại bằng giọng thật của anh
  - nền là gradient thương hiệu → nên thay bằng b-roll khi có
Mục đích: có video đăng đều tay ngay từ tuần này, không chờ dựng tay.

Dùng:
    python3 scripts/render-video-nhap.py VD-001
    python3 scripts/render-video-nhap.py VD-001 --tone sang --toc-do 132
    python3 scripts/render-video-nhap.py VD-001 --nhac assets/music/nen-nhe.mp3

Kết quả: video/exports/VD-001-nhap.mp4  (ngoài GitHub)

Cần: ffmpeg, rsvg-convert, giọng Linh của macOS.
"""

from __future__ import annotations

import argparse
import re
import shutil
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import nhan_dien as nd  # noqa: E402

TOI_DA_MOI_THE = 120     # số ký tự tối đa mỗi thẻ chữ
KHOANG_LANG = 0.45       # giây nghỉ sau mỗi thẻ
GIU_QUOTE = 3.0          # giây giữ ảnh quote ở cuối
AM_LUONG_NHAC = 0.14     # nhạc nền so với giọng đọc


def chay(cmd: list[str]) -> str:
    kq = subprocess.run(cmd, capture_output=True, text=True)
    if kq.returncode != 0:
        print(f"❌ Lỗi khi chạy: {' '.join(cmd[:3])}...", file=sys.stderr)
        print(kq.stderr.strip()[-1500:], file=sys.stderr)
        sys.exit(1)
    return kq.stdout.strip()


def kiem_tra_cong_cu() -> None:
    thieu = [t for t in ("ffmpeg", "ffprobe", "rsvg-convert", "say") if not shutil.which(t)]
    if thieu:
        sys.exit(
            f"❌ Máy thiếu: {', '.join(thieu)}\n"
            "   ffmpeg/ffprobe → brew install ffmpeg\n"
            "   rsvg-convert  → brew install librsvg"
        )


def tach_doan(text: str) -> list[str]:
    """Cắt lời đọc thành từng thẻ chữ: theo câu, gộp lại cho vừa một khung.

    Câu đầu (hook) luôn đứng riêng một thẻ — 3 giây đầu quyết định người xem
    có dừng lại hay không, không nên nhồi thêm câu khác vào đó.
    """
    cau = [c.strip() for c in re.split(r"(?<=[.!?])\s+", " ".join(text.split())) if c.strip()]
    if not cau:
        sys.exit("❌ File lời đọc rỗng.")
    the: list[str] = [cau[0]]
    hien_tai = ""
    for c in cau[1:]:
        if hien_tai and len(hien_tai) + len(c) + 1 > TOI_DA_MOI_THE:
            the.append(hien_tai)
            hien_tai = c
        else:
            hien_tai = f"{hien_tai} {c}".strip()
    if hien_tai:
        the.append(hien_tai)
    return the


def do_dai(f: Path) -> float:
    return float(chay(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                       "-of", "csv=p=0", str(f)]))


def main() -> int:
    p = argparse.ArgumentParser(description="Render video nháp 1:1 cho kênh Sống Tốt")
    p.add_argument("ma_so", help="Mã video, vd VD-001")
    p.add_argument("--tone", choices=sorted(nd.TONES), default="vua", help="Sắc nền")
    p.add_argument("--toc-do", type=int, default=138, help="Tốc độ đọc (từ/phút), mặc định 138")
    p.add_argument("--nhac", help="File nhạc nền (phải là nhạc được phép dùng thương mại)")
    a = p.parse_args()

    kiem_tra_cong_cu()

    loi_doc = nd.REPO / "content" / "scripts" / "loi-doc" / f"{a.ma_so}-loi-doc.txt"
    quote = nd.REPO / "assets" / "templates" / "quotes" / f"{a.ma_so}-quote.png"
    if not loi_doc.exists():
        sys.exit(f"❌ Không thấy {loi_doc.relative_to(nd.REPO)}")
    if not quote.exists():
        sys.exit(f"❌ Không thấy ảnh quote {quote.relative_to(nd.REPO)}\n"
                 f"   Tạo bằng: python3 scripts/tao-anh-quote.py {a.ma_so} \"Dòng 1\" \"Dòng 2\"")

    lam_viec = nd.REPO / "video" / "edit" / f"{a.ma_so}-nhap"
    if lam_viec.exists():
        shutil.rmtree(lam_viec)
    lam_viec.mkdir(parents=True)
    ra = nd.REPO / "video" / "exports" / f"{a.ma_so}-nhap.mp4"
    ra.parent.mkdir(parents=True, exist_ok=True)

    the = tach_doan(loi_doc.read_text(encoding="utf-8"))
    print(f"📝 {len(the)} thẻ chữ")

    wavs: list[Path] = []
    thoi_luong: list[float] = []
    for i, doan in enumerate(the):
        txt = lam_viec / f"{i:02d}.txt"
        aiff = lam_viec / f"{i:02d}.aiff"
        wav = lam_viec / f"{i:02d}.wav"
        svg = lam_viec / f"{i:02d}.svg"
        png = lam_viec / f"{i:02d}.png"

        # Giọng đọc từng thẻ → thẻ chữ và tiếng khớp nhau chính xác
        txt.write_text(doan, encoding="utf-8")
        chay(["say", "-v", "Linh", "-r", str(a.toc_do), "-f", str(txt), "-o", str(aiff)])
        chay(["ffmpeg", "-y", "-loglevel", "error", "-i", str(aiff),
              "-af", f"apad=pad_dur={KHOANG_LANG}", "-ar", "44100", "-ac", "1", str(wav)])

        svg.write_text(
            nd.tao_svg(nd.boc_dong(doan, 26), tone=a.tone, cta=False, giua=True),
            encoding="utf-8",
        )
        nd.xuat_png(svg, png)

        giay = do_dai(wav)
        wavs.append(wav)
        thoi_luong.append(giay)
        print(f"   {i + 1:2d}. {giay:5.1f}s  {doan[:52]}{'…' if len(doan) > 52 else ''}")

    tong = sum(thoi_luong) + GIU_QUOTE
    print(f"⏱  Tổng: {tong:.0f}s", "✅ trên 60s" if tong > 60 else "⚠️  DƯỚI 60s")

    # Ghép giọng đọc + 3 giây lặng cho ảnh quote cuối
    ds_am = lam_viec / "am-thanh.txt"
    ds_am.write_text("".join(f"file '{w}'\n" for w in wavs), encoding="utf-8")
    giong = lam_viec / "giong.wav"
    chay(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", str(ds_am),
          "-af", f"apad=pad_dur={GIU_QUOTE}", "-c:a", "pcm_s16le", str(giong)])

    # Danh sách hình: mỗi thẻ giữ đúng thời lượng tiếng của nó, cuối là ảnh quote
    dong_hinh = "".join(
        f"file '{lam_viec / f'{i:02d}.png'}'\nduration {t:.3f}\n"
        for i, t in enumerate(thoi_luong)
    )
    dong_hinh += f"file '{quote}'\nduration {GIU_QUOTE}\nfile '{quote}'\n"
    ds_hinh = lam_viec / "hinh.txt"
    ds_hinh.write_text(dong_hinh, encoding="utf-8")

    cmd = ["ffmpeg", "-y", "-loglevel", "error",
           "-f", "concat", "-safe", "0", "-i", str(ds_hinh),
           "-i", str(giong)]

    if a.nhac:
        nhac = Path(a.nhac)
        if not nhac.is_absolute():
            nhac = nd.REPO / nhac
        if not nhac.exists():
            sys.exit(f"❌ Không thấy file nhạc {nhac}")
        # Nhạc lặp vô hạn rồi cắt theo độ dài giọng đọc
        cmd += ["-stream_loop", "-1", "-i", str(nhac),
                "-filter_complex",
                f"[2:a]volume={AM_LUONG_NHAC}[nhac];"
                "[1:a][nhac]amix=inputs=2:duration=first:dropout_transition=0[am]",
                "-map", "0:v", "-map", "[am]"]
    else:
        cmd += ["-map", "0:v", "-map", "1:a"]

    # Zoom vào cực chậm cho video khỏi tĩnh cứng + mờ dần ở đầu và cuối
    hinh_anh = (
        "fps=30,"
        "zoompan=z='min(1+0.00003*on,1.06)':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)'"
        ":d=1:s=1080x1080:fps=30,"
        "fade=t=in:st=0:d=0.5,"
        f"fade=t=out:st={max(tong - 0.9, 0.1):.2f}:d=0.9,"
        "format=yuv420p"
    )
    cmd += ["-r", "30", "-vf", hinh_anh,
            "-c:v", "libx264", "-preset", "medium", "-crf", "20",
            "-c:a", "aac", "-b:a", "160k", "-shortest", str(ra)]
    print("🎬 Đang render...")
    chay(cmd)

    print(f"✅ {ra.relative_to(nd.REPO)}  ({ra.stat().st_size / 1e6:.1f} MB, {do_dai(ra):.0f}s)")
    print(f"   File trung gian giữ ở {lam_viec.relative_to(nd.REPO)} (xoá được).")
    print("👉 Đây là bản NHÁP: nên thu lại giọng thật và thay nền b-roll khi có.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
