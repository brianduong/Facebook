# Lịch đăng bài

> Cập nhật mỗi khi lên kế hoạch hoặc đăng xong. Đánh dấu ✅ khi đã đăng.
>
> **Nhịp cố định: 2 ngày 1 video lúc 19:30 giờ Việt Nam** (anh đổi ngày 11/08, trước đó
> là mỗi ngày 1 bài). **Neo chuỗi ngày vào bài đã lên sóng gần nhất**, không phải bài đã
> xếp lịch gần nhất: lấy ngày đó +2, +4, +6… Ví dụ 10/08 vừa lên → 12/08 · 14/08 · 16/08.
> Mốc tính ra mà đã trôi qua thì lấy 19:30 gần nhất còn ít nhất 10 phút, rồi lại cách 2 ngày.
> **Đổi nhịp thì dời cả lịch đang chờ**, không chỉ áp cho bài mới.
> Nhịp này cần ~15 video/tháng — em soạn trước theo lô, luân phiên
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
| **04/08** | **VD-009** | **Để mình nghĩ đã** | ✅ | ✅ | ✅ |
| 05/08 | VD-011 | Một việc tốt không ai biết | ✅ | ✅ | ✅ |
| 06/08 | VD-010 | Tha thứ không phải cho người kia | 🕒 | 🕒 | 🕒 19:30 |
| 07/08 | VD-012 | Người phục vụ mình cũng có tên | 🕒 | 🕒 | 🕒 19:30 |
| 08/08 | VD-013 | Mười phút đầu tiên | 🕒 | 🕒 | 🕒 19:30 |
| **09/08** | **VD-014** | **Những thứ hôm nay không hỏng** | 🕒 | 🕒 | 🕒 19:30 |
| **10/08** | **VD-015** | **Nói với mình như nói với bạn thân** | 🕒 | 🕒 | 🕒 19:30 |
| 11/08 | — | _để trống theo nhịp mới 2 ngày 1 bài_ | — | — | — |
| **12/08** | **VD-016** | **Hỏi thêm một câu** | ❗ còn 11/08 | ❗ còn 11/08 | 🕒 19:30 |
| 13/08 | — | _để trống theo nhịp mới_ | — | — | — |
| **14/08** | **VD-017** | **Ngồi im năm phút** | ❓ | ❓ | ✅ đã lên |
| 15/08 | — | _để trống theo nhịp 2 ngày_ | — | — | — |
| **16/08** | **VD-018** | **Làm dở vẫn tính** | ❗ mất quyền | ❗ mất quyền | 🕒 19:30 |
| 17/08 | — | _để trống theo nhịp 2 ngày_ | — | — | — |
| **18/08** | **VD-019** | **Mình của ngày trước từng mong điều này** | ❗ mất quyền | ❗ mất quyền | 🕒 19:30 |
| 19/08 | — | _để trống theo nhịp 2 ngày_ | — | — | — |
| **20/08** | **VD-020** | **Để người khác giúp mình** | ❗ mất quyền | ❗ mất quyền | 🕒 19:30 |

## 🔒 Chốt chặn lớn nhất lúc này (15/08) — mất quyền cả hai kênh YouTube

**Chưa xin lại quyền thì không đăng được gì lên YouTube, và cũng không đọc được API để
kiểm tra.** Đọc thử ngày 15/08, cả hai kênh đều trả về *chưa có quyền*:

- `secrets/youtube-token-vi.json` **không còn trên máy** — kênh tiếng Việt phải xin lại từ đầu.
- `secrets/youtube-token-en.json` còn đó nhưng lưu ngày 02/08, tức **trước** lúc thêm phạm vi
  `youtube` vào `PHAM_VI`. `google-auth` so phạm vi lúc nạp token, lệch là coi như chưa có
  quyền — nên token này cũng hỏng.

Hai dòng này **phải chạy tay, có mở trình duyệt và chọn đúng tài khoản của từng kênh**:

```bash
.venv-dang/bin/python scripts/dang-video-youtube.py xin-quyen --kenh vi
.venv-dang/bin/python scripts/dang-video-youtube.py xin-quyen --kenh en
```

