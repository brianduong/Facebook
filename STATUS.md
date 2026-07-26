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

## Quy trình mới

```bash
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
| VD-002 | ✅ | ✅ **đã viết lại** | ✅ **đã viết lại** | ✅ | 🟢 **đã render 63s — sẵn sàng đăng** |
| VD-003 → VD-006 | ✅ | ⚠️ cần viết lại theo văn nói | ✅ | ✅ | ⬜ chưa render |
| VD-007 → VD-012 | ⬜ | ⚠️ như trên | ⬜ | ⬜ | ⬜ |

**Công cụ mới (`scripts/`)**
- `tai-anh-pexels.py` — tải ảnh thật theo từ khoá B-roll ghi trong kịch bản
- `giong_vieneu.py` — giọng VieNeu + chuỗi hậu kỳ tiếng đã sửa
- `khung_reels.py` — lớp chữ trong suốt 9:16, đè lên ảnh
- `render-video-v2.py` — render Reels hoàn chỉnh
- `thu-giong-vieneu.py` — nghe thử giọng

**Công cụ cũ** (`render-video-nhap.py`, `nhan_vat.py`, `canh_nen.py`, `giong_doc.py`)
vẫn giữ để đối chiếu, **không dùng nữa**.

## Làm tiếp 👉

1. **Anh xem VD-002** (`video/exports/VD-002-reels.mp4`) rồi duyệt → đăng dạng Reels
   tối nay 20:00 kèm caption trong `content/captions/VD-002-caption.md`.
2. **Anh nghe 3 giọng** trong `video/thu-giong/` rồi chốt giọng cho kênh.
3. Render lại VD-001 bằng ảnh thật → đăng lại dạng Reels (bản 1:1 cũ để nguyên trên Page).
4. Viết lại lời đọc VD-003 → VD-006 theo `docs/giong-van-tieng-viet.md`.

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
