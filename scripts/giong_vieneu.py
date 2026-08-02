"""Giọng nói tiếng Việt bằng VieNeu-TTS v3 Turbo (chạy offline trên máy).

Thay cho `say` của macOS (giọng Linh, 22 kHz, ghép âm đời cũ). VieNeu ra
48 kHz, có hơi thở và chỗ chùng giọng — nghe là **giọng nói**, không phải
giọng đọc. Tổng hợp nhanh hơn thời gian thực, không tốn token, không cần mạng
sau lần tải model đầu tiên.

⚠️ Phải chạy bằng Python của môi trường riêng, KHÔNG phải python3 hệ thống:

    .venv-tts/bin/python scripts/render-video-v2.py VD-001

(Lý do: onnxruntime chưa có bản cho Python 3.14 của máy, nên môi trường
`.venv-tts` dựng trên Python 3.13.)

Giọng có sẵn — xem đủ 14 giọng bằng:
    .venv-tts/bin/python scripts/thu-giong-vieneu.py --liet-ke


Về hậu kỳ tiếng
---------------
Bản cũ (`giong_doc.py`) chữa cháy cho giọng máy khô bằng echo + nâng 220 Hz +
nén mạnh, rồi chuẩn hoá độ to **từng câu một**. Bốn thứ đó cộng lại chính là
cái "nhão": echo 24 ms gây lược tần số làm tiếng rỗng, 220 Hz làm đục, nén
mạnh bẹp phụ âm, còn chuẩn hoá từng câu làm to nhỏ nhấp nhô.

Giọng VieNeu vốn đã dày và sạch nên ở đây làm ngược lại — đụng vào càng ít
càng tốt, và chỉ chuẩn hoá độ to **một lần** trên toàn bộ giọng đã ghép.
"""

from __future__ import annotations

import re
from pathlib import Path
from typing import Any

GIONG_MAC_DINH = "Phạm Tuyên"     # nam, giọng Bắc
KIEU_MAC_DINH = "doc_truyen"      # tu_nhien | tin_tuc | doc_truyen

# Hai cần gạt quyết định "giọng nói" hay "giọng đọc":
#   nhiet     — temperature của model. Thấp thì câu nào cũng một đường cao độ như
#               nhau, nghe ra người đọc thuộc lòng. Cao thì cao độ nhấp nhô hơn,
#               có nhấn có chùng. Cao quá thì bắt đầu vấp và đọc sai chữ.
#   im_lang   — xác suất chèn khoảng lặng. Cao hơn thì có chỗ ngắt để lấy hơi,
#               là thứ người nói có mà máy đọc thì không.
#
# Chọn bằng cách đo độ lệch chuẩn cao độ trên 16 cấu hình (scripts/so-ngu-dieu.py,
# chạy 27/07). Kết quả bất ngờ: kiểu **doc_truyen** cho ngữ điệu cao hơn tu_nhien
# tới 44% (F0 std 60,7 so với 42,2). Tên nghe như "giọng đọc" nhưng thực tế nó là
# lối kể chuyện — có nhấn có chùng; còn tu_nhien của VieNeu lại ra đều đều, đúng
# thứ anh chê là "giọng đọc chứ không phải giọng nói" ở VD-001.
#
# Giữ nhiệt ở mức mặc định 0.8: nhiệt cao hơn không cho thêm ngữ điệu (đo rồi) mà
# lại làm model vấp và đọc sai chữ. Chỉ nâng im_lang để có chỗ ngắt lấy hơi.
NHIET_MAC_DINH = 0.8

# Nâng 0.28 → 0.34 ngày 02/08 theo góp ý "chậm một chút và truyền cảm một chút".
# Khoảng lặng dài hơn cho câu có chỗ rơi, đó là thứ làm giọng bớt gấp.
IM_LANG_MAC_DINH = 0.34

