"""Generate SVG parts for all 12 scenes of the ear-pressure Short (1080x1920).

Style (from episode 9 on): blueprint + pop art. Navy grid paper with white line drawings and
cyan dimension notes, mixed with pop accents: thick black outlines, yellow/red bursts, speech
bubbles and halftone dots. Fonts: Black Han Sans for headlines, Jua for pop exclamations,
Do Hyeon for notes and subtitles (shorts/fonts/).

Each scene is a list of parts; each part becomes its own full-frame SVG so the exported PNG
layers line up in EffectCraft. A manifest records the timing and animation hints.
"""
import json
import math
import os

W, H = 1080, 1920
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "svg")
LABEL = "지식 쇼츠 · 귀가 먹먹한 이유"

# fonts
HEAD, POP, NOTE = "Black Han Sans", "Jua", "Do Hyeon"
FONT = NOTE  # subtitles

# palette
NAVY, NAVY_D = "#0f4c8a", "#0b3866"
LINE, CYAN = "#e8f4ff", "#7fd3ff"
YELLOW, RED, INK, WHITE = "#ffd400", "#e63946", "#111111", "#ffffff"
SKY = "#4cc9f0"


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


def text(s, x, y, size, fill=WHITE, anchor="middle", font=NOTE, extra=""):
    assert text_width(s, size) < 1000, f"text too wide: {s}"
    s = s.replace("&", "&amp;").replace("<", "&lt;")
    return (f'<text x="{x}" y="{y}" font-family="{font}" font-size="{size}" '
            f'fill="{fill}" text-anchor="{anchor}" {extra}>{s}</text>')


def head(s, x, y, size, fill=WHITE, anchor="middle", stroke=12):
    """Pop headline: Black Han Sans with a thick black outline."""
    return text(s, x, y, size, fill, anchor, HEAD, f'stroke="{INK}" stroke-width="{stroke}" paint-order="stroke" stroke-linejoin="round"')


def popword(s, x, y, size, fill=YELLOW, stroke=10, rotate=0):
    body = text(s, x, y, size, fill, "middle", POP, f'stroke="{INK}" stroke-width="{stroke}" paint-order="stroke" stroke-linejoin="round"')
    return f'<g transform="rotate({rotate} {x} {y})">{body}</g>' if rotate else body


def pill(s, cx, cy, size, bg, fg=INK, pad=36, font=POP):
    w = text_width(s, size) + pad * 2
    h = size * 1.6
    return (f'<rect x="{cx - w / 2 + 6:.1f}" y="{cy - h / 2 + 8:.1f}" width="{w:.1f}" height="{h:.1f}" rx="{h / 2:.1f}" fill="{INK}"/>'
            f'<rect x="{cx - w / 2:.1f}" y="{cy - h / 2:.1f}" width="{w:.1f}" height="{h:.1f}" rx="{h / 2:.1f}" fill="{bg}" stroke="{INK}" stroke-width="6"/>'
            + text(s, cx, cy + size * 0.36, size, fg, "middle", font))


def panel(x, y, w, h, fill=WHITE, rx=24):
    """Pop comic box: black offset shadow + thick outline."""
    return (f'<rect x="{x + 10}" y="{y + 12}" width="{w}" height="{h}" rx="{rx}" fill="{INK}"/>'
            f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{fill}" stroke="{INK}" stroke-width="8"/>')


def svg(body):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">'
            f'<rect x="0" y="0" width="{W}" height="{H}" fill="#000000" fill-opacity="0"/>{body}</svg>')


def grid():
    out = "".join(f'<path d="M{x} 0 V{H}" stroke="{LINE}" stroke-opacity="{0.26 if x % 200 == 0 else 0.09}" stroke-width="2"/>'
                  for x in range(0, W + 1, 40))
    return out + "".join(f'<path d="M0 {y} H{W}" stroke="{LINE}" stroke-opacity="{0.26 if y % 200 == 0 else 0.09}" stroke-width="2"/>'
                         for y in range(0, H + 1, 40))


