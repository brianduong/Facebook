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

    # 4. Đọc lượt xem từng video, kèm tuổi (để đọc số 48 giờ)
    .venv-dang/bin/python scripts/dang-video-youtube.py so-lieu --kenh vi

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
    # Cần cho lệnh `doi-lich`: sửa `publishAt` của video đã tải lên.
    # `youtube.upload` chỉ cho tạo mới, gọi videos.update là 403 insufficientPermissions.
    # Thêm phạm vi này thì token cũ hết dùng được — phải chạy lại `xin-quyen` cả hai kênh.
    "https://www.googleapis.com/auth/youtube",
    # Cần cho lệnh `binh-luan`. Mọi thao tác bình luận của YouTube đều đòi phạm vi này,
    # kể cả chỉ ĐỌC: đã đo ngày 03/09 với token có đủ upload + readonly + youtube, gọi
    # `commentThreads.list` vẫn trả 403 insufficient scopes.
    # ⚠️ Phạm vi này **kèm cả quyền xoá video**. Dự án cố ý né nó tới 03/09 mới thêm, vì
    # hai lẽ: dán bình luận tự thú cho VD-018, và đọc bình luận người xem làm nguyên liệu
    # nghĩ ý mới (kho ý tưởng cạn từ VD-037). Anh chốt 03/09.
    # ⚠️ Script này KHÔNG bao giờ gọi videos.delete — đừng thêm lệnh xoá vào đây.
    "https://www.googleapis.com/auth/youtube.force-ssl",
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
        # `select_account` là chỗ mấu chốt, đừng bỏ. Hai kênh Sống Tốt và One Small Thing
        # nằm CHUNG một tài khoản Google, nên khâu chọn kênh mới là khâu quyết định token
        # này thuộc kênh nào. Chỉ `prompt="consent"` thì Google hiện lại màn hình đồng ý
        # nhưng **dùng lại kênh đã chọn lần trước, không hỏi lại** — đó là cách token `vi`
        # nối nhầm vào One Small Thing hai lần: 15/08 và 03/09.
        quyen = luong.run_local_server(port=0, prompt="select_account consent")
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
        # Bai VD-xxx dung anh Pexels, bai QX-xxx (QuayXe) dung art tu ve.
        "dung_pexels": ma_so.upper().startswith("VD-"),
    }


def doc_binh_luan_ghim(ma_so: str, ma_kenh: str) -> str:
    """Bóc câu bình luận soạn sẵn trong mục nhắc cuối file caption.

    Khuôn: mục "## Nhắc khi đăng" (bản Việt) hoặc "## Posting notes" (bản Anh), khối ```
    đầu tiên nằm trong đó. Chỉ bài nào cố ý cần bình luận mở hàng mới có khối này —
    không có thì báo lỗi chứ đừng tự nghĩ chữ thay.
    """
    f = REPO / "content" / "captions" / KENH[ma_kenh]["caption"].format(ma=ma_so)
    if not f.exists():
        sys.exit(f"❌ Không thấy file caption {f.relative_to(REPO)}")
    noi_dung = f.read_text(encoding="utf-8")

    ten_muc = "Nhắc khi đăng" if ma_kenh == "vi" else "Posting notes"
    moc = re.search(rf"^##\s*{ten_muc}\b", noi_dung, re.M)
    if not moc:
        sys.exit(f"❌ {f.name} không có mục '## {ten_muc}'.")

    # Chặn ở mục kế tiếp: "Tiêu đề dự phòng" / "Alternate titles" cũng có khối ```.
    phan = noi_dung[moc.end():]
    het = re.search(r"^##\s", phan, re.M)
    if het:
        phan = phan[: het.start()]

    # Khối này nằm lồng trong một gạch đầu dòng nên thụt lề — phải bắt lấy phần thụt
    # rồi gỡ ra, không thì chữ đăng lên kèm hai dấu cách đầu dòng.
    khoi = re.search(r"^([ \t]*)```[a-z]*\n(.*?)\n\1```", phan, re.S | re.M)
    if not khoi:
        sys.exit(
            f"❌ {f.name} mục '## {ten_muc}' không có khối ``` nào.\n"
            "   Bài này không soạn sẵn bình luận mở hàng — viết câu vào file caption trước,\n"
            "   đừng để script tự nghĩ chữ."
        )
    thut = khoi.group(1)
    dong = [d[len(thut):] if d.startswith(thut) else d for d in khoi.group(2).splitlines()]
    return "\n".join(dong).strip()


