"""Generate SVG parts for all 6 scenes of the first-salary Short (45 s, 1080x1920).

Style (episode 23 on): Korean webtoon; episode 24 continues with the same character. Each scene's bottom layer is a webtoon-style AI illustration
(Seedream 4.0, gen_backgrounds_seedream.py) of the same office-worker character, drifting slowly
(kenburns). On top: a black panel border, Black Han Sans headlines with a thick black outline,
Jua speech bubbles and slanted sound-effect words, and white caption boxes with black borders in
Do Hyeon (the subtitles use the same box). Palette: webtoon yellow, red and sky blue on black ink.

Each scene is a list of parts; each part becomes its own full-frame SVG so the exported PNG
layers line up in EffectCraft. A manifest records the timing and animation hints.
"""
import json
import math
import os

W, H = 1080, 1920
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "svg")
LABEL = "지식 쇼츠 · 돈과 생활"

# fonts
HEAD, BUBBLE, NOTE = "Black Han Sans", "Jua", "Do Hyeon"
NUM = HEAD
FONT = NOTE  # subtitles

# palette
INK, WHITE, PAPER = "#111111", "#ffffff", "#fffdf5"
YELLOW, RED, SKY, GREEN = "#ffe14d", "#e63946", "#4cc9f0", "#2a9d8f"
PLUM = INK  # kept so shared helpers (finger) still work


def text_width(s, size):
    w = 0.0
    for ch in s:
        if ord(ch) > 0x2E80:
            w += size * 1.0
        elif ch == " ":
            w += size * 0.3
        else:
            w += size * 0.58
    return w


def text(s, x, y, size, fill=INK, anchor="middle", font=NOTE, extra=""):
    assert text_width(s, size) < 1000, f"text too wide: {s}"
    s = s.replace("&", "&amp;").replace("<", "&lt;")
    return (f'<text x="{x}" y="{y}" font-family="{font}" font-size="{size}" '
            f'fill="{fill}" text-anchor="{anchor}" {extra}>{s}</text>')


def head(s, x, y, size, fill=WHITE, anchor="middle"):
    """Webtoon headline: Black Han Sans with a thick black outline."""
    return text(s, x, y, size, fill, anchor, HEAD, f'stroke="{INK}" stroke-width="13" paint-order="stroke" stroke-linejoin="round"')


def num(s, x, y, size, fill=INK, anchor="middle"):
    return text(s, x, y, size, fill, anchor, HEAD)