def rays(cx, cy, color="#2f86dc", opacity=0.45, step=15):
    return "".join(f'<path d="M{cx} {cy} L{cx + 2200 * math.cos(math.radians(a)):.0f} {cy + 2200 * math.sin(math.radians(a)):.0f} '
                   f'L{cx + 2200 * math.cos(math.radians(a + step / 2)):.0f} {cy + 2200 * math.sin(math.radians(a + step / 2)):.0f} Z" '
                   f'fill="{color}" fill-opacity="{opacity}"/>' for a in range(0, 360, step))


def dots(x0, y0, x1, y1, color=CYAN, opacity=0.35):
    return "".join(f'<circle cx="{x}" cy="{y}" r="{max(2, 9 - ((x - x0) + (y - y0)) // 70)}" fill="{color}" fill-opacity="{opacity}"/>'
                   for x in range(x0, x1, 34) for y in range(y0, y1, 34) if (x - x0) + (y - y0) < 560)


def bg(extra="", burst=None):
    """Blueprint paper + corner halftone + optional sunburst and the label pill (no title block from episode 10)."""
    b = f'<rect x="0" y="0" width="{W}" height="{H}" fill="{NAVY}"/>'
    if burst:
        b += rays(*burst)
    b += grid() + dots(0, 0, 560, 560) + dots(560, 1360, 1080, 1920)
    b += pill(LABEL, 540, 200, 36, YELLOW)
    return b + extra


def burst_star(cx, cy, r, word, fill=RED, word_fill=YELLOW, size=60, points=12):
    pts = " L".join(f"{cx + (r if i % 2 == 0 else r * 0.62) * math.cos(math.pi * i / points):.1f} "
                    f"{cy + (r if i % 2 == 0 else r * 0.62) * math.sin(math.pi * i / points):.1f}" for i in range(points * 2))
    return f'<path d="M{pts} Z" fill="{fill}" stroke="{INK}" stroke-width="8" stroke-linejoin="round"/>' + popword(word, cx, cy + size * 0.36, size, word_fill, 8)


def bubble(cx, cy, w, h, s, size=56, tail=(-1, 1)):
    tx, ty = cx + tail[0] * w * 0.25, cy + h / 2
    return (f'<rect x="{cx - w / 2}" y="{cy - h / 2}" width="{w}" height="{h}" rx="{h / 2}" fill="{WHITE}" stroke="{INK}" stroke-width="8"/>'
            f'<path d="M{tx - 30} {ty - 6} L{tx + tail[0] * 40} {ty + 70} L{tx + 30} {ty - 6} Z" fill="{WHITE}" stroke="{INK}" stroke-width="8" stroke-linejoin="round"/>'
            f'<rect x="{tx - 26}" y="{ty - 16}" width="52" height="14" fill="{WHITE}"/>'
            + text(s, cx, cy + size * 0.36, size, INK, "middle", POP))


def dim(x1, x2, y, label, color=CYAN):
    return (f'<path d="M{x1} {y} H{x2} M{x1} {y - 16} V{y + 16} M{x2} {y - 16} V{y + 16}" stroke="{color}" stroke-width="3"/>'
            + text(label, (x1 + x2) / 2, y - 18, 34, color))


def arrow(x1, y1, x2, y2, color=LINE, w=6):
    ang = math.atan2(y2 - y1, x2 - x1)
    a1 = (x2 - 24 * math.cos(ang - 0.45), y2 - 24 * math.sin(ang - 0.45))
    a2 = (x2 - 24 * math.cos(ang + 0.45), y2 - 24 * math.sin(ang + 0.45))
    return (f'<path d="M{x1} {y1} L{x2} {y2} M{a1[0]:.1f} {a1[1]:.1f} L{x2} {y2} L{a2[0]:.1f} {a2[1]:.1f}" '
            f'fill="none" stroke="{color}" stroke-width="{w}" stroke-linecap="round" stroke-linejoin="round"/>')


