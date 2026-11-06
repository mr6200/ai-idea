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
# title chosen by the user before the thumbnail was made: 「사막의 거대한 그림, 누가 왜?」
# the hummingbird lies in the lower two thirds of the S01 still, so the title goes in the top band
body = (
    shade()
    + '<rect width="1080" height="820" fill="#000" fill-opacity="0.25"/>'
    + head("사막의 거대한 그림", 540, 420, 118)
    + head("누가 왜 그렸을까?", 540, 590, 128, GOLD)
    + pill("2,000년 전 · 땅에선 안 보이는 그림", 540, 740, 50, RED, "#ffffff")
    + text("페루 · 나스카 라인", 540, 1640, 52, "#ffffff", extra=OUT_LINE)
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
