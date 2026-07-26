# STATUS — Ghi chú tiến độ

_Cập nhật: 2026-07-26_

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

**Chờ anh:** nghe 4 giọng rồi chốt · giữ chỗ handle `@onesmallthing`

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
3. **Giữ chỗ handle**: `@songtot.in` trên YouTube/TikTok/Instagram, `@onesmallthing`
   trên YouTube. Chưa đăng gì cũng cứ giữ — mất tên là mất hẳn.
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
