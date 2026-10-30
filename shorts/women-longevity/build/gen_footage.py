"""Documentary footage for every scene through Runpod Public Endpoints (no endpoint to create or delete).

  python gen_footage.py images   -> Seedream 4.0 stills, two seeds per scene: footage/cand/Sxx_{a,b}.jpg ($0.027 each)
  python gen_footage.py video    -> WAN 2.2 I2V 720p animates the picked still (PICK): footage/Sxx.mp4 ($0.30 per 5 s clip)
  python gen_footage.py images S07 --redo -> one more still with a new seed (Sxx_d; earlier redo seeds: c = 1703)
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

LOOK = ("Documentary film still, vertical 9:16 frame, realistic photograph, natural skin texture, "
        "soft natural light, shallow depth of field, 35mm film look, muted warm colour grade. ")
NEG = "text, letters, watermark, logo, cartoon, illustration, 3d render, deformed face, extra fingers, distorted hands"

# scene -> (still prompt, motion prompt)
SCENES = {
    "S01": ("An elderly Korean couple in their 80s sitting on a wooden park bench in autumn, the grandmother smiling warmly "
            "in the foreground, the grandfather beside her, golden afternoon light, falling leaves",
            "the grandmother smiles and turns her head slightly toward the grandfather, leaves drift down, gentle slow push-in"),
    "S02": ("Three Korean grandmothers in their late 80s walking together briskly along a riverside path in the morning, "
            "wearing sun visors and light jackets, laughing, Seoul apartment towers far behind, soft haze",
            "the grandmothers walk toward the camera chatting and laughing, slow tracking shot backward"),
    "S03": ("A Korean female scientist in a white lab coat looking into a microscope in a modern genetics laboratory, "
            "blue monitor light showing a chromosome image, glass test tubes, cool tones",
            "she adjusts the microscope focus knob and leans closer, monitor light flickers softly, slow dolly in"),
    "S04": ("Extreme close-up of a DNA double helix model and chromosome karyotype photos on a light table in a laboratory, "
            "a gloved hand holding tweezers, scientific documentary macro shot, blue and white light",
            "slow macro camera slide across the light table, the gloved hand moves a photo, subtle light shimmer"),
    "S05": ("A Korean female doctor with a stethoscope listening to the heartbeat of a smiling Korean woman in her 50s "
            "in a bright clinic examination room, a heart monitor in the background",
            "the doctor moves the stethoscope gently and nods, the patient breathes calmly, heart monitor line pulses, slow push-in"),
    "S06": ("A muscular young Korean man in his 20s lifting a heavy barbell in a gritty gym at night, sweat, "
            "dramatic side light, intense expression",
            "he lifts the barbell up with effort and lowers it, chalk dust floats in the light, slow handheld camera"),
    "S07": ("Historical drama reenactment: a dignified elderly Korean court eunuch of the Joseon dynasty, completely clean-shaven smooth face with no beard and no mustache, soft features, "
            "wearing a dark blue dallyeong official robe and a black silk samo court cap with two small wings at the back (not a wide-brimmed gat), standing in a wooden corridor of Gyeongbokgung palace, "
            "soft morning light through paper doors",
            "the old court official walks slowly along the palace corridor with hands folded in his sleeves, slow tracking shot"),
    "S08": ("A tired Korean office worker man in his 40s smoking a cigarette at night outside a street food tent bar, "
            "green soju bottles on a plastic table, neon lights reflecting on wet pavement, cinematic night",
            "he exhales cigarette smoke slowly and looks away, neon lights flicker, smoke drifts, slow push-in"),
    "S09": ("A newborn baby girl sleeping in a hospital nursery bassinet wrapped in a soft pink blanket, "
            "a nurse's gentle hand touching her tiny hand, warm soft light",
            "the baby stirs and her tiny fingers curl around the nurse's finger, gentle slow push-in"),
    "S10": ("An elderly Korean woman in her late 80s sitting by a hospital window holding a cup of tea, an IV stand beside her, "
            "a caring nurse adjusting her blanket, calm overcast light",
            "the elderly woman looks out the window and sips tea slowly while the nurse tucks the blanket, slow push-in"),
    "S11": ("A pair of mandarin ducks swimming on a calm pond in a Korean palace garden, the colourful male and the brown female "
            "side by side, autumn trees reflected on the water, wildlife documentary telephoto shot",
            "the two ducks glide slowly across the pond, ripples spread, leaves float on the water, slow pan"),
    "S11b": ("Close-up of a male mandarin duck with vivid orange sail feathers standing on a mossy rock by a pond, "
             "wildlife documentary telephoto shot, soft background bokeh",
             "the male duck turns his head, ruffles his feathers and looks around, water sparkles behind, slow push-in"),
    "S12": ("A Korean man in his 40s jogging along the Han River at sunrise in running clothes, city bridge behind him, "
            "golden rim light, healthy and determined",
            "he jogs toward the camera with steady breathing, sunrise light flares, slow tracking shot backward"),
    "S12b": ("A Korean man in his 40s having a health checkup, a Korean doctor in a white coat explaining a chest X-ray "
             "on a monitor to him in a bright hospital office, the man listening and nodding",
             "the doctor points at the X-ray on the monitor and explains, the man nods slowly, slow push-in"),
}

# picked still per scene after looking at footage/cand ('a' or 'b')
PICK = {"S01": "a", "S02": "b", "S03": "a", "S04": "a", "S05": "a", "S06": "a", "S07": "b", "S08": "a",
        "S09": "a", "S10": "a", "S11": "b", "S11b": "a", "S12": "b", "S12b": "a"}


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
        seeds = (("d", 1704),) if "--redo" in sys.argv else (("a", 1701), ("b", 1702))
        jobs = [(s, v, seed) for s in only if s != "--redo" for v, seed in seeds]
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
