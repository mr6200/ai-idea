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
# title chosen by the user before the thumbnail was made: 「600년간 아무도 해석하지 못한 책이 있다?」
# the S01 still: the open book fills the middle -> title in the top band
body = (
    shade()
    + '<rect width="1080" height="860" fill="#000" fill-opacity="0.35"/>'
    + head("600년간 아무도", 540, 400, 124)
    + head("해석하지 못한 책", 540, 570, 124, GOLD)
    + pill("이 책이 정말 있다?", 540, 740, 60, RED, "#ffffff")
    + text("보이니치 필사본", 540, 1660, 56, "#ffffff", extra=OUT_LINE)
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
