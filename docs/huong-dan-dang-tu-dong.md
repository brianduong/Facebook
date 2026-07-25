# Hướng dẫn đăng tự động qua Facebook Graph API

> Mục đích: anh chỉ chạy **một dòng lệnh** là video + caption tự lên Page, không phải mở app bấm tay.
> Script: `scripts/dang-video-fb.py`

## Anh cần cung cấp 2 thứ

### 1. `FB_PAGE_ID` — ID của Page
- Vào Page **Sống Tốt** → **Cài đặt (Settings)** → **Thông tin về Trang (Page info)** → kéo xuống thấy **ID Trang**.
- Hoặc: mở https://www.facebook.com/songtot.in → **Giới thiệu** → phần "ID Trang".

### 2. `FB_PAGE_TOKEN` — Page Access Token
Cách nhanh (token ngắn hạn, ~2 tháng — đủ để thử):
1. Mở **https://developers.facebook.com/tools/explorer/**
2. Góc trên phải: **Meta App** → chọn app của anh (chưa có thì bấm *Create App* → loại **Business**).
3. Ô **User or Page** → chọn **Get Page Access Token** → chọn Page **Sống Tốt**.
4. Bấm **Add a Permission**, thêm đủ 3 quyền:
   - `pages_manage_posts` (đăng bài)
   - `pages_read_engagement` (đọc số liệu)
   - `pages_show_list`
5. Bấm **Generate Access Token** → copy chuỗi dài đó.

Muốn token **không hết hạn** thì cần đổi sang token dài hạn — khi nào anh cần em hướng dẫn tiếp bước đó.

### Điền vào đâu
Tạo file `.env` ở gốc repo (copy từ `.env.example`):

```
FB_PAGE_ID=123456789012345
FB_PAGE_TOKEN=EAAG...
```

⚠️ **Không** dán token vào Messenger/chat công khai, và **không** commit file `.env` (đã bị .gitignore chặn sẵn).

## Dùng script

```bash
# 1. Kiểm tra token sống chưa + đúng Page chưa
python3 scripts/dang-video-fb.py kiem-tra

# 2. Xem trước caption (chạy thử, KHÔNG đăng)
python3 scripts/dang-video-fb.py video video/exports/VD-001.mp4 --ma VD-001

# 3. Đăng thật, kèm thumbnail là ảnh quote
python3 scripts/dang-video-fb.py video video/exports/VD-001.mp4 --ma VD-001 \
    --thumb assets/templates/quotes/VD-001-quote.png --dang-that

# Đăng một bài ảnh quote (dùng xen giữa các video cho Page đều tay)
python3 scripts/dang-video-fb.py anh assets/templates/quotes/VD-002-quote.png --ma VD-002 --dang-that
```

Script **mặc định chạy thử** — phải có `--dang-that` mới thật sự đăng. Caption được lấy tự động từ `content/captions/<mã>-caption.md`.

## Lưu ý
- Video 1:1 đăng qua `/videos` là **bài video thường** trên Page. Nếu muốn lên **Reels** thì dùng luồng khác (`/video_reels`, tải theo 3 bước) — khi nào cần em bổ sung.
- Facebook đổi phiên bản API theo thời gian; script đang dùng `v21.0`, nếu báo lỗi phiên bản thì sửa biến `API` trong `scripts/dang-video-fb.py`.
- Đăng xong nhớ cập nhật `schedule/calendar.md` (script có nhắc).
