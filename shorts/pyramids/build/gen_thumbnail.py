"""Shorts thumbnail (1080x1920): the S01 ghost-ship still with the headline and the hook."""
import os
import subprocess

from PIL import Image

from gen_scenes import GOLD, RED, head, pill, shade, svg, text
from prep_footage import still

ROOT = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(ROOT, "..", "thumbnail")

OUT_LINE = 'stroke="#000" stroke-opacity="0.7" stroke-width="7" paint-order="stroke"'
# the ship sits in the upper half of the still, so the title goes on the sea below it
# title chosen by the user before the thumbnail was made: 「이집트 vs 멕시코, 피라미드의 차이」
# background: the real Giza photo (left half) and the real Chichen Itza photo (right half), side by side
body = (
    shade()
    + '<rect width="1080" height="820" fill="#000" fill-opacity="0.35"/>'
    + '<rect x="536" y="820" width="8" height="1100" fill="#ffffff" fill-opacity="0.85"/>'
    + head("이집트 vs 멕시코", 540, 420, 126)
    + head("피라미드의 차이", 540, 590, 136, GOLD)
    + pill("만난 적 없는 두 문명", 540, 750, 56, RED, "#ffffff")
    + text("이집트", 270, 1640, 64, "#ffffff", extra=OUT_LINE)
    + text("멕시코", 810, 1640, 64, "#ffffff", extra=OUT_LINE)
)


def split_background():
    """Left half: Giza (photos/giza_khufu.jpg), right half: Chichen Itza (photos/kukulcan.jpg), each cover-cropped."""
    out = Image.new("RGB", (1080, 1920))
    for i, name in enumerate(("giza_khufu.jpg", "kukulcan.jpg")):
        im = Image.open(os.path.join(ROOT, "photos", name)).convert("RGB")
        s = max(540 / im.width, 1920 / im.height)
        im = im.resize((round(im.width * s), round(im.height * s)), Image.LANCZOS)
        x0 = (im.width - 540) // 2
        out.paste(im.crop((x0, (im.height - 1920) // 2, x0 + 540, (im.height - 1920) // 2 + 1920)), (i * 540, 0))
    return out.convert("RGBA")


def main():
    os.makedirs(OUT, exist_ok=True)
    src = os.path.join(OUT, "thumbnail.svg")
    with open(src, "w") as f:
        f.write(svg(body))
    for ext in ("vectorcraft", "png"):
        subprocess.run(["vectorcraft-cli", "convert", src, os.path.join(OUT, f"thumbnail.{ext}")],
                       check=True, capture_output=True)
    png = os.path.join(OUT, "thumbnail.png")
    Image.alpha_composite(split_background(), Image.open(png).convert("RGBA")).convert("RGB").save(png)
    print("wrote", OUT)


if __name__ == "__main__":
    main()
