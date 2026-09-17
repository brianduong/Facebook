#!/usr/bin/env python3
"""Đăng video / ảnh lên Page Sống Tốt qua Facebook Graph API.

Cần một file `.env` ở gốc repo (đã nằm trong .gitignore, KHÔNG lên GitHub):

    FB_PAGE_ID=123456789012345
    FB_PAGE_TOKEN=EAAG...

Cách dùng:
    # 1. Kiểm tra token còn sống và đúng Page không
    python3 scripts/dang-video-fb.py kiem-tra

    # 2. Xem trước caption sẽ đăng (KHÔNG đăng thật)
    python3 scripts/dang-video-fb.py video video/exports/VD-001.mp4 --ma VD-001

    # 3. Đăng thật
    python3 scripts/dang-video-fb.py video video/exports/VD-001.mp4 --ma VD-001 --dang-that

    # Đăng ảnh quote (dùng khi muốn ra bài ảnh giữa hai video)
    python3 scripts/dang-video-fb.py anh assets/templates/quotes/VD-001-quote.png --ma VD-001 --dang-that

Mặc định là **chạy thử** — chỉ in ra những gì sẽ gửi. Phải thêm `--dang-that` mới đăng lên Page.
"""

import argparse
import json
import re
import subprocess
import sys
from datetime import datetime
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
API = "https://graph.facebook.com/v21.0"


def doc_env() -> dict[str, str]:
    f = REPO / ".env"
    if not f.exists():
        sys.exit(
            "❌ Chưa có file .env ở gốc repo.\n"
            "   Tạo file .env với 2 dòng:\n"
            "     FB_PAGE_ID=<id của Page>\n"
            "     FB_PAGE_TOKEN=<Page Access Token>\n"
            "   (xem docs/huong-dan-dang-tu-dong.md để biết cách lấy)"
        )
    env = {}
    for dong in f.read_text(encoding="utf-8").splitlines():
        dong = dong.strip()
        if dong and not dong.startswith("#") and "=" in dong:
            k, v = dong.split("=", 1)
            env[k.strip()] = v.strip().strip('"').strip("'")
    for can in ("FB_PAGE_ID", "FB_PAGE_TOKEN"):
        if not env.get(can):
            sys.exit(f"❌ Thiếu {can} trong .env")
    return env


def goi_api(args: list[str]) -> dict:
    """Gọi curl và trả về JSON. Tách riêng để dễ đọc log khi lỗi."""
    kq = subprocess.run(["curl", "-sS", *args], capture_output=True, text=True)
    if kq.returncode != 0:
        sys.exit(f"❌ curl lỗi: {kq.stderr.strip()}")
    try:
        data = json.loads(kq.stdout)
    except json.JSONDecodeError:
        sys.exit(f"❌ Facebook trả về không phải JSON:\n{kq.stdout[:500]}")
    if "error" in data:
        loi = data["error"]
        sys.exit(f"❌ Facebook báo lỗi: {loi.get('message')} (code {loi.get('code')})")
    return data


def _khoi_duoi_muc(noi_dung: str, ten_muc: str) -> str | None:
    """Lấy khối ``` đầu tiên nằm dưới tiêu đề mục khớp `ten_muc` (khuôn VD-004 trở đi)."""
    m = re.search(rf"^##\s*(?:\d+\s*[·.]\s*)?{ten_muc}\b", noi_dung, re.M | re.I)
    if not m:
        return None
    khoi = re.search(r"```[a-z]*\n(.*?)\n```", noi_dung[m.end():], re.S)
    return khoi.group(1).strip() if khoi else None


def lay_caption(ma_so: str) -> str:
    """Ghép caption + hashtag từ content/captions/<ma>-caption.md.

    Đọc được cả hai khuôn: khuôn cũ (VD-001 → VD-003, chữ nằm thẳng dưới tiêu đề)
    và khuôn mới (VD-004 trở đi, chữ nằm trong khối ``` để copy nguyên khối).
    """
    f = REPO / "content" / "captions" / f"{ma_so}-caption.md"
    if not f.exists():
        sys.exit(f"❌ Không thấy {f.relative_to(REPO)}")
    noi_dung = f.read_text(encoding="utf-8")

    # Khuôn mới có cả phần Facebook lẫn phần YouTube — cắt lấy phần Facebook.
    moc_fb = re.search(r"^#\s*Đăng Facebook", noi_dung, re.M)
    if moc_fb:
        moc_yt = re.search(r"^#\s*Đăng YouTube", noi_dung[moc_fb.start():], re.M)
        phan_fb = noi_dung[moc_fb.start():moc_fb.start() + moc_yt.start()] if moc_yt else noi_dung[moc_fb.start():]
        text = _khoi_duoi_muc(phan_fb, "Caption")
        if not text:
            sys.exit(f"❌ {f.name} có mục '# Đăng Facebook' nhưng không thấy khối Caption")
        tag = _khoi_duoi_muc(phan_fb, "Hashtag")
    else:
        than = re.search(r"## Caption đăng Facebook\s*(.+?)\n---", noi_dung, re.S)
        if not than:
            sys.exit(f"❌ {f.name} thiếu mục '## Caption đăng Facebook'")
        text = than.group(1).strip()
        m_tag = re.search(r"## Hashtag\s*(.+?)(?:\n##|\Z)", noi_dung, re.S)
        tag = m_tag.group(1).strip() if m_tag else None

    if tag:
        text += "\n\n" + tag

    # Bỏ ký hiệu markdown (Facebook không hiểu **đậm**)
    text = re.sub(r"\*\*(.+?)\*\*", r"\1", text)
    text = re.sub(r"_(.+?)_", r"\1", text)
    return text.strip()


