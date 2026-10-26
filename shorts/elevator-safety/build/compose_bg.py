"""Lay each scene's AI engraving (ai_bg/Sxx.png), toned sepia, under its translucent paper bg layer.

Writes parts/Sxx/bg.png (what EffectCraft uses) and scenes/Sxx.png (previews). Scenes
without an AI image get a solid paper base, so the build also works without ai_bg/.
"""
import os

from PIL import Image, ImageFilter, ImageOps

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
    # one sepia ink tone for every scene, slightly softened so it reads as backdrop
    im = ImageOps.colorize(ImageOps.grayscale(im.crop((x, y, x + W, y + H))), black="#2b1d14", white="#f3e7cc")
    return im.filter(ImageFilter.GaussianBlur(1.5)).convert("RGBA")


def main():
    n = 0
    for sid in sorted(os.listdir(os.path.join(ROOT, "svg"))):
        if not sid.startswith("S"):
            continue
        base = backdrop(sid)
        for path in (os.path.join(ROOT, "parts", sid, "bg.png"), os.path.join(ROOT, "..", "scenes", f"{sid}.png")):
            Image.alpha_composite(base, Image.open(path).convert("RGBA")).save(path)
        n += os.path.exists(os.path.join(ROOT, "ai_bg", f"{sid}.png"))
    print(f"composed backgrounds, {n} with AI art")


if __name__ == "__main__":
    main()
