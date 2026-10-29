"""Shorts thumbnail (1080x1920): the S01 clay painting under the infographic, drawn with the scene helpers."""
import os
import subprocess

from PIL import Image

from compose_bg import backdrop
from gen_scenes import RED, TEAL, WHITE, YELLOW, bg, card, chart_axes, chart_line, cross, head, legend, pill, svg

ROOT = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(ROOT, "..", "thumbnail")

# the cumulative chart from S06/S07, moved down to sit under the headline
chart = (card(90, 600, 900, 720) + chart_axes() + legend("early", "normal", "late") + chart_line("early") + chart_line("normal") + chart_line("late")
         + cross(76.7, 11.7, "77세", RED) + cross(83.9, 18.9, "84세", TEAL))
body = (
    bg()
    + head("국민연금,", 540, 420, 130)
    + head("일찍? 늦게?", 540, 580, 140, YELLOW)
    + f'<g transform="translate(0 220)">{chart}</g>'
    + pill("몇 살에 역전될까?", 540, 1760, 60, RED, WHITE)
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
