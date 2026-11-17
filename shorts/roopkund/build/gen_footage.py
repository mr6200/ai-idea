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

LOOK = ("Documentary film still, vertical 9:16 frame, realistic photograph, the high Himalaya of Uttarakhand, "
        "India, thin cold air, rocky glacial terrain, natural colours, 35mm film grain, cinematic. ")
NEG = ("text, letters, writing, signboard, watermark, logo, flag, gore, blood, flesh, cartoon, illustration, 3d render, "
       "deformed face, extra fingers, distorted hands, rotated image, sideways image")

# scene -> (still prompt, motion prompt). Only VIDEO scenes are animated by WAN; real CC BY-SA photos (photos/)
# carry the documentary scenes, the rest are Seedream stills moved with a Ken Burns camera (user rules).
# Clip jobs are submitted one at a time and their ids saved to footage/jobs.json (see clip()).
SCENES = {
    "S01": ("A small round glacial lake high in the Himalaya at dawn, surrounded by grey scree slopes and patches of "
            "snow, thin mist drifting over the clear shallow water, a few pale old bones faintly visible on the stony "
            "lake bed near the shore, eerie and silent, wide shot from the rim",
            "mist drifts slowly over the still water, a little snow blows off the ridge, very slow push-in toward "
            "the lake"),
    "S03": ("A 1942 Indian forest ranger in a khaki uniform and wool cap seen from behind, standing on a rocky snowy "
            "Himalayan slope above a small half-frozen lake, looking down, overcast, cold mist", ""),
    "S05": ("An ancient royal pilgrimage procession of hundreds of people in medieval Indian clothes climbing a narrow "
            "snowy Himalayan mountain path in a long line, banners and palanquins, dark storm clouds gathering above, "
            "seen from far away, figures small", ""),
    "S06": ("A sudden violent hailstorm in the high Himalaya, huge white hailstones the size of cricket balls "
            "bouncing on grey rocks and snow, dark sky, people far away in cloaks running for cover, figures small "
            "and anonymous",
            "large hailstones fall hard and bounce on the rocks, the wind blows, the distant figures run, handheld "
            "documentary camera"),
    "S08": ("A modern genetics laboratory, a scientist in a white coat, mask and gloves holding a small old bone "
            "fragment with tweezers over a clean bench, a DNA sequencer and sample tubes behind, blue light, face "
            "covered by mask", ""),
    "S10": ("A small group of 19th century travellers in dusty European clothes and hats walking up a snowy "
            "Himalayan pass in a line, porters with loads, seen from far behind, figures small and anonymous, "
            "misty and lonely, historical reconstruction", ""),
    "S12": ("A high Himalayan glacial lake at sunset under towering snowy peaks, golden light on the summits, the "
            "lake half frozen and calm, nobody there, mysterious",
            "clouds move slowly over the peaks, the golden light fades, a little mist rises from the lake, slow "
            "pull-back"),
}
VIDEO = ("S01", "S06", "S12")

# picked still per scene after looking at footage/cand ('a' or 'b')
PICK = {"S01": "a", "S03": "a", "S05": "a", "S06": "a", "S08": "a", "S10": "a", "S12": "a"}


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
        seeds = (("e" if "--e" in sys.argv else "d", 3305 if "--e" in sys.argv else 3304),) if "--redo" in sys.argv else (("a", 3301), ("b", 3302))
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
