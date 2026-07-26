# VD-000 — [Tên video]

- **Ngày viết:** YYYY-MM-DD
- **Thông điệp chính:** _(một câu)_
- **Thời lượng ước tính:** _(máy tính giúp khi chạy `--dong-bo`)_
- **Trạng thái duyệt:** ⬜ chờ anh review · ✅ đã duyệt → được render

> **Cách đọc file này.** Đọc phần **Đọc liền mạch** ngay dưới đây trước để soi nghĩa
> một lượt — EN và VI đầy đủ, đặt trên dưới nhau. Phần đó máy ghép, không sửa tay.
>
> Muốn sửa chữ thì xuống phần **Từng khối**. Khối **EN** là bản gốc để soi ý cho chặt;
> khối **VI** là bản **viết lại bằng tiếng Việt**, không phải dịch từng chữ — nên có chỗ
> câu VI ngắn hơn hoặc đổi hình ảnh so với EN, đó là cố ý.
> Sửa xong chạy `python3 scripts/tach-loi-doc.py VD-000 --dong-bo` để phần trên cập nhật theo.

---

_(Phần "Đọc liền mạch" sẽ tự hiện ra ở đây sau lần chạy `--dong-bo` đầu tiên.)_

---

## Từng khối — sửa ở đây

## 1 · Hook

**EN**
> …

**VI**
> …

---

## 2 · …

**EN**
> …

**VI**
> …

---

## Ghi chú cho anh khi review

_(Liệt kê những chỗ cố ý không dịch sát EN và lý do — để anh soi nhanh.)_

| Khối | EN | Dịch sát sẽ ra | Em viết thành | Vì sao |
|---|---|---|---|---|
|  |  |  |  |  |

---

## Sau khi anh duyệt

```bash
# Rút bản VI ra thành lời đọc cho máy render (đồng thời cập nhật phần đọc liền mạch)
python3 scripts/tach-loi-doc.py VD-000

# Rồi làm ảnh + render như bình thường
python3 scripts/tai-anh-pexels.py VD-000 --chon 6
.venv-tts/bin/python scripts/render-video-v2.py VD-000 --nhac assets/music/nen-am-ap.m4a
```
