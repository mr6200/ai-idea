"""Shorts thumbnail (1080x1920), drawn with the scene helpers and rendered by vectorcraft-cli."""
import os
import subprocess

from gen_scenes import CYAN, RED, YELLOW, bg, bubble, burst_star, ear_icon, head, pill, plane_icon, popword, svg

ROOT = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(ROOT, "..", "thumbnail")

body = (
    bg(burst=(540, 1060))
    + head("비행기 타면", 540, 470, 116)
    + head("귀가 먹먹한 이유", 540, 630, 120, YELLOW, stroke=16)
    + plane_icon(820, 800, 0.8, 20)
    + ear_icon(480, 1100, 1.6)
    + popword("웅~", 190, 980, 100, CYAN, 12, -12)
    + burst_star(830, 1180, 130, "아야!", RED, YELLOW, 64)
    + bubble(540, 1470, 640, 130, "착륙 때 더 아픈 이유는?", 54, (1, 1))
    + pill("꿀꺽 삼키면 풀려요", 540, 1690, 50, "#ffffff")
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
