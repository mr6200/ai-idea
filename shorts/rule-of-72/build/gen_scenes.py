"""Generate SVG parts for all 18 scenes of the rule-of-72 Short (1080x1920).

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
LABEL = "지식 쇼츠 · 72의 법칙"

CREAM, GLOW, SHADOW = "#fde9c8", "#fff4e2", "#ecd3aa"
INK, MUTED = "#2b2b2b", "#7a6f63"
ORANGE, GREEN, RED = "#f28c28", "#2f7d6d", "#c8553d"
GOLD, GOLD_D = "#e0b23a", "#b98a1e"
WHITE = "#ffffff"
BILL, BILL_D, BAND = "#9fd3b0", "#2f7d6d", "#f4e6b8"


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


# the cream wash is translucent so compose_bg.py can lay an AI illustration underneath
BG_WASH, GLOW_ALPHA = 0.58, 0.6


def bg_cream(extra=""):
    return (f'<rect x="0" y="0" width="{W}" height="{H}" fill="{CREAM}" fill-opacity="{BG_WASH}"/>'
            f'<circle cx="540" cy="860" r="470" fill="{GLOW}" fill-opacity="{GLOW_ALPHA}"/>'
            + pill(LABEL, 540, 256, 38, ORANGE) + extra)


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




def bill(cx, cy, w, label, fs=None):
    """Banknote bundle: green note with a paper band and the amount on it."""
    h = w * 0.5
    fs = fs or w * 0.17
    x, y = cx - w / 2, cy - h / 2
    return (f'<rect x="{x + 10:.1f}" y="{y + 12:.1f}" width="{w:.1f}" height="{h:.1f}" rx="{w * 0.05:.1f}" fill="{BILL_D}"/>'
            f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" rx="{w * 0.05:.1f}" fill="{BILL}" stroke="{BILL_D}" stroke-width="5"/>'
            f'<circle cx="{cx - w * 0.3:.1f}" cy="{cy:.1f}" r="{h * 0.26:.1f}" fill="none" stroke="{BILL_D}" stroke-width="4"/>'
            f'<rect x="{cx - w * 0.09:.1f}" y="{y:.1f}" width="{w * 0.18:.1f}" height="{h:.1f}" fill="{BAND}"/>'
            + text(label, cx + w * 0.22, cy + fs * 0.36, fs, INK))


def card(x, y, w, h, stroke=None, sw=6, fill=WHITE, rx=32):
    st = f' stroke="{stroke}" stroke-width="{sw}"' if stroke else ""
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{fill}"{st}/>'


def confetti_at(spots):
    cols = [ORANGE, GREEN, RED, GOLD, "#3b82c4"]
    out = ""
    for i, (x, y) in enumerate(spots):
        r = (i * 37) % 180
        out += f'<rect x="{x}" y="{y}" width="22" height="12" rx="3" fill="{cols[i % 5]}" transform="rotate({r} {x + 11} {y + 6})"/>'
    return out


# ---------------------------------------------------------------- scenes
# Each scene: dict(id, start, end, parts=[(name, svg_body, anim)])
# anim: dict(type=pop|fade|slideL|slideR|slideU|growY|wipeL|wipeU|wipeD|drop|stamp|spin|tap, at=seconds
#            from scene start, anchor=[x,y] for pop/growY/spin)
scenes = []


def scene(sid, start, end, parts):
    scenes.append({"id": sid, "start": start, "end": end, "parts": parts})


# S01 1,000만 → 2,000만 ---------------------------------------------------------------
scene("S01", 0, 5, [
    ("bg", bg_cream(), {"type": "none"}),
    ("title", text("1,000만 원이", 540, 470, 84) + text("2,000만 원 되려면?", 540, 590, 84, ORANGE),
     {"type": "pop", "at": 0.0, "anchor": [540, 530]}),
    ("billL", bill(270, 900, 300, "1,000만", 40), {"type": "pop", "at": 0.4, "anchor": [270, 900]}),
    ("arrow", arrow(450, 900, 590, 900, INK, 10), {"type": "wipeL", "at": 1.1, "dur": 0.5}),
    ("billR", bill(820, 960, 300, "", 40) + bill(800, 900, 300, "2,000만", 40), {"type": "pop", "at": 1.6, "anchor": [810, 930]}),
    ("q", pill("몇 년?", 540, 1200, 96, RED), {"type": "stamp", "at": 2.7, "anchor": [540, 1200]}),
])

# S02 연 2% vs 연 8% 레이스 ---------------------------------------------------------
PX = 25.0  # px per year
scene("S02", 5, 10, [
    ("bg", bg_cream(f'<path d="M140 680 V1110" stroke="{INK}" stroke-width="6" stroke-linecap="round"/>'
                    + text("두 배가 될 때까지", 540, 450, 70)), {"type": "none"}),
    ("row1", text("연 2% 예금", 160, 735, 50, MUTED, "start")
     + f'<rect x="140" y="760" width="{35 * PX:.0f}" height="96" rx="18" fill="{GOLD}"/>'
     + text("약 35년", 140 + 35 * PX - 20, 826, 54, WHITE, "end"), {"type": "wipeL", "at": 0.2, "dur": 2.2, "ease": "linear"}),
    ("row2", text("연 8%", 160, 975, 50, MUTED, "start")
     + f'<rect x="140" y="1000" width="{9 * PX:.0f}" height="96" rx="18" fill="{ORANGE}"/>'
     + text("약 9년", 140 + 9 * PX + 24, 1066, 54, ORANGE, "start"), {"type": "wipeL", "at": 2.6, "dur": 0.55, "ease": "linear"}),
    ("badge", pill("26년 차이!", 540, 1270, 64, RED), {"type": "stamp", "at": 3.6, "anchor": [540, 1270]}),
])

# S03 계산기 없이 3초 ------------------------------------------------------------------
calc = (card(170, 650, 260, 360, fill=INK, rx=36) + card(200, 690, 200, 80, fill="#cfe6df", rx=12)
        + "".join(f'<rect x="{205 + c * 52}" y="{800 + r * 52}" width="40" height="40" rx="10" fill="{MUTED if c < 3 else ORANGE}"/>'
                  for r in range(4) for c in range(4)))
xmark = f'<path d="M150 640 L450 1030 M450 640 L150 1030" stroke="{RED}" stroke-width="26" stroke-linecap="round"/>'
SW = (780, 830, 150)
watch = (f'<rect x="{SW[0] - 30}" y="{SW[1] - SW[2] - 60}" width="60" height="44" rx="10" fill="{INK}"/>'
         f'<circle cx="{SW[0]}" cy="{SW[1]}" r="{SW[2]}" fill="{WHITE}" stroke="{INK}" stroke-width="14"/>'
         + "".join(f'<circle cx="{SW[0] + 118 * math.sin(math.radians(a)):.1f}" cy="{SW[1] - 118 * math.cos(math.radians(a)):.1f}" r="7" fill="{INK}"/>'
                   for a in range(0, 360, 30)))
scene("S03", 10, 14, [
    ("bg", bg_cream(), {"type": "none"}),
    ("title", text("계산기 없이", 540, 450, 80) + text("3초 만에", 540, 570, 96, ORANGE), {"type": "pop", "at": 0.0, "anchor": [540, 510]}),
    ("calc", calc, {"type": "pop", "at": 0.3, "anchor": [300, 830]}),
    ("xmark", xmark, {"type": "stamp", "at": 0.9, "anchor": [300, 835]}),
    ("watch", watch, {"type": "pop", "at": 0.6, "anchor": [SW[0], SW[1]]}),
    ("hand", f'<path d="M{SW[0]} {SW[1] + 16} V{SW[1] - 110}" stroke="{ORANGE}" stroke-width="12" stroke-linecap="round"/>'
             f'<circle cx="{SW[0]}" cy="{SW[1]}" r="16" fill="{INK}"/>', {"type": "spin", "at": 0.8, "anchor": [SW[0], SW[1]], "speed": 360}),
])

# S04 공식 ---------------------------------------------------------------------------
scene("S04", 14, 22, [
    ("bg", bg_cream(), {"type": "none"}),
    ("title", text("72의 법칙", 540, 470, 110), {"type": "pop", "at": 0.2, "anchor": [540, 435]}),
    ("num", text("72", 540, 860, 300, ORANGE), {"type": "drop", "at": 3.2}),
    ("line", f'<rect x="300" y="905" width="480" height="16" rx="8" fill="{INK}"/>', {"type": "wipeL", "at": 4.0}),
    ("denom", text("수익률(%)", 540, 1070, 120), {"type": "pop", "at": 4.6, "anchor": [540, 1025]}),
    ("result", pill("= 돈이 두 배 되는 데 걸리는 해", 540, 1250, 50, GREEN), {"type": "pop", "at": 6.0, "anchor": [540, 1250]}),
])

# S05 예시 세 줄 -----------------------------------------------------------------------


def example_row(y, rate, calc_, years):
    return (card(100, y - 75, 880, 150, rx=36) + text(rate, 235, y + 22, 58, ORANGE)
            + text(calc_, 540, y + 24, 70) + text(years, 850, y + 26, 76, GREEN))


scene("S05", 22, 35, [
    ("bg", bg_cream(), {"type": "none"}),
    ("title", text("직접 해 볼까요?", 540, 450, 80), {"type": "pop", "at": 0.0, "anchor": [540, 420]}),
    ("r1", example_row(640, "연 6%", "72 ÷ 6", "12년"), {"type": "slideR", "at": 0.2}),
    ("r2", example_row(840, "연 8%", "72 ÷ 8", "9년"), {"type": "slideR", "at": 3.4}),
    ("r3", example_row(1040, "연 12%", "72 ÷ 12", "6년"), {"type": "slideR", "at": 6.6}),
    ("done", pill("나눗셈 한 번이면 끝!", 540, 1260, 58, INK), {"type": "stamp", "at": 9.8, "anchor": [540, 1260]}),
])

# S06 법칙 vs 실제 --------------------------------------------------------------------
B6, YPX = 1150, 42
G6 = [(250, "6%", 12, 11.9), (540, "8%", 9, 9.0), (830, "12%", 6, 6.1)]
bars_o = "".join(f'<rect x="{x - 108}" y="{B6 - r * YPX}" width="100" height="{r * YPX}" rx="12" fill="{ORANGE}"/>' for x, _, r, _ in G6)
bars_g = "".join(f'<rect x="{x + 8}" y="{B6 - e * YPX:.0f}" width="100" height="{e * YPX:.0f}" rx="12" fill="{GREEN}"/>' for x, _, _, e in G6)
vals_o = "".join(text(f"{r}", x - 58, B6 - r * YPX - 20, 46, ORANGE) for x, _, r, _ in G6)
vals_g = "".join(text(f"{e}", x + 58, B6 - e * YPX - 20, 46, GREEN) for x, _, _, e in G6)
scene("S06", 35, 47, [
    ("bg", bg_cream(f'<path d="M110 {B6} H970" stroke="{INK}" stroke-width="6" stroke-linecap="round"/>'
                    + "".join(text(f"연 {lab}", x, B6 + 64, 46) for x, lab, _, _ in G6)), {"type": "none"}),
    ("title", text("정말 맞을까?", 540, 420, 80), {"type": "pop", "at": 0.0, "anchor": [540, 390]}),
    ("legend", pill("72의 법칙", 345, 530, 40, ORANGE) + pill("실제 계산", 735, 530, 40, GREEN), {"type": "fade", "at": 0.5}),
    ("barsO", bars_o, {"type": "growY", "at": 1.0, "anchor": [540, B6], "dur": 1.0, "ease": "decel"}),
    ("valsO", vals_o, {"type": "fade", "at": 1.9}),
    ("barsG", bars_g, {"type": "growY", "at": 3.4, "anchor": [540, B6], "dur": 1.0, "ease": "decel"}),
    ("valsG", vals_g, {"type": "fade", "at": 4.3}),
    ("badge", pill("오차 두 달 미만", 540, 1295, 56, RED), {"type": "stamp", "at": 7.6, "anchor": [540, 1295]}),
])

# S07 왜 하필 72? ----------------------------------------------------------------------
bubble = (f'<circle cx="420" cy="810" r="14" fill="{WHITE}" stroke="{INK}" stroke-width="4"/>'
          f'<circle cx="455" cy="760" r="24" fill="{WHITE}" stroke="{INK}" stroke-width="4"/>'
          f'<circle cx="515" cy="680" r="56" fill="{WHITE}" stroke="{INK}" stroke-width="5"/>' + text("?", 515, 710, 84, ORANGE))
answer = (card(600, 770, 400, 330, stroke=GREEN, sw=8) + text("수학적 정답", 800, 860, 46, MUTED)
          + text("69.3", 800, 1020, 140, GREEN))
scene("S07", 47, 55, [
    ("bg", bg_cream(), {"type": "none"}),
    ("title", text("왜 하필", 540, 410, 72) + text("72?", 540, 560, 150, ORANGE), {"type": "pop", "at": 0.1, "anchor": [540, 480]}),
    ("person", person(290, 1250, GREEN, s=0.78), {"type": "slideL", "at": 0.5}),
    ("bubble", bubble, {"type": "pop", "at": 1.3, "anchor": [480, 740]}),
    ("answer", answer, {"type": "pop", "at": 3.6, "anchor": [800, 935]}),
])

# S08 ln 2 → 69.3 → 암산? ----------------------------------------------------------------
sweat = "".join(f'<path d="M{x} {y} q-14 26 0 34 q14 -8 0 -34 Z" fill="#6aa6d8"/>' for x, y in ((880, 1080), (920, 1130), (180, 1100)))
scene("S08", 55, 68, [
    ("bg", bg_cream(), {"type": "none"}),
    ("title", text("두 배의 비밀", 540, 430, 80), {"type": "pop", "at": 0.0, "anchor": [540, 400]}),
    ("ln", text("ln 2 ≈ 0.693", 540, 650, 120), {"type": "pop", "at": 1.6, "anchor": [540, 610]}),
    ("to", arrow(540, 700, 540, 790, ORANGE, 8) + text("× 100  →  69.3", 540, 880, 76, ORANGE), {"type": "fade", "at": 2.8}),
    ("q", text("이걸로 암산?", 540, 1030, 56, MUTED), {"type": "fade", "at": 4.6}),
    ("hard", text("69.3 ÷ 7 = ?", 540, 1210, 110, RED), {"type": "stamp", "at": 8.6, "anchor": [540, 1170]}),
    ("sweat", sweat, {"type": "drop", "at": 9.6}),
])

# S09 72의 약수 ----------------------------------------------------------------------
C9, R9 = (540, 800), 285
divs = [1, 2, 3, 4, 6, 8, 9, 12]
s09 = [
    ("bg", bg_cream(), {"type": "none"}),
    ("core", f'<circle cx="{C9[0]}" cy="{C9[1]}" r="150" fill="{ORANGE}"/>' + text("72", C9[0], C9[1] + 54, 150, WHITE),
     {"type": "pop", "at": 0.0, "anchor": list(C9)}),
]
for i, d in enumerate(divs):
    a = math.radians(i * 45)
    x, y = C9[0] + R9 * math.sin(a), C9[1] - R9 * math.cos(a)
    s09.append((f"d{i + 1}", f'<circle cx="{x:.0f}" cy="{y:.0f}" r="62" fill="{WHITE}" stroke="{GREEN}" stroke-width="6"/>'
                + text(str(d), x, y + 22, 62, GREEN), {"type": "pop", "at": 0.5 + i * 0.45, "anchor": [round(x), round(y)]}))
s09 += [
    ("compare", card(130, 1150, 820, 200, stroke=INK, sw=5) + text("수익률 8%면 실제 9.0년", 540, 1218, 44, MUTED)
     + text("72 → 9.0년", 335, 1300, 54, GREEN) + text("69.3 → 8.7년", 745, 1300, 54, MUTED),
     {"type": "pop", "at": 4.4, "anchor": [540, 1250]}),
    ("win", pill("72 승!", 335, 1130, 44, RED), {"type": "stamp", "at": 8.4, "anchor": [335, 1130]}),
]
scene("S09", 68, 80, s09)

# S10 거꾸로 쓰기 ----------------------------------------------------------------------
scene("S10", 80, 90, [
    ("bg", bg_cream(), {"type": "none"}),
    ("title", text("거꾸로도 된다", 540, 420, 84), {"type": "pop", "at": 0.0, "anchor": [540, 390]}),
    ("sub", text("기간을 넣으면 필요한 수익률이 나와요", 540, 510, 42, MUTED), {"type": "fade", "at": 0.8}),
    ("goal", pill("목표 · 10년 안에 2배", 540, 660, 58, INK), {"type": "pop", "at": 3.8, "anchor": [540, 660]}),
    ("formula", text("72 ÷ 10년", 540, 900, 120), {"type": "pop", "at": 5.0, "anchor": [540, 860]}),
    ("result", text("= 7.2%", 540, 1110, 170, ORANGE), {"type": "stamp", "at": 6.8, "anchor": [540, 1050]}),
    ("note", text("필요한 연 수익률", 540, 1220, 46, MUTED), {"type": "fade", "at": 7.4}),
])

# S11 30살 1,000만 원이 9년마다 두 배 --------------------------------------------------
TB = 1200
X11 = [160, 350, 540, 730, 920]
H11 = [37.5, 75, 150, 300, 600]
L11 = ["1천만", "2천만", "4천만", "8천만", "1.6억"]
A11 = ["30살", "39살", "48살", "57살", "66살"]
shades = ["#f8c48a", "#f6b26b", "#f4a04a", "#f28c28", "#e0731a"]
s11 = [
    ("bg", bg_cream(f'<path d="M70 {TB} H1010" stroke="{INK}" stroke-width="6" stroke-linecap="round"/>'
                    + "".join(text(a, x, TB + 62, 42) for x, a in zip(X11, A11))), {"type": "none"}),
    ("header", pill("1,000만 원 · 연 8%", 540, 430, 54, INK), {"type": "pop", "at": 0.0, "anchor": [540, 430]}),
]
for i, (x, h, lab) in enumerate(zip(X11, H11, L11)):
    body = (f'<rect x="{x - 66}" y="{TB - 8 - h}" width="132" height="{h}" rx="14" fill="{shades[i]}"/>'
            + text(lab, x, TB - 8 - h - 24, 50, RED if i == 4 else INK))
    s11.append((f"b{i + 1}", body, {"type": "pop", "at": 0.8 + i * 1.6, "anchor": [x, TB - 8]}))
s11.append(("every", text("9년마다 ×2", 300, 700, 60, ORANGE), {"type": "fade", "at": 4.6}))
scene("S11", 90, 100, s11)

# S12 물가 3% ------------------------------------------------------------------------
scene("S12", 100, 110, [
    ("bg", bg_cream(), {"type": "none"}),
    ("title", text("72의 법칙의", 540, 400, 64) + text("무서운 얼굴", 540, 510, 100, RED), {"type": "pop", "at": 0.0, "anchor": [540, 460]}),
    ("rule", pill("물가 3% → 72 ÷ 3 = 24년", 540, 660, 50, INK), {"type": "pop", "at": 4.2, "anchor": [540, 660]}),
    ("big", bill(290, 900, 380, "1만 원", 52) + text("오늘", 290, 1060, 48, MUTED), {"type": "pop", "at": 4.6, "anchor": [290, 900]}),
    ("arrow", arrow(510, 900, 640, 900, INK, 10), {"type": "wipeL", "at": 5.6, "dur": 0.5}),
    ("small", bill(820, 900, 200, "5천", 30) + text("24년 뒤 가치", 820, 1060, 48, MUTED), {"type": "pop", "at": 6.4, "anchor": [820, 900]}),
    ("half", pill("반토막!", 540, 1220, 80, RED), {"type": "stamp", "at": 7.6, "anchor": [540, 1220]}),
])

# S13 연 18% 빚 ------------------------------------------------------------------------
B13 = 1220
X13 = [180, 360, 540, 720, 900]
V13 = [1000, 1180, 1392, 1643, 1939]
reds = ["#e8a291", "#e08b76", "#d6735c", "#cf6449", "#c8553d"]
s13 = [
    ("bg", bg_cream(f'<path d="M80 {B13} H1000" stroke="{INK}" stroke-width="6" stroke-linecap="round"/>'
                    + "".join(text(a, x, B13 + 62, 42) for x, a in zip(X13, ["지금", "1년", "2년", "3년", "4년"]))), {"type": "none"}),
    ("title", text("연 18% 이자의 빚은?", 540, 420, 76, RED), {"type": "pop", "at": 0.0, "anchor": [540, 395]}),
]
for i, (x, v) in enumerate(zip(X13, V13)):
    h = v * 0.28
    s13.append((f"b{i + 1}", f'<rect x="{x - 62}" y="{B13 - 8 - h:.0f}" width="124" height="{h:.0f}" rx="12" fill="{reds[i]}"/>',
                {"type": "growY", "at": 0.8 + i * 0.6, "anchor": [x, B13 - 8], "dur": 0.5, "ease": "decel"}))
s13 += [
    ("first", text("1,000만", 180, B13 - 8 - 280 - 22, 44), {"type": "fade", "at": 0.9}),
    ("formula", pill("72 ÷ 18 = 4년", 540, 540, 54, INK), {"type": "pop", "at": 4.2, "anchor": [540, 540]}),
    ("double", text("약 2배!", 900, B13 - 8 - 543 - 26, 56, RED), {"type": "stamp", "at": 6.0, "anchor": [900, B13 - 8 - 543 - 45]}),
]
scene("S13", 110, 120, s13)

# S14 보너스 114 · 144 ------------------------------------------------------------------


def rule_row(y, mult, const, color, emph):
    return (card(130, y - 80, 820, 160, stroke=color if emph else None, sw=8, rx=40)
            + text(mult, 270, y + 28, 80, color) + text(f"{const} ÷ 수익률", 650, y + 24, 66))


scene("S14", 120, 128, [
    ("bg", bg_cream(), {"type": "none"}),
    ("badge", pill("보너스!", 540, 430, 70, RED), {"type": "stamp", "at": 0.0, "anchor": [540, 430]}),
    ("x2", rule_row(640, "2배", 72, MUTED, False), {"type": "fade", "at": 0.3}),
    ("x3", rule_row(860, "3배", 114, ORANGE, True), {"type": "pop", "at": 1.4, "anchor": [540, 860]}),
    ("x4", rule_row(1080, "4배", 144, GREEN, True), {"type": "pop", "at": 4.6, "anchor": [540, 1080]}),
    ("note", text("연 8% 근처 기준", 540, 1250, 40, MUTED), {"type": "fade", "at": 5.4}),
])

# S15 정리 ---------------------------------------------------------------------------


def sum_card(y, num, line, color):
    return (card(120, y - 85, 840, 170, rx=40) + f'<circle cx="215" cy="{y}" r="50" fill="{color}"/>'
            + text(num, 215, y + 22, 60, WHITE) + text(line, 300, y + 22, 58, INK, "start"))


scene("S15", 128, 136, [
    ("bg", bg_cream(), {"type": "none"}),
    ("title", text("숫자 72 하나로", 540, 440, 88), {"type": "pop", "at": 0.2, "anchor": [540, 410]}),
    ("c1", sum_card(650, "1", "두 배 걸리는 시간", ORANGE), {"type": "slideR", "at": 3.6}),
    ("c2", sum_card(860, "2", "필요한 수익률", GREEN), {"type": "slideR", "at": 4.8}),
    ("c3", sum_card(1070, "3", "물가와 빚의 무서움", RED), {"type": "slideR", "at": 6.0}),
])

# S16 퀴즈 ---------------------------------------------------------------------------
spots = [(140 + i * 66, 980 + (i % 3) * 14) for i in range(13)] + [(60 + (i % 2) * 22, 820 + i * 50) for i in range(6)] \
    + [(990 + (i % 2) * 22, 820 + i * 50) for i in range(6)]
scene("S16", 136, 142, [
    ("bg", bg_cream(), {"type": "none"}),
    ("badge", pill("퀴즈", 540, 420, 64, ORANGE), {"type": "pop", "at": 0.0, "anchor": [540, 420]}),
    ("question", text("연 9%면 몇 년?", 540, 600, 88), {"type": "pop", "at": 0.3, "anchor": [540, 570]}),
    ("formula", text("72 ÷ 9", 540, 860, 160), {"type": "pop", "at": 1.0, "anchor": [540, 805]}),
    ("answer", pill("= 8년", 540, 1110, 110, GREEN), {"type": "stamp", "at": 2.7, "anchor": [540, 1110]}),
    ("confetti", confetti_at(spots), {"type": "drop", "at": 2.9}),
])

# S17 72를 기억하세요 ---------------------------------------------------------------
note = (f'<g transform="rotate(-5 540 830)"><rect x="300" y="590" width="480" height="480" rx="10" fill="{SHADOW}"/>'
        f'<rect x="285" y="570" width="480" height="480" rx="10" fill="#ffe27a"/>'
        f'<circle cx="525" cy="600" r="18" fill="{RED}"/>' + text("72", 525, 900, 260, ORANGE) + "</g>")
scene("S17", 142, 146, [
    ("bg", bg_cream(), {"type": "none"}),
    ("title", text("오늘부터 기억할 숫자", 540, 440, 70), {"type": "fade", "at": 0.0}),
    ("note", note, {"type": "pop", "at": 0.3, "anchor": [540, 830]}),
    ("tip", text("두 배가 궁금할 땐 72 ÷ 수익률", 540, 1220, 48, MUTED), {"type": "fade", "at": 1.6}),
])

# S18 구독 CTA ---------------------------------------------------------------------
button = (f'<rect x="290" y="760" width="500" height="170" rx="85" fill="{RED}"/>'
          f'<path d="M405 795 C375 795 368 825 368 850 L360 880 H450 L442 850 C442 825 435 795 405 795 Z M392 890 a13 13 0 0 0 26 0 Z" fill="{WHITE}"/>'
          + text("구독", 600, 878, 92, WHITE))
finger = (f'<path d="M700 905 V1010 C700 1040 740 1060 770 1060 H820 C850 1060 870 1030 870 1000 V960 C870 945 845 940 835 955 '
          f'C835 935 810 930 800 948 C800 930 775 925 765 945 V905 C765 880 700 880 700 905 Z" fill="#f6d2b3" stroke="{INK}" stroke-width="6"/>')
scene("S18", 146, 150, [
    ("bg", bg_cream(), {"type": "none"}),
    ("title", text("더 많은 지식이 궁금하다면", 540, 560, 64), {"type": "pop", "at": 0.0, "anchor": [540, 535]}),
    ("button", button, {"type": "pop", "at": 0.4, "anchor": [540, 845]}),
    ("finger", finger, {"type": "tap", "at": 1.2, "anchor": [785, 980]}),
    ("prev", text("지난 편: 복리의 마법", 540, 1130, 50, MUTED), {"type": "fade", "at": 1.6}),
    ("disclaimer", text("※ 투자 수익은 보장되지 않으며 세금·수수료·물가에 따라 달라집니다", 540, 1290, 26, MUTED), {"type": "fade", "at": 1.8}),
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
