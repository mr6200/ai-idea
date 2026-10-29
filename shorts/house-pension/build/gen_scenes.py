"""Generate SVG parts for all 12 scenes of the house-pension Short (1080x1920).

Style (episode 13 on): 3D clay AI paintings mixed with a minimal infographic. Each scene's bottom
layer is a RunPod clay painting (ai_bg/Sxx.png) that drifts slowly (kenburns); over it a teal
gradient carries the Jua headline, and the numbers sit on off-white infographic cards with big
Black Han Sans figures, a teal/red palette and Do Hyeon labels. Subtitles use Do Hyeon.

Each scene is a list of parts; each part becomes its own full-frame SVG so the exported PNG
layers line up in EffectCraft. A manifest records the timing and animation hints.
"""
import json
import os

W, H = 1080, 1920
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "svg")
LABEL = "지식 쇼츠 · 노후 준비 4"

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


def house(cx, base, s=1.0, door=TEAL):
    """Flat infographic house: red roof, white walls, teal door (base = ground line)."""
    p = lambda x, y: f"{cx + x * s:.0f} {base + y * s:.0f}"
    return (f'<path d="M{p(-170, -190)} L{p(0, -330)} L{p(170, -190)} Z" fill="{RED}" stroke="{PLUM}" stroke-width="{6 * s:.0f}" stroke-linejoin="round"/>'
            f'<rect x="{cx - 140 * s:.0f}" y="{base - 190 * s:.0f}" width="{280 * s:.0f}" height="{190 * s:.0f}" fill="{WHITE}" stroke="{PLUM}" stroke-width="{6 * s:.0f}"/>'
            f'<rect x="{cx - 30 * s:.0f}" y="{base - 110 * s:.0f}" width="{60 * s:.0f}" height="{110 * s:.0f}" fill="{door}"/>'
            f'<rect x="{cx - 115 * s:.0f}" y="{base - 160 * s:.0f}" width="{60 * s:.0f}" height="{50 * s:.0f}" fill="{YELLOW}" stroke="{PLUM}" stroke-width="{4 * s:.0f}"/>'
            f'<rect x="{cx + 55 * s:.0f}" y="{base - 160 * s:.0f}" width="{60 * s:.0f}" height="{50 * s:.0f}" fill="{YELLOW}" stroke="{PLUM}" stroke-width="{4 * s:.0f}"/>')


def person(cx, base, col=TEAL, s=1.0):
    return (f'<circle cx="{cx}" cy="{base - 150 * s:.0f}" r="{34 * s:.0f}" fill="#f6d2b3" stroke="{PLUM}" stroke-width="5"/>'
            f'<path d="M{cx - 55 * s:.0f} {base} Q{cx - 55 * s:.0f} {base - 110 * s:.0f} {cx} {base - 110 * s:.0f} Q{cx + 55 * s:.0f} {base - 110 * s:.0f} {cx + 55 * s:.0f} {base} Z" fill="{col}" stroke="{PLUM}" stroke-width="5"/>')


def price_vs_pension():
    """House price line falling while the monthly pension stays flat."""
    out = f'<path d="M170 1180 H930 M170 760 V1180" stroke="{INK}" stroke-width="5" fill="none"/>'
    out += f'<path d="M200 820 C380 830 520 960 900 1080" fill="none" stroke="{RED}" stroke-width="12" stroke-linecap="round"/>' + text("집값", 900, 1060, 40, RED, "end", NUM)
    out += f'<path d="M200 940 H900" stroke="{TEAL}" stroke-width="12" stroke-linecap="round"/>' + text("월 연금", 900, 920, 40, TEAL, "end", NUM)
    return out


