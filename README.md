# Facebook — Kênh nội dung lan toả thông điệp tốt

Dự án sản xuất và đăng tải video mang **thông điệp tích cực cho cuộc sống** lên Facebook Page.

Đây là "trung tâm điều hành" của kênh: nơi lưu ý tưởng, kịch bản, caption, lịch đăng và tài sản thiết kế. Riêng file video gốc/đã render **không lưu trên GitHub** (xem [.gitignore](.gitignore)) vì dung lượng lớn — chúng nằm ở máy/ổ cứng/cloud của anh.

## Cấu trúc thư mục

```
Facebook/
├── content/            # Phần "nội dung chữ" — đưa lên GitHub
│   ├── ideas/          # Kho ý tưởng, chủ đề còn thô
│   ├── scripts/        # Kịch bản video hoàn chỉnh
│   │   └── loi-doc/    # Lời đọc thuần văn bản (để thu giọng / tạo giọng nháp)
│   ├── captions/       # Nội dung bài đăng (caption + hashtag) cho Facebook
│   └── research/       # Tư liệu, trích dẫn, nguồn tham khảo
│
├── assets/             # Tài sản thiết kế dùng lại — đưa lên GitHub (nếu nhẹ)
│   ├── logo/           # Logo, watermark kênh
│   ├── images/         # Ảnh nền, ảnh minh hoạ
│   ├── music/          # Nhạc nền (lưu ý bản quyền)
│   ├── fonts/          # Font chữ
│   └── templates/      # Khung video 1:1
│       └── quotes/     # Ảnh quote 1:1 từng video (thumbnail + cảnh kết)
│
├── video/              # File video — KHÔNG đưa lên GitHub
│   ├── raw/            # Footage quay gốc
│   ├── edit/           # File dự án đang dựng
│   ├── exports/        # Video đã render, sẵn sàng đăng
│   └── thumbnails/     # Ảnh bìa
│
├── schedule/           # Lịch đăng bài, kế hoạch nội dung theo tuần/tháng
├── docs/               # Tài liệu: định hướng kênh, brand guide, quy trình
└── scripts/            # Công cụ tự động (tạo ảnh quote, giọng nháp, đăng bài)
```

## Quy trình gợi ý (từ ý tưởng → đăng bài)

1. **Ý tưởng** → ghi vào [content/ideas/](content/ideas/)
2. **Kịch bản** → viết theo mẫu [content/scripts/](content/scripts/)
3. **Sản xuất** → dựng theo [docs/huong-dan-dung-video.md](docs/huong-dan-dung-video.md), file để trong `video/` (ngoài GitHub)
4. **Caption** → soạn bài đăng trong [content/captions/](content/captions/)
5. **Lên lịch** → cập nhật [schedule/calendar.md](schedule/calendar.md)
6. **Đăng** → bấm tay trên Page, hoặc chạy [scripts/dang-video-fb.py](scripts/dang-video-fb.py) (xem [docs/huong-dan-dang-tu-dong.md](docs/huong-dan-dang-tu-dong.md))

## Công cụ trong `scripts/`

| Lệnh | Làm gì |
|------|--------|
| `python3 scripts/tao-anh-quote.py VD-007 "Dòng 1" "Dòng 2"` | Tạo ảnh quote 1:1 đúng nhận diện kênh (SVG + PNG) |
| `python3 scripts/render-video-nhap.py VD-001 --nhan-vat chi --canh ban-tra` | **Render cả video nháp 1:1** — nhân vật kể, cảnh nền, chữ khớp giọng đọc |
| `python3 scripts/xem-thu.py` | Xem thử 4 nhân vật + 6 cảnh nền trước khi render |
| `python3 scripts/so-sanh-giong.py VD-001` | Nghe so sánh giọng đọc đều vs giọng có ngữ điệu |
| `./scripts/tao-giong-doc.sh VD-001 138` | Chỉ tạo giọng đọc **nháp** + đo thời lượng (cảnh báo nếu dưới 60s) |
| `python3 scripts/dang-video-fb.py kiem-tra` | Kiểm tra Page Access Token |
| `python3 scripts/dang-video-fb.py video <file> --ma VD-001 --dang-that` | Đăng video + caption lên Page |

## Định hướng

- Tiến độ hiện tại: [STATUS.md](STATUS.md)
- Kế hoạch tổng thể: [PLAN.md](PLAN.md)
- Nhận diện & bảng màu: [docs/dinh-huong-kenh.md](docs/dinh-huong-kenh.md)
- Kiếm tiền: [docs/ke-hoach-kiem-tien.md](docs/ke-hoach-kiem-tien.md)
