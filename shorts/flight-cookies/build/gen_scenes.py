"""Generate SVG parts for all 7 scenes of the flight-cookies Short (58 s, 1080x1920).

Style: the Korean webtoon frame (episode 23 on) with the semi-realistic action webtoon drawing
(episode 26 on, user choice) and the same office-worker character. Each scene's bottom layer is an AI illustration
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
YELLOW, RED, SKY, GREEN = "#ffb703", "#e63946", "#4cc9f0", "#2a9d8f"
ORANGE, NAVY, DARK = "#ff5400", "#2b1055", "#14141f"
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
    return text(s, x, y, size, fill, anchor, HEAD, f'stroke="{NAVY}" stroke-width="14" paint-order="stroke" stroke-linejoin="round"')


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


def hours(label, t, y, col=SKY, size=78):
    """Opening-hours row: label on the left, big time range on the right."""
    return text(label, 150, y, 46, INK, "start") + num(t, 930, y + 6, size, col, "end")


# S01 훅: 쿠키 지우면 싸진다? -----------------------------------------------------------------------
scene("S01", 0, 8.6, [
    ai(8.6, (104, 114), (0, 30)),
    ("bg", bg(), {"type": "none"}),
    ("title", head("비행기표,", 540, 250, 110) + head("쿠키 지우면 싸질까?", 540, 375, 96, YELLOW), {"type": "pop", "at": 0.0, "anchor": [540, 310]}),
    ("bubble", bubble(["검색할수록", "비싸져?!"], 60, 960, 400, 200, (420, 1230), 54, [INK, RED]), {"type": "pop", "at": 3.2, "anchor": [260, 1060]}),
    ("flip", pill("사실이 아니에요!", 540, 1280, 60, RED, WHITE), {"type": "stamp", "at": 6.4, "anchor": [540, 1280]}),
])

# S02 조사 결과 --------------------------------------------------------------------------------------
def row(y, what):
    return (text(what, 160, y, 54, INK, "start", HEAD) + num("→ 그대로", 930, y, 60, GREEN, "end"))
scene("S02", 8.6, 18.2, [
    ai(9.6, (112, 104), (-30, 0)),
    ("bg", bg(), {"type": "none"}),
    ("title", head("실제로 조사해 보니", 540, 300, 106), {"type": "pop", "at": 0.0, "anchor": [540, 260]}),
    ("study", card(90, 420, 900, 120) + tag("네덜란드 시장 감독 기관(ACM) · 2026년 9월", 540, 490, 36, INK, WHITE), {"type": "pop", "at": 0.4, "anchor": [540, 480]}),
    ("rows", card(90, 580, 900, 270) + row(690, "쿠키 지우기") + f'<path d="M150 735 H930" stroke="{INK}" stroke-opacity="0.2" stroke-width="4"/>' + row(810, "기기 바꾸기"),
     {"type": "wipeD", "at": 3.7, "dur": 1.6}),
    ("sky", pill("스카이스캐너: 쿠키와 가격은 무관 (2019)", 540, 940, 40, SKY, INK), {"type": "fade", "at": 6.8}),
])

# S03 진짜 이유: 가격 칸 ----------------------------------------------------------------------------
def step(i, label, state, col, y):
    w = 560 + i * 120
    x = 540 - w / 2
    return (f'<rect x="{x + 10:.0f}" y="{y + 12}" width="{w}" height="120" rx="18" fill="{INK}"/>'
            f'<rect x="{x:.0f}" y="{y}" width="{w}" height="120" rx="18" fill="{col}" stroke="{INK}" stroke-width="8"/>'
            + text(label, x + 40, y + 80, 54, INK, "start", HEAD) + text(state, x + w - 40, y + 80, 50, INK, "end", HEAD))
ladder = step(2, "3단계", "지금 가격", "#ffb4a2", 440) + step(1, "2단계", "매진", YELLOW, 590) + step(0, "1단계", "매진", "#8bd3a0", 740)
scene("S03", 18.2, 26.7, [
    ai(8.5, (106, 116), (0, -30)),
    ("bg", bg(), {"type": "none"}),
    ("title", head("진짜 이유: 가격 단계", 540, 300, 100), {"type": "pop", "at": 0.0, "anchor": [540, 260]}),
    ("ladder", ladder, {"type": "wipeU", "at": 2.5, "dur": 2.4}),
    ("sfx", sfx("다음 단계 오픈!", 540, 990, 80, ORANGE, -6), {"type": "stamp", "at": 5.5, "anchor": [540, 960]}),
])

# S04 숫자 -------------------------------------------------------------------------------------------
scene("S04", 26.7, 34.0, [
    ai(7.3, (110, 104), (0, 30)),
    ("bg", bg(), {"type": "none"}),
    ("title", head("값은 계속 바뀐다", 540, 300, 112), {"type": "pop", "at": 0.0, "anchor": [540, 260]}),
    ("times", card(90, 420, 900, 230) + text("자리 하나, 판매 기간 동안", 540, 500, 46, INK, font=HEAD) + num("30~35번 변경", 540, 610, 96, RED),
     {"type": "pop", "at": 0.3, "anchor": [540, 535]}),
    ("third", card(90, 690, 900, 170) + text("3장 중 1장은 평균보다", 540, 765, 46, INK, font=HEAD) + num("40% 이상 비싸게", 540, 835, 64, RED),
     {"type": "pop", "at": 3.5, "anchor": [540, 775]}),
])

# S05 앞으로는 ---------------------------------------------------------------------------------------
scene("S05", 34.0, 40.5, [
    ai(6.5, (104, 114), (-20, 20)),
    ("bg", bg(), {"type": "none"}),
    ("title", head("하지만 앞으로는?", 540, 300, 112), {"type": "pop", "at": 0.0, "anchor": [540, 260]}),
    ("aiprice", pill("AI 맞춤 가격 늘어날 전망", 540, 500, 56, YELLOW), {"type": "pop", "at": 2.4, "anchor": [540, 500]}),
    ("now", tag("지금은 회원 프로그램 등 일부에서만", 540, 630, 38, INK, WHITE), {"type": "fade", "at": 3.6}),
])

# S06 퀴즈 -------------------------------------------------------------------------------------------
opts = ["출발 1년 전", "출발 두 달쯤 전", "출발 당일"]
choices = "".join(card(130, 860 + i * 140, 820, 120) + text(o, 540, 938 + i * 140, 58, INK, font=HEAD) for i, o in enumerate(opts))
scene("S06", 40.5, 49.6, [
    ai(9.1, (106, 116), (0, -30)),
    ("bg", bg(), {"type": "none"}),
    ("badge", pill("퀴즈", 540, 240, 56, RED, WHITE), {"type": "pop", "at": 0.0, "anchor": [540, 240]}),
    ("question", head("항공권 값이 크게", 540, 400, 92) + head("오르기 시작한 때는?", 540, 510, 88, YELLOW), {"type": "pop", "at": 0.3, "anchor": [540, 455]}),
    ("choices", choices, {"type": "pop", "at": 0.9, "anchor": [540, 1060]}),
    ("answer", f'<rect x="114" y="984" width="852" height="152" rx="24" fill="none" stroke="{RED}" stroke-width="14"/>' + sfx("정답!", 900, 1000, 90, RED, 12),
     {"type": "stamp", "at": 4.5, "anchor": [540, 1060]}),
    ("why", pill("그 전에 가격 알림 켜 두기", 540, 1330, 42, SKY, INK), {"type": "fade", "at": 7.0}),
])

# S07 마무리 + 구독 ---------------------------------------------------------------------------------------
scene("S07", 49.6, 58.0, [
    ai(8.4, (110, 102), (0, 0)),
    ("bg", bg(), {"type": "none"}),
    ("look", head("쿠키 대신", 540, 250, 110) + head("타이밍!", 540, 380, 130, YELLOW), {"type": "pop", "at": 0.2, "anchor": [540, 310]}),
    ("button", pill("구독하기", 540, 1250, 80, RED, WHITE), {"type": "pop", "at": 2.9, "anchor": [540, 1250]}),
    ("finger", f'<g transform="translate(0 170)">{finger}</g>', {"type": "tap", "at": 3.5, "anchor": [785, 1390]}),
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
