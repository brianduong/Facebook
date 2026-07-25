# Hướng dẫn dựng video (CapCut / Canva) — khung 1:1

> Mục tiêu: mỗi video ~60–75 giây, vuông 1080×1080, đúng tông xanh của kênh. Video **dài trên 1 phút** mới đủ tiêu chí quảng cáo trong luồng (xem `docs/ke-hoach-kiem-tien.md`).

## Chuẩn bị trước khi mở app
- Kịch bản: `content/scripts/VD-00X-*.md` (có sẵn hook, nội dung, CTA, mốc thời gian).
- Ảnh quote làm khung/thumbnail: `assets/templates/quotes/VD-00X-quote.png`.
- Khung mẫu chung: `assets/templates/khung-video-1x1.png`.
- Nhạc nền: **chỉ dùng nguồn cho phép dùng thương mại** (thư viện nhạc của Meta, hoặc nhạc mua bản quyền). Nhạc lấy từ TikTok/YouTube của người khác có thể làm Page **mất quyền kiếm tiền**.

## Các bước trong CapCut
1. **Tạo project** → tỉ lệ khung hình **1:1**.
2. **Ghi giọng đọc trước** (đọc theo kịch bản, chậm và ấm). Dựng hình theo giọng, không ngược lại.
3. **Rải B-roll** theo mục "Hình ảnh/B-roll" trong kịch bản. Mỗi cảnh 3–5 giây, chuyển cảnh mờ nhẹ — tránh hiệu ứng giật.
4. **Thêm phụ đề** (auto caption rồi sửa tay). Đặt phụ đề trong **dải tối phía dưới**, không quá 6 chữ/dòng.
   - Font: Be Vietnam Pro / Montserrat · Màu chữ `#F7FAF5` · Chữ đậm.
5. **Logo + tên kênh** góc trên bên trái, giữ suốt video (lấy từ `assets/logo/icon-song-tot.png`).
6. **3 giây đầu:** câu hook phải hiện **bằng chữ to** — rất nhiều người xem tắt tiếng.
7. **Kết video:** 2–3 giây ảnh quote `VD-00X-quote.png` + dòng "theo dõi để sống tốt mỗi ngày".
8. **Xuất:** 1080×1080, 30fps, chất lượng cao. Lưu vào `video/` trên máy (thư mục này **không** đẩy lên GitHub).

## Khi đăng lên Page
- Dán caption từ `content/captions/VD-00X-caption.md` — **giữ nguyên dòng đầu** (đó là câu hook, Facebook chỉ hiện vài dòng đầu).
- Chọn thumbnail = ảnh quote.
- Đặt tiêu đề video ngắn, có từ khoá cảm xúc.
- Sau 24–48h: ghi số liệu vào bảng cuối `schedule/calendar.md` để biết dạng nào chạy tốt.

## Ba lỗi làm tụt lượt xem
1. Mở đầu vòng vo ("xin chào các bạn, hôm nay mình sẽ...") → cắt bỏ, vào thẳng hook.
2. Không có phụ đề.
3. Nhạc to hơn giọng đọc.
