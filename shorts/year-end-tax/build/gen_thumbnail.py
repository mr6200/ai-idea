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
    + head("연말정산,", 540, 260, 130)
    + head("12월에 끝난다!", 540, 400, 116, YELLOW)
    + bubble(["1월 아니었어?!"], 560, 1330, 470, 130, (700, 1440), 54)
    + sfx("12월 31일 마감!", 330, 1640, 90, ORANGE)
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
