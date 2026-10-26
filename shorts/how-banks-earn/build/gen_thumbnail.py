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
    + pill("은행의 돈벌이", 540, 300, 64, ORANGE)
    # headline
    + text("은행은 어떻게", 540, 560, 104)
    + f'<rect x="150" y="610" width="780" height="190" rx="30" fill="{ORANGE}" transform="rotate(-2 540 705)"/>'
    + '<g transform="rotate(-2 540 705)">' + text("돈을 벌까?", 540, 750, 120, WHITE) + "</g>"
    # the spread
    + f'<rect x="90" y="930" width="420" height="300" rx="40" fill="{WHITE}" stroke="{GREEN}" stroke-width="10"/>'
    + text("예금", 300, 1040, 70, GREEN) + text("3%", 300, 1180, 120, GREEN)
    + f'<rect x="570" y="930" width="420" height="300" rx="40" fill="{WHITE}" stroke="{ORANGE}" stroke-width="10"/>'
    + text("대출", 780, 1040, 70, ORANGE) + text("5%", 780, 1180, 120, ORANGE)
    + text("이 차이가 은행 몫", 540, 1420, 84, INK)
    + text("10원 중 약 9원이 이자", 540, 1580, 64, RED)
    + text("예시 금리 · 2025년 국내 은행 실적 기준", 540, 1790, 34, MUTED)
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
