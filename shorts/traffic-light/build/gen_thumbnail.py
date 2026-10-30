"""Shorts thumbnail (1080x1920): the S02 engraving under the paper layer, drawn with the scene helpers."""
import os
import subprocess

from PIL import Image

from compose_bg import backdrop
from gen_scenes import RED, bg, head, note, ribbon, rule, seal, signal, svg

ROOT = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(ROOT, "..", "thumbnail")

body = (
    bg()
    + head("신호등은 왜", 540, 440, 120)
    + head("빨강·노랑·초록?", 540, 600, 128, RED)
    + rule(660)
    + signal(540, 1080, "ryg", "ryg", 1.25)
    + seal(860, 820, 120, "1868", 56, RED, -8)
    + note("시작은 기차였다", 540, 1560, 52)
    + ribbon("세계 첫 신호등은 폭발했다?", 540, 1720, 46)
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
