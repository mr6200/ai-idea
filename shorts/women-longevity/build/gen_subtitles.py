"""Subtitle cards as full-frame SVGs, exported to PNG through vectorcraft-cli."""
import json
import os
import subprocess

from gen_scenes import FONT, svg, text_width

ROOT = os.path.dirname(os.path.abspath(__file__))
CY = 1480  # centre of the card, above the Shorts bottom UI band
SIZE = 54


def card(lines):
    lh = SIZE * 1.3
    w = max(text_width(l, SIZE) for l in lines) + 80
    assert w < 1020, lines
    h = lh * len(lines) + 40
    top = CY - h / 2
    # documentary caption: white Do Hyeon with a dark outline on a faint dark glass box
    body = f'<rect x="{540 - w / 2:.1f}" y="{top:.1f}" width="{w:.1f}" height="{h:.1f}" rx="16" fill="#000" fill-opacity="0.34"/>'
    for i, l in enumerate(lines):
        y = top + 20 + lh * i + SIZE * 0.98
        l = l.replace("&", "&amp;")
        body += (f'<text x="540" y="{y:.1f}" font-family="{FONT}" font-size="{SIZE}" fill="#ffffff" text-anchor="middle" '
                 f'stroke="#000" stroke-opacity="0.7" stroke-width="7" paint-order="stroke" stroke-linejoin="round">{l}</text>')
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
