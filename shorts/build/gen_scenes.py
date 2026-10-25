"""Generate SVG parts for storyboard scenes S04-S18 (1080x1920).

Each scene is a list of parts; each part becomes its own full-frame SVG so the
exported PNG layers line up in EffectCraft. A manifest records the timing and
animation hints the EffectCraft build script reads.
"""
import json
import math
import os

W, H = 1080, 1920
FONT = "WenQuanYi Zen Hei"
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "svg")

CREAM, GLOW, SHADOW = "#fde9c8", "#fff4e2", "#ecd3aa"
INK, MUTED = "#2b2b2b", "#7a6f63"
ORANGE, GREEN, RED = "#f28c28", "#2f7d6d", "#c8553d"
GOLD, GOLD_D = "#e0b23a", "#b98a1e"
WHITE = "#ffffff"


def text_width(s, size):
    w = 0.0
    for ch in s:
        if ord(ch) > 0x2E80:
            w += size * 0.98
        elif ch == " ":
            w += size * 0.3
        else:
            w += size * 0.56
    return w


def text(s, x, y, size, fill=INK, anchor="middle", extra=""):
    assert text_width(s, size) < 1000, f"text too wide: {s}"
    s = s.replace("&", "&amp;").replace("<", "&lt;")
    return (f'<text x="{x}" y="{y}" font-family="{FONT}" font-size="{size}" '
            f'fill="{fill}" text-anchor="{anchor}" {extra}>{s}</text>')


def pill(s, cx, cy, size, bg, fg=WHITE, pad=40):
    w = text_width(s, size) + pad * 2
    h = size * 1.7
    return (f'<rect x="{cx - w / 2:.1f}" y="{cy - h / 2:.1f}" width="{w:.1f}" height="{h:.1f}" '
            f'rx="{h / 2:.1f}" fill="{bg}"/>' + text(s, cx, cy + size * 0.36, size, fg))


def svg(body):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">'
            f'<rect x="0" y="0" width="{W}" height="{H}" fill="#000000" fill-opacity="0"/>{body}</svg>')


def bg_cream(extra=""):
    return (f'<rect x="0" y="0" width="{W}" height="{H}" fill="{CREAM}"/>'
            f'<circle cx="540" cy="860" r="470" fill="{GLOW}"/>'
            + pill("지식 쇼츠 · 복리의 마법", 540, 256, 38, ORANGE) + extra)


def coin(cx, cy, rx, label="", fs=40, color=GOLD, edge=GOLD_D):
    ry = rx * 0.3
    t = text(label, cx, cy + fs * 0.36, fs, WHITE) if label else ""
    return (f'<ellipse cx="{cx}" cy="{cy + ry * 0.45:.1f}" rx="{rx}" ry="{ry:.1f}" fill="{edge}"/>'
            f'<ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry:.1f}" fill="{color}" stroke="{edge}" stroke-width="4"/>' + t)


def stack(cx, base, n, rx=110, label="원금"):
    out = ""
    for i in range(n):
        out += coin(cx, base - i * 40, rx, label if i == n - 1 else "")
    return out


def arrow(x1, y1, x2, y2, color=INK, w=6):
    ang = math.atan2(y2 - y1, x2 - x1)
    a1 = (x2 - 22 * math.cos(ang - 0.45), y2 - 22 * math.sin(ang - 0.45))
    a2 = (x2 - 22 * math.cos(ang + 0.45), y2 - 22 * math.sin(ang + 0.45))
    return (f'<path d="M{x1} {y1} L{x2} {y2} M{a1[0]:.1f} {a1[1]:.1f} L{x2} {y2} L{a2[0]:.1f} {a2[1]:.1f}" '
            f'fill="none" stroke="{color}" stroke-width="{w}" stroke-linecap="round" stroke-linejoin="round"/>')


