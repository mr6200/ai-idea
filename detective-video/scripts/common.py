"""파이프라인 공통: 대본(YAML) 로딩과 경로 규칙."""
import json
import subprocess
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
DEFAULT_STORY = ROOT / "story" / "episode01.yaml"
REFS = ROOT / "refs"
OUT = ROOT / "output"
TTS_DIR = OUT / "tts"
LIPSYNC_DIR = OUT / "lipsync"
CLIPS_DIR = OUT / "clips"
MANIFEST = OUT / "manifest.json"


def load_story(path=None):
    with open(path or DEFAULT_STORY, encoding="utf-8") as f:
        story = yaml.safe_load(f)
    for shot in story["shots"]:
        if shot["char"] not in story["characters"]:
            raise ValueError(f"{shot['id']}: 알 수 없는 인물 '{shot['char']}'")
        shot.setdefault("expr", "neutral")
        shot.setdefault("action", "")
    return story


def base_ref(char):
    return REFS / f"{char}.png"


def shot_ref(shot):
    """표정 변형 이미지가 있으면 그것을, 없으면 기준이미지를 쓴다."""
    if shot["expr"] != "neutral":
        variant = REFS / f"{shot['char']}_{shot['expr']}.png"
        if variant.exists():
            return variant
    return base_ref(shot["char"])


def load_manifest():
    if not MANIFEST.exists():
        raise SystemExit("output/manifest.json 이 없습니다. 먼저 03_tts.py 를 실행하세요.")
    return json.loads(MANIFEST.read_text(encoding="utf-8"))


def media_duration(path):
    out = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "default=nw=1:nk=1", str(path)],
        check=True, capture_output=True, text=True,
    ).stdout
    return float(out.strip())
