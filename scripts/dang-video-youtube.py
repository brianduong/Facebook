#!/usr/bin/env python3
"""Đăng video lên hai kênh YouTube — tiếng Anh (One Small Thing) và tiếng Việt (Sống Tốt).

Tiêu đề, mô tả và thẻ được bóc thẳng từ file caption trong `content/captions/`,
nên không phải gõ lại chữ, và không sợ dán nhầm bài.

Cần chạy bằng Python của môi trường `.venv-dang`, KHÔNG phải `python3`:

    # 0. Xin quyền lần đầu cho từng kênh (mở trình duyệt, làm một lần)
    .venv-dang/bin/python scripts/dang-video-youtube.py xin-quyen --kenh en

    # 1. Kiểm tra đang nối vào đúng kênh nào
    .venv-dang/bin/python scripts/dang-video-youtube.py kiem-tra --kenh en

    # 2. Xem trước những gì sẽ gửi (KHÔNG đăng thật)
    .venv-dang/bin/python scripts/dang-video-youtube.py dang VD-009 --kenh en

    # 3. Đăng thật
    .venv-dang/bin/python scripts/dang-video-youtube.py dang VD-009 --kenh en --dang-that

Mặc định là **chạy thử** — chỉ in ra những gì sẽ gửi. Phải thêm `--dang-that` mới đăng.

⚠️ Video đăng qua API từ project chưa qua vòng audit của Google sẽ **bị khoá ở chế độ
riêng tư**, dù mình xin `public`. Đó là chính sách của YouTube, không lách được bằng code.
Nên mặc định script để `private`, đăng xong anh vào Studio bấm công khai.
Xem `docs/huong-dan-dang-youtube.md`.
"""

import argparse
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent

# Chỉ xin quyền tải lên và quyền đọc. Không xin `force-ssl` vì quyền đó kèm cả xoá
# video — mình không cần, mà lỡ hỏng thì mất bài.
# Quyền đọc để `kiem-tra` in được tên kênh đang nối: hai kênh nằm chung một tài khoản
# Google nên đây là chốt chặn duy nhất phát hiện xin quyền nhầm kênh.
PHAM_VI = [
    "https://www.googleapis.com/auth/youtube.upload",
    "https://www.googleapis.com/auth/youtube.readonly",
]

THU_MUC_BI_MAT = "secrets"

# Danh mục "Con người và Blog" (People & Blogs) — đã chốt cho cả hai kênh, mọi video.
DANH_MUC_NGUOI_VA_BLOG = "22"

KENH = {
    "en": {
        "ten": "YouTube tiếng Anh — One Small Thing",
        "handle": "@onesmallthingdaily",
        "caption": "{ma}-caption-en.md",
        "video": "{ma}-reels-en.mp4",
        "token": "youtube-token-en.json",
        "ngon_ngu": "en",
    },
    "vi": {
        "ten": "YouTube tiếng Việt — Sống Tốt",
        "handle": "@songtotdaily",
        "caption": "{ma}-caption.md",
        "video": "{ma}-reels.mp4",
        "token": "youtube-token-vi.json",
        "ngon_ngu": "vi",
    },
}

# Giới hạn của YouTube — vượt là API trả lỗi khó hiểu, nên chặn từ đây cho dễ sửa.
MAX_TIEU_DE = 100
MAX_MO_TA = 5000
MAX_THE_TONG = 500


def _thieu_thu_vien(loi: ImportError) -> None:
    sys.exit(
        f"❌ Thiếu thư viện Google ({loi.name}).\n"
        "   Script này phải chạy bằng Python của .venv-dang, không phải python3:\n"
        "     .venv-dang/bin/python scripts/dang-video-youtube.py ...\n"
        "   Chưa có môi trường thì dựng lại:\n"
        "     /usr/local/opt/python@3.13/bin/python3.13 -m venv .venv-dang\n"
        "     .venv-dang/bin/pip install google-api-python-client google-auth-oauthlib"
    )