def person(cx, feet, shirt, s=1.0, glasses=False, hair="#3b2a20"):
    """Friendly flat character; feet at y=feet, about 560*s tall."""
    def p(v):
        return v * s
    head_cy = feet - p(440)
    out = ""
    # legs
    out += (f'<rect x="{cx - p(70):.1f}" y="{feet - p(150):.1f}" width="{p(55):.1f}" height="{p(150):.1f}" rx="{p(22):.1f}" fill="#46506b"/>'
            f'<rect x="{cx + p(15):.1f}" y="{feet - p(150):.1f}" width="{p(55):.1f}" height="{p(150):.1f}" rx="{p(22):.1f}" fill="#46506b"/>')
    # arms
    out += (f'<rect x="{cx - p(150):.1f}" y="{feet - p(320):.1f}" width="{p(50):.1f}" height="{p(170):.1f}" rx="{p(25):.1f}" fill="{shirt}" transform="rotate(12 {cx - p(125):.1f} {feet - p(320):.1f})"/>'
            f'<rect x="{cx + p(100):.1f}" y="{feet - p(320):.1f}" width="{p(50):.1f}" height="{p(170):.1f}" rx="{p(25):.1f}" fill="{shirt}" transform="rotate(-12 {cx + p(125):.1f} {feet - p(320):.1f})"/>')
    # body
    out += f'<rect x="{cx - p(115):.1f}" y="{feet - p(330):.1f}" width="{p(230):.1f}" height="{p(220):.1f}" rx="{p(70):.1f}" fill="{shirt}"/>'
    # head
    out += f'<circle cx="{cx}" cy="{head_cy:.1f}" r="{p(110):.1f}" fill="#f6d2b3"/>'
    # hair cap
    out += (f'<path d="M{cx - p(112):.1f} {head_cy - p(5):.1f} C{cx - p(110):.1f} {head_cy - p(130):.1f} {cx + p(110):.1f} {head_cy - p(130):.1f} '
            f'{cx + p(112):.1f} {head_cy - p(5):.1f} C{cx + p(60):.1f} {head_cy - p(55):.1f} {cx - p(40):.1f} {head_cy - p(70):.1f} {cx - p(112):.1f} {head_cy - p(5):.1f} Z" fill="{hair}"/>')
    # eyes, cheeks, smile
    ey = head_cy + p(15)
    out += (f'<circle cx="{cx - p(40):.1f}" cy="{ey:.1f}" r="{p(11):.1f}" fill="{INK}"/>'
            f'<circle cx="{cx + p(40):.1f}" cy="{ey:.1f}" r="{p(11):.1f}" fill="{INK}"/>'
            f'<circle cx="{cx - p(68):.1f}" cy="{ey + p(30):.1f}" r="{p(16):.1f}" fill="#f2a58e" fill-opacity="0.7"/>'
            f'<circle cx="{cx + p(68):.1f}" cy="{ey + p(30):.1f}" r="{p(16):.1f}" fill="#f2a58e" fill-opacity="0.7"/>'
            f'<path d="M{cx - p(28):.1f} {ey + p(38):.1f} Q{cx} {ey + p(62):.1f} {cx + p(28):.1f} {ey + p(38):.1f}" fill="none" stroke="{INK}" stroke-width="{p(7):.1f}" stroke-linecap="round"/>')
    if glasses:
        out += (f'<circle cx="{cx - p(40):.1f}" cy="{ey:.1f}" r="{p(26):.1f}" fill="none" stroke="{INK}" stroke-width="{p(6):.1f}"/>'
                f'<circle cx="{cx + p(40):.1f}" cy="{ey:.1f}" r="{p(26):.1f}" fill="none" stroke="{INK}" stroke-width="{p(6):.1f}"/>'
                f'<path d="M{cx - p(14):.1f} {ey:.1f} H{cx + p(14):.1f}" stroke="{INK}" stroke-width="{p(6):.1f}"/>')
    return out


def poly(points):
    return " ".join(f"{'M' if i == 0 else 'L'}{x:.1f} {y:.1f}" for i, (x, y) in enumerate(points))


# ---------------------------------------------------------------- scenes
# Each scene: dict(id, start, end, parts=[(name, svg_body, anim)])
# anim: dict(type=pop|fade|slideL|slideR|slideU|growY|wipeL|wipeU|drop|stamp|spin, at=seconds
#            from scene start, anchor=[x,y] for pop/growY/spin)
scenes = []


def scene(sid, start, end, parts):
    scenes.append({"id": sid, "start": start, "end": end, "parts": parts})


# S04 단리 vs 복리 -------------------------------------------------------------
left_interest = (coin(270, 900, 62, "이자", 34) + arrow(270, 1010, 270, 950, INK, 5))
right_interest = (coin(810, 900, 62, "이자", 34) + arrow(810, 1010, 810, 950, INK, 5))
right_interest2 = (coin(810, 760, 46, "", 0, ORANGE, "#c96a14") + text("이자의 이자", 810, 700, 36, ORANGE)
                   + arrow(810, 872, 810, 800, ORANGE, 5))
