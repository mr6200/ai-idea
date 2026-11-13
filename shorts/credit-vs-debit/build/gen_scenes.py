"""Generate SVG parts for all 8 scenes of the credit-vs-debit Short (49 s, 1080x1920).

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


# S01 훅: 체크카드만 쓰면 이득? -----------------------------------------------------------------------
scene("S01", 0, 4.6, [
    ai(4.6, (104, 114), (0, 30)),
    ("bg", bg(), {"type": "none"}),
    ("title", head("체크카드만 쓰면", 540, 300, 112) + head("손해일까?", 540, 440, 130, YELLOW), {"type": "pop", "at": 0.0, "anchor": [540, 370]}),
    ("bubble", bubble(["아껴 쓰면", "되는 거 아냐?"], 40, 520, 380, 190, (360, 780), 50), {"type": "pop", "at": 0.8, "anchor": [230, 615]}),
    ("flip", pill("놓치는 게 있어요!", 540, 1280, 60, RED, WHITE), {"type": "stamp", "at": 2.1, "anchor": [540, 1280]}),
])

# S02 신용점수는 갚은 기록 -------------------------------------------------------------------------
scene("S02", 4.6, 10.6, [
    ai(6.0, (112, 104), (-30, 0)),
    ("bg", bg(), {"type": "none"}),
    ("title", head("신용점수의 비밀", 540, 300, 112), {"type": "pop", "at": 0.0, "anchor": [540, 260]}),
    ("q", pill("빌린 돈을 잘 갚았나?", 540, 450, 54, YELLOW), {"type": "pop", "at": 0.6, "anchor": [540, 450]}),
    ("flow", flow(["쓰기", "한 달 뒤", "갚기"], 580, [WHITE, SKY, YELLOW]) + text("신용카드 = 작은 빚", 540, 800, 56, WHITE, font=HEAD, extra=f'stroke="{NAVY}" stroke-width="12" paint-order="stroke"'),
     {"type": "wipeL", "at": 2.6, "dur": 1.6}),
])

# S03 갚은 기록 vs 기록 없음 ------------------------------------------------------------------------
def col(x, name, line1, line2, mark, mcol):
    return (text(name, x, 560, 58, INK, font=HEAD) + text(line1, x, 640, 40, INK) + text(line2, x, 690, 40, INK)
            + f'<circle cx="{x}" cy="790" r="52" fill="{mcol}" stroke="{INK}" stroke-width="7"/>' + text(mark, x, 812, 64, WHITE, font=HEAD))
scene("S03", 10.6, 17.0, [
    ai(6.4, (104, 112), (20, -20)),
    ("bg", bg(), {"type": "none"}),
    ("title", head("갚은 기록 = 믿음", 540, 300, 112), {"type": "pop", "at": 0.0, "anchor": [540, 260]}),
    ("credit", card(80, 470, 440, 400) + col(300, "신용카드", "제때 갚으면", "기록이 쌓임", "O", GREEN), {"type": "pop", "at": 0.4, "anchor": [300, 670]}),
    ("debit", card(560, 470, 440, 400) + col(780, "체크카드", "점수엔 반영,", "갚은 기록은 없음", "X", RED), {"type": "pop", "at": 3.1, "anchor": [780, 670]}),
])

# S04 혜택 -------------------------------------------------------------------------------------------
scene("S04", 17.0, 20.3, [
    ai(3.3, (106, 116), (30, -20)),
    ("bg", bg(), {"type": "none"}),
    ("title", head("혜택도 차이", 540, 300, 120), {"type": "pop", "at": 0.0, "anchor": [540, 260]}),
    ("perks", pill("할인", 330, 640, 64, YELLOW) + pill("적립", 750, 640, 64, SKY), {"type": "pop", "at": 0.3, "anchor": [540, 640]}),
    ("sfx", sfx("대체로 더 커!", 540, 840, 84, ORANGE, -6), {"type": "stamp", "at": 1.6, "anchor": [540, 810]}),
])

# S05 체크카드의 반격 ------------------------------------------------------------------------------
scene("S05", 20.3, 27.3, [
    ai(7.0, (110, 104), (0, 30)),
    ("bg", bg(), {"type": "none"}),
    ("title", head("체크카드의 반격", 540, 300, 112), {"type": "pop", "at": 0.0, "anchor": [540, 260]}),
    ("news", card(90, 440, 900, 360) + tag("2026년 9~10월부터 · 금융감독원 개선안", 540, 510, 34, INK, WHITE)
     + text("은행 대출 금리 깎아 주는", 540, 620, 54, INK, font=HEAD) + text("카드 실적에", 540, 690, 54, INK, font=HEAD)
     + text("체크카드도 똑같이 인정", 540, 765, 58, RED, font=HEAD), {"type": "wipeD", "at": 2.8, "dur": 2.0}),
    ("sfx", sfx("인정!", 860, 900, 96, ORANGE, 10), {"type": "stamp", "at": 5.0, "anchor": [860, 870]}),
])

# S06 함정 -------------------------------------------------------------------------------------------
scene("S06", 27.3, 29.7, [
    ai(2.4, (104, 114), (-20, 20)),
    ("bg", bg(), {"type": "none"}),
    ("title", head("신용카드의 함정", 540, 300, 112), {"type": "pop", "at": 0.0, "anchor": [540, 260]}),
    ("sfx", sfx("주의!", 540, 1220, 130, RED, -8), {"type": "stamp", "at": 0.8, "anchor": [540, 1180]}),
])

# S07 퀴즈: 가장 피해야 할 습관 ---------------------------------------------------------------------
opts = ["매달 전액 결제", "리볼빙으로 조금씩", "체크카드도 같이"]
choices = "".join(card(130, 860 + i * 140, 820, 120) + text(o, 540, 938 + i * 140, 58, INK, font=HEAD) for i, o in enumerate(opts))
scene("S07", 29.7, 39.7, [
    ai(10.0, (106, 116), (0, -30)),
    ("bg", bg(), {"type": "none"}),
    ("badge", pill("퀴즈", 540, 240, 56, RED, WHITE), {"type": "pop", "at": 0.0, "anchor": [540, 240]}),
    ("question", head("신용카드 쓸 때", 540, 400, 92) + head("가장 피할 습관은?", 540, 510, 92, YELLOW), {"type": "pop", "at": 0.3, "anchor": [540, 455]}),
    ("choices", choices, {"type": "pop", "at": 0.9, "anchor": [540, 1060]}),
    ("answer", f'<rect x="114" y="984" width="852" height="152" rx="24" fill="none" stroke="{RED}" stroke-width="14"/>' + sfx("정답!", 900, 1000, 90, RED, 12),
     {"type": "stamp", "at": 4.1, "anchor": [540, 1060]}),
    ("why", pill("리볼빙 평균 금리 연 17.4% (2026년 7월)", 540, 1330, 40, SKY, INK), {"type": "fade", "at": 6.0}),
])

# S08 마무리 + 구독 ---------------------------------------------------------------------------------------
scene("S08", 39.7, 49.0, [
    ai(9.3, (110, 102), (0, 0)),
    ("bg", bg(), {"type": "none"}),
    ("look", head("한 장만, 조금만,", 540, 250, 100) + head("매달 다 갚기", 540, 370, 110, YELLOW), {"type": "pop", "at": 0.2, "anchor": [540, 310]}),
    ("button", pill("구독하기", 540, 1250, 80, RED, WHITE), {"type": "pop", "at": 3.9, "anchor": [540, 1250]}),
    ("finger", f'<g transform="translate(0 170)">{finger}</g>', {"type": "tap", "at": 4.5, "anchor": [785, 1390]}),
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
