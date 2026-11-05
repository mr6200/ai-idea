"""Shorts thumbnail (1080x1920): the S01 ghost-ship still with the headline and the hook."""
import os
import subprocess

from PIL import Image

from gen_scenes import GOLD, RED, head, pill, shade, svg, text
from prep_footage import still

ROOT = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(ROOT, "..", "thumbnail")

OUT_LINE = 'stroke="#000" stroke-opacity="0.7" stroke-width="7" paint-order="stroke"'
# the ship sits in the upper half of the still, so the title goes on the sea below it
body = (
    shade()
    + '<rect y="1000" width="1080" height="920" fill="#000" fill-opacity="0.3"/>'
    # title chosen by the user before the thumbnail was made: 「유령선 미스터리. 진실은 어디에..?」
    + head("유령선 미스터리", 540, 1150, 128)
    + head("진실은 어디에..?", 540, 1320, 128, GOLD)
    + pill("배는 멀쩡한데 10명이 사라졌다", 540, 1480, 54, RED, "#ffffff")
    + text("1872년 · 메리 셀레스트호", 540, 1630, 50, "#ffffff", extra=OUT_LINE)
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
    Image.alpha_composite(still("S01"), Image.open(png).convert("RGBA")).convert("RGB").save(png)
    print("wrote", OUT)


if __name__ == "__main__":
    main()
