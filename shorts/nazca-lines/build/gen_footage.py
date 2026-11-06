"""Documentary footage for every scene through Runpod Public Endpoints (no endpoint to create or delete).

  python gen_footage.py images   -> Seedream 4.0 stills, two seeds per scene: footage/cand/Sxx_{a,b}.jpg ($0.027 each)
  python gen_footage.py video    -> WAN 2.2 I2V 720p animates the picked still (PICK): footage/Sxx.mp4 ($0.30 per 5 s clip)
  python gen_footage.py images S07 --redo -> one more still with a new seed (Sxx_d; earlier redo seeds: none yet)
  python gen_footage.py video S03 -> redo one scene

The still decides the faces (WAN only moves it), so stills are generated first and picked by eye.
Image URLs returned by Seedream are kept in footage/urls.json and passed to WAN as its input image.
Calls go through curl because Python's urllib gets 403 from the proxy here. Needs RUNPOD_API_KEY.
"""
import json
import os
import subprocess
import sys
import time
from concurrent.futures import ThreadPoolExecutor

ROOT = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(ROOT, "footage")
API = "https://api.runpod.ai/v2"
KEY = os.environ.get("RUNPOD_API_KEY", "")

LOOK = ("Documentary film still, vertical 9:16 frame, realistic photograph, the Nazca desert in southern Peru, "
        "dry reddish-brown stony desert, clear harsh sunlight, natural colours, 35mm film grain, cinematic. ")
NEG = ("text, letters, writing, signboard, watermark, logo, flag, cartoon, illustration, 3d render, "
       "deformed face, extra fingers, distorted hands, rotated image, sideways image")

# scene -> (still prompt, motion prompt). Only VIDEO scenes are animated by WAN (user rule: 3-4 video scenes,
# the rest are stills moved with a Ken Burns camera in EffectCraft), to keep the episode near $1.5.
SCENES = {
    "S01": ("High aerial view looking straight down at a giant hummingbird figure drawn as a single pale continuous "
            "line on the flat reddish-brown desert floor, long beak and spread wings, a few straight lines crossing "
            "the desert, soft morning light",
            "slow aerial drone flight over the desert drawing, the camera glides forward and slightly rotates, "
            "light dust drifts across the ground"),
    "S02": ("Upright portrait composition, horizon level. A lone hiker in a sun hat standing on the flat stony "
            "reddish-brown desert floor seen from behind, only a faint pale shallow line running across the ground "
            "in front of her, impossible to see any figure from here, wide empty desert, hazy hills far away", ""),
    "S03": ("Upright portrait composition, horizon level. Wide view of the dry Nazca desert plateau in southern "
            "Peru, flat reddish-brown stony plain with long straight pale lines and a large trapezoid shape "
            "stretching to the brown Andes foothills, cloudless sky", ""),
    "S04": ("High aerial view looking straight down at a giant monkey figure with a large spiral tail drawn as a "
            "pale continuous line on the reddish-brown desert floor, crossed by long straight lines, clear daylight", ""),
    "S05": ("Close-up of a pair of hands in simple woven cotton sleeves moving dark reddish-brown stones aside on "
            "the desert ground, revealing a strip of pale yellow-grey soil underneath, small piles of dark stones "
            "along both edges of the pale strip, ancient times, harsh sunlight", ""),
    "S06": ("A small 1930s propeller airplane flying low over the Nazca desert, seen from above and behind, below "
            "it giant pale lines and a large spider-like figure drawn on the reddish-brown ground, historical "
            "documentary photograph look, warm light",
            "the old propeller plane flies slowly over the desert drawings, its shadow moves across the ground, "
            "slow tracking shot from above"),
    "S07": ("A Japanese archaeologist in a sun hat kneeling in the stony desert next to a laptop and a small drone, "
            "examining a faint small figure of a human shape made of pale lines on a low desert slope, field "
            "research, harsh sunlight, face partly shaded by the hat", ""),
    "S08": ("A procession of ancient Nazca people in woven cotton tunics walking in a single file along a long "
            "pale straight line across the desert at dusk, seen from a distance, carrying clay pots, mystical "
            "orange light, figures small and anonymous", ""),
    "S09": ("Aerial view of the Nazca desert at golden sunset, long shadows, giant pale lines and a huge "
            "condor figure on the reddish ground glowing in the low light, mysterious and quiet",
            "slow aerial pull-back and rise above the desert drawings at sunset, the light fades slowly"),
}
VIDEO = ("S01", "S06", "S09")

