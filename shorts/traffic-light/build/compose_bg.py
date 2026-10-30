"""AI paintings as their own moving layer, plus the old-film overlay.

For each scene, ai_bg/Sxx.png is toned sepia and written to parts/Sxx/ai.png, the bottom layer
that gen_effectcraft.py drifts slowly (kenburns) under the translucent paper bg layer. The
scene preview scenes/Sxx.png gets the painting composited underneath. Also writes film.png
(vignette + grain) that sits over every scene in the main comp.
"""
import os

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageOps

ROOT = os.path.dirname(os.path.abspath(__file__))
W, H = 1080, 1920
PAPER = (239, 226, 196, 255)


def backdrop(sid):
    path = os.path.join(ROOT, "ai_bg", f"{sid}.png")
    if not os.path.exists(path):
        return Image.new("RGBA", (W, H), PAPER)
    im = Image.open(path).convert("RGB")
    s = max(W / im.width, H / im.height)
    im = im.resize((round(im.width * s), round(im.height * s)), Image.LANCZOS)
    x, y = (im.width - W) // 2, (im.height - H) // 2
    # one sepia ink tone for every scene, a touch of softness so it reads as backdrop
    im = ImageOps.colorize(ImageOps.grayscale(im.crop((x, y, x + W, y + H))), black="#24170f", white="#f6ead0")
    return im.filter(ImageFilter.GaussianBlur(0.8)).convert("RGBA")


def film():
    """Dark oval vignette with sparse grain and a few faint scratches, mostly transparent."""
    yy, xx = np.mgrid[0:H, 0:W]
    r = np.sqrt(((xx - W / 2) / (W * 0.62)) ** 2 + ((yy - H / 2) / (H * 0.62)) ** 2)
    alpha = np.clip((r - 0.55) / 0.5, 0, 1) ** 1.6 * 170
    rgba = np.zeros((H, W, 4), np.uint8)
    rgba[..., :3] = (20, 12, 6)
    rgba[..., 3] = alpha.astype(np.uint8)
    rng = np.random.default_rng(12)
    n = 9000
    ys, xs = rng.integers(0, H, n), rng.integers(0, W, n)
    light = rng.random(n) < 0.5
    rgba[ys, xs, :3] = np.where(light[:, None], 235, 25)
    rgba[ys, xs, 3] = np.maximum(rgba[ys, xs, 3], rng.integers(30, 90, n))
    im = Image.fromarray(rgba, "RGBA")
    d = ImageDraw.Draw(im)
    for x in rng.integers(80, W - 80, 5):
        d.line((int(x), 0, int(x) + int(rng.integers(-20, 20)), H), fill=(250, 240, 220, 40), width=2)
    im.save(os.path.join(ROOT, "film.png"))


def main():
    n = 0
    for sid in sorted(os.listdir(os.path.join(ROOT, "svg"))):
        if not sid.startswith("S"):
            continue
        base = backdrop(sid)
        base.save(os.path.join(ROOT, "parts", sid, "ai.png"))
        prev = os.path.join(ROOT, "..", "scenes", f"{sid}.png")
        Image.alpha_composite(base, Image.open(prev).convert("RGBA")).save(prev)
        n += os.path.exists(os.path.join(ROOT, "ai_bg", f"{sid}.png"))
    film()
    print(f"composed backgrounds, {n} with AI art, film overlay")


if __name__ == "__main__":
    main()
