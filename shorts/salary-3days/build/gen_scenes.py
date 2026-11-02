"""Generate SVG parts for all 7 scenes of the salary-3days Short (48 s, 1080x1920).

Style (episode 23): Korean webtoon. Each scene's bottom layer is a webtoon-style AI illustration
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


# S01 훅: 월급, 왜 3일 만에? ------------------------------------------------------------------------
scene("S01", 0, 4.0, [
    ai(4.0, (104, 114), (0, 30)),
    ("bg", bg(), {"type": "none"}),
    ("title", head("월급, 왜", 540, 300, 124) + head("3일 만에 사라질까?", 540, 440, 108, YELLOW), {"type": "pop", "at": 0.0, "anchor": [540, 370]}),
    ("bubble", bubble(["어?! 내 월급", "어디 갔어?!"], 50, 820, 400, 200, (520, 900), 50, [INK, RED]), {"type": "pop", "at": 0.7, "anchor": [250, 920]}),
    ("sfx", sfx("털썩", 860, 1240), {"type": "stamp", "at": 2.4, "anchor": [860, 1210]}),
])

# S02 줄 서 있는 자동이체 -------------------------------------------------------------------------------
bills = [("월세 · 관리비", 0.9), ("대출 이자", 1.6), ("보험료", 2.4), ("통신비", 3.2)]
s02 = [ai(10.4, (112, 104), (-30, 0)), ("bg", bg(), {"type": "none"}),
       ("title", head("월급날 줄 선 돈들", 540, 300, 108), {"type": "pop", "at": 0.0, "anchor": [540, 260]})]
for i, (name, at) in enumerate(bills):
    y = 470 + i * 150
    s02.append((f"bill{i}", pill(name, 250, y, 50, [YELLOW, SKY, YELLOW, SKY][i]), {"type": "slideR", "at": 2.8 + at}))
s02 += [("auto", card(110, 1080, 860, 200) + text("자동이체", 540, 1160, 56, INK, font=HEAD) + text("월급날 바로 뒤에 몰려 있어요", 540, 1240, 46, INK),
         {"type": "pop", "at": 6.6, "anchor": [540, 1180]}),
        ("sfx", sfx("쑥!", 880, 470, 100, RED, 10), {"type": "stamp", "at": 3.6, "anchor": [880, 440]})]
scene("S02", 4.0, 14.4, s02)

# S03 가장 큰 건 카드값 -----------------------------------------------------------------------------------
scene("S03", 14.4, 19.6, [
    ai(5.2, (106, 116), (30, -20)),
    ("bg", bg(), {"type": "none"}),
    ("title", head("가장 큰 건 카드값", 540, 300, 108), {"type": "pop", "at": 0.0, "anchor": [540, 260]}),
    ("flow", card(110, 990, 860, 300) + text("이번 달 월급", 300, 1100, 54, INK, font=HEAD) + text("지난달 카드값", 780, 1100, 54, RED, font=HEAD)
     + f'<path d="M470 1085 H600 M575 1060 L605 1085 L575 1110" fill="none" stroke="{INK}" stroke-width="10" stroke-linecap="round" stroke-linejoin="round"/>'
     + text("이번 달 월급으로 지난달 쓴 돈을 메우는 셈", 540, 1215, 42, INK), {"type": "pop", "at": 2.6, "anchor": [540, 1140]}),
    ("bubble", bubble(["벌써 다 썼다고?!"], 50, 420, 460, 130, (560, 560), 50), {"type": "pop", "at": 1.0, "anchor": [280, 485]}),
])

# S04 69% --------------------------------------------------------------------------------------------
scene("S04", 19.6, 23.8, [
    ai(4.2, (110, 104), (0, 30)),
    ("bg", bg(), {"type": "none"}),
    ("title", head("실제로 얼마나 쓸까?", 540, 300, 104), {"type": "pop", "at": 0.0, "anchor": [540, 260]}),
    ("big", burst(540, 560, 200, 150, 16, YELLOW) + num("69%", 540, 610, 150, RED), {"type": "stamp", "at": 0.8, "anchor": [540, 560]}),
    ("src", tag("쓸 수 있는 돈 중 소비 비율 · 가계동향 2026년 2분기", 540, 1300, 34, INK, WHITE), {"type": "fade", "at": 1.2}),
])

# S05 해결: 저축 먼저 · 통장 나누기 -------------------------------------------------------------------------
env = lambda cx, label, col: (f'<rect x="{cx - 130}" y="1010" width="260" height="190" rx="14" fill="{col}" stroke="{INK}" stroke-width="8"/>'
                              f'<path d="M{cx - 130} 1020 L{cx} 1115 L{cx + 130} 1020" fill="none" stroke="{INK}" stroke-width="8" stroke-linejoin="round"/>'
                              + text(label, cx, 1270, 48, INK, font=HEAD, extra=f'stroke="{WHITE}" stroke-width="10" paint-order="stroke"'))
scene("S05", 23.8, 31.0, [
    ai(7.2, (104, 114), (-30, 20)),
    ("bg", bg(), {"type": "none"}),
    ("title", head("그럼 어떻게?", 540, 300, 120), {"type": "pop", "at": 0.0, "anchor": [540, 260]}),
    ("first", bubble(["월급날 = 저축날!"], 40, 820, 540, 130, (430, 700), 54, [RED]), {"type": "pop", "at": 1.8, "anchor": [310, 885]}),
    ("envs", env(230, "① 저축 먼저", YELLOW) + env(540, "② 고정 지출", SKY) + env(850, "③ 생활비", "#ffb4a2"), {"type": "pop", "at": 4.4, "anchor": [540, 1120]}),
])

# S06 퀴즈: 결제일 14일이면? ----------------------------------------------------------------------------
opts = ["이번 달 1~14일", "지난달 1일~말일", "지난달 15일~이번 달 14일"]
choices = "".join(card(130, 620 + i * 170, 820, 130) + text(o, 540, 702 + i * 170, 54, INK, font=HEAD) for i, o in enumerate(opts))
scene("S06", 31.0, 40.8, [
    ai(9.8, (106, 116), (0, -30)),
    ("bg", bg(), {"type": "none"}),
    ("badge", pill("퀴즈", 540, 240, 56, RED, WHITE), {"type": "pop", "at": 0.0, "anchor": [540, 240]}),
    ("question", head("카드 결제일이 14일이면", 540, 400, 84) + head("언제 쓴 돈이 청구될까?", 540, 510, 84, YELLOW), {"type": "pop", "at": 0.3, "anchor": [540, 455]}),
    ("choices", choices, {"type": "pop", "at": 0.9, "anchor": [540, 790]}),
    ("answer", f'<rect x="114" y="774" width="852" height="162" rx="24" fill="none" stroke="{RED}" stroke-width="14"/>' + sfx("정답!", 900, 800, 90, RED, 12),
     {"type": "stamp", "at": 4.4, "anchor": [540, 855]}),
    ("why", pill("카드사마다 조금 달라요 · 앱에서 확인", 540, 1210, 44, SKY, INK), {"type": "fade", "at": 6.8}),
])

# S07 마무리 + 구독 ---------------------------------------------------------------------------------------
scene("S07", 40.8, 48.0, [
    ai(7.2, (110, 102), (0, 0)),
    ("bg", bg(), {"type": "none"}),
    ("look", head("다음 월급은", 540, 250, 96) + head("사흘보다 오래!", 540, 370, 104, YELLOW), {"type": "pop", "at": 0.2, "anchor": [540, 310]}),
    ("button", pill("구독하기", 540, 1250, 80, RED, WHITE), {"type": "pop", "at": 2.2, "anchor": [540, 1250]}),
    ("finger", f'<g transform="translate(0 170)">{finger}</g>', {"type": "tap", "at": 2.8, "anchor": [785, 1390]}),
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