def lay_binh_luan_ghim(ma_so: str) -> str:
    """Bóc câu bình luận soạn sẵn ở mục "## Nhắc khi đăng" cuối file caption tiếng Việt.

    Chỉ bài nào cố ý cần bình luận mở hàng mới có khối này — không có thì báo lỗi chứ
    đừng tự nghĩ chữ thay.
    """
    f = REPO / "content" / "captions" / f"{ma_so}-caption.md"
    if not f.exists():
        sys.exit(f"❌ Không thấy {f.relative_to(REPO)}")
    noi_dung = f.read_text(encoding="utf-8")

    moc = re.search(r"^##\s*Nhắc khi đăng\b", noi_dung, re.M)
    if not moc:
        sys.exit(f"❌ {f.name} không có mục '## Nhắc khi đăng'.")

    phan = noi_dung[moc.end():]
    het = re.search(r"^##\s", phan, re.M)
    if het:
        phan = phan[: het.start()]

    # Khối này nằm lồng trong một gạch đầu dòng nên thụt lề — phải bắt lấy phần thụt
    # rồi gỡ ra, không thì chữ đăng lên kèm hai dấu cách đầu dòng.
    khoi = re.search(r"^([ \t]*)```[a-z]*\n(.*?)\n\1```", phan, re.S | re.M)
    if not khoi:
        sys.exit(
            f"❌ {f.name} mục '## Nhắc khi đăng' không có khối ``` nào.\n"
            "   Bài này không soạn sẵn bình luận mở hàng — viết câu vào file caption trước."
        )
    thut = khoi.group(1)
    dong = [d[len(thut):] if d.startswith(thut) else d for d in khoi.group(2).splitlines()]
    return "\n".join(dong).strip()


def dang_binh_luan(bai_id: str, token: str, chu: str) -> str:
    """Đăng bình luận lên một bài của Page. Trả về id bình luận.

    ⚠️ Graph API **không có thao tác ghim bình luận** — ghim vẫn phải bấm tay trên Facebook.
    """
    kq = goi_api(["-F", f"message={chu}", "-F", f"access_token={token}", f"{API}/{bai_id}/comments"])
    return kq["id"]


def dang_reels(page_id: str, token: str, f: Path, caption: str, hen_gio: str | None) -> str:
    """Đăng Reels — luồng ba bước riêng của Facebook, không dùng chung với /videos.

    Đăng qua /videos ra bài video thường; video dọc 9:16 phải đi đường này mới
    thành Reels và mới được đẩy trong tab Reels.
    """
    print("① Xin chỗ tải lên...")
    mo = goi_api(["-X", "POST", f"{API}/{page_id}/video_reels",
                  "-F", "upload_phase=start", "-F", f"access_token={token}"])
    vid, url = mo.get("video_id"), mo.get("upload_url")
    if not vid or not url:
        sys.exit(f"❌ Facebook không trả về chỗ tải lên: {mo}")

    kich_thuoc = f.stat().st_size
    print(f"② Đang tải {kich_thuoc / 1e6:.1f} MB... (video nặng có thể mất vài phút)")
    kq = subprocess.run(
        ["curl", "-sS", "-X", "POST", url,
         "-H", f"Authorization: OAuth {token}",
         "-H", "offset: 0",
         "-H", f"file_size: {kich_thuoc}",
         "--data-binary", f"@{f}"],
        capture_output=True, text=True,
    )
    if kq.returncode != 0:
        sys.exit(f"❌ Tải lên lỗi: {kq.stderr.strip()}")
    try:
        ket = json.loads(kq.stdout)
    except json.JSONDecodeError:
        sys.exit(f"❌ Facebook trả về không phải JSON khi tải lên:\n{kq.stdout[:300]}")
    if not ket.get("success"):
        sys.exit(f"❌ Facebook báo tải lên chưa xong: {ket}")

    print("③ Chốt bài...")
    form = ["-X", "POST", f"{API}/{page_id}/video_reels",
            "-F", f"video_id={vid}", "-F", "upload_phase=finish",
            "-F", f"description={caption}", "-F", f"access_token={token}"]
    if hen_gio:
        moc = datetime.fromisoformat(hen_gio)
        giay = int(moc.timestamp())
        con = giay - int(datetime.now(moc.tzinfo).timestamp())
        if con < 600:
            sys.exit(f"❌ Facebook đòi hẹn giờ cách hiện tại ít nhất 10 phút (đang còn {con // 60} phút).")
        form += ["-F", "video_state=SCHEDULED", "-F", f"scheduled_publish_time={giay}"]
    else:
        form += ["-F", "video_state=PUBLISHED"]

    xong = goi_api(form)
    if not xong.get("success", True):
        sys.exit(f"❌ Chốt bài không thành: {xong}")
    return vid