scene("S04", 12, 20, [
    ("bg", bg_cream(), {"type": "none"}),
    ("divider", f'<path d="M540 420 V1270" stroke="{MUTED}" stroke-width="5" stroke-dasharray="18 14"/>', {"type": "wipeD", "at": 0.0}),
    ("title_l", text("단리", 270, 520, 110) + text("원금에만 이자", 270, 600, 42, MUTED), {"type": "pop", "at": 0.3, "anchor": [270, 540]}),
    ("title_r", text("복리", 810, 520, 110, ORANGE) + text("이자에도 이자", 810, 600, 42, MUTED), {"type": "pop", "at": 2.6, "anchor": [810, 540]}),
    ("stack_l", stack(270, 1150, 4), {"type": "slideU", "at": 0.8}),
    ("stack_r", stack(810, 1150, 4), {"type": "slideU", "at": 3.0}),
    ("int_l", left_interest, {"type": "pop", "at": 1.6, "anchor": [270, 900]}),
    ("int_r", right_interest, {"type": "pop", "at": 3.8, "anchor": [810, 900]}),
    ("int_r2", right_interest2, {"type": "pop", "at": 4.8, "anchor": [810, 760]}),
])

# S05 1년 뒤 +7만 ------------------------------------------------------------------
scene("S05", 20, 28, [
    ("bg", bg_cream(f'<path d="M540 640 V1180" stroke="{MUTED}" stroke-width="5" stroke-dasharray="18 14"/>'), {"type": "none"}),
    ("header", pill("100만 원 · 연 7%", 540, 470, 60, INK), {"type": "pop", "at": 0.0, "anchor": [540, 470]}),
    ("labels", text("단리 · 1년 뒤", 270, 680, 48, MUTED) + text("복리 · 1년 뒤", 810, 680, 48, MUTED), {"type": "fade", "at": 0.8}),
    ("plus_l", text("+7만", 270, 860, 150, GOLD_D), {"type": "pop", "at": 1.6, "anchor": [270, 810]}),
    ("plus_r", text("+7만", 810, 860, 150, ORANGE), {"type": "pop", "at": 2.0, "anchor": [810, 810]}),
    ("coins", coin(270, 1060, 90, "7만", 40) + coin(810, 1060, 90, "7만", 40), {"type": "drop", "at": 2.6}),
    ("shrug", text("별거 아닌 것 같죠?", 540, 1270, 76), {"type": "pop", "at": 4.6, "anchor": [540, 1245]}),
])

# S06 10년 뒤 막대 -----------------------------------------------------------------
BASE = 1180
h170, h197, h100 = 170 * 2.4, 197 * 2.4, 100 * 2.4
scene("S06", 28, 35, [
    ("bg", bg_cream(f'<path d="M120 {BASE} H960" stroke="{INK}" stroke-width="6" stroke-linecap="round"/>'
                    + text("단리", 300, BASE + 70, 50) + text("복리", 780, BASE + 70, 50, ORANGE)), {"type": "none"}),
    ("header", text("10년 뒤", 540, 460, 96), {"type": "pop", "at": 0.0, "anchor": [540, 430]}),
    ("ref", f'<path d="M150 {BASE - h100:.0f} H930" stroke="{MUTED}" stroke-width="4" stroke-dasharray="14 10"/>'
            + text("처음 100만", 540, BASE - h100 - 18, 34, MUTED), {"type": "fade", "at": 0.4}),
    ("bar_l", f'<rect x="200" y="{BASE - h170:.0f}" width="200" height="{h170:.0f}" rx="16" fill="{GOLD}"/>', {"type": "growY", "at": 0.8, "anchor": [300, BASE], "dur": 2.2, "ease": "linear"}),
    ("bar_r", f'<rect x="680" y="{BASE - h197:.0f}" width="200" height="{h197:.0f}" rx="16" fill="{ORANGE}"/>', {"type": "growY", "at": 0.8, "anchor": [780, BASE], "dur": 2.6, "ease": "accel"}),
    ("val_l", text("170만", 300, BASE - h170 - 30, 72, GOLD_D), {"type": "pop", "at": 3.1, "anchor": [300, BASE - h170 - 55]}),
    ("val_r", text("197만", 780, BASE - h197 - 30, 84, ORANGE), {"type": "pop", "at": 3.5, "anchor": [780, BASE - h197 - 60]}),
    ("badge", pill("거의 2배!", 540, 1330, 64, RED), {"type": "stamp", "at": 4.3, "anchor": [540, 1330]}),
])

