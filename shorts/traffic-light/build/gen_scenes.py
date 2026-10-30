"""Generate SVG parts for all 10 scenes of the traffic-light Short (1080x1920).

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
LABEL = "지식 쇼츠 · 신호등"

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


LAMP = {"r": "#c0392b", "y": "#e0a020", "g": "#2e8b57", "b": "#1fa38f", "w": "#fff6d8", "off": "#3a2e24"}


def ai(dur, z=(108, 118), pan=(0, 0)):
    """Bottom layer: the scene's AI engraving (written by compose_bg.py) with a slow camera move."""
    return ("ai", "", {"type": "kenburns", "dur": dur, "z": z, "pan": pan})


def lamp(cx, cy, r, col, lit=True):
    glow = (f'<circle cx="{cx}" cy="{cy}" r="{r * 1.6:.0f}" fill="{LAMP[col]}" fill-opacity="0.25"/>' if lit else "")
    return glow + f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{LAMP[col] if lit else LAMP["off"]}" stroke="{INK}" stroke-width="5"/>'


def signal(cx, cy, lit="ryg", order="ryg", s=1.0, vertical=True):
    """Signal head: dark housing with lamps; `lit` lists which colours glow."""
    n = len(order)
    r, gap = 56 * s, 140 * s
    w, h = (170 * s, gap * n + 30 * s) if vertical else (gap * n + 30 * s, 170 * s)
    out = f'<rect x="{cx - w / 2:.0f}" y="{cy - h / 2:.0f}" width="{w:.0f}" height="{h:.0f}" rx="{28 * s:.0f}" fill="{INK}" stroke="{INK}" stroke-width="6"/>'
    for i, c in enumerate(order):
        off = (i - (n - 1) / 2) * gap
        x, y = (cx, cy + off) if vertical else (cx + off, cy)
        out += lamp(x, y, r, c, c in lit)
    return out


def semaphore(cx, base, s=1.0, arms="stop", night=None):
    """Knight's 1868 signal: a tall pillar, two semaphore arms and a gas lantern on top."""
    p = lambda x, y: f"{cx + x * s:.0f} {base + y * s:.0f}"
    out = (f'<path d="M{p(-26, 0)} L{p(-18, -560)} L{p(18, -560)} L{p(26, 0)} Z" fill="{BROWN}" stroke="{INK}" stroke-width="6"/>'
           + hatch(cx - 20 * s, base - 550 * s, 40 * s, 540 * s, 10, 2)
           + f'<rect x="{cx - 70 * s:.0f}" y="{base - 30 * s:.0f}" width="{140 * s:.0f}" height="{30 * s:.0f}" fill="{BROWN}" stroke="{INK}" stroke-width="5"/>')
    ang = 0 if arms == "stop" else 45
    for sx in (-1, 1):
        out += (f'<g transform="rotate({sx * ang} {cx} {base - 480 * s})"><rect x="{cx + (0 if sx > 0 else -230 * s):.0f}" y="{base - 495 * s:.0f}" width="{230 * s:.0f}" height="{32 * s:.0f}" '
                f'fill="{RED}" stroke="{INK}" stroke-width="5"/><rect x="{cx + (150 if sx > 0 else -190) * s:.0f}" y="{base - 495 * s:.0f}" width="{40 * s:.0f}" height="{32 * s:.0f}" fill="{PAPER}"/></g>')
    out += (f'<rect x="{cx - 50 * s:.0f}" y="{base - 640 * s:.0f}" width="{100 * s:.0f}" height="{90 * s:.0f}" rx="{10 * s:.0f}" fill="{MUST}" stroke="{INK}" stroke-width="6"/>'
            f'<path d="M{p(-60, -640)} L{p(0, -690)} L{p(60, -640)} Z" fill="{INK}"/>')
    if night:
        out += lamp(cx, base - 595 * s, 34 * s, night)
    return out


def lantern(cx, cy, col, s=1.0, broken=False):
    """Railway hand lamp: brass body with a coloured lens (or a bare white flame when the lens is gone)."""
    out = (f'<rect x="{cx - 80 * s:.0f}" y="{cy - 110 * s:.0f}" width="{160 * s:.0f}" height="{220 * s:.0f}" rx="{20 * s:.0f}" fill="{MUST}" stroke="{INK}" stroke-width="6"/>'
           f'<path d="M{cx - 50 * s:.0f} {cy - 110 * s:.0f} Q{cx:.0f} {cy - 190 * s:.0f} {cx + 50 * s:.0f} {cy - 110 * s:.0f}" fill="none" stroke="{INK}" stroke-width="8"/>')
    out += lamp(cx, cy, 56 * s, "w" if broken else col)
    if broken:
        out += (f'<path d="M{cx + 90 * s:.0f} {cy + 140 * s:.0f} l{40 * s:.0f} {-30 * s:.0f} l{20 * s:.0f} {40 * s:.0f} Z" fill="{LAMP[col]}" stroke="{INK}" stroke-width="4"/>'
                f'<path d="M{cx + 70 * s:.0f} {cy + 170 * s:.0f} l{50 * s:.0f} 10" stroke="{LAMP[col]}" stroke-width="6"/>')
    return out


