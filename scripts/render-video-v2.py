#!/usr/bin/env python3
"""Render video Reels 9:16 — ảnh chụp thật + chữ theo timeline + giọng VieNeu.

Khác bản cũ (`render-video-nhap.py`) ở ba điểm:
  1. **Bỏ nhân vật vẽ tay nhấp nháy miệng.** Nền là ảnh chụp thật tải từ Pexels.
  2. **Giọng VieNeu-TTS v3 Turbo** (48 kHz, có hơi thở) thay `say` của macOS.
  3. **Chuẩn hoá độ to một lần** trên toàn bài thay vì từng câu → hết nhấp nhô.

⚠️ Chạy bằng Python của môi trường TTS, KHÔNG phải python3 hệ thống:

    .venv-tts/bin/python scripts/render-video-v2.py VD-001
    .venv-tts/bin/python scripts/render-video-v2.py VD-001 --giong "Trúc Ly"
    .venv-tts/bin/python scripts/render-video-v2.py VD-001 --nhac assets/music/nen-am-ap.m4a

Trước khi render phải có ảnh nền:

    python3 scripts/tai-anh-pexels.py VD-001

Kết quả: video/exports/VD-001-reels.mp4  (ngoài GitHub)
Cần: ffmpeg, rsvg-convert, và môi trường .venv-tts.
"""

from __future__ import annotations

import argparse
import re
import shutil
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import giong_vieneu as gv  # noqa: E402
import khung_reels as kr  # noqa: E402

REPO = Path(__file__).resolve().parent.parent

TOI_DA_MOI_THE = 92      # ký tự tối đa mỗi thẻ chữ (khung dọc hẹp hơn khung vuông)
KHOANG_LANG = 0.42       # giây nghỉ sau mỗi thẻ (VieNeu nói gọn hơn `say` nên nghỉ dài hơn chút)
GIU_KET = 3.2            # giây giữ thẻ chốt cuối video
AM_LUONG_NHAC = 0.42     # nhạc nền so với giọng
RONG, CAO = kr.RONG, kr.CAO


def chay(cmd: list[str]) -> str:
    kq = subprocess.run(cmd, capture_output=True, text=True)
    if kq.returncode != 0:
        print(f"❌ Lỗi khi chạy: {' '.join(cmd[:4])}...", file=sys.stderr)
        print(kq.stderr.strip()[-1500:], file=sys.stderr)
        sys.exit(1)
    return kq.stdout.strip()


def kiem_tra_cong_cu() -> None:
    thieu = [t for t in ("ffmpeg", "ffprobe", "rsvg-convert") if not shutil.which(t)]
    if thieu:
        sys.exit(f"❌ Máy thiếu: {', '.join(thieu)}\n"
                 "   ffmpeg/ffprobe → brew install ffmpeg\n"
                 "   rsvg-convert  → brew install librsvg")
    try:
        import vieneu  # noqa: F401
    except ImportError:
        sys.exit("❌ Không thấy thư viện vieneu.\n"
                 "   Phải chạy bằng:  .venv-tts/bin/python scripts/render-video-v2.py ...")


def tach_the(text: str) -> list[str]:
    """Cắt lời đọc thành từng thẻ chữ. Câu đầu (hook) luôn đứng riêng một thẻ."""
    cau = [c.strip() for c in re.split(r"(?<=[.!?])\s+", " ".join(text.split())) if c.strip()]
    if not cau:
        sys.exit("❌ File lời đọc rỗng.")
    the = [cau[0]]
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


def lay_anh(ma: str) -> list[Path]:
    thu_muc = REPO / "assets" / "images" / "canh" / ma
    anh = sorted(p for p in thu_muc.glob("*.jpg")) + sorted(thu_muc.glob("*.jpeg"))
    if not anh:
        sys.exit(f"❌ Chưa có ảnh nền ở {thu_muc.relative_to(REPO)}\n"
                 f"   Tải về bằng:  python3 scripts/tai-anh-pexels.py {ma}")
    return anh


