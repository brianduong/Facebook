# STATUS — Ghi chú tiến độ

_Cập nhật: 2026-08-06_

## 📍 Ba nơi đăng — tên gọi quy ước

Mỗi bài đi lên **ba nơi**, gọi đúng ba tên này:

| Tên gọi | Bản dùng | Nơi thật |
|---|---|---|
| **YouTube tiếng Việt** | tiếng Việt | https://youtube.com/@songtotdaily |
| **YouTube tiếng Anh** | tiếng Anh | https://youtube.com/@onesmallthingdaily |
| **Facebook** | **tiếng Việt** | https://www.facebook.com/songtot.in · ~9,9K người theo dõi |

Facebook dùng **chung file video tiếng Việt** với YouTube tiếng Việt, không render riêng.
Nên mỗi bài có 2 file video nhưng **3 lượt đăng**.

## 🤖 Đăng tự động — dựng xong 02/08, cả ba nơi ✅

Đăng bằng dòng lệnh, chữ bóc thẳng từ file caption nên không phải dán tay ô nào.
**Đã chạy thật, không còn phải bấm gì trên trình duyệt.**

| Nơi | Script | Chìa khoá |
|---|---|---|
| YouTube tiếng Anh · tiếng Việt | `scripts/dang-video-youtube.py` | `secrets/youtube-token-{en,vi}.json` |
| Facebook | `scripts/dang-video-fb.py reels` | `.env` → `FB_PAGE_TOKEN` |

### Nguyên tắc đăng (anh chốt 02/08)

- **Nhiều nhất 1 bài/ngày**
- **Đồng bộ cả ba nơi cùng ngày, cùng một bài** — đừng để nơi này đi trước nơi kia
- **Công khai lúc 19:30** giờ Việt Nam
- **Luôn đăng trước rồi đặt lịch**, không đăng đúng giờ, không để tự lên ngay
- Khi có một lô bài: dùng **19:30 gần nhất còn trống** cho bài đầu (tối nay chỉ khi còn
  ít nhất 10 phút), rồi **19:30 mỗi ngày kế tiếp** cho từng bài còn lại
- Sau khi lên lịch phải đọc lại API, khớp ngày/giờ/câu đầu và xóa lịch trùng nếu có

### Ba dòng lệnh của một ngày

```bash
.venv-dang/bin/python scripts/dang-video-youtube.py dang VD-009 --kenh en \
    --hen-gio 2026-08-03T19:30:00+07:00 --dang-that
.venv-dang/bin/python scripts/dang-video-youtube.py dang VD-009 --kenh vi \
    --hen-gio 2026-08-03T19:30:00+07:00 --dang-that
python3 scripts/dang-video-fb.py reels video/exports/VD-009-reels.mp4 --ma VD-009 \
    --hen-gio 2026-08-03T19:30:00+07:00 --dang-that
```

Bỏ `--dang-that` là chạy thử, chỉ in ra những gì sắp gửi. Xem trước **không cần đăng nhập**.

### Mấy chỗ phải nhớ

- ⚠️ **Facebook phải dùng lệnh `reels`**, không dùng `video`. Lệnh `video` đi đường
  `/videos` ra bài video thường; video dọc 9:16 phải qua `/video_reels` mới vào tab Reels.
- ⚠️ **YouTube khoá video ở chế độ riêng tư trước giờ hẹn** vì project chưa qua audit,
  nhưng đã đo thật: tới `publishAt` video vẫn tự công khai đúng giờ.
- ⚠️ **Facebook hẹn giờ chạy thẳng**, không vướng audit. Đòi cách hiện tại ≥10 phút.
- ⚠️ Màn hình đồng ý của Google phải ở **In production**, không thì Google thu hồi quyền
  sau 7 ngày. Đã chuyển 02/08.
- 🔒 `secrets/` và `.env` đều bị `.gitignore` chặn. **Đừng dán token vào chat.**

Các bước lấy chìa khoá (nếu phải làm lại): `docs/huong-dan-dang-youtube.md` cho YouTube,
`docs/huong-dan-dang-tu-dong.md` cho Facebook.

### Ảnh bìa — anh chốt 02/08: không làm

Không bài nào có ảnh bìa tự chọn, tất cả để YouTube và Facebook tự cắt khung hình. Hai kênh
YouTube **đã xác minh** nên đặt bìa được, nhưng anh quyết không cần: Shorts và Reels chạy
ngay khi lướt tới, hiếm ai nhìn bìa. Công cụ `scripts/tao-anh-bia-reels.py` vẫn còn đó,
`video/thumbnails/` mới có mỗi `VD-002-bia.png` từ hồi thử nghiệm.

## 📍 Dừng ở đâu — làm tiếp từ đây

### Đã hẹn giờ tới hết 10/08 lúc 19:30 — đủ cả ba nơi

| Ngày | Bài | YouTube tiếng Việt | YouTube tiếng Anh | Facebook | Trạng thái |
|---|---|---|---|---|---|
| 04/08 | VD-009 | `rmgkx_XTnJo` | `leBaRFd4fXQ` | `315460902683557_1660124185681318` | ✅ đã lên |
| 05/08 | VD-011 | `tY5SZz3F5kY` | `ZzcZEZD_TSE` | `315460902683557_1660124532347950` | ✅ đã lên |
| 06/08 | VD-010 | `qUGygq8-qw4` | `MJCbGstdSgQ` | `315460902683557_1660124749014595` | 🕒 19:30 |
| 07/08 | VD-012 | `wECczzrqARA` | `EO_qomjUYPE` | `315460902683557_1660125055681231` | 🕒 19:30 |
| 08/08 | VD-013 | `VrHJoc6XGSg` | `DOYFZXQ_VC0` | Reels `787834854408440` | 🕒 19:30 |
| **09/08** | **VD-014** | `y6FLC-NdpwQ` | `Of0VLegiUvQ` | Reels `944174878692756` | 🕒 19:30 |
| **10/08** | **VD-015** | `UbdSj9x9bFg` | `aDd1IUzvab0` | Reels `2328234654652391` | 🕒 19:30 |

