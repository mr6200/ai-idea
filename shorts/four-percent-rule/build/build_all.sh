#!/usr/bin/env bash
# Rebuild the 4%-rule Short. Done so far: scenes, storyboard, narration.
# Still to adapt from shorts/rule-of-72/build: gen_backgrounds prompts (run on RunPod), gen_thumbnail,
# gen_subtitles, gen_audio, gen_effectcraft and the render step.
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
python3 gen_narration.py   # Google Cloud TTS (GOOGLE_TTS_API_KEY); cached in tts/
# preview copy of the narration for review (narration.wav itself is regenerated, not committed)
mkdir -p ../audio
ffmpeg -v error -y -i narration.wav -c:a libmp3lame -b:a 128k ../audio/narration-preview.mp3