# S07 72의 법칙 ---------------------------------------------------------------------
scene("S07", 35, 43, [
    ("bg", bg_cream(), {"type": "none"}),
    ("title", text("72의 법칙", 540, 470, 100), {"type": "pop", "at": 0.0, "anchor": [540, 440]}),
    ("num", text("72", 540, 860, 300, ORANGE), {"type": "drop", "at": 1.0}),
    ("line", f'<rect x="300" y="905" width="480" height="16" rx="8" fill="{INK}"/>', {"type": "wipeL", "at": 2.2}),
    ("denom", text("수익률", 540, 1070, 130), {"type": "pop", "at": 2.8, "anchor": [540, 1020]}),
    ("result", pill("= 돈이 두 배 되는 데 걸리는 해", 540, 1250, 50, GREEN), {"type": "pop", "at": 4.4, "anchor": [540, 1250]}),
])

# S08 타임라인 2배씩 ------------------------------------------------------------------
TX = [200, 420, 640, 860]
TB = 1160
bar_h = [60, 120, 240, 480]
labels = ["×1", "×2", "×4", "×8"]
years = ["지금", "10년", "20년", "30년"]
s08_parts = [
    ("bg", bg_cream(f'<path d="M110 {TB} H970" stroke="{INK}" stroke-width="6" stroke-linecap="round"/>'
                    + "".join(f'<circle cx="{x}" cy="{TB}" r="12" fill="{INK}"/>' + text(yv, x, TB + 70, 44) for x, yv in zip(TX, years))),
     {"type": "none"}),
    ("header", text("연 7%면 약 10년마다 2배", 540, 440, 64), {"type": "pop", "at": 0.0, "anchor": [540, 415]}),
    ("sub", text("72 ÷ 7 ≈ 10년 · 72 ÷ 10 ≈ 7년", 540, 520, 44, MUTED), {"type": "fade", "at": 0.6}),
]
shades = ["#f6b26b", "#f4a04a", "#f28c28", "#e0731a"]
for i, (x, h, lab) in enumerate(zip(TX, bar_h, labels)):
    body = (f'<rect x="{x - 70}" y="{TB - 12 - h}" width="140" height="{h}" rx="14" fill="{shades[i]}"/>'
            + text(lab, x, TB - 12 - h - 26, 64, ORANGE if i == 3 else INK))
    s08_parts.append((f"b{i + 1}", body, {"type": "pop", "at": 2.0 + i * 2.2, "anchor": [x, TB - 12]}))
scene("S08", 43, 55, s08_parts)

# S09 두 사람 ---------------------------------------------------------------------
scene("S09", 55, 63, [
    ("bg", bg_cream(), {"type": "none"}),
    ("title", text("두 사람이 있습니다", 540, 450, 80), {"type": "pop", "at": 0.0, "anchor": [540, 420]}),
    ("charA", person(300, 1120, GREEN) + pill("A · 25살", 300, 1190, 50, GREEN), {"type": "slideL", "at": 0.8}),
    ("charB", person(780, 1120, ORANGE, glasses=True, hair="#5a4636") + pill("B · 35살", 780, 1190, 50, ORANGE), {"type": "slideR", "at": 1.6}),
    ("question", text("누가 더 많이 모았을까?", 540, 1330, 66, INK), {"type": "pop", "at": 4.0, "anchor": [540, 1305]}),
])

# S10 넣은 돈 ------------------------------------------------------------------------
B10 = 1150


def blocks(cx, n, color):
    return "".join(f'<rect x="{cx - 90}" y="{B10 - (i + 1) * 20 + 3}" width="180" height="17" rx="5" fill="{color}"/>' for i in range(n))


