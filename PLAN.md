# PLAN — Kênh Facebook lan toả thông điệp tốt

> File này ghi lại **những gì em đã hiểu** về dự án. Anh cứ sửa/bổ sung trực tiếp vào đây, sau này em đọc lại và làm tiếp theo đúng ý anh.

## 1. Mục tiêu (em hiểu)

- **Page có sẵn:** Sống Tốt — https://www.facebook.com/songtot.in
- Đăng **video** mang **thông điệp tích cực, tốt đẹp cho cuộc sống**.
- **Thiết kế lại nhận diện Page:** ảnh đại diện (icon), ảnh bìa (banner), thông điệp, mô tả, phần "Giới thiệu"...
- **Kiếm tiền từ Page** (monetization).
- Repo GitHub này là nơi quản lý toàn bộ phần "chất xám" của kênh: ý tưởng, kịch bản, caption, lịch đăng, tài sản thiết kế.
- **File video không lưu GitHub** (nặng) → chỉ lưu ở máy anh; mọi thứ còn lại thì đưa lên GitHub.

## 1b. Về quyền admin Page

Anh có đề nghị cấp quyền admin. Em (Claude) **không thể tự đăng nhập hay thao tác trực tiếp trên Facebook** — nên anh **chưa cần** cấp quyền cho em. Việc thay icon/banner, sửa mô tả, bật kiếm tiền... **anh sẽ tự bấm trên Facebook**, còn em lo phần:
- Thiết kế file ảnh (icon, banner) để anh tải lên.
- Viết sẵn toàn bộ chữ (mô tả, giới thiệu, thông điệp, câu chốt).
- Hướng dẫn từng bước cần bấm ở đâu.
- Lập chiến lược kiếm tiền và điều kiện cần đạt.

## 2. Phạm vi hiện tại

- [x] Dựng cấu trúc thư mục
- [x] Tạo `.gitignore` (loại trừ `video/` và file media nặng)
- [x] Tạo README, các mẫu (kịch bản, caption, lịch đăng)
- [x] Khởi tạo Git và đẩy lên `https://github.com/brianduong/Facebook.git`

## 3. Những điểm cần anh xác nhận / bổ sung sau

Em để trống những chỗ chưa rõ, anh điền giúp:

- **Tên Page / thương hiệu kênh**: _(chưa có)_
- **Đối tượng khán giả**: _(vd: người trẻ 18–35, dân văn phòng...)_
- **Chủ đề chính**: _(vd: động lực sống, tử tế, sức khoẻ tinh thần, câu chuyện đời thường...)_
- **Định dạng video**: _(Reels dọc 9:16? Video ngang? Thời lượng bao lâu?)_
- **Tần suất đăng**: _(vd: 3 video/tuần)_
- **Phong cách**: giọng đọc / chữ chạy / nhạc nền / màu sắc chủ đạo?
- **Công cụ dựng video**: _(CapCut? Premiere? Canva?)_
- **Ngôn ngữ**: tiếng Việt? có phụ đề không?

## 3b. Thiết kế lại Page & Kiếm tiền (việc anh vừa thêm)

**A. Nhận diện & thiết kế** — tài liệu và file để trong `docs/` và `assets/`:
- [ ] Chốt tên hiển thị, slogan, màu chủ đạo, font → `docs/dinh-huong-kenh.md`
- [ ] Thiết kế **ảnh đại diện / icon** (khuyến nghị 500×500px, dạng tròn) → `assets/logo/`
- [ ] Thiết kế **ảnh bìa / banner** (khuyến nghị 1640×856px cho Page) → `assets/images/`
- [ ] Viết **mô tả ngắn + phần Giới thiệu (About)** → `docs/mo-ta-page.md`
- [ ] Bộ **thông điệp/khẩu hiệu** dùng lại trong video & bài đăng

**B. Kiếm tiền từ Page** — chi tiết trong `docs/ke-hoach-kiem-tien.md`:
- [ ] Rà điều kiện bật kiếm tiền của Facebook (số follower, giờ xem, tuân thủ chính sách)
- [ ] Chọn hình thức: quảng cáo trong video (in-stream ads), Stars, nội dung có thương hiệu (branded content), affiliate, bán sản phẩm/khoá học...
- [ ] Lộ trình đạt điều kiện + lịch nội dung đều đặn

## 4. Ý tưởng mở rộng (khi cần)

- Tự động hoá đăng bài qua **Facebook Graph API** (script trong `scripts/`).
- Thư viện "hook" mở đầu và "call-to-action" kết bài để tái sử dụng.
- Thống kê hiệu quả từng video (lưu trong `schedule/` hoặc bảng riêng).

## 5. Ghi chú

- Repo để **public hay private**? → hiện đang đẩy theo mặc định, anh đổi trong Settings của GitHub nếu muốn private.
- Nhạc/nền/font trong `assets/` cần lưu ý **bản quyền** trước khi dùng thương mại.
