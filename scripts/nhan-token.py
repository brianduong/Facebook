#!/usr/bin/env python3
"""Nhận token Facebook anh vừa copy, tự lo phần còn lại.

    python3 scripts/nhan-token.py

Script sẽ hỏi token (dán vào, chữ không hiện ra màn hình, không lưu vào history),
rồi tự làm hết những chỗ dễ sai:

  • Nhận ra token anh dán là **token người dùng** hay **token Page** —
    đây là chỗ nhầm phổ biến nhất, vì Explorer cho cả hai loại trông y như nhau.
  • Nếu là token người dùng → tự gọi /me/accounts lấy token của Page Sống Tốt.
  • Kiểm tra token có đủ quyền đăng bài chưa, thiếu quyền nào thì nói rõ tên quyền.
  • Ghi FB_PAGE_ID + FB_PAGE_TOKEN vào .env với quyền 600 (chỉ máy anh đọc được).

Nếu có thêm App ID + App Secret thì dùng `scripts/lay-token-dai-han.py` để có
token không hết hạn. Script này chỉ nhận token đang có, không cần secret.
"""

from __future__ import annotations

import getpass
import json
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import nhan_dien as nd  # noqa: E402

API = "https://graph.facebook.com/v21.0"
QUYEN_CAN = ("pages_manage_posts", "pages_read_engagement", "pages_show_list")


def goi(duong_dan: str, token: str) -> dict:
    """Gọi Graph API. Trả về dict; lỗi của Facebook cũng trả về nguyên văn để đọc."""
    noi = "&" if "?" in duong_dan else "?"
    kq = subprocess.run(
        ["curl", "-sS", "-G", f"{API}/{duong_dan}{noi}access_token={token}"],
        capture_output=True, text=True,
    )
    if kq.returncode != 0:
        sys.exit(f"❌ Không gọi được Facebook: {kq.stderr.strip()}")
    try:
        return json.loads(kq.stdout)
    except json.JSONDecodeError:
        sys.exit(f"❌ Facebook trả về không phải JSON:\n{kq.stdout[:300]}")


def doc_env() -> dict[str, str]:
    f = nd.REPO / ".env"
    if not f.exists():
        return {}
    ra = {}
    for dong in f.read_text(encoding="utf-8").splitlines():
        dong = dong.strip()
        if dong and not dong.startswith("#") and "=" in dong:
            k, v = dong.split("=", 1)
            ra[k.strip()] = v.strip()
    return ra


def ghi_env(page_id: str, token: str) -> None:
    """Chỉ sửa hai dòng của Facebook, giữ nguyên mọi dòng khác trong .env.

    Bản cũ ghi đè cả file nên nuốt mất PEXELS_API_KEY — chạy xong là hỏng khâu
    tải ảnh nền mà không báo gì.
    """
    f = nd.REPO / ".env"
    moi = {"FB_PAGE_ID": page_id, "FB_PAGE_TOKEN": token}
    ra: list[str] = []
    da_ghi: set[str] = set()

    if f.exists():
        for dong in f.read_text(encoding="utf-8").splitlines():
            kho = dong.strip()
            if kho and not kho.startswith("#") and "=" in kho:
                k = kho.split("=", 1)[0].strip()
                if k in moi:
                    ra.append(f"{k}={moi[k]}")
                    da_ghi.add(k)
                    continue
            ra.append(dong)
    else:
        ra = [
            "# Page Sống Tốt — https://www.facebook.com/songtot.in",
            "# File này KHÔNG lên GitHub (đã bị .gitignore chặn)",
        ]

    for k, v in moi.items():
        if k not in da_ghi:
            ra.append(f"{k}={v}")

    f.write_text("\n".join(ra).rstrip("\n") + "\n", encoding="utf-8")
    f.chmod(0o600)


