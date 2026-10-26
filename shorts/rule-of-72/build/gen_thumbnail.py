"""Shorts thumbnail (1080x1920), drawn with the scene helpers and rendered by vectorcraft-cli."""
import os
import subprocess

from PIL import Image

from compose_bg import backdrop
from gen_scenes import BG_WASH, CREAM, GLOW, GLOW_ALPHA, INK, MUTED, ORANGE, WHITE, bill, pill, svg, text

ROOT = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(ROOT, "..", "thumbnail")

body = (
    f'<rect x="0" y="0" width="1080" height="1920" fill="{CREAM}" fill-opacity="{BG_WASH}"/>'
    f'<circle cx="540" cy="1100" r="560" fill="{GLOW}" fill-opacity="{GLOW_ALPHA}"/>'
    + pill("72의 법칙", 540, 300, 64, ORANGE)
    # headline
    + text("돈이 두 배 되는 날", 540, 560, 104)
    + f'<rect x="150" y="610" width="780" height="190" rx="30" fill="{ORANGE}" transform="rotate(-2 540 705)"/>'
    + '<g transform="rotate(-2 540 705)">' + text("3초 만에 계산", 540, 750, 116, WHITE) + "</g>"
    # the formula
    + f'<circle cx="540" cy="1080" r="200" fill="{ORANGE}"/>' + text("72", 540, 1155, 210, WHITE)
    + text("÷ 수익률", 540, 1400, 110, INK)
    # money doubling
    + bill(250, 1600, 280, "1천만", 40) + text("→", 540, 1625, 90, INK) + bill(840, 1630, 280, "") + bill(820, 1600, 280, "2천만", 40)
    + text("연 1회 복리 기준", 540, 1790, 34, MUTED)
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
