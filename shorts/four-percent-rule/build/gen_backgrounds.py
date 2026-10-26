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
    "S01": "elderly couple relaxing on a sunny porch with potted plants, retirement",
    "S02": "soft fog over a quiet path with scattered signposts, uncertainty",
    "S03": "minimal desk with a notebook and a single round wall clock, morning light",
    "S04": "kitchen shelf with glass jars of coins, warm window light",
    "S05": "drafting table with rulers and paper sheets, seen from above",
    "S06": "household budget desk with receipts, calculator and a coffee cup",
    "S07": "row of three small houses of increasing size on a gentle hill",
    "S08": "post office counter with envelopes and a calendar, calm",
    "S09": "old university library with tall bookshelves and reading lamps",
    "S10": "research desk with stacks of archive folders and a desk lamp",
    "S11": "big tree with deep roots on a hill, wide landscape, steady growth",
    "S12": "stormy sea with a small sailboat, dramatic clouds, red and dark orange tones",
    "S13": "long winding road through seasons, spring to winter, far horizon",
    "S14": "two stacks of wooden blocks of different heights on a table",
    "S15": "tidy desk with a checklist clipboard and a desk lamp",
    "S16": "cozy study with a corkboard and a warm floor lamp",
    "S17": "quiz show stage with spotlights and curtains",
    "S18": "cozy living room with a smartphone resting on the sofa",
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