def card(x, y, w, h, fill=PAPER, rx=18):
    """Webtoon panel: white box, thick black border, hard black offset shadow."""
    return (f'<rect x="{x + 12}" y="{y + 14}" width="{w}" height="{h}" rx="{rx}" fill="{INK}"/>'
            f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{fill}" stroke="{INK}" stroke-width="8"/>')


def pill(s, cx, cy, size=44, bg=YELLOW, fg=INK, font=BUBBLE):
    w = text_width(s, size) + 70
    h = size * 1.8
    return (f'<rect x="{cx - w / 2 + 8:.1f}" y="{cy - h / 2 + 10:.1f}" width="{w:.1f}" height="{h:.1f}" rx="{h / 2:.1f}" fill="{INK}"/>'
            f'<rect x="{cx - w / 2:.1f}" y="{cy - h / 2:.1f}" width="{w:.1f}" height="{h:.1f}" rx="{h / 2:.1f}" fill="{bg}" stroke="{INK}" stroke-width="7"/>'
            + text(s, cx, cy + size * 0.36, size, fg, "middle", font))


def tag(s, cx, cy, size=44, bg=INK, fg=WHITE):
    w = text_width(s, size) + 60
    return (f'<rect x="{cx - w / 2:.1f}" y="{cy - size * 0.85:.1f}" width="{w:.1f}" height="{size * 1.7:.1f}" rx="10" fill="{bg}"/>'
            + text(s, cx, cy + size * 0.36, size, fg, "middle", NOTE))


def bubble(lines, x, y, w, h, tail=(0, 0), size=54, colors=None):
    """Speech bubble: rounded white balloon with a black outline and a tail pointing at tail=(tx, ty)."""
    tx, ty = tail
    cx = x + w / 2
    body = (f'<path d="M{cx - 40} {y + h - 4} L{tx} {ty} L{cx + 30} {y + h - 4} Z" fill="{WHITE}" stroke="{INK}" stroke-width="8" stroke-linejoin="round"/>'
            f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{h / 2}" fill="{WHITE}" stroke="{INK}" stroke-width="8"/>'
            f'<path d="M{cx - 34} {y + h - 8} L{cx + 24} {y + h - 8}" stroke="{WHITE}" stroke-width="12"/>')
    colors = colors or [INK] * len(lines)
    lh = size * 1.15
    top = y + h / 2 - lh * (len(lines) - 1) / 2 + size * 0.36
    for i, (l, c) in enumerate(zip(lines, colors)):
        body += text(l, cx, top + i * lh, size, c, font=BUBBLE)
    return body


def sfx(s, x, y, size=110, fill=RED, rot=-12):
    """Sound-effect word: slanted Jua with a white then black outline."""
    t = s.replace("&", "&amp;")
    return (f'<g transform="rotate({rot} {x} {y})">'
            f'<text x="{x}" y="{y}" font-family="{BUBBLE}" font-size="{size}" fill="{INK}" text-anchor="middle" stroke="{INK}" stroke-width="22" stroke-linejoin="round">{t}</text>'
            f'<text x="{x}" y="{y}" font-family="{BUBBLE}" font-size="{size}" fill="{fill}" text-anchor="middle" stroke="{WHITE}" stroke-width="8" paint-order="stroke" stroke-linejoin="round">{t}</text></g>')


def burst(cx, cy, r1, r2, n=14, fill=YELLOW):
    pts = []
    for i in range(n * 2):
        a = math.pi * i / n
        r = r1 if i % 2 == 0 else r2
        pts.append(f"{cx + r * math.cos(a):.0f},{cy + r * math.sin(a):.0f}")
    return f'<polygon points="{" ".join(pts)}" fill="{fill}" stroke="{INK}" stroke-width="8" stroke-linejoin="round"/>'


def svg(body):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">'
            f'<rect x="0" y="0" width="{W}" height="{H}" fill="#000000" fill-opacity="0"/>{body}</svg>')


def bg():
    """Black webtoon panel border and the label tab at the top."""
    return (f'<rect x="22" y="22" width="1036" height="1876" rx="10" fill="none" stroke="{INK}" stroke-width="16"/>'
            + tag(LABEL, 540, 120, 36, INK, WHITE))


def ai(dur, z=(104, 112), pan=(0, 0)):
    """Bottom layer: the scene's webtoon illustration (written by compose_bg.py) with a slow camera move."""
    return ("ai", "", {"type": "kenburns", "dur": dur, "z": z, "pan": pan})


# ---------------------------------------------------------------- scenes
scenes = []


def scene(sid, start, end, parts):
    scenes.append({"id": sid, "start": start, "end": end, "parts": parts})


finger = (f'<path d="M700 1145 V1250 C700 1280 740 1300 770 1300 H820 C850 1300 870 1270 870 1240 V1200 C870 1185 845 1180 835 1195 '
          f'C835 1175 810 1170 800 1188 C800 1170 775 1165 765 1185 V1145 C765 1120 700 1120 700 1145 Z" fill="#f6d2b3" stroke="{INK}" stroke-width="6"/>')


