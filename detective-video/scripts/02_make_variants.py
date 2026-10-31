"""2단계(선택): 기준이미지에서 표정 변형 만들기 (FLUX.1-Kontext-dev, GPU 필요).

Kontext는 입력 이미지를 '편집'하는 모델이라 얼굴·옷·배경을 유지한 채 표정만 바꿉니다.
대본에서 실제로 쓰이는 (인물, 표정) 조합만 생성합니다.
결과: refs/<인물>_<표정>.png  -> 결과가 마음에 안 들면 지우면 됩니다(기준이미지로 대체됨).

  python scripts/02_make_variants.py
  python scripts/02_make_variants.py --force          # 이미 있는 것도 다시
"""
import argparse

from common import REFS, base_ref, load_story


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--story")
    p.add_argument("--steps", type=int, default=28)
    p.add_argument("--guidance", type=float, default=2.5)
    p.add_argument("--force", action="store_true")
    args = p.parse_args()

    story = load_story(args.story)
    needed = sorted({(s["char"], s["expr"]) for s in story["shots"] if s["expr"] != "neutral"})
    todo = [(c, e) for c, e in needed if args.force or not (REFS / f"{c}_{e}.png").exists()]
    if not todo:
        print("만들 표정 변형이 없습니다.")
        return

    import torch
    from diffusers import FluxKontextPipeline
    from PIL import Image

    pipe = FluxKontextPipeline.from_pretrained(
        "black-forest-labs/FLUX.1-Kontext-dev", torch_dtype=torch.bfloat16
    ).to("cuda")

    for char, expr in todo:
        ref = base_ref(char)
        if not ref.exists():
            raise SystemExit(f"기준이미지가 없습니다: {ref} (01_make_refs.py --pick 먼저)")
        src = Image.open(ref).convert("RGB")
        image = pipe(
            image=src,
            prompt=story["expressions"][expr],
            guidance_scale=args.guidance,
            num_inference_steps=args.steps,
            generator=torch.Generator("cuda").manual_seed(story["characters"][char]["seed"]),
        ).images[0]
        # Kontext는 자체 선호 해상도로 출력하므로 기준이미지 크기로 되돌린다
        image = image.resize(src.size, Image.LANCZOS)
        path = REFS / f"{char}_{expr}.png"
        image.save(path)
        print(f"[{char}/{expr}] {path}")


if __name__ == "__main__":
    main()
