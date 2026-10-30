"""AI scene backgrounds from the Runpod Public Endpoint for Seedream 4.0 (no endpoint to create or delete).

Draws ai_bg/Sxx.png at 1080x1920 from the prompts in gen_backgrounds.py ($0.027 per image).
Existing images are kept, so delete ai_bg/Sxx.png to redraw one scene; SEED + scene number, or
pass --seed N to try another. Calls go through curl because Python's urllib gets 403 from the proxy.
    python gen_backgrounds_seedream.py [S03 S07 ...] [--seed 2]
"""
import json
import os
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor

from gen_backgrounds import NEGATIVE, OUT, SCENES, STYLE

URL = "https://api.runpod.ai/v2/seedream-v4-t2i/runsync"
SEED = 2000


def draw(sid, seed):
    body = {"input": {"prompt": f"{SCENES[sid]}, {STYLE}", "negative_prompt": NEGATIVE, "size": "1080*1920",
                      "seed": seed + int(sid[1:]), "enable_safety_checker": True}}
    for _ in range(3):
        r = subprocess.run(["curl", "-sS", "-m", "300", "-X", "POST", URL, "-H", f"Authorization: Bearer {os.environ['RUNPOD_API_KEY']}",
                            "-H", "Content-Type: application/json", "-d", json.dumps(body)], capture_output=True, text=True)
        try:
            res = json.loads(r.stdout)
        except json.JSONDecodeError:
            continue
        if res.get("status") == "COMPLETED":
            jpg = os.path.join(OUT, f"{sid}.jpg")
            subprocess.run(["curl", "-sS", "-o", jpg, res["output"]["result"]], check=True)
            subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", jpg, os.path.join(OUT, f"{sid}.png")], check=True)
            os.remove(jpg)
            return f"{sid} done (${res['output'].get('cost')})"
    return f"{sid} failed: {r.stdout[:200]}"


def main():
    args = sys.argv[1:]
    seed = SEED
    if "--seed" in args:
        i = args.index("--seed")
        seed += 100 * int(args[i + 1])
        del args[i:i + 2]
    os.makedirs(OUT, exist_ok=True)
    todo = [s for s in (args or SCENES) if not os.path.exists(os.path.join(OUT, f"{s}.png"))]
    with ThreadPoolExecutor(8) as ex:
        for line in ex.map(lambda s: draw(s, seed), todo):
            print(line, flush=True)


if __name__ == "__main__":
    main()
