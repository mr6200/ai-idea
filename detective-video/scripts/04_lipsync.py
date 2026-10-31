"""4단계: 기준이미지 + 대사 음성 -> 말하는 영상 (InfiniteTalk, GPU 필요).

모든 컷이 같은 기준이미지에서 새로 출발하므로 컷이 바뀌어도 인물/배경이 흔들리지 않습니다.
이미 만들어진 컷은 건너뜁니다(--force 로 다시).

  python scripts/04_lipsync.py --only s01            # 먼저 한 컷으로 품질/시간 확인
  python scripts/04_lipsync.py                       # 전체
  python scripts/04_lipsync.py --fast                # 가속 LoRA 사용 (8스텝)
  python scripts/04_lipsync.py --low-vram            # 24~48GB GPU
"""
import argparse
import json
import os
import subprocess
import sys
import time
from pathlib import Path

from common import LIPSYNC_DIR, OUT, load_manifest, load_story, shot_ref

IT_DIR = Path(os.environ.get("INFINITETALK_DIR", "/workspace/InfiniteTalk"))
IT_PYTHON = os.environ.get("INFINITETALK_PYTHON", "/workspace/venv-talk/bin/python")
FAST_LORA = os.environ.get("FAST_LORA", str(IT_DIR / "weights" / "Wan2.1_I2V_14B_FusionX_LoRA.safetensors"))


def build_cmd(args, input_json, save_file):
    w = IT_DIR / "weights"
    cmd = [
        IT_PYTHON, "generate_infinitetalk.py",
        "--ckpt_dir", str(w / "Wan2.1-I2V-14B-480P"),
        "--wav2vec_dir", str(w / "chinese-wav2vec2-base"),
        "--infinitetalk_dir", str(w / "InfiniteTalk" / "single" / "infinitetalk.safetensors"),
        "--input_json", str(input_json),
        "--size", args.size,
        "--mode", "streaming",
        "--motion_frame", "9",
        "--save_file", str(save_file),
    ]
    if args.fast:
        cmd += ["--lora_dir", FAST_LORA, "--lora_scale", "1.0", "--sample_steps", "8",
                "--sample_shift", "2", "--sample_text_guide_scale", "1",
                "--sample_audio_guide_scale", "2"]
    else:
        cmd += ["--sample_steps", str(args.steps)]
    if args.low_vram:
        cmd += ["--num_persistent_param_in_dit", "0"]
    if args.extra:
        cmd += args.extra.split()
    return cmd


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--story")
    p.add_argument("--only", nargs="*")
    p.add_argument("--force", action="store_true")
    p.add_argument("--size", default="infinitetalk-480", choices=["infinitetalk-480", "infinitetalk-720"])
    p.add_argument("--steps", type=int, default=40)
    p.add_argument("--fast", action="store_true", help="FusionX LoRA로 8스텝 고속 생성")
    p.add_argument("--low-vram", action="store_true")
    p.add_argument("--extra", help="generate_infinitetalk.py 에 그대로 넘길 추가 인자")
    args = p.parse_args()

    story = load_story(args.story)
    manifest = load_manifest()
    LIPSYNC_DIR.mkdir(parents=True, exist_ok=True)
    jobs = LIPSYNC_DIR / "jobs"
    jobs.mkdir(exist_ok=True)

    for shot in story["shots"]:
        sid = shot["id"]
        if args.only and sid not in args.only:
            continue
        out_mp4 = LIPSYNC_DIR / f"{sid}.mp4"
        if out_mp4.exists() and not args.force:
            print(f"{sid}: 이미 있음, 건너뜀")
            continue
        ref = shot_ref(shot)
        if not ref.exists():
            sys.exit(f"{sid}: 기준이미지가 없습니다 ({ref})")

        c = story["characters"][shot["char"]]
        job = {
            "prompt": f"{c['talk_prompt']}, {shot['action']}".strip(", "),
            "cond_video": str(ref.resolve()),
            "cond_audio": {"person1": str((OUT / manifest[sid]["audio"]).resolve())},
        }
        input_json = jobs / f"{sid}.json"
        input_json.write_text(json.dumps(job, ensure_ascii=False, indent=2), encoding="utf-8")

        save_file = (LIPSYNC_DIR / sid).resolve()  # InfiniteTalk가 .mp4 를 붙여 저장
        print(f"\n=== {sid} [{c['name']}] {manifest[sid]['duration']:.1f}s  ref={ref.name}")
        t0 = time.time()
        subprocess.run(build_cmd(args, input_json.resolve(), save_file), cwd=IT_DIR, check=True)
        if not out_mp4.exists():
            candidates = sorted(LIPSYNC_DIR.glob(f"{sid}*.mp4"))
            if not candidates:
                sys.exit(f"{sid}: 결과 영상을 찾지 못했습니다 ({LIPSYNC_DIR})")
            candidates[-1].rename(out_mp4)
        print(f"{sid}: 완료 ({time.time() - t0:.0f}초) -> {out_mp4}")


if __name__ == "__main__":
    main()
