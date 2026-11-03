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
    + head("은행은 왜", 540, 290, 130)
    + head("4시에 문 닫을까?", 540, 440, 118, YELLOW)
    + bubble(["벌써", "닫았어?!"], 580, 1180, 420, 220, (660, 1460), 58, [INK, RED])
    + sfx("철컥!", 230, 1640, 130, RED)
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