**Đã đọc lại API cả ba nơi ngày 06/08 để xác nhận, không tin dòng báo thành công của
script:** hai kênh YouTube đều **15 video, khớp đủ VD-001 → VD-015**, không trùng không
thiếu; bốn bài đang chờ đều lưu `publishAt = 12:30Z` đúng ngày của nó. Facebook có **đúng
5 lịch** (06/08 → 10/08), mỗi ngày một bài, không trùng giờ, permalink trả về `/reel/…`
nên chắc chắn là Reels chứ không phải video thường. `12:30Z` = **19:30 giờ Việt Nam**.

Hai lịch trùng phát sinh lúc chạy đợt VD-009→012 đã được xóa. VD-003 và VD-007 cũng đã
xác nhận công khai đúng lịch ngày 02/08.

### VD-014 · VD-015 — viết mới và đăng ngày 06/08

Hai bài đầu tiên **không còn nháp cũ nào để dựa**, viết mới hoàn toàn từ hồ sơ ý tưởng.

| Mã | Trụ | Chốt bài | CTA |
|---|---|---|---|
| VD-014 | 3 · What you already have | Cái hỏng thì kêu nên mình đếm; cái không hỏng thì im nên mình bỏ sót | Kể một thứ hôm nay không hỏng, càng nhỏ càng tốt |
| VD-015 | 4 · The voice in your head | Cùng một chuyện có hai câu — câu tử tế thì mình để dành cho người khác | Viết lại câu tự mắng theo kiểu nhắn cho bạn thân |

- **Thời lượng:** VD-014 88s (VI) · 87s (EN) · VD-015 79s (VI) · 77s (EN) — đều trên mốc 60s.
- **Xếp lịch không phạm luật trụ:** VD-013 trụ 1 → VD-014 trụ 3 → VD-015 trụ 4, không có
  hai bài cùng trụ đứng cạnh nhau. Kiểu CTA cũng khác nhau ba bài liền (hành động ngay lúc
  xem → kể chuyện ở bình luận → viết một dòng).
- **VD-014 cấm chữ "biết ơn"**, VD-015 **cấm cụm "yêu thương bản thân"** — cả trong caption
  lẫn khi trả lời bình luận. Ghi rõ trong hai file caption.
- ⚠️ **Thẻ tiếng Anh VD-014 lúc đầu lọt chữ `quiet gratitude`**, trái đúng luật của chính
  bài. Bắt được lúc chạy thử nên đã sửa trước khi đăng. **Bài trụ 3 sau này phải soi cả
  phần thẻ, không chỉ soi lời đọc.**
- 📌 **Anh chốt 06/08: không đọc lại chữ hai bài này.** Trạng thái duyệt để 🤖, lời đọc rút
  bằng `--cu-lam`, và **cứ để nguyên như đã đăng** — đừng hỏi duyệt lại, đừng render lại.
- Chỗ lệch cũ vẫn còn: ảnh rải **đều** trên các thẻ chữ, không gắn theo nội dung từng khối.

⏳ **Bài vừa hẹn giờ trên Facebook mất khoảng một phút mới hiện trong `/scheduled_posts`.**
VD-013 đăng lúc 17:18 ngày 04/08, đọc ngay sau đó thấy danh sách chỉ có 4 bài, tưởng hụt.
Tra thẳng `/{video-id}` thì đã `publish_status = scheduled` đúng mốc. **Chưa thấy trong
danh sách thì tra mã bài trước, đừng vội đăng lại** — đăng lại là ra hai lịch trùng.

⚠️ **Tên mục trong file caption phải viết bằng tiếng Việt, kể cả file `-en.md`.**
`dang-video-youtube.py` tìm đúng ba chuỗi `Tiêu đề` · `Mô tả` · `Thẻ`. Bản tiếng Anh của
VD-013 ban đầu đặt là `Title` · `Description` · `Tags` nên script báo *thiếu mục* dù chữ
có đủ, và kênh tiếng Anh không đăng được. Bài sau cứ chép khuôn `VD-012-caption-en.md`.

### Lịch còn chờ công khai

| Bài | Trạng thái |
|---|---|
| **VD-010 · VD-012 · VD-013** | 🕒 chờ công khai 06 → 08/08 |
| **VD-014 · VD-015** | 🕒 chờ công khai 09 → 10/08 |

**Thứ tự: VD-009 → VD-011 → VD-010 → VD-012 → VD-013 → VD-014 → VD-015**, mỗi ngày một
bài, hết ngày 10/08. VD-010 không được đứng liền sau VD-009, mà VD-011 · VD-012 cùng trụ 2
nên cũng không được dính nhau — xếp kiểu này gỡ được cả hai.

🔻 **Hết bài từ 11/08.** VD-016 (*Hỏi thêm một câu*, trụ 5) mới có hồ sơ ý tưởng trong
`content/ideas/y-tuong-VD-007-020.md`, chưa viết chữ nào. Muốn giữ nhịp mỗi ngày một bài
thì phải bắt đầu viết trước 10/08.

### ❗ Bài học 02/08: sổ và trí nhớ đều sai, chỉ API là đúng

Sổ cũ ghi "đã đăng tới VD-008, ba nơi đồng bộ". Nối API vào đọc thẳng thì không phải:

| Nơi | Thực tế trước hôm nay | Thiếu |
|---|---|---|
| YouTube tiếng Anh | VD-001→006, VD-008 | **VD-007** |
| YouTube tiếng Việt | VD-001→006, VD-008 | **VD-007** |
| Facebook | VD-001, 002, 004, 005, 006, 008 · VD-002 đăng 2 lần | **VD-003 · VD-007** |

VD-007 render xong 30/07 mà chưa đăng đâu cả. Facebook còn sót thêm VD-003 từ 27/07 —
hơn một tuần không ai biết. Cả hai đã bù trong tối nay.

**Cách kiểm cho lần sau:** đọc danh sách video qua API rồi khớp mô tả với `content/captions/`
**bằng máy, đừng nhìn mắt**. Bài 27/07 trên Facebook mở đầu *"Sáng nay mở mắt ra…"* trông
hệt VD-003 nhưng thực ra là VD-001 bản caption viết lại.

### ⚠️ Chỗ nghẽn thật — đã có số lần đầu (04/08)

Kéo bằng API ngày 04/08, tám bài đã công khai:

| Mã | Sống Tốt (VI) | One Small Thing (EN) |
|---|---:|---:|
| VD-001 | 824 | 8 |
| VD-002 | 875 | 24 |
| VD-003 | 588 | 39 |
| VD-004 | **29** | 41 |
| VD-005 | 903 | 1 |
| VD-006 | 498 | 0 |
| VD-007 | 1.082 | 9 |
| VD-008 | **1.174** | 8 |
| **Tổng** | **5.971** · 12 đăng ký | **130** · 3 đăng ký |

Page Facebook: 9.926 người theo dõi.

**1. Kênh Việt chạy, kênh Anh thì không** — chênh 46 lần trên cùng nội dung, cùng ngày
đăng. Đây không phải chuyện nội dung hay dở. Trước khi đổ thêm công vào kênh EN thì phải
hiểu vì sao nó không được đẩy, không thì làm bao nhiêu cũng vậy.

**2. Kênh Việt đang lên dần** — hai bài mới nhất là hai bài cao nhất (VD-008: 1.174,
VD-007: 1.082) so với ~500–900 hồi cuối tháng 7. Nhịp đăng đều có tác dụng.

**3. VD-004 tiếng Việt chỉ 29 lượt** trong khi mọi bài VI khác đều 500+. Lệch 20 lần so
với bài kém nhất kế tiếp, khó mà do nội dung — nghi bị hạn chế hiển thị. Đáng vào Studio
xem thử.

**4. Cả 16 bài, hai kênh, đều 0 bình luận.** Không hẳn bất thường với Shorts, nhưng cũng
có thể do tắt bình luận — kiểm trong Studio là biết ngay.

⚠️ **Còn thiếu tỉ lệ xem hết** — đây mới là số YouTube chấm, mà API công khai không trả
về. Phải lấy qua YouTube Analytics API hoặc xem tay trong Studio. Bảng trong
`schedule/calendar.md` vẫn đang chờ điền.

**Hết hàng có nháp cũ.** VD-011 và VD-012 là hai bài cuối còn nháp từ pipeline cũ. VD-013
viết mới ngày 04/08, VD-014 và VD-015 viết mới ngày 06/08. Từ **VD-016 trở đi chỉ có hồ sơ
ý tưởng, chưa có chữ nào** — mỗi bài phải viết mới từ đầu.

### Ba bài mới — làm ngày 31/07

Cả ba đi trọn quy trình: hồ sơ ý tưởng → file song ngữ 13 khối → rút lời đọc hai thứ
tiếng → chấm ảnh tay từ bảng ứng viên → render VI + EN → caption hai kênh.

| Mã | Trụ | Chốt bài | CTA |
|---|---|---|---|
| VD-008 | 1 · Heavy days | Đi ngủ là việc tử tế đầu tiên làm cho mình của ngày mai | Đặt **báo thức ngược**, thả chữ "đặt rồi" |
| VD-009 | 4 · The voice in your head | "Để mình nghĩ đã, tối nay mình trả lời nhé" | Chép câu đó lại, dùng thử rồi quay lại kể |
| VD-010 | 5 · Reaching people | Cái nặng mấy năm nay không phải người ta — là cái mình vác | Viết một dòng cho riêng mình, thả chữ "rồi" |

- **Ba nháp cũ chỉ dùng làm sườn, đã viết lại hẳn** — lý do từng chỗ ghi cuối mỗi file
  `song-ngu/`. Đáng chú ý: nháp VD-008 xưng **"em"** ở CTA (trái quy ước `bạn`/`mình`) và
  dùng hành động trùng ý dự trữ; nháp VD-010 chốt bằng *"cho nhẹ người mà đi"* — đúng lời
  hứa mà vòng chấm đã cấm, nên bỏ và thay bằng hai khối "không nhẹ ngay đâu".
- **VD-009 khối 7 đứng riêng một thẻ chữ** — câu chép được hiện to giữa màn hình, đúng
  công thức đã ăn ở VD-005. Đã kiểm bằng `--chi-do-dai`: nó là thẻ số 9, không dính khối nào.
- **Đổi một ảnh sau khi soi khung hình:** ảnh nền số 4 của VD-009 lúc đầu là người đang
  **hút thuốc** ngồi bên cửa sổ — không hợp kênh, đã thay bằng ảnh tay cầm điện thoại
  trên bàn làm việc rồi render lại cả hai bản.
- ⚠️ **Chữ chưa ai đọc lại** — cả ba để trạng thái duyệt 🤖, rút lời đọc bằng `--cu-lam`.
- **Nhắc trong caption:** VD-008 nên **đăng buổi tối 21–22h** (CTA đặt báo thức làm được
  ngay tại chỗ); VD-009 có **CTA độ trễ** nên phải mở lại bài sau 3–4 ngày để trả lời;
  VD-010 **đừng đăng liền sau VD-009**, xen một bài trụ 2 vào giữa.
- Chỗ lệch cũ vẫn còn: ảnh rải **đều** trên các thẻ chữ, không gắn theo nội dung từng khối.
  Lần này rơi trúng khá nhiều (VD-010 khối "không phải quay lại làm bạn" đúng lúc ảnh cái
  ghế trống bên cửa sổ) nhưng đó là may, không phải do máy hiểu.

### Hai bài nữa — cũng làm ngày 31/07

| Mã | Trụ | Chốt bài | CTA |
|---|---|---|---|
| VD-011 | 2 · Small kindness | Chỗ khó không nằm ở lúc làm — nằm ở lúc mình thèm kể | **Đảo: cấm kể ở bình luận**, giữ cho riêng mình |
| VD-012 | 2 · Small kindness | Cảm ơn thì có nói, mà mắt vẫn ở trên điện thoại | Xin **người đứng bên kia quầy** kể chuyện của họ |

- ⚠️ **VD-012 phải lật góc vì nháp cũ trùng VD-004.** Nháp dựng cả bài quanh *"một lời khen
  cụ thể"* (*"ly này pha đúng ý em"*), mà VD-004 đã là **"cảm ơn có chữ vì"** — cùng đúng
  một cơ chế, và VD-004 còn có sẵn câu *"nói xong thì để ý mặt người ta"*. Hai bài sẽ như
  một bài làm hai lần. Bản mới **bỏ hẳn phần lời nói, dồn vào ánh mắt**: cái VD-004 không
  có là *người phục vụ là người lạ* và chỗ hỏng nằm ở chỗ mắt vẫn ở trên điện thoại.
  **Nếu sửa chữ về sau, giữ nguyên nguyên tắc này** — đã ghi trong ghi chú sản xuất.
