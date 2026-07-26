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
import giong_piper as gp  # noqa: E402
import giong_vieneu as gv  # noqa: E402
import khung_reels as kr  # noqa: E402

REPO = Path(__file__).resolve().parent.parent

TOI_DA_MOI_THE = 92      # ký tự tối đa mỗi thẻ chữ (khung dọc hẹp hơn khung vuông)
KHOANG_LANG = 0.55       # giây nghỉ sau mỗi thẻ
# Nâng từ 0,42 lên 0,55 ngày 27/07, hai lý do cùng chiều:
#   1. Kiểu đọc doc_truyen (chốt vì ngữ điệu tốt hơn 44%) đọc nhanh hơn tu_nhien ~14%,
#      làm bài tụt xuống sát mốc 60 giây — mốc bắt buộc để ăn thưởng TikTok.
#   2. Người nói thì nghỉ giữa hai ý, người đọc thì không. Nghỉ dài hơn chính là thứ
#      anh đòi khi bảo "giọng nói chứ không phải giọng đọc" — không phải chỗ độn thời lượng.
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


def kiem_tra_cong_cu(en: bool = False) -> None:
    thieu = [t for t in ("ffmpeg", "ffprobe", "rsvg-convert") if not shutil.which(t)]
    if thieu:
        sys.exit(f"❌ Máy thiếu: {', '.join(thieu)}\n"
                 "   ffmpeg/ffprobe → brew install ffmpeg\n"
                 "   rsvg-convert  → brew install librsvg")
    thu_vien = "piper" if en else "vieneu"
    try:
        __import__(thu_vien)
    except ImportError:
        sys.exit(f"❌ Không thấy thư viện {thu_vien}.\n"
                 "   Phải chạy bằng:  .venv-tts/bin/python scripts/render-video-v2.py ...")


def tach_the(text: str) -> list[str]:
    """Cắt lời đọc thành thẻ chữ. Một thẻ KHÔNG được vắt qua hai khối.

    Mỗi khối trong file lời đọc (cách nhau một dòng trống) là một ý trọn vẹn do
    người viết chia ra. Gộp hai khối vào chung một thẻ thì chữ trên màn hình vắt
    ngang đúng chỗ chuyển ý — người xem đọc thấy hai ý dính làm một. Nên chỉ gộp
    câu **trong cùng một khối**; khối dài quá thì cắt nhỏ ra.

    Câu đầu (hook) luôn đứng riêng một thẻ.
    """
    khoi = [k.strip() for k in re.split(r"\n\s*\n", text) if k.strip()]
    if not khoi:
        sys.exit("❌ File lời đọc rỗng.")

    the: list[str] = []
    for i, k in enumerate(khoi):
        cau = [c.strip() for c in re.split(r"(?<=[.!?])\s+", " ".join(k.split())) if c.strip()]
        if i == 0 and cau:
            the.append(cau.pop(0))        # hook đứng riêng
        hien_tai = ""
        for c in cau:
            if hien_tai and len(hien_tai) + len(c) + 1 > TOI_DA_MOI_THE:
                the.append(hien_tai)
                hien_tai = c
            else:
                hien_tai = f"{hien_tai} {c}".strip()
        if hien_tai:
            the.append(hien_tai)
    return the