def dang_binh_luan(dich_vu, video_id: str, chu: str) -> str:
    """Đăng một bình luận gốc lên video. Trả về id của bình luận."""
    kq = (
        dich_vu.commentThreads()
        .insert(
            part="snippet",
            body={
                "snippet": {
                    "videoId": video_id,
                    "topLevelComment": {"snippet": {"textOriginal": chu}},
                }
            },
        )
        .execute()
    )
    return kq["id"]


def tim_video(dich_vu, tieu_de: str) -> str | None:
    """Tìm video trên kênh theo đúng tiêu đề. Trả về video id, không thấy thì None.

    Dùng cho `doi-lich`: mã bài không nằm trên YouTube, chỉ có tiêu đề trong file caption.
    Phải duyệt playlist `uploads` chứ không dùng `search.list` — search bỏ qua video riêng tư,
    mà bài đang hẹn giờ thì luôn riêng tư.
    """
    kenh = dich_vu.channels().list(part="contentDetails", mine=True).execute()
    uploads = kenh["items"][0]["contentDetails"]["relatedPlaylists"]["uploads"]

    ids, trang = [], None
    while True:
        r = dich_vu.playlistItems().list(
            part="contentDetails", playlistId=uploads, maxResults=50, pageToken=trang
        ).execute()
        ids += [m["contentDetails"]["videoId"] for m in r["items"]]
        trang = r.get("nextPageToken")
        if not trang:
            break

    for i in range(0, len(ids), 50):
        r = dich_vu.videos().list(part="snippet", id=",".join(ids[i:i + 50])).execute()
        for v in r["items"]:
            if v["snippet"]["title"].strip() == tieu_de.strip():
                return v["id"]
    return None


def doi_lich(dich_vu, vid: str, hen_gio: str) -> dict:
    """Dời mốc `publishAt` của một video đã tải lên, giữ nguyên mọi thiết lập khác."""
    from datetime import datetime, timezone

    cu = dich_vu.videos().list(part="status,snippet", id=vid).execute()["items"][0]
    if cu["status"]["privacyStatus"] != "private":
        sys.exit(
            f"❌ Video {vid} đang ở chế độ '{cu['status']['privacyStatus']}', không phải hẹn giờ nữa.\n"
            "   Đã công khai rồi thì không dời lịch được — chỉ còn cách gỡ hoặc để nguyên."
        )

    moc_utc = datetime.fromisoformat(hen_gio).astimezone(timezone.utc)
    ra = dich_vu.videos().update(part="status", body={
        "id": vid,
        "status": {
            "privacyStatus": "private",
            "publishAt": moc_utc.strftime("%Y-%m-%dT%H:%M:%SZ"),
            "selfDeclaredMadeForKids": cu["status"].get("selfDeclaredMadeForKids", False),
            "license": cu["status"].get("license", "youtube"),
            "embeddable": cu["status"].get("embeddable", True),
            "publicStatsViewable": cu["status"].get("publicStatsViewable", True),
        },
    }).execute()
    return {"truoc": cu["status"].get("publishAt"), "sau": ra["status"].get("publishAt"),
            "tieu_de": cu["snippet"]["title"]}


