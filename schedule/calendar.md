# Lịch đăng bài

> Cập nhật mỗi khi lên kế hoạch hoặc đăng xong. Đánh dấu ✅ khi đã đăng.
>
> **Nhịp cố định: mỗi ngày 1 video lúc 19:30 giờ Việt Nam.** Khi đăng một lô, lấy
> 19:30 gần nhất còn trống làm bài đầu, rồi xếp mỗi bài tiếp theo vào 19:30 của ngày kế tiếp.
> Mỗi ngày một bài nên cần ~30 video/tháng — em soạn trước theo lô, luân phiên
> nhân vật/cảnh/nhạc cho khỏi trùng cảm giác.

## Tháng 7–8/2026

Mỗi bài đi lên **ba nơi**: **YouTube tiếng Việt** (`@songtotdaily`) · **YouTube tiếng Anh**
(`@onesmallthingdaily`) · **Facebook** (page Sống Tốt, dùng bản tiếng Việt).

| Ngày | Mã số | Tên video | YT tiếng Việt | YT tiếng Anh | Facebook |
|------|-------|-----------|:---:|:---:|:---:|
| 25/07 | VD-001 | Ba điều biết ơn mỗi sáng | ✅ | ✅ | ✅ |
| 26/07 | VD-002 | Tử tế không bao giờ là điều lãng phí | ✅ | ✅ | ✅ |
| 27/07 | VD-003 | Hôm nay chỉ cần làm được một việc | ✅ | ✅ | ✅ bù 02/08 21:45 |
| — | VD-004 | Câu cảm ơn có chữ vì | ✅ | ✅ | ✅ |
| — | VD-005 | Tin nhắn lâu không hỏi thăm | ✅ | ✅ | ✅ |
| — | VD-006 | So sánh với chính mình | ✅ | ✅ | ✅ |
| **31/07** | **VD-008** | **Thức khuya trả thù** | ✅ | ✅ | ✅ |
| **02/08** | **VD-007** | **Không ai tự nhiên tử tế cả** | ✅ | ✅ | ✅ |
| 03/08 | — | _lỡ nhịp, không đăng gì_ | — | — | — |
| **04/08** | **VD-009** | **Để mình nghĩ đã** | 🕒 | 🕒 | 🕒 19:30 |
| 05/08 | VD-011 | Một việc tốt không ai biết | 🕒 | 🕒 | 🕒 19:30 |
| 06/08 | VD-010 | Tha thứ không phải cho người kia | 🕒 | 🕒 | 🕒 19:30 |
| 07/08 | VD-012 | Người phục vụ mình cũng có tên | 🕒 | 🕒 | 🕒 19:30 |
| 08/08 | VD-013 | Mười phút đầu tiên | 🕒 | 🕒 | 🕒 19:30 |
| 08/08 | VD-013 | Mười phút đầu tiên | 🟢 sẵn sàng | 🟢 sẵn sàng | 🟢 sẵn sàng |

**Chú thích:** ⬜ Chưa render · 📝 Có lời đọc, chưa có caption/ảnh quote · 🟡 Đang làm · 🟢 Sẵn sàng / đang đăng · 🕒 Đã tải lên, hẹn giờ · ✅ Đã đăng · ❗ Bị bỏ sót · ❓ Chưa kiểm

## Nguyên tắc đăng (anh chốt 02/08)

- **Nhiều nhất 1 bài/ngày**
- **Đồng bộ cả ba nơi cùng ngày, cùng một bài** — đừng để nơi này đi trước nơi kia
- **Công khai lúc 19:30** giờ Việt Nam
- **Luôn đăng trước rồi đặt lịch**, không đăng đúng giờ, không để tự lên ngay
- Facebook phải dùng lệnh **`reels`**, không dùng `video`
- Khi có nhiều bài: bài đầu vào **19:30 gần nhất còn trống** (chỉ dùng tối nay nếu còn
  ít nhất 10 phút); các bài sau vào **19:30 từng ngày liên tiếp**, không tự đổi giờ