# picked still per scene after looking at footage/cand ('a' or 'b')
PICK = {"S01": "a", "S02": "b", "S03": "b", "S04": "a", "S05": "a", "S06": "a", "S07": "a", "S08": "a", "S09": "a"}


def post(endpoint, payload, timeout=420):
    """runsync, then poll /status while the job is still running; retries on transient errors."""
    for attempt in range(4):
        r = subprocess.run(["curl", "-sS", "-m", "300", "-X", "POST", f"{API}/{endpoint}/runsync",
                            "-H", f"Authorization: Bearer {KEY}", "-H", "Content-Type: application/json",
                            "-d", json.dumps({"input": payload})], capture_output=True, text=True)
        try:
            res = json.loads(r.stdout)
        except json.JSONDecodeError:
            time.sleep(5 * (attempt + 1))
            continue
        t0 = time.time()
        while res.get("status") in ("IN_QUEUE", "IN_PROGRESS") and time.time() - t0 < timeout:
            time.sleep(10)
            r = subprocess.run(["curl", "-sS", f"{API}/{endpoint}/status/{res['id']}",
                                "-H", f"Authorization: Bearer {KEY}"], capture_output=True, text=True)
            res = json.loads(r.stdout)
        if res.get("status") == "COMPLETED":
            return res["output"]
        print("retry", endpoint, res.get("status"), str(res)[:200], flush=True)
        time.sleep(5 * (attempt + 1))
    raise RuntimeError(f"{endpoint} failed")


def download(url, path):
    subprocess.run(["curl", "-sS", "-o", path, url], check=True)


def urls():
    p = os.path.join(OUT, "urls.json")
    return json.load(open(p)) if os.path.exists(p) else {}


def still(job):
    sid, var, seed = job
    out = post("seedream-v4-t2i", {"prompt": LOOK + SCENES[sid][0], "negative_prompt": NEG,
                                    "size": "1080*1920", "seed": seed, "enable_safety_checker": True})
    download(out["result"], os.path.join(OUT, "cand", f"{sid}_{var}.jpg"))
    print(sid, var, out.get("cost"), flush=True)
    return f"{sid}_{var}", out["result"]


def clip(sid):
    src = urls()[f"{sid}_{PICK.get(sid, 'a')}"]
    out = post("wan-2-2-i2v-720", {"prompt": SCENES[sid][1] + ", realistic documentary footage, natural motion",
                                   "image": src, "negative_prompt": NEG + ", morphing, flicker, jitter",
                                   "size": "720*1280", "num_inference_steps": 30, "guidance": 5, "duration": 5,
                                   "flow_shift": 5, "seed": 17, "enable_prompt_optimization": False,
                                   "enable_safety_checker": True})
    url = out["result"] if isinstance(out, dict) else out
    download(url, os.path.join(OUT, f"{sid}.mp4"))
    print(sid, "clip", out.get("cost") if isinstance(out, dict) else "", flush=True)


def main():
    os.makedirs(os.path.join(OUT, "cand"), exist_ok=True)
    stage = sys.argv[1]
    only = sys.argv[2:] or (list(SCENES) if stage == "images" else list(VIDEO))
    if stage == "images":
        seeds = (("e" if "--e" in sys.argv else "d", 2905 if "--e" in sys.argv else 2904),) if "--redo" in sys.argv else (("a", 2901), ("b", 2902))
        jobs = [(s, v, seed) for s in only if s not in ("--redo", "--e") for v, seed in seeds]
        with ThreadPoolExecutor(6) as ex:
            got = dict(ex.map(still, jobs))
        u = urls()
        u.update(got)
        json.dump(u, open(os.path.join(OUT, "urls.json"), "w"), indent=1)
    elif stage == "video":
        with ThreadPoolExecutor(6) as ex:
            list(ex.map(clip, only))


if __name__ == "__main__":
    main()
