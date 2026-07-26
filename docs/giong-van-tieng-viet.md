# Viết lời đọc nghe ra tiếng Việt, không nghe ra bản dịch

Ghi lại sau khi VD-001 lên sóng và nhận góp ý: *"text dịch đủ nghĩa nhưng không phải đặc trưng tiếng Việt"*.

Vấn đề không nằm ở từ vựng — không có từ nào sai. Nó nằm ở **nhịp câu**. Câu viết ra
đúng ngữ pháp, đủ chủ–vị, mạch lạc như một bài giảng, và đó chính là chỗ hỏng: người
Việt **nói** không như vậy.

## Bốn lỗi hay gặp

### 1. Câu nào cũng đủ chủ ngữ – vị ngữ

Tiếng Anh bắt buộc có chủ ngữ, tiếng Việt thì không. Dịch sát khiến câu nào cũng
lù lù một chủ ngữ, nghe rất cứng.

| Nghe như dịch | Nghe như nói |
|---|---|
| Chúng ta thường bắt đầu ngày bằng một danh sách. | Sáng ra là đã thấy một đống việc. |
| Bạn nên thử điều này. | Thử cái này một hôm xem. |

### 2. Thiếu tiểu từ tình thái

*nhé · thôi · mà · đâu · đấy · chứ · cơ · đúng không* — đây là thứ làm câu tiếng Việt
có hơi người. Bỏ hết đi thì thành văn bản hành chính.

| Nghe như dịch | Nghe như nói |
|---|---|
| Chỉ ba mươi giây. | Ba mươi giây **thôi mà**. |
| Sáng mai hãy thử. | Sáng mai thử **nhé**. |
| Biết ơn không xoá được việc khó. | Biết ơn không làm việc khó biến mất **đâu**. |

### 3. Ẩn dụ mượn nguyên từ tiếng Anh

Đây là lỗi lộ nhất. Câu đúng nghĩa nhưng hình ảnh không phải của người Việt.

> ❌ "Bộ não được **mồi** bằng cái thiếu, nên cả ngày nó đi tìm cái thiếu."

*primed by lack* — mặc áo tiếng Việt nhưng vẫn là câu tiếng Anh. Người Việt nói thẳng:

> ✅ "Mình bắt đầu một ngày bằng danh sách những thứ mình còn thiếu. Rồi cả ngày cứ thế, đi tìm cái thiếu."

### 4. Ví dụ không có mùi Việt Nam

Ví dụ càng cụ thể và càng "ở đây" thì người xem càng thấy mình trong đó.

| Chung chung | Có mùi Việt Nam |
|---|---|
| Một bữa ăn đầy đủ | Một bữa cơm nóng tối qua |
| Một nơi trú ẩn an toàn | Một chỗ nằm khô ráo |
| Một người bạn đáng tin | Một người mà mình nhắn là chắc chắn có người trả lời |

## Cách kiểm nhanh trước khi render

1. **Đọc to lên.** Chỗ nào lưỡi vấp, chỗ đó là câu dịch.
2. **Đếm tiểu từ.** Cả bài mà không có lấy một chữ *nhé/thôi/mà/đâu* → chắc chắn còn cứng.
3. **Soi từng ẩn dụ.** Tự hỏi: người Việt có nói thế bao giờ chưa? Chưa thì bỏ.
4. **Câu dài quá 20 chữ** thì cắt đôi. Nói chuyện thì không ai thở dài như vậy.

## Quy ước xưng hô của kênh

- Gọi người xem là **bạn**, tự xưng là **mình** — thân nhưng không suồng sã.
- Không dùng "chúng ta" ở câu khuyên. "Chúng ta nên…" nghe như giáo viên;
  "Thử cái này xem…" nghe như người ngồi cạnh.
- Không lên gân, không giáo điều — đúng như ghi chú sản xuất trong mọi kịch bản.

## File mẫu

[VD-001-loi-doc-v2.txt](../content/scripts/loi-doc/VD-001-loi-doc-v2.txt) là bản viết
lại theo đúng những điều trên. Đặt cạnh
[VD-001-loi-doc.txt](../content/scripts/loi-doc/VD-001-loi-doc.txt) để so từng câu.

Từ VD-002 trở đi, viết thẳng theo lối này — đặt tên file `*-loi-doc.txt` như bình thường,
không cần hậu tố `-v2`.

## Quy trình duyệt chữ trước khi render (từ VD-003)

VD-002 đăng rồi vẫn còn chỗ nghe ra bản dịch. Nguyên nhân: chữ chỉ được đọc lại **sau khi
video đã dựng**, lúc đó ngại sửa. Nên tách hẳn khâu duyệt chữ ra trước.

Mỗi video có một file song ngữ: `content/scripts/song-ngu/VD-XXX-song-ngu.md`, gồm hai tầng:

1. **Đọc liền mạch** (đầu file) — toàn bộ EN rồi toàn bộ VI, để soi nghĩa một lượt xem
   cả bài có chạy không. Phần này **máy ghép từ các khối bên dưới**, không sửa tay:
   để hai bản chữ trong cùng một file mà sửa hai nơi thì sớm muộn cũng lệch nhau.
2. **Từng khối** — chỗ sửa thật, mỗi khối có **EN** và **VI** đặt cạnh nhau.

Sửa xong chạy `tach-loi-doc.py VD-XXX --dong-bo`, phần đọc liền mạch tự cập nhật theo.

- **EN** là bản gốc, dùng để soi ý cho chặt — mỗi khối phải nói được đúng một điều.
- **VI** **không phải bản dịch**. Đọc EN xong thì gấp lại, viết bằng tiếng Việt.
  Hai cột khớp ý, không khớp chữ. Chỗ nào cố dịch sát là chỗ đó hỏng.
- Cuối file ghi rõ những chỗ cố ý đi lệch khỏi EN và lý do, để người duyệt soi nhanh.

Anh sửa thẳng vào khối **VI**, đổi `Trạng thái duyệt` thành ✅, rồi:

```bash
python3 scripts/tach-loi-doc.py VD-XXX      # rút bản VI ra content/scripts/loi-doc/
```

Script sẽ **từ chối chạy** nếu chưa duyệt, và báo luôn thời lượng ước tính
(dưới 60 giây thì cảnh báo — Reels cần dài hơn). Không sửa tay file `*-loi-doc.txt`
nữa: nguồn duy nhất là file song ngữ, sửa tay sẽ bị ghi đè ở lần rút tiếp theo.