def lay_dich_vu(ma_kenh: str, cho_dang_nhap: bool = False):
    """Trả về đối tượng gọi API YouTube của đúng kênh đang chọn."""
    try:
        from google.auth.transport.requests import Request
        from google.oauth2.credentials import Credentials
        from google_auth_oauthlib.flow import InstalledAppFlow
        from googleapiclient.discovery import build
    except ImportError as loi:
        _thieu_thu_vien(loi)

    thu_muc = REPO / THU_MUC_BI_MAT
    f_token = thu_muc / KENH[ma_kenh]["token"]
    f_secret = thu_muc / "youtube-client.json"
    quyen = None

    if f_token.exists():
        quyen = Credentials.from_authorized_user_file(str(f_token), PHAM_VI)

    if quyen and quyen.expired and quyen.refresh_token:
        from google.auth.exceptions import RefreshError

        try:
            quyen.refresh(Request())
        except RefreshError:
            # Hay gặp nhất: màn hình đồng ý còn ở chế độ "Testing" → Google thu hồi
            # refresh token sau 7 ngày. Xoá token cũ rồi xin lại.
            f_token.unlink(missing_ok=True)
            quyen = None

    if not quyen or not quyen.valid:
        if not cho_dang_nhap:
            sys.exit(
                f"❌ Chưa có quyền cho kênh {KENH[ma_kenh]['ten']} (hoặc quyền đã hết hạn).\n"
                f"   Chạy: .venv-dang/bin/python scripts/dang-video-youtube.py xin-quyen --kenh {ma_kenh}"
            )
        if not f_secret.exists():
            sys.exit(
                f"❌ Không thấy {THU_MUC_BI_MAT}/youtube-client.json\n"
                "   Đây là file Google Cloud cho tải về khi tạo OAuth client (Desktop app).\n"
                "   Các bước lấy: docs/huong-dan-dang-youtube.md (mục A)"
            )
        luong = InstalledAppFlow.from_client_secrets_file(str(f_secret), PHAM_VI)
        print(f"🌐 Đang mở trình duyệt để xin quyền cho: {KENH[ma_kenh]['ten']}")
        print(f"   ⚠️ Nhớ chọn đúng tài khoản đang quản lý kênh {KENH[ma_kenh]['handle']}")
        quyen = luong.run_local_server(port=0, prompt="consent")
        thu_muc.mkdir(mode=0o700, exist_ok=True)
        f_token.write_text(quyen.to_json(), encoding="utf-8")
        f_token.chmod(0o600)
        print(f"✅ Đã lưu quyền vào {THU_MUC_BI_MAT}/{f_token.name} (không lên GitHub)")

    return build("youtube", "v3", credentials=quyen, cache_discovery=False)


def _boc_khoi(noi_dung: str, ten_muc: str) -> str | None:
    """Lấy khối ``` đầu tiên nằm ngay dưới tiêu đề mục khớp `ten_muc`.

    File caption có nhiều khối ``` (kể cả mục "Tiêu đề dự phòng" ở cuối), nên phải
    neo theo tiêu đề mục rồi lấy khối liền sau, không được quét cả file.
    """
    dau_muc = re.compile(
        rf"^##\s*(?:\d+\s*[·.]\s*)?{ten_muc}\b(?!\s*dự phòng)", re.M | re.I
    )
    m = dau_muc.search(noi_dung)
    if not m:
        return None
    khoi = re.search(r"```[a-z]*\n(.*?)\n```", noi_dung[m.end():], re.S)
    return khoi.group(1).strip() if khoi else None


