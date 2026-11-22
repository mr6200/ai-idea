"""Generate SVG parts for all 7 scenes of the year-end-tax Short (53 s, 1080x1920).

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


# S01 훅: 연말정산은 1월? -------------------------------------------------------------------------
scene("S01", 0, 6.6, [
    ai(6.6, (104, 112), (0, 20)),
    ("bg", bg(), {"type": "none"}),
    ("title", head("연말정산,", 540, 260, 120) + head("12월에 끝난다!", 540, 395, 110, YELLOW), {"type": "pop", "at": 0.0, "anchor": [540, 330]}),
    ("sfx", sfx("땡!", 860, 560, 120, ORANGE, 10), {"type": "stamp", "at": 1.9, "anchor": [860, 530]}),
    ("flip", pill("승부는 12월 31일", 540, 1280, 60, RED, WHITE), {"type": "stamp", "at": 2.4, "anchor": [540, 1280]}),
])

# S02 ① 연말정산 미리보기 ------------------------------------------------------------------------------
scene("S02", 6.6, 14.6, [
    ai(8.0, (112, 104), (-30, 0)),
    ("bg", bg(), {"type": "none"}),
    ("title", head("① 연말정산 미리보기", 540, 300, 100), {"type": "pop", "at": 0.0, "anchor": [540, 260]}),
    ("how", card(90, 420, 900, 250) + tag("홈택스 · 무료", 540, 490, 38, INK, WHITE)
     + text("1~9월 카드 사용액으로", 540, 580, 52, INK, font=HEAD) + text("예상 환급액 미리 계산", 540, 645, 52, RED, font=HEAD),
     {"type": "wipeD", "at": 2.8, "dur": 1.6}),
    ("tip", pill("토해낼 것 같으면 지금 손쓰기", 540, 760, 48, YELLOW), {"type": "pop", "at": 5.6, "anchor": [540, 760]}),
])

# S03 ② 연금저축 · IRP --------------------------------------------------------------------------------
scene("S03", 14.6, 23.4, [
    ai(8.8, (106, 116), (0, -30)),
    ("bg", bg(), {"type": "none"}),
    ("title", head("② 연금저축 · IRP", 540, 270, 100), {"type": "pop", "at": 0.0, "anchor": [540, 230]}),
    ("limit", card(90, 720, 900, 220) + tag("12월 31일 납입분까지 올해 공제", 540, 790, 38, INK, WHITE) + num("합쳐서 900만 원", 540, 905, 84, INK),
     {"type": "pop", "at": 0.6, "anchor": [540, 830]}),
    ("back", card(90, 980, 900, 200) + text("최대 16.5% 돌려받으면", 540, 1055, 48, INK, font=HEAD) + num("148만 5천 원", 540, 1145, 80, RED),
     {"type": "pop", "at": 5.4, "anchor": [540, 1080]}),
])

# S04 ③ 고향사랑기부 ---------------------------------------------------------------------------------
scene("S04", 23.4, 30.6, [
    ai(7.2, (104, 112), (0, 20)),
    ("bg", bg(), {"type": "none"}),
    ("title", head("③ 고향사랑기부", 540, 260, 112), {"type": "pop", "at": 0.0, "anchor": [540, 220]}),
    ("flow", flow(["기부 10만", "공제 10만", "선물 3만"], 360, [WHITE, SKY, YELLOW]), {"type": "wipeL", "at": 2.2, "dur": 2.4}),
    ("gift", sfx("답례품까지!", 300, 1220, 84, ORANGE, -8), {"type": "stamp", "at": 5.1, "anchor": [300, 1190]}),
])

# S05 단, 조건 ----------------------------------------------------------------------------------------
scene("S05", 30.6, 34.2, [
    ai(3.6, (104, 114), (-20, 20)),
    ("bg", bg(), {"type": "none"}),
    ("title", head("단, 조건!", 540, 300, 130), {"type": "pop", "at": 0.0, "anchor": [540, 260]}),
    ("cond", pill("내야 할 세금(결정세액)이 있어야", 540, 450, 48, YELLOW), {"type": "pop", "at": 0.4, "anchor": [540, 450]}),
])

# S06 퀴즈 -------------------------------------------------------------------------------------------
opts = ["10만 원", "3만 원", "0원"]
choices = "".join(card(130, 860 + i * 140, 820, 120) + text(o, 540, 938 + i * 140, 62, INK, font=HEAD) for i, o in enumerate(opts))
scene("S06", 34.2, 43.8, [
    ai(9.6, (106, 116), (0, -30)),
    ("bg", bg(), {"type": "none"}),
    ("badge", pill("퀴즈", 540, 210, 52, RED, WHITE), {"type": "pop", "at": 0.0, "anchor": [540, 210]}),
    ("question", head("10만 원 기부, 다 돌려받으면", 540, 330, 66) + head("실제 부담은?", 540, 435, 96, YELLOW), {"type": "pop", "at": 0.3, "anchor": [540, 385]}),
    ("choices", choices, {"type": "pop", "at": 0.9, "anchor": [540, 1060]}),
    ("answer", f'<rect x="114" y="1124" width="852" height="152" rx="24" fill="none" stroke="{RED}" stroke-width="14"/>' + sfx("정답!", 900, 1140, 90, RED, 12),
     {"type": "stamp", "at": 4.9, "anchor": [540, 1200]}),
    ("why", pill("답례품 3만 원만큼 이득", 540, 1330, 42, SKY, INK), {"type": "fade", "at": 7.5}),
])

# S07 마무리 + 구독 ---------------------------------------------------------------------------------------
scene("S07", 43.8, 53.0, [
    ai(9.2, (110, 102), (0, 0)),
    ("bg", bg(), {"type": "none"}),
    ("look", head("마감은", 540, 250, 110) + head("12월 31일!", 540, 380, 130, YELLOW), {"type": "pop", "at": 0.2, "anchor": [540, 310]}),
    ("button", pill("구독하기", 540, 1250, 80, RED, WHITE), {"type": "pop", "at": 3.3, "anchor": [540, 1250]}),
    ("finger", f'<g transform="translate(0 170)">{finger}</g>', {"type": "tap", "at": 3.9, "anchor": [785, 1390]}),
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
