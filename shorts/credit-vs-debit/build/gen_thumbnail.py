"""Shorts thumbnail (1080x1920): the S01 webtoon illustration under the headline, drawn with the scene helpers."""
import os
import subprocess

from PIL import Image

from compose_bg import backdrop
from gen_scenes import INK, ORANGE, RED, YELLOW, bg, bubble, head, sfx, svg

ROOT = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(ROOT, "..", "thumbnail")

body = (
    bg()
    + head("체크카드만 쓰면", 540, 290, 116)
    + head("손해일까?", 540, 440, 140, YELLOW)
    + bubble(["진짜", "손해라고?!"], 580, 1180, 420, 220, (660, 1460), 58, [INK, RED])
    + sfx("반전!", 230, 1640, 130, ORANGE)
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