def doc_caption(ma_so: str, ma_kenh: str) -> dict:
    """Bóc tiêu đề · mô tả · thẻ từ file caption của kênh tương ứng."""
    f = REPO / "content" / "captions" / KENH[ma_kenh]["caption"].format(ma=ma_so)
    if not f.exists():
        sys.exit(f"❌ Không thấy file caption {f.relative_to(REPO)}")
    noi_dung = f.read_text(encoding="utf-8")

    # File tiếng Việt có cả phần Facebook lẫn phần YouTube trong một file.
    # Cắt bỏ phần trên để không bóc nhầm caption Facebook.
    if ma_kenh == "vi":
        moc = re.search(r"^#\s*Đăng YouTube", noi_dung, re.M)
        if not moc:
            sys.exit(
                f"❌ {f.name} không có mục '# Đăng YouTube Shorts'.\n"
                "   File caption đời cũ (VD-001 → VD-003) viết theo khuôn khác — phải sửa\n"
                "   thành khuôn mới trước khi đăng bằng script."
            )
        noi_dung = noi_dung[moc.start():]

    tieu_de = _boc_khoi(noi_dung, "Tiêu đề")
    mo_ta = _boc_khoi(noi_dung, "Mô tả")
    the = _boc_khoi(noi_dung, "Thẻ")

    thieu = [t for t, v in (("Tiêu đề", tieu_de), ("Mô tả", mo_ta), ("Thẻ", the)) if not v]
    if thieu:
        sys.exit(f"❌ {f.name} thiếu mục: {' · '.join(thieu)}")

    return {
        "tieu_de": tieu_de,
        "mo_ta": mo_ta,
        "the": [t.strip() for t in the.split(",") if t.strip()],
        "nguon": f.relative_to(REPO),
    }


def soi_loi(bai: dict, ma_kenh: str) -> list[str]:
    """Những chỗ YouTube sẽ từ chối hoặc mình sẽ tiếc — soi trước khi gửi."""
    canh_bao = []
    if len(bai["tieu_de"]) > MAX_TIEU_DE:
        canh_bao.append(f"Tiêu đề {len(bai['tieu_de'])} ký tự, quá {MAX_TIEU_DE} — YouTube sẽ từ chối")
    if len(bai["mo_ta"]) > MAX_MO_TA:
        canh_bao.append(f"Mô tả {len(bai['mo_ta'])} ký tự, quá {MAX_MO_TA} — YouTube sẽ từ chối")
    tong_the = sum(len(t) for t in bai["the"]) + len(bai["the"])
    if tong_the > MAX_THE_TONG:
        canh_bao.append(f"Thẻ cộng lại {tong_the} ký tự, quá {MAX_THE_TONG} — YouTube sẽ từ chối")
    if "<" in bai["mo_ta"] or ">" in bai["mo_ta"]:
        canh_bao.append("Mô tả có dấu < hoặc > — YouTube cấm, sẽ từ chối cả bài")
    if "#Shorts" not in bai["tieu_de"] and "#shorts" not in bai["tieu_de"].lower():
        canh_bao.append("Tiêu đề không có #Shorts — YouTube dễ xếp nhầm sang video thường")
    if "Pexels" not in bai["mo_ta"]:
        canh_bao.append("Mô tả thiếu dòng ghi nguồn Pexels — điều khoản API Pexels bắt buộc")
    return canh_bao


def tai_len(dich_vu, f_video: Path, bai: dict, ma_kenh: str, che_do: str, hen_gio: str | None):
    try:
        from googleapiclient.errors import HttpError
        from googleapiclient.http import MediaFileUpload
    except ImportError as loi:
        _thieu_thu_vien(loi)

    than = {
        "snippet": {
            "title": bai["tieu_de"],
            "description": bai["mo_ta"],
            "tags": bai["the"],
            "categoryId": DANH_MUC_NGUOI_VA_BLOG,
            "defaultLanguage": KENH[ma_kenh]["ngon_ngu"],
            "defaultAudioLanguage": KENH[ma_kenh]["ngon_ngu"],
        },
        "status": {
            "privacyStatus": che_do,
            # Bắt buộc phải trả lời, không khai thì YouTube treo video lại.
            "selfDeclaredMadeForKids": False,
        },
    }
    if hen_gio:
        # Hẹn giờ chỉ chạy khi video đang ở chế độ riêng tư.
        than["status"]["privacyStatus"] = "private"
        than["status"]["publishAt"] = hen_gio

    tai = MediaFileUpload(str(f_video), chunksize=4 * 1024 * 1024, resumable=True)
    yeu_cau = dich_vu.videos().insert(part="snippet,status", body=than, media_body=tai)

    print("⏳ Đang tải lên...")
    phan_hoi = None
    while phan_hoi is None:
        try:
            tien_do, phan_hoi = yeu_cau.next_chunk()
        except HttpError as loi:
            if loi.resp.status in (500, 502, 503, 504):
                print(f"   ⚠️ YouTube trả lỗi {loi.resp.status}, thử lại...")
                continue
            _bao_loi_http(loi)
        if tien_do:
            print(f"   {int(tien_do.progress() * 100)}%")
    return phan_hoi


