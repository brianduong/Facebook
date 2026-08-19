# STATUS — Ghi chú tiến độ

_Cập nhật: 2026-08-19_

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

✅ **Ngày 15/08 mất quyền cả hai kênh YouTube, đã xin lại xong.** Nhưng lần xin lại đó
**tráo nhầm hai kênh** — đọc mục "LẦN SAU VÀO THÌ LÀM TỪ ĐÂY" ngay dưới trước khi xin quyền
lần sau, có ghi cách bắt và cách sửa.

| Nơi | Script | Chìa khoá |
|---|---|---|
| YouTube tiếng Anh · tiếng Việt | `scripts/dang-video-youtube.py` | `secrets/youtube-token-{en,vi}.json` |
| Facebook | `scripts/dang-video-fb.py reels` | `.env` → `FB_PAGE_TOKEN` |

### Nguyên tắc đăng (chốt 02/08, đổi nhịp 11/08)

- **2 ngày 1 bài** — anh đổi ngày 11/08, luật cũ (02/08) là mỗi ngày 1 bài
- **Đồng bộ cả ba nơi cùng ngày, cùng một bài** — đừng để nơi này đi trước nơi kia
- **Công khai lúc 19:30** giờ Việt Nam
- **Luôn đăng trước rồi đặt lịch**, không đăng đúng giờ, không để tự lên ngay
- **Neo chuỗi ngày vào bài đã LÊN SÓNG gần nhất**, không phải bài đã xếp lịch gần nhất:
  lấy ngày đó +2, +4, +6… Ví dụ VD-015 lên 10/08 → chuỗi là 12/08 · 14/08 · 16/08.
  Mốc đã trôi qua thì lấy **19:30 gần nhất còn ít nhất 10 phút**, rồi lại cách 2 ngày
- **Đổi nhịp thì dời cả lịch đang chờ** cho khớp chuỗi mới, không chỉ áp cho bài mới
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

### ▶️ LẦN SAU VÀO THÌ LÀM TỪ ĐÂY — ghim bình luận VD-018 (đang trễ), rồi viết VD-027 trước 03/09

_Chốt lúc ngày 19/08. Đọc `CLAUDE.md` trước để lấy luật đăng, rồi đọc API để lấy
trạng thái thật — đừng tin bảng dưới đây._

- ⏰ **VIỆC NÀY ANH ĐÃ NHẬN, HẸN LÀM NGÀY 20/08 — ghim bình luận tự thú cho VD-018, cả ba
  nơi.** Chi tiết đầy đủ (đường dẫn từng nơi + chữ dán sẵn hai thứ tiếng) ở mục **"VIỆC ANH
  LÀM TAY"** ngay dưới đây. Em không đăng hộ, anh chốt tự vào làm.
  CTA của bài này là kiểu mới: kênh kể trước rồi mới mời người xem kể. Khối cuối video nói
  thẳng *"mình kể trước, có sẵn một cái ghim trên đầu bình luận rồi đấy"* — không ghim là
  bài nói dối người xem.

  | Nơi | Vào đâu |
  |---|---|
  | YouTube tiếng Việt | https://studio.youtube.com/video/QkKOTAKB6AI/comments |
  | YouTube tiếng Anh | https://studio.youtube.com/video/jME8ehrxkg8/comments |
  | Facebook Reels | `1086214770915645` |

  Câu chữ **đã soạn sẵn, đừng viết lại**: `content/captions/VD-018-caption.md` mục "Nhắc khi
  đăng" (tiếng Việt) · `VD-018-caption-en.md` mục "Posting notes" (tiếng Anh).

  **Chia việc người/máy — đã kiểm ngày 15/08:**
  - **Ghim thì phải bấm tay.** YouTube Data API v3 không có thao tác ghim bình luận (chỉ
    `list` · `insert` · `update` · `delete` · `setModerationStatus`); ghim chỉ có trong
    Studio. Khoảng hai cú bấm mỗi kênh.
  - **Viết bình luận thì script làm được**, nhưng chưa viết: Facebook chỉ cần
    `POST /{post-id}/comments` bằng Page Token sẵn có; YouTube thì `commentThreads.insert`
    đòi phạm vi `youtube.force-ssl` — thêm vào `PHAM_VI` là **token cũ hỏng ngay, phải
    `xin-quyen` lại cả hai kênh** rồi `kiem-tra` (xem mục tráo kênh bên dưới).

- ✅ **Đã xong tới 01/09, đủ ba nơi — bảy bài đang chờ.** VD-020 (20/08) · VD-022 (22/08) ·
  VD-023 (24/08) · VD-021 (26/08) · VD-024 (28/08) · VD-025 (30/08) · VD-026 (01/09).
  Ngày lẻ để trống là **đúng nhịp 2 ngày**, không phải quên.
  Mốc trống kế tiếp là **03/09**, chưa có bài — viết VD-027 trước ngày đó.

- ⚠️ **BÀI HỌC 15/08 — xin quyền YouTube xong PHẢI chạy `kiem-tra` cả hai kênh trước khi
  đăng.** Lần xin lại quyền ngày 15/08 **tráo nhầm hai kênh**: token `vi` nối vào *One Small
  Thing*, token `en` nối vào *Sống Tốt*. Đăng luôn là video tiếng Việt lên kênh tiếng Anh và
  ngược lại — hỏng thật, phải gỡ, mà gỡ thì mất số liệu. Lệnh `kiem-tra` in dòng *"Đang nối
  vào"* cạnh dòng *"Mong đợi"* đúng để bắt chuyện này.

  **Sửa không cần xin lại quyền** — mỗi file token chỉ là chìa khoá của một tài khoản, nên
  tráo tên hai file là xong, rồi chạy lại `kiem-tra`:

  ```bash
  cd secrets && mv youtube-token-vi.json _tam.json \
    && mv youtube-token-en.json youtube-token-vi.json && mv _tam.json youtube-token-en.json
  ```

