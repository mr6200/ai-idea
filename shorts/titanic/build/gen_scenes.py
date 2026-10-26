"""Generate SVG parts for all 10 scenes of the titanic Short (1080x1920).

Style (episode 11 on): vintage poster mixed with AI engraving backgrounds; from episode 12 the AI
painting is its own "ai" layer that drifts slowly (kenburns) and the paper wash is lighter. Each scene's bg layer is
translucent aged paper with a double border and a red ribbon; compose_bg.py lays the sepia-toned
AI engraving (ai_bg/Sxx.png) underneath. Drawings are ink line art with hatching; headlines,
notes and subtitles use Nanum Myeongjo (shorts/fonts/).

Each scene is a list of parts; each part becomes its own full-frame SVG so the exported PNG
layers line up in EffectCraft. A manifest records the timing and animation hints.
"""
import json
import math
import os

W, H = 1080, 1920
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "svg")
LABEL = "지식 쇼츠 · 타이타닉"

# fonts
SERIF = "NanumMyeongjo"
FONT = SERIF  # subtitles

# palette
PAPER, PAPER_D = "#efe2c4", "#e2d1aa"
INK, BROWN = "#2b1d14", "#6b4f35"
RED, MUST = "#a8281e", "#c9912e"
WHITE = "#fffaf0"


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


def text(s, x, y, size, fill=INK, anchor="middle", weight=700, extra=""):
    assert text_width(s, size) < 1000, f"text too wide: {s}"
    s = s.replace("&", "&amp;").replace("<", "&lt;")
    return (f'<text x="{x}" y="{y}" font-family="{SERIF}" font-weight="{weight}" font-size="{size}" '
            f'fill="{fill}" text-anchor="{anchor}" {extra}>{s}</text>')


def head(s, x, y, size, fill=INK, anchor="middle"):
    """Headline: extra-bold Myeongjo with a thin paper halo so it reads over the engraving."""
    return text(s, x, y, size, fill, anchor, 800, f'stroke="{PAPER}" stroke-width="8" paint-order="stroke" stroke-linejoin="round"')


def rule(y, x1=200, x2=880):
    return f'<path d="M{x1} {y} H{x2}" stroke="{INK}" stroke-width="4"/><path d="M{x1} {y + 12} H{x2}" stroke="{INK}" stroke-width="1.5"/>'


def ribbon(s, cx, cy, size=44, fill=RED, fg=PAPER):
    w = text_width(s, size) + 120
    x0, x1, h = cx - w / 2, cx + w / 2, size * 2
    return (f'<path d="M{x0} {cy - h / 2} H{x1} L{x1 - 30} {cy} L{x1} {cy + h / 2} H{x0} L{x0 + 30} {cy} Z" fill="{fill}" stroke="{INK}" stroke-width="4"/>'
            + text(s, cx, cy + size * 0.36, size, fg, "middle", 800))


def seal(cx, cy, r, word, size=52, fill=RED, rot=0):
    body = (f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{fill}" stroke="{INK}" stroke-width="5"/>'
            f'<circle cx="{cx}" cy="{cy}" r="{r - 14}" fill="none" stroke="{PAPER}" stroke-width="2.5"/>'
            + text(word, cx, cy + size * 0.36, size, PAPER, "middle", 800))
    return f'<g transform="rotate({rot} {cx} {cy})">{body}</g>' if rot else body


def card(x, y, w, h, fill=PAPER):
    """Paper panel with a double ink border."""
    return (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{fill}" fill-opacity="0.94" stroke="{INK}" stroke-width="5"/>'
            f'<rect x="{x + 12}" y="{y + 12}" width="{w - 24}" height="{h - 24}" fill="none" stroke="{INK}" stroke-width="1.5"/>')


def note(s, cx, cy, size=48, fill=INK):
    w = text_width(s, size) + 80
    return card(cx - w / 2, cy - size * 0.95, w, size * 1.9) + text(s, cx, cy + size * 0.36, size, fill, "middle", 800)


