"""Shorts thumbnail (1080x1920): the S01 webtoon illustration under the headline, drawn with the scene helpers."""
import os
import subprocess

from PIL import Image

from compose_bg import backdrop
from gen_scenes import INK, RED, YELLOW, bg, bubble, head, sfx, svg

ROOT = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(ROOT, "..", "thumbnail")

body = (
    bg()
    + head("월급, 왜", 540, 330, 150)
    + head("3일 만에", 540, 500, 150, YELLOW)
    + head("사라질까?", 540, 670, 150, YELLOW)
    + bubble(["어?! 내 월급", "어디 갔어?!"], 560, 1180, 460, 220, (640, 1460), 56, [INK, RED])
    + sfx("털썩", 220, 1640, 130)
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