- Sau khi xếp xong phải đọc lại API, khớp **ngày + giờ + câu đầu caption**, và xóa ngay
  lịch trùng; không chỉ tin dòng báo thành công của script

Hết bài tồn: VD-009 → VD-012 đã lên lịch YouTube tới **07/08**. Sau đó **hết chữ** — VD-013
trở đi mới chỉ có hồ sơ ý tưởng, chưa viết. Muốn giữ nhịp mỗi ngày một bài thì phải bắt đầu
viết VD-013 trước 07/08.

⚠️ **Render lại bản tiếng Việt trước khi đăng nếu file cũ hơn commit sửa giọng gần nhất.**
File trong `video/exports/` không tự biết nó render bằng thiết lập giọng nào — so ngày sửa
file với `git log -1 --format=%ci -- scripts/giong_vieneu.py` là ra.

### Lệnh một ngày — thay VD-0XX rồi chạy ba dòng

```bash
.venv-dang/bin/python scripts/dang-video-youtube.py dang VD-0XX --kenh en \
    --hen-gio 2026-08-0DT19:30:00+07:00 --dang-that
.venv-dang/bin/python scripts/dang-video-youtube.py dang VD-0XX --kenh vi \
    --hen-gio 2026-08-0DT19:30:00+07:00 --dang-that
python3 scripts/dang-video-fb.py reels video/exports/VD-0XX-reels.mp4 --ma VD-0XX \
    --hen-gio 2026-08-0DT19:30:00+07:00 --dang-that
```

## Đợt đăng 04/08 — VD-009 → VD-013 lên cả ba nơi

Đọc lại từ API sau khi đăng: hai kênh YouTube đều có **13 video, khớp đủ VD-001 →
VD-013**, không trùng không thiếu, cả 5 bài chờ đều `uploadStatus = processed` và
`processingStatus = succeeded`. Facebook có đúng năm lịch dưới đây, mỗi ngày một bài,
không trùng giờ. Tất cả đều lưu mốc `12:30Z` (**19:30 giờ Việt Nam**) đúng ngày.

| Ngày 19:30 | Mã | YouTube tiếng Việt | YouTube tiếng Anh | Facebook post ID |
|---|---|---|---|---|
| 04/08 | VD-009 | https://youtu.be/rmgkx_XTnJo | https://youtu.be/leBaRFd4fXQ | `315460902683557_1660124185681318` |
| 05/08 | VD-011 | https://youtu.be/tY5SZz3F5kY | https://youtu.be/ZzcZEZD_TSE | `315460902683557_1660124532347950` |
| 06/08 | VD-010 | https://youtu.be/qUGygq8-qw4 | https://youtu.be/MJCbGstdSgQ | `315460902683557_1660124749014595` |
| 07/08 | VD-012 | https://youtu.be/wECczzrqARA | https://youtu.be/EO_qomjUYPE | `315460902683557_1660125055681231` |
| **08/08** | **VD-013** | https://youtu.be/VrHJoc6XGSg | https://youtu.be/DOYFZXQ_VC0 | Reels `787834854408440` |

⏳ **Bài vừa hẹn giờ trên Facebook mất khoảng một phút mới hiện trong `/scheduled_posts`.**
VD-013 đăng lúc 17:18 ngày 04/08, đọc ngay sau đó thì danh sách chỉ có 4 bài, tưởng hụt.
Tra thẳng `/{video-id}` thì đã thấy `publish_status = scheduled` đúng mốc. **Chưa thấy trong
danh sách thì tra mã bài trước, đừng vội đăng lại** — đăng lại là ra hai lịch trùng.