def _bao_loi_http(loi) -> None:
    """Dịch mấy lỗi hay gặp sang tiếng người."""
    text = str(loi)
    if "quotaExceeded" in text:
        sys.exit(
            "❌ Hết hạn mức API trong ngày.\n"
            "   Mỗi lần đăng tốn 1.600 điểm, một ngày có 10.000 điểm → tối đa 6 video/ngày.\n"
            "   Hạn mức reset lúc 0h theo giờ Thái Bình Dương (khoảng 14–15h giờ Việt Nam)."
        )
    if "youtubeSignupRequired" in text:
        sys.exit("❌ Tài khoản Google này chưa có kênh YouTube nào. Kiểm tra lại đăng nhập đúng tài khoản chưa.")
    if "forbidden" in text.lower() or "insufficientPermissions" in text:
        sys.exit(
            "❌ Không đủ quyền. Hay gặp nhất là lúc xin quyền đã chọn nhầm tài khoản Google.\n"
            "   Xoá file token của kênh đó rồi chạy lại `xin-quyen`."
        )
    sys.exit(f"❌ YouTube báo lỗi: {text}")


def main() -> int:
    p = argparse.ArgumentParser(description="Đăng video lên YouTube")
    p.add_argument("viec", choices=["xin-quyen", "kiem-tra", "dang"])
    p.add_argument("ma", nargs="?", help="Mã video, vd VD-009")
    p.add_argument("--kenh", choices=["en", "vi"], required=True, help="en = tiếng Anh · vi = tiếng Việt")
    p.add_argument("--video", help="Đường dẫn file video (mặc định lấy theo mã)")
    p.add_argument(
        "--che-do",
        choices=["private", "unlisted", "public"],
        default="private",
        help="Mặc định private — project chưa qua audit thì YouTube ép về private dù xin public",
    )
    p.add_argument("--hen-gio", help="Hẹn giờ công khai, dạng 2026-08-03T20:00:00+07:00")
    p.add_argument("--dang-that", action="store_true", help="Đăng thật (mặc định chỉ chạy thử)")
    a = p.parse_args()

    kenh = KENH[a.kenh]

    if a.viec == "xin-quyen":
        lay_dich_vu(a.kenh, cho_dang_nhap=True)
        print("✅ Xong. Giờ chạy `kiem-tra` để chắc là đã nối đúng kênh.")
        return 0

    if a.viec == "kiem-tra":
        dich_vu = lay_dich_vu(a.kenh)
        # channels.list mine=true không nằm trong phạm vi youtube.upload nên có thể bị từ
        # chối; khi đó vẫn coi như đạt vì token đã dùng được để dựng dịch vụ.
        try:
            from googleapiclient.errors import HttpError

            kq = dich_vu.channels().list(part="snippet,statistics", mine=True).execute()
            muc = kq.get("items", [])
            if not muc:
                sys.exit("❌ Tài khoản này không quản lý kênh YouTube nào.")
            c = muc[0]
            print(f"✅ Đang nối vào: {c['snippet']['title']}")
            print(f"   Mong đợi:     {kenh['ten']} ({kenh['handle']})")
            tk = c.get("statistics", {})
            if tk.get("subscriberCount"):
                print(f"   Người đăng ký: {int(tk['subscriberCount']):,}")
            if tk.get("videoCount"):
                print(f"   Số video:      {tk['videoCount']}")
            print("\n👉 Tên kênh ở trên có khớp dòng 'Mong đợi' không? Lệch là đã xin quyền nhầm tài khoản.")
        except HttpError:
            print(f"✅ Quyền dùng được cho kênh {kenh['ten']}.")
            print("   (Không đọc được tên kênh vì script chỉ xin quyền tải lên, không xin quyền đọc.)")
        return 0

    if not a.ma:
        sys.exit("❌ Thiếu mã video. Vd: dang VD-009 --kenh en")

    f_video = Path(a.video) if a.video else REPO / "video" / "exports" / kenh["video"].format(ma=a.ma)
    if not f_video.is_absolute():
        f_video = REPO / f_video
    if not f_video.exists():
        sys.exit(f"❌ Không thấy file video {f_video}")

    bai = doc_caption(a.ma, a.kenh)
    canh_bao = soi_loi(bai, a.kenh)

    print("─" * 68)
    print(f"Kênh:     {kenh['ten']} ({kenh['handle']})")
    print(f"Video:    {f_video.relative_to(REPO)} · {f_video.stat().st_size / 1e6:.1f} MB")
    print(f"Chữ lấy:  {bai['nguon']}")
    print("─" * 68)
    print(f"TIÊU ĐỀ ({len(bai['tieu_de'])}/{MAX_TIEU_DE})")
    print(f"  {bai['tieu_de']}")
    print(f"\nMÔ TẢ ({len(bai['mo_ta'])}/{MAX_MO_TA})")
    for dong in bai["mo_ta"].splitlines():
        print(f"  {dong}")
    print(f"\nTHẺ ({len(bai['the'])} thẻ)")
    print(f"  {', '.join(bai['the'])}")
    print(f"\nDanh mục: Con người và Blog · Trẻ em: không · Chế độ: {a.che_do}")
    if a.hen_gio:
        print(f"Hẹn giờ:  {a.hen_gio}")
    print("─" * 68)

    if canh_bao:
        print("⚠️ Soi thấy mấy chỗ này:")
        for c in canh_bao:
            print(f"   · {c}")
        print("─" * 68)

    if not a.dang_that:
        print("🟡 Đang chạy thử, chưa gửi gì lên YouTube.")
        print("   Ưng rồi thì thêm --dang-that.")
        return 0

    chan = [c for c in canh_bao if "sẽ từ chối" in c]
    if chan:
        sys.exit("❌ Không đăng — có chỗ YouTube chắc chắn từ chối. Sửa file caption trước.")

    # Chỉ xin quyền khi đăng thật, để xem trước chạy được cả lúc chưa có token.
    dich_vu = lay_dich_vu(a.kenh)
    kq = tai_len(dich_vu, f_video, bai, a.kenh, a.che_do, a.hen_gio)
    vid = kq["id"]
    che_do_that = kq.get("status", {}).get("privacyStatus", a.che_do)

    print(f"\n✅ Đã đăng. https://youtu.be/{vid}")
    print(f"   Sửa trong Studio: https://studio.youtube.com/video/{vid}/edit")

    if che_do_that != a.che_do:
        print(
            f"\n⚠️ Xin '{a.che_do}' nhưng YouTube để '{che_do_that}'.\n"
            "   Đúng như dự đoán: project chưa qua audit thì video bị khoá riêng tư.\n"
            "   Vào Studio bấm công khai bằng tay là xong."
        )
    elif che_do_that == "private" and not a.hen_gio:
        print("\n👉 Video đang riêng tư. Vào Studio bấm công khai khi muốn lên sóng.")

    print("👉 Nhớ đánh dấu ✅ vào schedule/calendar.md")
    return 0


if __name__ == "__main__":
    sys.exit(main())
