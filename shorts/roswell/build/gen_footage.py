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

LOOK = ("Historical documentary film still, vertical 9:16 frame, realistic photograph, New Mexico in 1947, "
        "period accuracy, dry high desert ranch land, warm faded colours, 35mm film grain, cinematic. ")
NEG = ("text, letters, writing, newspaper headline, signboard, watermark, logo, flag, insignia, alien, ufo, flying saucer, "
       "cartoon, illustration, 3d render, deformed face, extra fingers, distorted hands, rotated image, sideways image")

# scene -> (still prompt, motion prompt). Only VIDEO scenes are animated by WAN; real archive images (photos/) carry
# the factual scenes, and the remaining scenes are Seedream stills moved with a Ken Burns camera (user rules).
SCENES = {
    "S01": ("Night on a lonely New Mexico desert ranch in 1947, a thunderstorm on the horizon, lightning flashing over "
            "the dark plain, a wooden windmill and fence silhouetted, strange shiny scraps glinting on the ground",
            "lightning flashes on the horizon, clouds roll, the shiny scraps glint, slow push-in across the plain"),
    "S02": ("A 1940s American rancher in a cowboy hat and work clothes seen from behind, crouching on dry grassland "
            "and picking up scattered debris: strips of shiny foil, torn grey rubber, tough brown paper, thin wooden "
            "sticks and tape, the pieces spread over the ground, morning light", ""),
    "S04": ("A 1947 US Army Air Forces office, two officers in khaki uniforms seen from behind and the side, faces not "
            "visible, looking down at crumpled foil, rubber strips and broken wooden sticks spread on brown paper on "
            "the floor, a desk and a window with blinds, no insignia readable", ""),
    "S05": ("A small 1970s living room, an old man in a cardigan seen from behind sitting in an armchair talking to a "
            "visitor holding a cassette tape recorder on the table between them, warm lamp light, faces not visible", ""),
    "S08": ("1947 New Mexico desert at dawn, a very long vertical chain of a dozen white weather balloons rising "
            "into the sky tied on a single long rope with hanging foil radar reflectors and small boxes, a few men in "
            "1940s work clothes on the ground below seen from far away",
            "the long chain of balloons rises slowly into the sky, the reflectors twist and glint, the men look up, "
            "slow tilt up"),
    "S10": ("A lonely desert highway at night under a vast starry sky with the Milky Way, a small town glowing far "
            "away on the horizon, mysterious mood, no signs",
            "stars twinkle, a faint light moves slowly across the sky, slow push-in along the road"),
}
VIDEO = ("S01", "S08", "S10")

# picked still per scene after looking at footage/cand ('a' or 'b')
PICK = {"S01": "b", "S02": "a", "S04": "a", "S05": "a", "S08": "a", "S10": "a"}


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
        seeds = (("e" if "--e" in sys.argv else "d", 3005 if "--e" in sys.argv else 3004),) if "--redo" in sys.argv else (("a", 3001), ("b", 3002))
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
