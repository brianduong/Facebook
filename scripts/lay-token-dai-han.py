#!/usr/bin/env python3
"""Đổi token ngắn hạn của Facebook thành token Page dùng lâu dài, rồi ghi vào .env.

Token copy từ Graph API Explorer chỉ sống 1–2 giờ. Script này làm hai bước
mà Facebook yêu cầu để có token bền:

  1. Đổi token người dùng ngắn hạn → token người dùng dài hạn (khoảng 60 ngày)
  2. Dùng token dài hạn gọi /me/accounts → lấy token của Page
     (token Page sinh ra từ token dài hạn thì không hết hạn, miễn là anh không
      đổi mật khẩu, không thu hồi quyền, và app không bị vô hiệu hoá)

Cách dùng — KHÔNG truyền token/secret trên dòng lệnh (nó lưu vào history của
shell), script sẽ hỏi và anh dán vào, chữ không hiện lên màn hình:

    python3 scripts/lay-token-dai-han.py --app-id 1234567890

Xong việc, script ghi FB_PAGE_ID và FB_PAGE_TOKEN vào file .env ở gốc repo
(.env đã bị .gitignore chặn nên không lên GitHub).
"""

from __future__ import annotations

import argparse
import getpass
import json
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import nhan_dien as nd  # noqa: E402

API = "https://graph.facebook.com/v21.0"


def goi(url: str) -> dict:
    kq = subprocess.run(["curl", "-sS", "-G", url], capture_output=True, text=True)
    if kq.returncode != 0:
        sys.exit(f"❌ curl lỗi: {kq.stderr.strip()}")
    try:
        data = json.loads(kq.stdout)
    except json.JSONDecodeError:
        sys.exit(f"❌ Facebook trả về không phải JSON:\n{kq.stdout[:400]}")
    if "error" in data:
        e = data["error"]
        sys.exit(f"❌ Facebook báo lỗi: {e.get('message')} (code {e.get('code')})")
    return data


def che(token: str) -> str:
    return f"…{token[-6:]} ({len(token)} ký tự)"


def main() -> int:
    p = argparse.ArgumentParser(description="Lấy token Page dùng lâu dài")
    p.add_argument("--app-id", required=True, help="App ID (số) trong developers.facebook.com")
    p.add_argument("--ten-page", help="Chỉ lấy Page có tên chứa chuỗi này, vd 'Sống Tốt'")
    a = p.parse_args()

    print("Dán App Secret (Cài đặt → Cơ bản trong app). Chữ sẽ không hiện ra:")
    secret = getpass.getpass("  App Secret: ").strip()
    print("Dán User Access Token ngắn hạn (copy từ Graph API Explorer):")
    token_ngan = getpass.getpass("  User Token: ").strip()
    if not secret or not token_ngan:
        sys.exit("❌ Thiếu App Secret hoặc token.")

    print("\n① Đổi sang token người dùng dài hạn...")
    dai = goi(
        f"{API}/oauth/access_token?grant_type=fb_exchange_token"
        f"&client_id={a.app_id}&client_secret={secret}&fb_exchange_token={token_ngan}"
    )
    token_dai = dai.get("access_token")
    if not token_dai:
        sys.exit(f"❌ Không nhận được token dài hạn: {dai}")
    print(f"   ✅ {che(token_dai)}")

    print("② Lấy danh sách Page anh quản lý...")
    ds = goi(f"{API}/me/accounts?fields=id,name,access_token&access_token={token_dai}")
    pages = ds.get("data", [])
    if not pages:
        sys.exit("❌ Tài khoản này không quản lý Page nào, hoặc token thiếu quyền pages_show_list.")

    if a.ten_page:
        pages = [p for p in pages if a.ten_page.lower() in p.get("name", "").lower()] or pages

    for i, pg in enumerate(pages, 1):
        print(f"   {i}. {pg['name']} — ID {pg['id']}")

    if len(pages) == 1:
        chon = pages[0]
    else:
        so = input("Chọn Page số mấy? ").strip()
        if not so.isdigit() or not 1 <= int(so) <= len(pages):
            sys.exit("❌ Số không hợp lệ.")
        chon = pages[int(so) - 1]

    print(f"③ Ghi vào .env cho Page: {chon['name']}")
    env = nd.REPO / ".env"
    if env.exists():
        cu = env.read_text(encoding="utf-8")
        if "FB_PAGE_TOKEN" in cu and input("   .env đã có token. Ghi đè? (co/khong) ").strip().lower() not in ("co", "c", "y"):
            print("   Bỏ qua, không ghi gì.")
            return 0
    env.write_text(
        f"FB_PAGE_ID={chon['id']}\nFB_PAGE_TOKEN={chon['access_token']}\n", encoding="utf-8"
    )
    env.chmod(0o600)
    print(f"   ✅ Đã ghi .env — Page ID {chon['id']}, token {che(chon['access_token'])}")
    print("\nKiểm tra lại: python3 scripts/dang-video-fb.py kiem-tra")
    return 0


if __name__ == "__main__":
    sys.exit(main())