- 🔑 **Vì sao mất quyền ngày 15/08 — hai kiểu hỏng khác nhau, nhớ để lần sau chẩn nhanh:**
  - `youtube-token-vi.json` **tự biến mất**. Không ai xoá — chính script xoá
    ([`dang-video-youtube.py:113-117`](scripts/dang-video-youtube.py#L113-L117)): làm mới
    token thất bại thì `unlink` file rồi bắt xin lại. Nguyên nhân hay gặp nhất ghi ngay
    trong comment: **màn hình đồng ý về lại "Testing" → Google thu hồi refresh token sau 7
    ngày**. Token lưu 02/08, hỏng 15/08 — khớp. **Nên kiểm Publishing status = In production
    trong Google Cloud Console trước khi xin lại**, không thì tuần sau hỏng y hệt.
  - `youtube-token-en.json` còn nguyên nhưng lưu trước lúc thêm phạm vi `youtube` vào
    `PHAM_VI`; `google-auth` so phạm vi lúc nạp token, lệch là coi như chưa có quyền.

- ❗ **VD-016 và VD-017 trên YouTube lệch một ngày so với Facebook — chuyện đã rồi.** Đọc API
  ngày 15/08 xác nhận: VD-016 `publishedAt = 2026-08-11T12:30Z`, VD-017 `2026-08-13T12:30Z`,
  tức đã tự công khai ở mốc cũ trong lúc còn kẹt quyền, còn Facebook giữ 12/08 và 14/08.
  **Công khai rồi thì không dời được; để nguyên, đừng gỡ** — gỡ rồi đăng lại là mất số liệu
  và ra hai bản trùng.

- 🔻 **Còn lại VD-027 → VD-030 trong `content/ideas/y-tuong-VD-021-030.md`** — có hồ sơ,
  đã qua vòng chấm, chưa viết chữ nào. Hết VD-030 là **tròn 6 bài mỗi trụ**, đủ dựng 5
  video dài 16:9. **Sau VD-030 kho ý tưởng cạn** — dự trữ chỉ còn 2 ý và đều dính chủ đề
  ngủ, nên đợt VD-031+ phải có một vòng nghĩ ý mới (lấy từ bình luận người xem và từ số
  liệu 48 giờ, xem mục "Báo cáo vướng mắc" cuối hồ sơ ý tưởng).
  ⚠️ **VD-027 mở bằng cảnh chờ thang máy** — VD-021 (26/08) đã dùng cảnh *cửa thang máy sắp
  đóng*. Hai bài chỉ cách nhau vài mốc, nên khi viết VD-027 phải **đổi hẳn cảnh mở đầu**
  (đèn đỏ, xếp hàng) chứ đừng lặp thang máy.
  ⚠️ **Trụ của bài kế tiếp không được là trụ 4** — VD-026 (01/09) đã là trụ 4. VD-027 trụ 3,
  hợp lệ.

**Bảy bước của một bài** (VD-018 → VD-020 đi đúng đường này; ba bài một buổi là làm được):

```bash
# 1. Viết content/scripts/VD-0XX-*.md (có dòng '**Hình ảnh/B-roll:**') + song-ngu/VD-0XX-song-ngu.md
python3 scripts/tach-loi-doc.py VD-0XX --dong-bo           # dựng lại phần Đọc liền mạch
python3 scripts/tach-loi-doc.py VD-0XX --cu-lam            # rút lời đọc VI
python3 scripts/tach-loi-doc.py VD-0XX --en --cu-lam       # rút lời đọc EN
# 2. Đo trước khi chấm ảnh — dưới ~70 giây thì thêm khối, đừng chèn khối rỗng.
#    Con số ước ngay ở bước 1 là đủ để quyết có thêm khối hay không.
#    SỐ THẺ (để chọn số ảnh ở bước 3) thì gọi thẳng tach_the() cho nhanh — xem ghi chú dưới:
.venv-tts/bin/python scripts/render-video-v2.py VD-0XX --chi-do-dai   # chỉ khi cần đo thật
# 3. Chấm ảnh tay từ bảng ứng viên — chọn số ảnh CHIA CHẴN cho số thẻ nếu được
python3 scripts/tai-anh-pexels.py VD-0XX --chon 6
python3 scripts/tai-anh-pexels.py VD-0XX --lay 1,12,39,...
# 4. Render hai bản
.venv-tts/bin/python scripts/render-video-v2.py VD-0XX --nhac assets/music/nen-am-ap.m4a
.venv-tts/bin/python scripts/render-video-v2.py VD-0XX --en --nhac assets/music/nen-am-ap.m4a
# 5. Viết content/captions/VD-0XX-caption.md và -caption-en.md — chép khuôn **VD-017 trở đi**,
#    đừng chép VD-016: bản EN cũ còn câu "One video a day", sai nhịp mới
# 6. Chạy thử không có --dang-that trước, rồi đăng thật ba nơi
# 7. Đọc lại API cả ba nơi, khớp ngày + giờ + câu đầu caption, xóa lịch trùng nếu có
```

📌 **Lấy số thẻ đừng chạy `--chi-do-dai` nữa — nó đọc TTS thật, mất ~5 phút một bài.**
Import `render-video-v2.py` rồi gọi `tach_the(loi_doc)` là ra danh sách thẻ trong một giây,
đủ để chọn số ảnh. Chỉ chạy `--chi-do-dai` khi thật sự cần thời lượng từng thẻ. Đợt
VD-021→023 làm theo cách này, ảnh vẫn rơi đúng nhóm cả ba bài.

📌 **Chọn số ảnh theo số thẻ là cách rẻ nhất để ảnh rơi đúng khối.** Máy rải ảnh đều theo
công thức `anh[i * số_ảnh // số_thẻ]`, không hiểu nội dung. Biết trước số thẻ thì chọn số
ảnh chia chẵn cho nó là mỗi ảnh ôm gọn một nhóm khối — VD-019 có 18 thẻ, lấy 6 ảnh, ra
đúng 3 thẻ mỗi ảnh, khớp ngay từ lần lấy đầu. Chia lẻ vẫn xếp được (VD-018 25 thẻ ÷ 8 ảnh,
VD-020 22 ÷ 8) miễn là tính trước nhóm nào dài mấy thẻ. **Cả ba bài đợt này không phải đảo
`--lay` như VD-016.**

### Đã hẹn giờ tới hết 01/09 lúc 19:30

| Ngày | Bài | YouTube tiếng Việt | YouTube tiếng Anh | Facebook | Trạng thái |
|---|---|---|---|---|---|
| 04/08 | VD-009 | `rmgkx_XTnJo` | `leBaRFd4fXQ` | `315460902683557_1660124185681318` | ✅ đã lên |
| 05/08 | VD-011 | `tY5SZz3F5kY` | `ZzcZEZD_TSE` | `315460902683557_1660124532347950` | ✅ đã lên |
| 06/08 | VD-010 | `qUGygq8-qw4` | `MJCbGstdSgQ` | `315460902683557_1660124749014595` | ✅ đã lên |
| 07/08 | VD-012 | `wECczzrqARA` | `EO_qomjUYPE` | `315460902683557_1660125055681231` | ✅ đã lên |
| 08/08 | VD-013 | `VrHJoc6XGSg` | `DOYFZXQ_VC0` | Reels `787834854408440` | ✅ đã lên |
| 09/08 | VD-014 | `y6FLC-NdpwQ` | `Of0VLegiUvQ` | Reels `944174878692756` | ✅ đã lên |
| 10/08 | VD-015 | `UbdSj9x9bFg` | `aDd1IUzvab0` | Reels `2328234654652391` | ✅ đã lên **— bài neo chuỗi mới** |
| **12/08** | **VD-016** | `-QPXDUMNjeA` | `JuyV6yuT4O8` | Reels `1597246682117680` | ✅ FB 12/08 · ❗YT lên sớm 11/08 |
| **14/08** | **VD-017** | `gSRZoHt2Qns` | `xfpddU0eEAI` | Reels `2274455883304906` | ✅ FB 14/08 · ❗YT lên sớm 13/08 **— bài neo chuỗi mới** |
| **16/08** | **VD-018** | `QkKOTAKB6AI` | `jME8ehrxkg8` | Reels `1086214770915645` | ✅ đã lên — **còn nợ ghim bình luận** |
| **18/08** | **VD-019** | `S_unSrIUQrQ` | `TVVSGArEhko` | Reels `4372283653084479` | ✅ đã lên |
| **20/08** | **VD-020** | `GHllc5Y9Dcg` | `Ke8NOUMGFvI` | Reels `2324658331612348` | 🕒 đủ ba nơi |
| **22/08** | **VD-022** | `0PJEs8MmVhI` | `E_Ptc50eaBY` | Reels `1036926949220060` | 🕒 đủ ba nơi |
| **24/08** | **VD-023** | `QGTl_N9myyI` | `Jt_KCjctRZU` | Reels `27933369426273284` | 🕒 đủ ba nơi |
| **26/08** | **VD-021** | `H0FJCtH3mME` | `JR3v7P5wD10` | Reels `28043949088603153` | 🕒 đủ ba nơi |
| **28/08** | **VD-024** | `LCRzlnuXju4` | `JHDtW3BZVrE` | Reels `1767249877800838` | 🕒 đủ ba nơi |
| **30/08** | **VD-025** | `PpM9VLQWBqQ` | `W_fRsr5OtaI` | Reels `1684994275905731` | 🕒 đủ ba nơi |
| **01/09** | **VD-026** | `BVXmB70kgsk` | `Evmi4MDGsiA` | Reels `1692474351855713` | 🕒 đủ ba nơi |

**Chuỗi hiện tại neo vào VD-019 đã lên sóng 18/08** → 20 · 22 · 24 · 26 · 28 · 30/08 ·
01/09. Luật: neo vào **bài đã lên sóng gần nhất**, không phải bài đã xếp lịch gần nhất.

**Đã đọc lại API cả ba nơi ngày 15/08:** hai kênh YouTube đều **20 video, khớp đủ VD-001 →
VD-020**, không trùng không thiếu; ba bài mới còn `private` với `publishAt = 12:30Z` đúng
ngày, và **tiêu đề đúng kênh** (Sống Tốt toàn tiếng Việt, One Small Thing toàn tiếng Anh —
chỗ này phải soi vì suýt đăng nhầm kênh). Facebook: VD-017 `published = true`; ba bài mới
`published = false`, mốc đúng, `length` khớp file render, permalink `/reel/…`; edge
`/scheduled_posts` có **đúng 3 lịch chờ, không trùng**.

❗ **Hai bài VD-016 · VD-017 trên YouTube đã tự công khai ở mốc cũ** — đọc API xác nhận
`publishedAt` là `2026-08-11T12:30Z` và `2026-08-13T12:30Z`, lệch một ngày so với Facebook
(12/08 và 14/08). Để nguyên, không gỡ.

❗ **YouTube chưa dời được — thiếu quyền.** Token chỉ xin `youtube.upload`, gọi
`videos.update` trả **403 insufficientPermissions**. Đã thêm phạm vi `youtube` vào `PHAM_VI`
và viết lệnh `doi-lich` trong `scripts/dang-video-youtube.py`, nhưng **phải chạy lại
`xin-quyen` cả hai kênh** (mở trình duyệt, đăng nhập tay) thì lệnh mới chạy được. Các dòng
lệnh ghi trong `schedule/calendar.md`.

⏳ **Gấp: VD-016 trên YouTube tự công khai 19:30 ngày 11/08 nếu chưa dời kịp.** Chỉ dời
được khi video còn `private`.

Chuỗi 04/08 → 08/08 đã tự công khai đúng 19:30 từng ngày, không hụt ngày nào — đọc API
ngày 09/08 thấy cả năm bài đều `public` với `publishedAt` đúng mốc `12:30Z`.

📌 **Số video kênh báo ít hơn số bài thật là bình thường.** Lệnh `kiem-tra` in
`statistics.videoCount`, mà YouTube **không đếm bài đang riêng tư** — ngày 09/08 nó báo 13
trong khi trên kênh có 16 bài (13 đã công khai + 3 đang hẹn giờ). Đừng tưởng mất bài; muốn
biết đủ thiếu thì phải liệt kê `playlistItems` trên playlist `uploads`.

Hai lịch trùng phát sinh lúc chạy đợt VD-009→012 đã được xóa. VD-003 và VD-007 cũng đã
xác nhận công khai đúng lịch ngày 02/08.

### ⏰ VIỆC ANH LÀM TAY — ghim bình luận VD-018, anh hẹn làm **ngày 20/08/2026**

_Anh chốt 19/08: "phần bình luận ngày mai anh vô làm". Em không đăng hộ, để nguyên cho anh._

**Ba nơi, mỗi nơi hai bước: dán bình luận → ghim.** Cả YouTube lẫn Facebook đều **không cho
ghim qua API**, nên chỗ này bắt buộc bấm tay.

| Nơi | Vào đâu | Chữ lấy ở đâu |
|---|---|---|
| YouTube tiếng Việt | https://studio.youtube.com/video/QkKOTAKB6AI/comments | `content/captions/VD-018-caption.md` → mục "Nhắc khi đăng" |
| YouTube tiếng Anh | https://studio.youtube.com/video/jME8ehrxkg8/comments | `content/captions/VD-018-caption-en.md` → mục "Posting notes" |
| Facebook Reels | bài `1086214770915645` (`facebook.com/reel/1086214770915645`) | dùng bản tiếng Việt như trên |

**Bản tiếng Việt — dán nguyên khối:**

```
Mình kể trước cho công bằng: video đầu tiên của kênh này đọc bằng giọng máy của máy tính, nghe khô như đọc thông báo, chữ thì dịch từ tiếng Anh sang nên nghe không ra tiếng Việt. Xem lại vẫn ngượng. Nhưng nếu hồi đó chờ tới lúc làm được bản tử tế mới đăng thì giờ vẫn chưa có video nào cả. Còn bạn, hôm nay làm dở cái gì?
```

**Bản tiếng Anh — dán nguyên khối:**

```
I'll go first, to be fair. This channel's first video was read by my computer's built-in robot voice, dry as a station announcement, and the script was written in English and then bent into shape, so it never sounded like a person talking. I still wince at it. But if I'd waited until I could make a decent one, there'd be no videos at all. What did you make badly today?
```

**Vì sao không bỏ qua được:** khối cuối VD-018 nói thẳng *"Mình kể trước — có sẵn một cái
ghim trên đầu bình luận rồi đấy."* Bài đã lên sóng 19:30 ngày 16/08. Không có cái ghim thì
người xem bấm vào bình luận không thấy gì, thành ra video hứa một đằng thực tế một nẻo.

**Chỉ mỗi VD-018 cần việc này.** Chín bài đang chờ (VD-020 → VD-026) đều up-rồi-hẹn-giờ là
xong, không bài nào phải làm gì thêm. **Bài sau cũng sẽ không viết CTA kiểu cần ghim nữa** —
anh chốt 19/08 là quy trình chỉ nên có up và hẹn giờ.

**Ghim xong thì:** đánh dấu xong ở đây và xoá memory `viec-ghim-binh-luan-vd018.md`.

### VD-024 · VD-025 · VD-026 — viết mới ngày 19/08 · đợt hai trong cùng một ngày

Ba bài tiếp theo của hồ sơ `y-tuong-VD-021-030.md`, làm ngay sau đợt VD-022 · VD-023 ·
VD-021 trong cùng ngày. **Sáu bài một ngày là làm được** — đây là kỷ lục mới của kênh.

| Mã | Trụ | Chốt bài | CTA |
|---|---|---|---|
| VD-024 | 5 · Reaching people | Người đang đuối không mở lời xin đâu | Chọn sẵn một việc nhỏ rồi làm cho một người đang khó |
| VD-025 | 1 · Heavy days | Việc nào cũng có một bản nhỏ hơn | Hạ việc hôm nay xuống một nấc rồi làm bản nhỏ |
| VD-026 | 4 · Comparison | Tám mươi trang đó, đi tiếp hay bỏ thì cũng mất rồi | Gọi tên ở bình luận thứ mình đang theo vì lỡ rồi |

- **Thời lượng:** VD-024 86s (VI) · 75s (EN) · VD-025 84s · 82s · VD-026 85s · 81s.
- **Số thẻ ÷ số ảnh chia chẵn cả ba:** 21÷7 · 20÷10 · 18÷6. Ảnh rơi đúng nhóm ngay lần đầu.
- **Câu chốt đứng riêng một thẻ:** VD-024 thẻ 9 · VD-025 thẻ 7 · VD-026 thẻ 6.
- ⚠️ **VD-025 là bài dễ đụng VD-018 nhất trong cả kênh.** VD-018 nói *bản dở vẫn tính* —
  chuyện **chất lượng**; VD-025 nói **cỡ việc**: làm việc nhỏ hơn nhưng làm tử tế. Khối 10
  ("một vòng đi bộ vẫn là một vòng thật") là khối tách hai bài, bắt buộc giữ. **Cả bài
  VD-025 không được dùng chữ "bản dở"**, kể cả khi trả lời bình luận.
- ⚠️ **VD-026 phải giữ nguyên vế rào "chuyện lớn thì chưa bàn ở đây"** (khối 13) và hai
  khối 9–10 (*có thứ chán vẫn phải làm*). Bỏ đi là bài thành xúi bỏ học, bỏ việc — đúng rủi
  ro vòng chấm đã nêu. **Trả lời bình luận cũng không khuyên ai bỏ việc, bỏ học, bỏ hôn
  nhân**, kể cả khi bị hỏi thẳng.
- ⚠️ **CTA của VD-026 cố ý tránh khuôn "kể mình nghe một lần bạn…"** — VD-022 (22/08) đã
  dùng đúng khuôn đó và cũng là bài trụ 4. Hai bài cùng trụ mà lặp khuôn CTA thì lộ ngay.
- ⚠️ **VD-024 khối 2–3 phải đứng liền nhau** (*chính mình cũng đã im*) — thiếu chỗ đó thì
  khối 5 thành lời chê người xem. Khối 10 chặn cách hiểu "cứ tự tiện tới nhà người ta".
- ⚠️ **Cấm chữ theo từng bài:** VD-024 cấm "đồng hành · chữa lành · kết nối"; VD-025 cấm
  "kỷ luật · vượt qua chính mình · không có gì là không thể"; VD-026 cấm "buông bỏ · chữa
  lành · sống thật với chính mình".
- **Chấm ảnh — mấy ô phải né lần này:** ảnh shipper đeo khẩu trang (VD-024, nhìn ra dịch vụ
  giao hàng chứ không ra bạn bè); ảnh phòng gym kiểu quảng cáo (VD-025); ảnh chia tay đôi
  lứa (VD-026). Cộng thêm luật cũ: không đen trắng, không biển hiệu thương hiệu.
- ⚠️ **Chữ chưa ai đọc lại** — cả ba để trạng thái duyệt 🤖, rút lời đọc bằng `--cu-lam`.

### VD-022 · VD-023 · VD-021 — viết mới ngày 19/08 · ba bài trong một buổi

Ba bài đầu của hồ sơ `y-tuong-VD-021-030.md`. Viết mới hoàn toàn, đi trọn bảy bước, đăng
đủ **cả ba nơi**, không vướng gì về quyền.

| Mã | Trụ | Chốt bài | CTA |
|---|---|---|---|
| VD-022 | 4 · Comparison | Tới muộn hơn người ta không phải là không tới | Kể ở bình luận một việc làm muộn mà giờ thấy may là đã làm |
| VD-023 | 3 · What you already have | Cái gì thành hiển nhiên là do có người làm nó thành hiển nhiên | Nói với người nấu đúng một câu ngay tối nay |
| VD-021 | 2 · Small kindness | Tử tế lúc rảnh thì ai chả tử tế được | Làm một lần trong hôm nay vào lúc bất tiện nhất, rồi kể lại |

- ❗ **Thứ tự đăng đảo so với số hiệu, cố ý.** VD-020 (20/08) trụ 2, VD-021 cũng trụ 2 — để
  liền nhau là phạm luật trụ. Nên 22/08 là VD-022 (trụ 4), 24/08 là VD-023 (trụ 3), VD-021
  đẩy xuống 26/08. Chuỗi trụ: 2 → 4 → 3 → 2. Cùng cách xử lý như đợt VD-009 → VD-011 → VD-010.
- **Thời lượng:** VD-022 101s cả hai bản — **dài nhất từ trước tới nay** · VD-023 82s cả hai
  bản · VD-021 86s (VI) · 87s (EN). Cả ba đều 15 khối, không phải thêm khối nào.
- 📌 **Lấy số thẻ bằng `tach_the()` thay vì `--chi-do-dai`** — nhanh hơn ~5 phút mỗi bài, xem
  mục "Bảy bước". Chọn số ảnh chia chẵn cho số thẻ: VD-021 21÷7 · VD-022 24÷8 · VD-023 20÷10.
  **Ảnh rơi đúng nhóm cả ba bài ngay từ lần lấy đầu**, không phải đảo `--lay`.
- **Câu chốt đứng riêng một thẻ ở cả ba bài** — kiểm bằng log render: VD-021 thẻ 9 ·
  VD-022 thẻ 14 · VD-023 thẻ 8.
- **Nhịp CTA không lặp bài liền trước:** VD-020 hành động lần tới → VD-022 kể ở bình luận →
  VD-023 nói một câu ngay tối nay → VD-021 làm trong hôm nay rồi kể lại.
- ⚠️ **Mỗi bài có một khối chặn cách hiểu sai, bắt buộc giữ:** VD-022 khối 9 (không rủ buông
  xuôi — việc vẫn làm, chỉ bỏ đồng hồ của người khác); VD-023 khối 9–10 (không trách người
  ăn vô tâm); VD-021 khối 9 (không đòi lúc nào cũng sẵn sàng với mọi người).
- ⚠️ **VD-022 khối 12 phải đứng ngay sau khối 11** ("bốn năm đó" trỏ về bốn năm đại học);
  **VD-021 khối 7 chỉ chạy được nếu khối 8 đứng ngay sau** (một mình khối 7 nghe ra chê
  người xem).
- ⚠️ **Cấm chữ theo từng bài:** VD-022 cấm "thành công · chạm đỉnh · phiên bản tốt nhất của
  chính mình"; VD-023 cấm "biết ơn · trân trọng · biết đủ" (luật trụ 3, như VD-014 · VD-019);
  VD-021 cấm "lan toả · năng lượng tích cực · cho đi là còn mãi". Soi cả lời đọc, caption
  và **thẻ**.
- ⚠️ **VD-021 chỉ dùng thang máy ở khối 4 và 13, luôn là *cửa sắp đóng*** — VD-017 đã dùng
  cảnh *đứng chờ* thang máy. VD-027 trong hồ sơ cũng mở bằng cảnh chờ thang máy → xếp lịch
  phải để cách VD-021 thật xa.
- **Tách khỏi bài cũ dễ đụng:** VD-022 khác VD-006 (VD-006 so *thành tích*, VD-022 gỡ *mốc
  thời gian*; cả bài không có câu "đừng so với người khác"). VD-023 khác VD-004 (một câu
  khen tại mâm, không có chữ "cảm ơn", không dùng khung "…, vì…") và khác VD-014 · VD-019
  (hai bài kia nhìn *đồ vật*, bài này nhìn *con người* đứng sau). VD-021 khác VD-002 ·
  VD-011 · VD-012 · VD-020 — chiếm góc **thời điểm** của trụ 2.
- **Chấm ảnh:** loại thẳng ảnh đen trắng, ảnh đeo khẩu trang (làm bài dính mốc thời gian),
  ảnh có biển hiệu thương hiệu (`SUSHI TEI`, `TRAM Coffee & Tea`) và ảnh đồ ăn kiểu tạp chí
  bày trên nền trơn. Ảnh quán `XÔI CHÈ` thì giữ — chữ Việt, đúng chỗ muốn có.
- ⚠️ **Chữ chưa ai đọc lại** — cả ba để trạng thái duyệt 🤖, rút lời đọc bằng `--cu-lam`.
  Anh đọc phần "Từng khối" trong ba file `song-ngu/`, chưa ưng chỗ nào thì sửa, em render lại.

### VD-018 · VD-019 · VD-020 — viết mới ngày 15/08 · ba bài trong một buổi

Ba bài cuối của hồ sơ `y-tuong-VD-007-020.md`. Viết mới hoàn toàn, đi trọn bảy bước, đăng
đủ **cả ba nơi**. Giữa chừng vướng vụ mất quyền YouTube rồi tráo nhầm kênh — xem mục
"LẦN SAU VÀO THÌ LÀM TỪ ĐÂY".

| Mã | Trụ | Chốt bài | CTA |
|---|---|---|---|
| VD-018 | 1 · Heavy days | Bản dở là bản duy nhất có thật — và là bản duy nhất sửa được | **Kênh tự thú trước** rồi mời người xem kể (kiểu mới) |
| VD-019 | 3 · What you already have | Cái bạn đang chán, từng là cái bạn mơ | Ngẩng lên nhìn quanh ngay lúc xem, nói một câu với mình-hồi-đó |
| VD-020 | 2 · Small kindness | Nói "thôi khỏi" là giữ mất phần nhẹ của người ta | Lần tới có người ngỏ ý thì nói "ừ, giúp mình với" |

- **Thời lượng:** VD-018 97s (VI) · 104s (EN) — **dài nhất từ trước tới nay** · VD-019 82s ·
  89s · VD-020 86s · 82s. Cả ba đều 15 khối, ước 79–92 giây, render thật ra dài hơn ước —
  **không phải thêm khối nào**.
- ✅ **Ảnh rơi đúng nhóm ngay từ lần lấy đầu cả ba bài.** Cách làm ghi ở mục "Bảy bước":
  chạy `--chi-do-dai` lấy số thẻ trước, rồi chọn số ảnh chia chẵn cho số thẻ. Đây là lần
  đầu ba bài liền không phải đảo `--lay`.
- **Câu chốt đứng riêng một thẻ ở cả sáu file** (VI và EN) — kiểm bằng log render chứ không
  đoán: VD-018 thẻ 9 · VD-019 thẻ 7 · VD-020 thẻ 10. Đúng công thức VD-005 · VD-009 ·
  VD-016 · VD-017.
- **Xếp lịch không phạm luật trụ:** VD-017 trụ 3 → VD-018 trụ 1 → VD-019 trụ 3 → VD-020
  trụ 2. Kiểu CTA cũng khác nhau ba bài liền: kể ở bình luận → làm ngay lúc xem → hành động
  lần tới.
- ❗ **VD-018 phải ghim bình luận tự thú lúc bài lên sóng**, cả ba nơi. CTA kiểu mới này chỉ
  chạy nếu kênh kể trước. Câu soạn sẵn nằm trong hai file caption của bài.
- ⚠️ **VD-019 cấm chữ "biết ơn", "trân trọng", "biết đủ"** và **cấm kết "vậy nên đừng than
  nữa"** — vòng chấm dặn thẳng. Khối 9 và 10 (*cái chật vẫn chật, chán là chán thật*) là hai
  khối chặn, bỏ đi là bài thành giọng lên lớp. Thẻ đã soi lại cả hai thứ tiếng, sạch.
- ⚠️ **Mỗi bài có một khối chặn cách hiểu sai, bắt buộc giữ:** VD-018 khối 8 (không phải rủ
  làm ẩu — khối 9 mới nói lý do thật: bản dở **sửa được**); VD-019 khối 9–10 (không phải bảo
  thôi than); VD-020 khối 9 (không phải rủ đi nhờ vả tứ tung).
- ⚠️ **VD-020 khối 7 chỉ chạy được nếu khối 6 đứng ngay trước** — "phần nhẹ" trỏ về cảm giác
  nhẹ người ở khối 6. Đảo hai khối là câu chốt mất chỗ bám.
- **Tách khỏi bài cũ dễ đụng:** VD-018 khác VD-013 (VD-013 gỡ *cửa vào*, VD-018 gỡ *nỗi sợ
  kết quả xấu* — cả bài không nhắc mười phút hay chia nhỏ việc). VD-019 khác VD-014 (VD-014
  chạy trên trục tiếng động, VD-019 chạy trên trục thời gian, nhân vật là **mình của ngày
  trước**). VD-020 khác VD-011 · VD-012 — là bài đầu tiên của kênh đứng ở phía **mình nhận**,
  khép vòng trụ 2 với VD-002.
- ⚠️ **Chữ chưa ai đọc lại** — cả ba để trạng thái duyệt 🤖, rút lời đọc bằng `--cu-lam`.
  Anh đọc phần "Từng khối" trong ba file `song-ngu/`, chưa ưng chỗ nào thì sửa, em render lại.

### VD-017 — viết mới và đăng ngày 11/08 · bài đầu tiên theo nhịp 2 ngày

Xếp lần đầu vào 13/08 (tính từ VD-016 ngày 11/08), rồi anh dời cả hai sang **12/08 và
14/08** — neo lại vào VD-015 đã lên sóng ngày 10/08.

| Mã | Trụ | Chốt bài | CTA |
|---|---|---|---|
| VD-017 | 3 · What you already have | Cái ngứa ngáy lúc mới ngồi im mới là chỗ đáng để ý | Thử luôn trong lúc xem — năm phút, điện thoại úp xuống |

- **Thời lượng:** 94s cả hai bản — dài nhất từ trước tới nay. Tiếng −16,1 và −15,7 LUFS.
  15 khối, ước 86s, render thật ra 94s nên **không phải thêm khối nào**.
- **Hook không dùng câu hỏi như hồ sơ ý tưởng.** Hồ sơ chốt hook là *"lần cuối bạn ngồi im
  là bao giờ?"* — đã đẩy xuống khối 3 và đưa **cảnh chờ thang máy ba mươi giây** lên ba giây
  đầu. Câu hỏi bắt người xem *nhớ lại*, mà nhớ lại thì mất mấy giây — đúng mấy giây dễ mất
  người nhất. Cảnh thang máy nhận ra ngay, không phải nghĩ.
- **Khối 9 đứng riêng thẻ 14** — "Cái ngứa ngáy đó mới là chỗ đáng để ý", đúng công thức
  VD-005 · VD-009 · VD-016. Viết ngắn 38 ký tự cho chắc chắn không bị cắt đôi.
- **24 thẻ chia đúng 8 ảnh, mỗi ảnh 3 thẻ** — lần này ảnh rơi đúng nhóm ngay từ lần lấy đầu
  (`--lay 2,7,30,14,34,39,25,44`), không phải đảo thứ tự như VD-016. Biết trước số thẻ chia
  chẵn cho số ảnh thì xếp được ảnh theo nhóm ba thẻ ngay lúc chấm.
- ⚠️ **Chấm ảnh phải né hẳn ô "thiền"**: loại thẳng ảnh ngồi khoanh chân, thảm yoga, nến,
  nhang; chọn ghế, bàn, cửa sổ, điện thoại úp trên bàn. Cũng loại ảnh đen trắng (ứng viên
  4 · 11) và ảnh có biển hiệu thương hiệu (ứng viên 8 — `STARBUCKS`).
- ⚠️ **Hai khối chặn cách hiểu sai, bắt buộc giữ:** khối 7 ("không phải ngồi khoanh chân,
  không phải đếm hơi thở") chặn bài thành khẩu hiệu thiền — đúng rủi ro vòng chấm đã nêu;
  khối 13 ("không phải mẹo để xong rồi làm việc hăng hơn") chặn bài thành mẹo năng suất.
  Bỏ khối 13 là bài quay về coi mình như cái máy, trái hẳn thông điệp.
- ⚠️ **Cấm chữ "chánh niệm", "tĩnh tâm", "thiền định", "chữa lành"** — cả lời đọc, caption
  lẫn **thẻ**. Thẻ tiếng Việt các bài trước hay để "chữa lành", bài này đã bỏ.
- ⚠️ **Caption tiếng Anh bỏ câu "One video a day"**, đổi thành *"A new one every couple of
  days"* cho khớp nhịp mới. **Bài sau chép khuôn VD-017, đừng chép VD-016.**
- **Khác VD-013 (mười phút đầu tiên)** — hai bài dễ đụng nhau nhất: VD-013 gỡ cái cửa *bắt
  đầu* một việc; VD-017 nói về *dừng lại*, và năm phút ở đây không dẫn tới việc gì cả.
- ⚠️ **Chữ chưa ai đọc lại** — trạng thái duyệt để 🤖, rút lời đọc bằng `--cu-lam`.

### VD-016 — viết mới và đăng ngày 09/08

Bài đầu tiên **không còn nháp cũ, cũng không nằm trong lô nào** — viết một mình trong ngày
từ hồ sơ ý tưởng, đi trọn quy trình rồi hẹn giờ luôn.

| Mã | Trụ | Chốt bài | CTA |
|---|---|---|---|
| VD-016 | 5 · Reaching people | Câu hỏi đầu là lời chào đội dấu hỏi; câu thứ hai mới là câu quan tâm | Hỏi thêm đúng một câu với đúng một người, rồi kể ở bình luận |

- **Thời lượng:** 81s (VI) · 85s (EN) — đều trên mốc 60s. Tiếng −15,9 và −15,6 LUFS.
- **15 khối, không phải 13.** Bản 13 khối viết xong chỉ **ước 64 giây** — trên mốc nhưng sát
  mép, đúng kiểu VD-001 từng tụt xuống 59s. Thêm hai khối **có việc thật để làm**, không
  phải chèn cho dài:
  - **khối 4** — cảnh cụ thể duy nhất của bài (người ngồi cách hai mét ở chỗ làm); bản 13
    khối nói toàn ý chung, không có ai để người xem nghĩ tới.
  - **khối 11** — chặn cách hiểu sai nguy nhất: hỏi thêm một câu **không phải** đi moi
    chuyện. Khối 7 nêu nỗi sợ "chõ vào chuyện người ta" mà bản cũ không trả lời nỗi sợ đó.
- **Xếp lịch không phạm luật trụ:** VD-015 trụ 4 → VD-016 trụ 5. Kiểu CTA cũng khác bài
  liền trước (VD-015 viết một dòng → VD-016 kể chuyện ở bình luận).
- **Khối 8 đứng riêng một thẻ chữ** — câu "Ổn thật không đấy?" hiện to giữa màn hình, đúng
  công thức đã ăn ở VD-005 và VD-009. Đã kiểm bằng `--chi-do-dai`: nó là thẻ số 9, không
  dính khối nào.
- ⚠️ **VD-016 cấm chữ "kỹ năng", "lắng nghe chủ động", "thấu cảm"** — cả lời đọc, caption
  lẫn **thẻ**. Rút bài học VD-014: thẻ tiếng Việt các bài trước đều có `kỹ năng sống`, bài
  này đã bỏ; thẻ tiếng Anh không có `active listening` hay `empathy`.
- ✅ **Chỗ lệch ảnh — lần đầu vá được.** Lấy `--lay 4,28,30,16,…` thì ảnh văn phòng rơi trễ
  một nhịp, khối "người ngồi cách bạn hai mét ở chỗ làm" lại chạy trên ảnh khác. Đổi sang
  `--lay 4,30,28,16,25,27,19,13` rồi render lại là khớp. Máy **vẫn rải ảnh đều theo số thẻ,
  không hiểu nội dung** — nhưng chạy `--chi-do-dai` xem mỗi ảnh chiếm mấy thẻ rồi đảo thứ
  tự tay thì gắn được ảnh vào khối muốn. Rẻ hơn hẳn việc gắn từ khoá B-roll vào từng khối.
- ⚠️ **Chữ chưa ai đọc lại** — trạng thái duyệt để 🤖, rút lời đọc bằng `--cu-lam`.
  Anh đọc phần "Từng khối" trong `song-ngu/VD-016-song-ngu.md`, chưa ưng chỗ nào thì sửa,
  em render lại. Tám ảnh đã chấm tay, loại thẳng ảnh có biển hiệu chữ nước ngoài (ứng viên
  35), ảnh gần đen trắng (32 · 34 · 36), ảnh nền studio trơn dựng cảnh điện thoại bàn (7–12).

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
| **VD-020** | 🕒 đủ ba nơi, 19:30 ngày 20/08 |
| **VD-022** | 🕒 đủ ba nơi, 19:30 ngày 22/08 |
| **VD-023** | 🕒 đủ ba nơi, 19:30 ngày 24/08 |
| **VD-021** | 🕒 đủ ba nơi, 19:30 ngày 26/08 |
| **VD-024** | 🕒 đủ ba nơi, 19:30 ngày 28/08 |
| **VD-025** | 🕒 đủ ba nơi, 19:30 ngày 30/08 |
| **VD-026** | 🕒 đủ ba nơi, 19:30 ngày 01/09 |

VD-018 (16/08) và VD-019 (18/08) đã tự công khai đúng mốc — đọc API ngày 19/08 xác nhận
`publishedAt = 12:30Z` đúng ngày trên cả hai kênh. **VD-018 vẫn còn nợ cái ghim bình luận.**

**Thứ tự: VD-009 → VD-011 → VD-010 → VD-012 → VD-013 → VD-014 → VD-015** mỗi ngày một bài
tới 10/08, rồi theo nhịp 2 ngày: **VD-016 12/08 · VD-017 14/08 · VD-018 16/08 · VD-019
18/08 · VD-020 20/08**. VD-010 không được đứng liền sau VD-009, mà VD-011 · VD-012 cùng
trụ 2 nên cũng không được dính nhau — xếp kiểu này gỡ được cả hai.

🔻 **Hết bài sau 20/08.** VD-020 là bài cuối của hồ sơ `y-tuong-VD-007-020.md`. Mốc kế tiếp
là **19:30 ngày 22/08** và chưa có bài nào cho nó. Hàng đợi tiếp theo là **VD-021 → VD-030**
trong `content/ideas/y-tuong-VD-021-030.md` — đã có hồ sơ chi tiết và đã qua vòng chấm,
nhưng **chưa viết chữ nào**.

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
viết mới ngày 04/08, VD-014 · VD-015 ngày 06/08, VD-016 ngày 09/08, VD-017 ngày 11/08,
VD-018 · VD-019 · VD-020 ngày 15/08. Từ **VD-021 trở đi chỉ có hồ sơ ý tưởng, chưa có chữ
nào** — mỗi bài phải viết mới từ đầu.

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

### Làm tiếp theo thứ tự này (viết lại 15/08)

_(mục "viết VD-018" đã xong — VD-018 · VD-019 · VD-020 viết, render và đăng Facebook ngày
15/08, hẹn 16 · 18 · 20/08)_

1. **Ghim bình luận tự thú cho VD-018 lúc 19:30 ngày 16/08**, cả ba nơi — không thì CTA rỗng.
2. **Viết VD-021 trước 22/08.** Hồ sơ VD-021 → VD-030 đã có trong
   `content/ideas/y-tuong-VD-021-030.md` và đã qua vòng chấm, nhưng chưa có chữ nào. Đợt
   15/08 cho thấy **viết ba bài trong một buổi là làm được** — cứ làm theo lô cho đỡ vụn.
3. **Vào Studio xem VD-004 tiếng Việt** — chỉ 29 lượt trong khi mọi bài VI khác 500+.
   Nghi bị hạn chế hiển thị. Nhân tiện xem luôn vì sao cả 16 bài đều 0 bình luận.
4. **Lấy tỉ lệ xem hết.** Số lượt xem đã có (bảng ở mục "Chỗ nghẽn thật"), nhưng tỉ lệ
   xem hết — số YouTube thật sự chấm — thì API công khai không trả về. Phải qua YouTube
   Analytics API hoặc xem tay trong Studio, rồi điền vào `schedule/calendar.md`.
5. **Tìm hiểu vì sao kênh tiếng Anh không được đẩy** (130 lượt so với 5.971). Trước khi
   quyết có đầu tư tiếp cho kênh EN hay không.
6. Còn nợ cũ: **thêm lại link Facebook** vào mô tả 3 video đầu kênh Sống Tốt (mục dưới).

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
