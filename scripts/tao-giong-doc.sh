#!/bin/bash
# Tạo giọng đọc NHÁP tiếng Việt bằng giọng máy Linh của macOS.
#
# Dùng để: nghe thử nhịp kịch bản, đo thời lượng video trước khi thu giọng thật.
# KHÔNG nên dùng giọng máy này cho video đăng chính thức — giọng thật của anh
# luôn hiệu quả hơn với nội dung tâm tình.
#
#   ./scripts/tao-giong-doc.sh VD-001          # tốc độ mặc định 150 từ/phút
#   ./scripts/tao-giong-doc.sh VD-001 135      # đọc chậm hơn

set -euo pipefail

MA="${1:?Thiếu mã video, vd: ./scripts/tao-giong-doc.sh VD-001}"
TOCDO="${2:-150}"

GOC="$(cd "$(dirname "$0")/.." && pwd)"
VAO="$GOC/content/scripts/loi-doc/$MA-loi-doc.txt"
RA_DIR="$GOC/video/raw"
RA="$RA_DIR/$MA-giong-nhap.aiff"

[ -f "$VAO" ] || { echo "❌ Không thấy $VAO"; exit 1; }
mkdir -p "$RA_DIR"

say -v Linh -r "$TOCDO" -f "$VAO" -o "$RA"
echo "✅ $RA"

if command -v afinfo >/dev/null; then
  GIAY=$(afinfo "$RA" | awk -F': ' '/estimated duration/ {printf "%.0f", $2}')
  echo "⏱  Thời lượng: ${GIAY}s"
  if [ "$GIAY" -lt 60 ]; then
    echo "⚠️  Dưới 60s — video cần TRÊN 1 phút mới đủ tiêu chí quảng cáo trong luồng."
    echo "   Cách xử lý: đọc chậm hơn (tham số thứ 2), hoặc thêm khoảng lặng giữa các đoạn."
  fi
fi