- **VD-011 sửa lỗi "chúng ta"** ở đoạn hai của nháp (*"việc tốt của chúng ta"*), trái
  `docs/giong-van-tieng-viet.md`. Thêm hai khối 10 · 11 về **cơn thèm kể sau khi làm xong**
  — đó mới là chỗ bài này có thật; nháp chỉ bảo "rồi không kể với ai hết".
- ⚠️ **VD-011 sẽ ít bình luận hơn hẳn mọi bài khác, và đó là chủ ý** — CTA cấm kể. Đo bài
  này bằng **lượt lưu** và **tỉ lệ xem hết**, đừng đo bằng bình luận, và **đừng tự bình
  luận mở hàng** (mở hàng là phá đúng cái CTA).
- **Xếp lịch:** VD-011 và VD-012 cùng trụ 2 → hồ sơ ý tưởng dặn **đảo VD-012 với VD-013**
  để hai bài không liền nhau. Tiện thể tách luôn hai ảnh nền máy quẹt thẻ (VD-011 ảnh 5 và
  VD-012 ảnh 2) khỏi đứng cạnh nhau.
- ⚠️ **Chữ chưa ai đọc lại** — cả hai để trạng thái duyệt 🤖, rút lời đọc bằng `--cu-lam`.

### VD-007 — làm ngày 30/07

- **Render cả hai bản:** `VD-007-reels.mp4` (VI · 78s · −16,1 LUFS) và
  `VD-007-reels-en.mp4` (EN · 85s · −15,4 LUFS) — 1080×1920 · 30fps · đều trên 60s.
- **Chữ viết mới hoàn toàn, 13 khối** (`song-ngu/VD-007-song-ngu.md`). Nháp cũ
  `loi-doc/VD-007-loi-doc.txt` chỉ dùng làm sườn ý — nháp nhét cả ba cảnh vào một đoạn
  và mở bài bằng "Bạn có bao giờ thắc mắc…", kiểu câu của bài viết chứ không phải của ba
  giây đầu. **File nháp cũ đã bị ghi đè** bằng bản rút từ file song ngữ.
- **Ảnh:** 7 ảnh Pexels chấm tay — phòng có người ngồi làm việc → lớp học → hai người
  cùng một cái máy → hai bóng người trong khung cửa đêm → hai bàn tay đưa nhau →
  người trẻ ngồi bên cửa sổ → căn phòng nắng chiều.
- **Caption hai kênh:** `content/captions/VD-007-caption.md` và `VD-007-caption-en.md`.
- ⚠️ **Chữ chưa ai đọc lại** — trạng thái duyệt để 🤖 (em tự duyệt), rút lời đọc bằng
  `--cu-lam`. Anh đọc lại phần "Từng khối" trong file song ngữ, chỗ nào chưa ưng thì sửa,
  em render lại.
- Chỗ lệch cũ vẫn còn: ảnh rải **đều** trên các thẻ chữ nên "Chỉ ngồi đó tới khuya" đang
  chạy trên ảnh văn phòng, còn ảnh khung cửa đêm thì đến sau một nhịp.

### Làm tiếp theo thứ tự này (viết lại 06/08)

_(mục "viết VD-014" của bản 04/08 đã xong — VD-014 và VD-015 đăng ngày 06/08)_

1. **Viết VD-016 trước 10/08.** Đây là việc gấp nhất: hết 10/08 là đứt nhịp. Ý tưởng
   *Hỏi thêm một câu* (trụ 5) đã có trong `content/ideas/y-tuong-VD-007-020.md`,
   nhưng chưa có chữ nào.
2. **Vào Studio xem VD-004 tiếng Việt** — chỉ 29 lượt trong khi mọi bài VI khác 500+.
   Nghi bị hạn chế hiển thị. Nhân tiện xem luôn vì sao cả 16 bài đều 0 bình luận.
3. **Lấy tỉ lệ xem hết.** Số lượt xem đã có (bảng ở mục "Chỗ nghẽn thật"), nhưng tỉ lệ
   xem hết — số YouTube thật sự chấm — thì API công khai không trả về. Phải qua YouTube
   Analytics API hoặc xem tay trong Studio, rồi điền vào `schedule/calendar.md`.
4. **Tìm hiểu vì sao kênh tiếng Anh không được đẩy** (130 lượt so với 5.971). Trước khi
   quyết có đầu tư tiếp cho kênh EN hay không.
5. Còn nợ cũ: **thêm lại link Facebook** vào mô tả 3 video đầu kênh Sống Tốt (mục dưới).

### Chốt 28/07 — danh mục YouTube và thẻ tiếng Anh

**Danh mục: Con người và Blog (People & Blogs)** — cả hai kênh, mọi video. Ô này nằm
cuối trang Chi tiết, phải bấm **"Hiện thêm"** mới hiện ra nên rất dễ bỏ sót. Danh mục
là của **từng video**, không có chỗ đặt một lần cho cả kênh; sửa hàng loạt được ở
Studio → Nội dung → tích nhiều video → **Chỉnh sửa** → *Danh mục*.

**Bỏ thẻ học tiếng Anh** (`slow english` · `easy english listening` ·
`english listening practice`) — kênh One Small Thing không nhắm người học tiếng Anh nữa.
Đã gỡ khỏi caption VD-004 · VD-005 · VD-006 và ghi luật vào `docs/ke-hoach-kenh-tieng-anh.md`
(mục "Đăng mỗi Short"). **Ba video đã đăng (VD-001 → VD-003) để nguyên**, không sửa lại.

⚠️ **Còn hở:** bốn tài liệu định hướng kênh tiếng Anh vẫn viết trên nền "nhắm người Việt
và người châu Á đang học tiếng Anh" (`docs/ke-hoach-kenh-tieng-anh.md` mục "Kênh này nhắm
ai", `docs/dinh-huong-one-small-thing.md`, `content/ideas/kho-y-tuong-en.md`, mục kênh thứ
hai cuối file này). Chưa sửa vì cần anh nói kênh giờ nhắm ai. Để nguyên thì ý tưởng và
chữ của các video sau vẫn bị kéo về hướng cũ.

