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
    + head("연금저축 vs IRP", 540, 420, 120)
    + head("뭐가 다를까?", 540, 590, 130, YELLOW)
    + card(110, 1150, 860, 360) + text("둘 다 세액공제, 그런데", 540, 1240, 48, INK)
    + num("꺼내기 · 투자 제한", 540, 1410, 96, RED)
    + pill("어디부터 채울까?", 540, 1640, 70, RED, WHITE)
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
