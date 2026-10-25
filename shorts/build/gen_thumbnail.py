"""Shorts thumbnail (1080x1920), drawn with the scene helpers and rendered by vectorcraft-cli."""
import os
import subprocess

from gen_scenes import (CREAM, GLOW, GREEN, INK, MUTED, ORANGE, RED, WHITE, person, pill, svg, text)

ROOT = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(ROOT, "..", "thumbnail")


def card(cx, top, color, who, years, amount, big):
    w, h = 440, 250 if big else 220
    fs = 62 if big else 56
    return (f'<rect x="{cx - w / 2}" y="{top}" width="{w}" height="{h}" rx="32" fill="{WHITE}" '
            f'stroke="{color}" stroke-width="{12 if big else 6}"/>'
            + text(who, cx, top + 62, 40, color)
            + text(years, cx, top + 112, 34, MUTED)
            + text(amount, cx, top + 112 + fs * 1.25, fs, color))


body = (
    f'<rect x="0" y="0" width="1080" height="1920" fill="{CREAM}"/>'
    f'<circle cx="540" cy="1180" r="560" fill="{GLOW}"/>'
    + pill("복리의 마법", 540, 300, 64, ORANGE)
    # headline
    + text("3배 적게 넣고", 540, 560, 124)
    + f'<rect x="120" y="610" width="840" height="190" rx="30" fill="{ORANGE}" transform="rotate(-2 540 705)"/>'
    + f'<g transform="rotate(-2 540 705)">' + text("더 많이 번다?", 540, 750, 116, WHITE) + "</g>"
    # characters and their results
    + person(300, 1370, GREEN, s=0.95)
    + person(780, 1370, ORANGE, s=0.95, glasses=True, hair="#5a4636")
    + card(300, 1400, GREEN, "A · 25살 시작", "10년만 3,600만 원", "3억 7,900만", True)
    + card(780, 1400, ORANGE, "B · 35살 시작", "30년간 1억 800만 원", "3억 4천만", False)
    # winner badge
    + pill("승!", 150, 860, 56, RED)
    + text("연 7% 가정", 540, 1760, 34, MUTED)
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