SKIN = "#f6d2b3"


def ear_icon(cx, cy, s=1.0):
    """Pop-art outer ear (skin fill, thick black outline)."""
    p = lambda x, y: f"{cx + x * s:.0f} {cy + y * s:.0f}"
    return (f'<path d="M{p(-90, -40)} C{p(-100, -230)} {p(160, -250)} {p(150, -40)} C{p(145, 70)} {p(40, 80)} {p(40, 170)} '
            f'C{p(40, 250)} {p(-70, 260)} {p(-90, 170)} C{p(-110, 120)} {p(-100, 40)} {p(-90, -40)} Z" fill="{SKIN}" stroke="{INK}" stroke-width="{10 * s:.0f}" stroke-linecap="round" stroke-linejoin="round"/>'
            f'<path d="M{p(-30, -40)} C{p(-30, -140)} {p(90, -150)} {p(85, -40)} C{p(80, 20)} {p(10, 30)} {p(0, 90)}" fill="none" stroke="{INK}" stroke-width="{8 * s:.0f}" stroke-linecap="round"/>')


def ear(cy, drum=0, tube_open=False, tube_hi=False, labels=True):
    """Blueprint cross-section: ear canal -> eardrum -> middle ear -> Eustachian tube.
    drum: 0 flat, +1 pushed inward (to the right), -1 bulged outward."""
    out = (f'<path d="M110 {cy - 60} H450 M110 {cy + 60} H450" stroke="{LINE}" stroke-width="8" stroke-linecap="round"/>'
           f'<path d="M110 {cy - 60} C60 {cy - 120} 60 {cy - 220} 140 {cy - 240} M110 {cy + 60} C60 {cy + 120} 70 {cy + 220} 150 {cy + 240}" '
           f'fill="none" stroke="{LINE}" stroke-width="8" stroke-linecap="round"/>'
           f'<rect x="450" y="{cy - 170}" width="310" height="320" rx="60" fill="{SKY}" fill-opacity="0.18" stroke="{LINE}" stroke-width="8"/>')
    # eardrum
    out += (f'<path d="M450 {cy - 110} Q{450 + drum * 70} {cy} 450 {cy + 110}" fill="none" stroke="{YELLOW}" stroke-width="12" stroke-linecap="round"/>')
    # Eustachian tube from the bottom of the middle ear down to the back of the nose
    col = YELLOW if tube_hi else LINE
    if tube_open:
        out += (f'<path d="M680 {cy + 150} L860 {cy + 380} M730 {cy + 150} L900 {cy + 365}" stroke="{col}" stroke-width="8" stroke-linecap="round"/>'
                f'<rect x="684" y="{cy + 140}" width="42" height="16" fill="{NAVY}"/>')
    else:
        out += f'<path d="M705 {cy + 150} L880 {cy + 372}" stroke="{col}" stroke-width="10" stroke-linecap="round"/>'
    if labels:
        out += (text("바깥귀 통로", 280, cy - 80, 36, CYAN)
                + text("고막", 435, cy - 190, 44, YELLOW, "end", HEAD) + f'<path d="M420 {cy - 180} L448 {cy - 120}" stroke="{YELLOW}" stroke-width="4"/>'
                + text("중이", 610, cy - 10, 52, WHITE, "middle", HEAD) + text("공기 방", 610, cy + 50, 38, CYAN)
                + text("이관", 900, cy + 250, 52, col, "start", HEAD))
    return out


def air(x1, y1, x2, y2, color=CYAN):
    return arrow(x1, y1, x2, y2, color, 7)


