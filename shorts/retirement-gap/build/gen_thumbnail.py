"""Shorts thumbnail (1080x1920): the S01 clay painting under the infographic, drawn with the scene helpers."""
import os
import subprocess

from PIL import Image

from compose_bg import backdrop
from gen_scenes import RED, WHITE, YELLOW, bg, card, head, pill, svg, timeline

ROOT = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(ROOT, "..", "thumbnail")

body = (
    bg()
    + head("60세 퇴직,", 540, 430, 130)
    + head("연금은 65세?", 540, 590, 130, YELLOW)
    + card(80, 1180, 920, 420) + timeline(1360)
    + pill("5년 공백, 어떻게 메울까?", 540, 1720, 56, RED, WHITE)
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