# Làm chậm lại bao nhiêu phần. 1.0 là giữ nguyên, 1.09 là chậm hơn 9%.
#
# VieNeu không có tham số tốc độ nên phải làm ở khâu hậu kỳ bằng `atempo` —
# bộ lọc này đổi nhịp mà **không đổi cao độ**, nên giọng không bị trầm đi.
#
# Đặt 1.09 ngày 02/08 vì kiểu `doc_truyen` đọc 4,89 chữ/giây, nhanh hơn `tu_nhien`
# (4,28) tới 14% — được ngữ điệu nhưng mất nhịp thở. Chậm 9% kéo về khoảng
# 4,49 chữ/giây, vẫn nhanh hơn tu_nhien một chút nhưng đã có chỗ nghỉ.
#
# ⚠️ Đừng quá 1.15: atempo kéo xa quá thì tiếng bắt đầu nghe rỗng và ọc ạch.
# ⚠️ Đổi số này thì bài dài ra theo — nhớ đo lại `TOC_DO["VI"]` trong tach-loi-doc.py.
DO_CHAM_MAC_DINH = 1.09

# Lọc từng thẻ, phần dùng chung cho cả hai thứ tiếng: chỉ cắt ù trầm và ghìm đỉnh.
# Không echo, không nâng trung trầm, không chuẩn hoá độ to ở bước này.
LOC_TUNG_THE_CHUNG = (
    "highpass=f=70,"                                              # cắt ù trầm
    "acompressor=threshold=-20dB:ratio=2:attack=20:release=250"    # nén nhẹ cho đều
)

# Bản riêng cho tiếng Việt — có thêm khâu làm chậm.
# Tiếng Anh KHÔNG dùng chuỗi này: Piper đã chậm sẵn bằng length_scale 1.12,
# chồng thêm atempo nữa là thành giọng máy dạy học.
LOC_TUNG_THE = f"{LOC_TUNG_THE_CHUNG},atempo={1 / DO_CHAM_MAC_DINH:.4f}"

# Lọc một lần trên toàn bộ giọng đã ghép — đây mới là chỗ chuẩn hoá độ to.
LOC_TOAN_BAI = (
    "equalizer=f=3000:t=q:w=1.6:g=1.2,"       # rõ chữ, nhẹ tay
    "loudnorm=I=-16:TP=-1.5:LRA=11"           # độ to chuẩn cho mạng xã hội, chạy 1 lần
)


class Giong:
    """Bọc VieNeu lại cho gọn — nạp model một lần rồi đọc nhiều thẻ."""

    def __init__(self, ten_giong: str = GIONG_MAC_DINH, kieu: str = KIEU_MAC_DINH,
                 nhiet: float = NHIET_MAC_DINH,
                 im_lang: float = IM_LANG_MAC_DINH) -> None:
        from vieneu import Vieneu       # nạp trong hàm cho thông báo lỗi dễ hiểu hơn

        self.ten_giong = ten_giong
        self.kieu = kieu
        self.nhiet = nhiet
        self.im_lang = im_lang
        self._tts: Any = Vieneu()

        co_san = {ten for _, ten in self._tts.list_preset_voices()}
        if ten_giong not in co_san:
            raise SystemExit(
                f"❌ Không có giọng {ten_giong!r}.\n"
                f"   Giọng có sẵn: {', '.join(sorted(co_san))}"
            )

    @property
    def tan_so(self) -> int:
        return int(self._tts.sample_rate)

    def doc(self, chu: str, ra: Path) -> float:
        """Đọc một thẻ chữ ra file wav. Trả về thời lượng tính bằng giây."""
        am = self._tts.infer(lam_sach(chu), voice=self.ten_giong, style=self.kieu,
                             temperature=self.nhiet, silence_p=self.im_lang)
        self._tts.save(am, str(ra))
        return len(am) / self.tan_so

    def liet_ke(self) -> list[tuple[str, str]]:
        return list(self._tts.list_preset_voices())


def lam_sach(chu: str) -> str:
    """Dọn chữ trước khi đưa cho TTS.

    VieNeu đọc thẳng dấu câu tiếng Việt rất tốt, nên gần như không phải can
    thiệp — chỉ gộp khoảng trắng và đổi gạch dài thành dấu phẩy để nó ngắt hơi
    đúng chỗ thay vì đọc liền một hơi.
    """
    chu = " ".join(chu.split())
    chu = chu.replace(" — ", ", ").replace(" – ", ", ")
    return chu.strip()


def tach_cau(chu: str) -> list[str]:
    return [c.strip() for c in re.split(r"(?<=[.!?])\s+", " ".join(chu.split())) if c.strip()]
