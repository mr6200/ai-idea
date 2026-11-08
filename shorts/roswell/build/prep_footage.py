"""Footage for every scene: parts/Sxx/video.mp4 (WAN clip) or parts/Sxx/still.png (Ken Burns still), plus film.png.

Only the key scenes are WAN clips (user rule from mystery episode 2: 3-4 video scenes, the rest stills moved by
a slow Ken Burns camera in EffectCraft, one clip per scene at most). A WAN clip is about 5 s and is slowed to
fit its scene and motion-interpolated to 30 fps (ffmpeg minterpolate at 720x1280, then scaled to 1080x1920).
Stills get the same colour grade as the clips. film.png is a soft vignette that sits over every scene in the
main comp. scenes/Sxx.png previews (scene still + overlay) are written too.
"""
import json
import os
import subprocess
import sys

import numpy as np
from PIL import Image, ImageEnhance, ImageFilter

from gen_footage import PICK

ROOT = os.path.dirname(os.path.abspath(__file__))
FOOT = os.path.join(ROOT, "footage")
W, H = 1080, 1920
PAD = 0.2      # scene precomps run 0.2 s past their end
SPLIT = {}   # scene-local second where a second clip starts (not used: one clip per scene)
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
    """Write the scene's bottom layer: the fitted WAN clip, or the graded Ken Burns still."""
    sid = sc["id"]
    os.makedirs(os.path.join(ROOT, "parts", sid), exist_ok=True)
    for part in sc["parts"]:
        a = part["anim"]
        if a["type"] == "kenburns":
            load_src(a["src"]).convert("RGB").save(os.path.join(ROOT, "parts", sid, part["name"] + ".png"))
        elif a["type"] == "video":
            clips = a["clips"]
            length = sc["end"] - sc["start"] + PAD
            out = os.path.join(ROOT, "parts", sid, "video.mp4")
            if len(clips) == 1:
                fit(os.path.join(FOOT, f"{clips[0]}.mp4"), length, out)
                continue
            cut = SPLIT[sid]
            first, second = out + ".a.mp4", out + ".b.mp4"
            fit(os.path.join(FOOT, f"{clips[0]}.mp4"), cut, first)
            fit(os.path.join(FOOT, f"{clips[1]}.mp4"), length - cut, second)
            lst = out + ".txt"
            with open(lst, "w") as f:
                f.write(f"file '{first}'\nfile '{second}'\n")
            subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", lst, "-c", "copy", out], check=True)
            for x in (first, second, lst):
                os.remove(x)


def grade(im):
    im = im.convert("RGB").resize((W, H), Image.LANCZOS)
    return ImageEnhance.Contrast(ImageEnhance.Color(im).enhance(0.86)).enhance(1.05).convert("RGBA")


def archive_frame(im):
    """A real archive image (photos/, user rule from mystery episode 4) shown whole: fitted inside the frame
    between the label band and the subtitles, over a blurred, darkened copy of itself. Not colour-graded."""
    im = im.convert("RGB")
    sw, sh = im.size
    s = max(W / sw, H / sh)
    bg = im.resize((round(sw * s), round(sh * s)), Image.LANCZOS)
    bg = bg.crop(((bg.width - W) // 2, (bg.height - H) // 2, (bg.width - W) // 2 + W, (bg.height - H) // 2 + H))
    bg = ImageEnhance.Brightness(bg.filter(ImageFilter.GaussianBlur(28))).enhance(0.4)
    box_w, box_h, top = 960, 1060, 340
    s = min(box_w / sw, box_h / sh)
    fg = im.resize((round(sw * s), round(sh * s)), Image.LANCZOS)
    bg.paste(fg, ((W - fg.width) // 2, top + (box_h - fg.height) // 2))
    return bg.convert("RGBA")


def load_src(src):
    """Ken Burns source: 'photos/<file>' is a real archive image, anything else a Seedream still in footage/cand."""
    if src.startswith("photos/"):
        return archive_frame(Image.open(os.path.join(ROOT, src)))
    return grade(Image.open(os.path.join(FOOT, "cand", src + ".jpg")))


def scene_still(sc):
    """The still a scene starts from (its Ken Burns still, or the still its WAN clip was made from)."""
    for part in sc["parts"]:
        a = part["anim"]
        if a["type"] == "kenburns":
            return load_src(a["src"])
        if a["type"] == "video":
            return still(a["clips"][0])
    raise ValueError(sc["id"])


def still(name):
    """Picked Seedream still with the same grade (for scene previews, storyboard and thumbnail)."""
    return grade(Image.open(os.path.join(FOOT, "cand", f"{name}_{PICK.get(name, 'a')}.jpg")))


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
        Image.alpha_composite(scene_still(sc), Image.open(prev).convert("RGBA")).convert("RGB").save(prev)
        print(sc["id"], "footage ready", flush=True)
    film()


if __name__ == "__main__":
    main()
