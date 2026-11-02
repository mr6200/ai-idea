"""Shorts thumbnail (1080x1920): the S01 webtoon illustration under the headline, drawn with the scene helpers."""
import os
import subprocess

from PIL import Image

from compose_bg import backdrop
from gen_scenes import INK, RED, SKY, YELLOW, bg, bubble, head, sfx, svg

ROOT = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(ROOT, "..", "thumbnail")

body = (
    bg()
    + head("첫 월급 받으면", 540, 290, 120)
    + head("꼭 할 3가지!", 540, 440, 140, YELLOW)
    + bubble(["이것부터", "해야 해요!"], 560, 1180, 440, 220, (640, 1460), 56, [INK, RED])
    + sfx("띠링!", 230, 1640, 130, SKY)
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
    Image.alpha_composite(backdrop("S01"), Image.open(png).convert("RGBA")).convert("RGB").save(png)
    print("wrote", OUT)


if __name__ == "__main__":
    main()
