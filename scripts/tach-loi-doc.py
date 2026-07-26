#!/usr/bin/env python3
"""Rút bản tiếng Việt trong file song ngữ ra thành lời đọc cho máy render.

Anh review và sửa thẳng trong `content/scripts/song-ngu/VD-XXX-song-ngu.md`,
rồi chạy script này. Nó chỉ lấy các khối **VI**, bỏ hết phần **EN** và ghi chú,
ghi ra `content/scripts/loi-doc/VD-XXX-loi-doc.txt` — đúng file mà
`render-video-v2.py` đọc.

    python3 scripts/tach-loi-doc.py VD-003
    python3 scripts/tach-loi-doc.py VD-003 --xem       # chỉ in ra màn hình, không ghi
    python3 scripts/tach-loi-doc.py VD-003 --dong-bo   # chỉ dựng lại phần đọc liền mạch

Chưa duyệt (trạng thái còn ⬜) thì script dừng lại, trừ khi thêm --cu-lam.

Script còn dựng lại phần **"Đọc liền mạch"** ở đầu file song ngữ — EN và VI đầy đủ,
để soi nghĩa một lượt. Phần đó **máy ghép từ các khối bên dưới**, không sửa tay được:
để hai bản chữ trong cùng một file mà sửa hai nơi thì sớm muộn cũng lệch nhau.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent

# Mốc bao quanh phần "Đọc liền mạch" ở đầu file — máy ghép, không sửa tay.
MOC_MO = "<!-- ĐỌC LIỀN MẠCH · máy tự ghép từ các khối bên dưới — đừng sửa ở đây -->"
MOC_DONG = "<!-- HẾT PHẦN ĐỌC LIỀN MẠCH -->"


# Tốc độ đọc (chữ mỗi giây), cân theo thời lượng render thật của VD-003:
#   VI — VieNeu giọng Phạm Tuyên: 251 chữ, 17 thẻ → 69 giây
#   EN — Piper giọng en_US-ryan-high ở length_scale 1.12: 232 chữ, 20 thẻ → 75 giây
# Đổi giọng hoặc đổi `DO_CHAM_MAC_DINH` trong giong_piper.py thì phải đo lại.
TOC_DO = {"VI": 4.28, "EN": 3.66}

TOI_DA_MOI_THE = 92     # phải khớp hằng số cùng tên trong render-video-v2.py


def uoc_so_the(khoi: list[str]) -> int:
    """Ước số thẻ chữ mà render-video-v2.py sẽ cắt ra.

    Thẻ không vắt qua hai khối, mỗi thẻ tối đa 92 ký tự, và câu hook luôn đứng riêng.
    Chỉ là ước — con số thật lấy bằng `render-video-v2.py --chi-do-dai`.
    """
    so = sum(max(1, -(-len(k) // TOI_DA_MOI_THE)) for k in khoi)
    return so + 1 if khoi and len(khoi[0]) > TOI_DA_MOI_THE else so


def uoc_thoi_luong(so_chu: int, so_the: int, nhan: str = "VI") -> float:
    """Ước thời lượng video: thời gian đọc + khoảng lặng giữa thẻ + đoạn giữ thẻ chốt
    (`KHOANG_LANG` và `GIU_KET` trong render-video-v2.py)."""
    return so_chu / TOC_DO[nhan] + so_the * 0.42 + 3.2


def bo_phan_may_ghep(noi_dung: str) -> str:
    """Cắt phần "Đọc liền mạch" ra trước khi đọc khối, để không đếm chữ hai lần."""
    dau, cuoi = noi_dung.find(MOC_MO), noi_dung.find(MOC_DONG)
    if dau == -1 or cuoi == -1 or cuoi < dau:
        return noi_dung
    return noi_dung[:dau] + noi_dung[cuoi + len(MOC_DONG):]


def doc_khoi(noi_dung: str, nhan: str) -> list[str]:
    """Lấy nội dung mọi khối `**EN**` hoặc `**VI**` (blockquote ngay bên dưới nhãn)."""
    khoi: list[str] = []
    dong = bo_phan_may_ghep(noi_dung).splitlines()
    i = 0
    while i < len(dong):
        if dong[i].strip() in (f"**{nhan}**", f"**{nhan}**:"):
            i += 1
            while i < len(dong) and not dong[i].strip():   # bỏ dòng trống đệm
                i += 1
            cau: list[str] = []
            while i < len(dong) and dong[i].lstrip().startswith(">"):
                cau.append(dong[i].lstrip()[1:].strip())
                i += 1
            noi = " ".join(c for c in cau if c).strip()
            if noi:
                khoi.append(noi)
        else:
            i += 1
    return khoi


def dung_phan_lien_mach(en: list[str], vi: list[str], giay: float) -> str:
    """Ghép phần "Đọc liền mạch" đặt ở đầu file song ngữ."""
    dong = [
        MOC_MO,
        "",
        "## Đọc liền mạch",
        "",
        "_Phần này máy ghép lại từ các khối bên dưới, chỉ để soi nghĩa một lượt._",
        "_Muốn sửa chữ thì sửa ở khối bên dưới rồi chạy `tach-loi-doc.py` — phần này tự cập nhật._",
        "",
        "### EN — bản gốc",
        "",
        *_xen_dong_trong(en),
        "",
        f"### VI — lời đọc trong video _(≈ {giay:.0f} giây)_",
        "",
        *_xen_dong_trong(vi),
        "",
        MOC_DONG,
    ]
    return "\n".join(dong)


def _xen_dong_trong(doan: list[str]) -> list[str]:
    ra: list[str] = []
    for i, d in enumerate(doan):
        if i:
            ra.append("")
        ra.append(d)
    return ra


def dong_bo_lien_mach(noi_dung: str, phan: str) -> tuple[str, bool]:
    """Thay (hoặc chèn mới) phần "Đọc liền mạch". Trả về nội dung mới + có đổi không."""
    dau, cuoi = noi_dung.find(MOC_MO), noi_dung.find(MOC_DONG)
    if dau != -1 and cuoi != -1 and cuoi > dau:
        het = cuoi + len(MOC_DONG)
        if noi_dung[dau:het] == phan:
            return noi_dung, False
        return noi_dung[:dau] + phan + noi_dung[het:], True

    # Chưa có → chèn ngay trước khối đầu tiên (`## 1 · ...`)
    m = re.search(r"^##\s+1\s+·", noi_dung, re.M)
    if not m:
        return noi_dung, False
    return noi_dung[:m.start()] + phan + "\n\n---\n\n" + noi_dung[m.start():], True


def main() -> None:
    p = argparse.ArgumentParser(description="Rút bản VI trong file song ngữ ra lời đọc")
    p.add_argument("ma_so", help="Mã video, ví dụ VD-003")
    p.add_argument("--en", action="store_true",
                   help="Rút khối EN (kênh One Small Thing) thay vì khối VI")
    p.add_argument("--xem", action="store_true", help="Chỉ in ra, không ghi file")
    p.add_argument("--dong-bo", action="store_true",
                   help="Chỉ dựng lại phần 'Đọc liền mạch', chưa duyệt cũng chạy được")
    p.add_argument("--cu-lam", action="store_true", help="Ghi kể cả khi chưa duyệt")
    a = p.parse_args()

    nhan = "EN" if a.en else "VI"

    nguon = REPO / "content" / "scripts" / "song-ngu" / f"{a.ma_so}-song-ngu.md"
    if not nguon.exists():
        sys.exit(f"❌ Không thấy {nguon.relative_to(REPO)}")

    noi_dung = nguon.read_text(encoding="utf-8")

    da_duyet = bool(re.search(r"\*\*Trạng thái duyệt:\*\*.*✅", noi_dung))
    if not da_duyet and not a.xem and not a.dong_bo and not a.cu_lam:
        sys.exit(f"⛔ {a.ma_so} chưa duyệt.\n"
                 f"   Sửa dòng '**Trạng thái duyệt:**' trong {nguon.name} thành ✅ đã duyệt,\n"
                 f"   hoặc chạy lại với --cu-lam nếu muốn bỏ qua.\n"
                 f"   (Muốn dựng lại phần đọc liền mạch thôi thì dùng --dong-bo.)")

    khoi = doc_khoi(noi_dung, nhan)
    if not khoi:
        sys.exit(f"❌ Không tìm thấy khối **{nhan}** nào. Xem lại định dạng file song ngữ.")

    loi_doc = "\n\n".join(khoi) + "\n"
    so_chu = len(loi_doc.split())
    giay = uoc_thoi_luong(so_chu, uoc_so_the(khoi), nhan)
    canh_bao = "  ⚠️ dưới 60 giây — Reels/Shorts nên dài hơn" if giay < 62 else ""

    # Dựng lại phần đọc liền mạch ở đầu file song ngữ (trừ khi chỉ xem)
    if not a.xem:
        khoi_vi = doc_khoi(noi_dung, "VI")
        moi, da_doi = dong_bo_lien_mach(noi_dung, dung_phan_lien_mach(
            doc_khoi(noi_dung, "EN"), khoi_vi,
            uoc_thoi_luong(len(" ".join(khoi_vi).split()), uoc_so_the(khoi_vi), "VI")))
        if da_doi:
            nguon.write_text(moi, encoding="utf-8")
            print(f"🔄 Đã dựng lại phần 'Đọc liền mạch' trong {nguon.name}")

    if a.xem:
        print(loi_doc)
        print(f"— [{nhan}] {len(khoi)} khối · {so_chu} chữ · ước chừng {giay:.0f} giây{canh_bao}",
              file=sys.stderr)
        return
    if a.dong_bo:
        print(f"   [{nhan}] {len(khoi)} khối · {so_chu} chữ · ước chừng {giay:.0f} giây{canh_bao}")
        return

    hau_to = "-loi-doc-en.txt" if a.en else "-loi-doc.txt"
    dich = REPO / "content" / "scripts" / "loi-doc" / f"{a.ma_so}{hau_to}"
    dich.parent.mkdir(parents=True, exist_ok=True)
    ghi_de = dich.exists()
    dich.write_text(loi_doc, encoding="utf-8")

    print(f"{'♻️  Ghi đè' if ghi_de else '✅ Đã tạo'} {dich.relative_to(REPO)}")
    print(f"   [{nhan}] {len(khoi)} khối · {so_chu} chữ · ước chừng {giay:.0f} giây{canh_bao}")


if __name__ == "__main__":
    main()
