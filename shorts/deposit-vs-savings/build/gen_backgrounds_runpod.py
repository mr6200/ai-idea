"""AI scene backgrounds on a RunPod serverless GPU (runpod/worker-comfyui SDXL image), cached in ai_bg/.

Same prompts as gen_backgrounds.py, but full SDXL 1.0 at 30 steps with CFG, so the negative
prompt (no text, no watermark) takes effect. Needs RUNPOD_API_KEY and RUNPOD_ENDPOINT_ID
(an endpoint running runpod/worker-comfyui:5.10.0-sdxl; see README). Existing images are kept,
so delete ai_bg/Sxx.png to redraw one scene.
    python gen_backgrounds_runpod.py [S05 S12 ...]
"""
import base64
import json
import os
import sys
import time
import urllib.request

from gen_backgrounds import NEGATIVE, OUT, SCENES, STYLE

API = f"https://api.runpod.ai/v2/{os.environ.get('RUNPOD_ENDPOINT_ID', '')}"
HEADERS = {"Content-Type": "application/json", "Authorization": f"Bearer {os.environ.get('RUNPOD_API_KEY', '')}"}
STEPS, CFG = 30, 6.0


def call(path, body=None):
    req = urllib.request.Request(API + path, data=json.dumps(body).encode() if body else None, headers=HEADERS)
    with urllib.request.urlopen(req, timeout=120) as r:
        return json.load(r)


def workflow(sid):
    """ComfyUI API-format graph: SDXL base, 768x1344, seed 100 + scene number."""
    return {
        "4": {"class_type": "CheckpointLoaderSimple", "inputs": {"ckpt_name": "sd_xl_base_1.0.safetensors"}},
        "6": {"class_type": "CLIPTextEncode", "inputs": {"text": f"{SCENES[sid]}, {STYLE}", "clip": ["4", 1]}},
        "7": {"class_type": "CLIPTextEncode", "inputs": {"text": NEGATIVE, "clip": ["4", 1]}},
        "5": {"class_type": "EmptyLatentImage", "inputs": {"width": 768, "height": 1344, "batch_size": 1}},
        "3": {"class_type": "KSampler", "inputs": {
            "seed": 100 + int(sid[1:]), "steps": STEPS, "cfg": CFG, "sampler_name": "dpmpp_2m", "scheduler": "karras",
            "denoise": 1.0, "model": ["4", 0], "positive": ["6", 0], "negative": ["7", 0], "latent_image": ["5", 0]}},
        "8": {"class_type": "VAEDecode", "inputs": {"samples": ["3", 0], "vae": ["4", 2]}},
        "9": {"class_type": "SaveImage", "inputs": {"filename_prefix": sid, "images": ["8", 0]}},
    }


def main():
    todo = [s for s in (sys.argv[1:] or SCENES) if not os.path.exists(os.path.join(OUT, f"{s}.png"))]
    if not todo:
        print("all backgrounds cached")
        return
    os.makedirs(OUT, exist_ok=True)
    jobs = {call("/run", {"input": {"workflow": workflow(sid)}})["id"]: sid for sid in todo}
    print(f"queued {len(jobs)} jobs", flush=True)
    t0 = time.time()
    while jobs:
        time.sleep(10)
        for jid, sid in list(jobs.items()):
            st = call(f"/status/{jid}")
            if st["status"] == "COMPLETED":
                img = st["output"]["images"][0]
                with open(os.path.join(OUT, f"{sid}.png"), "wb") as f:
                    f.write(base64.b64decode(img["data"]))
                print(f"{sid} done at {time.time() - t0:.0f}s", flush=True)
                del jobs[jid]
            elif st["status"] in ("FAILED", "CANCELLED", "TIMED_OUT"):
                print(f"{sid} {st['status']}: {st.get('error') or st.get('output')}", flush=True)
                del jobs[jid]


if __name__ == "__main__":
    main()
