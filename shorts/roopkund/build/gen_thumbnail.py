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
# title chosen by the user before the thumbnail was made: 「히말라야 호수 밑 수백 명의 뼈.. 정체는?」
# (the user typed 「호수 및」; read as 「호수 밑」). The S01 still: lake in the lower half -> title in the top band
body = (
    shade()
    + '<rect width="1080" height="860" fill="#000" fill-opacity="0.35"/>'
    + head("히말라야 호수 밑", 540, 400, 118)
    + head("수백 명의 뼈", 540, 580, 150, GOLD)
    + pill("정체는?", 540, 750, 72, RED, "#ffffff")
    + text("인도 · 루프쿤드 해골 호수", 540, 1660, 52, "#ffffff", extra=OUT_LINE)
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