def fog(x, y, w, h):
    """Soft fog band: overlapping pale ellipses."""
    return "".join(f'<ellipse cx="{x + (i * 137) % w}" cy="{y + (i * 71) % h}" rx="{120 + (i % 3) * 40}" ry="40" fill="{PAPER}" fill-opacity="0.55"/>' for i in range(14))


def star(cx, cy, r=16):
    pts = " ".join(f"{cx + (r if i % 2 == 0 else r * 0.45) * math.cos(math.pi * i / 5 - math.pi / 2):.0f},{cy + (r if i % 2 == 0 else r * 0.45) * math.sin(math.pi * i / 5 - math.pi / 2):.0f}" for i in range(10))
    return f'<polygon points="{pts}" fill="{LAMP["w"]}" stroke="{INK}" stroke-width="2"/>'

# ---------------------------------------------------------------- scenes
scenes = []


def scene(sid, start, end, parts):
    scenes.append({"id": sid, "start": start, "end": end, "parts": parts})


# S01 왜 빨강·노랑·초록? ----------------------------------------------------------------------
scene("S01", 0, 5, [
    ai(5, (106, 120), (0, 30)),
    ("bg", bg(), {"type": "none"}),
    ("title", head("신호등은 왜", 540, 400, 100) + head("빨강·노랑·초록?", 540, 530, 110, RED) + rule(580), {"type": "pop", "at": 0.0, "anchor": [540, 470]}),
    ("sig", card(320, 640, 440, 640) + signal(540, 960, "ryg"), {"type": "pop", "at": 0.6, "anchor": [540, 960]}),
    ("train", seal(840, 1200, 105, "기차?", 54, RED, -8), {"type": "stamp", "at": 2.8, "anchor": [840, 1200]}),
])

# S02 1868년 런던, 세계 첫 신호등 -------------------------------------------------------------------
scene("S02", 5, 12, [
    ai(7, (112, 104), (-40, 0)),
    ("bg", bg(), {"type": "none"}),
    ("title", head("1868년 런던", 540, 410, 104) + text("국회의사당 앞 · 세계 첫 신호등", 540, 500, 44, BROWN, "middle", 800) + rule(550),
     {"type": "pop", "at": 0.0, "anchor": [540, 450]}),
    ("pole", semaphore(540, 1320, 0.95), {"type": "wipeU", "at": 0.4, "dur": 1.2}),
    ("note", note("철도 신호를 본뜬 팔", 300, 1010, 40), {"type": "pop", "at": 2.4, "anchor": [300, 1010]}),
    ("gas", semaphore(540, 1320, 0.95, "stop", "r") + note("밤엔 가스등", 800, 700, 40, RED), {"type": "fade", "at": 4.0}),
])

# S03 가스 폭발 ------------------------------------------------------------------------------------
boom = "".join(f'<path d="M540 720 L{540 + 200 * math.cos(math.radians(a)):.0f} {720 + 200 * math.sin(math.radians(a)):.0f}" stroke="{MUST}" stroke-width="10"/>' for a in range(0, 360, 30))
scene("S03", 12, 19, [
    ai(7, (104, 116), (30, -30)),
    ("bg", bg(burst=(540, 900)), {"type": "none"}),
    ("title", head("한 달도 안 돼", 540, 410, 96) + head("가스 폭발!", 540, 530, 110, RED) + rule(580), {"type": "pop", "at": 0.0, "anchor": [540, 470]}),
    ("pole", semaphore(540, 1320, 0.95, "stop", "r"), {"type": "none"}),
    ("boom", boom + seal(540, 720, 110, "쾅!", 80, RED, -6), {"type": "stamp", "at": 2.0, "anchor": [540, 720]}),
    ("hurt", note("경찰관이 다쳤어요", 540, 1290, 46, RED), {"type": "pop", "at": 4.4, "anchor": [540, 1290]}),
])