def flow(items, y, colors):
    """Left-to-right chain of rounded boxes joined by arrows."""
    n = len(items)
    w = 250
    gap = (900 - n * w) / (n - 1)
    out = ""
    for i, (label, col) in enumerate(zip(items, colors)):
        x = 90 + i * (w + gap)
        out += (f'<rect x="{x:.0f}" y="{y}" width="{w}" height="130" rx="20" fill="{col}" stroke="{INK}" stroke-width="8"/>'
                + text(label, x + w / 2, y + 85, 50, INK, font=HEAD))
        if i < n - 1:
            ax = x + w + 6
            out += (f'<path d="M{ax:.0f} {y + 65} H{ax + gap - 12:.0f} M{ax + gap - 34:.0f} {y + 45} L{ax + gap - 12:.0f} {y + 65} L{ax + gap - 34:.0f} {y + 85}" '
                    f'fill="none" stroke="{INK}" stroke-width="9" stroke-linecap="round" stroke-linejoin="round"/>')
    return out


# S01 훅: 첫 월급, 뭐부터? -------------------------------------------------------------------------
scene("S01", 0, 4.0, [
    ai(4.0, (104, 114), (0, 30)),
    ("bg", bg(), {"type": "none"}),
    ("title", head("첫 월급 받으면", 540, 300, 112) + head("꼭 할 3가지!", 540, 440, 124, YELLOW), {"type": "pop", "at": 0.0, "anchor": [540, 370]}),
    ("sfx", sfx("띠링!", 850, 1130, 110, SKY, 10), {"type": "stamp", "at": 0.5, "anchor": [850, 1100]}),
    ("bubble", bubble(["첫 월급이다!"], 50, 900, 420, 130, (480, 1000), 54), {"type": "pop", "at": 1.0, "anchor": [260, 965]}),
    ("three", pill("딱 3가지만", 540, 1280, 58, RED, WHITE), {"type": "stamp", "at": 2.8, "anchor": [540, 1280]}),
])

# S02 ① 비상금 통장 --------------------------------------------------------------------------------
scene("S02", 4.0, 11.8, [
    ai(7.8, (112, 104), (-30, 0)),
    ("bg", bg(), {"type": "none"}),
    ("title", head("① 비상금 통장", 540, 300, 116), {"type": "pop", "at": 0.0, "anchor": [540, 260]}),
    ("amount", card(110, 980, 860, 220) + text("갑자기 아프거나 일이 끊길 때", 540, 1060, 44, INK) + num("생활비 3~6개월 치", 540, 1160, 74, RED),
     {"type": "pop", "at": 2.8, "anchor": [540, 1090]}),
    ("where", pill("언제든 꺼낼 수 있는 파킹통장에", 540, 1290, 46, SKY, INK), {"type": "fade", "at": 5.4}),
])

# S03 ② 저축은 자동이체로 먼저 ---------------------------------------------------------------------------
scene("S03", 11.8, 17.4, [
    ai(5.6, (106, 116), (30, -20)),
    ("bg", bg(), {"type": "none"}),
    ("title", head("② 저축은 먼저", 540, 300, 116), {"type": "pop", "at": 0.0, "anchor": [540, 260]}),
    ("flow", flow(["월급", "저축", "쓰기"], 1060, [WHITE, YELLOW, SKY]) + tag("월급날 자동이체", 540, 1250, 44, INK, WHITE), {"type": "wipeL", "at": 1.2, "dur": 1.6}),
    ("bubble", bubble(["남은 돈은 안 남아요"], 40, 420, 560, 130, (480, 580), 50, [RED]), {"type": "pop", "at": 3.4, "anchor": [320, 485]}),
])

