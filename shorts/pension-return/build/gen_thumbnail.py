"""Shorts thumbnail (1080x1920): the S01 clay painting under the infographic, drawn with the scene helpers."""
import os
import subprocess

from PIL import Image

from compose_bg import backdrop
from gen_scenes import RED, WHITE, YELLOW, bg, card, head, pill, ratio_bars, svg, text

ROOT = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(ROOT, "..", "thumbnail")

# the paid-vs-received bars from S05, moved down to sit under the headline
body = (
    bg()
    + head("국민연금,", 540, 420, 130)
    + head("낸 돈보다 더?", 540, 580, 140, YELLOW)
    + f'<g transform="translate(0 260)">{card(110, 600, 860, 700) + text("평균 소득자 · 개혁 후", 540, 680, 40) + ratio_bars()}</g>'
    + pill("약 1.6~2배 받는다", 540, 1720, 64, RED, WHITE)
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
