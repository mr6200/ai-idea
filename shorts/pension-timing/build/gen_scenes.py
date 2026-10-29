"""Generate SVG parts for all 12 scenes of the pension-timing Short (1080x1920).

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
LABEL = "지식 쇼츠 · 노후 준비 2"

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


# cumulative pension chart: ages 60..90 on x, total received on y (monthly amount at 65 = 1)
CX0, CX1, CY0, CY1 = 190, 930, 1180, 760
PLANS = {"early": (60, 0.70, RED, "60세 70%"), "normal": (65, 1.00, INK, "65세 100%"), "late": (70, 1.36, TEAL, "70세 136%")}


def cx(age):
    return CX0 + (age - 60) * (CX1 - CX0) / 30


def cy(total):
    return CY0 - total * (CY0 - CY1) / 28


def chart_axes():
    out = f'<path d="M{CX0} {CY1 - 20} V{CY0} H{CX1 + 20}" fill="none" stroke="{INK}" stroke-width="5"/>'
    for age in (60, 65, 70, 75, 80, 85, 90):
        out += f'<path d="M{cx(age)} {CY0} v12" stroke="{INK}" stroke-width="4"/>' + text(f"{age}", cx(age), CY0 + 50, 34, INK)
    return out + text("받은 돈 합계", CX0 + 10, CY1 - 34, 34, INK, "start")


def chart_line(plan, upto=90):
    start, rate, col, label = PLANS[plan]
    x1, y1 = cx(upto), cy(rate * (upto - start))
    return f'<path d="M{cx(start)} {CY0} L{x1:.0f} {y1:.0f}" stroke="{col}" stroke-width="12" stroke-linecap="round"/>'


def legend(*plans):
    """Colour key along the top of the chart card, one entry per plan shown."""
    out = ""
    for i, plan in enumerate(plans):
        _, _, col, label = PLANS[plan]
        x = 150 + i * 280
        out += f'<path d="M{x} 655 h50" stroke="{col}" stroke-width="12" stroke-linecap="round"/>' + text(label, x + 66, 668, 36, col, "start", NUM)
    return out


def cross(age, total, label, col, dx=0):
    x, y = cx(age), cy(total)
    return (f'<circle cx="{x:.0f}" cy="{y:.0f}" r="22" fill="{YELLOW}" stroke="{PLUM}" stroke-width="6"/>'
            f'<path d="M{x:.0f} {y + 22:.0f} V{CY0}" stroke="{PLUM}" stroke-width="4" stroke-dasharray="12 8"/>'
            + pill(label, x + dx, y - 70, 40, col, WHITE))


def amounts():
    out = ""
    for i, (age, amt, col) in enumerate(((60, 70, RED), (65, 100, INK), (70, 136, TEAL))):
        x = 250 + i * 290
        h = amt * 3.2
        out += (f'<rect x="{x - 70}" y="{1180 - h:.0f}" width="140" height="{h:.0f}" rx="18" fill="{col}"/>'
                + num(f"{amt}만", x, 1160 - h, 56, col) + text(f"{age}세부터", x, 1235, 42, INK))
    return out


# S01 일찍 vs 늦게 --------------------------------------------------------------------------
scene("S01", 0, 5, [
    ai(5, (104, 118), (0, 30)),
    ("bg", bg(), {"type": "none"}),
    ("title", head("국민연금,", 540, 400, 110) + head("일찍? 늦게?", 540, 540, 120, YELLOW), {"type": "pop", "at": 0.0, "anchor": [540, 470]}),
    ("vs", card(110, 820, 380, 300) + num("60세", 300, 960, 110, RED) + text("당겨 받기", 300, 1060, 46, INK)
     + card(590, 820, 380, 300) + num("70세", 780, 960, 110, TEAL) + text("늦춰 받기", 780, 1060, 46, INK)
     + pill("VS", 540, 970, 50, PLUM, WHITE), {"type": "pop", "at": 0.8, "anchor": [540, 970]}),
    ("key", pill("몇 살까지 사느냐가 답", 540, 1260, 48, RED, WHITE), {"type": "stamp", "at": 2.6, "anchor": [540, 1260]}),
])

# S02 65세, 당기거나 늦추거나 -------------------------------------------------------------------
arrows = (f'<path d="M520 1000 H260" stroke="{RED}" stroke-width="14" stroke-linecap="round"/><path d="M280 970 L240 1000 L280 1030" fill="none" stroke="{RED}" stroke-width="14" stroke-linecap="round" stroke-linejoin="round"/>'
          f'<path d="M560 1000 H820" stroke="{TEAL}" stroke-width="14" stroke-linecap="round"/><path d="M800 970 L840 1000 L800 1030" fill="none" stroke="{TEAL}" stroke-width="14" stroke-linecap="round" stroke-linejoin="round"/>')
scene("S02", 5, 12, [
    ai(7, (114, 104), (-30, 0)),
    ("bg", bg(), {"type": "none"}),
    ("title", head("원래는 65세부터", 540, 430, 100), {"type": "pop", "at": 0.0, "anchor": [540, 410]}),
    ("base", card(110, 640, 860, 280) + tag("1969년생부터", 540, 720, 44, TEAL) + num("65세", 540, 870, 130), {"type": "pop", "at": 0.4, "anchor": [540, 780]}),
    ("move", card(110, 960, 860, 300) + arrows + num("60세", 200, 1140, 70, RED) + num("70세", 880, 1140, 70, TEAL) + text("최대 5년", 540, 1150, 44, INK),
     {"type": "slideU", "at": 3.6}),
])

# S03 -6% / +7.2% ---------------------------------------------------------------------------
scene("S03", 12, 19, [
    ai(7, (106, 116), (30, -20)),
    ("bg", bg(), {"type": "none"}),
    ("title", head("1년마다 얼마나?", 540, 430, 100), {"type": "pop", "at": 0.0, "anchor": [540, 410]}),
    ("early", card(110, 620, 860, 300) + text("당겨 받기 (조기노령연금)", 540, 700, 44, INK) + num("1년 −6% · 최대 −30%", 540, 840, 70, RED),
     {"type": "slideL", "at": 0.4}),
    ("late", card(110, 960, 860, 300) + text("늦춰 받기 (연기연금)", 540, 1040, 44, INK) + num("1년 +7.2% · 최대 +36%", 540, 1180, 66, TEAL),
     {"type": "slideR", "at": 3.4}),
])

# S04 월 100만 원이라면 -------------------------------------------------------------------------------
scene("S04", 19, 26, [
    ai(7, (110, 120), (0, 40)),
    ("bg", bg(), {"type": "none"}),
    ("title", head("월 100만 원이라면?", 540, 430, 96), {"type": "pop", "at": 0.0, "anchor": [540, 410]}),
    ("bars", card(110, 620, 860, 680) + amounts(), {"type": "wipeL", "at": 0.4, "dur": 2.4}),
])

# S05 다 더해 보면? (단순 계산) ----------------------------------------------------------------------------
stack = "".join(f'<ellipse cx="540" cy="{1150 - i * 26}" rx="120" ry="30" fill="{YELLOW}" stroke="{PLUM}" stroke-width="5"/>' for i in range(10))
scene("S05", 26, 33, [
    ai(7, (116, 106), (0, -30)),
    ("bg", bg(), {"type": "none"}),
    ("title", head("받은 돈을", 540, 410, 100) + head("다 더해 보면?", 540, 540, 110, YELLOW), {"type": "pop", "at": 0.0, "anchor": [540, 470]}),
    ("coins", card(110, 640, 860, 640) + stack + text("매달 받은 연금 합계", 540, 760, 46, INK), {"type": "pop", "at": 0.4, "anchor": [540, 960]}),
    ("note", pill("물가·이자 빼고 단순 계산", 540, 1240, 44, PLUM, WHITE), {"type": "stamp", "at": 3.6, "anchor": [540, 1240]}),
])

# S06 일찍: 77세에 따라잡힘 ------------------------------------------------------------------------------
scene("S06", 33, 41, [
    ai(8, (104, 114), (-30, 20)),
    ("bg", bg(), {"type": "none"}),
    ("title", head("일찍 받으면?", 540, 430, 100), {"type": "pop", "at": 0.0, "anchor": [540, 410]}),
    ("axes", card(90, 600, 900, 720) + chart_axes() + legend("early", "normal"), {"type": "fade", "at": 0.2}),
    ("early", chart_line("early"), {"type": "wipeL", "at": 0.6, "dur": 1.6}),
    ("normal", chart_line("normal"), {"type": "wipeL", "at": 2.0, "dur": 1.6}),
    ("cross", cross(76.7, 11.7, "약 77세 역전", RED), {"type": "stamp", "at": 4.6, "anchor": [cx(76.7), cy(11.7)]}),
])

# S07 늦게: 84세부터 앞섬 ----------------------------------------------------------------------------------
scene("S07", 41, 48, [
    ai(7, (112, 104), (20, 0)),
    ("bg", bg(), {"type": "none"}),
    ("title", head("늦게 받으면?", 540, 430, 100), {"type": "pop", "at": 0.0, "anchor": [540, 410]}),
    ("axes", card(90, 600, 900, 720) + chart_axes() + chart_line("normal") + legend("normal", "late"), {"type": "fade", "at": 0.2}),
    ("late", chart_line("late"), {"type": "wipeL", "at": 0.8, "dur": 1.6}),
    ("cross", cross(83.9, 18.9, "약 84세부터 앞섬", TEAL, -90), {"type": "stamp", "at": 3.6, "anchor": [cx(83.9), cy(18.9)]}),
])

# S08 기대여명 -----------------------------------------------------------------------------------------
scene("S08", 48, 55, [
    ai(7, (106, 118), (0, -40)),
    ("bg", bg(), {"type": "none"}),
    ("title", head("우리는 몇 살까지?", 540, 430, 96), {"type": "pop", "at": 0.0, "anchor": [540, 410]}),
    ("life", card(110, 620, 860, 380) + text("65세의 기대여명", 540, 700, 46, INK) + num("21.7년", 540, 850, 130, TEAL) + text("평균 약 87세까지 (2024년 생명표)", 540, 950, 40, INK),
     {"type": "pop", "at": 0.4, "anchor": [540, 810]}),
    ("sex", card(110, 1040, 410, 200) + text("남자", 315, 1110, 42, INK) + num("84.5세", 315, 1200, 64, INK)
     + card(560, 1040, 410, 200) + text("여자", 765, 1110, 42, INK) + num("88.7세", 765, 1200, 64, RED), {"type": "slideU", "at": 2.6}),
    ("so", pill("평균만 보면 늦게가 유리", 540, 1300, 46, TEAL, WHITE), {"type": "stamp", "at": 4.0, "anchor": [540, 1300]}),
])

# S09 하지만 일찍이 나을 때 ----------------------------------------------------------------------------------
scene("S09", 55, 62, [
    ai(7, (114, 104), (-20, 20)),
    ("bg", bg(), {"type": "none"}),
    ("title", head("일찍이 나을 때도", 540, 430, 100), {"type": "pop", "at": 0.0, "anchor": [540, 410]}),
    ("a", card(110, 620, 860, 200) + text("건강이 걱정될 때", 540, 740, 56, INK), {"type": "slideL", "at": 0.4}),
    ("b", card(110, 860, 860, 200) + text("당장 생활비가 급할 때", 540, 980, 56, INK), {"type": "slideR", "at": 1.6}),
    ("c", card(110, 1100, 860, 200) + text("다른 소득이 없을 때", 540, 1220, 56, INK), {"type": "slideL", "at": 3.6}),
])

# S10 건보료 주의 ----------------------------------------------------------------------------------------------
scene("S10", 62, 70, [
    ai(8, (104, 114), (0, 30)),
    ("bg", bg(), {"type": "none"}),
    ("title", head("주의할 점!", 540, 430, 110, YELLOW), {"type": "pop", "at": 0.0, "anchor": [540, 410]}),
    ("rule", card(110, 620, 860, 340) + text("연금 등 소득이 1년에", 540, 710, 46, INK) + num("2,000만 원 초과", 540, 850, 100, RED),
     {"type": "pop", "at": 0.4, "anchor": [540, 790]}),
    ("out", card(110, 1000, 860, 280) + text("건강보험 피부양자에서 빠져", 540, 1100, 48, INK) + num("건보료를 내야 해요", 540, 1220, 70, TEAL),
     {"type": "slideU", "at": 3.8}),
])

# S11 퀴즈: 깎인 연금, 65세 지나면 회복? ------------------------------------------------------------------------
scene("S11", 70, 80, [
    ai(10, (106, 120), (0, -30)),
    ("bg", bg(), {"type": "none"}),
    ("badge", pill("퀴즈", 540, 340, 56, RED, WHITE), {"type": "pop", "at": 0.0, "anchor": [540, 340]}),
    ("question", head("당겨 받아 깎인 연금,", 540, 490, 84) + head("65세 지나면 회복?", 540, 600, 90, YELLOW), {"type": "pop", "at": 0.3, "anchor": [540, 545]}),
    ("box", card(140, 720, 800, 460) + num("70만", 540, 880, 110, RED) + text("60세부터 받은 월 연금", 540, 960, 44, INK), {"type": "pop", "at": 0.8, "anchor": [540, 950]}),
    ("answer", pill("정답 X · 평생 70만", 540, 1080, 60, RED, WHITE), {"type": "stamp", "at": 3.6, "anchor": [540, 1080]}),
    ("why", pill("한 번 깎이면 평생 그대로", 540, 1260, 46, TEAL, WHITE), {"type": "fade", "at": 6.6}),
])

# S12 마무리 + 구독 ---------------------------------------------------------------------------------------
finger = (f'<path d="M700 1145 V1250 C700 1280 740 1300 770 1300 H820 C850 1300 870 1270 870 1240 V1200 C870 1185 845 1180 835 1195 '
          f'C835 1175 810 1170 800 1188 C800 1170 775 1165 765 1185 V1145 C765 1120 700 1120 700 1145 Z" fill="#f6d2b3" stroke="{PLUM}" stroke-width="6"/>')
scene("S12", 80, 90, [
    ai(10, (110, 100), (0, 0)),
    ("bg", bg(), {"type": "none"}),
    ("look", head("건강과 생활비 따져", 540, 430, 96) + head("받는 나이 고르기", 540, 560, 100, YELLOW), {"type": "pop", "at": 0.2, "anchor": [540, 500]}),
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