### Hàng đợi nối thêm VD-021 → VD-030 (27/07) — tròn 6 bài mỗi trụ

Hồ sơ + vòng chấm: `content/ideas/y-tuong-VD-021-030.md`. 10/12 ý dự trữ dùng được;
2 ý loại vì trùng chủ đề ngủ với VD-008. Ba ý phải lật góc mới qua cửa "không trùng"
(VD-023 món ăn→người nấu · VD-030 nhìn người ta→nhìn mình · VD-022 kẻ ranh giới với
VD-006). **Hết VD-030 = đúng 6 bài mỗi trụ → đủ dựng 5 video dài 16:9.** Kho dự trữ
chỉ còn 2 ý: đợt VD-031+ phải nghĩ vòng mới, nguồn lấy từ bình luận người xem + số
liệu 48h, và tránh hai cụm đã chật (điện thoại · nới-tay-với-mình).

### Hàng đợi ý tưởng đã chốt đến VD-020 (27/07) — đã qua vòng chấm

Bảng thứ tự sản xuất: `content/ideas/kho-y-tuong.md` (mục "Xếp hàng làm tiếp").
**Hồ sơ chi tiết 14 ý — mỗi ý có thông điệp, hook hai thứ tiếng, cảnh cụ thể, CTA —
và bảng chấm 5 cửa: `content/ideas/y-tuong-VD-007-020.md`.** Kết quả chấm: 14/14 giữ,
3 ý sửa trong lúc chấm (VD-007 đổi CTA vì trùng, VD-010 thêm neo cụ thể, VD-017 né từ
ngữ thiền); lịch đăng đảo VD-012 ↔ VD-013 cho hai bài trụ 2 khỏi liền nhau.

- **VD-007 → VD-012** — sáu bài đã có lời đọc nháp từ pipeline cũ (`loi-doc/VD-00X-loi-doc.txt`).
  Khi làm: lấy nháp làm sườn ý, viết lại thành file song ngữ 12–13 khối, **đừng render
  thẳng từ nháp** — chưa duyệt và có chỗ dùng "chúng ta" (VD-011).
- **VD-013 → VD-020** — tám ý mới chọn từ kho chung, rải đều năm trụ: mười phút đầu tiên ·
  những thứ hôm nay không hỏng · nói với mình như nói với bạn thân · hỏi thêm một câu ·
  ngồi im năm phút · làm dở vẫn tính · mình của ngày trước từng mong điều này · để người
  khác giúp mình.
- Kho EN (`kho-y-tuong-en.md`) đã đổi mã các ý xếp hàng sang `VD-0XX` dùng chung; mã
  `EN-0XX` còn lại là kho chờ cho VD-021 trở đi.

### VD-006 — làm xong đêm 27/07

- **Render cả hai bản:** `VD-006-reels.mp4` (VI · 67s · −16,0 LUFS) và
  `VD-006-reels-en.mp4` (EN · 70s · −15,7 LUFS) — đều 1080×1920 · 30fps · trên 60s.
- **Thêm khối 5 "Cuộc đua không có thật"** vào file song ngữ (12 → 13 khối): bản 12
  khối ước chỉ ~60 giây tiếng Việt, đúng mép mốc thưởng. Lý do ghi cuối file song ngữ.
  ⚠️ Khối này em tự viết, anh chưa đọc.
- **Ảnh:** 7 ảnh Pexels chấm tay theo mạch bài — cuộn điện thoại trong tối → ảnh tốt
  nghiệp (đoạn kết người ta khoe) → người chạy giữa phố → cửa sổ có người ngồi ngẫm →
  khoảng lặng bên cửa sổ → đường quê một người chạy → đường sáng bình minh.
- **Caption hai kênh:** `content/captions/VD-006-caption.md` (Facebook + YouTube Shorts)
  và `VD-006-caption-en.md` — viết lại theo kịch bản 13 khối, bản caption cũ dùng chữ
  của dàn ý 1:1 hồi 25/07.
- Dòng B-roll trong `content/scripts/VD-006-so-sanh-voi-chinh-minh.md` đã cập nhật
  từ khoá theo kiểu VD-004/VD-005.

**Còn nợ:** chưa đăng Facebook Page · chưa chốt giọng tiếng Anh (đang tạm
`en_US-ryan-high`, còn 3 giọng chờ anh nghe ở `video/thu-giong-en/`).

## 🎉 Đã lên sóng — đêm 27/07

**Hai kênh YouTube đã lập và đăng xong ba video đầu.**

| Kênh | Handle | Video đã đăng |
|---|---|---|
| **One Small Thing** (tiếng Anh) | https://youtube.com/@onesmallthingdaily | VD-001 · VD-002 · VD-003 |
| **Sống Tốt** (tiếng Việt) | https://youtube.com/@songtotdaily | VD-001 · VD-002 · VD-003 |

Thứ tự đăng VD-001 → VD-002 → VD-003 là cố ý: YouTube xếp video mới nhất lên đầu, nên
VD-003 nằm trên cùng — nó là bài giải thích đúng cái tên kênh tiếng Anh.

Facebook Page vẫn chưa đăng ba bài này. Chưa commit, chưa push — đúng như anh dặn.

### Đo số sau 48 giờ

Ghi vào `schedule/calendar.md`, **tách riêng từng kênh**:

| Số cần lấy | Vì sao |
|---|---|
| Lượt xem | biết bài nào được đẩy |
| **Tỉ lệ xem hết** | **quan trọng nhất** — YouTube chấm bằng cái này |
| Người đăng ký mới | đường tới mốc 1.000 để bật kiếm tiền |
| Lưu / chia sẻ | dấu hiệu ý đó đáng gom vào video dài |

## ⏰ Việc phải làm sau 24 giờ (đặt lịch 28/07)

Kênh **Sống Tốt** (`@songtotdaily`) đang chờ YouTube duyệt xác minh — số điện thoại vừa
dùng cho kênh One Small Thing nên không xác minh tức thì được.

