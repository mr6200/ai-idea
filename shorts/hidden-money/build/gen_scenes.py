"""Generate SVG parts for all 8 scenes of the hidden-money Short (60 s) (1080x1920).

Style (episode 13 on): 3D clay AI paintings mixed with a minimal infographic. Each scene's bottom
layer is a clay painting (Seedream 4.0 via RunPod, gen_backgrounds_seedream.py) (ai_bg/Sxx.png) that drifts slowly (kenburns); over it a teal
gradient carries the Jua headline, and the numbers sit on off-white infographic cards with big
Black Han Sans figures, a teal/red palette and Do Hyeon labels. Subtitles use Do Hyeon.

Each scene is a list of parts; each part becomes its own full-frame SVG so the exported PNG
layers line up in EffectCraft. A manifest records the timing and animation hints.
"""
import json
import os

W, H = 1080, 1920
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "svg")
LABEL = "지식 쇼츠 · 돈과 생활"

# fonts
HEAD, NUM, NOTE = "Jua", "Black Han Sans", "Do Hyeon"
FONT = NOTE  # subtitles

# palette
TEAL, TEAL_D = "#1f7a6d", "#2f5d6a"
RED, INK, CARD = "#e4572e", "#1d1d1f", "#f5f3ee"
YELLOW, WHITE, PLUM = "#ffd166", "#ffffff", "#3a2a4a"


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
    """Clay-friendly headline: Jua with a thick plum outline."""
    return text(s, x, y, size, fill, anchor, HEAD, f'stroke="{PLUM}" stroke-width="12" paint-order="stroke" stroke-linejoin="round"')


def num(s, x, y, size, fill=INK, anchor="middle"):
    return text(s, x, y, size, fill, anchor, NUM)


def pill(s, cx, cy, size=38, bg=YELLOW, fg=PLUM, font=HEAD):
    w = text_width(s, size) + 70
    h = size * 1.8
    return (f'<rect x="{cx - w / 2:.1f}" y="{cy - h / 2:.1f}" width="{w:.1f}" height="{h:.1f}" rx="{h / 2:.1f}" fill="{bg}"/>'
            + text(s, cx, cy + size * 0.36, size, fg, "middle", font))


def card(x, y, w, h, fill=CARD, rx=34):
    """Infographic card: off-white, rounded, soft drop shadow."""
    return (f'<rect x="{x + 6}" y="{y + 12}" width="{w}" height="{h}" rx="{rx}" fill="#000000" fill-opacity="0.18"/>'
            f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{fill}" fill-opacity="0.96"/>')


def tag(s, cx, cy, size=44, bg=INK, fg=WHITE):
    """Flat label chip (infographic)."""
    w = text_width(s, size) + 60
    return (f'<rect x="{cx - w / 2:.1f}" y="{cy - size * 0.85:.1f}" width="{w:.1f}" height="{size * 1.7:.1f}" rx="14" fill="{bg}"/>'
            + text(s, cx, cy + size * 0.36, size, fg, "middle", NOTE))


def svg(body):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">'
            f'<rect x="0" y="0" width="{W}" height="{H}" fill="#000000" fill-opacity="0"/>{body}</svg>')


def bg():
    """Teal gradient at the top for the headline, a soft one at the bottom for the subtitle, label pill."""
    return (f'<defs><linearGradient id="top" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{TEAL_D}" stop-opacity="0.85"/>'
            f'<stop offset="1" stop-color="{TEAL_D}" stop-opacity="0"/></linearGradient>'
            f'<linearGradient id="bot" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{TEAL_D}" stop-opacity="0"/>'
            f'<stop offset="1" stop-color="{TEAL_D}" stop-opacity="0.55"/></linearGradient></defs>'
            f'<rect x="0" y="0" width="{W}" height="720" fill="url(#top)"/>'
            f'<rect x="0" y="1300" width="{W}" height="620" fill="url(#bot)"/>'
            + pill(LABEL, 540, 200))


def ai(dur, z=(106, 116), pan=(0, 0)):
    """Bottom layer: the scene's clay painting (written by compose_bg.py) with a slow camera move."""
    return ("ai", "", {"type": "kenburns", "dur": dur, "z": z, "pan": pan})


# ---------------------------------------------------------------- scenes
scenes = []


def scene(sid, start, end, parts):
    scenes.append({"id": sid, "start": start, "end": end, "parts": parts})


def coins(cx, base, n, color=YELLOW):
    return "".join(f'<ellipse cx="{cx}" cy="{base - i * 24}" rx="90" ry="26" fill="{color}" stroke="{PLUM}" stroke-width="5"/>' for i in range(n))