def _tld():
    """Nạp tach-loi-doc.py (tên có dấu gạch nên không import thẳng được)."""
    import importlib.util
    d = Path(__file__).resolve().parent / "tach-loi-doc.py"
    spec = importlib.util.spec_from_file_location("tach_loi_doc", d)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


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
    p = argparse.ArgumentParser(
        description="Render Reels/Shorts 9:16 — Sống Tốt (tiếng Việt) hoặc "
                    "One Small Thing (tiếng Anh, thêm --en)")
    p.add_argument("ma_so", help="Mã video, vd VD-001")
    p.add_argument("--en", action="store_true",
                   help="Làm bản tiếng Anh cho kênh One Small Thing: đọc lời từ "
                        "*-loi-doc-en.txt, giọng Piper, logo và lời kêu gọi tiếng Anh")
    p.add_argument("--giong",
                   help=f"Giọng đọc. Mặc định {gv.GIONG_MAC_DINH!r} (VieNeu) hoặc "
                        f"{gp.GIONG_MAC_DINH!r} khi có --en. Xem danh sách: "
                        f"thu-giong-vieneu.py --liet-ke · thu-giong-piper.py --liet-ke")
    p.add_argument("--kieu", default=gv.KIEU_MAC_DINH,
                   choices=["tu_nhien", "tin_tuc", "doc_truyen"],
                   help="Kiểu đọc của VieNeu (bỏ qua khi có --en)")
    p.add_argument("--cham", type=float, default=gp.DO_CHAM_MAC_DINH,
                   help=f"Chỉ dùng với --en: tốc độ đọc, >1 là chậm lại "
                        f"(mặc định %(default)s). Đổi thì nhớ đo lại TOC_DO['EN'] "
                        f"trong tach-loi-doc.py")
    p.add_argument("--nhac", help="File nhạc nền (phải được phép dùng thương mại)")
    p.add_argument("--loi-doc", type=Path,
                   help="Chỉ định file lời đọc khác (mặc định tự tìm bản -v2 trước)")
    p.add_argument("--chi-do-dai", action="store_true",
                   help="Chỉ đọc thử để đo thời lượng, không cần ảnh nền, không render. "
                        "Dùng để kiểm bài có đủ 60 giây chưa trước khi làm tiếp.")
    a = p.parse_args()

    kiem_tra_cong_cu(a.en)

    kenh = "en" if a.en else "vi"
    hau_to = "-reels-en" if a.en else "-reels"

    thu_muc_loi = REPO / "content" / "scripts" / "loi-doc"
    song_ngu = REPO / "content" / "scripts" / "song-ngu" / f"{a.ma_so}-song-ngu.md"

    if a.en:
        ung_vien = (thu_muc_loi / f"{a.ma_so}-loi-doc-en.txt",)
    elif song_ngu.exists():
        # Có file song ngữ thì nó là nguồn thật, và tach-loi-doc.py luôn ghi ra
        # `-loi-doc.txt`. KHÔNG được ngó tới `-loi-doc-v2.txt` nữa: file v2 là di sản
        # từ trước khi có quy trình song ngữ, để nó ưu tiên thì render ra bản chữ cũ
        # mà nhìn video không tài nào biết (đã dính đúng lỗi này với VD-001 ngày 27/07).
        ung_vien = (thu_muc_loi / f"{a.ma_so}-loi-doc.txt",)
    else:
        # Bài chưa có file song ngữ: giữ nếp cũ, ưu tiên bản v2 đã viết lại theo văn nói
        ung_vien = (thu_muc_loi / f"{a.ma_so}-loi-doc-v2.txt",
                    thu_muc_loi / f"{a.ma_so}-loi-doc.txt")
    loi_doc = a.loi_doc or next((f for f in ung_vien if f.exists()), None)
    if not loi_doc or not loi_doc.exists():
        sys.exit(f"❌ Không thấy lời đọc cho {a.ma_so} ({'EN' if a.en else 'VI'}) trong "
                 f"{thu_muc_loi.relative_to(REPO)}\n"
                 f"   Rút ra từ file song ngữ:  python3 scripts/tach-loi-doc.py "
                 f"{a.ma_so}{' --en' if a.en else ''}")

    # File song ngữ là nguồn thật; loi-doc chỉ là bản rút ra. Sửa chữ mà quên rút lại thì
    # render ra video mang chữ cũ, mà nhìn video không tài nào biết — nên phải chặn.
    #
    # So **nội dung** chứ không so giờ sửa file: `tach-loi-doc.py --dong-bo` có ghi lại
    # phần đọc liền mạch nên file song ngữ luôn mới hơn, so giờ thì báo nhầm suốt.
    if song_ngu.exists():
        cu = loi_doc.read_text(encoding="utf-8").split()
        moi = " ".join(_tld().doc_khoi(song_ngu.read_text(encoding="utf-8"),
                                       "EN" if a.en else "VI")).split()
        if moi and cu != moi:
            sys.exit(f"⛔ {loi_doc.name} không khớp {song_ngu.name} — chữ trong file song "
                     f"ngữ đã sửa mà chưa rút ra.\n"
                     f"   Rút lại:  python3 scripts/tach-loi-doc.py {a.ma_so}"
                     f"{' --en' if a.en else ''}")

    anh_nen = [] if a.chi_do_dai else lay_anh(a.ma_so)
    the = tach_the(loi_doc.read_text(encoding="utf-8"))

    lam_viec = REPO / "video" / "edit" / f"{a.ma_so}{hau_to}"
    if lam_viec.exists():
        shutil.rmtree(lam_viec)
    lam_viec.mkdir(parents=True)
    ra = REPO / "video" / "exports" / f"{a.ma_so}{hau_to}.mp4"
    ra.parent.mkdir(parents=True, exist_ok=True)

    ten_giong = a.giong or (gp.GIONG_MAC_DINH if a.en else gv.GIONG_MAC_DINH)
    mo_ta_giong = f"{ten_giong} (chậm {a.cham:g})" if a.en else f"{ten_giong} ({a.kieu})"
    print(f"📝 [{kenh.upper()}] {len(the)} thẻ chữ · "
          f"{'chỉ đo thời lượng' if a.chi_do_dai else f'{len(anh_nen)} ảnh nền'} · "
          f"giọng {mo_ta_giong} · nguồn chữ {loi_doc.name}")

    if a.en:
        print("⏳ Đang nạp model Piper...")
        giong: object = gp.Giong(ten_giong, a.cham)
        loc_the, loc_bai = gp.LOC_TUNG_THE, gp.LOC_TOAN_BAI
    else:
        print("⏳ Đang nạp model VieNeu-TTS v3 Turbo...")
        giong = gv.Giong(ten_giong, a.kieu)
        loc_the, loc_bai = gv.LOC_TUNG_THE, gv.LOC_TOAN_BAI

    wavs: list[Path] = []
    thoi_luong: list[float] = []
    khung: list[Path] = []

    for i, doan in enumerate(the):
        # Giọng đọc từng thẻ → lấy đúng thời lượng tiếng làm thời lượng hình
        tho = lam_viec / f"{i:02d}-tho.wav"
        wav = lam_viec / f"{i:02d}.wav"
        giong.doc(doan, tho)
        chay(["ffmpeg", "-y", "-loglevel", "error", "-i", str(tho),
              "-af", f"{loc_the},apad=pad_dur={KHOANG_LANG}",
              "-ar", "48000", "-ac", "1", "-c:a", "pcm_s16le", str(wav)])

        giay = do_dai(wav)
        wavs.append(wav)
        thoi_luong.append(giay)

        if a.chi_do_dai:
            print(f"   {i + 1:2d}. {giay:5.1f}s  {doan[:52]}{'…' if len(doan) > 52 else ''}")
            continue

        # Ảnh xoay vòng nếu số thẻ nhiều hơn số ảnh
        anh = anh_nen[i * len(anh_nen) // len(the)]
        lop = kr.tao_lop_chu(doan, dau_video=(i == 0), kenh=kenh)
        khung.append(dung_khung(anh, lop, lam_viec, f"{i:02d}"))
        print(f"   {i + 1:2d}. {giay:5.1f}s  {anh.name}  {doan[:46]}{'…' if len(doan) > 46 else ''}")

    tong = sum(thoi_luong) + GIU_KET
    print(f"⏱  Tổng: {tong:.0f}s",
          "✅ trên 60s" if tong > 60 else "⚠️  DƯỚI 60s — cần thêm nội dung")

    if a.chi_do_dai:
        shutil.rmtree(lam_viec, ignore_errors=True)
        return 0

    # Thẻ chốt cuối: câu kết + dòng kêu gọi theo dõi, đứng im 3,2 giây
    ket = kr.tao_lop_chu(the[-1], cta=True, kenh=kenh)
    khung_ket = dung_khung(anh_nen[-1], ket, lam_viec, "ket")

    # ---- Tiếng: ghép các thẻ rồi mới chuẩn hoá độ to MỘT LẦN trên toàn bài ----
    ds_am = lam_viec / "am-thanh.txt"
    ds_am.write_text("".join(f"file '{w}'\n" for w in wavs), encoding="utf-8")
    giong_wav = lam_viec / "giong.wav"
    chay(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", str(ds_am),
          "-af", f"{loc_bai},apad=pad_dur={GIU_KET}",
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
