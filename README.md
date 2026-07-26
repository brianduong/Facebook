# Facebook — Kênh nội dung lan toả thông điệp tốt

Dự án sản xuất và đăng tải video mang **thông điệp tích cực cho cuộc sống** lên Facebook Page.

Đây là "trung tâm điều hành" của kênh: nơi lưu ý tưởng, kịch bản, caption, lịch đăng và tài sản thiết kế. Riêng file video gốc/đã render **không lưu trên GitHub** (xem [.gitignore](.gitignore)) vì dung lượng lớn — chúng nằm ở máy/ổ cứng/cloud của anh.

## Cấu trúc thư mục

```
Facebook/
├── content/            # Phần "nội dung chữ" — đưa lên GitHub
│   ├── ideas/          # Kho ý tưởng, chủ đề còn thô
│   ├── scripts/        # Kịch bản video hoàn chỉnh
│   │   ├── song-ngu/   # EN + VI đặt cạnh nhau — chỗ DUYỆT chữ, nuôi cả hai kênh
│   │   └── loi-doc/    # Lời đọc thuần văn bản (máy render đọc file này — sinh tự động)
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

1. **Ý tưởng** → ghi vào [content/ideas/](content/ideas/) — kênh Việt: [kho-y-tuong.md](content/ideas/kho-y-tuong.md) · kênh Anh: [kho-y-tuong-en.md](content/ideas/kho-y-tuong-en.md)
2. **Kịch bản** → viết theo mẫu [content/scripts/](content/scripts/)
3. **Duyệt chữ** → file song ngữ EN/VI trong [content/scripts/song-ngu/](content/scripts/song-ngu/), sửa xong đánh ✅ rồi chạy `tach-loi-doc.py` (xem [docs/giong-van-tieng-viet.md](docs/giong-van-tieng-viet.md))
4. **Sản xuất** → dựng theo [docs/huong-dan-dung-video.md](docs/huong-dan-dung-video.md), file để trong `video/` (ngoài GitHub)
5. **Caption** → soạn bài đăng trong [content/captions/](content/captions/)
6. **Lên lịch** → cập nhật [schedule/calendar.md](schedule/calendar.md)
7. **Đăng** → bấm tay trên Page, hoặc chạy [scripts/dang-video-fb.py](scripts/dang-video-fb.py) (xem [docs/huong-dan-dang-tu-dong.md](docs/huong-dan-dang-tu-dong.md))

## Công cụ trong `scripts/`

### Quy trình chính (bản mới — Reels 9:16, ảnh thật, giọng VieNeu)

| Lệnh | Làm gì |
|------|--------|
| `python3 scripts/tach-loi-doc.py VD-001` | Rút bản VI trong file song ngữ ra lời đọc (từ chối chạy nếu anh chưa duyệt; báo luôn thời lượng ước tính) |
| `python3 scripts/tach-loi-doc.py VD-001 --xem` | Chỉ in bản VI ra màn hình để đọc to thử, không ghi file |
| `python3 scripts/tach-loi-doc.py VD-001 --dong-bo` | Dựng lại phần "Đọc liền mạch" ở đầu file song ngữ sau khi sửa chữ (chưa duyệt cũng chạy được) |
| `python3 scripts/tach-loi-doc.py VD-001 --en` | Rút khối **EN** ra lời đọc cho kênh One Small Thing |
| `.venv-tts/bin/python scripts/thu-giong-piper.py` | Nghe thử giọng tiếng Anh (Piper, chạy offline) |
| `.venv-tts/bin/python scripts/render-video-v2.py VD-001 --en --nhac assets/music/nen-am-ap.m4a` | **Render bản tiếng Anh** — giọng Piper, logo và lời kêu gọi của One Small Thing |
| `python3 scripts/tai-anh-pexels.py VD-001` | Tải ảnh chụp thật từ Pexels theo từ khoá B-roll ghi trong kịch bản (lấy luôn ảnh đầu tiên) |
| `python3 scripts/tai-anh-pexels.py VD-001 --chon 6` | **Nên dùng cái này** — lấy 6 ứng viên mỗi từ khoá, ghép thành một bảng ảnh có số để xem một lượt |
| `python3 scripts/tai-anh-pexels.py VD-001 --lay 4,10,18` | Sau khi xem bảng, lấy đúng những số đã chấm (thứ tự gõ = thứ tự xuất hiện trong video) |
| `.venv-tts/bin/python scripts/thu-giong-vieneu.py --liet-ke` | Xem 14 giọng VieNeu có sẵn |
| `.venv-tts/bin/python scripts/thu-giong-vieneu.py` | Nghe thử vài giọng trên cùng một đoạn chữ |
| `.venv-tts/bin/python scripts/render-video-v2.py VD-001 --chi-do-dai` | Đo thử bài dài bao nhiêu giây (chưa cần ảnh, chưa render) |
| `.venv-tts/bin/python scripts/render-video-v2.py VD-001 --nhac assets/music/nen-am-ap.m4a` | **Render Reels 9:16** — ảnh thật + chữ theo timeline + giọng VieNeu |
| `python3 scripts/tao-anh-bia-reels.py VD-001 "Câu quote." --anh 2` | Tạo ảnh bìa Reels 9:16 (ảnh quote 1:1 cũ lên Reels bị cắt) |

> ⚠️ Ba lệnh giọng/render phải chạy bằng `.venv-tts/bin/python`, không phải `python3`.
> Lý do: `onnxruntime` chưa có bản cho Python 3.14 của máy nên môi trường TTS dựng riêng trên Python 3.13.
> Dựng lại môi trường khi cần: `/usr/local/opt/python@3.13/bin/python3.13 -m venv .venv-tts && .venv-tts/bin/pip install vieneu`

### Công cụ khác

| Lệnh | Làm gì |
|------|--------|
| `python3 scripts/tao-anh-quote.py VD-007 "Dòng 1" "Dòng 2"` | Tạo ảnh quote 1:1 đúng nhận diện kênh (SVG + PNG) |
| `python3 scripts/render-video-nhap.py VD-001 --nhan-vat chi --canh ban-tra` | Render video vuông 1:1 bản cũ — *đã ngừng dùng* (nhân vật vẽ tay nhìn rẻ tiền) |
| `python3 scripts/xem-thu.py` | Xem thử 4 nhân vật + 6 cảnh nền của bản cũ |
| `python3 scripts/so-sanh-giong.py VD-001` | Nghe so sánh giọng `say` đều vs có ngữ điệu (bản cũ) |
| `python3 scripts/tao-nhac-nen.py` | Tự tổng hợp nhạc nền **gốc** của kênh (3 kiểu, không lo bản quyền) |
| `python3 scripts/lay-token-dai-han.py --app-id ...` | Đổi token Facebook ngắn hạn thành token Page dùng lâu dài |
| `./scripts/tao-giong-doc.sh VD-001 138` | Chỉ tạo giọng đọc **nháp** + đo thời lượng (cảnh báo nếu dưới 60s) |
| `python3 scripts/dang-video-fb.py kiem-tra` | Kiểm tra Page Access Token |
| `python3 scripts/dang-video-fb.py video <file> --ma VD-001 --dang-that` | Đăng video + caption lên Page |

## Định hướng

- Tiến độ hiện tại: [STATUS.md](STATUS.md)
- Kế hoạch tổng thể: [PLAN.md](PLAN.md)
- **Cách viết lời đọc nghe ra tiếng Việt: [docs/giong-van-tieng-viet.md](docs/giong-van-tieng-viet.md)**
- Lấy Pexels API key để tải ảnh nền: [docs/lay-pexels-api-key.md](docs/lay-pexels-api-key.md)
- **Đăng Reels lên Page từng bước: [docs/huong-dan-dang-reels.md](docs/huong-dan-dang-reels.md)**
- Nhận diện & bảng màu: [docs/dinh-huong-kenh.md](docs/dinh-huong-kenh.md)
- Kiếm tiền: [docs/ke-hoach-kiem-tien.md](docs/ke-hoach-kiem-tien.md)