def plane_icon(cx, cy, s=1.0, angle=0):
    body = (f'<path d="M-140 0 C-140 -26 -110 -34 -80 -34 H120 C150 -34 170 -14 170 0 C170 14 150 34 120 34 H-80 C-110 34 -140 26 -140 0 Z" '
            f'fill="{WHITE}" stroke="{INK}" stroke-width="8"/>'
            f'<path d="M-10 -20 L-70 -120 H-30 L60 -20 Z M-10 20 L-70 120 H-30 L60 20 Z M-120 -20 L-150 -80 H-120 L-80 -20 Z" fill="{YELLOW}" stroke="{INK}" stroke-width="7" stroke-linejoin="round"/>'
            + "".join(f'<circle cx="{x}" cy="-6" r="9" fill="{SKY}" stroke="{INK}" stroke-width="3"/>' for x in range(-50, 130, 34)))
    return f'<g transform="translate({cx} {cy}) rotate({angle}) scale({s})">{body}</g>'

# ---------------------------------------------------------------- scenes
scenes = []


def scene(sid, start, end, parts):
    scenes.append({"id": sid, "start": start, "end": end, "parts": parts})


# S01 귀가 먹먹? ---------------------------------------------------------------------------
scene("S01", 0, 5, [
    ("bg", bg(burst=(540, 960)), {"type": "none"}),
    ("title", head("비행기만 타면", 540, 410, 96) + head("귀가 먹먹?!", 540, 560, 124, YELLOW, stroke=14),
     {"type": "pop", "at": 0.0, "anchor": [540, 480]}),
    ("ear", ear_icon(540, 930, 1.5), {"type": "pop", "at": 0.3, "anchor": [540, 930]}),
    ("muffle", popword("웅~", 230, 820, 90, CYAN, 10, -12) + popword("먹먹", 860, 1060, 80, YELLOW, 10, 10),
     {"type": "stamp", "at": 1.0, "anchor": [540, 940]}),
    ("who", bubble(540, 1240, 560, 120, "범인은 귀 속 공기!", 52, (1, 1)), {"type": "pop", "at": 2.6, "anchor": [540, 1240]}),
])

# S02 귀 속 구조 ----------------------------------------------------------------------------
equal = (text("바깥 기압", 250, 1110, 42, WHITE, "middle", HEAD) + popword("=", 450, 1120, 80, YELLOW, 8)
         + text("안쪽 기압", 640, 1110, 42, WHITE, "middle", HEAD))
scene("S02", 5, 12, [
    ("bg", bg(), {"type": "none"}),
    ("title", head("귀 속을 보면", 540, 440, 96), {"type": "pop", "at": 0.0, "anchor": [540, 410]}),
    ("ear", ear(800), {"type": "pop", "at": 0.4, "anchor": [540, 800]}),
    ("equal", equal, {"type": "slideU", "at": 3.4}),
    ("same", pill("평소엔 안팎이 같아요", 540, 1290, 52, YELLOW), {"type": "stamp", "at": 4.0, "anchor": [540, 1290]}),
])

# S03 기내 기압 = 2,400m 산 위 -----------------------------------------------------------------
mountain = (f'<path d="M80 1180 L420 700 L560 880 L700 640 L1000 1180 Z" fill="{SKY}" fill-opacity="0.18" stroke="{LINE}" stroke-width="8" stroke-linejoin="round"/>'
            f'<path d="M640 725 L700 640 L760 725 L720 705 L700 730 L675 705 Z" fill="{WHITE}" stroke="{LINE}" stroke-width="4"/>'
            f'<path d="M900 1180 V640 M880 640 H920 M880 1180 H920" stroke="{CYAN}" stroke-width="4"/>'
            + text("2,400m", 930, 920, 46, CYAN, "start"))
scene("S03", 12, 19, [
    ("bg", bg(), {"type": "none"}),
    ("title", head("비행기 안 기압은", 540, 430, 92) + head("땅보다 낮아요", 540, 550, 96, YELLOW), {"type": "pop", "at": 0.0, "anchor": [540, 490]}),
    ("mountain", mountain, {"type": "wipeU", "at": 3.4, "dur": 0.8}),
    ("plane", plane_icon(560, 690, 0.9), {"type": "slideR", "at": 3.8}),
    ("same", pill("산 위와 비슷한 기압", 540, 1290, 52, WHITE), {"type": "stamp", "at": 4.8, "anchor": [540, 1290]}),
])

