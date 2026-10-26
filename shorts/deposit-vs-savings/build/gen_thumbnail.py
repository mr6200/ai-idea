"""Shorts thumbnail (1080x1920), drawn with the scene helpers and rendered by vectorcraft-cli."""
import os
import subprocess

from PIL import Image

from compose_bg import backdrop
from gen_scenes import BG_WASH, CREAM, GLOW, GLOW_ALPHA, GREEN, INK, MUTED, ORANGE, WHITE, pill, svg, text

ROOT = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(ROOT, "..", "thumbnail")

body = (
    f'<rect x="0" y="0" width="1080" height="1920" fill="{CREAM}" fill-opacity="{BG_WASH}"/>'
    f'<circle cx="540" cy="1100" r="560" fill="{GLOW}" fill-opacity="{GLOW_ALPHA}"/>'
    + pill("예금 vs 적금", 540, 300, 64, ORANGE)
    # headline
    + text("금리 높은 적금이", 540, 560, 100)
    + f'<rect x="150" y="610" width="780" height="190" rx="30" fill="{ORANGE}" transform="rotate(-2 540 705)"/>'
    + '<g transform="rotate(-2 540 705)">' + text("이자는 더 적다?", 540, 750, 110, WHITE) + "</g>"
    # the two products
    + f'<rect x="90" y="930" width="420" height="330" rx="40" fill="{WHITE}" stroke="{GREEN}" stroke-width="10"/>'
    + text("예금 3%", 300, 1040, 70, GREEN) + text("36만", 300, 1190, 110, GREEN)
    + f'<rect x="570" y="930" width="420" height="330" rx="40" fill="{WHITE}" stroke="{ORANGE}" stroke-width="10"/>'
    + text("적금 3.5%", 780, 1040, 66, ORANGE) + text("22만", 780, 1190, 110, ORANGE)
    + text("1,200만 원 · 1년 이자", 540, 1380, 56, MUTED)
    + text("이유는 6.5달?", 540, 1600, 96, INK)
    + text("예시 금리 · 세전 · 단리 기준", 540, 1790, 34, MUTED)
)


def main():
    os.makedirs(OUT, exist_ok=True)
    src = os.path.join(OUT, "thumbnail.svg")
    with open(src, "w") as f:
        f.write(svg(body))
    for ext in ("vectorcraft", "png"):
        subprocess.run(["vectorcraft-cli", "convert", src, os.path.join(OUT, f"thumbnail.{ext}")],
                       check=True, capture_output=True)
    # same AI backdrop as the opening scene, under the translucent cream wash
    png = os.path.join(OUT, "thumbnail.png")
    Image.alpha_composite(backdrop("S01"), Image.open(png).convert("RGBA")).convert("RGB").save(png)
    print("wrote", OUT)


if __name__ == "__main__":
    main()