def lay_so_lieu(page_id: str, token: str) -> list[dict]:
    """Lượt xem từng Reel trên Page, đọc bằng quyền sẵn có.

    ⚠️ **Đừng dùng `/{video-id}/video_insights`** — nó đòi phạm vi `read_insights`, mà token
    của dự án không có (đo ngày 18/09: trả 403 `read_insights permission missing`). Xin thêm
    phạm vi đó thì phải qua vòng App Review của Meta.

    Edge `/{page-id}/video_reels` **có sẵn `views` và `post_views`**, đọc được bằng
    `pages_read_engagement` đang có. Đây là đường lấy số Facebook của dự án.

    `views` là lượt xem; `post_views` thấp hơn nhiều và là lượt xem tính theo bài đăng.
    """
    ra: list[dict] = []
    url = (f"{API}/{page_id}/video_reels"
           f"?fields=id,created_time,views,post_views,length&limit=100&access_token={token}")
    while url and len(ra) < 500:
        d = goi_api([url])
        ra += d.get("data", [])
        url = d.get("paging", {}).get("next")
    return ra


def ma_theo_reel() -> dict[str, str]:
    """Tra mã bài (VD-0XX) theo id Reel, bóc từ bảng trong schedule/calendar.md."""
    f = REPO / "schedule" / "calendar.md"
    if not f.exists():
        return {}
    ra = {}
    for dong in f.read_text(encoding="utf-8").splitlines():
        ma = re.search(r"\*\*(VD-\d{3})\*\*", dong)
        rid = re.search(r"`(\d{15,17})`", dong)
        if ma and rid:
            ra.setdefault(rid.group(1), ma.group(1))
    return ra


