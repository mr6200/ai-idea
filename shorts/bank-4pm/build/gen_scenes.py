"""Generate SVG parts for all 7 scenes of the bank-4pm Short (48 s, 1080x1920).

Style (episode 23 on): Korean webtoon; episodes 24-25 continue with the same character. Each scene's bottom layer is a webtoon-style AI illustration
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


def hours(label, t, y, col=SKY, size=78):
    """Opening-hours row: label on the left, big time range on the right."""
    return text(label, 150, y, 46, INK, "start") + num(t, 930, y + 6, size, col, "end")


# S01 훅: 은행은 왜 4시에? ------------------------------------------------------------------------
scene("S01", 0, 4.8, [
    ai(4.8, (104, 114), (0, 30)),
    ("bg", bg(), {"type": "none"}),
    ("title", head("은행은 왜", 540, 300, 124) + head("4시에 문 닫을까?", 540, 440, 110, YELLOW), {"type": "pop", "at": 0.0, "anchor": [540, 370]}),
    ("sfx", sfx("철컥!", 850, 640, 110, RED, 10), {"type": "stamp", "at": 0.4, "anchor": [850, 610]}),
    ("bubble", bubble(["벌써 닫았어?!"], 50, 900, 440, 130, (500, 1000), 54), {"type": "pop", "at": 1.0, "anchor": [270, 965]}),
    ("flip", pill("사실은 정반대!", 540, 1280, 60, RED, WHITE), {"type": "stamp", "at": 3.7, "anchor": [540, 1280]}),
])

# S02 4시 이후: 현금 맞추기 ------------------------------------------------------------------------
check = lambda y, n, s: (f'<circle cx="190" cy="{y - 18}" r="34" fill="{YELLOW}" stroke="{INK}" stroke-width="6"/>' + num(n, 190, y, 44, INK)
                         + text(s, 250, y, 50, INK, "start", HEAD))
scene("S02", 4.8, 14.0, [
    ai(9.2, (112, 104), (-30, 0)),
    ("bg", bg(), {"type": "none"}),
    ("title", head("4시 이후의 은행", 540, 300, 112), {"type": "pop", "at": 0.0, "anchor": [540, 260]}),
    ("list", card(110, 980, 860, 300) + check(1090, "1", "현금을 1원까지 맞추기") + check(1210, "2", "안 맞으면 거래 내역 다시 보기"),
     {"type": "wipeD", "at": 3.0, "dur": 3.4}),
    ("sfx", sfx("착착착", 820, 860, 96, SKY, -8), {"type": "stamp", "at": 3.4, "anchor": [820, 830]}),
])

# S03 밤늦게까지 -----------------------------------------------------------------------------------
scene("S03", 14.0, 17.8, [
    ai(3.8, (106, 116), (30, -20)),
    ("bg", bg(), {"type": "none"}),
    ("title", head("일은 계속된다", 540, 300, 116), {"type": "pop", "at": 0.0, "anchor": [540, 260]}),
    ("tasks", pill("수표 정리", 270, 1020, 50, YELLOW) + pill("세금 정리", 690, 1020, 50, SKY) + pill("대출 서류", 480, 1160, 50, "#ffb4a2"),
     {"type": "pop", "at": 0.4, "anchor": [480, 1090]}),
    ("late", pill("밤늦게 끝나는 날도", 540, 1290, 52, INK, WHITE), {"type": "fade", "at": 2.2}),
])

# S04 영업시간의 변화 ------------------------------------------------------------------------------
scene("S04", 17.8, 24.6, [
    ai(6.8, (110, 104), (0, 30)),
    ("bg", bg(), {"type": "none"}),
    ("title", head("영업시간의 변화", 540, 300, 112), {"type": "pop", "at": 0.0, "anchor": [540, 260]}),
    ("rows", card(90, 440, 900, 340) + hours("코로나 때 (2021년~)", "9:30~15:30", 560, INK, 70)
     + f'<path d="M150 610 H930" stroke="{INK}" stroke-opacity="0.2" stroke-width="4"/>' + hours("2023년 1월 30일~", "9:00~16:00", 710, RED, 70),
     {"type": "wipeD", "at": 0.5, "dur": 3.4}),
])

# S05 내년 4월부터 30분 늦게 ------------------------------------------------------------------------
scene("S05", 24.6, 30.2, [
    ai(5.6, (104, 114), (-30, 20)),
    ("bg", bg(), {"type": "none"}),
    ("title", head("내년 4월부터", 540, 300, 120), {"type": "pop", "at": 0.0, "anchor": [540, 260]}),
    ("new", card(110, 440, 860, 310) + tag("2027년 4월~ · 금융 노사 합의(2026년 10월)", 540, 510, 34, INK, WHITE)
     + num("9:30~16:00", 540, 670, 120, RED), {"type": "pop", "at": 0.4, "anchor": [540, 595]}),
    ("sfx", sfx("30분 늦게!", 260, 900, 86, RED, -8), {"type": "stamp", "at": 1.0, "anchor": [260, 870]}),
])

# S06 퀴즈: 4시 넘어 급하면? ------------------------------------------------------------------------
opts = ["편의점", "탄력점포", "본점 금고"]
choices = "".join(card(130, 780 + i * 150, 820, 130) + text(o, 540, 862 + i * 150, 60, INK, font=HEAD) for i, o in enumerate(opts))
scene("S06", 30.2, 39.8, [
    ai(9.6, (106, 116), (0, -30)),
    ("bg", bg(), {"type": "none"}),
    ("badge", pill("퀴즈", 540, 240, 56, RED, WHITE), {"type": "pop", "at": 0.0, "anchor": [540, 240]}),
    ("question", head("4시 넘어 급한 은행 일,", 540, 400, 86) + head("어디로 가야 할까?", 540, 510, 92, YELLOW), {"type": "pop", "at": 0.3, "anchor": [540, 455]}),
    ("choices", choices, {"type": "pop", "at": 0.9, "anchor": [540, 925]}),
    ("answer", f'<rect x="114" y="914" width="852" height="162" rx="24" fill="none" stroke="{RED}" stroke-width="14"/>' + sfx("정답!", 900, 940, 90, RED, 12),
     {"type": "stamp", "at": 4.2, "anchor": [540, 995]}),
    ("why", pill("저녁 · 주말 점포 · 은행연합회에서 조회", 540, 1295, 44, SKY, INK), {"type": "fade", "at": 6.0}),
])

# S07 마무리 + 구독 ---------------------------------------------------------------------------------------
scene("S07", 39.8, 48.0, [
    ai(8.2, (110, 102), (0, 0)),
    ("bg", bg(), {"type": "none"}),
    ("look", head("4시 이후에도", 540, 250, 100) + head("불 켜진 은행", 540, 370, 110, YELLOW), {"type": "pop", "at": 0.2, "anchor": [540, 310]}),
    ("button", pill("구독하기", 540, 1250, 80, RED, WHITE), {"type": "pop", "at": 3.0, "anchor": [540, 1250]}),
    ("finger", f'<g transform="translate(0 170)">{finger}</g>', {"type": "tap", "at": 3.6, "anchor": [785, 1390]}),
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
