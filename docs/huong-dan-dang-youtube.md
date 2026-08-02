# Hướng dẫn đăng video YouTube tự động

> Mục đích: chạy **một dòng lệnh** là video + tiêu đề + mô tả + thẻ + danh mục tự lên kênh,
> khỏi ngồi dán tay từng ô.
> Script: `scripts/dang-video-youtube.py` · Môi trường: `.venv-dang/`

**Làm mục A và B một lần duy nhất.** Xong rồi thì mỗi ngày chỉ còn mục D — hai dòng lệnh.

---

## ⚠️ Đọc chỗ này trước — luật của YouTube, không lách được

**Video đăng qua API từ một project chưa qua vòng audit sẽ bị YouTube khoá cứng ở chế độ
riêng tư (private).** Mình xin `public` thì API vẫn nhận, nhưng YouTube âm thầm để lại
`private`. Đây là chính sách của Google từ tháng 7/2020, áp cho mọi project mới — không
phải lỗi script, và không sửa được bằng code.

Nghĩa là quy trình thật sẽ là:

1. Script tải video lên, điền sẵn tiêu đề · mô tả · thẻ · danh mục · khai báo trẻ em
2. Anh vào Studio bấm **Công khai** — hai cú bấm

Vẫn đáng làm, vì phần nặng là tải file và dán bốn ô chữ, không phải cú bấm cuối.

**Muốn bỏ luôn bước bấm tay** thì phải nộp đơn xin audit — xem mục E. Được duyệt rồi thì
chỉ cần thêm `--che-do public` là chạy thẳng, không phải sửa gì trong script.

---

## A. Dựng project bên Google (một lần)

### A1. Tạo project và bật API

1. Mở **https://console.cloud.google.com** — đăng nhập bằng **đúng Gmail đang quản lý hai kênh**
2. Thanh trên cùng, bấm ô chọn project → **New Project**
3. **Project name**: `One Small Thing Poster` → **Create** — đợi ~10 giây
4. Chắc chắn thanh trên đang hiện đúng project vừa tạo (rất dễ tạo xong mà vẫn đứng ở project cũ)
5. Vào **APIs & Services → Library**, gõ tìm `YouTube Data API v3` → bấm vào nó → **Enable**

### A2. Khai màn hình xin quyền

Google đổi tên khu này trong bản console mới, nên anh có thể thấy một trong hai kiểu:
menu **Google Auth Platform** (mới), hoặc **APIs & Services → OAuth consent screen** (cũ).
Nội dung cần điền như nhau.

1. **User type / Audience**: chọn **External** → **Create**
2. **App name**: `One Small Thing Poster`
3. **User support email**: chọn Gmail của anh
4. **Developer contact email**: gõ lại Gmail của anh
5. **Save and Continue** — mục **Scopes** cứ bỏ qua, script tự xin lúc chạy
6. Mục **Test users**: bấm **Add users**, thêm chính Gmail của anh

### A3. ⚠️ Chuyển sang "In production" — bước hay bị bỏ sót nhất

Ở màn hình **Audience** (hoặc **OAuth consent screen**), tìm mục **Publishing status**:

- Đang là **Testing** → bấm **Publish app** → **Confirm**

**Vì sao bắt buộc:** để ở Testing thì Google **thu hồi quyền sau đúng 7 ngày**, tuần sau
chạy lại sẽ báo lỗi và phải xin quyền lại từ đầu. Chuyển sang In production thì quyền dùng
được lâu dài.

Đổi sang In production **không** có nghĩa là app đã được Google kiểm duyệt. Lúc xin quyền
vẫn hiện màn hình cảnh báo — mục C nói cách đi qua.

### A4. Tạo chìa khoá

1. Vào **APIs & Services → Credentials** (bản mới: **Google Auth Platform → Clients**)
2. **Create Credentials → OAuth client ID**
3. **Application type**: chọn **Desktop app** — ⚠️ chọn nhầm *Web application* là hỏng, script chạy trên máy
4. **Name**: `May cua Brian` → **Create**
5. Hộp thoại hiện ra → bấm **Download JSON**
6. Đổi tên file vừa tải thành **`.google-client-secret.json`** rồi để vào **gốc repo**
   (`/Users/mac/Miganet/OneSmallThing/`)