def svg(body):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">'
            f'<rect x="0" y="0" width="{W}" height="{H}" fill="#000000" fill-opacity="0"/>{body}</svg>')


def rays(cx, cy, opacity=0.28):
    return "".join(f'<path d="M{cx} {cy} L{cx + 2200 * math.cos(math.radians(a)):.0f} {cy + 2200 * math.sin(math.radians(a)):.0f}" '
                   f'stroke="{MUST}" stroke-opacity="{opacity}" stroke-width="12"/>' for a in range(0, 360, 10))


def bg(burst=None):
    """Translucent aged paper over the AI engraving + vignette + double border + ribbon label."""
    b = (f'<defs><linearGradient id="top" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{PAPER}" stop-opacity="0.85"/>'
         f'<stop offset="1" stop-color="{PAPER}" stop-opacity="0"/></linearGradient></defs>'
         f'<rect x="0" y="0" width="{W}" height="{H}" fill="{PAPER}" fill-opacity="0.34"/>'
         f'<rect x="0" y="0" width="{W}" height="760" fill="url(#top)"/>')
    if burst:
        b += rays(*burst)
    b += (f'<rect x="0" y="0" width="{W}" height="{H}" fill="none" stroke="{BROWN}" stroke-opacity="0.35" stroke-width="90"/>'
          f'<rect x="40" y="40" width="1000" height="1840" fill="none" stroke="{INK}" stroke-width="10"/>'
          f'<rect x="62" y="62" width="956" height="1796" fill="none" stroke="{INK}" stroke-width="3"/>')
    return b + ribbon(LABEL, 540, 200, 40)