def main() -> int:
    env = doc_env()
    page_id_biet = env.get("FB_PAGE_ID", "")

    print("Dán token vừa copy từ Graph API Explorer rồi Enter.")
    print("(Chữ sẽ không hiện ra — dán xong cứ Enter, kể cả khi thấy trống.)")
    token = getpass.getpass("  Token: ").strip()
    if not token:
        sys.exit("❌ Chưa dán gì cả.")
    if len(token) < 50:
        print(f"⚠️  Token chỉ {len(token)} ký tự — hơi ngắn, có thể copy thiếu. Vẫn thử tiếp...")

    print("\n① Xem token này là của ai...")
    toi = goi("me?fields=id,name", token)
    if "error" in toi:
        e = toi["error"]
        sys.exit(
            f"❌ Facebook từ chối token: {e.get('message')}\n"
            "   Hay gặp nhất là token đã hết hạn (token từ Explorer chỉ sống 1–2 giờ)\n"
            "   → mở lại Graph API Explorer, bấm Generate Access Token rồi chạy lại script này."
        )
    print(f"   Token thuộc về: {toi.get('name')} (id {toi.get('id')})")

    la_token_page = bool(page_id_biet) and toi.get("id") == page_id_biet

    if la_token_page:
        print("   → Đây là TOKEN PAGE, đúng loại cần dùng.")
        page_id, page_token = toi["id"], token
    else:
        print("   → Đây là token người dùng. Em đi lấy token Page từ nó.")

        quyen = goi("me/permissions", token)
        if "data" in quyen:
            da_cap = {q["permission"] for q in quyen["data"] if q.get("status") == "granted"}
            thieu = [q for q in QUYEN_CAN if q not in da_cap]
            print(f"   Quyền đã cấp: {', '.join(sorted(da_cap)) or 'không có gì'}")
            if thieu:
                sys.exit(
                    "❌ Token thiếu quyền: " + ", ".join(thieu) + "\n"
                    "   Về Graph API Explorer → Add a Permission → tích đủ 3 quyền:\n"
                    "     pages_show_list · pages_read_engagement · pages_manage_posts\n"
                    "   → bấm Generate Access Token LẦN NỮA → copy token mới → chạy lại script này.\n"
                    "   (Nếu Facebook báo 'Invalid Scopes' thì app đang dùng không phải loại Business —\n"
                    "    tạo app mới: My Apps → Create App → Other → Business.)"
                )

        print("② Lấy token Page...")
        ds = goi("me/accounts?fields=id,name,access_token", token)
        if "error" in ds:
            sys.exit(f"❌ {ds['error'].get('message')}")
        pages = ds.get("data", [])
        if not pages:
            sys.exit("❌ Token này không thấy Page nào. Kiểm tra tài khoản có đang là quản trị Page không.")

        chon = next((p for p in pages if p["id"] == page_id_biet), None)
        if chon is None:
            for i, p in enumerate(pages, 1):
                print(f"   {i}. {p['name']} — ID {p['id']}")
            so = input("   Chọn Page số mấy? ").strip()
            if not so.isdigit() or not 1 <= int(so) <= len(pages):
                sys.exit("❌ Số không hợp lệ.")
            chon = pages[int(so) - 1]
        page_id, page_token = chon["id"], chon["access_token"]
        print(f"   ✅ Lấy được token của Page: {chon['name']}")

    print("③ Thử token Page trên Page thật...")
    thu = goi(f"{page_id}?fields=name,followers_count,fan_count", page_token)
    if "error" in thu:
        sys.exit(f"❌ Token Page không đọc được Page: {thu['error'].get('message')}")
    print(f"   ✅ {thu.get('name')} — {thu.get('followers_count', thu.get('fan_count', '?'))} người theo dõi")

    ghi_env(page_id, page_token)
    print(f"\n✅ Đã ghi .env (quyền 600): FB_PAGE_ID={page_id}, token …{page_token[-6:]}")
    print("Bước tiếp: python3 scripts/dang-video-fb.py kiem-tra")
    return 0


if __name__ == "__main__":
    sys.exit(main())
