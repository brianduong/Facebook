#!/usr/bin/env python3
"""Render VIDEO NHÁP 1:1 từ lời đọc — có nhân vật kể, cảnh nền, chữ khớp giọng.

Video ra đăng được ngay. Vẫn gọi là NHÁP vì giọng là giọng máy (Linh của macOS)
→ nên thu lại bằng giọng thật của anh khi có thời gian.

Dùng:
    python3 scripts/render-video-nhap.py VD-001
    python3 scripts/render-video-nhap.py VD-001 --nhan-vat chu --canh ben-mua,duong-cay
    python3 scripts/render-video-nhap.py VD-001 --toc-do 160 --nhac assets/music/nen.mp3
    python3 scripts/render-video-nhap.py VD-001 --nhan-vat khong --canh trong   # nền gradient trơn

Nhân vật: anh (đàn ông trẻ) · chi (phụ nữ trẻ) · chu (đàn ông lớn tuổi) · co (phụ nữ lớn tuổi)
Cảnh nền: sang-cua-so · ban-tra · duong-cay · ben-mua · bep · dem-sao

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
import canh_nen  # noqa: E402
import nhan_dien as nd  # noqa: E402
import nhan_vat as nv  # noqa: E402

TOI_DA_MOI_THE = 100     # ký tự tối đa mỗi thẻ chữ (≈ 4 dòng, vừa vùng chữ)
CHU_MOI_DONG = 26        # ký tự tối đa mỗi dòng
KHOANG_LANG = 0.34       # giây nghỉ sau mỗi thẻ (nói chuyện thì nghỉ ngắn)
GIU_QUOTE = 3.0          # giây giữ ảnh quote cuối video
NHIP_MIENG = 0.16        # giây mỗi lần mở/đóng miệng
AM_LUONG_NHAC = 0.14     # nhạc nền so với giọng đọc
CANH_MAC_DINH = "sang-cua-so,ban-tra,duong-cay"


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
    p.add_argument("--nhan-vat", default="chi",
                   choices=[*nv.KIEU, "khong"], help="Nhân vật kể (mặc định: chi)")
    p.add_argument("--canh", default=CANH_MAC_DINH,
                   help=f"Danh sách cảnh cách nhau bởi dấu phẩy, hoặc 'trong'. Có: {', '.join(canh_nen.CANH)}")
    p.add_argument("--tone", choices=sorted(nd.TONES), default="vua",
                   help="Sắc nền khi dùng --canh trong")
    p.add_argument("--toc-do", type=int, default=155,
                   help="Tốc độ đọc (từ/phút). 138 = đọc, 155 = nói chuyện (mặc định)")
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

    nhan_vat = None if a.nhan_vat == "khong" else a.nhan_vat
    canh_list = [] if a.canh.strip() == "trong" else [c.strip() for c in a.canh.split(",") if c.strip()]
    for c in canh_list:
        if c not in canh_nen.CANH:
            sys.exit(f"❌ Không có cảnh '{c}'. Chọn: {', '.join(canh_nen.CANH)}")

    lam_viec = nd.REPO / "video" / "edit" / f"{a.ma_so}-nhap"
    if lam_viec.exists():
        shutil.rmtree(lam_viec)
    lam_viec.mkdir(parents=True)
    ra = nd.REPO / "video" / "exports" / f"{a.ma_so}-nhap.mp4"
    ra.parent.mkdir(parents=True, exist_ok=True)

    the = tach_doan(loi_doc.read_text(encoding="utf-8"))
    print(f"📝 {len(the)} thẻ chữ · nhân vật: {nhan_vat or 'không'} · "
          f"cảnh: {', '.join(canh_list) or 'nền trơn'} · tốc độ: {a.toc_do} từ/phút")

    wavs: list[Path] = []
    thoi_luong: list[float] = []
    hinh: list[tuple[Path, Path | None]] = []   # (miệng đóng, miệng mở)

    for i, doan in enumerate(the):
        txt = lam_viec / f"{i:02d}.txt"
        aiff = lam_viec / f"{i:02d}.aiff"
        wav = lam_viec / f"{i:02d}.wav"

        # Giọng đọc từng thẻ → lấy đúng thời lượng tiếng làm thời lượng hình
        txt.write_text(doan, encoding="utf-8")
        chay(["say", "-v", "Linh", "-r", str(a.toc_do), "-f", str(txt), "-o", str(aiff)])
        chay(["ffmpeg", "-y", "-loglevel", "error", "-i", str(aiff),
              "-af", f"apad=pad_dur={KHOANG_LANG}", "-ar", "44100", "-ac", "1", str(wav)])

        dong = nd.boc_dong(doan, CHU_MOI_DONG)
        bo_hinh: list[Path] = []
        # Cảnh đổi theo từng khúc video cho đỡ đơn điệu
        canh = canh_list[i * len(canh_list) // len(the)] if canh_list else None

        for ten, mo in (("a", False), ("b", True)):
            svg = lam_viec / f"{i:02d}-{ten}.svg"
            png = lam_viec / f"{i:02d}-{ten}.png"
            if canh:
                svg.write_text(
                    nd.tao_the_video(dong, canh, nhan_vat=nhan_vat, mieng_mo=mo), encoding="utf-8"
                )
            else:
                svg.write_text(
                    nd.tao_svg(dong, tone=a.tone, cta=False, giua=True), encoding="utf-8"
                )
            nd.xuat_png(svg, png)
            bo_hinh.append(png)
            if not (canh and nhan_vat):
                break   # không có người thì khỏi cần khung miệng mở

        giay = do_dai(wav)
        wavs.append(wav)
        thoi_luong.append(giay)
        hinh.append((bo_hinh[0], bo_hinh[1] if len(bo_hinh) > 1 else None))
        print(f"   {i + 1:2d}. {giay:5.1f}s  {doan[:52]}{'…' if len(doan) > 52 else ''}")

    tong = sum(thoi_luong) + GIU_QUOTE
    print(f"⏱  Tổng: {tong:.0f}s", "✅ trên 60s" if tong > 60 else "⚠️  DƯỚI 60s — cần đọc chậm lại hoặc thêm nội dung")

    # Ghép giọng đọc + 3 giây lặng cho ảnh quote cuối
    ds_am = lam_viec / "am-thanh.txt"
    ds_am.write_text("".join(f"file '{w}'\n" for w in wavs), encoding="utf-8")
    giong = lam_viec / "giong.wav"
    chay(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", str(ds_am),
          "-af", f"apad=pad_dur={GIU_QUOTE}", "-c:a", "pcm_s16le", str(giong)])

    # Danh sách hình: mỗi thẻ giữ đúng thời lượng tiếng của nó.
    # Có nhân vật thì đổi qua lại hai khung miệng đóng/mở → trông như đang nói.
    dong_hinh: list[str] = []
    for (dong_png, mo_png), giay in zip(hinh, thoi_luong):
        if mo_png is None:
            dong_hinh.append(f"file '{dong_png}'\nduration {giay:.3f}\n")
            continue
        con_lai = giay
        dang_mo = False
        while con_lai > 0.001:
            khuc = min(NHIP_MIENG, con_lai)
            dong_hinh.append(f"file '{mo_png if dang_mo else dong_png}'\nduration {khuc:.3f}\n")
            dang_mo = not dang_mo
            con_lai -= khuc
    dong_hinh.append(f"file '{quote}'\nduration {GIU_QUOTE}\nfile '{quote}'\n")
    ds_hinh = lam_viec / "hinh.txt"
    ds_hinh.write_text("".join(dong_hinh), encoding="utf-8")

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

    # Zoom vào cực chậm cho khung hình khỏi tĩnh + mờ dần ở đầu và cuối
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
    print("👉 Đây là bản NHÁP: nên thu lại giọng thật khi có thời gian.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
