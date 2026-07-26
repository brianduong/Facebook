# Quy trình hai tuyến: Short và video dài

_Chốt 27/07/2026, sau khi chốt mục tiêu kiếm tiền từ YouTube._

Áp dụng cho **cả hai kênh** — Sống Tốt (tiếng Việt) và One Small Thing (tiếng Anh).

## Vì sao phải có hai tuyến

Để bật kiếm tiền trên YouTube cần **1.000 người đăng ký**, cộng **một trong hai**:

- **4.000 giờ xem** trong 12 tháng — *chỉ tính video dài*
- **10 triệu lượt xem Shorts** trong 90 ngày

Chỗ quyết định: **giờ xem Shorts không được tính vào 4.000 giờ.** Hai đường tách hẳn nhau.

Quy ra việc phải làm:

| Đường | Cần bao nhiêu |
|---|---|
| Video dài 10 phút, xem hết 40% → 4 phút/lượt | **~60.000 lượt xem** |
| Shorts | **10.000.000 lượt xem** |

Chênh **hơn 160 lần**. Nên video dài là đường chính, Shorts là đường phụ.

Thêm một mốc: **trên 8 phút mới được chèn quảng cáo giữa bài**. Dưới 8 phút chỉ có một
chỗ quảng cáo. Nên đích là **10–12 phút**, không phải vừa đủ 8 — chừa biên cho phần
dựng có thể co lại.

> ⚠️ Con số của YouTube đổi theo thời gian và theo nước. Kiểm lại trong
> **YouTube Studio → Kiếm tiền** trước khi bám sát.

Nhưng Shorts vẫn phải làm, vì **1.000 người đăng ký** là điều kiện chung của cả hai
đường, mà Shorts kéo người đăng ký nhanh hơn video dài rất nhiều — YouTube đẩy Shorts
vào dòng lướt của người chưa biết mình, còn video dài phải chờ người ta tìm.

**Tóm lại: Shorts lo người đăng ký. Video dài lo giờ xem.**

## Cách hai tuyến nối vào nhau

Đây là chỗ tiết kiệm nhất của cả quy trình:

> **Short là nguyên liệu thô của video dài. Cứ 6 bài Short gộp thành một video dài.**

Không viết bài dài từ giấy trắng. Mỗi Short là một ý **đã được thử nghiệm thật** — sau
48 giờ mình có số: bài nào lưu nhiều, xem hết nhiều thì biết ý đó ăn. Chọn 6 bài cùng
một chủ đề, viết phần mở, phần chuyển đoạn và phần kết, thế là thành bài 10 phút.

Được ba thứ cùng lúc: bài dài không phải nghĩ lại từ đầu, nội dung đã có bằng chứng là
người ta thích, và mỗi ngày vẫn có Short ra đều để nuôi lượng đăng ký.

Ví dụ một video dài gom được từ các bài đã có:

| Video dài | Gom từ |
|---|---|
| *Những ngày không đủ sức* | VD-003 (một việc) · VD-006 (so sánh với chính mình) · +4 bài nữa cùng mạch |
| *Tử tế mà không ai thấy* | VD-002 (che mưa) · VD-004 (cảm ơn có lý do) · VD-005 (tin nhắn lâu không hỏi thăm) · +3 |

## Tuyến 1 — Short (9:16)

Đang chạy được rồi, không phải dựng gì thêm.

| | |
|---|---|
| Khung hình | 1080×1920 |
| Độ dài | **trên 60 giây**, dưới 3 phút |
| Nhịp | mỗi ngày |
| Đăng ở đâu | Facebook · Instagram · TikTok · YouTube (cả hai kênh) |
| Việc của nó | kéo người đăng ký, thử ý xem ý nào ăn |

Quy trình sản xuất: xem `docs/ke-hoach-da-nen-tang.md`.

## Tuyến 2 — Video dài (16:9)

**Chưa dựng được.** Phần này là việc phải làm, ghi ra đây để khỏi quên chỗ nào.

| | |
|---|---|
| Khung hình | 1920×1080 |
| Độ dài | **10–12 phút** (trên 8 phút mới có quảng cáo giữa bài) |
| Số chữ | **1.700–2.000 từ** — gấp bảy lần một bài Short |
| Nhịp | 1 bài/tuần mỗi kênh (đề xuất, chưa chốt) |
| Đăng ở đâu | chỉ YouTube |
| Việc của nó | **giờ xem → kiếm tiền** |

### Còn phải dựng những gì

1. **Khung hình 16:9.** `khung_reels.py` đang cứng ở 1080×1920. Cần bản 1920×1080 với
   cách đặt chữ khác hẳn — video dài xem trên máy tính và TV, không có giao diện app
   che mất góc nào, nên chữ được đặt rộng hơn và **không cần phụ đề kín màn hình**
   như Shorts.
2. **Ảnh nền.** 10 phút cần **25–40 ảnh**, không phải 7. Phải sửa `tai-anh-pexels.py`
   lấy ảnh ngang (`orientation=landscape`) và lấy nhiều từ khoá hơn.
3. **Cách viết bài 2.000 từ.** Đây là phần khó nhất, không phải phần kỹ thuật. Cần một
   mẫu riêng: mở bài giữ chân trong 30 giây đầu, 5–6 đoạn có mốc chương, chuyển đoạn
   không hụt hơi, kết bài gọi hành động. Sẽ có `_TEMPLATE-video-dai.md`.
4. **Mốc chương (chapters).** Video dài phải có timestamp trong phần mô tả — YouTube
   dùng nó để hiện thanh chương, và người xem nhảy đoạn thì vẫn tính giờ xem.

### Cái bẫy lớn nhất

**YouTube chấm bằng tỉ lệ xem hết, không phải độ dài.** Video 10 phút bị bỏ ở phút thứ
hai tệ hơn hẳn video 76 giây xem trọn — nó kéo tụt cả kênh xuống. Nên **tuyệt đối không
kéo dãn** một bài Short cho đủ 10 phút. Không đủ nội dung thật thì làm 6 phút, chấp nhận
mất quảng cáo giữa bài, còn hơn nhồi cho đủ 8.

## Kênh nào làm video dài trước

Hai chiều đều có lý:

- **Sống Tốt (tiếng Việt) trước** — có sẵn 9,9K người trên Facebook để kéo sang, và anh
  tự thẩm định được chất lượng chữ. Rủi ro thấp nhất.
- **One Small Thing (tiếng Anh) trước** — đơn giá quảng cáo cho người xem Âu Mỹ cao hơn
  người xem Việt Nam **khoảng mười lần**. Cùng một giờ xem, tiền chênh rất xa.

**Em đề nghị làm tiếng Việt trước** — không phải vì nó đáng tiền hơn, mà vì nó **rẻ hơn
để học**. Bài dài đầu tiên chắc chắn hỏng vài chỗ; hỏng ở nơi anh đọc ra được thì sửa
được. Khi định dạng đã vững thì bê sang tiếng Anh, và lúc đó mới ăn phần đơn giá cao.

## Nhịp đề xuất

| | Sống Tốt | One Small Thing |
|---|---|---|
| Short | mỗi ngày | 3 bài/tuần lúc đầu |
| Video dài | 1 bài/tuần *(mở trước)* | 1 bài/tuần *(mở sau, khi định dạng đã vững)* |

Đừng mở cả bốn thứ cùng lúc. Thứ tự em đề nghị: **Short tiếng Việt (đang chạy) → Short
tiếng Anh → video dài tiếng Việt → video dài tiếng Anh**, mỗi bước cách nhau 2–3 tuần và
chỉ bước tiếp khi bước trước đã thành nếp.
