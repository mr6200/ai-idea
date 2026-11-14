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

LOOK = ("Historical documentary film still, vertical 9:16 frame, realistic photograph, Strasbourg in the summer "
        "of 1518, late medieval Alsace, half-timbered houses, period-accurate clothing, hot hazy sunlight, "
        "warm desaturated colours, 35mm film grain, cinematic. ")
NEG = ("text, letters, writing, signboard, watermark, logo, flag, coat of arms, modern clothing, cartoon, illustration, "
       "3d render, deformed face, extra fingers, distorted hands, extra limbs, rotated image, sideways image")

# scene -> (still prompt, motion prompt). Only VIDEO scenes are animated by WAN; real public-domain prints
# (photos/) carry the documentary scenes, the rest are Seedream stills moved with a Ken Burns camera (user rules).
SCENES = {
    "S01": ("A woman in a plain 16th century linen dress and white headscarf dancing alone in a narrow cobblestone "
            "street between half-timbered houses on a hot summer day, arms raised, eyes half closed, exhausted, a few "
            "townspeople in the doorways watching her uneasily",
            "the woman keeps dancing and turning in the street, her skirt swirls, dust rises, the onlookers step back, "
            "slow push-in"),
    "S02": ("A crowd of thirty exhausted townspeople in 16th century clothing dancing wildly in a sunlit medieval "
            "square, some stumbling, some with bare bleeding feet, others watching in fear from the edges, dust and "
            "heat haze", ""),
    "S04": ("Inside a dim 1518 town council chamber with wooden panelling, a group of city councillors and a physician "
            "in dark robes and caps standing around a long table, seen from behind and from the side, faces in shadow, "
            "worried discussion, light from leaded windows", ""),
    "S05": ("A wooden stage set up in a large medieval guild hall, three 16th century musicians playing a drum, a fife "
            "and a bagpipe, a crowd of exhausted people dancing in front of the stage, dusty light beams",
            "the musicians play, the dancers keep moving and swaying, dust floats in the light beams, slow dolly in"),
    "S07": ("A small procession of exhausted 16th century townspeople wearing red shoes walking up a forest path toward "
            "a small stone chapel on a hilltop in the Vosges mountains, holding small wooden crosses, seen from behind, "
            "early autumn morning mist", ""),
    "S09": ("Extreme macro photograph of a single ripe golden rye ear filling the frame, with three long hard black "
            "curved horn-shaped ergot sclerotia sticking out between the grains instead of seeds, botanical documentary "
            "macro, plain blurred field background, no people, overcast light", ""),
    "S10": ("A starving 16th century family in a bare dark room, an empty bread basket and an empty wooden bowl on the "
            "table, thin faces in shadow, candlelight, poverty and famine", ""),
    "S12": ("An empty cobblestone street of medieval Strasbourg at dusk, a single worn red leather shoe lying in the "
            "middle of the street, long shadows, the cathedral spire faintly visible far away in the haze",
            "dust drifts across the empty street, the light fades slowly, very slow push-in toward the red shoe"),
}
VIDEO = ("S01", "S05", "S12")

# picked still per scene after looking at footage/cand ('a' or 'b')
PICK = {"S01": "a", "S02": "a", "S04": "a", "S05": "a", "S07": "a", "S09": "d", "S10": "a", "S12": "a"}


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
        seeds = (("e" if "--e" in sys.argv else "d", 3105 if "--e" in sys.argv else 3104),) if "--redo" in sys.argv else (("a", 3101), ("b", 3102))
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
