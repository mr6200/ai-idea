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

LOOK = ("Documentary film still, vertical 9:16 frame, realistic photograph, Neolithic Britain reconstruction, "
        "natural light, rich natural colours, 35mm film grain, cinematic. ")
NEG = ("text, letters, writing, signboard, watermark, logo, flag, modern buildings, cars, tourists, metal tools, pyramids, wheels, carts, cartoon, "
       "illustration, 3d render, deformed face, extra fingers, distorted hands, rotated image, sideways image")

# scene -> (still prompt, motion prompt). Only VIDEO scenes are animated by WAN; real CC0 / CC BY / CC BY-SA photos
# (photos/) carry the comparison scenes (user rules). Clip jobs are submitted one at a time and their ids saved
# to footage/jobs.json (see clip()).
SCENES = {
    "S01": ("Neolithic people in simple hide and wool clothing raising a huge grey sarsen stone upright with thick "
            "ropes and a wooden A-frame on a wide grassy plain at dawn, a half-built ring of giant standing stones "
            "behind them, mist, golden sunrise, wide shot, figures small, epic",
            "the people pull the ropes together and the huge stone slowly tilts upright, mist drifts, the sun rises, "
            "slow push-in"),
    "S06": ("Upright vertical portrait photo, eye-level view, horizon level across the frame, sky at the top. A team of Neolithic people dragging a long grey-blue stone pillar lying flat on its side on a low wooden sledge over log rails "
            "through green rolling Welsh hills, ropes over their shoulders, overcast soft light, wide shot, figures "
            "small",
            "the people lean into the ropes and the sledge with the stone slides forward over the logs, grass moves "
            "in the wind, slow tracking shot"),
    "S08": ("Upright vertical portrait photo, eye-level view from the shore, horizon level across the frame, sky at the top. A large flat reddish sandstone slab tied onto a wide wooden raft made of lashed log boats, paddled by "
            "Neolithic people along a rugged rocky Scottish coastline, grey sea, dramatic clouds, wide shot, figures "
            "small", ""),
    "S11": ("A great crowd of Neolithic people from many communities gathered at sunset around a huge ring of "
            "standing stones on a grassy plain, campfires and smoke, people seen from behind, wide shot", ""),
    "S13": ("The complete ring of giant standing stones with lintels on top, as it looked 4,500 years ago, on a "
            "lonely grassy plain under the Milky Way, faint dawn glow on the horizon, nobody there, mysterious, "
            "wide shot",
            "stars slowly wheel over the stone circle, a faint glow spreads on the horizon, slow aerial pull-back"),
}
VIDEO = ("S01", "S06", "S13")

# picked still per scene after looking at footage/cand ('a' or 'b')
PICK = {"S01": "a", "S06": "e", "S08": "d", "S11": "b", "S13": "a"}


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
        seeds = (("e" if "--e" in sys.argv else "d", 3705 if "--e" in sys.argv else 3704),) if "--redo" in sys.argv else (("a", 3701), ("b", 3702))
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
