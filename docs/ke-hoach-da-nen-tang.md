# Kế hoạch đăng ba nền tảng: Facebook · YouTube · Instagram

_Chốt 26/07/2026. Mục tiêu giai đoạn này: **đăng đều và tăng người xem**. Kiếm tiền tính sau._

## Ý chính

**Một video, đăng ba nơi.** Không làm lại nội dung cho từng nền tảng — cùng file
1080×1920 đó đăng cả Facebook Reels, YouTube Shorts và Instagram Reels. Chỉ khác
phần chữ đi kèm (tiêu đề, mô tả, hashtag).

Lý do làm vậy: nút thắt của kênh là **viết kịch bản**, không phải sản xuất. Render
một video mất ~3 phút. Nên nhân số nơi đăng lên là cách tăng người xem rẻ nhất.

## Vì sao một file dùng được cả ba

Cả ba nền tảng đều nhận 9:16, 1080×1920, h264 + AAC. Khác nhau ở chỗ **giao diện
che mất bao nhiêu phần khung**:

| | đáy che | phải che | đỉnh che | Dài tối đa |
|---|---|---|---|---|
| Facebook Reels | ~320px | ~120px | ~110px | 90 giây |
| Instagram Reels | ~400px | ~120px | ~110px | 90 giây (có nơi 3 phút) |
| YouTube Shorts | ~330px | ~140px | ~130px | **3 phút** |

`khung_reels.py` đã lấy **mức khắt khe nhất của cả ba** — đáy 470px, phải 140px,
đỉnh 130px. Chữ nằm trong y 980–1450, nên không nền tảng nào che mất.

> Video 63 giây của mình lọt cả ba. YouTube tự xếp mọi video dọc ≤3 phút vào Shorts,
> không phải làm gì thêm.

**Không có watermark của nền tảng nào trong video** — chỉ có logo Sống Tốt. Đây là
điểm quan trọng: cả ba nền tảng đều dìm video có watermark của đối thủ (logo TikTok,
chữ "Made with Instagram"…). Vì mình tự render nên không mắc lỗi này.

## Quy trình mỗi ngày

Sản xuất một lần, đăng ba lần:

```bash
# Sản xuất (khoảng 10 phút, chủ yếu là chọn ảnh)
.venv-tts/bin/python scripts/render-video-v2.py VD-00X --chi-do-dai
python3 scripts/tai-anh-pexels.py VD-00X --chon 6
open video/thu-anh/VD-00X-chon.png
python3 scripts/tai-anh-pexels.py VD-00X --lay <số đã chấm>
.venv-tts/bin/python scripts/render-video-v2.py VD-00X --nhac assets/music/nen-am-ap.m4a
python3 scripts/tao-anh-bia-reels.py VD-00X "Câu quote ngắn." --anh 2
```

Rồi đăng, giãn giờ ra để không dồn cục:

| Giờ | Nơi | Ghi chú |
|---|---|---|
| **12:00** | YouTube Shorts | Buổi trưa người ta lướt điện thoại |
| **20:00** | Facebook Reels | Giờ chính của kênh, giữ nguyên |
| **21:00** | Instagram Reels | Muộn hơn Facebook một tiếng |

Giãn giờ để mỗi nền tảng có một cửa sổ riêng, và để anh còn thời gian trả lời
bình luận từng nơi.

---

## Facebook Reels

Đã có hướng dẫn riêng: [huong-dan-dang-reels.md](huong-dan-dang-reels.md).

Dùng: file video + ảnh bìa + caption trong `content/captions/`.

---

## YouTube Shorts

### Lập kênh (làm một lần)

1. Vào https://youtube.com → đăng nhập bằng Gmail của anh
2. Bấm avatar → **Tạo kênh** → tên **Sống Tốt**
3. **Tùy chỉnh kênh**:
   - Ảnh đại diện: `assets/logo/icon-song-tot.png`
   - Ảnh banner: `assets/images/banner-song-tot.png`
   - Mô tả: lấy từ `docs/mo-ta-page.md`
   - Liên kết: thêm link Facebook Page
4. **Cài đặt → Kênh → Cài đặt nâng cao**: đặt quốc gia **Việt Nam**, ngôn ngữ **Tiếng Việt**

### Đăng mỗi video

1. Bấm **Tạo → Tải video lên**, chọn `VD-00X-reels.mp4`
2. **Tiêu đề** — quan trọng nhất trên YouTube, vì người ta tìm bằng chữ.
   Viết dạng câu hỏi hoặc lời hứa, **kèm `#Shorts` ở cuối**:
   ```
   Tử tế có bao giờ là lãng phí không? #Shorts
   ```
