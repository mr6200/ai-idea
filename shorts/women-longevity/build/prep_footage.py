"""Fit the WAN clips to their scenes: parts/Sxx/video.mp4 for every scene, plus the documentary grade and film.png.

A WAN clip is about 5 s; a scene is 5-8.6 s, so each clip is slowed to fit its segment and
motion-interpolated to 30 fps (ffmpeg minterpolate at 720x1280, then scaled to 1080x1920). Scenes
with two clips (S11, S12) cut from the first to the second at SPLIT. The grade is a little less
colour, a touch more contrast, slightly warm, with fine moving grain. film.png is a soft vignette that
sits over every scene in the main comp. scenes/Sxx.png previews (picked still + overlay) are written too.
"""
import json
import os
import subprocess
import sys

import numpy as np
from PIL import Image, ImageEnhance

from gen_footage import PICK

ROOT = os.path.dirname(os.path.abspath(__file__))
FOOT = os.path.join(ROOT, "footage")
W, H = 1080, 1920
PAD = 0.2      # scene precomps run 0.2 s past their end
SPLIT = {"S11": 4.6, "S12": 4.0}   # scene-local second where the second clip starts
GRADE = ("eq=saturation=0.86:contrast=1.05:gamma=0.98,colorbalance=rs=0.03:bs=-0.03:rm=0.02:bm=-0.02,"
         "noise=alls=7:allf=t")


def probe(path):
    out = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "json", path],
                         capture_output=True, text=True, check=True).stdout
    return float(json.loads(out)["format"]["duration"])


def fit(src, length, dst):
    """Slow (or trim) src to exactly `length` seconds, 30 fps, graded, 1080x1920."""
    dur = probe(src) - 0.1   # the last frames of a WAN clip sometimes blur
    factor = max(1.0, length / dur)
    vf = (f"setpts={factor:.4f}*PTS,scale=720:1280,"
          + ("minterpolate=fps=30:mi_mode=mci:mc_mode=aobmc:vsbmc=1," if factor > 1.02 else "fps=30,")
          + f"scale={W}:{H}:flags=lanczos,{GRADE},format=yuv420p")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", src, "-an", "-vf", vf, "-t", f"{length:.3f}",
                    "-c:v", "libx264", "-crf", "16", "-preset", "medium", dst], check=True)


def scene_video(sc):
    sid = sc["id"]
    clips = next(p["anim"]["clips"] for p in sc["parts"] if p["anim"]["type"] == "video")
    length = sc["end"] - sc["start"] + PAD
    out = os.path.join(ROOT, "parts", sid, "video.mp4")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    if len(clips) == 1:
        fit(os.path.join(FOOT, f"{clips[0]}.mp4"), length, out)
        return
    cut = SPLIT[sid]
    a, b = out + ".a.mp4", out + ".b.mp4"
    fit(os.path.join(FOOT, f"{clips[0]}.mp4"), cut, a)
    fit(os.path.join(FOOT, f"{clips[1]}.mp4"), length - cut, b)
    lst = out + ".txt"
    with open(lst, "w") as f:
        f.write(f"file '{a}'\nfile '{b}'\n")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", lst, "-c", "copy", out], check=True)
    for p in (a, b, lst):
        os.remove(p)


def still(name):
    """Picked Seedream still with the same grade (for scene previews, storyboard and thumbnail)."""
    im = Image.open(os.path.join(FOOT, "cand", f"{name}_{PICK.get(name, 'a')}.jpg")).convert("RGB").resize((W, H), Image.LANCZOS)
    im = ImageEnhance.Contrast(ImageEnhance.Color(im).enhance(0.86)).enhance(1.05)
    return im.convert("RGBA")


def film():
    """Soft dark oval vignette, transparent in the middle."""
    yy, xx = np.mgrid[0:H, 0:W]
    r = np.sqrt(((xx - W / 2) / (W * 0.66)) ** 2 + ((yy - H / 2) / (H * 0.66)) ** 2)
    rgba = np.zeros((H, W, 4), np.uint8)
    rgba[..., 3] = (np.clip((r - 0.6) / 0.5, 0, 1) ** 1.5 * 150).astype(np.uint8)
    Image.fromarray(rgba, "RGBA").save(os.path.join(ROOT, "film.png"))


def main():
    with open(os.path.join(ROOT, "manifest_scenes.json")) as f:
        scenes = json.load(f)
    # --previews: only redo the scene previews (after an overlay change), the clips stay as they are
    previews = "--previews" in sys.argv
    only = set(sys.argv[1:]) - {"--previews"}
    for sc in scenes:
        if only and sc["id"] not in only:
            continue
        if not previews:
            scene_video(sc)
        prev = os.path.join(ROOT, "..", "scenes", f"{sc['id']}.png")
        Image.alpha_composite(still(sc["id"]), Image.open(prev).convert("RGBA")).convert("RGB").save(prev)
        print(sc["id"], "footage ready", flush=True)
    film()


if __name__ == "__main__":
    main()