# S04 철도 신호: 빨강 멈춤, 흰색 출발 -----------------------------------------------------------------
scene("S04", 19, 26, [
    ai(7, (110, 120), (0, -40)),
    ("bg", bg(), {"type": "none"}),
    ("title", head("색은 기차에서 왔어요", 540, 430, 90) + rule(480), {"type": "pop", "at": 0.0, "anchor": [540, 410]}),
    ("lamps", card(90, 600, 900, 520) + lantern(320, 840, "r") + text("멈춤", 320, 1060, 56, RED, "middle", 800)
     + lantern(760, 840, "w") + text("출발", 760, 1060, 56, INK, "middle", 800), {"type": "pop", "at": 0.4, "anchor": [540, 860]}),
    ("old", note("초기 철도 신호 (1830~40년대)", 540, 1260, 40), {"type": "fade", "at": 1.4}),
])

# S05 흰빛의 문제 → 초록·노랑 -------------------------------------------------------------------------
stars = "".join(star(x, y) for x, y in ((180, 700), (300, 660), (860, 690), (950, 760), (620, 650)))
scene("S05", 26, 33, [
    ai(7, (116, 106), (0, 30)),
    ("bg", bg(), {"type": "none"}),
    ("title", head("흰빛은 헷갈렸어요", 540, 430, 92) + rule(480), {"type": "pop", "at": 0.0, "anchor": [540, 410]}),
    ("night", card(90, 600, 900, 520) + f'<rect x="110" y="620" width="860" height="480" fill="{INK}" fill-opacity="0.85"/>' + stars
     + lantern(320, 900, "w", 0.8) + lantern(720, 900, "r", 0.8, True) + text("별빛·가로등?", 320, 1080, 40, PAPER, "middle", 800)
     + text("빨간 유리가 빠지면?", 720, 1080, 40, PAPER, "middle", 800), {"type": "fade", "at": 0.3}),
    ("new", card(90, 1150, 900, 170) + lamp(230, 1235, 40, "g") + text("출발은 초록", 400, 1250, 46, INK, "middle", 800)
     + lamp(620, 1235, 40, "y") + text("주의는 노랑", 800, 1250, 46, INK, "middle", 800), {"type": "slideU", "at": 3.6}),
])

# S06 왜 빨강이 멈춤? + 안개 오해 ---------------------------------------------------------------------
scene("S06", 33, 41, [
    ai(8, (104, 114), (-30, 20)),
    ("bg", bg(), {"type": "none"}),
    ("title", head("왜 빨강이 멈춤일까?", 540, 430, 90) + rule(480), {"type": "pop", "at": 0.0, "anchor": [540, 410]}),
    ("danger", card(90, 600, 900, 280) + lamp(220, 740, 60, "r") + text("피와 불, 오래된", 560, 720, 50, INK, "middle", 800) + text("위험의 색", 560, 800, 60, RED, "middle", 800),
     {"type": "slideL", "at": 0.4}),
    ("fog", card(90, 920, 900, 400) + lamp(260, 1110, 50, "r") + lamp(540, 1110, 50, "y") + lamp(820, 1110, 50, "g") + fog(110, 1040, 860, 150)
     + text("빨강이 안개를 잘 뚫는다?", 540, 990, 44, INK, "middle", 800), {"type": "fade", "at": 3.8}),
    ("myth", seal(850, 1250, 90, "오해!", 48, RED, -8) + text("모든 색이 비슷하게 흩어져요", 430, 1290, 38, RED, "middle", 800), {"type": "stamp", "at": 5.4, "anchor": [850, 1250]}),
])

# S07 1914 클리블랜드 첫 전기 신호등 ---------------------------------------------------------------------
scene("S07", 41, 48, [
    ai(7, (112, 104), (20, 0)),
    ("bg", bg(), {"type": "none"}),
    ("title", head("1914년 클리블랜드", 540, 410, 96) + text("미국 · 첫 전기 신호등", 540, 500, 44, BROWN, "middle", 800) + rule(550),
     {"type": "pop", "at": 0.0, "anchor": [540, 450]}),
    ("sig", card(320, 640, 440, 500) + signal(540, 890, "rg", "rg"), {"type": "pop", "at": 0.6, "anchor": [540, 890]}),
    ("two", note("빨강과 초록, 두 색뿐", 540, 1260, 48, RED), {"type": "pop", "at": 3.6, "anchor": [540, 1260]}),
])

# S08 1920 디트로이트, 노란불 ------------------------------------------------------------------------------
scene("S08", 48, 55, [
    ai(7, (106, 118), (0, -40)),
    ("bg", bg(), {"type": "none"}),
    ("title", head("1920년 디트로이트", 540, 410, 96) + text("경찰관 윌리엄 포츠", 540, 500, 44, BROWN, "middle", 800) + rule(550),
     {"type": "pop", "at": 0.0, "anchor": [540, 450]}),
    ("sig", card(320, 620, 440, 640) + signal(540, 940, "y"), {"type": "pop", "at": 0.6, "anchor": [540, 940]}),
    ("amber", seal(840, 940, 100, "노랑!", 52, MUST, -8), {"type": "stamp", "at": 3.6, "anchor": [840, 940]}),
    ("three", ribbon("세 가지 색 신호등", 540, 1310, 50), {"type": "stamp", "at": 4.4, "anchor": [540, 1310]}),
])

