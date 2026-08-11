# Quy tắc vận hành bắt buộc

Đọc `STATUS.md` và `schedule/calendar.md` trước khi đăng để lấy trạng thái mới nhất.

## Lịch đăng cố định

- **Nhịp đăng: 2 ngày 1 bài** (anh chốt 11/08/2026). Đăng ngày 14/08 thì bài kế tiếp
  là 16/08, không phải 15/08.
- Giờ công khai cố định: **19:30 giờ Việt Nam** (`Asia/Ho_Chi_Minh`, UTC+7).
- **Neo chuỗi ngày vào bài đã LÊN SÓNG gần nhất, không phải bài đã xếp lịch gần nhất.**
  Lấy ngày đó cộng 2, cộng 4, cộng 6… ra chuỗi mốc; mọi bài đang chờ đều phải nằm trên
  chuỗi này. Ví dụ 10/08 vừa lên → chuỗi là 12/08 · 14/08 · 16/08.
- **Đổi nhịp thì phải dời cả lịch đang chờ**, không chỉ áp cho bài mới. Bỏ sót chỗ này
  thì lịch cũ và lịch mới lẫn vào nhau — đúng lỗi đã mắc ngày 11/08.
- Nếu mốc tính ra đã trôi qua (bỏ nhịp lâu), lấy **19:30 gần nhất còn ít nhất 10 phút**
  làm bài đầu, rồi lại cách 2 ngày cho các bài sau.
- Khi có một lô bài, xếp lần lượt cách nhau 2 ngày. Không tự đổi sang giờ khác.
- **Dời lịch bài đã tải lên:**
  - YouTube: `scripts/dang-video-youtube.py doi-lich VD-0XX --kenh vi --hen-gio … --dang-that`
    (chạy thử trước khi bỏ `--dang-that`). Chỉ dời được khi video còn `private`.
  - Facebook: `POST /{video-id}` với `scheduled_publish_time`.
- Đồng bộ cùng mã bài, cùng ngày và cùng giờ trên YouTube tiếng Việt, YouTube tiếng Anh
  và Facebook; ngoại lệ phải do anh yêu cầu rõ.
- Facebook video dọc phải đăng bằng `scripts/dang-video-fb.py reels`, không dùng `video`.
- Sau mỗi đợt lên lịch, **bắt buộc đọc lại API**, khớp ngày, giờ và câu đầu caption.
  Nếu có lịch trùng thì giữ một bản và xóa bản trùng ngay.

Không ghi token hoặc App Secret vào tài liệu, Git hay nội dung chat.
