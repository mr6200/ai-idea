"""Generate SVG parts for all 18 scenes of the 4%-rule Short (1080x1920).

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
LABEL = "지식 쇼츠 · 4%의 법칙"

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


# S01 은퇴하려면 얼마? ------------------------------------------------------------------
scene("S01", 0, 5, [
    ("bg", bg_cream(), {"type": "none"}),
    ("title", text("은퇴하려면", 540, 450, 84) + text("얼마가 필요할까?", 540, 570, 84, ORANGE),
     {"type": "pop", "at": 0.0, "anchor": [540, 510]}),
    ("person", person(300, 1250, GREEN, s=0.8, glasses=True, hair="#a8a8a8"), {"type": "slideL", "at": 0.3}),
    ("q1", pill("10억?", 760, 800, 80, ORANGE), {"type": "pop", "at": 3.0, "anchor": [760, 800]}),
    ("q2", pill("20억?", 800, 1020, 80, RED), {"type": "pop", "at": 3.8, "anchor": [800, 1020]}),
])

# S02 막연함 → 곱셈 한 번 -------------------------------------------------------------
FOG = [(170, 700, 110), (900, 680, 90), (250, 1080, 80), (860, 1110, 120), (130, 900, 70), (960, 900, 70),
       (380, 650, 60), (700, 1180, 60)]
scene("S02", 5, 10, [
    ("bg", bg_cream(), {"type": "none"}),
    ("title", text("막연한 은퇴 자금", 540, 450, 80), {"type": "pop", "at": 0.0, "anchor": [540, 420]}),
    ("fog", "".join(text("?", x, y, s, MUTED, extra='fill-opacity="0.55"') for x, y, s in FOG), {"type": "fade", "at": 0.2}),
    ("times", f'<circle cx="540" cy="880" r="170" fill="{ORANGE}"/>' + text("×", 540, 955, 240, WHITE),
     {"type": "pop", "at": 2.2, "anchor": [540, 880]}),
    ("once", pill("곱셈 한 번!", 540, 1200, 70, INK), {"type": "stamp", "at": 3.0, "anchor": [540, 1200]}),
])

# S03 4% ---------------------------------------------------------------------------
scene("S03", 10, 14, [
    ("bg", bg_cream(), {"type": "none"}),
    ("title", text("오늘의 숫자", 540, 450, 64, MUTED), {"type": "fade", "at": 0.0}),
    ("four", f'<circle cx="540" cy="830" r="270" fill="{ORANGE}"/>' + text("4%", 540, 910, 240, WHITE),
     {"type": "pop", "at": 0.3, "anchor": [540, 830]}),
    ("name", pill("4%의 법칙", 540, 1230, 70, INK), {"type": "stamp", "at": 1.2, "anchor": [540, 1230]}),
])

# S04 매년 4%만 꺼내 쓰기 ------------------------------------------------------------
jar = (f'<rect x="200" y="600" width="340" height="50" rx="16" fill="{GOLD_D}"/>'
       f'<rect x="170" y="640" width="400" height="540" rx="60" fill="{WHITE}" fill-opacity="0.85" stroke="{INK}" stroke-width="8"/>'
       + stack(370, 1110, 8, rx=130, label="") + pill("은퇴 자금", 370, 760, 46, GREEN))
scene("S04", 14, 22, [
    ("bg", bg_cream(), {"type": "none"}),
    ("title", text("매년 4%만 꺼내 쓰기", 540, 440, 76), {"type": "pop", "at": 0.0, "anchor": [540, 410]}),
    ("jar", jar, {"type": "pop", "at": 0.4, "anchor": [370, 900]}),
    ("out", arrow(590, 830, 720, 830, INK, 10) + coin(850, 830, 100, "4%", 56) + text("매년", 850, 730, 50, MUTED),
     {"type": "slideR", "at": 1.6}),
    ("ok", pill("30년 OK", 820, 1080, 66, GREEN), {"type": "stamp", "at": 4.0, "anchor": [820, 1080]}),
])

# S05 4% = 1/25 → 생활비 × 25 --------------------------------------------------------
scene("S05", 22, 30, [
    ("bg", bg_cream(), {"type": "none"}),
    ("title", text("거꾸로 뒤집으면", 540, 450, 84), {"type": "pop", "at": 0.2, "anchor": [540, 420]}),
    ("frac", text("4% = 1/25", 540, 780, 150), {"type": "pop", "at": 2.2, "anchor": [540, 730]}),
    ("result", card(80, 960, 920, 300, stroke=ORANGE, sw=8, rx=44) + text("필요한 돈", 540, 1050, 52, MUTED)
     + text("1년 생활비 × 25", 540, 1190, 100, ORANGE), {"type": "stamp", "at": 4.8, "anchor": [540, 1110]}),
])

# S06 월 300만 원 → 9억 ---------------------------------------------------------------
scene("S06", 30, 42, [
    ("bg", bg_cream(), {"type": "none"}),
    ("title", text("내 숫자로 계산", 540, 440, 84), {"type": "pop", "at": 0.0, "anchor": [540, 410]}),
    ("r1", card(100, 550, 880, 150, rx=36) + text("한 달 생활비", 160, 645, 46, MUTED, "start") + text("300만 원", 920, 650, 72, INK, "end"),
     {"type": "slideR", "at": 0.2}),
    ("r2", card(100, 730, 880, 150, rx=36) + text("× 12", 160, 828, 60, MUTED, "start") + text("연 3,600만 원", 920, 830, 72, INK, "end"),
     {"type": "slideR", "at": 3.2}),
    ("r3", card(100, 910, 880, 200, stroke=ORANGE, sw=8, rx=40) + text("× 25", 160, 1030, 64, ORANGE, "start")
     + text("9억 원", 920, 1045, 120, ORANGE, "end"), {"type": "stamp", "at": 5.8, "anchor": [540, 1010]}),
    ("goal", pill("목표 금액!", 540, 1250, 64, RED), {"type": "stamp", "at": 9.2, "anchor": [540, 1250]}),
])

# S07 생활비별 목표 금액 -------------------------------------------------------------
B7, U7 = 1200, 50  # baseline, px per 억
G7 = [(250, "월 200만", 6), (540, "월 300만", 9), (830, "월 400만", 12)]
s07 = [
    ("bg", bg_cream(f'<path d="M110 {B7} H970" stroke="{INK}" stroke-width="6" stroke-linecap="round"/>'
                    + "".join(text(lab, x, B7 + 64, 46) for x, lab, _ in G7)), {"type": "none"}),
    ("title", text("생활비별 목표 금액", 540, 430, 76), {"type": "pop", "at": 0.0, "anchor": [540, 400]}),
]
for i, ((x, _, v), at, col) in enumerate(zip(G7, (0.4, 1.8, 3.6), ("#f8c48a", ORANGE, "#e0731a"))):
    s07.append((f"b{i + 1}", f'<rect x="{x - 90}" y="{B7 - 8 - v * U7}" width="180" height="{v * U7}" rx="16" fill="{col}"/>'
                + text(f"{v}억", x, B7 - 8 - v * U7 - 26, 64, INK if i != 2 else RED),
                {"type": "growY", "at": at, "anchor": [x, B7 - 8], "dur": 0.7, "ease": "decel"}))
scene("S07", 42, 50, s07)

# S08 국민연금이 있다면 --------------------------------------------------------------
scene("S08", 50, 58, [
    ("bg", bg_cream(text("필요한 생활비 · 월 300만 원", 540, 640, 46, MUTED)
                    + f'<rect x="120" y="680" width="840" height="150" rx="24" fill="{WHITE}" stroke="{INK}" stroke-width="5"/>'),
     {"type": "none"}),
    ("title", text("국민연금이 있다면", 540, 440, 80), {"type": "pop", "at": 0.0, "anchor": [540, 410]}),
    ("pension", f'<rect x="126" y="686" width="274" height="138" rx="20" fill="{GREEN}"/>' + text("연금 100만", 263, 772, 46, WHITE),
     {"type": "wipeL", "at": 1.2, "dur": 0.6}),
    ("mine", f'<rect x="406" y="686" width="548" height="138" rx="20" fill="{ORANGE}"/>' + text("내 돈 200만", 680, 772, 52, WHITE),
     {"type": "wipeL", "at": 3.6, "dur": 0.8}),
    ("formula", text("200만 × 12 × 25", 540, 1010, 80) + text("= 6억", 540, 1180, 140, ORANGE),
     {"type": "stamp", "at": 6.0, "anchor": [540, 1080]}),
])

# S09 벤겐 1994 · 트리니티 1998 -------------------------------------------------------


def source_card(y, year, color, name, sub, name_size=60):
    return (card(90, y, 900, 250, stroke=color, sw=6, rx=40) + text(year, 245, y + 158, 96, color)
            + text(name, 420, y + 115, name_size, INK, "start") + text(sub, 420, y + 185, 40, MUTED, "start"))


scene("S09", 58, 69, [
    ("bg", bg_cream(), {"type": "none"}),
    ("title", text("어디서 나온 숫자?", 540, 440, 80), {"type": "pop", "at": 0.0, "anchor": [540, 410]}),
    ("c1", source_card(600, "1994", ORANGE, "윌리엄 벤겐", "미국 재무설계사 · 처음 제안"), {"type": "slideL", "at": 3.0}),
    ("c2", source_card(900, "1998", GREEN, "트리니티 대학 연구", "Cooley · Hubbard · Walz", 54), {"type": "slideR", "at": 7.4}),
])

# S10 실험 방법 -----------------------------------------------------------------------
pie = (f'<path d="M230 620 A62 62 0 0 1 230 744 Z" fill="{ORANGE}"/><path d="M230 744 A62 62 0 0 1 230 620 Z" fill="{GREEN}"/>')


def step(y, icon, line):
    return card(90, y - 95, 900, 190, rx=40) + icon + text(line, 340, y + 20, 58, INK, "start")


up = (f'<path d="M230 1150 V1050 M190 1090 L230 1046 L270 1090" fill="none" stroke="{RED}" stroke-width="16" '
      f'stroke-linecap="round" stroke-linejoin="round"/>')
scene("S10", 69, 80, [
    ("bg", bg_cream(), {"type": "none"}),
    ("header", pill("1926–1995 · 미국 70년 데이터", 540, 440, 50, INK), {"type": "pop", "at": 0.2, "anchor": [540, 440]}),
    ("s1", step(682, pie, "주식 50 : 채권 50"), {"type": "slideR", "at": 4.0}),
    ("s2", step(892, coin(230, 892, 80, "4%", 44), "첫해 4% 꺼내기"), {"type": "slideR", "at": 5.6}),
    ("s3", step(1102, up, "매년 물가만큼 늘리기"), {"type": "slideR", "at": 7.6}),
])

# S11 95% -----------------------------------------------------------------------------
C11, R11 = (540, 840), 250
a11 = math.radians(360 * 0.95)
arc = (f'<path d="M{C11[0]} {C11[1] - R11} A{R11} {R11} 0 1 1 {C11[0] + R11 * math.sin(a11):.1f} {C11[1] - R11 * math.cos(a11):.1f}" '
       f'fill="none" stroke="{GREEN}" stroke-width="64" stroke-linecap="round"/>')
scene("S11", 80, 90, [
    ("bg", bg_cream(f'<circle cx="{C11[0]}" cy="{C11[1]}" r="{R11}" fill="none" stroke="{SHADOW}" stroke-width="64"/>'), {"type": "none"}),
    ("title", text("30년 버틴 비율", 540, 440, 80), {"type": "pop", "at": 0.2, "anchor": [540, 410]}),
    ("arc", arc, {"type": "pop", "at": 0.8, "anchor": list(C11)}),
    ("pct", text("95%", 540, 905, 180, GREEN), {"type": "stamp", "at": 2.4, "anchor": [540, 840]}),
    ("why", pill("꺼내는 동안에도 계속 굴러가요", 540, 1230, 46, ORANGE), {"type": "fade", "at": 4.8}),
])

# S12 순서 위험 --------------------------------------------------------------------
from verify_numbers import SEQ, balances  # noqa: E402

B12, X0, XS, YS = 1200, 130, 27, 36  # baseline, x of year 0, px per year, px per 억


def curve(vals, color):
    pts = [(X0 + i * XS, B12 - v / 10000 * YS) for i, v in enumerate(vals)]
    if 0 in vals:
        pts = pts[:vals.index(0) + 1]
    return f'<path d="{poly(pts)}" fill="none" stroke="{color}" stroke-width="12" stroke-linecap="round" stroke-linejoin="round"/>'


good, bad = balances(SEQ[::-1]), balances(SEQ)
scene("S12", 90, 100, [
    ("bg", bg_cream(f'<path d="M{X0} 640 V{B12} H{X0 + 30 * XS + 20}" fill="none" stroke="{INK}" stroke-width="6" stroke-linecap="round"/>'
                    + "".join(text(f"{y}년", X0 + y * XS, B12 + 60, 40) for y in (0, 10, 20, 30))
                    + text("잔액", X0 + 10, 620, 36, MUTED, "start")), {"type": "none"}),
    ("title", text("주의 ① 은퇴 직후 폭락", 540, 430, 72, RED), {"type": "pop", "at": 0.2, "anchor": [540, 400]}),
    ("good", curve(good, GREEN) + text("좋은 순서", X0 + 11 * XS, 655, 42, GREEN),
     {"type": "wipeL", "at": 2.2, "dur": 1.4, "ease": "linear"}),
    ("bad", curve(bad, RED) + text("나쁜 순서", X0 + 6 * XS, 1110, 42, RED),
     {"type": "wipeL", "at": 4.0, "dur": 1.4, "ease": "linear"}),
    ("note", text("같은 30년 수익률, 순서만 반대 (예시)", 540, 530, 36, MUTED), {"type": "fade", "at": 5.4}),
    ("zero", pill("20년 만에 0원", 720, 1070, 42, RED), {"type": "stamp", "at": 7.0, "anchor": [720, 1070]}),
])

# S13 30년 기준 ----------------------------------------------------------------------
XU = 17  # px per year
scene("S13", 100, 110, [
    ("bg", bg_cream(text("60세 은퇴", 120, 660, 46, MUTED, "start") + text("40대 은퇴", 120, 900, 46, MUTED, "start")), {"type": "none"}),
    ("title", text("주의 ② 30년 기준", 540, 440, 80, RED), {"type": "pop", "at": 0.2, "anchor": [540, 410]}),
    ("r30", f'<rect x="120" y="690" width="{30 * XU}" height="110" rx="24" fill="{GREEN}"/>' + text("30년 · 4%", 120 + 15 * XU, 763, 52, WHITE),
     {"type": "wipeL", "at": 0.4, "dur": 0.8}),
    ("r50", f'<rect x="120" y="930" width="{50 * XU}" height="110" rx="24" fill="{ORANGE}"/>' + text("50년 · ?", 120 + 25 * XU, 1003, 52, WHITE),
     {"type": "wipeL", "at": 2.8, "dur": 1.2}),
    ("lower", pill("3~3.5%로 낮추기", 540, 1210, 64, RED), {"type": "stamp", "at": 6.4, "anchor": [540, 1210]}),
])

# S14 3%면 × 33 ----------------------------------------------------------------------
B14, U14 = 1200, 45
scene("S14", 110, 117, [
    ("bg", bg_cream(f'<path d="M150 {B14} H930" stroke="{INK}" stroke-width="6" stroke-linecap="round"/>'
                    + text("4% 기준", 360, B14 + 62, 46) + text("3% 기준", 720, B14 + 62, 46)), {"type": "none"}),
    ("title", text("3%면 × 33", 540, 470, 110, ORANGE), {"type": "pop", "at": 0.2, "anchor": [540, 430]}),
    ("b4", f'<rect x="270" y="{B14 - 8 - 9 * U14}" width="180" height="{9 * U14}" rx="16" fill="{GREEN}"/>'
           + text("9억", 360, B14 - 8 - 9 * U14 - 26, 64), {"type": "growY", "at": 3.0, "anchor": [360, B14 - 8], "dur": 0.6, "ease": "decel"}),
    ("b3", f'<rect x="630" y="{B14 - 8 - 12 * U14}" width="180" height="{12 * U14}" rx="16" fill="{ORANGE}"/>'
           + text("12억", 720, B14 - 8 - 12 * U14 - 26, 64, RED), {"type": "growY", "at": 3.6, "anchor": [720, B14 - 8], "dur": 0.6, "ease": "decel"}),
    ("more", pill("+3억", 520, 580, 50, RED), {"type": "stamp", "at": 4.6, "anchor": [520, 580]}),
])

# S15 수수료 · 세금 · 한국 시장 ------------------------------------------------------


def check_card(y, line):
    return (card(110, y - 75, 860, 150, rx=36) + f'<circle cx="200" cy="{y}" r="44" fill="{ORANGE}"/>'
            f'<path d="M178 {y} L195 {y + 18} L224 {y - 16}" fill="none" stroke="{WHITE}" stroke-width="10" stroke-linecap="round" stroke-linejoin="round"/>'
            + text(line, 280, y + 20, 56, INK, "start"))


scene("S15", 117, 128, [
    ("bg", bg_cream(), {"type": "none"}),
    ("title", text("이것도 기억하세요", 540, 440, 80), {"type": "pop", "at": 0.2, "anchor": [540, 410]}),
    ("k1", check_card(620, "수수료"), {"type": "slideR", "at": 0.4}),
    ("k2", check_card(810, "세금"), {"type": "slideR", "at": 1.8}),
    ("k3", check_card(1000, "한국 시장은 미국과 달라요"), {"type": "slideR", "at": 3.0}),
    ("start", pill("4%는 출발점!", 540, 1220, 66, GREEN), {"type": "stamp", "at": 6.2, "anchor": [540, 1220]}),
])

# S16 정리 ---------------------------------------------------------------------------
scene("S16", 128, 136, [
    ("bg", bg_cream(), {"type": "none"}),
    ("badge", pill("정리", 540, 430, 64, ORANGE), {"type": "pop", "at": 0.0, "anchor": [540, 430]}),
    ("main", card(80, 560, 920, 320, stroke=ORANGE, sw=8, rx=44) + text("은퇴 자금", 540, 660, 56, MUTED)
     + text("1년 생활비 × 25", 540, 800, 100, ORANGE), {"type": "pop", "at": 0.4, "anchor": [540, 720]}),
    ("long", card(160, 940, 760, 260, rx=44) + text("오래 버티려면", 540, 1030, 50, MUTED) + text("× 33", 540, 1160, 120, GREEN),
     {"type": "pop", "at": 4.0, "anchor": [540, 1070]}),
])

# S17 퀴즈 ---------------------------------------------------------------------------
spots = [(140 + i * 66, 1010 + (i % 3) * 14) for i in range(13)] + [(60 + (i % 2) * 22, 820 + i * 50) for i in range(6)] \
    + [(990 + (i % 2) * 22, 820 + i * 50) for i in range(6)]
scene("S17", 136, 146, [
    ("bg", bg_cream(), {"type": "none"}),
    ("badge", pill("퀴즈", 540, 420, 64, ORANGE), {"type": "pop", "at": 0.0, "anchor": [540, 420]}),
    ("question", text("월 250만 원이면?", 540, 600, 88), {"type": "pop", "at": 0.3, "anchor": [540, 570]}),
    ("formula", text("3,000만 × 25", 540, 810, 110), {"type": "pop", "at": 1.4, "anchor": [540, 770]}),
    ("answer", pill("= 7억 5천만 원", 540, 1060, 90, GREEN), {"type": "stamp", "at": 2.7, "anchor": [540, 1060]}),
    ("confetti", confetti_at(spots), {"type": "drop", "at": 2.9}),
    ("tip", text("내 생활비로 계산해 보세요", 540, 1250, 48, MUTED), {"type": "fade", "at": 6.2}),
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
    ("prev", text("지난 편: 72의 법칙", 540, 1130, 50, MUTED), {"type": "fade", "at": 1.6}),
    ("disclaimer", text("※ 과거 미국 데이터에 기반한 경험칙이며 미래 수익을 보장하지 않습니다", 540, 1290, 26, MUTED), {"type": "fade", "at": 1.8}),
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