def main() -> int:
    p = argparse.ArgumentParser(description="Đăng bài lên Page Sống Tốt")
    p.add_argument("loai", choices=["kiem-tra", "video", "reels", "anh", "binh-luan", "so-lieu"])
    p.add_argument("file", nargs="?", help="Đường dẫn file video/ảnh")
    p.add_argument("--bai", help="ID bài đã đăng, dùng cho binh-luan")
    p.add_argument("--ma", help="Mã video để lấy caption, vd VD-001")
    p.add_argument("--caption", help="Caption gõ trực tiếp (thay cho --ma)")
    p.add_argument("--thumb", help="Ảnh thumbnail cho video (chỉ dùng với loại video)")
    p.add_argument("--tieu-de", help="Tiêu đề video")
    p.add_argument("--hen-gio", help="Hẹn giờ cho Reels, vd 2026-08-03T19:30:00+07:00")
    p.add_argument("--dang-that", action="store_true", help="Đăng thật lên Page")
    a = p.parse_args()

    env = doc_env()
    page_id, token = env["FB_PAGE_ID"], env["FB_PAGE_TOKEN"]

    if a.loai == "kiem-tra":
        me = goi_api([f"{API}/{page_id}?fields=name,followers_count,fan_count&access_token={token}"])
        print("✅ Token dùng được.")
        print(f"   Page: {me.get('name')} (id {me.get('id', page_id)})")
        if me.get("followers_count"):
            print(f"   Followers: {me['followers_count']:,}")
        return 0

    if a.loai == "so-lieu":
        rows = lay_so_lieu(page_id, token)
        ten = ma_theo_reel()
        rows.sort(key=lambda x: x.get("created_time", ""))
        print(f"{'mã':<9}{'ngày':<12}{'lượt xem':>9}{'post_views':>12}")
        print("─" * 42)
        for x in rows:
            ma = ten.get(x["id"], "—")
            print(f"{ma:<9}{x.get('created_time', '')[:10]:<12}"
                  f"{x.get('views', 0):>9}{x.get('post_views', 0):>12}")
        # Mốc 02/08 là ngày dựng tự động hoá — chia hai nhóm để thấy ngay chênh lệch.
        tay = [x for x in rows if x.get("created_time", "") < "2026-08-02"]
        app = [x for x in rows if x.get("created_time", "") >= "2026-08-02"]
        print("─" * 42)
        for nhan, nhom in (("đăng tay (trước 02/08)", tay), ("đăng bằng app (từ 02/08)", app)):
            if nhom:
                tong = sum(x.get("views", 0) for x in nhom)
                print(f"{nhan:<26} {len(nhom):>3} bài · {tong:>6} lượt · TB {tong / len(nhom):.1f}")
        return 0

    if a.loai == "binh-luan":
        if not a.bai:
            sys.exit("❌ Thiếu --bai <id bài>. Vd: binh-luan --ma VD-018 --bai 1086214770915645")
        chu = a.caption or (lay_binh_luan_ghim(a.ma) if a.ma else None)
        if not chu:
            sys.exit("❌ Cần --ma VD-0XX hoặc --caption \"...\"")
        print("─" * 60)
        print(f"Sẽ bình luận vào bài {a.bai}  →  Page Sống Tốt")
        print("─" * 60)
        print(chu)
        print("─" * 60)
        if not a.dang_that:
            print("🟡 Đang chạy thử. Thêm --dang-that để đăng lên Page thật.")
            return 0
        ma_bl = dang_binh_luan(a.bai, token, chu)
        print(f"✅ Đã đăng bình luận. id: {ma_bl}")
        print("\n⚠️ GHIM THÌ PHẢI BẤM TAY — Graph API không có thao tác ghim bình luận.")
        print(f"   Vào: https://www.facebook.com/reel/{a.bai}")
        return 0

    if not a.file:
        sys.exit("❌ Thiếu đường dẫn file.")
    f = Path(a.file)
    if not f.is_absolute():
        f = REPO / f
    if not f.exists():
        sys.exit(f"❌ Không thấy file {f}")

    if a.caption:
        caption = a.caption
    elif a.ma:
        caption = lay_caption(a.ma)
    else:
        sys.exit("❌ Cần --ma VD-00X hoặc --caption \"...\"")

    if a.loai == "reels":
        print("─" * 60)
        print(f"Sẽ đăng REELS: {f.name}  →  Page Sống Tốt")
        if a.hen_gio:
            print(f"Hẹn giờ: {a.hen_gio}")
        print("─" * 60)
        print(caption)
        print("─" * 60)
        if not a.dang_that:
            print("🟡 Đang chạy thử. Thêm --dang-that để đăng lên Page thật.")
            return 0
        vid = dang_reels(page_id, token, f, caption, a.hen_gio)
        print(f"\n✅ Đã đăng Reels. ID: {vid}")
        if a.hen_gio:
            print(f"   Đang hẹn giờ — xem ở Meta Business Suite → Nội dung → Đã lên lịch")
        else:
            print(f"   Xem: https://www.facebook.com/reel/{vid}")
        print("👉 Nhớ cập nhật trạng thái ✅ trong schedule/calendar.md")
        return 0

    if a.loai == "video":
        endpoint = f"{API}/{page_id}/videos"
        form = ["-F", f"source=@{f}", "-F", f"description={caption}"]
        if a.tieu_de:
            form += ["-F", f"title={a.tieu_de}"]
        if a.thumb:
            t = Path(a.thumb)
            if not t.is_absolute():
                t = REPO / t
            if not t.exists():
                sys.exit(f"❌ Không thấy thumbnail {t}")
            form += ["-F", f"thumb=@{t}"]
    else:
        endpoint = f"{API}/{page_id}/photos"
        form = ["-F", f"source=@{f}", "-F", f"message={caption}"]

    print("─" * 60)
    print(f"Sẽ đăng: {f.name}  →  {endpoint}")
    print("─" * 60)
    print(caption)
    print("─" * 60)

    if not a.dang_that:
        print("🟡 Đang chạy thử. Thêm --dang-that để đăng lên Page thật.")
        return 0

    print("⏳ Đang tải lên... (video nặng có thể mất vài phút)")
    kq = goi_api([*form, "-F", f"access_token={token}", endpoint])
    bai_id = kq.get("id") or kq.get("post_id")
    print(f"✅ Đã đăng. ID: {bai_id}")
    print(f"   Xem: https://www.facebook.com/{bai_id}")
    print("👉 Nhớ cập nhật trạng thái ✅ trong schedule/calendar.md")
    return 0


if __name__ == "__main__":
    sys.exit(main())
