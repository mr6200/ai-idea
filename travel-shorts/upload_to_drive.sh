#!/usr/bin/env bash
# 완성된 영상(mp4)과 업로드 정보(txt)를 구글 드라이브 폴더에 올립니다.
#
# 준비: 환경 변수 GDRIVE_TOKEN 에 `rclone authorize "drive"` 로 받은 토큰(JSON)을 넣어두세요.
# usage: ./upload_to_drive.sh projects/<name> "드라이브 폴더 이름"
set -euo pipefail
cd "$(dirname "$0")"

PROJECT="${1:?usage: ./upload_to_drive.sh projects/<name> \"드라이브 폴더 이름\"}"
FOLDER="${2:-유튜브 쇼츠 - $(basename "$PROJECT")}"
: "${GDRIVE_TOKEN:?환경 변수 GDRIVE_TOKEN 이 없습니다. README 의 '구글 드라이브 자동 업로드'를 참고하세요.}"

# rclone 이 없으면 내려받기
if ! command -v rclone >/dev/null; then
  BIN="$HOME/.local/bin"; mkdir -p "$BIN"
  if [ ! -x "$BIN/rclone" ]; then
    TMP="$(mktemp -d)"
    curl -fsSL -o "$TMP/rclone.zip" https://downloads.rclone.org/rclone-current-linux-amd64.zip
    python3 -c "import zipfile,sys; zipfile.ZipFile(sys.argv[1]).extractall(sys.argv[2])" "$TMP/rclone.zip" "$TMP"
    install -m 755 "$TMP"/rclone-*-linux-amd64/rclone "$BIN/rclone"
  fi
  export PATH="$BIN:$PATH"
fi

# 설정 파일 없이 환경 변수로 원격 저장소 'gdrive' 정의
export RCLONE_CONFIG_GDRIVE_TYPE=drive
export RCLONE_CONFIG_GDRIVE_SCOPE=drive
export RCLONE_CONFIG_GDRIVE_TOKEN="$GDRIVE_TOKEN"

rclone copy "$PROJECT/output" "gdrive:$FOLDER" \
  --include "*.mp4" --include "*.txt" --progress
echo "업로드 완료: 내 드라이브 / $FOLDER"
rclone lsl "gdrive:$FOLDER"