Chưa xác minh thì **link ngoài trong mô tả không bấm được**, và YouTube tô đỏ ô mô tả.
Nên ba video đầu đăng **không có dòng Facebook**.

**Xong 24 giờ, quay lại làm:** Content → sửa mô tả từng video → thêm lại dòng
`Facebook: https://www.facebook.com/songtot.in`. Sửa mô tả không ảnh hưởng lượt xem.

Đây là đường duy nhất kéo 9,9K người bên Facebook sang YouTube, đừng bỏ qua.

## 👉 Anh đọc chỗ này trước — làm đêm 27/07

**Sáu video đã render xong, sẵn sàng đăng.** Ba bài × hai thứ tiếng.

| Mã | Tiếng Việt (Sống Tốt) | Tiếng Anh (One Small Thing) |
|---|---|---|
| VD-001 · Ba điều biết ơn | `VD-001-reels.mp4` · 75s | `VD-001-reels-en.mp4` · 84s |
| VD-002 · Tử tế không lãng phí | `VD-002-reels.mp4` · 62s | `VD-002-reels-en.mp4` · 70s |
| VD-003 · Hôm nay một việc | `VD-003-reels.mp4` · 69s | `VD-003-reels-en.mp4` · 78s |

Tất cả 1080×1920, tiếng đều −15,5 đến −16,2 LUFS, đều **trên 60 giây** (mốc thưởng TikTok).

**Giọng tiếng Việt đã sửa theo góp ý "phải có ngữ điệu"** — đổi sang kiểu `doc_truyen`,
đo được hơn `tu_nhien` 44% về độ dao động cao độ, cộng nới khoảng nghỉ giữa các ý.
Anh nghe lại xem đã ra "giọng nói" chưa.

**Chữ đăng bài** đã viết sẵn: `content/captions/VD-00X-caption.md` (Việt) và
`VD-00X-caption-en.md` (Anh, có sẵn tiêu đề · mô tả · thẻ).

**Chưa làm, đúng như anh dặn:** chưa đăng lên Page, chưa commit, chưa push.

**Một lỗi suýt lọt:** VD-001 bản đầu render thiếu hẳn hai khối chữ, vì `render-video-v2.py`
ưu tiên file `-loi-doc-v2.txt` cũ hơn bản rút từ file song ngữ. Đã sửa, và đã thêm chốt
chặn: giờ render sẽ **dừng hẳn** nếu lời đọc không khớp file song ngữ, thay vì lặng lẽ
dựng ra video mang chữ cũ.

**Một chỗ chưa hoàn hảo, em chưa sửa:** ảnh nền rải **đều** trên các thẻ chữ chứ không
gắn theo nội dung từng khối. Nên có chỗ lệch nhẹ — ví dụ VD-001 thẻ "không nghĩ ra đủ ba
thì hai cũng được" lại đang chạy trên ảnh bát bún. Không sai hẳn (bữa cơm là một trong ba
thứ) nhưng chưa khớp. Sửa được, nhưng phải gắn từ khoá B-roll với từng khối trong file
song ngữ — việc đó lớn hơn một đêm, để anh quyết có làm không.


## Chốt trong ngày 26/07 — làm lại toàn bộ cách sản xuất

VD-001 đã đăng hôm qua (bản 1:1, video thường). Sau khi xem lại và nhận góp ý,
có **4 chỗ hỏng** — đã sửa cả 4:

| Hỏng | Nguyên nhân thật | Đã sửa thế nào |
|---|---|---|
| Âm thanh nhão | `aecho` trễ 24 ms gây lược tần số, nâng 220 Hz làm đục, nén quá tay, và **chuẩn hoá độ to từng câu một** | Bỏ echo, bỏ nâng 220 Hz, nén nhẹ đi, chuẩn hoá độ to **một lần** trên toàn bài |
| Giọng đọc chứ không phải giọng nói | `say` của macOS (giọng Linh) là TTS ghép âm 22 kHz, không có hơi thở | **VieNeu-TTS v3 Turbo 48 kHz**, giọng **Phạm Tuyên**, kiểu `tu_nhien` |
| Chữ nghe như bản dịch | Câu nào cũng đủ chủ–vị, không tiểu từ, ẩn dụ mượn từ tiếng Anh | Viết lại theo `docs/giong-van-tieng-viet.md` |
| Hình nhìn rẻ tiền | Nhân vật SVG vẽ tay đảo qua lại 2 khung miệng đóng/mở | **Bỏ hẳn nhân vật.** Nền là ảnh chụp thật tải từ Pexels |

Kèm theo: **đổi hẳn sang Reels dọc 9:16** (1080×1920), chừa vùng an toàn đáy 320px / phải 120px.

## VD-002 — bản thật đầu tiên của pipeline mới ✅

`video/exports/VD-002-reels.mp4` · 1080×1920 · 30fps · h264+AAC 48 kHz · **63s** · **8,9 MB**
- 15 thẻ chữ · 7 ảnh chụp thật từ Pexels · giọng Phạm Tuyên · nhạc nền gốc `nen-am-ap`
- Tiếng: **−16,0 dB trung bình, đỉnh −0,4 dB** — đều từ đầu đến cuối
- Ảnh chọn tay qua bảng `--chon`: mái ngói mưa → hai người chung dù → phỏng vấn →
  phố mưa đêm → phố ướt ánh đèn → hai người đi mưa → đường tối ánh đèn ấm

Bản thử VD-001 (`VD-001-reels.mp4`) vẫn đang dùng **ảnh giả** (gradient + hạt nhiễu) vì
render trước khi có Pexels key — cần chạy lại bằng ảnh thật nếu muốn đăng lại dạng Reels.

## Duyệt chữ trước khi render (mới, từ VD-003)

Anh xem VD-002 xong thấy chữ vẫn "ngôn từ Google dịch". Nguyên nhân là chữ chỉ được đọc
lại sau khi video dựng xong. Nên giờ tách khâu duyệt chữ ra trước, thành bước riêng.

Mỗi video một file song ngữ `content/scripts/song-ngu/VD-XXX-song-ngu.md`, hai tầng:
đầu file là **Đọc liền mạch** (toàn bộ EN rồi toàn bộ VI, để soi nghĩa một lượt — máy ghép,
không sửa tay), dưới là **Từng khối** với EN và VI đặt cạnh nhau — chỗ sửa thật.

