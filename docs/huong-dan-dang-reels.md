# Đăng Reels lên Page Sống Tốt — từng bước bấm

Từ 26/07/2026 kênh đăng **Reels dọc 9:16**, không đăng video thường nữa.
Lý do: Reels được Facebook phân phối tới người **chưa** theo dõi, nên tăng follower
nhanh hơn nhiều; còn video thường chủ yếu hiện với người đã theo dõi.

## Chuẩn bị 3 thứ

| Thứ | Ở đâu |
|---|---|
| File video | `video/exports/VD-00X-reels.mp4` |
| Ảnh bìa 9:16 | `video/thumbnails/VD-00X-bia.png` |
| Caption | `content/captions/VD-00X-caption.md`, phần *"Caption đăng Facebook"* |

Tạo ảnh bìa nếu chưa có:
```bash
python3 scripts/tao-anh-bia-reels.py VD-002 "Câu quote ngắn." --anh 2
```

> ⚠️ **Đừng dùng ảnh trong `assets/templates/quotes/`** làm bìa Reels — đó là khung
> vuông 1:1, lên Reels bị cắt mất hai đầu.

## Các bước bấm (trên máy tính)

1. Mở https://www.facebook.com/songtot.in — đảm bảo đang ở **chế độ Trang**
   (ảnh đại diện góc trên phải là logo mầm cây Sống Tốt, không phải ảnh cá nhân anh).
2. Bấm **"Reels"** trong khu vực tạo bài. Nếu không thấy, bấm **"Công cụ đăng"
   / "Meta Business Suite"** → **Tạo Reels**.
3. **Tải video lên**: kéo `VD-00X-reels.mp4` vào, hoặc bấm *Thêm video*.
   Chờ Facebook xử lý xong (thanh tiến trình chạy hết).
4. Bước **Chỉnh sửa**: bỏ qua hết — **không** thêm nhạc của Facebook (video đã có
   nhạc nền gốc của kênh; thêm nhạc Facebook sẽ chồng lên giọng đọc và có thể
   làm video mất quyền kiếm tiền).
5. Bước **Ảnh bìa / Thumbnail**: chọn **"Tải lên"** rồi chọn `VD-00X-bia.png`.
   Đừng để Facebook tự chọn khung — nó hay lấy khung mờ lúc chuyển cảnh.
6. **Dán caption** vào ô mô tả. Copy nguyên phần *"Caption đăng Facebook"* trong
   file caption, **kèm cả dòng `Ảnh: Pexels.com`** ở cuối (điều khoản Pexels API
   bắt buộc dẫn nguồn).
7. Dán **hashtag** xuống dưới cùng, sau caption.
8. **Lên lịch**: bấm mũi tên cạnh nút *Đăng* → **Lên lịch** → chọn **20:00 hôm nay**.
   (Nhịp kênh là mỗi ngày 1 video, 20:00.)
9. Bấm **Lên lịch / Đăng**.

## Sau khi đăng

- Sau **24–48 giờ**, vào **Meta Business Suite → Thông tin chi tiết → Nội dung**
  lấy 3 số: **lượt xem**, **lượt xem hết**, **tương tác** (thích + bình luận + chia sẻ).
- Ghi vào bảng *"Ghi nhận hiệu quả"* trong [schedule/calendar.md](../schedule/calendar.md).
  Có số thật mới biết chủ đề nào ăn, để soạn tiếp theo hướng đó.
- **Trả lời bình luận trong 1–2 giờ đầu.** Câu kết của mọi video đều mời người xem
  kể chuyện của họ — có người kể mà không ai trả lời thì lần sau họ không kể nữa,
  và Facebook cũng đọc tương tác sớm để quyết định đẩy tiếp hay không.

## Những chỗ dễ sai

| Sai | Hậu quả |
|---|---|
| Đăng dạng **video thường** thay vì Reels | Mất phần phân phối tới người chưa theo dõi |
| Thêm nhạc của Facebook | Chồng lên giọng đọc; có thể mất quyền kiếm tiền |
| Để Facebook tự chọn ảnh bìa | Hay lấy khung mờ lúc chuyển cảnh |
| Quên dòng `Ảnh: Pexels.com` | Vi phạm điều khoản Pexels API |
| Đăng bằng tài khoản cá nhân | Bài không thuộc Page, không tính vào chỉ tiêu kiếm tiền |
