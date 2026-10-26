#!/usr/bin/env bash
# Rebuild the how-banks-earn Short end to end:
# SVG parts -> VectorCraft PNG layers -> subtitles/audio -> EffectCraft project -> MP4.
# AI backgrounds are committed in ai_bg/; to redraw them see gen_backgrounds_runpod.py (README).
set -euo pipefail
cd "$(dirname "$0")"

python3 verify_numbers.py
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
python3 compose_bg.py      # lays ai_bg/Sxx.png under the cream wash when present
python3 timeline.py
python3 gen_storyboard.py  # storyboard.html/.png from the scene art
python3 gen_thumbnail.py
python3 gen_subtitles.py
python3 gen_narration.py   # Google Cloud TTS (GOOGLE_TTS_API_KEY); cached in tts/
# preview copy of the narration for review (narration.wav itself is regenerated, not committed)
mkdir -p ../audio
ffmpeg -v error -y -i narration.wav -c:a libmp3lame -b:a 128k ../audio/narration-preview.mp3
python3 gen_audio.py
python3 gen_effectcraft.py

mkdir -p ../video
effectcraft-cli script build.jsx --empty --save-as ../video/how-banks-earn.ecproj
if [ "${1:-}" = "--render" ]; then
  effectcraft-cli render --project ../video/how-banks-earn.ecproj --comp Main \
    --out ../video/raw.mp4 --format h264 --audio on --quality best
  # loudness-normalised audio (single-pass loudnorm lands near -16, so +1.8 dB under a limiter), H.264 Main profile, moov atom up front for previews
  ffmpeg -v error -y -i ../video/raw.mp4 \
    -map 0:v -map 0:a -c:v libx264 -profile:v main -level 4.1 -pix_fmt yuv420p -crf 19 \
    -af "loudnorm=I=-14:TP=-1.5:LRA=11,volume=1.8dB,alimiter=limit=0.84:level=false" -c:a aac -b:a 192k -ar 48000 \
    -movflags +faststart -shortest ../video/how-banks-earn-shorts.mp4
  rm -f ../video/raw.mp4
fi
