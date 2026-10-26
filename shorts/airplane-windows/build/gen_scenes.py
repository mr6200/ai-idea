"""Generate SVG parts for all 12 scenes of the airplane-windows Short (1080x1920).

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
LABEL = "지식 쇼츠 · 비행기 창문"

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
    """Blueprint paper + corner halftone + optional sunburst, label pill and title block."""
    b = f'<rect x="0" y="0" width="{W}" height="{H}" fill="{NAVY}"/>'
    if burst:
        b += rays(*burst)
    b += grid() + dots(0, 0, 560, 560) + dots(560, 1360, 1080, 1920)
    b += pill(LABEL, 540, 200, 36, YELLOW)
    b += (f'<rect x="700" y="1790" width="330" height="80" fill="none" stroke="{LINE}" stroke-opacity="0.6" stroke-width="3"/>'
          + text("DWG. 009 · 지식 쇼츠", 865, 1842, 30, LINE, "middle", NOTE, 'fill-opacity="0.7"'))
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


def window(cx, cy, w, h, round_=True, sky=True, line=LINE, sw=8):
    rx = min(w, h) / 2 if round_ else 6
    inner = (f'<rect x="{cx - w / 2 + 26}" y="{cy - h / 2 + 26}" width="{w - 52}" height="{h - 52}" rx="{max(0, rx - 26)}" '
             f'fill="{SKY if sky else "none"}" stroke="{line}" stroke-width="3" stroke-dasharray="{"" if sky else "14 10"}"/>')
    return f'<rect x="{cx - w / 2}" y="{cy - h / 2}" width="{w}" height="{h}" rx="{rx}" fill="none" stroke="{line}" stroke-width="{sw}"/>' + inner


def corner_stress(cx, cy, w, h, color=YELLOW):
    out = ""
    for sx, sy in ((-1, -1), (1, -1), (-1, 1), (1, 1)):
        x, y = cx + sx * w / 2, cy + sy * h / 2
        out += (f'<circle cx="{x}" cy="{y}" r="24" fill="none" stroke="{color}" stroke-width="6"/>'
                + "".join(f'<path d="M{x + sx * 30} {y + sy * 30 + o} l{sx * 40} {sy * 40}" stroke="{color}" stroke-width="6" stroke-linecap="round"/>' for o in (-14, 14)))
    return out


def flow_ring(cx, cy, rx, ry, color=CYAN):
    return "".join(f'<path d="M{cx + rx * math.cos(a):.0f} {cy + ry * math.sin(a):.0f} A {rx} {ry} 0 0 1 {cx + rx * math.cos(a + 0.9):.0f} {cy + ry * math.sin(a + 0.9):.0f}" '
                   f'fill="none" stroke="{color}" stroke-width="6" stroke-linecap="round"/>' for a in (0.2, 1.75, 3.3, 4.85))


def fuselage(cx, cy, w, h, line=LINE):
    """Side view of an airliner body as a long capsule with oval windows."""
    out = (f'<rect x="{cx - w / 2}" y="{cy - h / 2}" width="{w}" height="{h}" rx="{h / 2}" fill="none" stroke="{line}" stroke-width="8"/>'
           f'<path d="M{cx + w / 2 - 160} {cy - h / 2} L{cx + w / 2 - 20} {cy - h / 2 - 150} L{cx + w / 2 + 30} {cy - h / 2 - 150} L{cx + w / 2 - 40} {cy - h / 2}" fill="none" stroke="{line}" stroke-width="8" stroke-linejoin="round"/>')
    n = 7
    for i in range(n):
        x = cx - w / 2 + 180 + i * (w - 360) / (n - 1)
        out += f'<rect x="{x - 18}" y="{cy - 30}" width="36" height="52" rx="18" fill="{SKY}" stroke="{line}" stroke-width="4"/>'
    return out


# ---------------------------------------------------------------- scenes
scenes = []


def scene(sid, start, end, parts):
    scenes.append({"id": sid, "start": start, "end": end, "parts": parts})


# S01 왜 다 둥글까? -------------------------------------------------------------------------
scene("S01", 0, 5, [
    ("bg", bg(burst=(540, 960)), {"type": "none"}),
    ("title", head("비행기 창문은", 540, 410, 96) + head("왜 다 둥글까?", 540, 560, 124, YELLOW, stroke=14),
     {"type": "pop", "at": 0.0, "anchor": [540, 480]}),
    ("window", window(540, 980, 380, 520, True, True, WHITE, 16) + f'<path d="M420 820 L460 790" stroke="{WHITE}" stroke-width="14" stroke-linecap="round"/>',
     {"type": "pop", "at": 0.3, "anchor": [540, 980]}),
    ("q", burst_star(830, 760, 120, "?!", RED, YELLOW, 90), {"type": "stamp", "at": 1.2, "anchor": [830, 760]}),
    ("no", bubble(300, 1200, 400, 120, "네모는 안 돼?", 50), {"type": "pop", "at": 2.6, "anchor": [300, 1200]}),
])

# S02 기압: 풍선처럼 밀린다 -------------------------------------------------------------------
push = "".join(arrow(540 + 150 * math.cos(math.radians(a)), 900 + 150 * math.sin(math.radians(a)),
                     540 + 300 * math.cos(math.radians(a)), 900 + 300 * math.sin(math.radians(a)), YELLOW, 8) for a in range(0, 360, 45))
scene("S02", 5, 12, [
    ("bg", bg(), {"type": "none"}),
    ("title", head("높은 하늘에서", 540, 420, 84) + head("비행기 안은?", 540, 540, 96, CYAN), {"type": "pop", "at": 0.0, "anchor": [540, 480]}),
    ("body", f'<circle cx="540" cy="900" r="250" fill="none" stroke="{LINE}" stroke-width="10"/>'
     + text("기내", 540, 890, 64, LINE, "middle", HEAD) + text("바깥보다 높은 기압", 540, 950, 38, CYAN), {"type": "pop", "at": 0.4, "anchor": [540, 900]}),
    ("push", push, {"type": "pop", "at": 3.6, "anchor": [540, 900]}),
    ("balloon", pill("풍선처럼 안에서 밀어요", 540, 1290, 50, YELLOW), {"type": "stamp", "at": 4.2, "anchor": [540, 1290]}),
])

# S03 부풀고 줄고, 매 비행마다 --------------------------------------------------------------
scene("S03", 12, 19, [
    ("bg", bg(), {"type": "none"}),
    ("up", text("이륙", 260, 520, 60, YELLOW, "middle", HEAD) + fuselage(540, 720, 760, 170) + popword("부풀고!", 560, 560, 56, YELLOW, 8, -8),
     {"type": "slideR", "at": 0.2}),
    ("down", text("착륙", 260, 960, 60, CYAN, "middle", HEAD) + fuselage(540, 1140, 700, 150) + popword("줄고!", 560, 990, 56, CYAN, 8, 8),
     {"type": "slideL", "at": 1.6}),
    ("repeat", pill("비행할 때마다 반복", 540, 1300, 54, WHITE), {"type": "stamp", "at": 3.8, "anchor": [540, 1300]}),
])

# S04 네모난 구멍은 모서리에 힘이 몰린다 -----------------------------------------------------
scene("S04", 19, 26, [
    ("bg", bg(), {"type": "none"}),
    ("title", head("네모난 구멍이면?", 540, 440, 96), {"type": "pop", "at": 0.0, "anchor": [540, 410]}),
    ("sq", window(540, 880, 400, 500, False, False) + dim(340, 740, 580, "직각 모서리"), {"type": "pop", "at": 0.4, "anchor": [540, 880]}),
    ("stress", corner_stress(540, 880, 400, 500), {"type": "pop", "at": 3.6, "anchor": [540, 880]}),
    ("bang", burst_star(760, 1170, 140, "힘이 몰려!", RED, YELLOW, 50, 14), {"type": "stamp", "at": 4.2, "anchor": [760, 1170]}),
])

# S05 금속 피로 -------------------------------------------------------------------------------
paper = (panel(110, 640, 380, 460) + f'<path d="M300 660 V1080" stroke="{INK}" stroke-width="5" stroke-dasharray="18 12"/>'
         + text("접었다 폈다", 300, 1180, 46, LINE, "middle", POP))
crack = (f'<rect x="590" y="640" width="380" height="460" rx="12" fill="#9aa7b4" stroke="{INK}" stroke-width="8"/>'
         f'<path d="M780 640 L760 740 L800 820 L770 920 L790 1000" fill="none" stroke="{INK}" stroke-width="10" stroke-linejoin="round"/>'
         + text("금속", 780, 1180, 46, LINE, "middle", POP))
scene("S05", 26, 33, [
    ("bg", bg(), {"type": "none"}),
    ("paper", paper + popword("찢!", 300, 600, 70, YELLOW, 8, -10), {"type": "pop", "at": 0.2, "anchor": [300, 870]}),
    ("metal", crack + popword("쩍!", 780, 600, 70, RED, 8, 10), {"type": "pop", "at": 3.4, "anchor": [780, 870]}),
    ("name", pill("금속 피로", 540, 1290, 76, YELLOW), {"type": "stamp", "at": 5.4, "anchor": [540, 1290]}),
    ("title", head("계속 힘을 받으면", 540, 440, 86), {"type": "fade", "at": 0.0}),
])

# S06 1954 코멧 ----------------------------------------------------------------------------
comet = fuselage(540, 860, 820, 180)
scene("S06", 33, 41, [
    ("bg", bg(burst=(540, 900), extra=""), {"type": "none"}),
    ("year", head("1954년", 540, 440, 130, YELLOW, stroke=14), {"type": "stamp", "at": 0.0, "anchor": [540, 400]}),
    ("plane", comet + text("세계 첫 제트 여객기", 540, 1030, 50, CYAN) + text("코멧", 540, 1115, 80, WHITE, "middle", HEAD),
     {"type": "slideR", "at": 0.6}),
    ("break", burst_star(820, 760, 130, "쾅!", RED, YELLOW, 80), {"type": "stamp", "at": 2.4, "anchor": [820, 760]}),
    ("two", bubble(540, 1245, 520, 120, "석 달 사이 두 대!", 54, (1, 1)), {"type": "pop", "at": 3.8, "anchor": [540, 1245]}),
])

# S07 물탱크 시험 -------------------------------------------------------------------------------
tank = (f'<rect x="110" y="560" width="860" height="560" rx="20" fill="{SKY}" fill-opacity="0.25" stroke="{LINE}" stroke-width="8"/>'
        + "".join(f'<path d="M140 {620 + i * 60} q40 -20 80 0 t80 0 t80 0 t80 0 t80 0 t80 0 t80 0 t80 0 t80 0 t80 0" fill="none" stroke="{CYAN}" stroke-width="3" stroke-opacity="0.6"/>'
                  for i in range(8))
        + fuselage(540, 840, 640, 150) + text("물탱크", 540, 1180, 48, CYAN))
scene("S07", 41, 48, [
    ("bg", bg(), {"type": "none"}),
    ("title", head("조사팀의 실험", 540, 440, 96), {"type": "pop", "at": 0.0, "anchor": [540, 410]}),
    ("tank", tank, {"type": "pop", "at": 0.4, "anchor": [540, 840]}),
    ("cycles", pill("압력 넣었다 뺐다 × 수천 번", 540, 1290, 48, YELLOW), {"type": "stamp", "at": 3.8, "anchor": [540, 1290]}),
])

# S08 각진 구멍 모서리에서 금 → 둥글게 -----------------------------------------------------------
scene("S08", 48, 55, [
    ("bg", bg(), {"type": "none"}),
    ("title", head("균열의 시작점", 540, 440, 96, YELLOW), {"type": "pop", "at": 0.0, "anchor": [540, 410]}),
    ("hole", window(540, 860, 360, 300, False, False) + f'<path d="M720 710 L780 660 L820 690 L880 620" fill="none" stroke="{RED}" stroke-width="10" stroke-linejoin="round"/>'
     + f'<circle cx="720" cy="710" r="34" fill="none" stroke="{YELLOW}" stroke-width="8"/>' + text("각진 구멍 모서리", 540, 1080, 50, CYAN),
     {"type": "pop", "at": 0.4, "anchor": [540, 860]}),
    ("after", arrow(540, 1120, 540, 1200, YELLOW, 10) + pill("그 뒤로 모서리는 둥글게", 540, 1285, 52, WHITE), {"type": "slideU", "at": 3.6}),
])

# S09 둥근 모서리는 힘을 고르게 -----------------------------------------------------------------
scene("S09", 55, 62, [
    ("bg", bg(), {"type": "none"}),
    ("sq", window(300, 920, 300, 400, False, False) + corner_stress(300, 920, 300, 400) + text("몰림", 300, 1190, 56, YELLOW, "middle", HEAD),
     {"type": "slideL", "at": 0.0}),
    ("rd", window(780, 920, 300, 400, True, True) + flow_ring(780, 920, 190, 240) + text("고르게", 780, 1190, 56, CYAN, "middle", HEAD),
     {"type": "slideR", "at": 0.4}),
    ("vs", burst_star(540, 920, 70, "VS", INK, WHITE, 44, 10), {"type": "stamp", "at": 1.0, "anchor": [540, 920]}),
    ("title", head("둥근 모서리의 힘", 540, 440, 96), {"type": "pop", "at": 0.0, "anchor": [540, 410]}),
    ("ok", pill("그래서 창문도 둥글게!", 540, 1300, 54, YELLOW), {"type": "stamp", "at": 3.6, "anchor": [540, 1300]}),
])

# S10 정리 --------------------------------------------------------------------------------------
scene("S10", 62, 70, [
    ("bg", bg(), {"type": "none"}),
    ("badge", pill("정리", 540, 400, 64, YELLOW), {"type": "pop", "at": 0.0, "anchor": [540, 400]}),
    ("a", panel(90, 520, 900, 300, NAVY_D) + window(250, 670, 160, 210, False, False, LINE, 6) + corner_stress(250, 670, 160, 210)
     + text("네모", 440, 650, 60, WHITE, "start", HEAD) + text("모서리에 힘이 몰림", 440, 730, 48, YELLOW, "start", NOTE),
     {"type": "slideL", "at": 0.4}),
    ("b", panel(90, 880, 900, 300, NAVY_D) + window(250, 1030, 160, 210, True, True, LINE, 6)
     + text("둥근 창문", 440, 1010, 60, WHITE, "start", HEAD) + text("힘을 고르게 나눔", 440, 1090, 48, CYAN, "start", NOTE),
     {"type": "slideR", "at": 3.6}),
])

# S11 퀴즈: 창문 아래 작은 구멍 ---------------------------------------------------------------------
spots = [(140 + i * 66, 1240 + (i % 3) * 14) for i in range(13)]
scene("S11", 70, 80, [
    ("bg", bg(burst=(540, 900)), {"type": "none"}),
    ("badge", pill("퀴즈", 540, 380, 64, YELLOW), {"type": "pop", "at": 0.0, "anchor": [540, 380]}),
    ("question", head("창문 아래 작은 구멍", 540, 530, 80) + head("정체는?", 540, 640, 90, YELLOW), {"type": "pop", "at": 0.3, "anchor": [540, 590]}),
    ("win", window(540, 950, 300, 400, True, True, WHITE, 12) + f'<circle cx="540" cy="1080" r="9" fill="{INK}"/>'
     + f'<circle cx="540" cy="1080" r="40" fill="none" stroke="{RED}" stroke-width="6"/>', {"type": "pop", "at": 0.8, "anchor": [540, 950]}),
    ("answer", burst_star(830, 1110, 145, "숨구멍!", RED, YELLOW, 54, 14), {"type": "stamp", "at": 3.6, "anchor": [830, 1110]}),
    ("why", pill("유리 사이 압력을 맞춰요", 540, 1305, 46, WHITE), {"type": "fade", "at": 6.8}),
])

# S12 창문 모서리를 봐 주세요 + 구독 ---------------------------------------------------------------
button = (f'<rect x="300" y="1010" width="500" height="170" rx="85" fill="{INK}"/>'
          f'<rect x="290" y="1000" width="500" height="170" rx="85" fill="{RED}" stroke="{INK}" stroke-width="8"/>'
          + popword("구독", 560, 1118, 92, WHITE, 8)
          + f'<path d="M405 1035 C375 1035 368 1065 368 1090 L360 1120 H450 L442 1090 C442 1065 435 1035 405 1035 Z M392 1130 a13 13 0 0 0 26 0 Z" fill="{WHITE}" stroke="{INK}" stroke-width="4"/>')
finger = (f'<path d="M700 1145 V1250 C700 1280 740 1300 770 1300 H820 C850 1300 870 1270 870 1240 V1200 C870 1185 845 1180 835 1195 '
          f'C835 1175 810 1170 800 1188 C800 1170 775 1165 765 1185 V1145 C765 1120 700 1120 700 1145 Z" fill="#f6d2b3" stroke="{INK}" stroke-width="6"/>')
scene("S12", 80, 90, [
    ("bg", bg(), {"type": "none"}),
    ("look", head("다음에 비행기 타면", 540, 440, 84) + head("창문 모서리를 보세요", 540, 560, 84, YELLOW), {"type": "pop", "at": 0.2, "anchor": [540, 500]}),
    ("win", window(540, 790, 200, 260, True, True, WHITE, 10), {"type": "pop", "at": 0.6, "anchor": [540, 790]}),
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