# S04 ③ 카드는 나눠 쓰기 ---------------------------------------------------------------------------------
row = lambda y, step, kind, pct, col: (text(step, 150, y, 46, INK, "start") + text(kind, 640, y, 52, INK, font=HEAD) + num(pct, 900, y + 4, 64, col, "end"))
scene("S04", 17.4, 27.0, [
    ai(9.6, (104, 114), (-30, 20)),
    ("bg", bg(), {"type": "none"}),
    ("title", head("③ 카드는 나눠 쓰기", 540, 300, 104), {"type": "pop", "at": 0.0, "anchor": [540, 260]}),
    ("rule", card(90, 900, 900, 380) + tag("연말정산 카드 소득공제", 540, 970, 40, INK, WHITE)
     + row(1080, "총급여 25%까지", "", "공제 없음", INK) + f'<path d="M150 1120 H930" stroke="{INK}" stroke-opacity="0.2" stroke-width="4"/>'
     + row(1180, "그다음 신용카드", "", "15%", SKY) + row(1250, "그다음 체크카드", "", "30%", RED),
     {"type": "wipeD", "at": 2.2, "dur": 3.0}),
    ("x2", sfx("2배!", 880, 860, 100, RED, 10), {"type": "stamp", "at": 6.4, "anchor": [880, 830]}),
])

# S05 퀴즈: 3천만 원이면? ----------------------------------------------------------------------------
opts = ["300만 원", "750만 원", "1,500만 원"]
choices = "".join(card(130, 640 + i * 170, 820, 130) + text(o, 540, 722 + i * 170, 60, INK, font=HEAD) for i, o in enumerate(opts))
scene("S05", 27.0, 36.4, [
    ai(9.4, (106, 116), (0, -30)),
    ("bg", bg(), {"type": "none"}),
    ("badge", pill("퀴즈", 540, 240, 56, RED, WHITE), {"type": "pop", "at": 0.0, "anchor": [540, 240]}),
    ("question", head("총급여 3천만 원이면", 540, 400, 88) + head("얼마부터 공제될까?", 540, 510, 92, YELLOW), {"type": "pop", "at": 0.3, "anchor": [540, 455]}),
    ("choices", choices, {"type": "pop", "at": 0.9, "anchor": [540, 810]}),
    ("answer", f'<rect x="114" y="794" width="852" height="162" rx="24" fill="none" stroke="{RED}" stroke-width="14"/>' + sfx("정답!", 900, 820, 90, RED, 12),
     {"type": "stamp", "at": 4.4, "anchor": [540, 875]}),
    ("why", pill("3천만 원 × 25% = 750만 원", 540, 1220, 50, SKY, INK), {"type": "fade", "at": 6.4}),
])

# S06 마무리 + 구독 ---------------------------------------------------------------------------------------
scene("S06", 36.4, 45.0, [
    ai(8.6, (110, 102), (0, 0)),
    ("bg", bg(), {"type": "none"}),
    ("look", head("첫 월급부터", 540, 250, 100) + head("습관 만들기!", 540, 370, 110, YELLOW), {"type": "pop", "at": 0.2, "anchor": [540, 310]}),
    ("button", pill("구독하기", 540, 1250, 80, RED, WHITE), {"type": "pop", "at": 3.6, "anchor": [540, 1250]}),
    ("finger", f'<g transform="translate(0 170)">{finger}</g>', {"type": "tap", "at": 4.2, "anchor": [785, 1390]}),
])


def main():
    manifest = []
    for sc in scenes:
        d = os.path.join(OUT, sc["id"])
        os.makedirs(d, exist_ok=True)
        full = ""
        parts = []
        for name, body, anim in sc["parts"]:
            with open(os.path.join(d, f"{name}.svg"), "w") as f:
                f.write(svg(body))
            full += f'<g id="{name}">{body}</g>'
            parts.append({"name": name, "anim": anim})
        with open(os.path.join(d, "_full.svg"), "w") as f:
            f.write(svg(full))
        manifest.append({"id": sc["id"], "start": sc["start"], "end": sc["end"], "parts": parts})
    with open(os.path.join(os.path.dirname(OUT), "manifest_scenes.json"), "w") as f:
        json.dump(manifest, f, ensure_ascii=False, indent=1)
    print(sum(len(s["parts"]) for s in scenes), "parts in", len(scenes), "scenes")


if __name__ == "__main__":
    main()
