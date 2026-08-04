# Quy tắc vận hành bắt buộc

Đọc `STATUS.md` và `schedule/calendar.md` trước khi đăng để lấy trạng thái mới nhất.

## Lịch đăng cố định

- Mỗi nền tảng nhiều nhất **1 bài/ngày**.
- Giờ công khai cố định: **19:30 giờ Việt Nam** (`Asia/Ho_Chi_Minh`, UTC+7).
- Khi có một lô bài, xếp bài đầu vào **19:30 gần nhất còn trống**. Chỉ dùng 19:30 tối nay
  nếu còn ít nhất 10 phút; nếu không thì bắt đầu từ 19:30 ngày mai.
- Mỗi bài tiếp theo vào 19:30 của từng ngày liên tiếp. Không tự đổi sang giờ khác.
- Đồng bộ cùng mã bài, cùng ngày và cùng giờ trên YouTube tiếng Việt, YouTube tiếng Anh
  và Facebook; ngoại lệ phải do anh yêu cầu rõ.
- Facebook video dọc phải đăng bằng `scripts/dang-video-fb.py reels`, không dùng `video`.
- Sau mỗi đợt lên lịch, **bắt buộc đọc lại API**, khớp ngày, giờ và câu đầu caption.
  Nếu có lịch trùng thì giữ một bản và xóa bản trùng ngay.

Không ghi token hoặc App Secret vào tài liệu, Git hay nội dung chat.
