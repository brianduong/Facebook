# Hướng dẫn dựng video — khung 1:1

> Mục tiêu: mỗi video ~60–75 giây, vuông 1080×1080, đúng tông xanh của kênh. Video **dài trên 1 phút** mới đủ tiêu chí quảng cáo trong luồng (xem `docs/ke-hoach-kiem-tien.md`).

## Cách nhanh nhất: render bản nháp bằng script

```bash
python3 scripts/render-video-nhap.py VD-001 --nhan-vat chi --canh sang-cua-so,ban-tra,duong-cay
```

Script tự làm hết: cắt lời đọc thành từng thẻ chữ, đọc bằng giọng máy tiếng Việt, khớp thời gian chữ với tiếng, ghép ảnh quote ở cuối, xuất `video/exports/VD-001-nhap.mp4` (1080×1080, 30fps).

**Nhân vật kể** (`--nhan-vat`) — vẽ vector nên không lo bản quyền hình người thật. Xem bảng mặt ở `assets/images/nhan-vat-mau.png`:

| Mã | Nhân vật |
|----|----------|
| `anh` | đàn ông trẻ |
| `chi` | phụ nữ trẻ (mặc định) |
| `chu` | đàn ông lớn tuổi |
| `co` | phụ nữ lớn tuổi |
| `khong` | không có người trong hình |

Miệng nhân vật mở/đóng theo nhịp → trông như đang nói, không phải hình tĩnh.

**Cảnh nền** (`--canh`, cách nhau bởi dấu phẩy — video sẽ đổi cảnh theo từng khúc):
`sang-cua-so` (nắng qua cửa sổ) · `ban-tra` (ly nước ấm) · `duong-cay` (đường đi bộ) · `ben-mua` (trạm chờ mưa) · `bep` (bồn rửa bát) · `dem-sao` (trời đêm) · `trong` (nền gradient trơn).

Xem thử nhân vật và cảnh trước khi render cả video: `python3 scripts/xem-thu.py`

**Giọng đọc & ngữ điệu**

Script tự gắn ngữ điệu cho giọng máy trước khi đọc (chi tiết trong `scripts/giong_doc.py`):
- **Câu hỏi** → nhấc cao độ lên, ngữ điệu rộng hơn, đọc chậm lại một nhịp.
- **Câu chốt cuối video** → hạ giọng trầm, chậm hẳn, nghe như đang đúc kết.
- **Câu ngắn / liệt kê** → đi nhanh hơn, nghỉ ngắn.
- **Câu kể thường** → cao độ nhích lên xuống theo thứ tự câu cho khỏi đều đều như đọc máy.
- Ngắt nghỉ ở dấu phẩy (0,13s), cuối câu (0,3s), sau câu hook (0,52s).
- Sau đó tiếng còn được hậu kỳ: lọc ù trầm, thêm ấm ở 220Hz, rõ chữ ở 3.2kHz, nén động cho đều, chút vang phòng, chuẩn hoá độ to về −16 LUFS (mức chuẩn cho mạng xã hội).

So sánh trước/sau: `python3 scripts/so-sanh-giong.py VD-001` → hai file trong `video/raw/`.
Muốn nghe lại kiểu đọc đều cũ: thêm `--giong-phang`.

`--giong <tên>` để đổi giọng khác của macOS (`say -v '?'` xem danh sách). Nếu anh tải thêm giọng tiếng Việt chất lượng cao trong **Cài đặt hệ thống → Trợ năng → Nội dung đọc → Giọng hệ thống → Tiếng Việt**, chỉ cần truyền tên giọng đó vào là dùng được, không phải sửa code.

**Các lựa chọn khác**
- `--toc-do 155` — tốc độ đọc, mặc định 155 từ/phút (nghe như nói chuyện). Hạ xuống 138 nếu muốn chậm rãi hơn.
- `--nhac assets/music/ten-file.mp3` — trộn nhạc nền (chỉ dùng nhạc được phép thương mại).
- Câu hook luôn đứng riêng một thẻ (3 giây đầu), có zoom vào rất chậm + mờ dần đầu/cuối.
- ⚠️ Đọc nhanh làm video ngắn lại. Script in ra tổng thời lượng và **cảnh báo nếu dưới 60 giây** — dưới mốc đó là mất tiêu chí quảng cáo trong luồng.

**Bản nháp dùng được để đăng ngay**, nhưng nên nâng cấp dần:
1. Thu lại **giọng thật của anh** thay giọng máy → thu vào `content/scripts/loi-doc/` đọc theo, rồi ghép trong CapCut.
2. Thay nền gradient bằng **b-roll thật** theo mục "Hình ảnh/B-roll" trong kịch bản.

Giọng thật + b-roll thật luôn hiệu quả hơn bản nháp — bản nháp là để kênh không bị trống bài trong lúc anh chuẩn bị.

## Cách kỹ hơn: dựng tay trong CapCut / Canva

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
