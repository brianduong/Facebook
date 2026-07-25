# STATUS — Ghi chú tiến độ

_Cập nhật: 2026-07-25_

## Đã xong ✅

**Nhận diện & Page**
- Icon `assets/logo/icon-song-tot.png`, banner `assets/images/banner-song-tot.png`, khung video 1:1 — palette chốt trong `docs/dinh-huong-kenh.md`.
- Anh đã đổi **ảnh đại diện + ảnh bìa** trên Page (25/07).

**Nội dung — 6 video đã đủ nguyên liệu (đăng tới giữa tháng 8)**
| Mã | Tên | Lời đọc |
|----|-----|---------|
| VD-001 | Ba điều biết ơn mỗi sáng | 64s |
| VD-002 | Tử tế không bao giờ là điều lãng phí | 64s |
| VD-003 | Hôm nay chỉ cần làm được một việc | 66s |
| VD-004 | Cảm ơn phải nói rõ lý do | 62s |
| VD-005 | Người bạn lâu không hỏi thăm | 64s |
| VD-006 | Đường của bạn không cùng vạch với ai | 72s |

Mỗi video có: kịch bản (`content/scripts/`), lời đọc thuần văn bản (`content/scripts/loi-doc/`), caption + hashtag (`content/captions/`), ảnh quote 1:1 (`assets/templates/quotes/`), và **giọng đọc nháp** đã render sẵn ở `video/raw/VD-00X-giong-nhap.aiff` (ngoài GitHub).
Tất cả đều **trên 60 giây** → đủ tiêu chí quảng cáo trong luồng.

**Công cụ tự động (`scripts/`)**
- `tao-anh-quote.py` — tạo ảnh quote 1:1 đúng nhận diện, chỉ cần gõ câu chữ.
- `tao-giong-doc.sh` — tạo giọng đọc nháp tiếng Việt + đo thời lượng, cảnh báo nếu dưới 60s.
- `dang-video-fb.py` — đăng video/ảnh + caption lên Page qua Graph API (mặc định chạy thử, phải thêm `--dang-that`).

**Tài liệu**
- `docs/huong-dan-dung-video.md` — quy trình dựng trong CapCut, 3 lỗi làm tụt lượt xem.
- `docs/huong-dan-dang-tu-dong.md` — cách lấy Page ID + Access Token.
- `schedule/calendar.md` — lịch 2 video/tuần (Ba & Sáu 20:00) + bảng ghi số liệu.
- `content/ideas/kho-y-tuong.md` — 13 ý tưởng, 6 đã thành kịch bản.

## Đang chờ anh ⏳
1. **Dán mô tả mới** vào phần Giới thiệu của Page (nội dung sẵn ở `docs/mo-ta-page.md`) — nếu chưa làm.
2. **Dựng VD-001** theo `docs/huong-dan-dung-video.md` → đăng 28/07, 20:00.
3. **Nguồn nhạc nền dùng được thương mại** (thư viện nhạc trong Meta Business Suite là an toàn nhất).
4. **Page ID + Page Access Token** → điền vào `.env` để em bật đăng tự động (`docs/huong-dan-dang-tu-dong.md`).
5. **Ảnh chụp Meta Business Suite → Monetization** để em lên lộ trình theo con số thật (đang ~9.9K followers).

## Bước tiếp theo 👉
- Sau khi đăng VD-001–002: điền số liệu vào bảng cuối `schedule/calendar.md` → em phân tích dạng nào chạy tốt để nhân bản.
- Có token thì chạy `dang-video-fb.py` là đăng được từ máy, khỏi bấm tay.
- Em soạn tiếp VD-007+ từ kho ý tưởng khi anh cần.
- Chưa cài `ffmpeg` nên em chưa tự render video được — nếu anh muốn em dựng video nháp tự động (chữ + ảnh quote + giọng nháp) thì cài `brew install ffmpeg` rồi bảo em.

## Thông tin nền
- Page: **Sống Tốt** — https://www.facebook.com/songtot.in — **~9.9K followers**.
- Video: **1:1 (1080×1080)**, thời lượng **>60s**.
- Kế hoạch: `PLAN.md` · Kiếm tiền: `docs/ke-hoach-kiem-tien.md`