def hatch(x, y, w, h, gap=14, sw=2, color=INK, op=0.7):
    return "".join(f'<path d="M{xx} {y} V{y + h}" stroke="{color}" stroke-opacity="{op}" stroke-width="{sw}"/>' for xx in range(int(x) + gap // 2, int(x + w), gap))


def arrow(x1, y1, x2, y2, color=INK, w=6):
    ang = math.atan2(y2 - y1, x2 - x1)
    a1 = (x2 - 24 * math.cos(ang - 0.45), y2 - 24 * math.sin(ang - 0.45))
    a2 = (x2 - 24 * math.cos(ang + 0.45), y2 - 24 * math.sin(ang + 0.45))
    return (f'<path d="M{x1} {y1} L{x2} {y2} M{a1[0]:.1f} {a1[1]:.1f} L{x2} {y2} L{a2[0]:.1f} {a2[1]:.1f}" '
            f'fill="none" stroke="{color}" stroke-width="{w}" stroke-linecap="round" stroke-linejoin="round"/>')


WATER = "#56707a"


def ai(dur, z=(108, 118), pan=(0, 0)):
    """Bottom layer: the scene's AI painting (written by compose_bg.py) with a slow camera move."""
    return ("ai", "", {"type": "kenburns", "dur": dur, "z": z, "pan": pan})


def ship(cx, cy, s=1.0, broken=False):
    """Side view of the liner (bow to the right): black hull, white superstructure, four funnels."""
    p = lambda x, y: f"{cx + x * s:.0f} {cy + y * s:.0f}"
    hull = f'<path d="M{p(-430, -40)} L{p(440, -40)} L{p(400, 60)} L{p(-400, 60)} Q{p(-440, 20)} {p(-430, -40)} Z" fill="{INK}" stroke="{INK}" stroke-width="4"/>'
    deck = (f'<rect x="{cx - 330 * s:.0f}" y="{cy - 90 * s:.0f}" width="{640 * s:.0f}" height="{50 * s:.0f}" fill="{PAPER}" stroke="{INK}" stroke-width="4"/>'
            + "".join(f'<rect x="{cx + (-310 + i * 40) * s:.0f}" y="{cy - 78 * s:.0f}" width="{14 * s:.0f}" height="{16 * s:.0f}" fill="{INK}"/>' for i in range(16)))
    funnels = "".join(f'<path d="M{p(x - 26, -90)} L{p(x - 20, -200)} L{p(x + 26, -200)} L{p(x + 30, -90)} Z" fill="{MUST}" stroke="{INK}" stroke-width="4"/>'
                      f'<path d="M{p(x - 20, -200)} L{p(x + 26, -200)} L{p(x + 27, -170)} L{p(x - 21, -170)} Z" fill="{INK}"/>' for x in (-200, -70, 60, 190))
    masts = f'<path d="M{p(-380, -40)} L{p(-370, -260)} M{p(360, -40)} L{p(350, -260)}" stroke="{INK}" stroke-width="5"/>'
    body = masts + deck + funnels + hull
    if broken:
        return (f'<g transform="rotate(-22 {cx - 120 * s:.0f} {cy})"><clipPath id="aft"><rect x="{cx - 500 * s:.0f}" y="{cy - 300 * s:.0f}" width="{480 * s:.0f}" height="{400 * s:.0f}"/></clipPath><g clip-path="url(#aft)">{body}</g></g>'
                f'<g transform="rotate(30 {cx + 60 * s:.0f} {cy}) translate({40 * s:.0f} {60 * s:.0f})"><clipPath id="bow"><rect x="{cx - 20 * s:.0f}" y="{cy - 300 * s:.0f}" width="{520 * s:.0f}" height="{400 * s:.0f}"/></clipPath><g clip-path="url(#bow)">{body}</g></g>')
    return body


def compartments(x, y, w, h, flooded=0, hi=0, tilt=0):
    """Hull cut into 16 watertight compartments; bulkheads stop short of the top deck.
    flooded: compartments from the bow (right) holding water; hi: bow compartments outlined in mustard."""
    cw = w / 16
    out = f'<g transform="rotate({tilt} {x + w / 2} {y + h / 2})">'
    out += f'<path d="M{x} {y} H{x + w} L{x + w - 30} {y + h} H{x + 20} Z" fill="{PAPER}" stroke="{INK}" stroke-width="6"/>'
    for i in range(16):
        cx0 = x + w - (i + 1) * cw
        if i < flooded:
            top = y + h * (0.05 if tilt else 0.35)
            out += f'<rect x="{cx0 + 3}" y="{top}" width="{cw - 6}" height="{y + h - top - 4}" fill="{WATER}" fill-opacity="0.8"/>'
        if i < hi:
            out += f'<rect x="{cx0 + 3}" y="{y + 4}" width="{cw - 6}" height="{h - 8}" fill="none" stroke="{MUST}" stroke-width="6"/>'
    out += "".join(f'<path d="M{x + i * cw} {y + h} V{y + h * 0.3}" stroke="{INK}" stroke-width="4"/>' for i in range(1, 16))
    return out + "</g>"


def iceberg(cx, wl, s=1.0):
    """Iceberg with the water line at wl; most of it under water (hatched)."""
    p = lambda x, y: f"{cx + x * s:.0f} {wl + y * s:.0f}"
    top = f'<path d="M{p(-120, 0)} L{p(-60, -150)} L{p(-10, -110)} L{p(30, -210)} L{p(110, 0)} Z" fill="{WHITE}" stroke="{INK}" stroke-width="5" stroke-linejoin="round"/>'
    under = f'<path d="M{p(-120, 0)} L{p(-200, 140)} L{p(-90, 320)} L{p(120, 300)} L{p(220, 120)} L{p(110, 0)} Z" fill="{WATER}" fill-opacity="0.35" stroke="{INK}" stroke-width="3" stroke-dasharray="12 8"/>'
    return under + top + f'<path d="M{cx - 330 * s:.0f} {wl} H{cx + 330 * s:.0f}" stroke="{INK}" stroke-width="4"/>'


def lifeboat(cx, cy, s=1.0):
    return (f'<path d="M{cx - 60 * s:.0f} {cy} H{cx + 60 * s:.0f} L{cx + 40 * s:.0f} {cy + 30 * s:.0f} H{cx - 40 * s:.0f} Z" fill="{PAPER}" stroke="{INK}" stroke-width="4"/>'
            f'<path d="M{cx - 50 * s:.0f} {cy + 8 * s:.0f} H{cx + 50 * s:.0f}" stroke="{RED}" stroke-width="4"/>')


def bar(x, y, length, label, fill, value):
    return (f'<rect x="{x}" y="{y}" width="{length}" height="70" fill="{fill}" stroke="{INK}" stroke-width="5"/>'
            + text(label, x, y - 18, 40, INK, "start", 800) + text(value, x + length + 16, y + 50, 44, fill if fill == RED else INK, "start", 800))


def wreck(cx, bed):
    """Two pieces on the seabed, 600 m apart in reality."""
    return (f'<path d="M{cx - 380} {bed} Q{cx} {bed - 30} {cx + 380} {bed}" fill="none" stroke="{INK}" stroke-width="5"/>'
            + hatch(cx - 380, bed, 760, 40, 16, 2)
            + f'<g transform="rotate(-4 {cx - 200} {bed - 30})"><path d="M{cx - 330} {bed - 10} L{cx - 90} {bed - 16} L{cx - 110} {bed - 70} L{cx - 320} {bed - 60} Z" fill="{INK}"/>'
            f'<path d="M{cx - 280} {bed - 60} L{cx - 270} {bed - 110} L{cx - 240} {bed - 110} L{cx - 240} {bed - 60} Z" fill="{MUST}" stroke="{INK}" stroke-width="3"/></g>'
            + f'<g transform="rotate(6 {cx + 220} {bed - 30})"><path d="M{cx + 70} {bed - 14} L{cx + 360} {bed - 10} L{cx + 330} {bed - 80} L{cx + 90} {bed - 70} Z" fill="{INK}"/></g>')

# ---------------------------------------------------------------- scenes
scenes = []


def scene(sid, start, end, parts):
    scenes.append({"id": sid, "start": start, "end": end, "parts": parts})


# S01 침몰하지 않는 배가 왜? ------------------------------------------------------------------
scene("S01", 0, 5, [
    ai(5, (106, 120), (0, 40)),
    ("bg", bg(), {"type": "none"}),
    ("title", head("침몰하지 않는 배,", 540, 400, 88) + head("왜 가라앉았을까?", 540, 520, 100, RED) + rule(570),
     {"type": "pop", "at": 0.0, "anchor": [540, 460]}),
    ("time", seal(820, 1180, 120, "2시간 40분", 38, RED, -8), {"type": "stamp", "at": 2.8, "anchor": [820, 1180]}),
])

# S02 1912년 4월 첫 항해 ------------------------------------------------------------------------
scene("S02", 5, 12, [
    ai(7, (112, 104), (-40, 0)),
    ("bg", bg(), {"type": "none"}),
    ("title", head("1912년 4월", 540, 410, 104) + text("당시 세계 최대 여객선 · 첫 항해", 540, 500, 44, BROWN, "middle", 800) + rule(550),
     {"type": "pop", "at": 0.0, "anchor": [540, 450]}),
    ("ship", card(70, 760, 940, 420) + ship(540, 1050, 0.95), {"type": "slideR", "at": 0.5}),
    ("name", ribbon("거의 가라앉지 않는 배", 540, 1300, 48), {"type": "stamp", "at": 3.6, "anchor": [540, 1300]}),
])

# S03 16개의 방수 칸 ------------------------------------------------------------------------------
scene("S03", 12, 19, [
    ai(7, (104, 114), (30, -30)),
    ("bg", bg(), {"type": "none"}),
    ("title", head("비밀은 16개의 방수 칸", 540, 430, 84) + rule(480), {"type": "pop", "at": 0.0, "anchor": [540, 410]}),
    ("hull", card(60, 700, 960, 420) + compartments(110, 820, 860, 220) + text("뱃머리 →", 900, 790, 36, BROWN, "middle", 800), {"type": "pop", "at": 0.4, "anchor": [540, 910]}),
    ("four", compartments(110, 820, 860, 220, 0, 4).replace(f'fill="{PAPER}" stroke="{INK}" stroke-width="6"', 'fill="none" stroke="none"')
     + note("앞쪽 4칸까지는 괜찮아요", 540, 1290, 46), {"type": "pop", "at": 3.4, "anchor": [540, 1100]}),
])

# S04 4월 14일 밤 빙산 -------------------------------------------------------------------------------
scene("S04", 19, 26, [
    ai(7, (110, 120), (0, -50)),
    ("bg", bg(), {"type": "none"}),
    ("title", head("4월 14일 밤", 540, 430, 100) + rule(480), {"type": "pop", "at": 0.0, "anchor": [540, 410]}),
    ("scene", card(60, 600, 960, 640) + iceberg(280, 920, 0.95) + ship(740, 880, 0.55), {"type": "fade", "at": 0.3}),
    ("scrape", f'<path d="M520 905 L960 905" stroke="{RED}" stroke-width="10" stroke-dasharray="26 12"/>' + text("옆구리가 긁혔어요", 740, 990, 38, RED, "middle", 800),
     {"type": "wipeL", "at": 1.6, "dur": 1.0}),
    ("six", seal(820, 1200, 110, "6칸 파손", 44, RED, -8), {"type": "stamp", "at": 3.6, "anchor": [820, 1200]}),
])

# S05 벽 꼭대기가 뚫려 있었다 ----------------------------------------------------------------------------
spill = "".join(arrow(820 - i * 54, 820 - i * 4, 790 - i * 54, 850 - i * 4, RED, 6) for i in range(5))
scene("S05", 26, 33, [
    ai(7, (116, 106), (0, 30)),
    ("bg", bg(), {"type": "none"}),
    ("title", head("벽 꼭대기가", 540, 410, 96) + head("뚫려 있었어요", 540, 520, 96, RED) + rule(570), {"type": "pop", "at": 0.0, "anchor": [540, 460]}),
    ("hull", card(60, 640, 960, 520) + compartments(110, 800, 860, 220, 6, 0, 8), {"type": "pop", "at": 0.4, "anchor": [540, 900]}),
    ("spill", spill + compartments(110, 800, 860, 220, 9, 0, 8).replace(f'fill="{PAPER}" stroke="{INK}" stroke-width="6"', 'fill="none" stroke="none"'),
     {"type": "wipeL", "at": 3.4, "dur": 1.6}),
    ("tray", note("얼음틀처럼 넘쳤어요", 540, 1290, 46), {"type": "pop", "at": 4.0, "anchor": [540, 1290]}),
])

# S06 구명보트 20척 ---------------------------------------------------------------------------------------
boats = "".join(lifeboat(170 + (i % 10) * 82, 1080 + (i // 10) * 60, 0.6) for i in range(20))
scene("S06", 33, 40, [
    ai(7, (104, 112), (-30, 0)),
    ("bg", bg(), {"type": "none"}),
    ("title", head("구명보트는 20척", 540, 430, 96) + rule(480), {"type": "pop", "at": 0.0, "anchor": [540, 410]}),
    ("bars", card(60, 600, 960, 640) + bar(120, 720, 330, "구명보트 자리", RED, "1,178명분"), {"type": "wipeL", "at": 0.4, "dur": 1.0}),
    ("people", bar(120, 900, 620, "탄 사람", INK, "2,200여 명"), {"type": "wipeL", "at": 3.4, "dur": 1.2}),
    ("boats", boats, {"type": "fade", "at": 1.4}),
])

# S07 둘로 부러진 배 ---------------------------------------------------------------------------------------
scene("S07", 40, 47, [
    ai(7, (108, 122), (0, 60)),
    ("bg", bg(), {"type": "none"}),
    ("title", head("배는 둘로 부러져", 540, 430, 92) + rule(480), {"type": "pop", "at": 0.0, "anchor": [540, 410]}),
    ("ship", card(60, 620, 960, 560) + f'<path d="M100 980 H980" stroke="{INK}" stroke-width="5"/>' + ship(540, 930, 0.8, True), {"type": "fade", "at": 0.3}),
    ("lost", ribbon("약 1,500명 희생", 540, 1300, 50), {"type": "stamp", "at": 3.6, "anchor": [540, 1300]}),
])

# S08 그 뒤로 바뀐 규칙 -------------------------------------------------------------------------------------
scene("S08", 47, 54, [
    ai(7, (114, 104), (40, 0)),
    ("bg", bg(), {"type": "none"}),
    ("title", head("그 뒤로 바뀐 규칙", 540, 430, 92) + rule(480), {"type": "pop", "at": 0.0, "anchor": [540, 410]}),
    ("year", seal(540, 680, 100, "1914", 56, RED), {"type": "stamp", "at": 0.4, "anchor": [540, 680]}),
    ("boats", note("모든 승객 몫의 구명보트", 540, 900, 50), {"type": "slideL", "at": 0.8}),
    ("ice", note("국제 빙산 순찰대", 540, 1110, 50), {"type": "slideR", "at": 3.4}),
])

# S09 퀴즈: 몇 년 만에 발견? ----------------------------------------------------------------------------------
scene("S09", 54, 62, [
    ai(8, (106, 118), (0, -40)),
    ("bg", bg(burst=(540, 980)), {"type": "none"}),
    ("badge", ribbon("퀴즈", 540, 360, 56), {"type": "pop", "at": 0.0, "anchor": [540, 360]}),
    ("question", head("사고 뒤 몇 년 만에", 540, 500, 84) + head("발견됐을까?", 540, 610, 96, RED), {"type": "pop", "at": 0.3, "anchor": [540, 560]}),
    ("sea", card(60, 700, 960, 560) + wreck(540, 1180)
     + f'<path d="M940 760 V1150 M920 760 H960 M920 1150 H960" stroke="{INK}" stroke-width="4"/>' + text("약 4,000m", 920, 960, 40, INK, "end", 800),
     {"type": "fade", "at": 0.8}),
    ("answer", seal(300, 880, 120, "73년", 64, RED, -8), {"type": "stamp", "at": 3.6, "anchor": [300, 880]}),
    ("when", note("1985년 발견", 540, 1330, 44), {"type": "pop", "at": 6.0, "anchor": [540, 1330]}),
])

# S10 교훈 + 구독 ---------------------------------------------------------------------------------------------
finger = (f'<path d="M700 1145 V1250 C700 1280 740 1300 770 1300 H820 C850 1300 870 1270 870 1240 V1200 C870 1185 845 1180 835 1195 '
          f'C835 1175 810 1170 800 1188 C800 1170 775 1165 765 1185 V1145 C765 1120 700 1120 700 1145 Z" fill="#d9b48f" stroke="{INK}" stroke-width="6"/>')
scene("S10", 62, 70, [
    ai(8, (110, 100), (0, 0)),
    ("bg", bg(), {"type": "none"}),
    ("look", head("가라앉지 않는 배는", 540, 430, 88) + head("없다", 540, 560, 130, RED) + rule(610), {"type": "pop", "at": 0.2, "anchor": [540, 500]}),
    ("ship", ship(540, 860, 0.7), {"type": "fade", "at": 0.6}),
    ("button", ribbon("구독하기", 540, 1080, 80), {"type": "pop", "at": 4.2, "anchor": [540, 1080]}),
    ("finger", finger, {"type": "tap", "at": 5.0, "anchor": [785, 1220]}),
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
