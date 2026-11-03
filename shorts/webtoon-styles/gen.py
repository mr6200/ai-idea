"""Five webtoon drawing-style samples of the same scene (Seedream 4.0, Runpod Public Endpoint, $0.027 each)."""
import json, os, subprocess, sys
from concurrent.futures import ThreadPoolExecutor
URL = "https://api.runpod.ai/v2/seedream-v4-t2i/runsync"
CHAR = "a young korean office worker man with short black hair, white shirt and navy tie"
SUBJ = f"{CHAR} running up in shock to a bank entrance as a metal shutter comes down in the late afternoon, plain wall with no signboard"
TAIL = ", vertical 9:16 composition, no text, no letters, no numbers, no speech bubbles"
P = {
    "1_watercolor": SUBJ + ", soft watercolor korean romance webtoon style, delicate thin line art, pastel washes, warm golden sunset light, dreamy glow, gentle shading" + TAIL,
    "2_chibi": SUBJ + ", super deformed chibi gag webtoon style, big head small body, huge round eyes, exaggerated shocked face with sweat drops, thick black outlines, bright candy colors, comedic speed lines" + TAIL,
    "3_manga": SUBJ + ", black and white korean manhwa style, crisp ink line art, halftone screentone shading, dramatic speed lines, high contrast, only one red accent color on the tie" + TAIL,
    "4_action": SUBJ + ", semi-realistic action fantasy webtoon style, dramatic cinematic lighting, rim light, saturated colors, detailed rendering, glowing sunset, dynamic low angle" + TAIL,
    "5_simple": SUBJ + ", minimal korean instagram daily life webtoon style, simple doodle line drawing, round cute face with dot eyes, flat limited colors, lots of white space, hand drawn wobbly lines" + TAIL,
}
NEG = "text, letters, words, numbers, speech bubble, watermark, logo, signature, deformed, extra fingers"

def draw(k):
    if os.path.exists(f"{k}.jpg"):
        return k, "kept"
    body = {"input": {"prompt": P[k], "negative_prompt": NEG, "size": "1080*1920", "seed": 2701 + int(sys.argv[1]) * 100 if len(sys.argv) > 1 else 2701, "enable_safety_checker": True}}
    r = subprocess.run(["curl", "-sS", "-m", "300", "-X", "POST", URL, "-H", f"Authorization: Bearer {os.environ['RUNPOD_API_KEY']}", "-H", "Content-Type: application/json", "-d", json.dumps(body)], capture_output=True, text=True)
    res = json.loads(r.stdout)
    subprocess.run(["curl", "-sS", "-o", f"{k}.jpg", res["output"]["result"]], check=True)
    return k, res["output"].get("cost")

with ThreadPoolExecutor(5) as ex:
    for x in ex.map(draw, P):
        print(x, flush=True)