Anh sửa ở khối VI → chạy `tach-loi-doc.py VD-XXX --dong-bo` để phần trên cập nhật theo →
ưng thì đổi `Trạng thái duyệt` thành ✅ → chạy `tach-loi-doc.py VD-XXX` để rút bản VI ra
`loi-doc/`. Chưa duyệt thì script không rút. Chi tiết trong `docs/giong-van-tieng-viet.md`.

## Quy trình mới

```bash
# 0. Anh duyệt chữ trước (file song ngữ), rồi rút ra lời đọc
python3 scripts/tach-loi-doc.py VD-003

# 1. Đo thử bài đủ 60 giây chưa
.venv-tts/bin/python scripts/render-video-v2.py VD-003 --chi-do-dai

# 2. Gom ứng viên ảnh rồi xem bảng, tự chấm số
python3 scripts/tai-anh-pexels.py VD-003 --chon 6
open video/thu-anh/VD-003-chon.png

# 3. Lấy đúng những số đã chấm (thứ tự gõ = thứ tự trong video), nên lấy ~7 ảnh
python3 scripts/tai-anh-pexels.py VD-003 --lay 4,10,18,16,12,9,29

# 4. Render Reels — chạy bằng Python của môi trường TTS, KHÔNG phải python3
.venv-tts/bin/python scripts/render-video-v2.py VD-003 --nhac assets/music/nen-am-ap.m4a
```

Chấm ảnh thì tránh: ảnh đen trắng (lệch với ảnh màu), logo thương hiệu trong khung,
biển hiệu chữ nước ngoài rõ mặt, ảnh studio nền trơn.

Nghe thử giọng trước khi chốt:
```bash
.venv-tts/bin/python scripts/thu-giong-vieneu.py --liet-ke    # 14 giọng có sẵn
.venv-tts/bin/python scripts/thu-giong-vieneu.py              # nghe 3 giọng gợi ý
```

## Môi trường TTS (`.venv-tts/`)

`onnxruntime` chưa có bản cho Python 3.14 của máy → dựng môi trường riêng trên Python 3.13.
Thư mục này **không lên GitHub**. Dựng lại khi cần:

```bash
brew install python@3.13
/usr/local/opt/python@3.13/bin/python3.13 -m venv .venv-tts
.venv-tts/bin/pip install vieneu
```

Model tải về lần đầu rồi chạy offline mãi, không tốn token. Tổng hợp nhanh hơn thời gian
thực (~13 giây tiếng mất ~7 giây máy chạy) — cả video 60s mất khoảng 40 giây.

## Đã xong ✅

**Nhận diện & Page**
- Icon + banner đã đổi trên Page. Bio đã dán ("🌱 Gieo một điều lành mỗi ngày…").
- Danh mục Page vẫn là *Personal blog* → **nên đổi** sang Community / Media / Video Creator.

**Nội dung**
| Mã | Kịch bản | Lời đọc | Caption | Ảnh quote | Video |
|----|:--------:|:-------:|:-------:|:---------:|:-----:|
| VD-001 | ✅ | ✅ **đã viết lại (v2)** | ✅ | ✅ | ✅ đã đăng bản cũ 1:1 · bản Reels mới đang thử |
| VD-002 | ✅ | ✅ **đã viết lại** | ✅ **đã viết lại** | ✅ | ✅ **đã đăng** (Reels 63s) |
| VD-003 | ✅ | 🟡 **song ngữ xong — chờ anh duyệt** | ✅ | ✅ | ⬜ chờ duyệt chữ |
| VD-004 → VD-006 | ✅ | ⚠️ chưa có file song ngữ | ✅ | ✅ | ⬜ bản nháp 1:1 **đã xoá 26/07** |

**Đã xoá bản nháp cũ của VD-003 → VD-006 (26/07).** 87 MB: `exports/VD-00X-nhap.mp4`,
`edit/VD-00X-nhap/`, `raw/VD-00X-giong-nhap.aiff` — render bằng pipeline cũ (1:1, nhân vật
vẽ tay, giọng `say`), không dùng lại được. Sẽ làm lại toàn bộ theo pipeline Reels 9:16.
| VD-007 → VD-012 | ⬜ | ⚠️ như trên | ⬜ | ⬜ | ⬜ |

**Công cụ mới (`scripts/`)**
- `tai-anh-pexels.py` — tải ảnh thật theo từ khoá B-roll ghi trong kịch bản
- `giong_vieneu.py` — giọng VieNeu + chuỗi hậu kỳ tiếng đã sửa
- `khung_reels.py` — lớp chữ trong suốt 9:16, đè lên ảnh
- `render-video-v2.py` — render Reels hoàn chỉnh
- `thu-giong-vieneu.py` — nghe thử giọng
- `tach-loi-doc.py` — rút bản VI trong file song ngữ ra lời đọc (chặn nếu chưa duyệt)
- `dang-video-youtube.py` — đăng lên hai kênh YouTube, chữ bóc thẳng từ file caption
- `dang-video-fb.py` — đăng lên Facebook · lệnh `reels` đi luồng /video_reels, có hẹn giờ

**Công cụ cũ** (`render-video-nhap.py`, `nhan_vat.py`, `canh_nen.py`, `giong_doc.py`)
vẫn giữ để đối chiếu, **không dùng nữa**.

## Kênh thứ hai: One Small Thing (YouTube tiếng Anh) — mở 27/07

Nhắm **người Việt và người châu Á đang học tiếng Anh** là chính, người bản ngữ là phụ.
Cách nhắm này gỡ được ba chỗ khó: có đường kéo người xem từ 9,9K Facebook, không rơi vào
ô motivational-shorts bão hoà, và giọng máy thành điểm cộng chứ không phải điểm trừ.

Bốn tài liệu của kênh này:

| File | Lo phần gì |
|---|---|
| `docs/ke-hoach-kenh-tieng-anh.md` | Lập kênh, nhận diện, giọng đọc, cách đăng |
| `docs/dinh-huong-one-small-thing.md` | Năm trụ nội dung, giọng điệu, luật viết chữ |
| `content/ideas/kho-y-tuong-en.md` | 30 ý tưởng + lịch làm video hai tháng |
| `docs/quy-trinh-short-va-video-dai.md` | Hai tuyến Short / video dài, đường kiếm tiền |

**Đã dựng xong:**
- **Giọng đọc offline**: Piper TTS chạy trên `onnxruntime` (cùng thư viện VieNeu).
  4 giọng ở `.piper-voices/` (ngoài GitHub, ~300 MB). Nghe thử ở `video/thu-giong-en/`.
- **Nhận diện**: `assets/logo/icon-one-small-thing.png` (ba chấm — một xong, hai để đấy)
  và `assets/images/banner-one-small-thing.png`. Chung màu nhấn vàng với Sống Tốt,
  khác nền (xanh đá thay xanh lá) để hai kênh không nhầm nhau.
- **Pipeline**: `render-video-v2.py --en` — đổi giọng, đổi logo, đổi lời kêu gọi và đổi
  màu lớp phủ tối theo kênh. `tach-loi-doc.py --en` rút khối EN ra lời đọc.

**Kênh đã lập 27/07:** https://youtube.com/@onesmallthingdaily
(`@onesmallthing` đã có người lấy trước)

**Chờ anh:** nghe 4 giọng tiếng Anh rồi chốt một

## Giọng Việt: đổi sang kiểu `doc_truyen` (27/07)

Anh chê giọng vẫn là "giọng đọc chứ không phải giọng nói, phải có ngữ điệu". Thay vì đoán,
em đo: ngữ điệu chính là **độ dao động cao độ**, đo được bằng độ lệch chuẩn F0.
`scripts/so-ngu-dieu.py` tổng hợp cùng một đoạn qua 16 cấu hình rồi chấm điểm.

| Cấu hình | F0 std |
|---|---|
| **`doc_truyen` · nhiệt 0.8 · lặng 0.28** ← chốt | **60,7** |
| `doc_truyen` · nhiệt 0.95 · lặng 0.15 | 57,2 |
| `tu_nhien` · nhiệt 0.8 · lặng 0.15 ← đang dùng trước đó | 42,2 |

Kết quả ngược trực giác: kiểu **`doc_truyen`** cho ngữ điệu cao hơn `tu_nhien` **44%**.
Tên nghe như "giọng đọc" nhưng thực chất là lối kể chuyện — có nhấn có chùng; còn
`tu_nhien` của VieNeu lại ra đều đều, đúng thứ bị chê.

Giữ nhiệt ở 0.8: đo rồi, nhiệt cao hơn **không** cho thêm ngữ điệu mà làm model vấp chữ.
Chỉ nâng `silence_p` lên 0.28 để có chỗ ngắt lấy hơi.

⚠️ `doc_truyen` đọc **nhanh hơn** (4,89 chữ/giây so với 4,28) → bài ngắn đi ~10%.
VD-001 tụt xuống 59 giây nên phải thêm một khối. `TOC_DO["VI"]` đã cân lại.

## Ba lỗi pipeline sửa nhân tiện (27/07)

| Lỗi | Hậu quả | Đã sửa |
|---|---|---|
| Thẻ chữ vắt qua hai khối | Chữ trên màn hình dính hai ý làm một, đúng chỗ chuyển ý | `tach_the` chỉ gộp câu trong cùng một khối |
| Render đọc `loi-doc` cũ mà không báo | Sửa chữ trong file song ngữ, quên rút lại → video mang chữ cũ | Báo khi file song ngữ mới hơn file lời đọc |
| Từ khoá B-roll nuốt cả câu ghi chú | Pexels tìm bằng cả câu "Tông trầm hơn hai video kia…" → ảnh vớ vẩn | Bỏ ngoặc đơn và cắt ở dấu chấm đầu tiên |

Ước lượng thời lượng cũng cân lại theo số render thật (VI 4,28 chữ/giây · EN 3,66),
và đếm theo **số thẻ** thay vì số khối. Giờ khớp đúng: ước 69/75s, thật 70/75s.

## Làm tiếp 👉

1. **Anh xem hai video VD-003** (`video/exports/VD-003-reels.mp4` và `-reels-en.mp4`)
   rồi duyệt. Chưa ưng chỗ nào thì sửa trong file song ngữ, em render lại.
2. **Anh nghe giọng**: `video/thu-giong/` (tiếng Việt) và `video/thu-giong-en/` (tiếng Anh)
   rồi chốt cho từng kênh.
3. **Giữ chỗ handle** `@songtotdaily` trên TikTok và Instagram nữa (YouTube đã lấy).
   Chưa đăng gì cũng cứ giữ — mất tên là mất hẳn, như vừa mất `@onesmallthing` và `@songtot.in`.
4. Render lại VD-001 bằng ảnh thật → đăng lại dạng Reels (bản 1:1 cũ để nguyên trên Page).
5. Làm file song ngữ cho VD-004 → VD-006 (VD-002 đã đăng, chỉ làm lại nếu muốn render lại).
6. **Tuyến video dài 16:9** — chưa dựng gì, xem `docs/quy-trinh-short-va-video-dai.md`.

✅ Pexels API key đã có trong `.env` — không còn chặn gì.

## Đang chờ anh trả lời
- **Chốt giọng nào?** Mặc định đang để Phạm Tuyên (nam · Bắc · tự nhiên).
- **Có thu giọng thật của anh không?** VieNeu nhân bản giọng từ clip 3–8 giây →
  kênh sẽ có giọng riêng, không đụng hàng ai.
- **Số liệu VD-001** sau 24–48h → ghi vào `schedule/calendar.md`.
- **Ảnh chụp tab Monetization** → em lên lộ trình theo con số thật (đang ~9.9K followers).

## Thông tin nền
- Page: **Sống Tốt** — https://www.facebook.com/songtot.in · Page ID trong `.env`
- Video: **Reels 9:16 (1080×1920)**, giữ **trên 60 giây**
- Kế hoạch: `PLAN.md` · Văn phong: `docs/giong-van-tieng-viet.md` ·
  Kiếm tiền: `docs/ke-hoach-kiem-tien.md` · Lịch: `schedule/calendar.md`