⚠️ **Tên mục trong file caption phải viết bằng tiếng Việt, kể cả file `-en.md`.** Script
tìm đúng ba chuỗi `Tiêu đề` · `Mô tả` · `Thẻ`. VD-013 bản tiếng Anh ban đầu đặt tên mục là
`Title` · `Description` · `Tags` nên `dang-video-youtube.py` báo *thiếu mục* dù chữ có đủ.
Đã sửa về khuôn chung. Bài sau cứ chép khuôn của `VD-012-caption-en.md` cho chắc.

⚠️ **Bốn bản tiếng Việt đã render lại ngày 04/08 trước khi đăng.** Bản cũ render 31/07,
tức trước commit 5b4fac8 (chậm giọng 9%, 02/08) — đăng nguyên si là lặp lại đúng lỗi anh
đã góp ý. Đo lại thẻ đầu VD-009: 1,680s → 1,817s (đã trừ phần đệm 0,55s) = **chậm 8,1%**,
khớp `atempo` 1,09. Bản tiếng Anh giữ nguyên file cũ vì Piper đã chậm sẵn 12%.

📌 **Thời lượng video tổng chỉ dài thêm ~4%, không phải 9%** — vì phần đệm 0,55s giữa các
thẻ và đuôi giữ kết nằm ngoài `atempo`. Đừng lấy thời lượng video ra kiểm việc chậm giọng;
phải đo file thẻ trong `video/edit/{ma}-reels/` — so `NN-tho.wav` với `NN.wav`.

✅ **Facebook đã có Page Token dài hạn và đã kiểm tra lại ngày 04/08.** VD-003 và VD-007
đều đã công khai đúng lịch. Mã Reels: VD-003 `2227069261412713` · VD-007
`4731819720383240`.

### VD-007 — tải lên 02/08 lúc 17:4x, hẹn 19:30

| Nơi | Mã bài | Chế độ |
|---|---|---|
| YouTube tiếng Anh | https://youtu.be/QaDH7_4ZaFA | ✅ **đã tự công khai 19:30** |
| YouTube tiếng Việt | https://youtu.be/Wfsv45pH9z0 | ✅ **đã tự công khai 19:30** |
| Facebook (**Reels**) | `4731819720383240` | ✅ **đã tự công khai 19:30** |

Cả ba nơi **đều nhận lịch**: YouTube lưu `publishAt = 12:30Z`, Facebook lưu
`scheduled_publish_time = 2026-08-02T12:30:00+0000` — đều là 19:30 giờ Việt Nam.

✅ **YouTube CÓ tự công khai đúng giờ hẹn dù project chưa qua vòng audit của Google.**
Đọc lại API ngày 04/08: cả hai bài VD-007 đều `public`, `publishedAt = 2026-08-02T12:30Z`
— đúng 19:30 giờ VN, không ai bấm tay. Nỗi lo cũ ("nhận lịch chưa chắc đã tự công khai")
là thừa, đã bỏ. Cứ đặt lịch rồi để đó.

**Facebook đăng bằng luồng Reels** (`/video_reels`, ba bước), không phải `/videos`. Đăng
qua `/videos` ra bài video thường, video dọc 9:16 không vào được tab Reels — mất chỗ được
đẩy mạnh nhất.

❗ **Hai chỗ bỏ sót — phát hiện 02/08 khi nối API vào cả ba nơi.** Trước đó sổ ghi
"đã đăng tới VD-008, ba nơi đồng bộ", thực tế không phải:

| Nơi | Thực tế trên đó | Thiếu |
|---|---|---|
| YouTube tiếng Anh | 7 video: VD-001→006, VD-008 | **VD-007** |
| YouTube tiếng Việt | 7 video: VD-001→006, VD-008 | **VD-007** |
| Facebook | 7 video nhưng chỉ 6 bài — VD-002 đăng 2 lần (đã xoá bản 26/07 ngày 02/08) | **VD-003 · VD-007** |