def dung_khung(anh: Path, lop_svg: str, lam_viec: Path, ten: str) -> Path:
    """Ảnh thật → cắt vừa khung dọc → đè lớp chữ trong suốt lên."""
    svg = lam_viec / f"{ten}.svg"
    lop_png = lam_viec / f"{ten}-chu.png"
    ra = lam_viec / f"{ten}.png"

    svg.write_text(lop_svg, encoding="utf-8")
    chay(["rsvg-convert", "-w", str(RONG), "-h", str(CAO), "-o", str(lop_png), str(svg)])

    # scale=…:force_original_aspect_ratio=increase + crop = "phủ kín khung, cắt phần thừa"
    chay(["ffmpeg", "-y", "-loglevel", "error", "-i", str(anh), "-i", str(lop_png),
          "-filter_complex",
          f"[0:v]scale={RONG}:{CAO}:force_original_aspect_ratio=increase,"
          f"crop={RONG}:{CAO},eq=brightness=0.02:contrast=1.06:saturation=1.05[nen];"
          "[nen][1:v]overlay=0:0:format=auto,format=rgb24[ra]",
          "-map", "[ra]", "-frames:v", "1", str(ra)])
    return ra


def main() -> int:
    p = argparse.ArgumentParser(description="Render video Reels 9:16 cho kênh Sống Tốt")
    p.add_argument("ma_so", help="Mã video, vd VD-001")
    p.add_argument("--giong", default=gv.GIONG_MAC_DINH,
                   help=f"Giọng VieNeu (mặc định {gv.GIONG_MAC_DINH}). "
                        f"Xem danh sách: .venv-tts/bin/python scripts/thu-giong-vieneu.py --liet-ke")
    p.add_argument("--kieu", default=gv.KIEU_MAC_DINH,
                   choices=["tu_nhien", "tin_tuc", "doc_truyen"],
                   help="Kiểu đọc (mặc định tu_nhien — giọng nói đời thường)")
    p.add_argument("--nhac", help="File nhạc nền (phải được phép dùng thương mại)")
    p.add_argument("--loi-doc", type=Path,
                   help="Chỉ định file lời đọc khác (mặc định tự tìm bản -v2 trước)")
    a = p.parse_args()

    kiem_tra_cong_cu()

    # Ưu tiên bản lời đọc v2 (đã viết lại theo văn nói) nếu có
    thu_muc_loi = REPO / "content" / "scripts" / "loi-doc"
    loi_doc = a.loi_doc or next(
        (f for f in (thu_muc_loi / f"{a.ma_so}-loi-doc-v2.txt",
                     thu_muc_loi / f"{a.ma_so}-loi-doc.txt") if f.exists()), None
    )
    if not loi_doc or not loi_doc.exists():
        sys.exit(f"❌ Không thấy lời đọc cho {a.ma_so} trong {thu_muc_loi.relative_to(REPO)}")

    anh_nen = lay_anh(a.ma_so)
    the = tach_the(loi_doc.read_text(encoding="utf-8"))

    lam_viec = REPO / "video" / "edit" / f"{a.ma_so}-reels"
    if lam_viec.exists():
        shutil.rmtree(lam_viec)
    lam_viec.mkdir(parents=True)
    ra = REPO / "video" / "exports" / f"{a.ma_so}-reels.mp4"
    ra.parent.mkdir(parents=True, exist_ok=True)

    print(f"📝 {len(the)} thẻ chữ · {len(anh_nen)} ảnh nền · "
          f"giọng {a.giong} ({a.kieu}) · nguồn chữ {loi_doc.name}")
    print("⏳ Đang nạp model VieNeu-TTS v3 Turbo...")
    giong = gv.Giong(a.giong, a.kieu)

    wavs: list[Path] = []
    thoi_luong: list[float] = []
    khung: list[Path] = []

    for i, doan in enumerate(the):
        # Giọng đọc từng thẻ → lấy đúng thời lượng tiếng làm thời lượng hình
        tho = lam_viec / f"{i:02d}-tho.wav"
        wav = lam_viec / f"{i:02d}.wav"
        giong.doc(doan, tho)
        chay(["ffmpeg", "-y", "-loglevel", "error", "-i", str(tho),
              "-af", f"{gv.LOC_TUNG_THE},apad=pad_dur={KHOANG_LANG}",
              "-ar", "48000", "-ac", "1", "-c:a", "pcm_s16le", str(wav)])

        # Ảnh xoay vòng nếu số thẻ nhiều hơn số ảnh
        anh = anh_nen[i * len(anh_nen) // len(the)]
        lop = kr.tao_lop_chu(doan, dau_video=(i == 0))
        khung.append(dung_khung(anh, lop, lam_viec, f"{i:02d}"))

        giay = do_dai(wav)
        wavs.append(wav)
        thoi_luong.append(giay)
        print(f"   {i + 1:2d}. {giay:5.1f}s  {anh.name}  {doan[:46]}{'…' if len(doan) > 46 else ''}")

    # Thẻ chốt cuối: câu kết + dòng kêu gọi theo dõi, đứng im 3,2 giây
    ket = kr.tao_lop_chu(the[-1], cta=True)
    khung_ket = dung_khung(anh_nen[-1], ket, lam_viec, "ket")

    tong = sum(thoi_luong) + GIU_KET
    print(f"⏱  Tổng: {tong:.0f}s",
          "✅ trên 60s" if tong > 60 else "⚠️  DƯỚI 60s — cần thêm nội dung")

    # ---- Tiếng: ghép các thẻ rồi mới chuẩn hoá độ to MỘT LẦN trên toàn bài ----
    ds_am = lam_viec / "am-thanh.txt"
    ds_am.write_text("".join(f"file '{w}'\n" for w in wavs), encoding="utf-8")
    giong_wav = lam_viec / "giong.wav"
    chay(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", str(ds_am),
          "-af", f"{gv.LOC_TOAN_BAI},apad=pad_dur={GIU_KET}",
          "-ar", "48000", "-c:a", "pcm_s16le", str(giong_wav)])

    # ---- Hình: mỗi thẻ giữ đúng thời lượng tiếng của nó ----
    dong_hinh = [f"file '{k}'\nduration {g:.3f}\n" for k, g in zip(khung, thoi_luong)]
    dong_hinh.append(f"file '{khung_ket}'\nduration {GIU_KET}\nfile '{khung_ket}'\n")
    ds_hinh = lam_viec / "hinh.txt"
    ds_hinh.write_text("".join(dong_hinh), encoding="utf-8")

    cmd = ["ffmpeg", "-y", "-loglevel", "error",
           "-f", "concat", "-safe", "0", "-i", str(ds_hinh),
           "-i", str(giong_wav)]

    if a.nhac:
        nhac = Path(a.nhac)
        if not nhac.is_absolute():
            nhac = REPO / nhac
        if not nhac.exists():
            sys.exit(f"❌ Không thấy file nhạc {nhac}")
        cmd += ["-stream_loop", "-1", "-i", str(nhac),
                "-filter_complex",
                # normalize=0: không cho amix chia đôi âm lượng, nếu không giọng bị tụt
                f"[2:a]volume={AM_LUONG_NHAC}[nhac];"
                "[1:a][nhac]amix=inputs=2:duration=first:dropout_transition=0:normalize=0,"
                "alimiter=limit=0.95[am]",
                "-map", "0:v", "-map", "[am]"]
    else:
        cmd += ["-map", "0:v", "-map", "1:a"]

    # Zoom vào cực chậm cho khung khỏi tĩnh + mờ dần đầu cuối
    hinh_anh = (
        "fps=30,"
        "zoompan=z='min(1+0.000032*on,1.07)':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)'"
        f":d=1:s={RONG}x{CAO}:fps=30,"
        "fade=t=in:st=0:d=0.5,"
        f"fade=t=out:st={max(tong - 0.9, 0.1):.2f}:d=0.9,"
        "format=yuv420p"
    )
    # maxrate/bufsize: chặn trần bitrate, nếu không ảnh nhiều hạt làm file phình lên
    # hàng chục MB mà mắt thường không thấy đẹp hơn.
    cmd += ["-r", "30", "-vf", hinh_anh,
            "-c:v", "libx264", "-preset", "medium", "-crf", "21",
            "-maxrate", "8M", "-bufsize", "16M",
            "-c:a", "aac", "-b:a", "192k", "-shortest", str(ra)]
    print("🎬 Đang render...")
    chay(cmd)

    print(f"✅ {ra.relative_to(REPO)}  ({ra.stat().st_size / 1e6:.1f} MB, {do_dai(ra):.0f}s)")
    print(f"   File trung gian giữ ở {lam_viec.relative_to(REPO)} (xoá được).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