```bash
# Chép từ Downloads vào repo, đổi tên luôn — sửa tên file cho khớp cái vừa tải
mv ~/Downloads/client_secret_*.json /Users/mac/Miganet/OneSmallThing/.google-client-secret.json
```

🔒 File này đã nằm trong `.gitignore`, không lên GitHub. **Ai có nó là đăng và xoá được
video trên kênh** — đừng gửi qua chat hay email.

---

## B. Dựng môi trường chạy (một lần)

Đã dựng sẵn rồi. Chỉ khi nào mất thư mục `.venv-dang/` mới cần làm lại:

```bash
cd /Users/mac/Miganet/OneSmallThing
/usr/local/opt/python@3.13/bin/python3.13 -m venv .venv-dang
.venv-dang/bin/pip install google-api-python-client google-auth-oauthlib
```

⚠️ Script này chạy bằng `.venv-dang/bin/python`, **không phải `python3`** — giống như
render video phải chạy bằng `.venv-tts/bin/python`.

---

## C. Xin quyền cho từng kênh (một lần mỗi kênh)

Hai kênh xin riêng, mỗi kênh một chìa. Bắt đầu bằng kênh tiếng Anh:

```bash
cd /Users/mac/Miganet/OneSmallThing
.venv-dang/bin/python scripts/dang-video-youtube.py xin-quyen --kenh en
```

Trình duyệt tự mở. Làm theo thứ tự này:

1. **Chọn tài khoản Google** đang quản lý kênh
2. Hiện màn hình đỏ **"Google hasn't verified this app"** → bấm **Advanced** (hoặc *Nâng cao*)
   → bấm **Go to One Small Thing Poster (unsafe)**.
   Chữ *unsafe* nghe đáng sợ nhưng đây là app của chính anh, chưa nộp kiểm duyệt thôi.
3. ⚠️ **Nếu hiện màn hình chọn kênh** (tài khoản quản lý nhiều kênh thì có bước này) —
   **chọn đúng One Small Thing**. Chọn nhầm là về sau đăng bài tiếng Anh sang kênh tiếng Việt.
4. Bấm **Continue** để cho phép tải video lên
5. Trình duyệt báo xong → quay lại cửa sổ dòng lệnh

Kiểm tra ngay xem có nối đúng kênh không:

```bash
.venv-dang/bin/python scripts/dang-video-youtube.py kiem-tra --kenh en
```

Nó in ra tên kênh đang nối và tên kênh mong đợi — **hai dòng phải khớp nhau**. Lệch thì
xoá chìa rồi làm lại:

```bash
rm .youtube-token-en.json
.venv-dang/bin/python scripts/dang-video-youtube.py xin-quyen --kenh en
```

Xong kênh tiếng Anh thì làm y hệt cho kênh tiếng Việt, đổi `--kenh en` thành `--kenh vi`,
và ở bước 3 chọn kênh **Sống Tốt**.

---

## D. Đăng bài — việc làm hằng ngày

**Bước 1 — xem trước.** Không gửi gì lên mạng, chỉ in ra những gì sắp gửi:

```bash
.venv-dang/bin/python scripts/dang-video-youtube.py dang VD-009 --kenh en
```

Đọc lại tiêu đề, mô tả, thẻ. Sai chỗ nào thì sửa trong `content/captions/VD-009-caption-en.md`
rồi chạy lại — chữ lấy thẳng từ file đó, không gõ tay vào lệnh.

**Bước 2 — đăng thật.** Thêm `--dang-that`:

```bash
.venv-dang/bin/python scripts/dang-video-youtube.py dang VD-009 --kenh en --dang-that
```

Xong nó in ra link video và link Studio. Vào Studio bấm **Công khai**.

**Hẹn giờ** — muốn video tự lên lúc 8 giờ tối mai:

