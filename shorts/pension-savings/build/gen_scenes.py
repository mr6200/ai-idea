"""Generate SVG parts for all 7 scenes of the pension-savings Short (60 s) (1080x1920).

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
        y = y0 + i * 150
        out += (text(label, x - 30, y + 56, 50, INK, "end")
                + f'<rect x="{x}" y="{y}" width="{full * frac:.0f}" height="80" rx="16" fill="{col}"/>'
                + num(value, x + full * frac + 18, y + 60, 54, INK if col == YELLOW else col, "start"))
    return out


def coins(cx, base, n, color=YELLOW):
    return "".join(f'<ellipse cx="{cx}" cy="{base - i * 24}" rx="90" ry="26" fill="{color}" stroke="{PLUM}" stroke-width="5"/>' for i in range(n))


def row(label, value, y, col=TEAL, size=58):
    """Label on the left, big value on the right, inside a card."""
    return text(label, 170, y, 46, INK, "start") + num(value, 910, y + 6, size, col, "end")


def check(cx, cy, ok=True):
    col = TEAL if ok else RED
    mark = (f'<path d="M{cx - 18} {cy} L{cx - 4} {cy + 16} L{cx + 20} {cy - 14}" fill="none" stroke="{WHITE}" stroke-width="9" stroke-linecap="round" stroke-linejoin="round"/>'
            if ok else f'<path d="M{cx - 14} {cy - 14} L{cx + 14} {cy + 14} M{cx + 14} {cy - 14} L{cx - 14} {cy + 14}" stroke="{WHITE}" stroke-width="9" stroke-linecap="round"/>')
    return f'<circle cx="{cx}" cy="{cy}" r="34" fill="{col}"/>' + mark


# S01 148만 원 돌려받는 통장? ---------------------------------------------------------------------------
scene("S01", 0, 4.6, [
    ai(4.6, (104, 116), (0, 30)),
    ("bg", bg(), {"type": "none"}),
    ("title", head("연말정산 최대", 540, 400, 110) + head("148만 원 돌려받기?", 540, 540, 100, YELLOW), {"type": "pop", "at": 0.0, "anchor": [540, 470]}),
    ("coins", coins(840, 1150, 7), {"type": "pop", "at": 0.8, "anchor": [840, 1070]}),
    ("name", pill("연금저축", 300, 900, 64, RED, WHITE), {"type": "stamp", "at": 3.4, "anchor": [300, 900]}),
])

# S02 세액공제 한도 -----------------------------------------------------------------------------------
scene("S02", 4.6, 13.0, [
    ai(8.4, (114, 104), (-30, 0)),
    ("bg", bg(), {"type": "none"}),
    ("title", head("세액공제 한도", 540, 430, 110), {"type": "pop", "at": 0.0, "anchor": [540, 410]}),
    ("limit", card(110, 600, 860, 330) + row("연금저축", "600만 원", 710) + f'<path d="M170 760 H910" stroke="{INK}" stroke-opacity="0.15" stroke-width="3"/>'
     + row("IRP와 합치면", "900만 원", 850, RED), {"type": "pop", "at": 0.4, "anchor": [540, 765]}),
    ("rate", card(110, 970, 860, 240) + text("넣은 돈의", 540, 1050, 46, INK) + num("13.2% 또는 16.5%", 540, 1160, 76, TEAL), {"type": "slideU", "at": 4.2}),
])

# S03 공제율 · 환급 계산 ---------------------------------------------------------------------------------
scene("S03", 13.0, 21.0, [
    ai(8.0, (106, 118), (30, -20)),
    ("bg", bg(), {"type": "none"}),
    ("title", head("나는 얼마 돌려받을까", 540, 430, 96), {"type": "pop", "at": 0.0, "anchor": [540, 410]}),
    ("table", card(110, 600, 860, 340) + text("총급여 기준", 540, 670, 40, INK) + row("5,500만 원 이하", "16.5%", 770, RED)
     + row("5,500만 원 초과", "13.2%", 880, TEAL), {"type": "pop", "at": 0.4, "anchor": [540, 770]}),
    ("calc", card(110, 980, 860, 250) + text("월 50만 원 · 연 600만 원 넣으면", 540, 1060, 44, INK) + num("최대 99만 원 환급", 540, 1170, 80, RED),
     {"type": "slideU", "at": 4.6}),
])

# S04 누구에게 유리? ------------------------------------------------------------------------------------
scene("S04", 21.0, 26.8, [
    ai(5.8, (112, 104), (0, 30)),
    ("bg", bg(), {"type": "none"}),
    ("title", head("이런 사람에게 유리", 540, 430, 100), {"type": "pop", "at": 0.0, "anchor": [540, 410]}),
    ("who", card(110, 600, 860, 420) + check(200, 720) + text("세금을 내는 직장인 · 자영업자", 260, 738, 48, INK, "start")
     + check(200, 900) + text("노후까지 묶어 둘 수 있는 돈", 260, 918, 48, INK, "start"), {"type": "wipeD", "at": 0.4, "dur": 3.0}),
])

# S05 주의할 점 ------------------------------------------------------------------------------------------
scene("S05", 26.8, 35.0, [
    ai(8.2, (104, 116), (-30, 20)),
    ("bg", bg(), {"type": "none"}),
    ("title", head("하지만 주의!", 540, 430, 116), {"type": "pop", "at": 0.0, "anchor": [540, 410]}),
    ("early", card(110, 590, 860, 300) + tag("55세 전에 해지하면", 540, 670, 44, RED) + num("기타소득세 16.5%", 540, 820, 86, RED), {"type": "pop", "at": 0.4, "anchor": [540, 740]}),
    ("more", pill("13.2% 공제받았다면 더 많이 냄", 540, 960, 48, PLUM, WHITE), {"type": "stamp", "at": 4.0, "anchor": [540, 960]}),
    ("zero", card(110, 1040, 860, 200) + check(200, 1140, False) + text("낸 세금이 0원이면 환급도 0원", 260, 1158, 48, INK, "start"), {"type": "slideU", "at": 6.2}),
])

# S06 퀴즈: 연금으로 받으면 세금은? ------------------------------------------------------------------------
choices = "".join(card(110 + i * 300, 760, 260, 200) + num(w, 240 + i * 300, 882, 60, INK) for i, w in enumerate(("0%", "3.3~5.5%", "16.5%")))
scene("S06", 35.0, 45.0, [
    ai(10.0, (106, 120), (0, -30)),
    ("bg", bg(), {"type": "none"}),
    ("badge", pill("퀴즈", 540, 340, 56, RED, WHITE), {"type": "pop", "at": 0.0, "anchor": [540, 340]}),
    ("question", head("55세 이후 연금으로", 540, 490, 92) + head("받으면 세금은?", 540, 610, 100, YELLOW), {"type": "pop", "at": 0.3, "anchor": [540, 550]}),
    ("choices", choices, {"type": "pop", "at": 0.8, "anchor": [540, 860]}),
    ("answer", f'<rect x="398" y="748" width="284" height="224" rx="40" fill="none" stroke="{RED}" stroke-width="12"/>' + pill("정답 · 3.3~5.5%", 540, 1060, 56, RED, WHITE),
     {"type": "stamp", "at": 4.6, "anchor": [540, 860]}),
    ("why", pill("55~69세 5.5% · 70~79세 4.4% · 80세~ 3.3%", 540, 1230, 40, TEAL, WHITE), {"type": "fade", "at": 7.8}),
])

# S07 마무리 + 구독 --------------------------------------------------------------------------------------
finger = (f'<path d="M700 1145 V1250 C700 1280 740 1300 770 1300 H820 C850 1300 870 1270 870 1240 V1200 C870 1185 845 1180 835 1195 '
          f'C835 1175 810 1170 800 1188 C800 1170 775 1165 765 1185 V1145 C765 1120 700 1120 700 1145 Z" fill="#f6d2b3" stroke="{PLUM}" stroke-width="6"/>')
scene("S07", 45.0, 60.0, [
    ai(15.0, (110, 100), (0, 0)),
    ("bg", bg(), {"type": "none"}),
    ("look", head("가입 전에", 540, 430, 110) + head("내 소득부터 확인", 540, 560, 104, YELLOW), {"type": "pop", "at": 0.2, "anchor": [540, 500]}),
    ("button", pill("구독하기", 540, 1250, 80, RED, WHITE), {"type": "pop", "at": 3.4, "anchor": [540, 1250]}),
    ("finger", f'<g transform="translate(0 170)">{finger}</g>', {"type": "tap", "at": 4.0, "anchor": [785, 1390]}),
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
