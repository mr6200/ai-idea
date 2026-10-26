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
    + pill("은행의 탄생", 540, 300, 64, ORANGE)
    # headline
    + text("은행은 처음에", 540, 560, 104)
    + f'<rect x="150" y="610" width="780" height="190" rx="30" fill="{ORANGE}" transform="rotate(-2 540 705)"/>'
    + '<g transform="rotate(-2 540 705)">' + text("탁자였다?", 540, 750, 120, WHITE) + "</g>"
    # the table
    + f'<rect x="240" y="1100" width="600" height="44" rx="12" fill="#8a5a3b"/>'
    + f'<rect x="280" y="1144" width="34" height="220" fill="#8a5a3b"/><rect x="766" y="1144" width="34" height="220" fill="#8a5a3b"/>'
    + f'<ellipse cx="420" cy="1080" rx="70" ry="20" fill="#e0b23a" stroke="#b98a1e" stroke-width="4"/>'
    + f'<ellipse cx="560" cy="1070" rx="70" ry="20" fill="#e0b23a" stroke="#b98a1e" stroke-width="4"/>'
    + f'<ellipse cx="680" cy="1082" rx="70" ry="20" fill="#e0b23a" stroke="#b98a1e" stroke-width="4"/>'
    + text("banco", 540, 1000, 120, "#8a5a3b")
    + text("4천 년의 이야기", 540, 1560, 96, INK)
    + text("곡식 창고에서 지폐까지", 540, 1680, 52, MUTED)
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