def debt_bars():
    """Received pension plus interest and fees grows each year against the house value."""
    out = f'<path d="M170 1180 H930" stroke="{INK}" stroke-width="5"/>'
    for i in range(6):
        h = 60 + i * 62
        x = 210 + i * 110
        out += (f'<rect x="{x}" y="{1180 - h}" width="70" height="{h}" rx="10" fill="{TEAL}"/>'
                + f'<rect x="{x}" y="{1180 - h}" width="70" height="{h * 0.28:.0f}" rx="10" fill="{RED}"/>')
    return (out + f'<path d="M170 800 H930" stroke="{PLUM}" stroke-width="6" stroke-dasharray="16 10"/>' + text("집값", 930, 780, 40, PLUM, "end", NUM)
            + text("받은 돈", 330, 1235, 36, TEAL, "middle", NUM) + text("+ 이자·보증료", 640, 1235, 36, RED, "middle", NUM))


# S01 집은 있는데 현금이 없다면? ------------------------------------------------------------------
scene("S01", 0, 5, [
    ai(5, (104, 118), (0, 30)),
    ("bg", bg(), {"type": "none"}),
    ("title", head("집은 있는데", 540, 400, 110) + head("현금이 없다면?", 540, 540, 110, YELLOW), {"type": "pop", "at": 0.0, "anchor": [540, 470]}),
    ("house", card(110, 720, 860, 480) + house(400, 1130, 1.0) + coins(780, 1130, 6) + text("매달 월급?", 780, 820, 46, INK), {"type": "pop", "at": 0.8, "anchor": [540, 960]}),
    ("name", pill("주택연금", 540, 1270, 60, RED, WHITE), {"type": "stamp", "at": 2.6, "anchor": [540, 1270]}),
])

# S02 집을 담보로 매달 연금, 계속 거주 ---------------------------------------------------------------
scene("S02", 5, 12, [
    ai(7, (114, 104), (-30, 0)),
    ("bg", bg(), {"type": "none"}),
    ("title", head("내 집에 살면서", 540, 410, 100) + head("매달 연금", 540, 540, 110, YELLOW), {"type": "pop", "at": 0.0, "anchor": [540, 470]}),
    ("flow", card(110, 660, 860, 560) + house(300, 1080, 0.8) + f'<path d="M470 900 H640" stroke="{TEAL}" stroke-width="14" stroke-linecap="round"/><path d="M620 870 L660 900 L620 930" fill="none" stroke="{TEAL}" stroke-width="14" stroke-linecap="round" stroke-linejoin="round"/>'
     + coins(800, 1060, 6) + text("집을 담보로", 300, 1170, 40, INK) + text("매달 받아요", 800, 1170, 40, INK), {"type": "wipeL", "at": 0.4, "dur": 1.6}),
    ("live", pill("계속 그 집에 살아요", 540, 1290, 50, RED, WHITE), {"type": "stamp", "at": 3.6, "anchor": [540, 1290]}),
])

# S03 가입 조건 ------------------------------------------------------------------------------------
scene("S03", 12, 19, [
    ai(7, (106, 116), (30, -20)),
    ("bg", bg(), {"type": "none"}),
    ("title", head("가입 조건", 540, 430, 110), {"type": "pop", "at": 0.0, "anchor": [540, 410]}),
    ("age", card(110, 620, 860, 300) + tag("나이", 540, 700, 44, TEAL) + num("부부 중 1명 만 55세+", 540, 850, 74, INK), {"type": "slideL", "at": 0.4}),
    ("price", card(110, 960, 860, 300) + tag("집값", 540, 1040, 44, TEAL) + num("공시가격 12억 원 이하", 540, 1190, 70, INK), {"type": "slideR", "at": 3.4}),
])

# S04 72세 4억 → 월 133만 원 -----------------------------------------------------------------------------
scene("S04", 19, 26, [
    ai(7, (110, 120), (0, 40)),
    ("bg", bg(), {"type": "none"}),
    ("title", head("얼마나 받을까?", 540, 430, 104), {"type": "pop", "at": 0.0, "anchor": [540, 410]}),
    ("case", card(110, 620, 860, 260) + num("72세", 330, 790, 110, INK) + num("4억 원 집", 730, 790, 90, INK), {"type": "pop", "at": 0.4, "anchor": [540, 750]}),
    ("pay", card(110, 920, 860, 360) + text("매달 평생 (종신 정액형)", 540, 1000, 44, INK) + num("약 133만 원", 540, 1170, 130, TEAL), {"type": "stamp", "at": 3.4, "anchor": [540, 1100]}),
])