def bars(rows, y0, full=520, x=300):
    """Horizontal value bars: (label, value text, fraction, colour)."""
    out = ""
    for i, (label, value, frac, col) in enumerate(rows):
        y = y0 + i * 110
        out += (text(label, x - 30, y + 52, 46, INK, "end")
                + f'<rect x="{x}" y="{y}" width="{full * frac:.0f}" height="72" rx="14" fill="{col}"/>'
                + num(value, x + full * frac + 18, y + 56, 50, INK if col == YELLOW else col, "start"))
    return out


def step(n, title, sub, y, col=TEAL):
    """Numbered how-to row inside a card."""
    return (f'<circle cx="200" cy="{y}" r="44" fill="{col}"/>' + num(str(n), 200, y + 22, 60, WHITE)
            + text(title, 270, y + 6, 54, INK, "start", NUM) + text(sub, 270, y + 62, 38, INK, "start"))


# S01 잠자는 내 돈? ------------------------------------------------------------------------------
scene("S01", 0, 5.0, [
    ai(5.0, (104, 116), (0, 30)),
    ("bg", bg(), {"type": "none"}),
    ("title", head("내 통장에", 540, 400, 120) + head("잠자는 돈이 있다?", 540, 540, 104, YELLOW), {"type": "pop", "at": 0.0, "anchor": [540, 470]}),
    ("zzz", text("Z", 760, 900, 120, WHITE, font=HEAD, extra=f'stroke="{PLUM}" stroke-width="10" paint-order="stroke"')
     + text("Z", 840, 820, 90, WHITE, font=HEAD, extra=f'stroke="{PLUM}" stroke-width="8" paint-order="stroke"')
     + text("Z", 900, 750, 64, WHITE, font=HEAD, extra=f'stroke="{PLUM}" stroke-width="6" paint-order="stroke"'), {"type": "pop", "at": 1.0, "anchor": [830, 830]}),
    ("more", pill("생각보다 많아요", 540, 1250, 56, RED, WHITE), {"type": "stamp", "at": 3.2, "anchor": [540, 1250]}),
])

# S02 18조 4천억 원 -----------------------------------------------------------------------------------
scene("S02", 5.0, 11.2, [
    ai(6.2, (114, 104), (-30, 0)),
    ("bg", bg(), {"type": "none"}),
    ("title", head("주인 없는 숨은 돈", 540, 430, 104), {"type": "pop", "at": 0.0, "anchor": [540, 410]}),
    ("total", card(110, 600, 860, 420) + tag("숨은 금융자산 (2025년 6월 말)", 540, 680, 40, TEAL) + num("18조", 540, 870, 190, RED)
     + text("4천억 원", 540, 960, 60, INK), {"type": "pop", "at": 0.6, "anchor": [540, 810]}),
    ("grow", pill("해마다 늘어요", 540, 1170, 52, PLUM, WHITE), {"type": "stamp", "at": 3.8, "anchor": [540, 1170]}),
])

# S03 무엇이 잠자고 있나 ------------------------------------------------------------------------------------
scene("S03", 11.2, 17.8, [
    ai(6.6, (106, 118), (30, -20)),
    ("bg", bg(), {"type": "none"}),
    ("title", head("무엇이 잠자고 있나", 540, 430, 100), {"type": "pop", "at": 0.0, "anchor": [540, 410]}),
    ("bars", card(90, 600, 900, 540) + text("금융위원회 · 금융감독원 (2025년 6월 말)", 540, 680, 38, INK)
     + bars([("예금", "7.5조", 7.52 / 8, TEAL), ("보험금", "5.8조", 5.85 / 8, RED), ("카드포인트", "2.9조", 2.91 / 8, YELLOW), ("증권", "2.1조", 2.07 / 8, PLUM)], 720, 440, 330),
     {"type": "wipeL", "at": 0.3, "dur": 2.6}),
])

# S04 예금: 어카운트인포 -------------------------------------------------------------------------------------
scene("S04", 17.8, 24.8, [
    ai(7.0, (112, 104), (0, 30)),
    ("bg", bg(), {"type": "none"}),
    ("title", head("① 잠든 예금", 540, 430, 116), {"type": "pop", "at": 0.0, "anchor": [540, 410]}),
    ("how", card(110, 600, 860, 300) + tag("어카운트인포", 540, 680, 48, TEAL) + text("내 계좌를 한 번에 조회", 540, 820, 60, INK), {"type": "slideL", "at": 0.3}),
    ("rule", card(110, 940, 860, 280) + text("1년 넘게 안 쓴 · 50만 원 이하", 540, 1040, 48, INK) + num("바로 옮기고 해지", 540, 1160, 76, RED), {"type": "slideR", "at": 3.0}),
])

