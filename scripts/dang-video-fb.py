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


def lay_caption(ma_so: str) -> str:
    """Ghép caption + hashtag từ content/captions/<ma>-caption.md."""
    f = REPO / "content" / "captions" / f"{ma_so}-caption.md"
    if not f.exists():
        sys.exit(f"❌ Không thấy {f.relative_to(REPO)}")
    noi_dung = f.read_text(encoding="utf-8")

    than = re.search(r"## Caption đăng Facebook\s*(.+?)\n---", noi_dung, re.S)
    if not than:
        sys.exit(f"❌ {f.name} thiếu mục '## Caption đăng Facebook'")
    text = than.group(1).strip()

    tag = re.search(r"## Hashtag\s*(.+?)(?:\n##|\Z)", noi_dung, re.S)
    if tag:
        text += "\n\n" + tag.group(1).strip()

    # Bỏ ký hiệu markdown (Facebook không hiểu **đậm**)
    text = re.sub(r"\*\*(.+?)\*\*", r"\1", text)
    text = re.sub(r"_(.+?)_", r"\1", text)
    return text.strip()


def main() -> int:
    p = argparse.ArgumentParser(description="Đăng bài lên Page Sống Tốt")
    p.add_argument("loai", choices=["kiem-tra", "video", "anh"])
    p.add_argument("file", nargs="?", help="Đường dẫn file video/ảnh")
    p.add_argument("--ma", help="Mã video để lấy caption, vd VD-001")
    p.add_argument("--caption", help="Caption gõ trực tiếp (thay cho --ma)")
    p.add_argument("--thumb", help="Ảnh thumbnail cho video (chỉ dùng với loại video)")
    p.add_argument("--tieu-de", help="Tiêu đề video")
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
