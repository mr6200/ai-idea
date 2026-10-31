"""Shorts thumbnail (1080x1920): the S01 clay painting under the infographic, drawn with the scene helpers."""
import os
import subprocess

from PIL import Image

from compose_bg import backdrop
from gen_scenes import RED, WHITE, YELLOW, INK, bg, card, head, num, pill, svg, text

ROOT = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(ROOT, "..", "thumbnail")

body = (
    bg()
    + head("맥도날드는", 540, 420, 130)
    + head("사실 부동산 회사?", 540, 590, 120, YELLOW)
    + card(110, 1150, 860, 360) + text("가맹점에서 받은 돈 (2024년)", 540, 1240, 48, INK)
    + num("임대료 100억 달러", 540, 1410, 96, RED)
    + pill("햄버거보다 땅", 540, 1640, 70, RED, WHITE)
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