Cách kiểm: đọc danh sách video qua API rồi khớp từng bài với caption trong
`content/captions/`. Bài 27/07 trên Facebook mở đầu *"Sáng nay mở mắt ra…"* là **VD-001**
bản caption viết lại, không phải VD-003 — dễ nhìn nhầm nên đã khớp bằng máy.

**Đây là số tồn tại thời điểm 02/08:** 5 bài + 1 lượt bù Facebook. Đến 04/08 đã bù
xong VD-003/VD-007 và xếp lịch đủ VD-009 → VD-012 trên cả ba nơi.

⚠️ **Thứ tự năm bài của đợt này được đảo có chủ ý: VD-007 → VD-009 → VD-011 → VD-010 → VD-012.**
VD-010 không được đứng liền sau VD-009, mà VD-007 · VD-011 · VD-012 đều trụ 2 nên cũng
không được dính nhau.

⚠️ **VD-011 sẽ ít bình luận hẳn, đó là chủ ý** — CTA của nó là *cấm kể*. Đo bài này bằng
lượt lưu và tỉ lệ xem hết, đừng đo bằng bình luận, và đừng tự bình luận mở hàng.

⚠️ **VD-008 nên đăng buổi tối 21–22h** · **VD-009 có CTA độ trễ** nên phải mở lại bài sau
3–4 ngày để trả lời người xem.

> Từ 26/07 bỏ cột "Nhân vật" — không còn vẽ nhân vật nữa, nền là ảnh chụp thật
> lấy theo từ khoá B-roll ghi trong từng kịch bản. Xem `STATUS.md`.

_Render khi anh yêu cầu (anh đã chốt như vậy ngày 25/07), không tự render trước._

## Ghi nhận hiệu quả (điền sau khi đăng 24–48h)

⚠️ **Tám bài đã đăng, chưa bài nào có số.** Đây là chỗ nghẽn thật của dự án — không có số
thì không biết nên đi hướng nào, làm thêm video chỉ làm kho dày thêm. **Ghi tách riêng
từng nơi**, vì ba nơi có tệp người xem khác hẳn nhau.

**Số quan trọng nhất là tỉ lệ xem hết** — YouTube chấm bằng cái này.

### YouTube tiếng Việt (`@songtotdaily`)

| Mã số | Lượt xem | Tỉ lệ xem hết | Đăng ký mới | Lưu / chia sẻ | Ghi chú |
|-------|----------|---------------|-------------|---------------|---------|
| VD-001 |  |  |  |  |  |
| VD-002 |  |  |  |  |  |
| VD-003 |  |  |  |  |  |
| VD-004 |  |  |  |  |  |
| VD-005 |  |  |  |  |  |
| VD-006 |  |  |  |  |  |
| VD-007 |  |  |  |  |  |
| VD-008 |  |  |  |  |  |

### YouTube tiếng Anh (`@onesmallthingdaily`)

| Mã số | Lượt xem | Tỉ lệ xem hết | Đăng ký mới | Lưu / chia sẻ | Ghi chú |
|-------|----------|---------------|-------------|---------------|---------|
| VD-001 |  |  |  |  |  |
| VD-002 |  |  |  |  |  |
| VD-003 |  |  |  |  |  |
| VD-004 |  |  |  |  |  |
| VD-005 |  |  |  |  |  |
| VD-006 |  |  |  |  |  |
| VD-007 |  |  |  |  |  |
| VD-008 |  |  |  |  |  |

### Facebook (page Sống Tốt)

| Mã số | Lượt xem | Xem hết ≥1 phút | Tương tác | Chia sẻ | Ghi chú |
|-------|----------|-----------------|-----------|---------|---------|
| VD-001 |  |  |  |  |  |
| VD-002 |  |  |  |  |  |
| VD-003 |  |  |  |  |  |
| VD-004 |  |  |  |  |  |
| VD-005 |  |  |  |  |  |
| VD-006 |  |  |  |  |  |
| VD-007 |  |  |  |  |  |
| VD-008 |  |  |  |  |  |
