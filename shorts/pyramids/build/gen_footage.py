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

LOOK = ("Documentary film still, vertical 9:16 frame, realistic photograph, ancient history reconstruction, "
        "natural light, rich natural colours, 35mm film grain, cinematic. ")
NEG = ("text, letters, writing, signboard, watermark, logo, flag, modern buildings, cars, tourists, cartoon, "
       "illustration, 3d render, deformed face, extra fingers, distorted hands, rotated image, sideways image")

# scene -> (still prompt, motion prompt). Only VIDEO scenes are animated by WAN; real CC0 / CC BY / CC BY-SA photos
# (photos/) carry the comparison scenes (user rules). Clip jobs are submitted one at a time and their ids saved
# to footage/jobs.json (see clip()).
SCENES = {
    "S01": ("A huge smooth white limestone Egyptian pyramid with a pointed golden capstone rising from the desert at "
            "sunrise, as it looked when newly built 4,500 years ago, long shadows on the sand, a line of tiny workers "
            "far below, epic wide shot",
            "the sun rises behind the pyramid, light spreads across its smooth white face, sand blows gently, slow "
            "push-in"),
    "S07": ("An ancient Mesoamerican ceremony at the flat top of a tall stepped stone pyramid, a small stone temple "
            "with a doorway, priests in feathered headdresses and capes seen from behind burning incense, smoke "
            "rising, crowds far below on a plaza, dramatic evening light",
            "incense smoke curls upward, feathers move in the wind, the priests raise their arms slowly, slow orbit "
            "around the temple top"),
    "S16": ("Ancient workers dragging and stacking large rough stone blocks and baskets of earth to build the wide "
            "base of a pyramid, the structure clearly wider at the bottom and narrower at the top, ramps of earth, "
            "dusty golden light, wide shot, figures small", ""),
    "S18": ("A tall stepped Maya pyramid rising above a dense green jungle at sunset, mist between the trees, birds "
            "flying, warm orange sky, nobody there, majestic and mysterious",
            "birds fly past the pyramid, mist drifts through the jungle canopy, the sunset light fades, slow aerial "
            "pull-back"),
}
VIDEO = ("S01", "S07", "S18")

# picked still per scene after looking at footage/cand ('a' or 'b')
PICK = {"S01": "b", "S07": "a", "S16": "a", "S18": "a"}


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


def run(*args):
    return json.loads(subprocess.run(["curl", "-sS", "-m", "120", *args, "-H", f"Authorization: Bearer {KEY}"],
                                     capture_output=True, text=True).stdout)


def clip(sid):
    """WAN clip for one scene. The job is submitted asynchronously and its id is written to footage/jobs.json
    before waiting, so a restarted container picks the same job up again instead of submitting (and paying for)
    a new one. A clip that is already on disk is skipped."""
    dst = os.path.join(OUT, f"{sid}.mp4")
    if os.path.exists(dst):
        print(sid, "already there", flush=True)
        return
    jp = os.path.join(OUT, "jobs.json")
    jobs = json.load(open(jp)) if os.path.exists(jp) else {}
    if sid not in jobs:
        src = urls()[f"{sid}_{PICK.get(sid, 'a')}"]
        payload = {"prompt": SCENES[sid][1] + ", realistic documentary footage, natural motion",
                   "image": src, "negative_prompt": NEG + ", morphing, flicker, jitter",
                   "size": "720*1280", "num_inference_steps": 30, "guidance": 5, "duration": 5,
                   "flow_shift": 5, "seed": 17, "enable_prompt_optimization": False, "enable_safety_checker": True}
        res = run("-X", "POST", f"{API}/wan-2-2-i2v-720/run", "-H", "Content-Type: application/json",
                  "-d", json.dumps({"input": payload}))
        jobs[sid] = res["id"]
        json.dump(jobs, open(jp, "w"), indent=1)
        print(sid, "submitted", res["id"], flush=True)
    t0 = time.time()
    while time.time() - t0 < 900:
        res = run(f"{API}/wan-2-2-i2v-720/status/{jobs[sid]}")
        if res.get("status") == "COMPLETED":
            out = res["output"]
            download(out["result"] if isinstance(out, dict) else out, dst)
            print(sid, "clip", out.get("cost") if isinstance(out, dict) else "", flush=True)
            return
        if res.get("status") not in ("IN_QUEUE", "IN_PROGRESS"):
            raise RuntimeError(f"{sid}: {str(res)[:300]}")
        time.sleep(10)
    raise RuntimeError(f"{sid}: timed out, run again to resume job {jobs[sid]}")


def main():
    os.makedirs(os.path.join(OUT, "cand"), exist_ok=True)
    stage = sys.argv[1]
    only = sys.argv[2:] or (list(SCENES) if stage == "images" else list(VIDEO))
    if stage == "images":
        seeds = (("e" if "--e" in sys.argv else "d", 3505 if "--e" in sys.argv else 3504),) if "--redo" in sys.argv else (("a", 3501), ("b", 3502))
        jobs = [(s, v, seed) for s in only if s not in ("--redo", "--e") for v, seed in seeds]
        with ThreadPoolExecutor(6) as ex:
            got = dict(ex.map(still, jobs))
        u = urls()
        u.update(got)
        json.dump(u, open(os.path.join(OUT, "urls.json"), "w"), indent=1)
    elif stage == "video":
        for sid in only:   # one at a time; each job id is saved before waiting (see clip)
            clip(sid)


if __name__ == "__main__":
    main()
