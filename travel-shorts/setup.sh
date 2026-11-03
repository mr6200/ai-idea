#!/usr/bin/env bash
# 필요한 파이썬 패키지와 무료 한글 폰트(OFL)를 설치합니다. ffmpeg은 별도 설치 필요.
set -e
cd "$(dirname "$0")"
pip install -r requirements.txt
mkdir -p fonts
[ -f fonts/BlackHanSans-Regular.ttf ] || curl -fsSL -o fonts/BlackHanSans-Regular.ttf \
  "https://cdn.jsdelivr.net/gh/google/fonts@main/ofl/blackhansans/BlackHanSans-Regular.ttf"
[ -f fonts/NotoSansKR-VF.ttf ] || curl -fsSL -o fonts/NotoSansKR-VF.ttf \
  "https://cdn.jsdelivr.net/gh/google/fonts@main/ofl/notosanskr/NotoSansKR%5Bwght%5D.ttf"
command -v ffmpeg >/dev/null || echo "※ ffmpeg이 없습니다. https://ffmpeg.org 에서 설치하세요."
echo "준비 완료"
