"""5단계: 컷 이어붙이기 + 타이틀/엔딩 + 한글 자막 + BGM -> 유튜브용 최종 영상.

립싱크 영상이 없는 컷은 기준이미지 정지화면으로 대신 넣습니다.
그래서 GPU 작업 전에도 03_tts.py 만 돌리고 실행하면 '애니매틱'(길이·흐름 확인용)이 나옵니다.

  python scripts/05_assemble.py
  python scripts/05_assemble.py --bgm assets/bgm.mp3 --bgm-volume 0.12
  python scripts/05_assemble.py --no-subs
결과: output/final.mp4, output/subtitles.srt
"""
import argparse
import os
import subprocess
from pathlib import Path

from common import CLIPS_DIR, LIPSYNC_DIR, OUT, load_manifest, load_story, shot_ref

FONT = os.environ.get("FONT_FILE", "/usr/share/fonts/truetype/nanum/NanumGothicBold.ttf")
FONT_NAME = os.environ.get("FONT_NAME", "NanumGothic")


def ff(*args):
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", *map(str, args)], check=True)


def encode_args(fps):
    return ["-c:v", "libx264", "-preset", "medium", "-crf", "18", "-pix_fmt", "yuv420p", "-r", fps,
            "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-ac", "2"]


def frame_filter(w, h, fps):
    return (f"scale={w}:{h}:force_original_aspect_ratio=increase:flags=lanczos,crop={w}:{h},"
            f"setsar=1,fps={fps},tpad=stop_mode=clone:stop_duration=3")


def make_shot_clip(shot, audio, duration, video, dst):
    w, h, fps = video["width"], video["height"], video["fps"]
    lipsync = LIPSYNC_DIR / f"{shot['id']}.mp4"
    src = ["-i", lipsync] if lipsync.exists() else ["-loop", "1", "-i", shot_ref(shot)]
    # 오디오는 항상 TTS 원본을 사용 (립싱크 결과의 오디오 트랙 유무와 무관하게 동일한 품질)
    ff(*src, "-i", audio, "-map", "0:v", "-map", "1:a", "-vf", frame_filter(w, h, fps),
       "-t", f"{duration:.3f}", *encode_args(fps), dst)
    return "video" if lipsync.exists() else "still"


def make_card(lines, seconds, video, dst):
    w, h, fps = video["width"], video["height"], video["fps"]
    filters = []
    for i, (text, size) in enumerate(lines):
        txt = dst.with_suffix(f".{i}.txt")
        txt.write_text(text, encoding="utf-8")
        y = f"(h-text_h)/2+{(i - (len(lines) - 1) / 2) * size * 1.8:.0f}"
        filters.append(f"drawtext=fontfile={FONT}:textfile={txt}:fontcolor=white:fontsize={size}:x=(w-text_w)/2:y={y}")
    fade_out = seconds - 0.8
    filters.append(f"fade=t=in:st=0:d=0.8,fade=t=out:st={fade_out}:d=0.8")
    ff("-f", "lavfi", "-i", f"color=c=black:s={w}x{h}:r={fps}:d={seconds}",
       "-f", "lavfi", "-i", "anullsrc=r=48000:cl=stereo",
       "-vf", ",".join(filters), "-t", seconds, *encode_args(fps), dst)


def srt_time(t):
    ms = int(round(t * 1000))
    return f"{ms // 3600000:02d}:{ms // 60000 % 60:02d}:{ms // 1000 % 60:02d},{ms % 1000:03d}"


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--story")
    p.add_argument("--bgm")
    p.add_argument("--bgm-volume", type=float, default=0.12)
    p.add_argument("--no-subs", action="store_true")
    args = p.parse_args()

    story = load_story(args.story)
    video = story["video"]
    manifest = load_manifest()
    CLIPS_DIR.mkdir(parents=True, exist_ok=True)

    clips, srt, t = [], [], 0.0
    title = CLIPS_DIR / "000_title.mp4"
    make_card([(story["title"], 96), (story.get("subtitle", ""), 44)], video["title_seconds"], video, title)
    clips.append(title)
    t += video["title_seconds"]

    stats = {"video": 0, "still": 0}
    for n, shot in enumerate(story["shots"], 1):
        sid = shot["id"]
        if sid not in manifest:
            raise SystemExit(f"{sid}: 음성이 없습니다. 03_tts.py 를 다시 실행하세요.")
        dur = manifest[sid]["duration"]
        dst = CLIPS_DIR / f"{sid}.mp4"
        stats[make_shot_clip(shot, OUT / manifest[sid]["audio"], dur, video, dst)] += 1
        clips.append(dst)
        name = story["characters"][shot["char"]]["name"]
        srt.append(f"{n}\n{srt_time(t + video['pad_before'])} --> {srt_time(t + dur - video['pad_after'] * 0.5)}\n"
                   f"{name}: {shot['line']}\n")
        t += dur
        print(f"{sid}: {dur:.2f}s")

    ending = CLIPS_DIR / "999_ending.mp4"
    make_card([("- 사건 종결 -", 80), ("이 영상은 AI로 제작된 픽션입니다", 36)], video["ending_seconds"], video, ending)
    clips.append(ending)
    t += video["ending_seconds"]

    (OUT / "subtitles.srt").write_text("\n".join(srt), encoding="utf-8")
    concat_list = CLIPS_DIR / "list.txt"
    concat_list.write_text("".join(f"file '{c.name}'\n" for c in clips), encoding="utf-8")
    body = OUT / "body.mp4"
    ff("-f", "concat", "-safe", "0", "-i", concat_list, "-c", "copy", body)

    cmd = ["-i", body.name]
    vf = [] if args.no_subs else [
        f"subtitles=subtitles.srt:force_style='FontName={FONT_NAME},FontSize=18,Outline=2,MarginV=28'"]
    if args.bgm:
        cmd += ["-stream_loop", "-1", "-i", Path(args.bgm).resolve(),
                "-filter_complex",
                f"[1:a]volume={args.bgm_volume},afade=t=out:st={t - 3:.2f}:d=3[b];"
                f"[0:a][b]amix=inputs=2:duration=first:normalize=0[a]",
                "-map", "0:v", "-map", "[a]"]
    if vf:
        cmd += ["-vf", ",".join(vf)]
    cmd += [*encode_args(video["fps"]), "-movflags", "+faststart", "final.mp4"]
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", *map(str, cmd)], cwd=OUT, check=True)

    print(f"\n완성: {OUT / 'final.mp4'}  ({int(t // 60)}분 {t % 60:.1f}초)")
    print(f"립싱크 영상 컷 {stats['video']}개, 정지화면 컷 {stats['still']}개")


if __name__ == "__main__":
    main()
