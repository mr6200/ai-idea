"""1단계: 인물별 기준이미지 후보 생성 (FLUX.1-dev, GPU 필요).

사용법:
  python scripts/01_make_refs.py                       # 인물마다 후보 4장 생성
  python scripts/01_make_refs.py --chars suspect -n 8  # 특정 인물만 다시
  python scripts/01_make_refs.py --pick detective=1102 suspect=2203 rookie=3301

후보는 refs/candidates/<인물>_<seed>.png 로 저장되고,
--pick 으로 고른 이미지가 refs/<인물>.png (최종 기준이미지)가 됩니다.
"""
import argparse
import shutil

from common import REFS, load_story


def pick(choices):
    for item in choices:
        char, seed = item.split("=")
        src = REFS / "candidates" / f"{char}_{seed}.png"
        if not src.exists():
            raise SystemExit(f"후보 이미지가 없습니다: {src}")
        shutil.copy(src, REFS / f"{char}.png")
        print(f"기준이미지 확정: refs/{char}.png  <-  {src.name}")


def generate(story, chars, n, steps, guidance):
    import torch
    from diffusers import FluxPipeline

    pipe = FluxPipeline.from_pretrained(
        "black-forest-labs/FLUX.1-dev", torch_dtype=torch.bfloat16
    ).to("cuda")

    video = story["video"]
    out_dir = REFS / "candidates"
    out_dir.mkdir(parents=True, exist_ok=True)
    for char in chars:
        c = story["characters"][char]
        prompt = f"{c['prompt']}, {story['setting']}"
        for i in range(n):
            seed = c["seed"] + i
            image = pipe(
                prompt,
                width=video["ref_width"],
                height=video["ref_height"],
                guidance_scale=guidance,
                num_inference_steps=steps,
                generator=torch.Generator("cuda").manual_seed(seed),
            ).images[0]
            path = out_dir / f"{char}_{seed}.png"
            image.save(path)
            print(f"[{char}] {path}")


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--story")
    p.add_argument("--chars", nargs="*", help="생성할 인물 키 (기본: 전부)")
    p.add_argument("-n", type=int, default=4, help="인물당 후보 수")
    p.add_argument("--steps", type=int, default=28)
    p.add_argument("--guidance", type=float, default=3.5)
    p.add_argument("--pick", nargs="*", metavar="CHAR=SEED", help="후보 중 기준이미지 확정")
    args = p.parse_args()

    if args.pick:
        pick(args.pick)
        return
    story = load_story(args.story)
    generate(story, args.chars or list(story["characters"]), args.n, args.steps, args.guidance)
    print("\n후보를 확인한 뒤 --pick 인물=seed 로 기준이미지를 확정하세요.")


if __name__ == "__main__":
    main()
