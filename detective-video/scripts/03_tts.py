"""3단계: 대사 음성 생성 (edge-tts, GPU 불필요) + 컷 길이 계산.

결과:
  output/tts/<컷>.wav      앞뒤 여백이 붙은 16kHz 모노 음성 (립싱크 입력 겸 최종 오디오)
  output/manifest.json     컷별 음성 경로와 길이

  python scripts/03_tts.py
  python scripts/03_tts.py --only s05 s06   # 일부 컷만 다시
"""
import argparse
import asyncio
import json
import subprocess

import edge_tts

from common import MANIFEST, TTS_DIR, load_story, media_duration


async def synth(text, voice, rate, pitch, path):
    await edge_tts.Communicate(text, voice, rate=rate, pitch=pitch).save(str(path))


def pad_to_wav(src, dst, before, after):
    subprocess.run(
        ["ffmpeg", "-y", "-loglevel", "error", "-i", str(src),
         "-af", f"adelay={int(before * 1000)},apad=pad_dur={after}",
         "-ar", "16000", "-ac", "1", str(dst)],
        check=True,
    )


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--story")
    p.add_argument("--only", nargs="*")
    args = p.parse_args()

    story = load_story(args.story)
    video = story["video"]
    TTS_DIR.mkdir(parents=True, exist_ok=True)
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8")) if MANIFEST.exists() else {}

    for shot in story["shots"]:
        sid = shot["id"]
        wav = TTS_DIR / f"{sid}.wav"
        if args.only and sid not in args.only:
            continue
        c = story["characters"][shot["char"]]
        mp3 = TTS_DIR / f"{sid}.mp3"
        asyncio.run(synth(shot["line"], c["voice"], c["rate"], c["pitch"], mp3))
        pad_to_wav(mp3, wav, video["pad_before"], video["pad_after"])
        mp3.unlink()
        manifest[sid] = {"audio": str(wav.relative_to(TTS_DIR.parent)), "duration": media_duration(wav)}
        print(f"{sid} [{c['name']}] {manifest[sid]['duration']:.2f}s  {shot['line'][:30]}")

    # 대본에서 빠진 컷은 정리
    manifest = {s["id"]: manifest[s["id"]] for s in story["shots"] if s["id"] in manifest}
    MANIFEST.write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")

    total = sum(m["duration"] for m in manifest.values()) + video["title_seconds"] + video["ending_seconds"]
    print(f"\n예상 영상 길이: {int(total // 60)}분 {total % 60:.1f}초 ({len(manifest)}컷)")


if __name__ == "__main__":
    main()
