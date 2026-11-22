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

LOOK = ("Documentary film still, vertical 9:16 frame, realistic photograph, prehistoric Stone Age reconstruction, "
        "natural light, rich natural colours, 35mm film grain, cinematic. ")
NEG = ("text, letters, writing, signboard, watermark, logo, flag, modern buildings, cars, tourists, metal tools, pyramids, cartoon, "
       "illustration, 3d render, deformed face, extra fingers, distorted hands, rotated image, sideways image")

# scene -> (still prompt, motion prompt). Only VIDEO scenes are animated by WAN; real CC0 / CC BY / CC BY-SA photos
# (photos/) carry the comparison scenes (user rules). Clip jobs are submitted one at a time and their ids saved
# to footage/jobs.json (see clip()).
SCENES = {
    "S01": ("A ring of huge T-shaped carved limestone pillars standing on a bare hilltop at night 11,600 years ago, "
            "a group of hunter-gatherers in animal-skin clothing gathered around a fire in the middle, firelight on "
            "the stone, a starry sky, wide shot, figures small, mysterious and awe-inspiring",
            "the fire flickers and sparks rise, firelight dances on the stone pillars, the people move slightly, "
            "slow push-in"),
    "S07": ("Close-up of the rough hands of a Stone Age hunter-gatherer chipping at a monochrome beige limestone "
            "pillar with a sharp flint stone, a half-finished wild boar carved in low relief in the stone itself like "
            "an archaeological stone sculpture, grey-beige stone only, no colours, stone chips and dust, warm side "
            "light, shallow depth of field", ""),
    "S08": ("Dozens of Stone Age hunter-gatherers in animal-skin clothing using thick ropes, wooden levers and log "
            "rollers to drag a huge T-shaped limestone pillar across a rocky limestone plateau, dust in golden light, "
            "wide shot, figures small",
            "the people pull the ropes together and the stone pillar slides slowly forward on the logs, dust rises, "
            "slow tracking shot"),
    "S09": ("A large gathering of Stone Age hunter-gatherer groups feasting at night among T-shaped stone pillars on "
            "a hilltop, roasting wild game over fires, people seen from behind, firelight and smoke, wide shot", ""),
    "S10": ("Close-up of Stone Age hands holding ears of wild einkorn wheat over a flat grinding stone, a field of "
            "wild grasses on rolling hills behind, golden evening light, shallow depth of field", ""),
    "S13": ("A ring of huge T-shaped carved limestone pillars on a lonely hilltop under the Milky Way, faint blue "
            "dawn light on the horizon, nobody there, ancient and mysterious, wide shot",
            "stars slowly wheel over the stone pillars, a faint glow spreads on the horizon, slow aerial pull-back"),
}
VIDEO = ("S01", "S08", "S13")

# picked still per scene after looking at footage/cand ('a' or 'b')
PICK = {"S01": "b", "S07": "e", "S08": "a", "S09": "a", "S10": "a", "S13": "a"}


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
        seeds = (("e" if "--e" in sys.argv else "d", 3605 if "--e" in sys.argv else 3604),) if "--redo" in sys.argv else (("a", 3601), ("b", 3602))
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