# S04 고막이 밀려 팽팽 ------------------------------------------------------------------------
push = "".join(air(170, y, 400, y, YELLOW) for y in (775, 825))
scene("S04", 19, 26, [
    ("bg", bg(), {"type": "none"}),
    ("title", head("기압이 바뀌면?", 540, 440, 96), {"type": "pop", "at": 0.0, "anchor": [540, 410]}),
    ("ear", ear(800, drum=1), {"type": "pop", "at": 0.4, "anchor": [540, 800]}),
    ("push", push, {"type": "slideR", "at": 2.4}),
    ("tight", burst_star(330, 1080, 120, "팽팽!", RED, YELLOW, 52), {"type": "stamp", "at": 3.6, "anchor": [330, 1080]}),
    ("muffle", pill("소리가 먹먹해져요", 540, 1290, 54, YELLOW), {"type": "stamp", "at": 4.6, "anchor": [540, 1290]}),
])

# S05 해결사 이관 -----------------------------------------------------------------------------
scene("S05", 26, 33, [
    ("bg", bg(), {"type": "none"}),
    ("title", head("해결사 등장!", 540, 440, 96, YELLOW), {"type": "pop", "at": 0.0, "anchor": [540, 410]}),
    ("ear", ear(780, tube_hi=True), {"type": "pop", "at": 0.3, "anchor": [540, 780]}),
    ("hi", f'<circle cx="790" cy="1045" r="150" fill="none" stroke="{RED}" stroke-width="8" stroke-dasharray="20 14"/>'
     + text("귀와 코 뒤를 잇는 통로", 400, 1150, 40, CYAN), {"type": "pop", "at": 1.6, "anchor": [790, 1045]}),
    ("closed", pill("평소엔 닫혀 있어요", 540, 1290, 52, WHITE), {"type": "stamp", "at": 3.6, "anchor": [540, 1290]}),
])

# S06 꿀꺽 → 이관 열림 → 뻥 -----------------------------------------------------------------------
flow = air(880, 1130, 730, 950) + air(710, 900, 710, 700)
scene("S06", 33, 41, [
    ("bg", bg(burst=(540, 860)), {"type": "none"}),
    ("words", popword("꿀꺽!", 300, 440, 110, YELLOW, 12, -8) + popword("하~암", 790, 470, 96, CYAN, 12, 8),
     {"type": "stamp", "at": 0.0, "anchor": [540, 450]}),
    ("ear", ear(780, tube_open=True, tube_hi=True), {"type": "pop", "at": 0.6, "anchor": [540, 780]}),
    ("flow", flow, {"type": "pop", "at": 2.4, "anchor": [720, 950]}),
    ("pop", burst_star(300, 1100, 130, "뻥!", RED, YELLOW, 80), {"type": "stamp", "at": 4.4, "anchor": [300, 1100]}),
])

# S07 이륙: 저절로 빠져나감 -------------------------------------------------------------------------
scene("S07", 41, 48, [
    ("bg", bg(), {"type": "none"}),
    ("title", head("올라갈 때", 540, 440, 100), {"type": "pop", "at": 0.0, "anchor": [540, 410]}),
    ("plane", plane_icon(860, 560, 0.55, -25), {"type": "slideU", "at": 0.3}),
    ("ear", ear(800, drum=-1, tube_open=True), {"type": "pop", "at": 0.5, "anchor": [540, 800]}),
    ("out", air(620, 900, 690, 1000) + air(730, 1010, 880, 1200), {"type": "pop", "at": 1.4, "anchor": [740, 1050]}),
    ("easy", pill("저절로 빠져나가요 · 쉬움", 540, 1290, 50, YELLOW), {"type": "stamp", "at": 3.6, "anchor": [540, 1290]}),
])

