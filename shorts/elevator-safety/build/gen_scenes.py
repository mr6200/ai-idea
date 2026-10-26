"""Generate SVG parts for all 12 scenes of the elevator-safety Short (1080x1920).

Style (episode 11): vintage poster mixed with AI engraving backgrounds. Each scene's bg layer is
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
LABEL = "지식 쇼츠 · 엘리베이터"

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
    b = (f'<defs><linearGradient id="top" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{PAPER}" stop-opacity="0.6"/>'
         f'<stop offset="1" stop-color="{PAPER}" stop-opacity="0"/></linearGradient></defs>'
         f'<rect x="0" y="0" width="{W}" height="{H}" fill="{PAPER}" fill-opacity="0.62"/>'
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


def car(cx, cy, w=300, h=340):
    """Engraved elevator car: hatched cabin, mustard roof, folding gate."""
    x, y = cx - w / 2, cy - h / 2
    return (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{PAPER}" stroke="{INK}" stroke-width="7"/>'
            + hatch(x + 8, y + 12, w - 16, h - 24, 24, 2)
            + f'<path d="M{x} {y} L{cx} {y - 60} L{x + w} {y} Z" fill="{MUST}" stroke="{INK}" stroke-width="6" stroke-linejoin="round"/>'
            + f'<path d="M{x + 30} {y + h - 40} H{x + w - 30}" stroke="{INK}" stroke-width="5"/>')


def rails(cx, top, bottom, gap=420, teeth=True):
    out = ""
    for sx in (-1, 1):
        x = cx + sx * gap / 2
        out += f'<rect x="{x - 9}" y="{top}" width="18" height="{bottom - top}" fill="{BROWN}" stroke="{INK}" stroke-width="4"/>'
        if teeth:
            out += "".join(f'<path d="M{x - sx * 9} {yy} l{-sx * 16} 12 l{sx * 16} 12" fill="{PAPER}" stroke="{INK}" stroke-width="3" stroke-linejoin="round"/>'
                           for yy in range(int(top) + 6, int(bottom) - 24, 26))
    return out


def cable(cx, y1, y2, sw=8):
    return f'<path d="M{cx} {y1} V{y2}" stroke="{INK}" stroke-width="{sw}"/>'


def snap(cx, cy):
    """Frayed cable ends with red spark lines."""
    return (f'<path d="M{cx} {cy - 30} l-14 18 l22 6 l-12 14" fill="none" stroke="{INK}" stroke-width="5"/>'
            f'<path d="M{cx} {cy + 40} l12 -14 l-20 -6 l10 -12" fill="none" stroke="{INK}" stroke-width="5"/>'
            + "".join(f'<path d="M{cx + 34 * math.cos(math.radians(a)):.0f} {cy + 5 + 34 * math.sin(math.radians(a)):.0f} '
                      f'L{cx + 80 * math.cos(math.radians(a)):.0f} {cy + 5 + 80 * math.sin(math.radians(a)):.0f}" stroke="{RED}" stroke-width="6"/>'
                      for a in range(0, 360, 30)))


def gentleman(cx, by, s=1.0, hand_up=False):
    """Ink silhouette of a man in a top hat and frock coat (feet at by)."""
    p = lambda x, y: f"{cx + x * s:.0f} {by + y * s:.0f}"
    arm = f'<path d="M{p(36, -250)} L{p(60, -150)}" stroke="{INK}" stroke-width="{22 * s:.0f}" stroke-linecap="round"/>'
    if hand_up:  # the other (left) arm raised
        arm += f'<path d="M{p(-30, -250)} L{p(-90, -330)} L{p(-100, -380)}" fill="none" stroke="{INK}" stroke-width="{22 * s:.0f}" stroke-linecap="round"/>'
    return (f'<path d="M{p(-50, -280)} L{p(50, -280)} L{p(70, -110)} L{p(30, -110)} L{p(25, 0)} L{p(5, 0)} L{p(0, -100)} L{p(-5, 0)} L{p(-25, 0)} L{p(-30, -110)} L{p(-70, -110)} Z" fill="{INK}"/>'
            f'<circle cx="{cx}" cy="{by - 320 * s:.0f}" r="{38 * s:.0f}" fill="#d9b48f" stroke="{INK}" stroke-width="{5 * s:.0f}"/>'
            f'<rect x="{cx - 36 * s:.0f}" y="{by - 430 * s:.0f}" width="{72 * s:.0f}" height="{80 * s:.0f}" fill="{INK}"/>'
            f'<rect x="{cx - 56 * s:.0f}" y="{by - 356 * s:.0f}" width="{112 * s:.0f}" height="{12 * s:.0f}" fill="{INK}"/>' + arm)


def pawl_diagram(cx, cy, tense):
    """Otis safety: toothed rails, a spring on top of the platform frame and two pawls."""
    out = rails(cx, cy - 260, cy + 260, 320)
    out += f'<rect x="{cx - 130}" y="{cy - 40}" width="260" height="70" fill="{PAPER}" stroke="{INK}" stroke-width="6"/>'
    if tense:
        out += cable(cx, cy - 260, cy - 120) + f'<path d="M{cx} {cy - 120} l-40 10 l80 14 l-80 14 l80 14 l-40 10 V{cy - 40}" fill="none" stroke="{INK}" stroke-width="5"/>'
        out += f'<path d="M{cx - 120} {cy - 40} L{cx - 100} {cy - 110} M{cx + 120} {cy - 40} L{cx + 100} {cy - 110}" stroke="{MUST}" stroke-width="16" stroke-linecap="round"/>'
    else:
        out += cable(cx, cy - 260, cy - 200) + f'<path d="M{cx} {cy - 200} q-30 30 10 50 q30 10 -10 40" fill="none" stroke="{INK}" stroke-width="7"/>'
        out += f'<path d="M{cx} {cy - 100} l-40 20 l80 20 l-80 20 V{cy - 40}" fill="none" stroke="{INK}" stroke-width="5"/>'
        out += f'<path d="M{cx - 110} {cy - 40} L{cx - 160} {cy - 30} M{cx + 110} {cy - 40} L{cx + 160} {cy - 30}" stroke="{RED}" stroke-width="16" stroke-linecap="round"/>'
    return out


def skyline(base=1240):
    out = ""
    for i, (x, w, h) in enumerate([(120, 120, 380), (250, 90, 520), (350, 140, 640), (500, 100, 460), (610, 150, 700), (770, 110, 540), (890, 80, 420)]):
        out += f'<rect x="{x}" y="{base - h}" width="{w}" height="{h}" fill="{PAPER}" stroke="{INK}" stroke-width="5"/>'
        out += "".join(f'<rect x="{x + 14 + c * 26}" y="{yy}" width="12" height="18" fill="{INK}" fill-opacity="0.75"/>'
                       for yy in range(base - h + 24, base - 20, 44) for c in range((w - 20) // 26))
    return out + f'<path d="M80 {base} H1000" stroke="{INK}" stroke-width="6"/>'


def sheave(cx, cy, r=110):
    return (f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{PAPER}" stroke="{INK}" stroke-width="7"/>'
            f'<circle cx="{cx}" cy="{cy}" r="{r - 26}" fill="none" stroke="{INK}" stroke-width="3"/>'
            f'<circle cx="{cx}" cy="{cy}" r="16" fill="{INK}"/>'
            + "".join(f'<path d="M{cx} {cy} L{cx + (r - 26) * math.cos(math.radians(a)):.0f} {cy + (r - 26) * math.sin(math.radians(a)):.0f}" stroke="{INK}" stroke-width="4"/>' for a in range(0, 360, 60)))


def wedge_gear(cx, cy, clamped):
    """Safety gear at a rail: two wedges either side of the rail."""
    out = f'<rect x="{cx - 14}" y="{cy - 300}" width="28" height="600" fill="{BROWN}" stroke="{INK}" stroke-width="5"/>'
    out += f'<rect x="{cx - 170}" y="{cy - 120}" width="340" height="240" fill="{PAPER}" fill-opacity="0.9" stroke="{INK}" stroke-width="6"/>'
    gap = 16 if clamped else 46
    col = RED if clamped else MUST
    for sx in (-1, 1):
        xi = cx + sx * (14 + gap)
        xo = cx + sx * (14 + gap + 60)
        dy = -40 if clamped else 0
        out += (f'<path d="M{xi} {cy - 80 + dy} L{xi} {cy + 80 + dy} L{xo} {cy + 80 + dy} L{xo + sx * 20} {cy - 80 + dy} Z" '
                f'fill="{col}" stroke="{INK}" stroke-width="5" stroke-linejoin="round"/>')
    return out


def building(cx, base, h=900):
    """Empire State Building silhouette in ink with window hatching."""
    out = (f'<path d="M{cx - 150} {base} V{base - h * 0.55} H{cx - 110} V{base - h * 0.72} H{cx - 70} V{base - h * 0.86} H{cx - 30} V{base - h * 0.95} '
           f'H{cx - 8} V{base - h} H{cx + 8} V{base - h * 0.95} H{cx + 30} V{base - h * 0.86} H{cx + 70} V{base - h * 0.72} H{cx + 110} V{base - h * 0.55} H{cx + 150} V{base} Z" '
           f'fill="{PAPER}" stroke="{INK}" stroke-width="6" stroke-linejoin="round"/>')
    return out + hatch(cx - 140, base - h * 0.55, 280, h * 0.55, 20, 2) + hatch(cx - 60, base - h * 0.86, 120, h * 0.31, 16, 2)


def bomber(cx, cy, s=1.0):
    p = lambda x, y: f"{cx + x * s:.0f} {cy + y * s:.0f}"
    return (f'<path d="M{p(-110, 0)} L{p(110, -6)} L{p(130, 4)} L{p(-100, 14)} Z M{p(-20, 0)} L{p(-60, -90)} L{p(-30, -90)} L{p(30, 0)} Z '
            f'M{p(-20, 10)} L{p(-60, 90)} L{p(-30, 90)} L{p(30, 10)} Z M{p(-100, 4)} L{p(-130, -40)} L{p(-110, -40)} L{p(-80, 4)} Z" fill="{INK}"/>')


def figure(cx, by, jump=False):
    """Small stick figure for the quiz (feet at by)."""
    dy = -60 if jump else 0
    y = by + dy
    legs = (f'M{cx} {y - 70} L{cx - 30} {y - 20} L{cx - 10} {y} M{cx} {y - 70} L{cx + 30} {y - 20} L{cx + 10} {y}' if jump
            else f'M{cx} {y - 70} L{cx - 20} {y} M{cx} {y - 70} L{cx + 20} {y}')
    return (f'<circle cx="{cx}" cy="{y - 165}" r="28" fill="{PAPER}" stroke="{INK}" stroke-width="6"/>'
            f'<path d="M{cx} {y - 137} V{y - 70} {legs} M{cx - 50} {y - 150} L{cx} {y - 115} L{cx + 50} {y - 150}" fill="none" stroke="{INK}" stroke-width="8" stroke-linecap="round" stroke-linejoin="round"/>')


# ---------------------------------------------------------------- scenes
scenes = []


def scene(sid, start, end, parts):
    scenes.append({"id": sid, "start": start, "end": end, "parts": parts})


# S01 줄이 끊어지면? -------------------------------------------------------------------------
scene("S01", 0, 5, [
    ("bg", bg(burst=(540, 980)), {"type": "none"}),
    ("title", head("엘리베이터 줄이", 540, 400, 92) + head("끊어지면?", 540, 530, 130, RED) + rule(580),
     {"type": "pop", "at": 0.0, "anchor": [540, 470]}),
    ("shaft", rails(540, 640, 1300, 420, False) + cable(540, 640, 740) + cable(540, 820, 880) + car(540, 1060), {"type": "fade", "at": 0.2}),
    ("snap", snap(540, 775), {"type": "stamp", "at": 0.8, "anchor": [540, 780]}),
    ("seal", seal(850, 760, 95, "추락?"), {"type": "stamp", "at": 1.6, "anchor": [850, 760]}),
    ("answer", note("거의 안 떨어져요", 540, 1290, 52, RED), {"type": "pop", "at": 2.8, "anchor": [540, 1290]}),
])

# S02 1854 뉴욕 박람회 ---------------------------------------------------------------------------
scene("S02", 5, 12, [
    ("bg", bg(), {"type": "none"}),
    ("title", head("1854년 뉴욕", 540, 410, 100) + text("세계 박람회 · 크리스털 팰리스", 540, 500, 44, BROWN) + rule(550),
     {"type": "pop", "at": 0.0, "anchor": [540, 450]}),
    ("platform", rails(540, 640, 1280, 420) + cable(540, 640, 820)
     + f'<rect x="350" y="1180" width="380" height="40" fill="{MUST}" stroke="{INK}" stroke-width="6"/>'
     + f'<path d="M350 1180 V820 H730 V1180" fill="none" stroke="{INK}" stroke-width="6"/>', {"type": "fade", "at": 0.3}),
    ("otis", gentleman(540, 1175, 0.9), {"type": "slideU", "at": 0.8}),
    ("name", note("엘리샤 오티스", 820, 760, 44), {"type": "pop", "at": 1.6, "anchor": [820, 760]}),
    ("cut", f'<path d="M513 950 L459 878 L450 833" fill="none" stroke="{INK}" stroke-width="20" stroke-linecap="round"/>'
     + note("줄을 끊으시오!", 280, 760, 46, RED), {"type": "stamp", "at": 3.6, "anchor": [400, 800]}),
])

# S03 멈췄다! 모두 안전합니다 ---------------------------------------------------------------------------
scene("S03", 12, 19, [
    ("bg", bg(burst=(540, 960)), {"type": "none"}),
    ("title", head("몇 센티 만에", 540, 410, 96) + head("멈췄어요", 540, 530, 110, RED) + rule(580), {"type": "pop", "at": 0.0, "anchor": [540, 470]}),
    ("platform", rails(540, 640, 1280, 420) + cable(540, 640, 700) + snap(540, 735)
     + f'<rect x="350" y="1200" width="380" height="40" fill="{MUST}" stroke="{INK}" stroke-width="6"/>'
     + f'<path d="M350 1200 V840 H730 V1200" fill="none" stroke="{INK}" stroke-width="6"/>' + gentleman(540, 1195, 0.85, True),
     {"type": "drop", "at": 0.3}),
    ("stop", f'<path d="M330 1215 l-30 0 M750 1215 l30 0" stroke="{RED}" stroke-width="14" stroke-linecap="round"/>'
     + seal(860, 1040, 90, "정지!", 50, RED, -8), {"type": "stamp", "at": 1.6, "anchor": [860, 1040]}),
    ("safe", ribbon("모두 안전합니다!", 540, 1310, 52), {"type": "stamp", "at": 3.6, "anchor": [540, 1310]}),
])

# S04 톱니 레일과 걸쇠 ---------------------------------------------------------------------------
scene("S04", 19, 26, [
    ("bg", bg(), {"type": "none"}),
    ("title", head("비밀은 톱니 레일", 540, 430, 96) + rule(480), {"type": "pop", "at": 0.0, "anchor": [540, 410]}),
    ("tense", pawl_diagram(300, 860, True) + text("줄이 팽팽 → 걸쇠 접힘", 300, 1180, 38, INK, "middle", 800), {"type": "slideL", "at": 0.4}),
    ("slack", pawl_diagram(780, 860, False) + text("줄이 느슨 → 걸쇠 철컥", 780, 1180, 38, RED, "middle", 800), {"type": "slideR", "at": 3.4}),
    ("click", seal(780, 640, 70, "철컥", 40, RED, 8), {"type": "stamp", "at": 4.4, "anchor": [780, 640]}),
])

# S05 높은 빌딩 ---------------------------------------------------------------------------------
scene("S05", 26, 33, [
    ("bg", bg(), {"type": "none"}),
    ("title", head("안심하고 탔더니", 540, 410, 96) + rule(460), {"type": "pop", "at": 0.0, "anchor": [540, 400]}),
    ("city", skyline(1240), {"type": "wipeU", "at": 0.4, "dur": 1.6}),
    ("up", arrow(960, 1180, 960, 620, RED, 10) + text("하늘로!", 960, 590, 46, RED, "middle", 800), {"type": "pop", "at": 3.4, "anchor": [960, 900]}),
    ("note", note("높은 빌딩이 가능해졌어요", 540, 1320, 46), {"type": "pop", "at": 4.0, "anchor": [540, 1320]}),
])

# S06 줄은 여러 가닥 ------------------------------------------------------------------------------
ropes = "".join(cable(420 + i * 48, 760, 1080, 7) for i in range(6))
scene("S06", 33, 41, [
    ("bg", bg(), {"type": "none"}),
    ("title", head("요즘 줄은", 540, 410, 96) + head("한 가닥이 아니에요", 540, 520, 88, RED) + rule(570), {"type": "pop", "at": 0.0, "anchor": [540, 460]}),
    ("rig", sheave(540, 720, 150) + ropes + car(540, 1180, 360, 220), {"type": "fade", "at": 0.3}),
    ("count", note("보통 4~8가닥", 860, 900, 44), {"type": "pop", "at": 3.8, "anchor": [860, 900]}),
    ("broken", f'<path d="M450 880 l50 50 M500 880 l-50 50" stroke="{RED}" stroke-width="12" stroke-linecap="round"/>'
     + note("하나가 끊겨도 버텨요", 300, 1330, 40), {"type": "stamp", "at": 5.0, "anchor": [475, 905]}),
])

# S07 조속기 ---------------------------------------------------------------------------------------
gov = (sheave(540, 800, 140) + f'<circle cx="490" cy="760" r="26" fill="{MUST}" stroke="{INK}" stroke-width="5"/><circle cx="590" cy="760" r="26" fill="{MUST}" stroke="{INK}" stroke-width="5"/>'
       + f'<path d="M400 800 V1260 M680 800 V1260" stroke="{INK}" stroke-width="6"/>' + text("조속기", 540, 1010, 56, INK, "middle", 800))
spin = "".join(f'<path d="M{540 + 190 * math.cos(math.radians(a)):.0f} {800 + 190 * math.sin(math.radians(a)):.0f} A190 190 0 0 1 {540 + 190 * math.cos(math.radians(a + 40)):.0f} {800 + 190 * math.sin(math.radians(a + 40)):.0f}" '
               f'fill="none" stroke="{RED}" stroke-width="7" stroke-linecap="round"/>' for a in (200, 320))
scene("S07", 41, 48, [
    ("bg", bg(), {"type": "none"}),
    ("title", head("너무 빠르면?", 540, 430, 100) + rule(480), {"type": "pop", "at": 0.0, "anchor": [540, 410]}),
    ("gov", gov, {"type": "pop", "at": 0.4, "anchor": [540, 900]}),
    ("spin", spin + seal(870, 680, 80, "과속!", 44, RED, 8), {"type": "stamp", "at": 2.0, "anchor": [870, 680]}),
    ("pull", arrow(400, 1100, 400, 1260, RED, 10) + note("비상 브레이크를 당겨요", 640, 1320, 42), {"type": "slideU", "at": 3.6}),
])

# S08 쐐기가 레일을 꽉 ---------------------------------------------------------------------------------
scene("S08", 48, 55, [
    ("bg", bg(), {"type": "none"}),
    ("title", head("쐐기가 레일을 꽉!", 540, 430, 92) + rule(480), {"type": "pop", "at": 0.0, "anchor": [540, 410]}),
    ("open", wedge_gear(300, 900, False) + text("평소", 300, 1240, 46, INK, "middle", 800), {"type": "slideL", "at": 0.3}),
    ("shut", wedge_gear(780, 900, True) + text("비상 정지", 780, 1240, 46, RED, "middle", 800), {"type": "slideR", "at": 1.6}),
    ("squeeze", arrow(640, 900, 700, 900, RED, 8) + arrow(920, 900, 860, 900, RED, 8), {"type": "pop", "at": 2.4, "anchor": [780, 900]}),
    ("modern", ribbon("오티스 걸쇠의 현대판", 540, 1320, 46), {"type": "stamp", "at": 3.6, "anchor": [540, 1320]}),
])

# S09 완충기 + 겹겹이 -------------------------------------------------------------------------------
spring = f'<path d="M420 1140 ' + " ".join(f"l{120 if k % 2 == 0 else -120} 22" for k in range(8)) + f'" fill="none" stroke="{INK}" stroke-width="8"/>'
layers = "".join(note(s, 760, 690 + i * 130, 40, RED if i == 3 else INK) for i, s in enumerate(("① 여러 가닥 줄", "② 조속기", "③ 비상정지장치", "④ 완충기")))
scene("S09", 55, 62, [
    ("bg", bg(), {"type": "none"}),
    ("title", head("맨 아래엔 완충기", 540, 430, 96) + rule(480), {"type": "pop", "at": 0.0, "anchor": [540, 410]}),
    ("pit", f'<rect x="300" y="1000" width="200" height="60" fill="{MUST}" stroke="{INK}" stroke-width="6"/>' + spring
     + f'<path d="M240 1320 H560" stroke="{INK}" stroke-width="8"/>' + hatch(250, 1325, 300, 30, 12, 2)
     + car(400, 820, 220, 220) + text("완충기", 200, 1240, 40, INK, "middle", 800), {"type": "pop", "at": 0.3, "anchor": [400, 1100]}),
    ("layers", layers, {"type": "slideR", "at": 3.4}),
])

# S10 1945 엠파이어 스테이트 ---------------------------------------------------------------------------
scene("S10", 62, 70, [
    ("bg", bg(), {"type": "none"}),
    ("title", head("1945년 뉴욕", 540, 430, 100) + rule(480), {"type": "pop", "at": 0.0, "anchor": [540, 410]}),
    ("bld", building(420, 1300, 760), {"type": "wipeU", "at": 0.3, "dur": 1.2}),
    ("plane", bomber(780, 760, 1.2) + f'<path d="M560 860 l30 -20 l10 30 l30 -20" fill="none" stroke="{RED}" stroke-width="6"/>', {"type": "slideL", "at": 1.0}),
    ("fall", f'<path d="M800 700 V1180 M780 700 H820 M780 1180 H820" stroke="{INK}" stroke-width="4"/>' + text("75층", 830, 960, 52, RED, "start", 800),
     {"type": "wipeD", "at": 3.8, "dur": 1.0}),
    ("alive", seal(780, 1250, 85, "생존!", 46, RED, -6), {"type": "stamp", "at": 6.0, "anchor": [780, 1250]}),
])

# S11 퀴즈: 점프하면 살까? ------------------------------------------------------------------------------
scene("S11", 70, 80, [
    ("bg", bg(burst=(540, 980)), {"type": "none"}),
    ("badge", ribbon("퀴즈", 540, 360, 56), {"type": "pop", "at": 0.0, "anchor": [540, 360]}),
    ("question", head("떨어지는 엘리베이터,", 540, 500, 76) + head("점프하면 살까?", 540, 600, 92, RED), {"type": "pop", "at": 0.3, "anchor": [540, 550]}),
    ("cab", f'<rect x="340" y="700" width="400" height="520" fill="{PAPER}" fill-opacity="0.9" stroke="{INK}" stroke-width="8"/>'
     + figure(540, 1200, True) + arrow(540, 900, 540, 830, INK, 6) + arrow(860, 760, 860, 1160, RED, 10),
     {"type": "pop", "at": 0.8, "anchor": [540, 960]}),
    ("answer", seal(820, 1180, 100, "X", 90, RED, -8), {"type": "stamp", "at": 3.6, "anchor": [820, 1180]}),
    ("why", note("점프는 너무 약해요", 540, 1320, 44), {"type": "fade", "at": 6.6}),
])

# S12 걱정 그만 + 구독 ----------------------------------------------------------------------------
button = ribbon("구독하기", 540, 1080, 80)
finger = (f'<path d="M700 1145 V1250 C700 1280 740 1300 770 1300 H820 C850 1300 870 1270 870 1240 V1200 C870 1185 845 1180 835 1195 '
          f'C835 1175 810 1170 800 1188 C800 1170 775 1165 765 1185 V1145 C765 1120 700 1120 700 1145 Z" fill="#d9b48f" stroke="{INK}" stroke-width="6"/>')
scene("S12", 80, 90, [
    ("bg", bg(), {"type": "none"}),
    ("look", head("엘리베이터 줄 걱정은", 540, 430, 84) + head("이제 그만!", 540, 550, 110, RED) + rule(600), {"type": "pop", "at": 0.2, "anchor": [540, 490]}),
    ("car", rails(540, 650, 960, 300, False) + cable(540, 650, 720) + car(540, 850, 220, 220), {"type": "pop", "at": 0.6, "anchor": [540, 820]}),
    ("button", button, {"type": "pop", "at": 4.8, "anchor": [540, 1080]}),
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
