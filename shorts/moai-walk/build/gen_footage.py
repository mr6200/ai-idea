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

LOOK = ("Documentary film still, vertical 9:16 frame, realistic photograph, Easter Island (Rapa Nui), "
        "natural Pacific light, rich but natural colours, 35mm film grain, cinematic. ")
NEG = ("text, letters, writing, signboard, watermark, logo, flag, cartoon, illustration, 3d render, "
       "deformed face, extra fingers, distorted hands, rotated image")

# scene -> (still prompt, motion prompt). Only VIDEO scenes are animated by WAN (user rule: 3-4 video scenes,
# the rest are stills moved with a Ken Burns camera in EffectCraft), to keep the episode near $1.5.
SCENES = {
    "S01": ("A row of giant moai stone statues standing on a stone platform near the Pacific coast of Easter Island "
            "at golden sunset, low angle, dramatic clouds, grass in the foreground",
            "clouds drift slowly across the sunset sky, grass sways in the wind, slow push-in toward the statues"),
    "S02": ("Upright portrait composition, horizon level. High aerial view of Easter Island: a triangular green island with "
            "an extinct volcano at each of its three corners, alone in the vast deep blue Pacific Ocean, white surf on the "
            "cliffs, a few clouds, no other land anywhere", ""),
    "S03": ("A single giant moai stone statue standing on a grassy slope, a small tourist in hiking clothes standing "
            "beside it seen from behind, the person reaching only to the statue's chest, overcast soft light", ""),
    "S04": ("Eye-level photo of three giant moai heads half buried in green grass on the slope of the Rano Raraku "
            "quarry, a brown volcanic rock wall rising behind them, blue sky with clouds at the top of the frame", ""),
    "S05": ("Night on ancient Easter Island, a few Polynesian islanders in bark-cloth wraps sitting around a small "
            "fire under a starry sky, seen from behind, giant moai silhouettes standing on the hill behind them, "
            "moonlight, mystical mood", ""),
    "S06": ("Archaeology experiment on a dirt road on Easter Island: an upright 3 metre tall grey replica moai statue "
            "with three long ropes tied around its head, a team of people in modern outdoor clothes and caps pulling "
            "one rope on the left, another team pulling a rope on the right, a third team holding a rope behind it, "
            "the statue tilted to one side, documentary photograph, dust",
            "the left team and the right team pull their ropes in turn, the upright statue rocks from side to side "
            "and shuffles forward step by step, dust rises, handheld documentary camera"),
    "S07": ("An ancient narrow dirt road across grassland on Easter Island, slightly sunken in the middle, with a "
            "broken moai statue lying face down beside the road, morning light, long shadows", ""),
    "S08": ("Giant moai stone statues silhouetted against a blazing orange sunset over the Pacific Ocean on Easter "
            "Island, the first stars appearing, calm and mysterious",
            "the sun sinks behind the statues, clouds move, the sky darkens slowly, slow pull-back"),
}
VIDEO = ("S01", "S06", "S08")

# picked still per scene after looking at footage/cand ('a' or 'b')
PICK = {"S01": "a", "S02": "d", "S03": "a", "S04": "e", "S05": "b", "S06": "a", "S07": "b", "S08": "b"}


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
        seeds = (("e" if "--e" in sys.argv else "d", 2805 if "--e" in sys.argv else 2704),) if "--redo" in sys.argv else (("a", 2801), ("b", 2802))
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