Xong rồi mới chạy được sáu dòng đăng ở mục "Đợt đăng 15/08" bên dưới.

❗ **VD-016 và VD-017 trên YouTube coi như đã lệch một ngày so với Facebook.** Mốc
`publishAt` cũ của chúng là 11/08 và 13/08, cả hai đã trôi qua trong lúc còn kẹt quyền, mà
**công khai rồi thì không dời được nữa**. Theo đúng cách xử lý đã chốt: **để nguyên, đừng
gỡ** — gỡ rồi đăng lại là mất số liệu và ra hai bản trùng. Facebook giữ 12/08 và 14/08.
Chỗ lệch này chưa xác nhận lại bằng API được vì chưa có quyền; **xin quyền xong thì đọc
lại và sửa dấu ❓ ở hai dòng đó trong bảng trên**.

**Chú thích:** ⬜ Chưa render · 📝 Có lời đọc, chưa có caption/ảnh quote · 🟡 Đang làm · 🟢 Sẵn sàng / đang đăng · 🕒 Đã tải lên, hẹn giờ · ✅ Đã đăng · ❗ Bị bỏ sót · ❓ Chưa kiểm

## Nguyên tắc đăng (anh chốt 02/08)

- **2 ngày 1 bài** (đổi ngày 11/08; luật cũ là mỗi ngày 1 bài)
- **Đồng bộ cả ba nơi cùng ngày, cùng một bài** — đừng để nơi này đi trước nơi kia
- **Công khai lúc 19:30** giờ Việt Nam
- **Luôn đăng trước rồi đặt lịch**, không đăng đúng giờ, không để tự lên ngay
- Facebook phải dùng lệnh **`reels`**, không dùng `video`
- Khi có nhiều bài: **neo vào ngày bài đã lên sóng gần nhất**, cộng 2 · 4 · 6… ra chuỗi
  mốc 19:30 (mốc đã trôi qua thì lấy 19:30 gần nhất còn ít nhất 10 phút); các bài sau
  **cách nhau 2 ngày**, không tự đổi giờ
- **Đổi nhịp thì dời cả lịch đang chờ** cho khớp chuỗi mới, không chỉ áp cho bài mới
- Sau khi xếp xong phải đọc lại API, khớp **ngày + giờ + câu đầu caption**, và xóa ngay
  lịch trùng; không chỉ tin dòng báo thành công của script

Đã lên lịch tới hết **20/08** (VD-020). VD-018 · VD-019 · VD-020 viết mới, render và đăng
Facebook trong ngày 15/08; **hai kênh YouTube còn nợ, chờ xin lại quyền** (mục trên).

🔻 **VD-020 là bài cuối của hồ sơ `y-tuong-VD-007-020.md`.** Sau nó, mốc kế tiếp là **22/08**
và **chưa có bài nào cho mốc đó**. Hàng đợi tiếp theo là VD-021 → VD-030 trong
`content/ideas/y-tuong-VD-021-030.md` — có hồ sơ ý tưởng và đã qua vòng chấm, nhưng
**chưa viết chữ nào**. Bảy bước của một bài ghi trong `STATUS.md`.

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

## Đợt đăng 06/08 — VD-014 và VD-015 lên cả ba nơi

Hai bài viết mới trong ngày 06/08 (từ VD-014 trở đi không còn nháp cũ, viết mới từ đầu).
Xếp vào **hai mốc 19:30 còn trống gần nhất** — 06/07/08 đã có bài rồi nên bài đầu rơi vào
09/08, đúng luật "19:30 gần nhất còn trống".

| Ngày 19:30 | Mã | YouTube tiếng Việt | YouTube tiếng Anh | Facebook Reels (post id) |
|---|---|---|---|---|
| **09/08** | **VD-014** | https://youtu.be/y6FLC-NdpwQ | https://youtu.be/Of0VLegiUvQ | `944174878692756` (`…_1661784295515307`) |
| **10/08** | **VD-015** | https://youtu.be/UbdSj9x9bFg | https://youtu.be/aDd1IUzvab0 | `2328234654652391` (`…_1661784848848585`) |

