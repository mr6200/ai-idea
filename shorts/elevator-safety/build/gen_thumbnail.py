"""Shorts thumbnail (1080x1920), drawn with the scene helpers over the S01 engraving and rendered by vectorcraft-cli."""
import os
import subprocess

from PIL import Image

from compose_bg import backdrop
from gen_scenes import RED, bg, cable, car, head, note, rails, ribbon, rule, seal, snap, svg

ROOT = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(ROOT, "..", "thumbnail")

body = (
    bg(burst=(540, 1060))
    + head("엘리베이터 줄이", 540, 450, 110)
    + head("끊어지면?", 540, 620, 160, RED)
    + rule(680)
    + rails(540, 740, 1420, 440, False) + cable(540, 740, 850) + cable(540, 940, 1000) + car(540, 1200, 340, 380)
    + snap(540, 890)
    + seal(860, 900, 120, "추락?", 64, RED, -8)
    + note("1854년, 줄을 직접 끊은 남자", 540, 1560, 48)
    + ribbon("정답은 영상에서", 540, 1720, 50)
)


def main():
    os.makedirs(OUT, exist_ok=True)
    src = os.path.join(OUT, "thumbnail.svg")
    with open(src, "w") as f:
        f.write(svg(body))
    for ext in ("vectorcraft", "png"):
        subprocess.run(["vectorcraft-cli", "convert", src, os.path.join(OUT, f"thumbnail.{ext}")],
                       check=True, capture_output=True)
    # same sepia engraving as the opening scene, under the translucent paper layer
    png = os.path.join(OUT, "thumbnail.png")
    Image.alpha_composite(backdrop("S01"), Image.open(png).convert("RGBA")).convert("RGB").save(png)
    print("wrote", OUT)


if __name__ == "__main__":
    main()