```bash
.venv-dang/bin/python scripts/dang-video-youtube.py dang VD-009 --kenh en \
    --hen-gio 2026-08-03T20:00:00+07:00 --dang-that
```

⚠️ Hẹn giờ **chỉ chạy sau khi project đã qua audit**. Chưa qua audit thì video vẫn nằm im
ở chế độ riêng tư, đến giờ cũng không tự lên.

### Script tự lo sẵn những gì

| Ô trên YouTube | Script điền |
|---|---|
| Tiêu đề · Mô tả · Thẻ | bóc từ file caption, đúng khối trong dấu ``` |
| Danh mục | **Con người và Blog** — khỏi phải bấm "Hiện thêm" tìm nữa |
| Đối tượng | **Không dành cho trẻ em** |
| Ngôn ngữ | theo kênh |

### Script chặn trước khi gửi

Tiêu đề quá 100 ký tự · mô tả quá 5.000 · thẻ cộng lại quá 500 · mô tả có dấu `<` `>`
(YouTube cấm) — mấy lỗi này script **không đăng**, báo ra để sửa file caption.

Còn thiếu `#Shorts` trong tiêu đề hay thiếu dòng ghi nguồn Pexels thì chỉ **nhắc**, vẫn
đăng nếu anh muốn.

---

## E. Xin audit để bỏ hẳn bước bấm tay

Chỉ nên làm khi đã đăng đều đặn một thời gian.

1. Mở **https://support.google.com/youtube/contact/yt_api_form**
2. Điền tên project Google Cloud (`One Small Thing Poster`) và số hiệu project
3. Mô tả cách dùng: *"Tải lên video do chính mình sản xuất, lên kênh của chính mình. Không
   thay mặt người dùng nào khác."*
4. Đợi Google trả lời — thường vài tuần

Duyệt rồi thì thêm `--che-do public` là video lên thẳng, không phải vào Studio nữa.

---

## F. Hạn mức mỗi ngày

Google cho mỗi project **10.000 điểm/ngày**, mỗi lần đăng tốn **1.600 điểm** →
**tối đa 6 video/ngày**.

Nhịp một bài/ngày × ba nơi thì chỉ tốn 3.200 điểm (hai kênh YouTube), thừa sức. Nhưng
**hôm nào đăng dồn nhiều bài thì phải để ý** — quá là API báo lỗi hết hạn mức.

Hạn mức reset lúc 0h giờ Thái Bình Dương, tức khoảng **14–15h giờ Việt Nam**.

---

## G. Hỏng thì xem đây

| Hiện tượng | Nguyên nhân thật | Cách sửa |
|---|---|---|
| `Thiếu thư viện Google` | Chạy bằng `python3` thay vì `.venv-dang/bin/python` | Chạy lại đúng lệnh trong mục D |
| `Chưa có quyền cho kênh…` | Chưa xin quyền, hoặc quyền hết hạn | Chạy lại `xin-quyen` |
| Tuần trước chạy được, giờ đòi xin lại | Màn hình đồng ý vẫn ở **Testing** → Google thu hồi sau 7 ngày | Làm mục **A3**, chuyển sang In production |
| `kiem-tra` in ra tên kênh khác | Lúc xin quyền chọn nhầm tài khoản hoặc nhầm kênh | `rm .youtube-token-<kênh>.json` rồi xin lại |
| Đăng xong video vẫn riêng tư | Đúng như dự kiến — project chưa qua audit | Vào Studio bấm công khai, hoặc làm mục E |
| `Hết hạn mức API trong ngày` | Quá 6 lượt đăng trong ngày | Đợi tới ~14–15h giờ Việt Nam |
| `không có mục '# Đăng YouTube Shorts'` | File caption đời cũ (VD-001 → VD-003) khuôn khác | Sửa file caption theo khuôn VD-004 trở đi |

---

## Liên quan

- Đăng Facebook: `docs/huong-dan-dang-tu-dong.md` · script `scripts/dang-video-fb.py`
- Ba nơi phát hành và tên gọi quy ước: `STATUS.md`
- Luật viết caption tiếng Anh: `docs/ke-hoach-kenh-tieng-anh.md`