def tim_hoac_tao_playlist(dich_vu, ten: str, mo_ta: str = "") -> str:
    """Tra ve id playlist ten `ten`, tao moi neu chua co. Khong bao gio tao trung.

    Playlist de gom video QuayXe mot cho, khong tron voi 33 bai cu cua kenh.
    Luu y: nguoi xem Shorts luot trong luong doc, khong mo playlist - cai nay
    chi giup trang kenh gon gang.
    """
    trang = None
    while True:
        r = dich_vu.playlists().list(part="snippet", mine=True, maxResults=50,
                                     pageToken=trang).execute()
        for x in r["items"]:
            if x["snippet"]["title"].strip().lower() == ten.strip().lower():
                return x["id"]
        trang = r.get("nextPageToken")
        if not trang:
            break
    r = dich_vu.playlists().insert(
        part="snippet,status",
        body={"snippet": {"title": ten, "description": mo_ta},
              "status": {"privacyStatus": "public"}},
    ).execute()
    return r["id"]


def them_vao_playlist(dich_vu, playlist_id: str, video_id: str) -> None:
    dich_vu.playlistItems().insert(
        part="snippet",
        body={"snippet": {"playlistId": playlist_id,
                          "resourceId": {"kind": "youtube#video", "videoId": video_id}}},
    ).execute()


def duong_dan_gon(f: Path) -> str:
    """Duong dan de doc. File video co the nam NGOAI repo nay.

    Du an QuayXe (/Users/mac/Miganet/QuayXe) dung chung script nay va tro
    `--video` thang sang thu muc cua no, nen relative_to(REPO) se nem ValueError.
    """
    try:
        return str(f.relative_to(REPO))
    except ValueError:
        return str(f)


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
    # Chi bai dung anh Pexels moi phai ghi nguon. Bai QuayXe dung art tu ve nen
    # khong rang buoc - truoc day rang buoc chung nen moi bai QuayXe deu bao nham.
    if bai.get("dung_pexels", True) and "Pexels" not in bai["mo_ta"]:
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


def ban_do_tieu_de(ma_kenh: str) -> dict[str, str]:
    """Tiêu đề → mã bài, bóc từ mọi file caption của kênh. Tiêu đề trên YouTube không
    mang mã bài, nên muốn biết video nào là VD-0xx thì phải đi ngược từ caption."""
    ban_do = {}
    duoi = KENH[ma_kenh]["caption"].format(ma="")
    for f in sorted((REPO / "content" / "captions").glob(f"*{duoi}")):
        ma = f.name[: -len(duoi)]
        if not re.fullmatch(r"[A-Z]+-\d+", ma):
            continue
        noi_dung = f.read_text(encoding="utf-8")
        if ma_kenh == "vi":
            moc = re.search(r"^#\s*Đăng YouTube", noi_dung, re.M)
            if not moc:
                continue
            noi_dung = noi_dung[moc.start():]
        tieu_de = _boc_khoi(noi_dung, "Tiêu đề")
        if tieu_de:
            ban_do[tieu_de.strip()] = ma
    return ban_do