**Đã đọc lại API cả ba nơi ngay sau khi đăng:** hai kênh YouTube đều **15 video, khớp đủ
VD-001 → VD-015**, không trùng không thiếu; bốn bài chờ đều `publishAt = 12:30Z` đúng ngày.
Facebook có **đúng 5 lịch**, mỗi ngày một bài từ 06/08 đến 10/08, không trùng giờ, cả hai
bài mới đều `publish_status = scheduled` và permalink trả về `/reel/…`.

⏳ **Lại gặp đúng độ trễ đã ghi:** VD-015 vừa đăng xong thì `/scheduled_posts` chỉ hiện 4
bài. Tra thẳng `/{video-id}` thì đã `scheduled` đúng mốc; một phút sau danh sách hiện đủ 5.
**Đừng đăng lại khi chưa thấy trong danh sách.**

⚠️ Thẻ tiếng Anh của VD-014 lúc đầu có `quiet gratitude` — trái luật "cấm chữ biết ơn" của
chính bài. Đã đổi trước khi đăng. Bài trụ 3 sau này soi lại thẻ, không chỉ soi lời đọc.

## Đợt đăng 15/08 — VD-018 · VD-019 · VD-020 · **Facebook xong, YouTube còn nợ**

Ba bài viết mới hoàn toàn trong ngày 15/08 từ hồ sơ ý tưởng, đi trọn bảy bước. Neo chuỗi
vào **VD-017 đã lên sóng 14/08** → 16/08 · 18/08 · 20/08, đúng nhịp 2 ngày.

| Ngày 19:30 | Mã | Trụ | Facebook Reels (post id) | YouTube |
|---|---|---|---|---|
| **16/08** | **VD-018** · Làm dở vẫn tính | 1 | `1086214770915645` (`…_1668958004797936`) | ❗ chưa đăng |
| **18/08** | **VD-019** · Mình của ngày trước từng mong điều này | 3 | `4372283653084479` (`…_1668963278130742`) | ❗ chưa đăng |
| **20/08** | **VD-020** · Để người khác giúp mình | 2 | `2324658331612348` (`…_1668963804797356`) | ❗ chưa đăng |

**Đã đọc lại API Facebook ngay sau khi đăng:** cả ba đều `published = false` với
`scheduled_publish_time` đúng `12:30Z` ngày của nó (= 19:30 giờ VN), `permalink_url` trả về
`/reel/…` nên chắc chắn là Reels, `length` khớp file đã render (97,27 · 81,83 · 85,86 giây).
Edge `/scheduled_posts` có **đúng 3 lịch chờ, không trùng**, ba mốc cách nhau tròn 172.800
giây = 2 ngày. Lại gặp đúng độ trễ đã ghi: `/video_reels` chưa hiện ba bài mới ngay, tra
thẳng `/{video-id}` thì đã `scheduled` đúng mốc — **đừng đăng lại**.

**Sáu dòng còn nợ trên YouTube.** Chạy `xin-quyen` cả hai kênh trước (mục 🔒 ở trên), rồi:

```bash
.venv-dang/bin/python scripts/dang-video-youtube.py dang VD-018 --kenh vi \
    --hen-gio 2026-08-16T19:30:00+07:00 --dang-that      # rồi --kenh en
.venv-dang/bin/python scripts/dang-video-youtube.py dang VD-019 --kenh vi \
    --hen-gio 2026-08-18T19:30:00+07:00 --dang-that      # rồi --kenh en
.venv-dang/bin/python scripts/dang-video-youtube.py dang VD-020 --kenh vi \
    --hen-gio 2026-08-20T19:30:00+07:00 --dang-that      # rồi --kenh en
```

⚠️ **Nếu để trôi qua 19:30 ngày 16/08 mới xin được quyền** thì đừng chép cứng ba mốc trên.
Facebook đã lên sóng bài nào rồi thì **để nguyên, chấp nhận lệch** như VD-016 · VD-017; các
bài còn lại tính lại từ 19:30 gần nhất còn ít nhất 10 phút, rồi cách 2 ngày.