# S08 착륙: 잘 안 열려서 더 아픔 ----------------------------------------------------------------------
xmark = f'<path d="M760 1020 L860 1120 M860 1020 L760 1120" stroke="{RED}" stroke-width="16" stroke-linecap="round"/>'
scene("S08", 48, 55, [
    ("bg", bg(), {"type": "none"}),
    ("title", head("내려갈 때", 540, 440, 100, YELLOW), {"type": "pop", "at": 0.0, "anchor": [540, 410]}),
    ("plane", plane_icon(860, 560, 0.55, 25), {"type": "slideU", "at": 0.3}),
    ("ear", ear(800, drum=1), {"type": "pop", "at": 0.5, "anchor": [540, 800]}),
    ("need", air(940, 1230, 900, 1180) + text("공기가 들어가야 하는데", 380, 1080, 40, CYAN), {"type": "fade", "at": 1.2}),
    ("block", xmark, {"type": "stamp", "at": 3.4, "anchor": [810, 1070]}),
    ("ouch", burst_star(220, 1220, 110, "아야!", RED, YELLOW, 56), {"type": "stamp", "at": 4.2, "anchor": [220, 1220]}),
])

# S09 착륙 전 이렇게 ---------------------------------------------------------------------------------
cup = (f'<path d="M830 700 L845 820 H915 L930 700 Z" fill="{SKY}" stroke="{INK}" stroke-width="7" stroke-linejoin="round"/>')
gum = f'<rect x="260" y="1000" width="120" height="60" rx="14" fill="#ff8fab" stroke="{INK}" stroke-width="7"/>'
tips = (panel(90, 620, 430, 300) + popword("꿀꺽", 305, 760, 80, YELLOW, 10) + text("침 삼키기", 305, 860, 44, INK, "middle", POP)
        + panel(560, 620, 430, 300) + popword("하~암", 680, 770, 60, CYAN, 10) + cup + text("하품 · 물", 775, 890, 44, INK, "middle", POP)
        + panel(90, 960, 430, 260) + gum + text("껌 씹기", 305, 1150, 44, INK, "middle", POP)
        + panel(560, 960, 430, 260) + text("코 막고", 775, 1065, 46, INK, "middle", POP) + text("살살 콧바람", 775, 1140, 46, RED, "middle", POP))
scene("S09", 55, 62, [
    ("bg", bg(), {"type": "none"}),
    ("title", head("착륙 전엔 이렇게!", 540, 440, 92), {"type": "pop", "at": 0.0, "anchor": [540, 410]}),
    ("tips", tips, {"type": "pop", "at": 0.4, "anchor": [540, 920]}),
])

# S10 아기는 더 힘들다 -------------------------------------------------------------------------------
baby = (f'<circle cx="330" cy="830" r="150" fill="{SKIN}" stroke="{INK}" stroke-width="10"/>'
        f'<circle cx="280" cy="810" r="12" fill="{INK}"/><circle cx="380" cy="810" r="12" fill="{INK}"/>'
        f'<path d="M300 690 Q330 650 350 690" fill="none" stroke="{INK}" stroke-width="8" stroke-linecap="round"/>'
        f'<circle cx="230" cy="860" r="18" fill="#ff8fab" fill-opacity="0.7"/><circle cx="430" cy="860" r="18" fill="#ff8fab" fill-opacity="0.7"/>')
bottle = (f'<g transform="rotate(-35 470 900)"><rect x="430" y="880" width="90" height="170" rx="24" fill="{WHITE}" stroke="{INK}" stroke-width="8"/>'
          f'<path d="M445 880 Q475 820 505 880 Z" fill="#ffd8a8" stroke="{INK}" stroke-width="7"/>'
          f'<path d="M430 950 H520 M430 1000 H520" stroke="{SKY}" stroke-width="8"/></g>')
tubes = (text("이관 굵기", 800, 690, 40, CYAN)
         + f'<path d="M690 770 H910 M690 830 H910" stroke="{LINE}" stroke-width="6"/>' + text("어른", 800, 880, 40, WHITE, "middle", HEAD)
         + f'<path d="M720 960 H880 M720 985 H880" stroke="{YELLOW}" stroke-width="6"/>' + text("아기", 800, 1040, 40, YELLOW, "middle", HEAD)
         + text("좁아요", 800, 1090, 36, YELLOW))