scene("S10", 63, 75, [
    ("bg", bg_cream(f'<path d="M140 {B10 + 6} H940" stroke="{INK}" stroke-width="6" stroke-linecap="round"/>'
                    + text("A", 300, B10 + 70, 52, GREEN) + text("B", 780, B10 + 70, 52, ORANGE)), {"type": "none"}),
    ("title", text("매년 360만 원씩 넣는다면", 540, 380, 62), {"type": "pop", "at": 0.0, "anchor": [540, 360]}),
    ("charA", person(300, 830, GREEN, s=0.5), {"type": "pop", "at": 0.6, "anchor": [300, 830]}),
    ("barA", blocks(300, 10, GREEN) + text("10년", 430, B10 - 110, 44, GREEN, "start"), {"type": "wipeU", "at": 1.0, "dur": 2.5}),
    ("stamp", f'<g transform="rotate(-12 300 880)"><rect x="180" y="835" width="240" height="96" rx="14" fill="none" stroke="{RED}" stroke-width="10"/>'
              + text("STOP", 300, 905, 70, RED) + "</g>", {"type": "stamp", "at": 3.8, "anchor": [300, 883]}),
    ("totalA", text("총 3,600만", 300, 1300, 58, GREEN), {"type": "pop", "at": 4.4, "anchor": [300, 1280]}),
    ("barB", blocks(780, 30, ORANGE) + text("30년", 900, B10 - 330, 44, ORANGE, "start"), {"type": "wipeU", "at": 5.8, "dur": 4.0}),
    ("totalB", text("총 1억 800만", 780, 1300, 58, ORANGE), {"type": "pop", "at": 10.0, "anchor": [780, 1280]}),
])

# S11 성장 곡선 레이스 ----------------------------------------------------------------
X0, X1, YB, YT = 150, 950, 1200, 520
MAXV = 38000.0


def ax(age):
    return X0 + (age - 25) / 40.0 * (X1 - X0)


def ay(v):
    return YB - v / MAXV * (YB - YT)


def value_a(age):
    yrs = age - 25
    if yrs <= 10:
        return 360 * ((1.07 ** yrs - 1) / 0.07)
    return 360 * ((1.07 ** 10 - 1) / 0.07) * 1.07 ** (yrs - 10)


def value_b(age):
    yrs = age - 35
    return 0 if yrs <= 0 else 360 * ((1.07 ** yrs - 1) / 0.07)


ages = [25 + i * 0.25 for i in range(161)]
pa = [(ax(a), ay(value_a(a))) for a in ages]
pb = [(ax(a), ay(value_b(a))) for a in ages if a >= 35]
ticks = "".join(f'<path d="M{ax(a):.0f} {YB} V{YB + 16}" stroke="{INK}" stroke-width="5"/>' + text(f"{a}", ax(a), YB + 70, 42)
                for a in (25, 35, 45, 55, 65))
scene("S11", 75, 88, [
    ("bg", bg_cream(f'<path d="M{X0} {YT - 40} V{YB} H{X1 + 20}" fill="none" stroke="{INK}" stroke-width="6" stroke-linecap="round"/>'
                    + ticks + text("나이", X1 + 10, YB + 130, 36, MUTED, "end") + text("모은 돈", X0 + 10, YT - 60, 36, MUTED, "start")),
     {"type": "none"}),
    ("title", text("연 7%로 65살까지 굴리면?", 540, 400, 62), {"type": "pop", "at": 0.0, "anchor": [540, 380]}),
    ("curveA", f'<path d="{poly(pa)}" fill="none" stroke="{GREEN}" stroke-width="14" stroke-linecap="round" stroke-linejoin="round"/>', {"type": "wipeL", "at": 1.0, "dur": 8.0, "ease": "linear"}),
    ("curveB", f'<path d="{poly(pb)}" fill="none" stroke="{ORANGE}" stroke-width="14" stroke-linecap="round" stroke-linejoin="round"/>', {"type": "wipeL", "at": 1.0, "dur": 8.0, "ease": "linear"}),
    ("endA", f'<circle cx="{pa[-1][0]:.0f}" cy="{pa[-1][1]:.0f}" r="26" fill="{GREEN}"/>' + text("A", pa[-1][0] - 60, pa[-1][1] - 14, 54, GREEN), {"type": "pop", "at": 9.0, "anchor": [pa[-1][0], pa[-1][1]]}),
    ("endB", f'<circle cx="{pb[-1][0]:.0f}" cy="{pb[-1][1]:.0f}" r="26" fill="{ORANGE}"/>' + text("B", pb[-1][0] - 60, pb[-1][1] + 66, 54, ORANGE), {"type": "pop", "at": 9.2, "anchor": [pb[-1][0], pb[-1][1]]}),
])

# S12 결과 공개 -----------------------------------------------------------------------
card_b = (f'<rect x="120" y="520" width="840" height="230" rx="36" fill="{WHITE}" stroke="{ORANGE}" stroke-width="6"/>'
          + person(230, 730, ORANGE, s=0.32, glasses=True, hair="#5a4636")
          + text("B · 30년 동안 1억 800만 원", 330, 600, 38, MUTED, "start")
          + text("약 3억 4천만 원", 330, 700, 72, ORANGE, "start"))