- **Thời lượng:** VD-018 97s (VI) · 104s (EN) — dài nhất từ trước tới nay · VD-019 82s ·
  89s · VD-020 86s · 82s. Cả ba đều 15 khối, không phải thêm khối nào.
- ✅ **Ảnh rơi đúng nhóm ngay từ lần lấy đầu cả ba bài**, không phải đảo `--lay` như VD-016.
  Cách làm: chạy `--chi-do-dai` lấy số thẻ trước, rồi chọn số ảnh **chia chẵn cho số thẻ** —
  VD-019 18 thẻ ÷ 6 ảnh = đúng 3 thẻ mỗi ảnh. VD-018 (25 thẻ ÷ 8) và VD-020 (22 thẻ ÷ 8)
  chia lẻ nhưng vẫn xếp được vì biết trước nhóm nào dài mấy thẻ.
- **Câu chốt của cả ba bài đứng riêng một thẻ**, cả bản VI lẫn bản EN — đã kiểm bằng log
  render, không phải đoán: VD-018 thẻ 9 · VD-019 thẻ 7 · VD-020 thẻ 10.
- ❗ **VD-018 có CTA kiểu mới — kênh tự thú trước.** Bài lên sóng thì **phải ghim ngay bình
  luận tự thú**, cả ba nơi, không thì CTA rỗng. Câu soạn sẵn nằm trong
  `content/captions/VD-018-caption.md` và bản EN trong `VD-018-caption-en.md`.
- ⚠️ **VD-019 cấm chữ "biết ơn", "trân trọng", "biết đủ"** và **cấm kết "vậy nên đừng than
  nữa"** — vòng chấm ý tưởng dặn thẳng. Thẻ đã soi lại cả hai thứ tiếng, sạch.
- **Xếp lịch không phạm luật trụ:** VD-017 trụ 3 → VD-018 trụ 1 → VD-019 trụ 3 → VD-020
  trụ 2. Kiểu CTA cũng khác nhau ba bài liền: kể ở bình luận → làm ngay lúc xem → hành
  động lần tới.

## Đợt đăng 11/08 — VD-017 lên cả ba nơi · **bài đầu tiên theo nhịp 2 ngày**

Viết mới hoàn toàn trong ngày 11/08 từ hồ sơ ý tưởng (*Ngồi im năm phút*, trụ 3). Đây là
bài đầu tiên xếp theo nhịp mới. Xếp lần đầu vào 13/08 (tính từ VD-016 ngày 11/08), rồi
anh dời cả VD-016 lẫn VD-017 sang **12/08 và 14/08** — neo lại vào VD-015 đã lên sóng
ngày 10/08. Ngày 11 và 13/08 để trống, không phải quên.

| Ngày 19:30 | Mã | YouTube tiếng Việt | YouTube tiếng Anh | Facebook Reels (post id) |
|---|---|---|---|---|
| **14/08** | **VD-017** | https://youtu.be/gSRZoHt2Qns | https://youtu.be/xfpddU0eEAI | `2274455883304906` (`…_1665772108449859`) |

**Đã đọc lại API cả ba nơi ngay sau khi đăng:** hai kênh YouTube đều **17 video, khớp đủ
VD-001 → VD-017**, không trùng không thiếu; VD-016 và VD-017 đều còn `private` với
`publishAt = 12:30Z` đúng ngày của nó (lúc đó là 11 và 13/08). Facebook có **đúng 2 lịch
chờ**, không trùng giờ; `permalink_url` trả về
`/reel/2274455883304906/` nên chắc chắn là Reels, `length = 93,725` giây khớp file đã render.

- **Thời lượng:** 94s cả hai bản (VI và EN) — dài nhất từ trước tới nay. Tiếng −16,1 và
  −15,7 LUFS. Bản 15 khối ước 86s, render thật ra 94s nên **không phải thêm khối nào**.
- **Khối 9 đứng riêng thẻ 14** — "Cái ngứa ngáy đó mới là chỗ đáng để ý" hiện to giữa màn
  hình, đúng công thức VD-005 · VD-009 · VD-016. Kiểm bằng `--chi-do-dai` trước khi render.
