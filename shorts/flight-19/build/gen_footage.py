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

LOOK = ("Historical documentary film still, vertical 9:16 frame, realistic photograph, December 1945, "
        "US Navy aviation off the coast of Florida, period accuracy, muted blue-grey colours, 35mm film grain, cinematic. ")
NEG = ("text, letters, writing, numbers, signboard, watermark, logo, flag, modern aircraft, jet, cartoon, illustration, "
       "3d render, deformed face, extra fingers, distorted hands, rotated image, sideways image")
PLANE = "dark blue single-engine WWII US Navy torpedo bomber propeller planes with a glass canopy"

# scene -> (still prompt, motion prompt). Only VIDEO scenes are animated by WAN; real US Navy photos (photos/)
# carry the documentary scenes, the rest are Seedream stills moved with a Ken Burns camera (user rules).
SCENES = {
    "S01": (f"Five {PLANE} flying in a loose formation low over the grey Atlantic ocean toward a wall of dark clouds "
            "at dusk, seen from behind and slightly above, the last light on the horizon",
            "the five planes fly steadily away toward the dark clouds, propellers spinning, clouds drift, the light "
            "fades, slow push-in"),
    "S03": ("Inside the cockpit of a 1945 single-engine navy plane, seen from behind the pilot's shoulder, his "
            "gloved hand on the stick, a round magnetic compass and old dials on the instrument panel, grey sea and "
            "clouds through the canopy, the pilot's face not visible", ""),
    "S04": ("A 1945 US Navy airfield radio room at dusk, a radio operator in headphones seen from behind leaning "
            "toward a large old radio set with glowing dials, a microphone on the desk, a window with palm trees "
            "outside, tense mood, face not visible", ""),
    "S05": ("Eye-level view from just above the water of a dark stormy Atlantic ocean at nightfall, a huge rough wave "
            "rising in the foreground with white spray, heavy black clouds above at the top of the frame, the tiny "
            "lights of two small planes far away low under the clouds",
            "the huge wave rolls and crashes, spray blows across the frame, the tiny lights move slowly and fade into "
            "the clouds, handheld documentary camera"),
    "S07": ("Night on the deck of a 1945 oil tanker ship at sea, two sailors in heavy coats seen from behind at the "
            "rail pointing at a tall column of orange flames and black smoke bursting in the dark sky far away above "
            "the horizon, pitch black night, no sun, no moon, firelight flickering on the water", ""),
    "S08": ("Grey dawn over the open Atlantic, a 1945 navy destroyer and two small patrol boats searching the empty "
            "sea, a propeller search plane flying low overhead, wide shot, nothing floating on the water", ""),
    "S10": ("A statistics-like calm scene: a busy shipping lane on a bright calm blue sea near Florida seen from "
            "high above, several cargo ships and sailboats and a small plane crossing peacefully, sunny day", ""),
    "S11": ("The empty calm Atlantic ocean at sunset, gentle swells, golden light on the water, a single seabird, "
            "quiet and mysterious, nothing else",
            "gentle swells roll slowly, the sun sinks toward the horizon, the light on the water shimmers, slow push-in"),
}
VIDEO = ("S01", "S05", "S11")

# picked still per scene after looking at footage/cand ('a' or 'b')
PICK = {"S01": "b", "S03": "a", "S04": "a", "S05": "d", "S07": "d", "S08": "a", "S10": "a", "S11": "a"}


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
        seeds = (("e" if "--e" in sys.argv else "d", 3205 if "--e" in sys.argv else 3204),) if "--redo" in sys.argv else (("a", 3201), ("b", 3202))
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