# S05 나이·집값 ↑ → 더 받음, 2026년 3월 +3.13% --------------------------------------------------------------
scene("S05", 26, 33, [
    ai(7, (116, 106), (0, -30)),
    ("bg", bg(), {"type": "none"}),
    ("title", head("이럴수록 더 받아요", 540, 430, 96), {"type": "pop", "at": 0.0, "anchor": [540, 410]}),
    ("more", card(110, 620, 410, 320) + text("나이가", 315, 720, 48, INK) + num("많을수록 ↑", 315, 850, 62, TEAL)
     + card(560, 620, 410, 320) + text("집값이", 765, 720, 48, INK) + num("비쌀수록 ↑", 765, 850, 62, TEAL), {"type": "pop", "at": 0.4, "anchor": [540, 780]}),
    ("up", card(110, 980, 860, 280) + text("2026년 3월 신규 가입부터", 540, 1060, 44, INK) + num("평균 +3.13%", 540, 1200, 100, RED), {"type": "slideU", "at": 3.6}),
])

# S06 장점 ① 배우자 100% 그대로 ---------------------------------------------------------------------------
scene("S06", 33, 41, [
    ai(8, (104, 114), (-30, 20)),
    ("bg", bg(), {"type": "none"}),
    ("title", head("장점 ① 부부 평생", 540, 430, 100), {"type": "pop", "at": 0.0, "anchor": [540, 410]}),
    ("couple", card(110, 620, 860, 560) + person(400, 1050, TEAL) + person(680, 1050, RED) + text("한 명이 먼저 떠나도", 540, 1130, 46, INK), {"type": "pop", "at": 0.4, "anchor": [540, 900]}),
    ("same", pill("남은 배우자 100% 그대로", 540, 1280, 52, TEAL, WHITE), {"type": "stamp", "at": 3.8, "anchor": [540, 1280]}),
])

# S07 장점 ② 집값 떨어져도 그대로, 국가 보증 --------------------------------------------------------------------
scene("S07", 41, 48, [
    ai(7, (112, 104), (20, 0)),
    ("bg", bg(), {"type": "none"}),
    ("title", head("장점 ② 집값이 떨어져도", 540, 430, 88), {"type": "pop", "at": 0.0, "anchor": [540, 410]}),
    ("chart", card(110, 640, 860, 640) + price_vs_pension(), {"type": "wipeL", "at": 0.4, "dur": 2.0}),
    ("gov", pill("나라가 지급 보증", 540, 1290, 52, RED, WHITE), {"type": "stamp", "at": 3.6, "anchor": [540, 1290]}),
])

# S08 장점 ③ 남으면 자녀에게, 모자라도 청구 없음 ------------------------------------------------------------------
scene("S08", 48, 55, [
    ai(7, (106, 118), (0, -40)),
    ("bg", bg(), {"type": "none"}),
    ("title", head("장점 ③ 정산할 때", 540, 430, 100), {"type": "pop", "at": 0.0, "anchor": [540, 410]}),
    ("left", card(110, 620, 860, 300) + text("집값이 받은 돈보다 많으면", 540, 710, 46, INK) + num("남은 돈은 자녀에게", 540, 850, 74, TEAL), {"type": "slideL", "at": 0.4}),
    ("short", card(110, 960, 860, 300) + text("집값이 받은 돈보다 적어도", 540, 1050, 46, INK) + num("자녀에게 청구 안 해요", 540, 1190, 70, RED), {"type": "slideR", "at": 3.4}),
])

