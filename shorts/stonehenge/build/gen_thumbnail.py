"""Shorts thumbnail (1080x1920): the S13 still (the stone circle under the Milky Way) with the title."""
import os
import subprocess

from PIL import Image

from gen_scenes import GOLD, RED, head, pill, shade, svg
from prep_footage import still

ROOT = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(ROOT, "..", "thumbnail")

# title chosen by the user before the thumbnail was made: 「스톤헨지 돌은 어디서 왔을까?」
# the stones sit in the lower half of the still, so the title goes on the night sky above them
body = (
    shade()
    + head("스톤헨지 돌은", 540, 440, 130)
    + head("어디서 왔을까?", 540, 610, 124, GOLD)
    + pill("700km 밖에서 온 돌도 있다", 540, 770, 54, RED, "#ffffff")
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
    Image.alpha_composite(still("S13"), Image.open(png).convert("RGBA")).convert("RGB").save(png)
    print("wrote", OUT)


if __name__ == "__main__":
    main()
