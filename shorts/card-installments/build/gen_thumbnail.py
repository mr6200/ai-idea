"""Shorts thumbnail (1080x1920), drawn with the scene helpers and rendered by vectorcraft-cli."""
import os
import subprocess

from PIL import Image

from compose_bg import backdrop
from gen_scenes import BG_WASH, CREAM, GLOW, GLOW_ALPHA, GREEN, INK, MUTED, ORANGE, RED, WHITE, pill, svg, text

ROOT = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(ROOT, "..", "thumbnail")

body = (
    f'<rect x="0" y="0" width="1080" height="1920" fill="{CREAM}" fill-opacity="{BG_WASH}"/>'
    f'<circle cx="540" cy="1100" r="560" fill="{GLOW}" fill-opacity="{GLOW_ALPHA}"/>'
    + pill("무이자 할부의 비밀", 540, 300, 60, ORANGE)
    # headline
    + text("무이자 할부", 540, 560, 110)
    + f'<rect x="150" y="610" width="780" height="190" rx="30" fill="{RED}" transform="rotate(-2 540 705)"/>'
    + '<g transform="rotate(-2 540 705)">' + text("카드사는 손해?", 540, 750, 112, WHITE) + "</g>"
    # the card
    + f'<rect x="300" y="930" width="480" height="300" rx="30" fill="#3b82c4"/>'
    + f'<rect x="340" y="1000" width="90" height="66" rx="8" fill="#e0b23a"/>'
    + f'<path d="M340 1170 H740" stroke="{WHITE}" stroke-width="10" stroke-dasharray="40 18" stroke-opacity="0.8"/>'
    + text("할부 수수료 수익", 540, 1420, 70, INK)
    + text("약 3조 6천억 원", 540, 1560, 100, RED)
    + text("카드사 7곳 · 2025년", 540, 1790, 34, MUTED)
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
