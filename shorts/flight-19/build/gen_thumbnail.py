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
# title chosen by the user before the thumbnail was made: 「버뮤다 삼각지대의 진실」
# the S01 still: storm clouds at the top, the five planes in the lower two thirds -> title in the top band
body = (
    shade()
    + '<rect width="1080" height="820" fill="#000" fill-opacity="0.35"/>'
    + head("버뮤다 삼각지대의", 540, 430, 118)
    + head("진실", 540, 640, 200, GOLD)
    + pill("1945년 · 사라진 폭격기 5대", 540, 780, 54, RED, "#ffffff")
    + text("플라이트 19 실종 사건", 540, 1660, 52, "#ffffff", extra=OUT_LINE)
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
