# Lịch đăng bài

> Cập nhật mỗi khi lên kế hoạch hoặc đăng xong. Đánh dấu ✅ khi đã đăng.
>
> **Nhịp: mỗi ngày 1 video, 20:00** (anh chốt ngày 25/07). Mỗi ngày một bài nên cần ~30 video/tháng — em soạn trước theo lô, luân phiên nhân vật/cảnh/nhạc cho khỏi trùng cảm giác.

## Tháng 7–8/2026

Mỗi bài đi lên **ba nơi**: **YouTube tiếng Việt** (`@songtotdaily`) · **YouTube tiếng Anh**
(`@onesmallthingdaily`) · **Facebook** (page Sống Tốt, dùng bản tiếng Việt).

| Ngày | Mã số | Tên video | YT tiếng Việt | YT tiếng Anh | Facebook |
|------|-------|-----------|:---:|:---:|:---:|
| 25/07 | VD-001 | Ba điều biết ơn mỗi sáng | ✅ | ✅ | ✅ |
| 26/07 | VD-002 | Tử tế không bao giờ là điều lãng phí | ✅ | ✅ | ✅ |
| 27/07 | VD-003 | Hôm nay chỉ cần làm được một việc | ✅ | ✅ | 🕒 bù 02/08 21:45 |
| — | VD-004 | Câu cảm ơn có chữ vì | ✅ | ✅ | ✅ |
| — | VD-005 | Tin nhắn lâu không hỏi thăm | ✅ | ✅ | ✅ |
| — | VD-006 | So sánh với chính mình | ✅ | ✅ | ✅ |
| **31/07** | **VD-008** | **Thức khuya trả thù** | ✅ | ✅ | ✅ |
| **02/08** | **VD-007** | **Không ai tự nhiên tử tế cả** | 🕒 | 🕒 | 🕒 |
| 03/08 | VD-009 | Để mình nghĩ đã | 🟢 | 🟢 | 🟢 |
| sau đó | VD-011 | Một việc tốt không ai biết | 🟢 | 🟢 | 🟢 |
| sau đó | VD-010 | Tha thứ không phải cho người kia | 🟢 | 🟢 | 🟢 |
| sau đó | VD-012 | Người phục vụ mình cũng có tên | 🟢 | 🟢 | 🟢 |

**Chú thích:** ⬜ Chưa render · 📝 Có lời đọc, chưa có caption/ảnh quote · 🟡 Đang làm · 🟢 Sẵn sàng / đang đăng · 🕒 Đã tải lên, hẹn giờ · ✅ Đã đăng · ❗ Bị bỏ sót · ❓ Chưa kiểm

## Nguyên tắc đăng (anh chốt 02/08)

- **Nhiều nhất 1 bài/ngày**
- **Đồng bộ cả ba nơi cùng ngày, cùng một bài** — đừng để nơi này đi trước nơi kia
- **Công khai lúc 19:30** giờ Việt Nam
- **Luôn đăng trước rồi đặt lịch**, không đăng đúng giờ, không để tự lên ngay
- Facebook phải dùng lệnh **`reels`**, không dùng `video`

Đang tồn 4 bài sau VD-007 → rải mỗi ngày một bài, hết ngày 06/08.

### Lệnh một ngày — thay VD-0XX rồi chạy ba dòng

```bash
.venv-dang/bin/python scripts/dang-video-youtube.py dang VD-0XX --kenh en \
    --hen-gio 2026-08-0DT19:30:00+07:00 --dang-that
.venv-dang/bin/python scripts/dang-video-youtube.py dang VD-0XX --kenh vi \
    --hen-gio 2026-08-0DT19:30:00+07:00 --dang-that
python3 scripts/dang-video-fb.py reels video/exports/VD-0XX-reels.mp4 --ma VD-0XX \
    --hen-gio 2026-08-0DT19:30:00+07:00 --dang-that
```

✅ **VD-003 đã bù xong cho Facebook** — đăng 02/08, hẹn **21:45** (tách khỏi khung 19:30 của
VD-007 để hai bài không đè nhau trong cùng một tối). Mã bài `2227069261412713`.

### VD-007 — tải lên 02/08 lúc 17:4x, hẹn 19:30

| Nơi | Mã bài | Chế độ |
|---|---|---|
| YouTube tiếng Anh | https://youtu.be/QaDH7_4ZaFA | riêng tư · hẹn 19:30 |
| YouTube tiếng Việt | https://youtu.be/Wfsv45pH9z0 | riêng tư · hẹn 19:30 |
| Facebook (**Reels**) | `4731819720383240` | chưa công khai · hẹn 19:30 |

Cả ba nơi **đều nhận lịch**: YouTube lưu `publishAt = 12:30Z`, Facebook lưu
`scheduled_publish_time = 2026-08-02T12:30:00+0000` — đều là 19:30 giờ Việt Nam.

⚠️ **Nhận lịch chưa chắc đã tự công khai** — riêng YouTube, project chưa qua audit nên
19:30 mới biết chắc. Không lên thì vào Studio bấm tay.

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

**Còn tồn: 5 bài + 1 lượt bù (VD-003 trên Facebook) = 16 lượt đăng.**

⚠️ **Thứ tự năm bài còn lại đã đảo có chủ ý: VD-007 → VD-009 → VD-011 → VD-010 → VD-012.**
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
