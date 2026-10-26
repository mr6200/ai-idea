"""Shorts thumbnail (1080x1920): the S01 painting under the paper layer, drawn with the scene helpers."""
import os
import subprocess

from PIL import Image

from compose_bg import backdrop
from gen_scenes import RED, bg, head, iceberg, note, ribbon, rule, seal, svg

ROOT = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(ROOT, "..", "thumbnail")

body = (
    bg()
    + head("침몰하지 않는 배", 540, 450, 104)
    + head("타이타닉", 540, 620, 170, RED)
    + rule(680)
    + iceberg(250, 1240, 0.8)
    + seal(820, 1000, 130, "왜?", 90, RED, -8)
    + note("2시간 40분 만에 가라앉은 이유", 540, 1560, 46)
    + ribbon("16개의 방수 칸의 비밀", 540, 1720, 48)
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
    Image.alpha_composite(backdrop("S01"), Image.open(png).convert("RGBA")).convert("RGB").save(png)
    print("wrote", OUT)


if __name__ == "__main__":
    main()
