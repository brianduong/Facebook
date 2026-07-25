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

Mỗi video có: kịch bản (`content/scripts/`), lời đọc thuần văn bản (`content/scripts/loi-doc/`), caption + hashtag (`content/captions/`), ảnh quote 1:1 (`assets/templates/quotes/`).
Tất cả đều **trên 60 giây** → đủ tiêu chí quảng cáo trong luồng.

**✅ 6 file MP4 nháp đã render xong** — `video/exports/VD-00X-nhap.mp4` (1080×1080, 30fps, ngoài GitHub).
Chữ chạy khớp giọng đọc, hook đứng riêng 3 giây đầu, zoom chậm, ảnh quote ở cuối. **Đăng được ngay.**
Giọng hiện tại là giọng máy (Linh của macOS) → nên thu lại bằng giọng thật của anh khi có thời gian.

**Công cụ tự động (`scripts/`)**
- `render-video-nhap.py` — render cả video 1:1 từ lời đọc: cắt thẻ chữ, đọc, khớp thời gian, ghép quote cuối.
- `nhan_dien.py` — nơi duy nhất định nghĩa màu/font/logo; đổi ở đây là ảnh và video đổi theo.
- `tao-anh-quote.py` — tạo ảnh quote 1:1, chỉ cần gõ câu chữ.
- `tao-giong-doc.sh` — chỉ tạo giọng nháp + đo thời lượng, cảnh báo nếu dưới 60s.
- `dang-video-fb.py` — đăng video/ảnh + caption lên Page qua Graph API (mặc định chạy thử, phải thêm `--dang-that`).

**Tài liệu**
- `docs/huong-dan-dung-video.md` — quy trình dựng trong CapCut, 3 lỗi làm tụt lượt xem.
- `docs/huong-dan-dang-tu-dong.md` — cách lấy Page ID + Access Token.
- `schedule/calendar.md` — lịch 2 video/tuần (Ba & Sáu 20:00) + bảng ghi số liệu.
- `content/ideas/kho-y-tuong.md` — 13 ý tưởng, 6 đã thành kịch bản.

## Chốt ngày 25/07
- **Nhịp đăng: mỗi ngày 1 video, 20:00** (đổi từ 2 video/tuần).
- **Không tự render trước** — chỉ render khi anh yêu cầu.
- VD-001 đã kiểm tra kỹ và **đăng ngày 25/07**: 1080×1080, 30fps, h264 + AAC, 70,4s,
  độ to trung bình −15,8 dB, đỉnh −0,8 dB (không vỡ tiếng), không có đoạn lặng chết.
- Có nhân vật kể (chị), 3 cảnh nền, giọng có ngữ điệu, nhạc nền gốc `nen-am-ap`.
- Đã có lời đọc cho VD-007 → VD-012 (chưa có caption/ảnh quote/video).
- Page ID: `315460902683557` đã ghi trong `.env`; còn thiếu token.

## Đang chờ anh ⏳
1. **Xem 6 file `video/exports/VD-00X-nhap.mp4`** → duyệt hoặc nói em sửa (chữ, nhịp, tone nền).
2. **Dán mô tả mới** vào phần Giới thiệu của Page (nội dung sẵn ở `docs/mo-ta-page.md`) — nếu chưa làm.
3. **Nguồn nhạc nền dùng được thương mại** → đưa file vào `assets/music/`, em render lại kèm nhạc (`--nhac`).
4. **Page ID + Page Access Token** → điền vào `.env` để em bật đăng tự động (`docs/huong-dan-dang-tu-dong.md`).
5. **Ảnh chụp Meta Business Suite → Monetization** để em lên lộ trình theo con số thật (đang ~9.9K followers).

## Bước tiếp theo 👉
- Anh duyệt video nháp → đăng VD-001 ngày 28/07, 20:00 (bấm tay, hoặc có token thì chạy `dang-video-fb.py`).
- Sau khi đăng VD-001–002: điền số liệu vào bảng cuối `schedule/calendar.md` → em phân tích dạng nào chạy tốt để nhân bản.
- Nâng cấp dần: thu **giọng thật** thay giọng máy, rồi thay nền gradient bằng **b-roll thật**.
- Em soạn tiếp VD-007+ từ kho ý tưởng khi anh cần.

## Thông tin nền
- Page: **Sống Tốt** — https://www.facebook.com/songtot.in — **~9.9K followers**.
- Video: **1:1 (1080×1080)**, thời lượng **>60s**.
- Kế hoạch: `PLAN.md` · Kiếm tiền: `docs/ke-hoach-kiem-tien.md`
