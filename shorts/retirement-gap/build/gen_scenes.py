"""Generate SVG parts for all 12 scenes of the retirement-gap Short (1080x1920).

Style (episode 13): 3D clay AI paintings mixed with a minimal infographic. Each scene's bottom
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
LABEL = "지식 쇼츠 · 노후 준비"

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


def timeline(y, x0=120, x1=960, start=60, end=65, label_gap="소득 0원?", gap_years="5년"):
    """Salary bar, hatched gap, pension dot: the income crevasse."""
    gx0, gx1 = 540, 860
    hatch = "".join(f'<path d="M{x} {y + 60} l40 -60" stroke="{RED}" stroke-width="6"/>' for x in range(gx0 + 10, gx1 - 30, 26))
    return (num(str(start), 230, y - 70, 130) + num(str(end), 900, y - 70, 130, TEAL)
            + f'<rect x="{x0}" y="{y}" width="{gx0 - x0}" height="60" rx="30" fill="{INK}"/>'
            + f'<rect x="{gx0}" y="{y}" width="{gx1 - gx0}" height="60" fill="none" stroke="{RED}" stroke-width="6" stroke-dasharray="14 10"/>' + hatch
            + f'<rect x="{gx1}" y="{y}" width="{x1 - gx1}" height="60" rx="30" fill="{TEAL}"/>'
            + text("월급", 330, y + 110, 44, INK) + text("연금", 910, y + 110, 44, TEAL)
            + num(gap_years, 700, y - 24, 64, RED) + num(label_gap, 700, y + 140, 56, RED))


def age_table(x, y):
    rows = [("1953~56년생", "61세"), ("1957~60년생", "62세"), ("1961~64년생", "63세"), ("1965~68년생", "64세"), ("1969년생~", "65세")]
    out = ""
    for i, (born, age) in enumerate(rows):
        yy = y + i * 92
        hi = i == 4
        out += (f'<rect x="{x}" y="{yy}" width="760" height="76" rx="18" fill="{TEAL if hi else WHITE}"/>'
                + text(born, x + 40, yy + 52, 44, WHITE if hi else INK, "start", NOTE)
                + num(age, x + 720, yy + 56, 52, WHITE if hi else TEAL, "end"))
    return out


def bridge(y, labels, lit=4):
    """A bridge over the 60-65 gap held up by up to four pillars."""
    out = (f'<path d="M100 {y} H220 M860 {y} H980" stroke="{INK}" stroke-width="16" stroke-linecap="round"/>'
           f'<path d="M220 {y} Q540 {y - 40} 860 {y}" fill="none" stroke="{TEAL}" stroke-width="22" stroke-linecap="round"/>'
           + num("60", 160, y - 30, 60) + num("65", 920, y - 30, 60, TEAL))
    for i, lab in enumerate(labels):
        x = 300 + i * 160
        col = TEAL if i < lit else "#c9c4b8"
        out += (f'<rect x="{x - 26}" y="{y - 8}" width="52" height="260" rx="10" fill="{col}"/>'
                + text(lab, x, y + 300, 36, INK if i < lit else "#9a958a", "middle", NOTE))
    return out


def coins(cx, cy, n, color=YELLOW):
    return "".join(f'<ellipse cx="{cx}" cy="{cy - i * 22}" rx="70" ry="22" fill="{color}" stroke="{PLUM}" stroke-width="5"/>' for i in range(n))


# ---------------------------------------------------------------- scenes
scenes = []


def scene(sid, start, end, parts):
    scenes.append({"id": sid, "start": start, "end": end, "parts": parts})


# S01 60세 퇴직, 연금은 65세? ----------------------------------------------------------------
scene("S01", 0, 5, [
    ai(5, (104, 118), (0, 30)),
    ("bg", bg(), {"type": "none"}),
    ("title", head("60세 퇴직,", 540, 400, 110) + head("연금은 65세부터?", 540, 540, 110, YELLOW),
     {"type": "pop", "at": 0.0, "anchor": [540, 470]}),
    ("gap", card(80, 820, 920, 420) + timeline(1000), {"type": "pop", "at": 2.4, "anchor": [540, 1030]}),
])

# S02 정년은 아직 60세 ---------------------------------------------------------------------
scene("S02", 5, 12, [
    ai(7, (114, 104), (-30, 0)),
    ("bg", bg(), {"type": "none"}),
    ("title", head("법정 정년은", 540, 410, 100) + head("지금도 60세", 540, 540, 110, YELLOW), {"type": "pop", "at": 0.0, "anchor": [540, 470]}),
    ("law", card(140, 760, 800, 300) + tag("고령자고용법", 540, 840, 44, TEAL) + num("60세 이상", 540, 990, 110), {"type": "pop", "at": 0.5, "anchor": [540, 910]}),
    ("talk", card(140, 1110, 800, 170) + text("65세 연장은 국회에서 논의 중", 540, 1180, 48, INK) + text("2026년 10월 기준, 아직 확정 안 됨", 540, 1245, 38, RED),
     {"type": "slideU", "at": 3.6}),
])

# S03 국민연금 수급 나이 ------------------------------------------------------------------------
scene("S03", 12, 19, [
    ai(7, (106, 116), (30, -20)),
    ("bg", bg(), {"type": "none"}),
    ("title", head("국민연금은 언제부터?", 540, 430, 96), {"type": "pop", "at": 0.0, "anchor": [540, 410]}),
    ("table", card(110, 640, 860, 560) + age_table(160, 690), {"type": "wipeD", "at": 0.4, "dur": 1.2}),
    ("hi", pill("1969년생부터 65세", 540, 1270, 46, RED, WHITE), {"type": "stamp", "at": 3.6, "anchor": [540, 1270]}),
])

# S04 소득 크레바스 ---------------------------------------------------------------------------
scene("S04", 19, 26, [
    ai(7, (110, 120), (0, 50)),
    ("bg", bg(), {"type": "none"}),
    ("title", head("월급도 연금도 없는", 540, 410, 96) + head("5년", 540, 540, 130, YELLOW), {"type": "pop", "at": 0.0, "anchor": [540, 470]}),
    ("gap", card(80, 760, 920, 420) + timeline(940), {"type": "pop", "at": 0.5, "anchor": [540, 970]}),
    ("name", pill("소득 크레바스", 540, 1270, 56, RED, WHITE), {"type": "stamp", "at": 3.6, "anchor": [540, 1270]}),
])

# S05 생활비 300만 원 × 60개월 ----------------------------------------------------------------------
scene("S05", 26, 33, [
    ai(7, (116, 106), (0, -30)),
    ("bg", bg(), {"type": "none"}),
    ("title", head("5년 생활비는?", 540, 430, 100), {"type": "pop", "at": 0.0, "anchor": [540, 410]}),
    ("month", card(110, 640, 860, 300) + text("부부 적정 생활비 (한 달)", 540, 720, 44, INK) + num("약 300만 원", 540, 860, 110, TEAL),
     {"type": "pop", "at": 0.4, "anchor": [540, 790]}),
    ("times", text("× 60개월", 540, 1030, 64, WHITE, "middle", NUM, f'stroke="{PLUM}" stroke-width="10" paint-order="stroke"'), {"type": "fade", "at": 3.2}),
    ("total", card(110, 1080, 860, 210) + num("약 1억 8천만 원", 540, 1220, 100, RED), {"type": "stamp", "at": 3.8, "anchor": [540, 1185]}),
])

# S06 다리 1: 조기수령 ----------------------------------------------------------------------------
bars = "".join(f'<rect x="{170 + i * 130}" y="{1180 - (100 - 6 * i) * 4.6:.0f}" width="96" height="{(100 - 6 * i) * 4.6:.0f}" rx="12" fill="{TEAL if i == 0 else RED}"/>'
               + text(f"{65 - i}세", 218 + i * 130, 1230, 38, INK) + num(f"{100 - 6 * i}%", 218 + i * 130, 1160 - (100 - 6 * i) * 4.6, 40, TEAL if i == 0 else RED)
               for i in range(6))
scene("S06", 33, 41, [
    ai(8, (104, 114), (-30, 20)),
    ("bg", bg(), {"type": "none"}),
    ("title", head("다리 ① 연금 당겨 받기", 540, 430, 88), {"type": "pop", "at": 0.0, "anchor": [540, 410]}),
    ("chart", card(110, 600, 860, 680) + text("조기노령연금 (최대 5년 앞당김)", 540, 670, 42, INK), {"type": "pop", "at": 0.3, "anchor": [540, 940]}),
    ("bars", bars, {"type": "wipeL", "at": 1.0, "dur": 2.0}),
    ("cut", pill("1년에 6%씩, 평생 감액", 540, 1290, 46, RED, WHITE), {"type": "stamp", "at": 4.4, "anchor": [540, 1290]}),
])

# S07 다리 2: 퇴직금·개인연금 ------------------------------------------------------------------------
scene("S07", 41, 48, [
    ai(7, (112, 104), (20, 0)),
    ("bg", bg(), {"type": "none"}),
    ("title", head("다리 ② 퇴직금 · 개인연금", 540, 430, 84), {"type": "pop", "at": 0.0, "anchor": [540, 410]}),
    ("acct", card(110, 620, 400, 330) + tag("IRP", 310, 710, 48, TEAL) + num("55세~", 310, 870, 90)
     + card(570, 620, 400, 330) + tag("연금저축", 770, 710, 48, TEAL) + num("55세~", 770, 870, 90), {"type": "pop", "at": 0.4, "anchor": [540, 785]}),
    ("tax", card(110, 1000, 860, 260) + text("퇴직금을 연금으로 나눠 받으면", 540, 1080, 44, INK) + num("퇴직소득세 30% ↓", 540, 1205, 84, RED),
     {"type": "slideU", "at": 3.6}),
])

# S08 다리 3: 주택연금 ------------------------------------------------------------------------------
house = (f'<path d="M380 1000 L540 860 L700 1000 Z" fill="{RED}" stroke="{PLUM}" stroke-width="6" stroke-linejoin="round"/>'
         f'<rect x="410" y="1000" width="260" height="190" fill="{WHITE}" stroke="{PLUM}" stroke-width="6"/>'
         f'<rect x="510" y="1080" width="60" height="110" fill="{TEAL}"/>')
scene("S08", 48, 55, [
    ai(7, (106, 118), (0, -40)),
    ("bg", bg(), {"type": "none"}),
    ("title", head("다리 ③ 내 집으로 연금", 540, 430, 88), {"type": "pop", "at": 0.0, "anchor": [540, 410]}),
    ("home", card(110, 620, 860, 640) + tag("주택연금", 540, 710, 48, TEAL) + house, {"type": "pop", "at": 0.4, "anchor": [540, 940]}),
    ("rule", text("부부 중 1명 55세 이상", 540, 790, 44, INK), {"type": "fade", "at": 1.2}),
    ("monthly", coins(820, 1180, 5) + text("매달", 820, 1000, 44, INK) + coins(260, 1180, 3) + text("살면서", 260, 1050, 44, INK),
     {"type": "pop", "at": 3.6, "anchor": [540, 1100]}),
])

# S09 다리 4: 일 -------------------------------------------------------------------------------------
scene("S09", 55, 62, [
    ai(7, (114, 104), (-20, 20)),
    ("bg", bg(), {"type": "none"}),
    ("title", head("다리 ④ 일하는 소득", 540, 430, 92), {"type": "pop", "at": 0.0, "anchor": [540, 410]}),
    ("work", card(110, 620, 860, 300) + text("재취업 · 계속 고용 · 작은 일거리", 540, 720, 46, INK) + num("월 100만 원이라도", 540, 850, 80, TEAL),
     {"type": "pop", "at": 0.4, "anchor": [540, 770]}),
    ("why", card(110, 970, 860, 260) + text("버는 만큼 모아 둔 돈을", 540, 1060, 46, INK) + num("덜 꺼내 써요", 540, 1180, 84, RED),
     {"type": "slideU", "at": 3.6}),
])

# S10 정리: 네 개의 다리 -------------------------------------------------------------------------------
scene("S10", 62, 70, [
    ai(8, (104, 114), (0, 30)),
    ("bg", bg(), {"type": "none"}),
    ("title", head("5년 다리는", 540, 410, 100) + head("여러 개로 받쳐요", 540, 540, 100, YELLOW), {"type": "pop", "at": 0.0, "anchor": [540, 470]}),
    ("bridge", card(80, 650, 920, 640) + bridge(820, ["조기연금", "개인연금", "주택연금", "일"], 0), {"type": "pop", "at": 0.4, "anchor": [540, 970]}),
    ("lit", bridge(820, ["조기연금", "개인연금", "주택연금", "일"], 4), {"type": "wipeL", "at": 3.8, "dur": 1.6}),
])

# S11 퀴즈: 5년 늦게 받으면? -------------------------------------------------------------------------------
scene("S11", 70, 80, [
    ai(10, (106, 120), (0, -30)),
    ("bg", bg(), {"type": "none"}),
    ("badge", pill("퀴즈", 540, 340, 56, RED, WHITE), {"type": "pop", "at": 0.0, "anchor": [540, 340]}),
    ("question", head("국민연금을 5년 늦게 받으면", 540, 490, 76) + head("얼마나 더 받을까?", 540, 600, 90, YELLOW), {"type": "pop", "at": 0.3, "anchor": [540, 545]}),
    ("box", card(140, 720, 800, 420) + text("월 100만 원이었다면", 540, 810, 46, INK), {"type": "pop", "at": 0.8, "anchor": [540, 930]}),
    ("answer", num("+36%", 540, 990, 170, RED) + num("월 136만 원", 540, 1100, 70, TEAL), {"type": "stamp", "at": 3.6, "anchor": [540, 980]}),
    ("why", pill("1년에 7.2%씩 증가", 540, 1250, 46, TEAL, WHITE), {"type": "fade", "at": 6.6}),
])

# S12 마무리 + 구독 ---------------------------------------------------------------------------------------
finger = (f'<path d="M700 1145 V1250 C700 1280 740 1300 770 1300 H820 C850 1300 870 1270 870 1240 V1200 C870 1185 845 1180 835 1195 '
          f'C835 1175 810 1170 800 1188 C800 1170 775 1165 765 1185 V1145 C765 1120 700 1120 700 1145 Z" fill="#f6d2b3" stroke="{PLUM}" stroke-width="6"/>')
scene("S12", 80, 90, [
    ai(10, (110, 100), (0, 0)),
    ("bg", bg(), {"type": "none"}),
    ("look", head("은퇴 준비는", 540, 430, 100) + head("5년 공백 메우기부터", 540, 560, 96, YELLOW), {"type": "pop", "at": 0.2, "anchor": [540, 500]}),
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