card_a = (f'<rect x="90" y="820" width="900" height="300" rx="40" fill="{WHITE}" stroke="{GREEN}" stroke-width="10"/>'
          + person(220, 1070, GREEN, s=0.4)
          + text("A · 10년 동안 3,600만 원", 340, 910, 40, MUTED, "start")
          + text("약 3억 7,900만", 340, 1040, 92, GREEN, "start"))
confetti = ""
cols = [ORANGE, GREEN, RED, GOLD, "#3b82c4"]
spots = [(140 + i * 66, 768 + (i % 3) * 14) for i in range(13)]
spots += [(40 + (i % 2) * 22, 840 + i * 46) for i in range(6)] + [(1010 + (i % 2) * 22, 840 + i * 46) for i in range(6)]
for i, (x, y) in enumerate(spots):
    r = (i * 37) % 180
    confetti += f'<rect x="{x}" y="{y}" width="22" height="12" rx="3" fill="{cols[i % 5]}" transform="rotate({r} {x + 11} {y + 6})"/>'
scene("S12", 88, 95, [
    ("bg", bg_cream(), {"type": "none"}),
    ("title", text("65살, 최종 금액은?", 540, 440, 72), {"type": "pop", "at": 0.0, "anchor": [540, 415]}),
    ("cardB", card_b, {"type": "slideR", "at": 0.6}),
    ("cardA", card_a, {"type": "pop", "at": 2.4, "anchor": [540, 970]}),
    ("confetti", confetti, {"type": "drop", "at": 2.6}),
    ("message", pill("세 배 적게 넣은 A가 더 많다", 540, 1270, 52, INK), {"type": "pop", "at": 4.2, "anchor": [540, 1270]}),
])

# S13 버핏 곡선 -----------------------------------------------------------------------
X0b, X1b, YBb, YTb = 150, 950, 1180, 560


def bx(age):
    return X0b + (age - 20) / 75.0 * (X1b - X0b)


curve = [(bx(a), YBb - (1.1 ** (a - 20) - 1) / (1.1 ** 75 - 1) * (YBb - YTb)) for a in [20 + i * 0.5 for i in range(151)]]
ticks_b = "".join(f'<path d="M{bx(a):.0f} {YBb} V{YBb + 16}" stroke="{INK}" stroke-width="5"/>' + text(f"{a}세", bx(a), YBb + 70, 40)
                  for a in (20, 40, 65, 90))
scene("S13", 95, 105, [
    ("bg", bg_cream(f'<path d="M{X0b} {YTb - 40} V{YBb} H{X1b + 20}" fill="none" stroke="{INK}" stroke-width="6" stroke-linecap="round"/>' + ticks_b),
     {"type": "none"}),
    ("title", text("워런 버핏의 재산", 540, 420, 80), {"type": "pop", "at": 0.0, "anchor": [540, 395]}),
    ("highlight", f'<rect x="{bx(65):.0f}" y="{YTb - 60}" width="{X1b + 20 - bx(65):.0f}" height="{YBb - YTb + 60}" fill="{ORANGE}" fill-opacity="0.16"/>'
                  + text("65세 이후", (bx(65) + X1b) / 2, YTb + 20, 44, ORANGE), {"type": "fade", "at": 4.0}),
    ("curve", f'<path d="{poly(curve)}" fill="none" stroke="{ORANGE}" stroke-width="14" stroke-linecap="round"/>', {"type": "wipeL", "at": 0.8, "dur": 4.5, "ease": "linear"}),
    ("caption", pill("재산 대부분 = 65세 이후", 540, 1320, 54, INK), {"type": "pop", "at": 5.4, "anchor": [540, 1320]}),
])

# S14 시계와 시간 ---------------------------------------------------------------------
CX, CY, R = 540, 780, 210
ticks_c = "".join(
    f'<path d="M{CX + (R - 18) * math.sin(math.radians(a)):.1f} {CY - (R - 18) * math.cos(math.radians(a)):.1f} '
    f'L{CX + (R - 42) * math.sin(math.radians(a)):.1f} {CY - (R - 42) * math.cos(math.radians(a)):.1f}" stroke="{INK}" stroke-width="8" stroke-linecap="round"/>'
    for a in range(0, 360, 30))
