"""Shorts thumbnail (1080x1920): the S01 documentary still with the headline and the key number."""
import os
import subprocess

from PIL import Image

from gen_scenes import GOLD, RED, head, pill, shade, svg, text
from prep_footage import still

ROOT = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(ROOT, "..", "thumbnail")

body = (
    shade()
    + '<rect y="1100" width="1080" height="820" fill="#000" fill-opacity="0.25"/>'
    + head("여자는 왜", 540, 470, 150)
    + head("더 오래 살까?", 540, 660, 156, GOLD)
    + pill("평균 5.8년 더", 540, 1330, 72, RED, "#ffffff")
    + text("2024년 생명표 · 여자 86.6세 / 남자 80.8세", 540, 1480, 44, "#ffffff",
           extra='stroke="#000" stroke-opacity="0.6" stroke-width="6" paint-order="stroke"')
    + text("비밀은 몸속에 있다", 540, 1600, 60, GOLD,
           extra='stroke="#000" stroke-opacity="0.6" stroke-width="6" paint-order="stroke"')
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
