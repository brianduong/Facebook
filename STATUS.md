# STATUS — Ghi chú tiến độ

_Cập nhật: 2026-07-25 (cuối ngày)_

## Chốt trong ngày 25/07
- **Nhịp đăng: mỗi ngày 1 video, 20:00** (đổi từ 2 video/tuần).
- **Không tự render trước** — chỉ render khi anh yêu cầu.
- **VD-001 đăng hôm nay, dạng video thường (post), không đăng Reel** vì file là 1:1, lên Reel bị cắt/viền.
- **Tạm gác token Facebook** — anh đăng tay. Script đã viết sẵn, khi nào cần thì dùng.
- Page ID `315460902683557` đã ghi trong `.env` (file này không lên GitHub).

## Đã xong ✅

**Nhận diện & Page**
- Icon + banner đã đổi trên Page. Bio đã dán ("🌱 Gieo một điều lành mỗi ngày…").
- Danh mục Page hiện là *Personal blog* → **nên đổi** sang Community / Media hoặc Video Creator.
- Phần mô tả dài trong `docs/mo-ta-page.md` chưa có chỗ dán ở giao diện Trang mới — không quan trọng.

**VD-001 — hoàn chỉnh, đã đăng**
`video/exports/VD-001-nhap.mp4` · 1080×1080 · 30fps · h264+AAC · 70,4s · 4,0 MB
- Nhân vật kể: **chị** · 3 cảnh: sáng cửa sổ → bàn trà → đường cây
- Giọng có ngữ điệu + hậu kỳ tiếng · nhạc nền gốc `nen-am-ap`
- Tiếng: −15,8 dB trung bình, đỉnh −0,8 dB (không vỡ), nhạc nằm dưới giọng 13 dB
- Độ sáng sau khi sửa: **131 / 133 / 147** trên 255 (bản đầu bị tối: 108 / 110 / 130)

**Nội dung đã có**
| Mã | Kịch bản | Lời đọc | Caption | Ảnh quote | Video |
|----|:--------:|:-------:|:-------:|:---------:|:-----:|
| VD-001 | ✅ | ✅ | ✅ | ✅ | ✅ đã đăng |
| VD-002 → VD-006 | ✅ | ✅ | ✅ | ✅ | ⬜ chưa render |
| VD-007 → VD-012 | ⬜ | ✅ | ⬜ | ⬜ | ⬜ |

**Công cụ (`scripts/`)** — xem bảng lệnh trong `README.md`
- `render-video-nhap.py` — render video 1:1 (nhân vật, cảnh, ngữ điệu, nhạc)
- `nhan_dien.py` · `nhan_vat.py` · `canh_nen.py` · `giong_doc.py` — màu/nhân vật/cảnh/ngữ điệu
- `tao-anh-quote.py` · `tao-nhac-nen.py` · `xem-thu.py` · `so-sanh-giong.py`
- `dang-video-fb.py` · `nhan-token.py` · `lay-token-dai-han.py` — đăng bài qua API (chưa dùng)

## Làm tiếp ngày mai (26/07) 👉
1. **Render VD-002** — "Tử tế không bao giờ là điều lãng phí", nhân vật **chú**, cảnh `ben-mua,duong-cay`, nhạc `nen-am-ap`:
   ```bash
   python3 scripts/render-video-nhap.py VD-002 --nhan-vat chu --canh ben-mua,duong-cay --nhac assets/music/nen-am-ap.m4a
   ```
2. Anh xem, duyệt rồi đăng dạng post kèm caption trong `content/captions/VD-002-caption.md`.

## Đang chờ anh trả lời
- **Bản dọc 9:16 cho Reels?** Reels được phân phối mạnh hơn video thường nhiều. Em sửa script xuất thêm bản dọc (cảnh cao hơn, nhân vật lớn hơn, vùng chữ dài hơn) → mỗi video có 2 bản.
- **Giọng đọc**: giọng máy có ngữ điệu này dùng tiếp, hay anh tự thu giọng? (Lời đọc sẵn ở `content/scripts/loi-doc/`.)
- **Số liệu VD-001** sau 24–48h → ghi vào `schedule/calendar.md`.
- **Ảnh chụp tab Monetization** → em lên lộ trình theo con số thật (đang ~9.9K followers).

## Thông tin nền
- Page: **Sống Tốt** — https://www.facebook.com/songtot.in
- Video: 1:1 (1080×1080), **trên 60 giây** để đủ tiêu chí quảng cáo trong luồng
- Kế hoạch: `PLAN.md` · Kiếm tiền: `docs/ke-hoach-kiem-tien.md` · Lịch: `schedule/calendar.md`
