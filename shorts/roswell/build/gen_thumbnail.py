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
# title chosen by the user before the thumbnail was made: 「로스웰 사건의 진짜 정체」
# the S01 still: windmill and lightning in the upper half, shiny scraps on the ground below
body = (
    shade()
    + '<rect y="980" width="1080" height="940" fill="#000" fill-opacity="0.35"/>'
    + head("로스웰 사건의", 540, 1150, 136)
    + head("진짜 정체", 540, 1330, 170, GOLD)
    + pill("1947년 미군 발표 「비행접시 회수」", 540, 1490, 52, RED, "#ffffff")
    + text("외계인일까, 비밀 풍선일까", 540, 1640, 52, "#ffffff", extra=OUT_LINE)
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