# S09 푸른빛 초록 (색약 배려) ---------------------------------------------------------------------------------
scene("S09", 55, 62, [
    ai(7, (114, 104), (-20, 20)),
    ("bg", bg(), {"type": "none"}),
    ("title", head("초록불의 비밀", 540, 430, 100) + rule(480), {"type": "pop", "at": 0.0, "anchor": [540, 410]}),
    ("cmp", card(90, 600, 900, 560) + lamp(300, 820, 110, "g") + text("그냥 초록", 300, 1040, 46, INK, "middle", 800)
     + lamp(780, 820, 110, "b") + text("푸른빛 초록", 780, 1040, 46, LAMP["b"], "middle", 800), {"type": "pop", "at": 0.4, "anchor": [540, 860]}),
    ("why", note("색약인 사람도 구별하기 쉽게", 540, 1270, 44, RED), {"type": "pop", "at": 3.6, "anchor": [540, 1270]}),
])

# S10 정리 ---------------------------------------------------------------------------------------------------
scene("S10", 62, 70, [
    ai(8, (104, 114), (0, 30)),
    ("bg", bg(), {"type": "none"}),
    ("title", head("정리하면", 540, 430, 110) + rule(480), {"type": "pop", "at": 0.0, "anchor": [540, 410]}),
    ("r", card(90, 600, 900, 200) + lamp(220, 700, 50, "r") + text("빨강: 오래된 위험의 색", 580, 720, 50, INK, "middle", 800), {"type": "slideL", "at": 0.4}),
    ("g", card(90, 840, 900, 200) + lamp(220, 940, 50, "g") + text("초록: 헷갈리던 흰색 대신", 580, 960, 48, INK, "middle", 800), {"type": "slideR", "at": 2.6}),
    ("y", card(90, 1080, 900, 200) + lamp(220, 1180, 50, "y") + text("노랑: 그 사이 주의", 580, 1200, 50, INK, "middle", 800), {"type": "slideL", "at": 4.8}),
])

# S11 퀴즈: 세로 신호등 빨간불 위치 -------------------------------------------------------------------------------
scene("S11", 70, 80, [
    ai(10, (106, 120), (0, -30)),
    ("bg", bg(burst=(540, 980)), {"type": "none"}),
    ("badge", ribbon("퀴즈", 540, 360, 56), {"type": "pop", "at": 0.0, "anchor": [540, 360]}),
    ("question", head("세로 신호등의 빨간불,", 540, 500, 80) + head("항상 어디에 있을까?", 540, 610, 90, RED), {"type": "pop", "at": 0.3, "anchor": [540, 555]}),
    ("sig", card(320, 680, 440, 600) + signal(540, 980, "", "ryg", 0.9), {"type": "pop", "at": 0.8, "anchor": [540, 980]}),
    ("answer", signal(540, 980, "r", "ryg", 0.9) + seal(840, 800, 95, "맨 위!", 46, RED, -8), {"type": "stamp", "at": 3.6, "anchor": [840, 800]}),
    ("why", note("색 대신 위치로도 알 수 있게", 540, 1330, 42), {"type": "fade", "at": 6.6}),
])

# S12 마무리 + 구독 ---------------------------------------------------------------------------------------------
finger = (f'<path d="M700 1145 V1250 C700 1280 740 1300 770 1300 H820 C850 1300 870 1270 870 1240 V1200 C870 1185 845 1180 835 1195 '
          f'C835 1175 810 1170 800 1188 C800 1170 775 1165 765 1185 V1145 C765 1120 700 1120 700 1145 Z" fill="#d9b48f" stroke="{INK}" stroke-width="6"/>')
scene("S12", 80, 90, [
    ai(10, (110, 100), (0, 0)),
    ("bg", bg(), {"type": "none"}),
    ("look", head("다음 신호등에선", 540, 430, 96) + head("색과 위치를 보세요", 540, 560, 96, RED) + rule(610), {"type": "pop", "at": 0.2, "anchor": [540, 500]}),
    ("sig", signal(540, 830, "g", "ryg", 0.7, False), {"type": "pop", "at": 0.6, "anchor": [540, 830]}),
    ("button", ribbon("구독하기", 540, 1080, 80), {"type": "pop", "at": 4.8, "anchor": [540, 1080]}),
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