# S09 단점 ① 이자가 쌓여 물려주기 어려움 ----------------------------------------------------------------------------
scene("S09", 55, 62, [
    ai(7, (114, 104), (-20, 20)),
    ("bg", bg(), {"type": "none"}),
    ("title", head("단점 ① 이자가 쌓여요", 540, 430, 96), {"type": "pop", "at": 0.0, "anchor": [540, 410]}),
    ("bars", card(110, 640, 860, 640) + debt_bars(), {"type": "wipeL", "at": 0.4, "dur": 2.4}),
    ("heir", pill("집 물려주기는 어려워요", 540, 1335, 50, RED, WHITE), {"type": "stamp", "at": 3.6, "anchor": [540, 1335]}),
])

# S10 단점 ② 집값 올라도 그대로, 중도해지 비용 ------------------------------------------------------------------------
scene("S10", 62, 70, [
    ai(8, (104, 114), (0, 30)),
    ("bg", bg(), {"type": "none"}),
    ("title", head("단점 ② · ③", 540, 430, 110), {"type": "pop", "at": 0.0, "anchor": [540, 410]}),
    ("up", card(110, 620, 860, 300) + text("집값이 올라도", 540, 710, 50, INK) + num("월 연금은 그대로", 540, 850, 76, TEAL), {"type": "slideL", "at": 0.4}),
    ("quit", card(110, 960, 860, 300) + text("중간에 그만두면", 540, 1050, 50, INK) + num("받은 돈 + 이자 상환", 540, 1190, 72, RED), {"type": "slideR", "at": 3.8}),
])

# S11 퀴즈: 해지 후 바로 재가입? ----------------------------------------------------------------------------------
scene("S11", 70, 80, [
    ai(10, (106, 120), (0, -30)),
    ("bg", bg(), {"type": "none"}),
    ("badge", pill("퀴즈", 540, 340, 56, RED, WHITE), {"type": "pop", "at": 0.0, "anchor": [540, 340]}),
    ("question", head("해지하고 같은 집으로", 540, 490, 84) + head("바로 다시 가입?", 540, 600, 96, YELLOW), {"type": "pop", "at": 0.3, "anchor": [540, 545]}),
    ("ox", card(140, 720, 360, 360) + num("O", 320, 960, 200, INK) + card(580, 720, 360, 360) + num("X", 760, 960, 200, INK), {"type": "pop", "at": 0.8, "anchor": [540, 900]}),
    ("answer", f'<rect x="566" y="706" width="388" height="388" rx="48" fill="none" stroke="{RED}" stroke-width="14"/>' + pill("정답 X", 760, 1150, 56, RED, WHITE),
     {"type": "stamp", "at": 3.6, "anchor": [760, 900]}),
    ("why", pill("같은 집은 3년 뒤에 다시", 540, 1270, 46, TEAL, WHITE), {"type": "fade", "at": 6.6}),
])

# S12 마무리 + 구독 ---------------------------------------------------------------------------------------
finger = (f'<path d="M700 1145 V1250 C700 1280 740 1300 770 1300 H820 C850 1300 870 1270 870 1240 V1200 C870 1185 845 1180 835 1195 '
          f'C835 1175 810 1170 800 1188 C800 1170 775 1165 765 1185 V1145 C765 1120 700 1120 700 1145 Z" fill="#f6d2b3" stroke="{PLUM}" stroke-width="6"/>')
scene("S12", 80, 90, [
    ai(10, (110, 100), (0, 0)),
    ("bg", bg(), {"type": "none"}),
    ("look", head("집 한 채가", 540, 430, 104) + head("노후 월급으로", 540, 560, 110, YELLOW), {"type": "pop", "at": 0.2, "anchor": [540, 500]}),
    ("button", pill("구독하기", 540, 1080, 80, RED, WHITE), {"type": "pop", "at": 4.8, "anchor": [540, 1080]}),
    ("finger", finger, {"type": "tap", "at": 5.6, "anchor": [785, 1220]}),
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