def so_lieu(dich_vu, ma_kenh: str) -> None:
    """In lượt xem từng video trên kênh, kèm tuổi tính từ lúc công khai.

    Tuổi là cột quan trọng nhất: so bài 3 ngày tuổi với bài 1 ngày tuổi là so lệch.
    Đọc số 48 giờ thì nhìn các dòng có tuổi quanh 48h.
    """
    from datetime import datetime, timedelta, timezone

    vn = timezone(timedelta(hours=7))
    bay_gio = datetime.now(vn)
    kenh = dich_vu.channels().list(part="contentDetails,statistics", mine=True).execute()["items"][0]
    ds_tai_len = kenh["contentDetails"]["relatedPlaylists"]["uploads"]

    ids, trang = [], None
    while True:
        kq = dich_vu.playlistItems().list(
            part="contentDetails", playlistId=ds_tai_len, maxResults=50, pageToken=trang
        ).execute()
        ids += [x["contentDetails"]["videoId"] for x in kq["items"]]
        trang = kq.get("nextPageToken")
        if not trang:
            break

    ban_do = ban_do_tieu_de(ma_kenh)
    dong = []
    for i in range(0, len(ids), 50):
        kq = dich_vu.videos().list(
            part="snippet,statistics,status,contentDetails", id=",".join(ids[i:i + 50])
        ).execute()
        for v in kq["items"]:
            tt = v["status"]
            moc = tt.get("publishAt") or v["snippet"]["publishedAt"]
            luc = datetime.fromisoformat(moc.replace("Z", "+00:00")).astimezone(vn)
            tieu_de = v["snippet"]["title"]
            giay = re.fullmatch(r"PT(?:(\d+)M)?(?:(\d+)S)?", v["contentDetails"]["duration"])
            dai = int(giay.group(1) or 0) * 60 + int(giay.group(2) or 0) if giay else 0
            dong.append({
                "luc": luc,
                "ma": ban_do.get(tieu_de.strip(), "—"),
                "cong_khai": tt["privacyStatus"] == "public",
                "xem": int(v["statistics"].get("viewCount", 0)),
                "thich": int(v["statistics"].get("likeCount", 0)),
                "dai": dai,
                "tieu_de": tieu_de,
            })
    dong.sort(key=lambda x: x["luc"])

    so_sub = kenh["statistics"].get("subscriberCount", "?")
    print(f"{KENH[ma_kenh]['ten']} · {so_sub} người đăng ký · {len(dong)} video")
    print(f"{'lên sóng':<13}{'mã':<8}{'tuổi':>6}{'dài':>6}{'xem':>7}{'thích':>7}  tiêu đề")
    print("─" * 90)
    cho = 0
    for x in dong:
        if not x["cong_khai"]:
            cho += 1
            continue
        gio = (bay_gio - x["luc"]).total_seconds() / 3600
        tuoi = f"{gio:.0f}h" if gio < 72 else f"{gio / 24:.0f}d"
        print(f"{x['luc']:%d/%m %H:%M}  {x['ma']:<8}{tuoi:>6}{x['dai']:>5}s{x['xem']:>7}{x['thich']:>7}"
              f"  {x['tieu_de'][:40]}")
    print("─" * 90)
    print(f"Còn {cho} video riêng tư đang chờ lên sóng (không in).")


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
    p.add_argument("viec", choices=["xin-quyen", "kiem-tra", "dang", "doi-lich", "binh-luan", "so-lieu"])
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
    p.add_argument("--playlist", help="Tên playlist để nhét video vào sau khi đăng. "
                                      "Chưa có thì tạo mới, có rồi thì dùng lại.")
    a = p.parse_args()

    kenh = KENH[a.kenh]

    if a.viec == "xin-quyen":
        # Phải xoá token cũ trước. `lay_dich_vu` thấy token còn hạn là dùng lại ngay,
        # nên nếu không xoá thì `xin-quyen` chạy suông: in "✅ Xong" mà không mở trình
        # duyệt, token nhầm kênh vẫn y nguyên. Đúng lỗi làm mất buổi 03/09 — chạy ba lần
        # tưởng đã xin lại, thật ra chỉ lần đầu là thật.
        f_token = REPO / THU_MUC_BI_MAT / KENH[a.kenh]["token"]
        if f_token.exists():
            f_token.unlink()
            print(f"🗑️  Đã xoá token cũ {THU_MUC_BI_MAT}/{f_token.name} để xin lại từ đầu.")
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

    if a.viec == "so-lieu":
        so_lieu(lay_dich_vu(a.kenh), a.kenh)
        return 0

    if a.viec == "doi-lich":
        if not a.ma:
            sys.exit("❌ Thiếu mã video. Vd: doi-lich VD-016 --kenh vi --hen-gio 2026-08-12T19:30:00+07:00")
        if not a.hen_gio:
            sys.exit("❌ Thiếu --hen-gio. Vd: --hen-gio 2026-08-12T19:30:00+07:00")

        bai = doc_caption(a.ma, a.kenh)
        dich_vu = lay_dich_vu(a.kenh)
        vid = a.video or tim_video(dich_vu, bai["tieu_de"])
        if not vid:
            sys.exit(
                f"❌ Không thấy video nào trên kênh {kenh['ten']} có tiêu đề:\n"
                f"   {bai['tieu_de']}\n"
                "   Tiêu đề trong file caption phải khớp đúng tiêu đề đã đăng, hoặc\n"
                "   truyền thẳng mã video bằng --video."
            )

        print("─" * 68)
        print(f"Kênh:  {kenh['ten']} ({kenh['handle']})")
        print(f"Video: {vid} · {bai['tieu_de']}")
        print(f"Dời:   → {a.hen_gio}")
        print("─" * 68)
        if not a.dang_that:
            print("🟡 Đang chạy thử, chưa sửa gì trên YouTube.")
            print("   Ưng rồi thì thêm --dang-that.")
            return 0

        kq = doi_lich(dich_vu, vid, a.hen_gio)
        print(f"✅ Đã dời: {kq['truoc']} → {kq['sau']}")
        print("👉 Đọc lại API để khớp ngày giờ, và nhớ sửa schedule/calendar.md")
        return 0

    if a.viec == "binh-luan":
        if not a.ma:
            sys.exit("❌ Thiếu mã video. Vd: binh-luan VD-018 --kenh vi")

        chu = doc_binh_luan_ghim(a.ma, a.kenh)
        bai = doc_caption(a.ma, a.kenh)
        dich_vu = lay_dich_vu(a.kenh)
        vid = a.video or tim_video(dich_vu, bai["tieu_de"])
        if not vid:
            sys.exit(
                f"❌ Không thấy video nào trên kênh {kenh['ten']} có tiêu đề:\n"
                f"   {bai['tieu_de']}\n"
                "   Truyền thẳng mã video bằng --video nếu tiêu đề đã sửa trên YouTube."
            )

        print("─" * 68)
        print(f"Kênh:  {kenh['ten']} ({kenh['handle']})")
        print(f"Video: {vid} · {bai['tieu_de']}")
        print(f"Chữ lấy: {bai['nguon']} → mục nhắc cuối file")
        print("─" * 68)
        for dong in chu.splitlines():
            print(f"  {dong}")
        print("─" * 68)
        if not a.dang_that:
            print("🟡 Đang chạy thử, chưa gửi gì lên YouTube.")
            print("   Ưng rồi thì thêm --dang-that.")
            return 0

        ma_bl = dang_binh_luan(dich_vu, vid, chu)
        print(f"✅ Đã đăng bình luận. id: {ma_bl}")
        print("\n⚠️ GHIM THÌ PHẢI BẤM TAY — YouTube Data API không có thao tác ghim.")
        print(f"   Vào: https://studio.youtube.com/video/{vid}/comments")
        print("   Bấm ba chấm cạnh bình luận vừa đăng → Ghim.")
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
    print(f"Video:    {duong_dan_gon(f_video)} · {f_video.stat().st_size / 1e6:.1f} MB")
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

    if a.playlist:
        try:
            pl = tim_hoac_tao_playlist(dich_vu, a.playlist)
            them_vao_playlist(dich_vu, pl, vid)
            print(f"   Đã cho vào playlist '{a.playlist}': "
                  f"https://www.youtube.com/playlist?list={pl}")
        except Exception as loi:
            # Khong lam hong ca lenh dang chi vi playlist - video da len roi.
            print(f"   ⚠️ Không cho vào playlist được: {type(loi).__name__}: {loi}")
            print(f"      Thêm tay trong Studio nếu cần.")

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
