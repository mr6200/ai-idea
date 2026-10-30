"""Subtitle cards as full-frame SVGs, exported to PNG through vectorcraft-cli."""
import json
import os
import subprocess

from gen_scenes import FONT, svg, text_width

ROOT = os.path.dirname(os.path.abspath(__file__))
CY = 1480  # centre of the card, above the Shorts bottom UI band
SIZE = 54


def card(lines):
    lh = SIZE * 1.32
    w = max(text_width(l, SIZE) for l in lines) + 90
    assert w < 1020, lines
    h = lh * len(lines) + 46
    top = CY - h / 2
    # vintage caption: aged paper card with a double ink border
    x = 540 - w / 2
    body = (f'<rect x="{x:.1f}" y="{top:.1f}" width="{w:.1f}" height="{h:.1f}" fill="#efe2c4" fill-opacity="0.96" stroke="#2b1d14" stroke-width="6"/>'
            f'<rect x="{x + 12:.1f}" y="{top + 12:.1f}" width="{w - 24:.1f}" height="{h - 24:.1f}" fill="none" stroke="#2b1d14" stroke-width="2"/>')
    for i, l in enumerate(lines):
        y = top + 23 + lh * i + SIZE * 1.0
        l = l.replace("&", "&amp;")
        body += (f'<text x="540" y="{y:.1f}" font-family="{FONT}" font-weight="700" font-size="{SIZE}" fill="#2b1d14" '
                 f'text-anchor="middle">{l}</text>')
    return svg(body)


def main():
    with open(os.path.join(ROOT, "manifest.json")) as f:
        cues = json.load(f)["cues"]
    sd = os.path.join(ROOT, "svg", "subs")
    pd = os.path.join(ROOT, "parts", "subs")
    os.makedirs(sd, exist_ok=True)
    os.makedirs(pd, exist_ok=True)
    for i, c in enumerate(cues):
        p = os.path.join(sd, f"sub{i:02d}.svg")
        with open(p, "w") as f:
            f.write(card(c["text"].split("\n")))
        subprocess.run(["vectorcraft-cli", "convert", p, os.path.join(pd, f"sub{i:02d}.png")],
                       check=True, capture_output=True)
    print(len(cues), "subtitle cards")


if __name__ == "__main__":
    main()
