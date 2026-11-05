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

LOOK = ("Historical documentary film still, vertical 9:16 frame, realistic photograph, 1870s period accuracy, "
        "cold overcast sea light, mist, desaturated teal and grey colour grade, 35mm film grain, cinematic. ")
NEG = ("text, letters, writing, signboard, watermark, logo, flag, modern ship, engine, cartoon, illustration, "
       "3d render, deformed face, extra fingers, distorted hands")
SHIP = "a small two-masted 19th century wooden merchant brigantine with a dark hull"

# scene -> (still prompt, motion prompt)
SCENES = {
    "S01": (f"{SHIP} drifting alone on the grey Atlantic ocean in thick fog, some sails torn and hanging loose, "
            "ropes dangling, no people anywhere on deck, eerie silence, wide shot from low over the waves",
            "the ghost ship drifts slowly through the fog, torn sails flap gently, waves roll, slow push-in"),
    "S02": ("Three 1870s sailors in wool coats and caps rowing a small wooden boat across a choppy grey sea toward "
            f"{SHIP} in the mist, seen from behind the rowers, tense mood",
            "the sailors row steadily toward the distant ship, oars dip into the water, spray, slow tracking shot"),
    "S03": ("Interior of a small 1870s ship captain's cabin, empty, dim grey daylight from a porthole, a wooden bunk, "
            "a little girl's rag doll on the bunk, a woman's shawl on a chair, scattered papers, damp wood, nobody there",
            "dust floats in the porthole light, the cabin sways slightly with the sea, slow dolly in toward the doll"),
    "S03b": ("Ship's storeroom below deck of an 1870s sailing ship, dark wooden walls, shelves full of small wooden casks, "
             "burlap sacks of flour, hanging salted meat and large wooden water barrels, a lantern, untouched supplies, "
             "no glass bottles, no windows, nobody there",
             "the lantern swings gently with the ship's motion, light moves over the barrels, slow pan"),
    "S04": ("Close-up of a china teacup with steam rising on a wooden cabin table beside a half-eaten plate of bread, "
            "candlelight, dreamlike soft focus, like a legend, nobody there",
            "steam curls up from the teacup, the candle flame flickers, very slow push-in"),
    "S04b": ("Victorian era author's desk at night, an ink pen writing on paper by an oil lamp, a gentleman's hand "
             "in a dark sleeve, stacks of books, warm lamp light, the face not visible, the paper blank without writing",
             "the hand moves the pen across the paper, the lamp flame flickers softly, slow push-in"),
    "S05": ("Close-up of a frayed, cut rope hanging down over the weathered wooden rail of an 1870s sailing ship, "
            "dangling above the empty grey sea, fog, water droplets on the rope, nobody there",
            "the cut rope sways in the wind over the water, sea spray drifts past the rail, slow push-in"),
    "S05b": ("A small wooden rowing boat with a few 1870s sailors and a woman rowing away across a grey misty sea, "
             "seen from far behind, the figures tiny and anonymous, lonely mood",
             "the little boat rows slowly away into the fog, the oars dip, waves roll, slow push-in"),
    "S06": ("Dark cargo hold of an 1870s wooden ship packed with rows of old oak barrels, seawater sloshing on the "
            "floor, a single lantern, a faint haze of vapour in the air, nobody there",
            "water sloshes across the floor between the barrels, the lantern sways, haze drifts, slow dolly forward"),
    "S07": (f"Silhouette of {SHIP} with ragged sails fading into the fog at dusk on a calm grey sea, "
            "last light on the horizon, lonely and mysterious, wide shot",
            "the ship slowly drifts away into the fog, the mist thickens, slow pull-back"),
}

# picked still per scene after looking at footage/cand ('a' or 'b')
PICK = {"S01": "a", "S02": "a", "S03": "b", "S03b": "d", "S04": "a", "S04b": "a", "S05": "e", "S05b": "b",
        "S06": "a", "S07": "a"}


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
    only = sys.argv[2:] or list(SCENES)
    if stage == "images":
        seeds = (("e" if "--e" in sys.argv else "d", 2705 if "--e" in sys.argv else 2704),) if "--redo" in sys.argv else (("a", 2701), ("b", 2702))
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
