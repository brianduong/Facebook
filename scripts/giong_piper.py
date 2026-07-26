"""Giọng nói tiếng Anh bằng Piper TTS (chạy offline trên máy).

Đây là bản tiếng Anh của `giong_vieneu.py`, cùng một giao diện (`Giong.doc()`,
`Giong.tan_so`) để `render-video-v2.py` thay giọng mà không phải sửa gì thêm.

Vì sao Piper chứ không phải `say` của macOS: `say` là TTS ghép âm đời cũ, đã
chứng minh là hỏng ở VD-001 (xem STATUS.md). Piper chạy trên **onnxruntime** —
đúng thư viện VieNeu đang dùng — nên không phải dựng thêm môi trường nào.
Tải model một lần rồi chạy offline mãi, không tốn token, không cần mạng.

⚠️ Phải chạy bằng Python của môi trường TTS:

    .venv-tts/bin/python scripts/thu-giong-piper.py

Model nằm ở `.piper-voices/` (ngoài GitHub). Tải thêm giọng:

    .venv-tts/bin/python -m piper.download_voices --data-dir .piper-voices en_GB-alba-medium


Về tốc độ đọc
-------------
Kênh One Small Thing nhắm người đang **học tiếng Anh** là chính, nên đọc chậm
hơn người bản ngữ một chút — `do_cham` (length_scale của Piper) mặc định 1.12,
tức chậm hơn khoảng 12%. Đừng đẩy quá 1.25: chậm quá thì nghe ra giọng máy dạy
học, mất hết cái ấm mà kênh cần.
"""

from __future__ import annotations

import re
import wave
from pathlib import Path
from typing import Any

# Chuỗi hậu kỳ tiếng dùng chung với bản tiếng Việt — lý do chọn từng bộ lọc ghi
# trong giong_vieneu.py, không chép lại ở đây.
from giong_vieneu import LOC_TOAN_BAI, LOC_TUNG_THE  # noqa: F401

REPO = Path(__file__).resolve().parent.parent
KHO_GIONG = REPO / ".piper-voices"

GIONG_MAC_DINH = "en_US-ryan-high"   # nam, Mỹ, ấm và chậm rãi
DO_CHAM_MAC_DINH = 1.12              # >1 là chậm lại; xem ghi chú đầu file


class Giong:
    """Bọc Piper lại cho gọn — nạp model một lần rồi đọc nhiều thẻ."""

    def __init__(self, ten_giong: str = GIONG_MAC_DINH,
                 do_cham: float = DO_CHAM_MAC_DINH) -> None:
        from piper import PiperVoice
        from piper.config import SynthesisConfig

        duong_dan = KHO_GIONG / f"{ten_giong}.onnx"
        if not duong_dan.exists():
            raise SystemExit(
                f"❌ Chưa có giọng {ten_giong!r} ở {KHO_GIONG.name}/.\n"
                f"   Tải về:  .venv-tts/bin/python -m piper.download_voices "
                f"--data-dir .piper-voices {ten_giong}\n"
                f"   Đang có: {', '.join(liet_ke()) or '(chưa có giọng nào)'}"
            )

        self.ten_giong = ten_giong
        self.do_cham = do_cham
        self._tts: Any = PiperVoice.load(str(duong_dan))
        self._cau_hinh = SynthesisConfig(length_scale=do_cham)

    @property
    def tan_so(self) -> int:
        return int(self._tts.config.sample_rate)

    def doc(self, chu: str, ra: Path) -> float:
        """Đọc một thẻ chữ ra file wav. Trả về thời lượng tính bằng giây."""
        with wave.open(str(ra), "wb") as f:
            self._tts.synthesize_wav(lam_sach(chu), f, syn_config=self._cau_hinh)
        with wave.open(str(ra), "rb") as f:
            return f.getnframes() / f.getframerate()


def liet_ke() -> list[str]:
    """Tên các giọng đã tải về máy."""
    return sorted(p.stem for p in KHO_GIONG.glob("*.onnx")) if KHO_GIONG.exists() else []


def lam_sach(chu: str) -> str:
    """Dọn chữ trước khi đưa cho Piper.

    Piper đọc gạch dài và dấu ngoặc kép cong rất tệ — nó hoặc đọc thành tên dấu,
    hoặc nuốt luôn chỗ ngắt. Đổi hết về dấu câu thường để nó ngắt hơi đúng chỗ.
    """
    chu = " ".join(chu.split())
    chu = chu.replace(" — ", ", ").replace(" – ", ", ").replace("—", ", ")
    chu = chu.replace("“", '"').replace("”", '"')      # ngoặc kép cong
    chu = chu.replace("‘", "'").replace("’", "'")      # nháy đơn cong
    return chu.strip()


def tach_cau(chu: str) -> list[str]:
    return [c.strip() for c in re.split(r"(?<=[.!?])\s+", " ".join(chu.split())) if c.strip()]
