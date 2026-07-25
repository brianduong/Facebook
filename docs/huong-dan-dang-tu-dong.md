# Hướng dẫn lấy Page Access Token & đăng bài tự động

> Mục đích: chạy **một dòng lệnh** là video + caption tự lên Page, khỏi mở app bấm tay.
> Script: `scripts/dang-video-fb.py` · `scripts/nhan-token.py` · `scripts/lay-token-dai-han.py`

**Page ID của Sống Tốt: `315460902683557`** (đã ghi trong `.env`, không cần lấy lại).

---

## A. Tạo app (chỉ làm một lần)

Cần app riêng loại **Business**. App game/consumer sẽ báo *"Invalid Scopes: pages_manage_posts"* vì loại đó không được xin quyền Trang.

1. Mở **developers.facebook.com** → góc trên phải bấm **My Apps**
2. Bấm nút xanh **Create App**
3. **App name**: `Song Tot Poster` · email để nguyên → **Next**
4. Mục **Use cases**: chọn **Other** → **Next**
5. Mục **Select an app type**: chọn **Business** → **Next**
6. **Business portfolio**: chọn cái có sẵn, hoặc "I don't want to connect a business portfolio yet" → **Create app**
7. Nhập mật khẩu Facebook nếu bị hỏi

App ID và App Secret nằm ở **Settings → Basic** (App Secret phải bấm **Show**). Hai thứ này để làm mục E.

---

## B. Lấy Page Access Token

1. Vào **https://developers.facebook.com/tools/explorer/**
2. Ô **Meta App** (bên phải): chọn **Song Tot Poster**
3. Ô **User or Page**: bấm vào → chọn **Get Page Access Token**
   → Facebook mở hộp thoại → chọn Trang **Sống Tốt** → **Continue** → **Save**
4. Mục **Permissions**: bấm **Add a Permission**, mở nhóm **Pages**, tích đủ 3 quyền:
   - `pages_show_list`
   - `pages_read_engagement`
   - `pages_manage_posts`
5. Bấm nút xanh **Generate Access Token** — **phải bấm lại sau khi tích quyền**, không thì token vẫn là token cũ thiếu quyền
6. Hộp thoại cấp quyền hiện ra → **Continue as …** → tích Trang **Sống Tốt** → **Done**
7. Ô **Access Token** phía trên có một chuỗi rất dài → bấm **icon copy** bên phải ô đó

---

## C. Kiểm tra token đúng loại chưa (làm ngay trong Explorer)

Explorer cho cả token người dùng và token Trang, trông y như nhau — đây là chỗ nhầm phổ biến nhất.

| Gõ vào ô đường dẫn | Bấm Submit → phải ra |
|--------------------|----------------------|
| `me?fields=id,name` | `{"id": "315460902683557", "name": "Sống Tốt"}` |
| `315460902683557?fields=name,followers_count` | tên Trang + số người theo dõi |

Nếu `me` trả về **tên anh** (không phải "Sống Tốt") thì đang là token người dùng — vẫn dùng được, script `nhan-token.py` sẽ tự đổi sang token Trang.

---

## D. Lưu token vào máy

**Cách 1 (nên dùng):**
```bash
python3 scripts/nhan-token.py
```
Dán token vào — chữ không hiện ra màn hình và không lưu vào history của shell. Script tự nhận biết loại token, tự lấy token Trang nếu cần, kiểm tra đủ quyền chưa, rồi ghi `.env` với quyền 600.

**Cách 2 (làm tay):** mở file `.env` ở gốc repo (VS Code: ⌘P rồi gõ `.env`), dán vào sau dấu `=`:
```
FB_PAGE_TOKEN=EAAG...
```

Kiểm tra: `python3 scripts/dang-video-fb.py kiem-tra` → in ra tên Page + số followers là xong.

---

## E. Token không hết hạn (làm sau cũng được)

Token ở mục B chỉ sống 1–2 giờ. Muốn dùng lâu dài:

```bash
python3 scripts/lay-token-dai-han.py --app-id <App ID>
```
Script hỏi **App Secret** và **token vừa lấy**, rồi làm hai bước Facebook yêu cầu: đổi sang token người dùng dài hạn (~60 ngày) → gọi `/me/accounts` lấy token Trang. Token Trang sinh ra kiểu này **không hết hạn**, miễn là không đổi mật khẩu, không thu hồi quyền, app không bị vô hiệu hoá.

**Làm tay nếu muốn:** Tools → **Access Token Debugger** → dán token → bấm **Extend Access Token** → copy token 60 ngày → về Explorer gọi `me/accounts?fields=id,name,access_token` bằng token đó → trường `access_token` của Trang trong kết quả chính là token bền.

---

## F. Lỗi hay gặp

| Lỗi | Nguyên nhân | Cách sửa |
|-----|-------------|----------|
| `Invalid Scopes: pages_manage_posts` | App không phải loại Business | Làm mục A, tạo app mới |
| `(#200) Requires pages_manage_posts permission` | Chưa tích quyền, hoặc tích rồi mà chưa bấm Generate lại | Làm lại bước B4 → B5 |
| `Error validating access token: Session has expired` | Token đã hết hạn | Làm mục E cho khỏi lặp lại |
| `Cannot parse access token` | Copy thiếu ký tự | Copy lại bằng icon copy, đừng bôi đen bằng tay |
| `URL Blocked` | Chỉ xảy ra khi tự dựng link OAuth | Dùng Explorer như mục B |

---

## Dùng script đăng bài

```bash
# Kiểm tra token
python3 scripts/dang-video-fb.py kiem-tra

# Xem trước caption, KHÔNG đăng
python3 scripts/dang-video-fb.py video video/exports/VD-001-nhap.mp4 --ma VD-001

# Đăng thật, kèm thumbnail là ảnh quote
python3 scripts/dang-video-fb.py video video/exports/VD-001-nhap.mp4 --ma VD-001 \
    --thumb assets/templates/quotes/VD-001-quote.png --dang-that

# Đăng một bài ảnh quote (dùng xen giữa các video)
python3 scripts/dang-video-fb.py anh assets/templates/quotes/VD-002-quote.png --ma VD-002 --dang-that
```

Script **mặc định chạy thử** — phải có `--dang-that` mới thật sự đăng. Caption lấy tự động từ `content/captions/<mã>-caption.md`.

## Lưu ý
- Video 1:1 đăng qua `/videos` là **bài video thường** trên Page. Muốn lên **Reels** thì dùng luồng `/video_reels` (tải theo 3 bước) — cần thì bổ sung sau.
- Script đang gọi API `v21.0`; nếu Facebook báo lỗi phiên bản thì sửa biến `API` trong `scripts/dang-video-fb.py`.
- Token là chìa khoá Page: chỉ để trong `.env` (đã bị `.gitignore` chặn), đừng dán vào chat hay commit.