hs = [(170 + i * 4, 1280 - 0.6 * (1.18 ** (i * 0.5) - 1)) for i in range(0, 186)]
hs = [(x, max(y, 1050)) for x, y in hs]
scene("S14", 105, 115, [
    ("bg", bg_cream(), {"type": "none"}),
    ("title", text("진짜 재료는", 540, 400, 64) + text("시간", 540, 510, 110, ORANGE), {"type": "pop", "at": 0.0, "anchor": [540, 450]}),
    ("face", f'<circle cx="{CX}" cy="{CY}" r="{R}" fill="{WHITE}" stroke="{INK}" stroke-width="12"/>' + ticks_c, {"type": "pop", "at": 0.4, "anchor": [CX, CY]}),
    ("hand_m", f'<path d="M{CX} {CY + 20} V{CY - 160}" stroke="{INK}" stroke-width="12" stroke-linecap="round"/>', {"type": "spin", "at": 0.4, "anchor": [CX, CY], "speed": 720}),
    ("hand_h", f'<path d="M{CX} {CY + 14} V{CY - 100}" stroke="{ORANGE}" stroke-width="16" stroke-linecap="round"/><circle cx="{CX}" cy="{CY}" r="18" fill="{INK}"/>',
     {"type": "spin", "at": 0.4, "anchor": [CX, CY], "speed": 60}),
    ("curve", f'<path d="{poly(hs)}" fill="none" stroke="{GREEN}" stroke-width="12" stroke-linecap="round"/>'
              + f'<path d="M160 1290 H930" stroke="{INK}" stroke-width="5"/>', {"type": "wipeL", "at": 3.0, "dur": 5.0, "ease": "linear"}),
    ("labels", text("지루하게 평평…", 330, 1345, 40, MUTED) + text("어느 순간 꺾인다!", 700, 1120, 44, GREEN), {"type": "fade", "at": 6.5}),
])

# S15 초록 계단 ---------------------------------------------------------------------
steps_up = []
x, y = 140, 1260
pts = [(x, y)]
for i in range(8):
    x += 100
    pts.append((x, y))
    y -= 30 + i * 12
    pts.append((x, y))
stairs_up = f'<path d="{poly(pts)} L{pts[-1][0]} 1260 Z" fill="#cfe6df"/><path d="{poly(pts)}" fill="none" stroke="{GREEN}" stroke-width="12" stroke-linejoin="round"/>'
top = pts[-1]
scene("S15", 115, 125, [
    ("bg", bg_cream(), {"type": "none"}),
    ("title", text("매일 1%씩 나아지면", 540, 420, 72), {"type": "pop", "at": 0.0, "anchor": [540, 395]}),
    ("formula", text("1.01³⁶⁵", 540, 560, 96, GREEN), {"type": "pop", "at": 1.0, "anchor": [540, 525]}),
    ("stairs", stairs_up, {"type": "wipeL", "at": 1.6, "dur": 3.0, "ease": "linear"}),
    ("runner", person(top[0] - 40, top[1], GREEN, s=0.36), {"type": "pop", "at": 4.6, "anchor": [top[0] - 40, top[1]]}),
    ("result", pill("약 37.8배", 540, 1310, 80, GREEN), {"type": "stamp", "at": 5.4, "anchor": [540, 1310]}),
])

# S16 빨간 계단 + 습관 아이콘 ----------------------------------------------------------
x, y = 140, 640
pts = [(x, y)]
for i in range(8):
    x += 100
    pts.append((x, y))
    y += 52 - i * 5
    pts.append((x, y))
stairs_dn = f'<path d="{poly(pts)} L{pts[-1][0]} 1060 L140 1060 Z" fill="#f2d3c9"/><path d="{poly(pts)}" fill="none" stroke="{RED}" stroke-width="12" stroke-linejoin="round"/>'
book = (f'<rect x="200" y="1110" width="140" height="110" rx="10" fill="{GREEN}"/><path d="M270 1110 V1220" stroke="{WHITE}" stroke-width="6"/>'
        + text("공부", 270, 1290, 46))
run = (f'<rect x="440" y="1150" width="200" height="30" rx="12" fill="{INK}"/><rect x="430" y="1120" width="34" height="90" rx="10" fill="{ORANGE}"/>'
       f'<rect x="616" y="1120" width="34" height="90" rx="10" fill="{ORANGE}"/>' + text("운동", 540, 1290, 46))
