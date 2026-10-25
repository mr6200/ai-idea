#!/usr/bin/env bash
# Rebuild the compound-interest Short end to end:
# SVG parts -> VectorCraft PNG layers -> subtitles/audio -> EffectCraft project -> MP4.
set -euo pipefail
cd "$(dirname "$0")"

python3 gen_scenes.py
for d in svg/S*; do
  id=$(basename "$d"); mkdir -p "parts/$id"
  for f in "$d"/*.svg; do
    n=$(basename "$f" .svg)
    if [ "$n" = "_full" ]; then
      vectorcraft-cli convert "$f" "../scenes/$id.vectorcraft" >/dev/null
      vectorcraft-cli convert "$f" "../scenes/$id.png" >/dev/null
    else
      vectorcraft-cli convert "$f" "parts/$id/$n.png" >/dev/null
    fi
  done
done
python3 export_s01_s03.py
python3 timeline.py
python3 gen_subtitles.py
python3 gen_narration.py   # Google Cloud TTS (GOOGLE_TTS_API_KEY); cached in tts/
python3 gen_audio.py
python3 gen_effectcraft.py

mkdir -p ../video
effectcraft-cli script build.jsx --empty --save-as ../video/compound-interest.ecproj
if [ "${1:-}" = "--render" ]; then
  effectcraft-cli render --project ../video/compound-interest.ecproj --comp Main \
    --out ../video/raw.mp4 --format h264 --audio on --quality best
  # loudness-normalised audio, H.264 Main profile, moov atom up front for previews
  ffmpeg -v error -y -i ../video/raw.mp4 \
    -map 0:v -map 0:a -c:v libx264 -profile:v main -level 4.1 -pix_fmt yuv420p -crf 19 \
    -af loudnorm=I=-14:TP=-1.5:LRA=11 -c:a aac -b:a 192k -ar 48000 \
    -movflags +faststart -shortest ../video/compound-interest-shorts.mp4
  rm -f ../video/raw.mp4
fi
