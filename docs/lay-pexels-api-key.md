# Lấy Pexels API key (miễn phí, ~2 phút)

## Key này để làm gì

Từ 26/07 video của kênh không dùng nhân vật vẽ tay nữa — nền là **ảnh chụp thật**.
Script `scripts/tai-anh-pexels.py` tự tìm và tải ảnh về theo từ khoá ghi trong kịch bản,
nhưng Pexels chỉ cho tải qua API nếu có key. Key giống như thẻ ra vào: không có thì
script bị chặn ngay từ bước đầu.

Không có key thì vẫn render được, nhưng phải tự đi tìm ảnh rồi bỏ tay vào thư mục
`assets/images/canh/VD-00X/` — mỗi ngày một video thì rất mất công.

## Các bước bấm

1. Mở https://www.pexels.com/api/
2. Bấm nút **"Get Started"** (nút xanh giữa trang).
3. Trang đăng nhập hiện ra:
   - Chưa có tài khoản Pexels → bấm **"Join"** / **"Sign up"**, hoặc chọn
     **Continue with Google** cho nhanh (dùng luôn Gmail của anh).
   - Có rồi → **Log in**.
4. Đăng nhập xong, Pexels hỏi **mô tả ứng dụng dùng API để làm gì**. Điền đại ý:

   | Ô | Điền |
   |---|---|
   | Tên ứng dụng | `Song Tot` |
   | Mô tả | `Tải ảnh nền cho video thông điệp tích cực đăng trên Facebook Page.` |
   | Website / URL | `https://www.facebook.com/songtot.in` |

5. Bấm gửi → **key hiện ra ngay lập tức** trên màn hình (một chuỗi chữ và số dài).
6. Copy chuỗi đó.

Sau này quên key thì vào lại https://www.pexels.com/api/new/ là thấy.

## Dán key vào đâu

Mở file `.env` ở thư mục gốc dự án, tìm dòng:

```
PEXELS_API_KEY=
```

Dán key vào ngay sau dấu `=`, **không có dấu cách, không có dấu nháy**:

```
PEXELS_API_KEY=abc123xyz...
```

Lưu lại. File `.env` nằm trong `.gitignore` nên key **không bị đẩy lên GitHub**.

## Kiểm tra đã được chưa

```bash
python3 scripts/tai-anh-pexels.py VD-002
```

- Được → in ra danh sách ảnh đã tải kèm tên người chụp.
- Sai key → báo `❌ PEXELS_API_KEY sai hoặc hết hạn`.
- Chưa dán → báo `❌ Chưa có PEXELS_API_KEY` kèm hướng dẫn.

## ⚠️ Bắt buộc ghi nguồn

Giấy phép **ảnh** của Pexels không bắt ghi nguồn, nhưng điều khoản **API** thì có:

> *"Whenever you are doing an API request make sure to show a prominent link to Pexels."*

Mình lấy ảnh qua API nên phải theo. Cách làm gọn nhất: thêm một dòng ở cuối
caption Facebook:

```
Ảnh: Pexels.com
```

Script tự ghi tên từng người chụp vào `assets/images/canh/VD-00X/nguon.txt`
nếu anh muốn ghi đầy đủ hơn.

## Hạn mức

200 lượt/giờ · 20.000 lượt/tháng — miễn phí. Mỗi video tốn 4–5 lượt, nên nhịp
1 video/ngày dùng chưa tới 1% hạn mức.