alarm = (f'<circle cx="810" cy="1168" r="56" fill="{WHITE}" stroke="{INK}" stroke-width="8"/><path d="M810 1168 V1130 M810 1168 L836 1180" stroke="{INK}" stroke-width="7" stroke-linecap="round"/>'
         f'<circle cx="768" cy="1112" r="16" fill="{INK}"/><circle cx="852" cy="1112" r="16" fill="{INK}"/>' + text("습관", 810, 1290, 46))
scene("S16", 125, 135, [
    ("bg", bg_cream(), {"type": "none"}),
    ("title", text("매일 1%씩 나빠지면", 540, 420, 72), {"type": "pop", "at": 0.0, "anchor": [540, 395]}),
    ("formula", text("0.99³⁶⁵ ≈ 0.03배", 540, 560, 84, RED), {"type": "pop", "at": 0.8, "anchor": [540, 530]}),
    ("stairs", stairs_dn, {"type": "wipeL", "at": 1.4, "dur": 2.6, "ease": "linear"}),
    ("icon1", book, {"type": "pop", "at": 5.0, "anchor": [270, 1170]}),
    ("icon2", run, {"type": "pop", "at": 5.6, "anchor": [540, 1170]}),
    ("icon3", alarm, {"type": "pop", "at": 6.2, "anchor": [810, 1170]}),
])

# S17 오늘 ------------------------------------------------------------------------
paper = (f'<ellipse cx="540" cy="1032" rx="250" ry="22" fill="{SHADOW}"/>'
         f'<path d="M270 560 L770 530 L810 930 L300 960 Z" fill="{WHITE}" stroke="{INK}" stroke-width="6"/>')
today = (f'<g transform="rotate(-4 540 745)">' + text("오늘", 540, 800, 170, ORANGE) +
         f'<path d="M380 840 Q540 870 700 830" fill="none" stroke="{ORANGE}" stroke-width="10" stroke-linecap="round"/></g>')
scene("S17", 135, 145, [
    ("bg", bg_cream(), {"type": "none"}),
    ("paper", paper, {"type": "pop", "at": 0.0, "anchor": [540, 745]}),
    ("word", today, {"type": "wipeL", "at": 1.0, "dur": 1.6, "ease": "linear"}),
    ("line1", text("가장 좋은 때는 10년 전", 540, 1160, 66), {"type": "fade", "at": 3.4}),
    ("line2", text("두 번째는 바로 지금", 540, 1275, 90, ORANGE), {"type": "pop", "at": 5.6, "anchor": [540, 1245]}),
])

# S18 구독 CTA ---------------------------------------------------------------------
button = (f'<rect x="290" y="760" width="500" height="170" rx="85" fill="{RED}"/>'
          f'<path d="M405 795 C375 795 368 825 368 850 L360 880 H450 L442 850 C442 825 435 795 405 795 Z M392 890 a13 13 0 0 0 26 0 Z" fill="{WHITE}"/>'
          + text("구독", 600, 878, 92, WHITE))
finger = (f'<path d="M700 905 V1010 C700 1040 740 1060 770 1060 H820 C850 1060 870 1030 870 1000 V960 C870 945 845 940 835 955 '
          f'C835 935 810 930 800 948 C800 930 775 925 765 945 V905 C765 880 700 880 700 905 Z" fill="#f6d2b3" stroke="{INK}" stroke-width="6"/>')
scene("S18", 145, 150, [
    ("bg", bg_cream(), {"type": "none"}),
    ("title", text("더 많은 지식이 궁금하다면", 540, 560, 64), {"type": "pop", "at": 0.0, "anchor": [540, 535]}),
    ("button", button, {"type": "pop", "at": 0.5, "anchor": [540, 845]}),
    ("finger", finger, {"type": "tap", "at": 1.4, "anchor": [785, 980]}),
    ("next", text("다음 편: 72의 법칙 활용법", 540, 1130, 50, MUTED), {"type": "fade", "at": 2.0}),
    ("disclaimer", text("※ 투자 수익은 보장되지 않으며 세금·수수료·물가에 따라 달라집니다", 540, 1290, 26, MUTED), {"type": "fade", "at": 2.2}),
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
    with open(os.path.join(os.path.dirname(OUT), "manifest_s04_s18.json"), "w") as f:
        json.dump(manifest, f, ensure_ascii=False, indent=1)
    print(sum(len(s["parts"]) for s in scenes), "parts in", len(scenes), "scenes")


if __name__ == "__main__":
    main()
