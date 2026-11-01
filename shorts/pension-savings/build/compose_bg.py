"""AI clay paintings as their own moving layer, plus a soft vignette overlay.

For each scene, ai_bg/Sxx.png (kept in colour) is written to parts/Sxx/ai.png, the bottom layer
that gen_effectcraft.py drifts slowly (kenburns) under the translucent paper bg layer. The
scene preview scenes/Sxx.png gets the painting composited underneath. Also writes film.png
(a soft vignette, no grain) that sits over every scene in the main comp.
"""
import os

import numpy as np
from PIL import Image, ImageFilter

ROOT = os.path.dirname(os.path.abspath(__file__))
W, H = 1080, 1920
CARD = (245, 243, 238, 255)


def backdrop(sid):
    path = os.path.join(ROOT, "ai_bg", f"{sid}.png")
    if not os.path.exists(path):
        return Image.new("RGBA", (W, H), CARD)
    im = Image.open(path).convert("RGB")
    s = max(W / im.width, H / im.height)
    im = im.resize((round(im.width * s), round(im.height * s)), Image.LANCZOS)
    x, y = (im.width - W) // 2, (im.height - H) // 2
    # keep the clay colours, slightly softened so the cards read on top
    return im.crop((x, y, x + W, y + H)).filter(ImageFilter.GaussianBlur(0.6)).convert("RGBA")


def film():
    """Soft dark-teal oval vignette, mostly transparent."""
    yy, xx = np.mgrid[0:H, 0:W]
    r = np.sqrt(((xx - W / 2) / (W * 0.62)) ** 2 + ((yy - H / 2) / (H * 0.62)) ** 2)
    rgba = np.zeros((H, W, 4), np.uint8)
    rgba[..., :3] = (20, 40, 46)
    rgba[..., 3] = (np.clip((r - 0.6) / 0.5, 0, 1) ** 1.8 * 110).astype(np.uint8)
    Image.fromarray(rgba, "RGBA").save(os.path.join(ROOT, "film.png"))


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
    print(f"composed backgrounds, {n} with AI art, vignette overlay")


if __name__ == "__main__":
    main()