scene("S10", 62, 70, [
    ("bg", bg(), {"type": "none"}),
    ("title", head("아기는 더 힘들어요", 540, 440, 88), {"type": "pop", "at": 0.0, "anchor": [540, 410]}),
    ("baby", baby, {"type": "pop", "at": 0.3, "anchor": [330, 830]}),
    ("tubes", tubes, {"type": "slideR", "at": 1.0}),
    ("bottle", bottle, {"type": "drop", "at": 3.8}),
    ("tip", pill("젖병 · 쪽쪽이로 꿀꺽", 540, 1290, 52, YELLOW), {"type": "stamp", "at": 4.4, "anchor": [540, 1290]}),
])

# S11 퀴즈: 잠들면 더 아플까? ---------------------------------------------------------------------------
o = (f'<circle cx="320" cy="920" r="140" fill="none" stroke="{WHITE}" stroke-width="26"/>')
x = (f'<path d="M660 800 L900 1040 M900 800 L660 1040" stroke="{WHITE}" stroke-width="26" stroke-linecap="round"/>')
scene("S11", 70, 80, [
    ("bg", bg(burst=(540, 920)), {"type": "none"}),
    ("badge", pill("퀴즈", 540, 380, 64, YELLOW), {"type": "pop", "at": 0.0, "anchor": [540, 380]}),
    ("question", head("착륙 때 잠들면", 540, 530, 84) + head("귀가 더 아플까?", 540, 640, 90, YELLOW), {"type": "pop", "at": 0.3, "anchor": [540, 590]}),
    ("ox", o + x, {"type": "pop", "at": 0.8, "anchor": [540, 920]}),
    ("answer", f'<circle cx="320" cy="920" r="170" fill="none" stroke="{RED}" stroke-width="14"/>' + burst_star(500, 1080, 100, "정답!", RED, YELLOW, 48),
     {"type": "stamp", "at": 3.6, "anchor": [320, 920]}),
    ("why", pill("자는 동안 침을 덜 삼켜요", 540, 1290, 48, WHITE), {"type": "fade", "at": 6.8}),
])

# S12 꿀꺽 삼키세요 + 구독 ----------------------------------------------------------------------------
button = (f'<rect x="300" y="1010" width="500" height="170" rx="85" fill="{INK}"/>'
          f'<rect x="290" y="1000" width="500" height="170" rx="85" fill="{RED}" stroke="{INK}" stroke-width="8"/>'
          + popword("구독", 560, 1118, 92, WHITE, 8)
          + f'<path d="M405 1035 C375 1035 368 1065 368 1090 L360 1120 H450 L442 1090 C442 1065 435 1035 405 1035 Z M392 1130 a13 13 0 0 0 26 0 Z" fill="{WHITE}" stroke="{INK}" stroke-width="4"/>')
finger = (f'<path d="M700 1145 V1250 C700 1280 740 1300 770 1300 H820 C850 1300 870 1270 870 1240 V1200 C870 1185 845 1180 835 1195 '
          f'C835 1175 810 1170 800 1188 C800 1170 775 1165 765 1185 V1145 C765 1120 700 1120 700 1145 Z" fill="{SKIN}" stroke="{INK}" stroke-width="6"/>')
scene("S12", 80, 90, [
    ("bg", bg(), {"type": "none"}),
    ("look", head("귀가 먹먹하면", 540, 440, 90) + head("꿀꺽 삼키세요!", 540, 560, 96, YELLOW), {"type": "pop", "at": 0.2, "anchor": [540, 500]}),
    ("ear", ear_icon(540, 790, 0.7) + popword("꿀꺽", 760, 760, 64, CYAN, 8, 10), {"type": "pop", "at": 0.6, "anchor": [540, 790]}),
    ("button", button, {"type": "pop", "at": 4.8, "anchor": [540, 1085]}),
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
