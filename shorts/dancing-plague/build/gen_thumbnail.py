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
# title chosen by the user before the thumbnail was made: 「멈추지 못한 춤, 1518년 춤 전염병」
# the S01 still: the dancing woman stands in the left/middle of the street, so the title goes in the lower band
body = (
    shade()
    + '<rect y="1000" width="1080" height="920" fill="#000" fill-opacity="0.35"/>'
    + head("멈추지 못한 춤", 540, 1160, 140)
    + head("1518년 춤 전염병", 540, 1330, 128, GOLD)
    + pill("한 사람에서 수백 명으로", 540, 1490, 56, RED, "#ffffff")
    + text("스트라스부르의 기이한 여름", 540, 1640, 52, "#ffffff", extra=OUT_LINE)
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
