"""Shorts thumbnail (1080x1920): the S02 clay house under the infographic, drawn with the scene helpers."""
import os
import subprocess

from PIL import Image

from compose_bg import backdrop
from gen_scenes import RED, TEAL, WHITE, YELLOW, bg, card, coins, head, house, num, pill, svg, text

ROOT = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(ROOT, "..", "thumbnail")

body = (
    bg()
    + head("집 한 채로", 540, 420, 130)
    + head("매달 얼마?", 540, 580, 140, YELLOW)
    + card(110, 860, 860, 700) + house(330, 1300, 0.9) + coins(760, 1300, 7)
    + text("72세 · 4억 원 집", 540, 960, 48) + num("월 약 133만 원", 540, 1460, 100, TEAL)
    + pill("주택연금 장단점", 540, 1720, 64, RED, WHITE)
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
    Image.alpha_composite(backdrop("S02"), Image.open(png).convert("RGBA")).convert("RGB").save(png)
    print("wrote", OUT)


if __name__ == "__main__":
    main()
