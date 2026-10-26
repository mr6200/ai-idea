"""Shorts thumbnail (1080x1920), drawn with the scene helpers and rendered by vectorcraft-cli."""
import os
import subprocess

from gen_scenes import RED, YELLOW, bg, burst_star, corner_stress, head, pill, popword, svg, window

ROOT = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(ROOT, "..", "thumbnail")

body = (
    bg(burst=(540, 1080))
    + head("비행기 창문은", 540, 470, 110)
    + head("왜 둥글까?", 540, 640, 150, YELLOW, stroke=16)
    # square window crossed out vs round window
    + window(300, 1100, 300, 380, False, False) + corner_stress(300, 1100, 300, 380)
    + f'<path d="M150 920 L450 1280 M450 920 L150 1280" stroke="{RED}" stroke-width="22" stroke-linecap="round"/>'
    + window(780, 1100, 300, 400, True, True, "#ffffff", 14)
    + burst_star(860, 860, 110, "정답!", RED, YELLOW, 48)
    + popword("네모면 금이 간다?!", 540, 1500, 84, YELLOW, 12, -3)
    + pill("1954년 코멧 사고의 교훈", 540, 1660, 46, "#ffffff")
)


def main():
    os.makedirs(OUT, exist_ok=True)
    src = os.path.join(OUT, "thumbnail.svg")
    with open(src, "w") as f:
        f.write(svg(body))
    for ext in ("vectorcraft", "png"):
        subprocess.run(["vectorcraft-cli", "convert", src, os.path.join(OUT, f"thumbnail.{ext}")],
                       check=True, capture_output=True)
    print("wrote", OUT)


if __name__ == "__main__":
    main()
