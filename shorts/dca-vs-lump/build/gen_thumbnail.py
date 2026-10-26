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
    + pill("적립식 vs 거치식", 540, 300, 60, ORANGE)
    # headline
    + text("목돈 1,200만 원", 540, 560, 104)
    + f'<rect x="150" y="610" width="780" height="190" rx="30" fill="{ORANGE}" transform="rotate(-2 540 705)"/>'
    + '<g transform="rotate(-2 540 705)">' + text("어떻게 넣을까?", 540, 750, 110, WHITE) + "</g>"
    # the two choices
    + pill("한 번에", 540, 1000, 100, ORANGE)
    + f'<circle cx="540" cy="1180" r="85" fill="{INK}"/>' + text("VS", 540, 1207, 76, WHITE)
    + pill("나눠서", 540, 1360, 100, GREEN)
    + text("3번 중 2번 이긴 쪽은?", 540, 1620, 84, INK)
    + text("뱅가드 연구 · 과거 데이터 기준", 540, 1790, 34, MUTED)
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