- **24 thẻ chia đúng 8 ảnh, mỗi ảnh 3 thẻ** — lần này không phải đảo thứ tự `--lay` như
  VD-016, ảnh rơi đúng nhóm ngay từ lần lấy đầu (`--lay 2,7,30,14,34,39,25,44`).
- ⚠️ **Chấm ảnh phải né hẳn ô "thiền":** loại thẳng ảnh ngồi khoanh chân, thảm yoga, nến,
  nhang — chọn ghế, bàn, cửa sổ, điện thoại úp trên bàn. Cũng loại ảnh đen trắng (ứng viên
  4 · 11) và ảnh có biển hiệu thương hiệu (ứng viên 8 — `STARBUCKS`).
- ⚠️ **Caption tiếng Anh đã bỏ câu "One video a day"** ở cuối mô tả, đổi thành *"A new one
  every couple of days"* cho khớp nhịp mới. **Bài sau chép khuôn VD-017, đừng chép VD-016**
  — khuôn cũ còn hứa mỗi ngày một video.
- ⚠️ **Cấm chữ "chánh niệm", "tĩnh tâm", "thiền định", "chữa lành"** — cả lời đọc, caption
  lẫn thẻ. Thẻ tiếng Việt các bài trước hay để "chữa lành", bài này đã bỏ.

## Đợt đăng 09/08 — VD-016 lên cả ba nơi

Viết mới hoàn toàn trong ngày 09/08 từ hồ sơ ý tưởng (*Hỏi thêm một câu*, trụ 5). Xếp vào
**19:30 gần nhất còn trống** — 09/08 và 10/08 đã có VD-014 · VD-015 nên rơi vào **11/08**.

| Ngày 19:30 | Mã | YouTube tiếng Việt | YouTube tiếng Anh | Facebook Reels (post id) |
|---|---|---|---|---|
| **11/08** | **VD-016** | https://youtu.be/-QPXDUMNjeA | https://youtu.be/JuyV6yuT4O8 | `1597246682117680` (`…_1664407845252952`) |

**Đã đọc lại API cả ba nơi ngay sau khi đăng:** hai kênh YouTube đều **16 video, khớp đủ
VD-001 → VD-016**, không trùng không thiếu; ba bài chờ đều `private` với `publishAt` đúng
ngày của nó (09, 10, 11/08 — cùng mốc `12:30Z`). Facebook có **đúng 3 lịch**, mỗi ngày một
bài từ 09/08 đến 11/08, không trùng giờ; `permalink_url` trả về `/reel/1597246682117680/`
nên chắc chắn là Reels, `length = 81,076` giây khớp file đã render.

⏳ Lần này `/scheduled_posts` **hiện đủ ngay**, không gặp độ trễ một phút như VD-013 và
VD-015. Nhưng luật vẫn giữ: chưa thấy trong danh sách thì tra `/{video-id}` trước, đừng đăng lại.

📌 **Đảo thứ tự ảnh để ảnh rơi đúng khối.** Lần lấy đầu (`--lay 4,28,30,16,…`) làm ảnh văn
phòng rơi trễ một nhịp, khối "người ngồi cách bạn hai mét ở chỗ làm" lại chạy trên ảnh khác.
Đổi sang `--lay 4,30,28,16,25,27,19,13` rồi render lại là khớp. **Máy vẫn rải ảnh đều theo
số thẻ, không hiểu nội dung** — nhưng biết số thẻ mỗi ảnh chiếm thì đảo thứ tự tay được.
Đây là cách vá rẻ nhất cho chỗ lệch cũ, chưa cần gắn từ khoá B-roll vào từng khối.

⚠️ **Bản 13 khối đầu tiên chỉ ước 64 giây** — trên mốc 60 nhưng sát mép, đúng kiểu VD-001
từng tụt xuống 59s. Thêm hai khối **có việc thật để làm** (khối 4 cảnh cụ thể ở chỗ làm,
khối 11 chặn cách hiểu "hỏi thêm là đi moi chuyện") thành 15 khối → **81 giây thật**.
Đừng chèn khối rỗng cho đủ mốc; tìm chỗ bài đang thiếu rồi bù vào đó.

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
