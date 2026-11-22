"""Shorts thumbnail (1080x1920): the S01 still (ring of T-shaped pillars by firelight) with the title."""
import os
import subprocess

from PIL import Image

from gen_scenes import GOLD, RED, head, pill, shade, svg
from prep_footage import still

ROOT = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(ROOT, "..", "thumbnail")

# title chosen by the user before the thumbnail was made: 「피라미드보다 7,000년 앞선 신전」
# the pillars and the fire sit in the lower half of the still, so the title goes on the night sky above them
body = (
    shade()
    + head("피라미드보다", 540, 440, 130)
    + head("7,000년 앞선 신전", 540, 610, 112, GOLD)
    + pill("약 1만 1,600년 전 · 튀르키예", 540, 770, 54, RED, "#ffffff")
)


def main():
    os.makedirs(OUT, exist_ok=True)
    src = os.path.join(OUT, "thumbnail.svg")
    with open(src, "w") as f:
        f.write(svg(body))
    for ext in ("vectorcraft", "png"):
        subprocess.run(["vectorcraft-cli", "convert", src, os.path.join(OUT, f"thumbnail.{ext}")],
                       check=True, capture_output=True)
    png = os.path.join(OUT, "thumbnail.png")
    Image.alpha_composite(still("S01"), Image.open(png).convert("RGBA")).convert("RGB").save(png)
    print("wrote", OUT)


if __name__ == "__main__":
    main()