3. **Mô tả** — dán caption Facebook vào, thêm 2 dòng cuối:
   ```
   🌱 Kênh Sống Tốt — mỗi ngày một điều lành.
   Facebook: https://www.facebook.com/songtot.in

   Ảnh: Pexels.com
   ```
4. **Ảnh thu nhỏ**: Shorts không dùng thumbnail tự tải như video dài — YouTube lấy
   một khung trong video. Chọn khung có chữ rõ.
5. **Đối tượng**: chọn **"Không, video này không dành cho trẻ em"**
   (bắt buộc phải trả lời, chọn sai sẽ tắt bình luận)
6. **Hiển thị**: Công khai, hoặc **Lên lịch** 12:00
7. Bấm **Xuất bản**

### Khác Facebook ở chỗ nào

- **Tiêu đề quyết định nhiều hơn**. YouTube có tìm kiếm thật, video sống lâu hơn —
  một Short tốt vẫn kéo view sau nhiều tháng, khác Facebook chết sau 2–3 ngày.
- **Hashtag ít quan trọng**, trừ `#Shorts`. Đừng nhồi.
- **Được để link ngoài** trong mô tả — dùng để kéo người về Facebook Page.

---

## Instagram Reels

### Lập tài khoản (làm một lần)

1. Tạo tài khoản mới, tên `@songtot.in` (giống Facebook cho dễ nhớ)
2. **Đổi sang tài khoản chuyên nghiệp**: Cài đặt → Loại tài khoản → **Chuyển sang tài khoản chuyên nghiệp** → chọn **Người sáng tạo**
3. **Liên kết với Facebook Page Sống Tốt** — làm được thì đăng một lần lên cả hai
   qua Meta Business Suite, đỡ một lượt tải file
4. Ảnh đại diện + bio lấy từ `assets/logo/` và `docs/mo-ta-page.md`

### Đăng mỗi video

1. Bấm **+** → **Reel** → chọn `VD-00X-reels.mp4`
2. **Ảnh bìa**: chọn *Thêm từ thư viện* → `VD-00X-bia.png`
3. **Chú thích**: caption Facebook nhưng **cắt ngắn còn 3–4 dòng đầu**. Instagram
   chỉ hiện 2 dòng rồi mới có "…thêm", viết dài người ta không mở ra đọc.
4. **Hashtag**: Instagram ăn hashtag mạnh hơn Facebook nhiều. Dùng **8–15 thẻ**,
   trộn thẻ lớn và thẻ nhỏ:
   ```
   #songtot #tute #songtichcuc #loisong #chualanh #binhyen
   #tuduytichcuc #moingaymotdieutotlanh #reelsvietnam #vietnam
   ```
5. Đăng, hoặc lên lịch 21:00

### Khác Facebook ở chỗ nào

- **Không có link bấm được trong chú thích.** Chỉ ô "link trong bio" mới bấm được —
  để link Facebook Page ở đó.
- **Chú thích phải ngắn.** Nội dung dài để trong video, không để trong chữ.
- **Hashtag thật sự có tác dụng**, khác Facebook.
- Đừng dùng nhạc của Instagram — video đã có nhạc nền gốc rồi.

---

## Cần theo dõi con số gì

Ghi vào `schedule/calendar.md` sau 48 giờ, **tách riêng từng nền tảng**:

| Nền tảng | Số cần lấy | Lấy ở đâu |
|---|---|---|
| Facebook | Lượt xem · xem hết · tương tác · người theo dõi mới | Meta Business Suite → Thông tin chi tiết |
| YouTube | Lượt xem · thời lượng xem trung bình · người đăng ký mới | YouTube Studio → Số liệu phân tích |
| Instagram | Lượt xem · lượt xem lại · lưu · người theo dõi mới | Instagram → Thông tin chi tiết |

Sau **2 tuần** sẽ thấy nền tảng nào ăn nhất với nội dung này, rồi dồn sức vào đó.
Đừng quyết định trước khi có số — đoán thì vô nghĩa.

## Việc chưa làm, cần quyết sau

- **Bản ngắn ~30 giây để so với bản 60 giây.** Reels và Shorts đều phân phối theo
  tỉ lệ xem hết, mà video ngắn dễ xem hết hơn. Chưa kiểm chứng nên chưa đổi.
- **TikTok.** Cùng khung 9:16 nên đăng được luôn, nhưng để sau khi ba nền tảng
  này vào nếp đã.
- **Tăng lên 2 video/ngày.** Cần soạn thêm kịch bản trước.
