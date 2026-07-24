# Facebook — Kênh nội dung lan toả thông điệp tốt

Dự án sản xuất và đăng tải video mang **thông điệp tích cực cho cuộc sống** lên Facebook Page.

Đây là "trung tâm điều hành" của kênh: nơi lưu ý tưởng, kịch bản, caption, lịch đăng và tài sản thiết kế. Riêng file video gốc/đã render **không lưu trên GitHub** (xem [.gitignore](.gitignore)) vì dung lượng lớn — chúng nằm ở máy/ổ cứng/cloud của anh.

## Cấu trúc thư mục

```
Facebook/
├── content/            # Phần "nội dung chữ" — đưa lên GitHub
│   ├── ideas/          # Kho ý tưởng, chủ đề còn thô
│   ├── scripts/        # Kịch bản video hoàn chỉnh
│   ├── captions/       # Nội dung bài đăng (caption + hashtag) cho Facebook
│   └── research/       # Tư liệu, trích dẫn, nguồn tham khảo
│
├── assets/             # Tài sản thiết kế dùng lại — đưa lên GitHub (nếu nhẹ)
│   ├── logo/           # Logo, watermark kênh
│   ├── images/         # Ảnh nền, ảnh minh hoạ
│   ├── music/          # Nhạc nền (lưu ý bản quyền)
│   ├── fonts/          # Font chữ
│   └── templates/      # Mẫu thiết kế (Canva/CapCut link, khung intro/outro)
│
├── video/              # File video — KHÔNG đưa lên GitHub
│   ├── raw/            # Footage quay gốc
│   ├── edit/           # File dự án đang dựng
│   ├── exports/        # Video đã render, sẵn sàng đăng
│   └── thumbnails/     # Ảnh bìa
│
├── schedule/           # Lịch đăng bài, kế hoạch nội dung theo tuần/tháng
├── docs/               # Tài liệu: định hướng kênh, brand guide, quy trình
└── scripts/            # Script tự động (đổi tên file, xử lý ảnh...) nếu cần
```

## Quy trình gợi ý (từ ý tưởng → đăng bài)

1. **Ý tưởng** → ghi vào [content/ideas/](content/ideas/)
2. **Kịch bản** → viết theo mẫu [content/scripts/](content/scripts/)
3. **Sản xuất** → quay/dựng, file để trong `video/` (ngoài GitHub)
4. **Caption** → soạn bài đăng trong [content/captions/](content/captions/)
5. **Lên lịch** → cập nhật [schedule/calendar.md](schedule/calendar.md)
6. **Đăng** → đăng lên Facebook Page, đánh dấu hoàn thành

## Định hướng

Xem [PLAN.md](PLAN.md) để biết kế hoạch tổng thể và những phần đang chờ anh bổ sung.