# S05 보험금: 내보험찾아줌 -------------------------------------------------------------------------------------
scene("S05", 24.8, 29.2, [
    ai(4.4, (104, 116), (-30, 20)),
    ("bg", bg(), {"type": "none"}),
    ("title", head("② 안 찾은 보험금", 540, 430, 104), {"type": "pop", "at": 0.0, "anchor": [540, 410]}),
    ("how", card(110, 600, 860, 440) + tag("내보험찾아줌", 540, 680, 48, TEAL) + text("몰랐던 중도보험금 · 만기보험금", 540, 810, 50, INK)
     + num("숨은 보험금 10.3조", 540, 960, 80, RED), {"type": "pop", "at": 0.4, "anchor": [540, 820]}),
    ("src", text("보험업계 집계 (2025년 말)", 540, 1100, 38, WHITE), {"type": "fade", "at": 1.0}),
])

# S06 카드포인트 ------------------------------------------------------------------------------------------
scene("S06", 29.2, 37.0, [
    ai(7.8, (110, 120), (0, -30)),
    ("bg", bg(), {"type": "none"}),
    ("title", head("③ 카드포인트", 540, 430, 116), {"type": "pop", "at": 0.0, "anchor": [540, 410]}),
    ("rate", card(110, 600, 860, 400) + num("1P = 1원", 540, 790, 150, TEAL) + text("여러 카드사 포인트를 한꺼번에 계좌로", 540, 920, 44, INK),
     {"type": "pop", "at": 0.4, "anchor": [540, 800]}),
    ("gone", pill("그냥 두면 해마다 약 800억 원 소멸", 540, 1130, 48, RED, WHITE), {"type": "stamp", "at": 4.8, "anchor": [540, 1130]}),
])

# S07 퀴즈: 휴면예금, 못 찾을까? -----------------------------------------------------------------------------
choices = "".join(card(170 + i * 400, 760, 340, 200) + num(w, 340 + i * 400, 882, 54, INK) for i, w in enumerate(("못 찾는다", "찾을 수 있다")))
scene("S07", 37.0, 47.4, [
    ai(10.4, (106, 120), (0, -30)),
    ("bg", bg(), {"type": "none"}),
    ("badge", pill("퀴즈", 540, 340, 56, RED, WHITE), {"type": "pop", "at": 0.0, "anchor": [540, 340]}),
    ("question", head("5년 넘게 잠든 예금,", 540, 490, 90) + head("이제 못 찾을까?", 540, 610, 96, YELLOW), {"type": "pop", "at": 0.3, "anchor": [540, 550]}),
    ("choices", choices, {"type": "pop", "at": 0.8, "anchor": [540, 860]}),
    ("answer", f'<rect x="562" y="748" width="356" height="224" rx="40" fill="none" stroke="{RED}" stroke-width="12"/>' + pill("정답 · 찾을 수 있다", 540, 1060, 56, RED, WHITE),
     {"type": "stamp", "at": 4.4, "anchor": [740, 860]}),
    ("why", pill("서민금융진흥원 「휴면예금 찾아줌」", 540, 1230, 44, TEAL, WHITE), {"type": "fade", "at": 6.6}),
])

# S08 마무리 + 구독 --------------------------------------------------------------------------------------
finger = (f'<path d="M700 1145 V1250 C700 1280 740 1300 770 1300 H820 C850 1300 870 1270 870 1240 V1200 C870 1185 845 1180 835 1195 '
          f'C835 1175 810 1170 800 1188 C800 1170 775 1165 765 1185 V1145 C765 1120 700 1120 700 1145 Z" fill="#f6d2b3" stroke="{PLUM}" stroke-width="6"/>')
scene("S08", 47.4, 60.0, [
    ai(12.6, (110, 100), (0, 0)),
    ("bg", bg(), {"type": "none"}),
    ("look", head("오늘 5분,", 540, 430, 110) + head("내 숨은 돈 찾기", 540, 560, 104, YELLOW), {"type": "pop", "at": 0.2, "anchor": [540, 500]}),
    ("steps", card(110, 640, 860, 340) + step(1, "어카운트인포", "예금 · 카드포인트", 720) + step(2, "내보험찾아줌", "보험금", 860),
     {"type": "slideU", "at": 0.8}),
    ("button", pill("구독하기", 540, 1100, 80, RED, WHITE), {"type": "pop", "at": 3.4, "anchor": [540, 1100]}),
    ("finger", finger, {"type": "tap", "at": 4.0, "anchor": [785, 1240]}),
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
