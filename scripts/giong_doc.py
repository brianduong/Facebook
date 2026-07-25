"""Làm giọng đọc máy nghe truyền cảm hơn — ngữ điệu lên xuống, ngắt nghỉ, hậu kỳ tiếng.

Giọng Linh của macOS nhận được các lệnh nhúng sau (đã thử trên máy, chạy thật):

    [[pbas N]]   cao độ nền — N nhỏ = giọng trầm, N lớn = giọng cao
    [[pmod N]]   độ lên xuống của giọng — N lớn = ngữ điệu nhiều, đỡ đều đều
    [[rate N]]   tốc độ (từ/phút)
    [[slnc N]]   im lặng N mili-giây
    [[volm x]]   âm lượng 0–1

⚠️ Phải viết **mỗi lệnh một cặp ngoặc**. Viết gộp kiểu `[[pbas 52 rate 145]]`
thì giọng đọc luôn cả chữ "rate 145" ra thành tiếng (đã thử: câu 4 giây phình
thành 7 giây).

Cách làm truyền cảm ở đây gồm hai lớp:
1. **Ngữ điệu theo loại câu** — câu hỏi thì nhấc giọng lên, câu chốt thì hạ
   giọng và đọc chậm lại, câu liệt kê ngắn thì đi nhanh hơn, và cao độ nhích
   lên xuống giữa các câu cho khỏi ru ngủ.
2. **Hậu kỳ tiếng** — lọc ù, thêm ấm ở dải 220Hz, rõ ở 3.2kHz, nén động cho
   đều, chút vang phòng rất nhẹ, cuối cùng chuẩn hoá độ to.
"""

from __future__ import annotations

import re

# Chuỗi lọc âm cho ffmpeg — giọng máy khô và mỏng, cần ấm và dày hơn
LOC_AM = (
    "highpass=f=85,"                                             # bỏ ù trầm
    "equalizer=f=220:t=q:w=1.2:g=2.6,"                            # thêm ấm
    "equalizer=f=3200:t=q:w=1.4:g=1.8,"                           # thêm rõ chữ
    "acompressor=threshold=-18dB:ratio=3:attack=12:release=180,"  # nén cho đều
    "aecho=0.9:0.65:24:0.07,"                                     # vang phòng rất nhẹ
    "loudnorm=I=-16:TP=-1.5:LRA=11"                               # độ to chuẩn cho mạng xã hội
)


def _tach_cau(text: str) -> list[str]:
    return [c.strip() for c in re.split(r"(?<=[.!?])\s+", " ".join(text.split())) if c.strip()]


def soan_ngu_dieu(doan: str, toc_do: int, la_the_dau: bool = False,
                  la_the_cuoi: bool = False) -> str:
    """Chuyển một thẻ chữ thành lời đọc có ngữ điệu cho `say`.

    doan        : nội dung thẻ (một hoặc vài câu)
    toc_do      : tốc độ nền, từ/phút
    la_the_dau  : thẻ mở đầu (câu hook) — cần chậm và rõ, nghỉ dài sau đó
    la_the_cuoi : thẻ kết — hạ giọng, đọc chậm, nghe như chốt lại
    """
    cau = _tach_cau(doan)
    ra: list[str] = []

    for i, c in enumerate(cau):
        cuoi_doan = i == len(cau) - 1

        if c.endswith("?"):
            # Câu hỏi: nhấc giọng, ngữ điệu rộng, chậm hơn chút cho người xem kịp nghĩ
            pbas, pmod, rate, nghi = 55, 94, toc_do - 8, 460
        elif la_the_cuoi and cuoi_doan:
            # Câu chốt cuối video: trầm xuống, chậm lại — chỗ này quyết định cảm giác đọng lại
            pbas, pmod, rate, nghi = 43, 76, toc_do - 18, 320
        elif len(c) < 45:
            # Câu ngắn, thường là liệt kê hoặc nhấn: đi nhanh hơn, nghỉ ngắn
            pbas, pmod, rate, nghi = 51, 84, toc_do + 8, 240
        else:
            # Câu kể thường: nhích cao độ lên xuống theo thứ tự câu cho đỡ đều đều
            pbas, pmod, rate, nghi = (49 if i % 2 == 0 else 46), 74, toc_do, 300

        if la_the_dau and cuoi_doan:
            nghi = 520          # nghỉ dài sau hook để câu mở đầu có chỗ lắng

        # Ngắt nhẹ ở dấu phẩy và gạch ngang cho câu có nhịp
        c = c.replace(", ", ", [[slnc 130]] ").replace(" — ", " [[slnc 200]] ")

        ra.append(f"[[pbas {pbas}]] [[pmod {pmod}]] [[rate {rate}]] {c} [[slnc {nghi}]]")

    return " ".join(ra)
