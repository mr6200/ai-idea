"""AI scene backgrounds with SDXL + SDXL-Lightning (4 steps), one per scene, cached in ai_bg/.

Runs on CPU in bfloat16 (about 5 minutes and 11 GB RAM per image). Needs torch, diffusers,
transformers, accelerate, peft and access to huggingface.co / *.hf.co. Existing images are
kept, so delete ai_bg/Sxx.png to redraw one scene.
    python gen_backgrounds.py [S05 S12 ...]
Both models are CreativeML Open RAIL++-M (commercial use allowed).
"""
import os
import sys
import time

ROOT = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(ROOT, "ai_bg")
STYLE = ("flat vector illustration, warm cream and soft orange palette, gentle sunlight, soft shadows, "
         "minimal clean shapes, calm empty space in the middle, editorial illustration, no text, no letters, no numbers")
NEGATIVE = "text, letters, numbers, words, watermark, logo, signature, photo, realistic, cluttered, dark"

SCENES = {
    "S01": "shopping street with store windows and price tags, bright day",
    "S02": "electronics store display with a laptop on a counter",
    "S03": "small shop counter with a card payment terminal, warm light",
    "S04": "modern office tower of a financial company, blue sky",
    "S05": "calm lake with a fishing rod on a wooden pier, golden hour",
    "S06": "busy cafe counter with a card reader and pastries",
    "S07": "office with charts on the wall and a city view",
    "S08": "evening city street with neon signs and shop fronts",
    "S09": "wall calendar with pages flying, desk below",
    "S10": "bank meeting room with a big window, soft light",
    "S11": "quiz show stage with spotlights and curtains",
    "S12": "cozy living room with a smartphone resting on the sofa",
}


def main():
    import torch
    from diffusers import EulerDiscreteScheduler, StableDiffusionXLPipeline
    from huggingface_hub import hf_hub_download

    todo = [s for s in (sys.argv[1:] or SCENES) if not os.path.exists(os.path.join(OUT, f"{s}.png"))]
    if not todo:
        print("all backgrounds cached")
        return
    os.makedirs(OUT, exist_ok=True)
    torch.set_num_threads(os.cpu_count())
    pipe = StableDiffusionXLPipeline.from_pretrained(
        "stabilityai/stable-diffusion-xl-base-1.0", variant="fp16", torch_dtype=torch.bfloat16, use_safetensors=True)
    pipe.load_lora_weights(hf_hub_download("ByteDance/SDXL-Lightning", "sdxl_lightning_4step_lora.safetensors"))
    pipe.fuse_lora()
    pipe.scheduler = EulerDiscreteScheduler.from_config(pipe.scheduler.config, timestep_spacing="trailing")
    for i, sid in enumerate(todo):
        t0 = time.time()
        # Lightning runs without CFG, so the negative prompt has no effect; kept for non-distilled runs
        img = pipe(f"{SCENES[sid]}, {STYLE}", num_inference_steps=4, guidance_scale=0,
                   width=768, height=1344, generator=torch.Generator().manual_seed(100 + int(sid[1:]))).images[0]
        img.save(os.path.join(OUT, f"{sid}.png"))
        print(f"{sid} {time.time() - t0:.0f}s ({i + 1}/{len(todo)})", flush=True)


if __name__ == "__main__":
    main()
