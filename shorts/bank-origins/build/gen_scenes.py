"""Generate SVG parts for all 18 scenes of the bank-origins Short (1080x1920).

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
LABEL = "지식 쇼츠 · 은행의 탄생"

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


SAND, STONE, BROWN = "#e9c98f", "#c9b18a", "#8a5a3b"


def bank(cx, base, s=1.0):
    def p(v):
        return v * s
    cols = "".join(f'<rect x="{cx + p(dx) - p(18):.0f}" y="{base - p(200):.0f}" width="{p(36):.0f}" height="{p(170):.0f}" fill="{WHITE}" stroke="{INK}" stroke-width="5"/>'
                   for dx in (-120, -40, 40, 120))
    return (f'<path d="M{cx - p(190):.0f} {base - p(210):.0f} L{cx:.0f} {base - p(320):.0f} L{cx + p(190):.0f} {base - p(210):.0f} Z" fill="{GREEN}" stroke="{INK}" stroke-width="6" stroke-linejoin="round"/>'
            + cols + f'<rect x="{cx - p(200):.0f}" y="{base - p(30):.0f}" width="{p(400):.0f}" height="{p(30):.0f}" fill="{INK}"/>')


def sack(cx, base, s=1.0, label=""):
    w, h = 150 * s, 170 * s
    out = (f'<path d="M{cx - w / 2:.0f} {base:.0f} Q{cx - w / 2 - 10 * s:.0f} {base - h * 0.6:.0f} {cx - w * 0.25:.0f} {base - h:.0f} '
           f'L{cx + w * 0.25:.0f} {base - h:.0f} Q{cx + w / 2 + 10 * s:.0f} {base - h * 0.6:.0f} {cx + w / 2:.0f} {base:.0f} Z" fill="{SAND}" stroke="{BROWN}" stroke-width="5"/>'
           f'<path d="M{cx - w * 0.3:.0f} {base - h + 12 * s:.0f} H{cx + w * 0.3:.0f}" stroke="{BROWN}" stroke-width="7"/>')
    return out + (text(label, cx, base - h * 0.35, 34 * s, BROWN) if label else "")


def table(cx, top, w=420):
    return (f'<rect x="{cx - w / 2}" y="{top}" width="{w}" height="34" rx="10" fill="{BROWN}"/>'
            f'<rect x="{cx - w / 2 + 30}" y="{top + 34}" width="26" height="150" fill="{BROWN}"/>'
            f'<rect x="{cx + w / 2 - 56}" y="{top + 34}" width="26" height="150" fill="{BROWN}"/>')


def ziggurat(cx, base):
    out = ""
    for i, (w, h) in enumerate(((560, 90), (430, 90), (300, 90), (170, 80))):
        y = base - (i + 1) * 90
        out += f'<rect x="{cx - w / 2}" y="{y}" width="{w}" height="{h + 2}" fill="{STONE}" stroke="{BROWN}" stroke-width="5"/>'
    return out + f'<rect x="{cx - 30}" y="{base - 270}" width="60" height="270" fill="{SAND}" stroke="{BROWN}" stroke-width="4"/>'


def tablet(cx, cy, w=300, h=380):
    marks = ""
    for r in range(6):
        for c in range(5):
            x, y = cx - w / 2 + 50 + c * 50, cy - h / 2 + 60 + r * 52
            marks += f'<path d="M{x} {y} l18 8 l-18 8 Z" fill="{BROWN}"/>'
    return f'<rect x="{cx - w / 2}" y="{cy - h / 2}" width="{w}" height="{h}" rx="40" fill="{STONE}" stroke="{BROWN}" stroke-width="6"/>' + marks


def columns(cx, base, n=4, gap=150):
    out = f'<path d="M{cx - gap * n / 2 - 40} {base - 330} L{cx} {base - 420} L{cx + gap * n / 2 + 40} {base - 330} Z" fill="{WHITE}" stroke="{INK}" stroke-width="5"/>'
    for i in range(n):
        x = cx - gap * (n - 1) / 2 + i * gap
        out += f'<rect x="{x - 26}" y="{base - 320}" width="52" height="300" fill="{WHITE}" stroke="{INK}" stroke-width="5"/>'
    return out + f'<rect x="{cx - gap * n / 2 - 50}" y="{base - 22}" width="{gap * n + 100}" height="22" fill="{INK}"/>'


def gold_bar(x, y, w=120):
    return (f'<path d="M{x} {y} L{x + w} {y} L{x + w - 20} {y - 46} L{x + 20} {y - 46} Z" fill="{GOLD}" stroke="{GOLD_D}" stroke-width="4"/>')


def receipt(cx, cy, w=260, label="보관증"):
    h = w * 0.62
    return (f'<rect x="{cx - w / 2}" y="{cy - h / 2}" width="{w}" height="{h}" rx="12" fill="#fff7e6" stroke="{BROWN}" stroke-width="5"/>'
            + text(label, cx, cy - h / 2 + 52, 40, BROWN)
            + f'<path d="M{cx - w / 2 + 30} {cy + 8} H{cx + w / 2 - 30} M{cx - w / 2 + 30} {cy + 40} H{cx + w / 4}" stroke="{MUTED}" stroke-width="5"/>')


# S01 은행은 처음부터? ------------------------------------------------------------------
scene("S01", 0, 5, [
    ("bg", bg_cream(), {"type": "none"}),
    ("title", text("은행은 처음부터", 540, 450, 84) + text("있었을까?", 540, 570, 96, ORANGE), {"type": "pop", "at": 0.0, "anchor": [540, 510]}),
    ("bank", bank(330, 1050, 0.9) + text("?", 330, 720, 120, RED), {"type": "pop", "at": 0.4, "anchor": [330, 900]}),
    ("grain", sack(720, 1060, 1.1) + sack(860, 1060, 0.9) + pill("곡식 창고!", 790, 1170, 52, BROWN), {"type": "pop", "at": 2.6, "anchor": [790, 980]}),
])

# S02 4천 년 연표 ---------------------------------------------------------------------
MS = [(170, "4천 년 전", "메소포타미아"), (400, "고대", "그리스"), (630, "중세", "이탈리아"), (880, "17세기", "런던")]
tl = f'<path d="M110 880 H980" stroke="{INK}" stroke-width="8" stroke-linecap="round"/>' + arrow(940, 880, 990, 880, INK, 8)
for x, a, b in MS:
    tl += f'<circle cx="{x}" cy="880" r="26" fill="{ORANGE}"/>' + text(a, x, 820, 40, MUTED) + text(b, x, 970, 42)
scene("S02", 5, 9, [
    ("bg", bg_cream(), {"type": "none"}),
    ("title", text("은행이 생기기까지", 540, 450, 80) + text("4천 년", 540, 620, 130, ORANGE), {"type": "pop", "at": 0.0, "anchor": [540, 540]}),
    ("line", tl, {"type": "wipeL", "at": 0.8, "dur": 2.0, "ease": "linear"}),
])

# S03 메소포타미아 신전 -------------------------------------------------------------------
scene("S03", 9, 16, [
    ("bg", bg_cream(), {"type": "none"}),
    ("title", pill("약 4천 년 전 · 메소포타미아", 540, 440, 50, INK), {"type": "pop", "at": 0.0, "anchor": [540, 440]}),
    ("temple", ziggurat(540, 1000) + text("신전", 540, 1060, 48, BROWN), {"type": "pop", "at": 0.4, "anchor": [540, 820]}),
    ("goods", sack(220, 1180, 0.9, "곡식") + coin(860, 1150, 90) + coin(860, 1110, 90, "은", 44), {"type": "drop", "at": 3.6}),
])

# S04 점토판 + 빌려주기 ------------------------------------------------------------------
scene("S04", 16, 23, [
    ("bg", bg_cream(), {"type": "none"}),
    ("tablet", tablet(300, 800) + text("점토판 기록", 300, 1050, 46, BROWN), {"type": "pop", "at": 0.2, "anchor": [300, 800]}),
    ("lend", sack(800, 760, 0.9) + arrow(800, 790, 800, 930, ORANGE, 10) + person(800, 1250, GREEN, s=0.5) + text("농부에게 빌려주기", 800, 1310, 42, ORANGE),
     {"type": "slideR", "at": 3.4}),
    ("title", text("맡기고, 빌려주고", 540, 450, 80), {"type": "fade", "at": 0.0}),
])

# S05 이자 + 함무라비 법전 -----------------------------------------------------------------
stele = (f'<path d="M560 1220 V720 Q560 560 720 560 Q880 560 880 720 V1220 Z" fill="#4a4a4a"/>'
         + "".join(f'<path d="M600 {760 + i * 46} H840" stroke="#8c8c8c" stroke-width="6"/>' for i in range(9))
         + text("함무라비 법전", 720, 1290, 44, INK))
scene("S05", 23, 29, [
    ("bg", bg_cream(), {"type": "none"}),
    ("interest", sack(260, 900, 1.0) + text("+", 260, 1000, 80, ORANGE) + sack(260, 1170, 0.6) + text("이자", 380, 1110, 46, ORANGE),
     {"type": "pop", "at": 0.2, "anchor": [260, 900]}),
    ("stele", stele, {"type": "slideR", "at": 2.8}),
    ("cap", pill("이자 상한!", 720, 640, 56, RED), {"type": "stamp", "at": 4.4, "anchor": [720, 640]}),
    ("title", text("갚을 땐 이자를", 540, 450, 80), {"type": "fade", "at": 0.0}),
])

# S06 고대 그리스 --------------------------------------------------------------------
scene("S06", 29, 36, [
    ("bg", bg_cream(columns(540, 1000)), {"type": "none"}),
    ("title", pill("고대 그리스", 540, 440, 60, INK), {"type": "pop", "at": 0.0, "anchor": [540, 440]}),
    ("coins", coin(400, 1150, 80, "동전", 34) + coin(560, 1170, 80) + coin(700, 1140, 80), {"type": "drop", "at": 0.6}),
    ("changer", pill("탁자에 앉은 환전상", 540, 1280, 52, ORANGE), {"type": "pop", "at": 3.4, "anchor": [540, 1280]}),
])

# S07 환전상: 맡아 주기, 빌려주기 -----------------------------------------------------------
scene("S07", 36, 42, [
    ("bg", bg_cream(table(540, 980, 560) + person(540, 990, ORANGE, s=0.6)), {"type": "none"}),
    ("title", text("트라페지테스", 540, 440, 80, ORANGE) + text("'탁자의 은행가'", 540, 530, 48, MUTED), {"type": "pop", "at": 0.0, "anchor": [540, 480]}),
    ("keep", pill("맡아 주기", 300, 700, 54, GREEN), {"type": "pop", "at": 0.2, "anchor": [300, 700]}),
    ("lend", pill("빌려주기", 780, 700, 54, GREEN), {"type": "pop", "at": 2.8, "anchor": [780, 700]}),
    ("coins", coin(400, 960, 60) + coin(680, 960, 60), {"type": "fade", "at": 0.4}),
])

# S08 중세 이탈리아: banco --------------------------------------------------------------
scene("S08", 42, 49, [
    ("bg", bg_cream(table(540, 960, 600)), {"type": "none"}),
    ("title", pill("중세 이탈리아", 540, 440, 60, INK), {"type": "pop", "at": 0.0, "anchor": [540, 440]}),
    ("coins", coin(400, 940, 70) + coin(540, 930, 70) + coin(680, 940, 70), {"type": "drop", "at": 0.6}),
    ("banco", pill("탁자 = banco", 540, 1260, 70, ORANGE), {"type": "stamp", "at": 3.6, "anchor": [540, 1260]}),
    ("say", text("방코", 540, 720, 110, BROWN), {"type": "pop", "at": 4.0, "anchor": [540, 680]}),
])

# S09 banco → bank → 은행 -----------------------------------------------------------------
scene("S09", 49, 55, [
    ("bg", bg_cream(), {"type": "none"}),
    ("w1", text("banco", 540, 640, 120, BROWN) + text("이탈리아어 · 탁자", 540, 710, 40, MUTED), {"type": "pop", "at": 0.0, "anchor": [540, 600]}),
    ("a1", arrow(540, 760, 540, 840, INK, 10), {"type": "fade", "at": 0.6}),
    ("w2", text("bank", 540, 980, 140, ORANGE), {"type": "pop", "at": 0.8, "anchor": [540, 930]}),
    ("a2", arrow(540, 1030, 540, 1110, INK, 10), {"type": "fade", "at": 2.8}),
    ("w3", pill("은행의 이름 = 탁자", 540, 1220, 64, GREEN), {"type": "stamp", "at": 3.0, "anchor": [540, 1220]}),
])

# S10 1397 메디치 + 어음 ----------------------------------------------------------------


def city(cx, base, name):
    out = ""
    for i, (dx, h) in enumerate(((-60, 140), (0, 200), (60, 120))):
        out += f'<rect x="{cx + dx - 28}" y="{base - h}" width="56" height="{h}" fill="{STONE}" stroke="{BROWN}" stroke-width="4"/>'
    return out + text(name, cx, base + 50, 42, INK)


scene("S10", 55, 62, [
    ("bg", bg_cream(city(220, 1150, "피렌체") + city(860, 1150, "먼 도시")), {"type": "none"}),
    ("title", text("1397년 피렌체", 540, 450, 80) + text("메디치 은행", 540, 570, 96, GREEN), {"type": "pop", "at": 0.0, "anchor": [540, 510]}),
    ("path", f'<path d="M260 920 Q540 700 820 920" fill="none" stroke="{MUTED}" stroke-width="6" stroke-dasharray="20 16"/>',
     {"type": "wipeL", "at": 3.4, "dur": 1.0}),
    ("note", receipt(540, 820, 200, "어음"), {"type": "pop", "at": 3.8, "anchor": [540, 820]}),
    ("noload", pill("동전 대신 종이 한 장", 540, 1290, 50, ORANGE), {"type": "fade", "at": 5.0}),
])

# S11 1472 몬테 데이 파스키 ----------------------------------------------------------------
scene("S11", 62, 68, [
    ("bg", bg_cream(), {"type": "none"}),
    ("card", card(90, 400, 900, 520, stroke=GREEN, sw=8, rx=44) + text("1472년", 540, 540, 110, GREEN)
     + text("몬테 데이 파스키", 540, 680, 72) + text("디 시에나 (이탈리아)", 540, 770, 50, MUTED),
     {"type": "pop", "at": 0.2, "anchor": [540, 660]}),
    ("open", pill("지금도 영업 중", 540, 1030, 64, ORANGE), {"type": "stamp", "at": 3.0, "anchor": [540, 1030]}),
    ("oldest", text("가장 오래된 은행", 540, 1200, 80, INK), {"type": "pop", "at": 3.8, "anchor": [540, 1170]}),
])

# S12 17세기 런던 금세공업자 금고 ------------------------------------------------------------
safe = (f'<rect x="120" y="640" width="440" height="520" rx="30" fill="#5d6470" stroke="{INK}" stroke-width="8"/>'
        f'<rect x="160" y="680" width="360" height="440" rx="20" fill="#3e444d"/>'
        + gold_bar(190, 1100) + gold_bar(330, 1100) + gold_bar(260, 1050) + gold_bar(190, 1000) + gold_bar(330, 1000))
scene("S12", 68, 75, [
    ("bg", bg_cream(), {"type": "none"}),
    ("title", pill("17세기 런던", 540, 440, 60, INK), {"type": "pop", "at": 0.0, "anchor": [540, 440]}),
    ("safe", safe + text("금세공업자 금고", 340, 1220, 44, INK), {"type": "pop", "at": 0.4, "anchor": [340, 900]}),
    ("receipt", receipt(800, 880, 320), {"type": "slideR", "at": 3.4}),
])

# S13 보관증을 돈처럼 ---------------------------------------------------------------------
scene("S13", 75, 81, [
    ("bg", bg_cream(person(230, 1220, GREEN, s=0.6) + person(850, 1220, ORANGE, s=0.6)), {"type": "none"}),
    ("title", text("보관증을 돈처럼", 540, 450, 84), {"type": "pop", "at": 0.0, "anchor": [540, 420]}),
    ("pass", receipt(540, 800, 260) + arrow(380, 940, 700, 940, INK, 8), {"type": "slideL", "at": 2.8}),
    ("instead", pill("금 대신 종이로 거래", 540, 1300, 52, ORANGE), {"type": "fade", "at": 3.6}),
])

# S14 지폐 탄생 ---------------------------------------------------------------------------
scene("S14", 81, 87, [
    ("bg", bg_cream(), {"type": "none"}),
    ("note", bill(540, 800, 600, "", 60), {"type": "pop", "at": 0.0, "anchor": [540, 800]}),
    ("born", pill("지폐 탄생!", 540, 560, 80, RED), {"type": "stamp", "at": 0.6, "anchor": [540, 560]}),
    ("sweden", card(140, 1040, 800, 200, rx=40) + text("1661년 스웨덴", 540, 1120, 56, GREEN) + text("유럽 첫 은행권", 540, 1200, 52),
     {"type": "slideR", "at": 2.8}),
])

# S15 맡은 돈 일부를 빌려주기 ---------------------------------------------------------------
vault = (f'<rect x="120" y="620" width="480" height="560" rx="30" fill="#5d6470" stroke="{INK}" stroke-width="8"/>'
         f'<rect x="160" y="660" width="400" height="480" rx="20" fill="#3e444d"/>'
         + "".join(gold_bar(190 + (i % 3) * 130, 1120 - (i // 3) * 56) for i in range(9)))
scene("S15", 87, 94, [
    ("bg", bg_cream(vault), {"type": "none"}),
    ("title", text("다 찾으러 오진 않네?", 540, 450, 76), {"type": "pop", "at": 0.0, "anchor": [540, 420]}),
    ("out", gold_bar(700, 880) + gold_bar(760, 830) + arrow(620, 900, 690, 900, ORANGE, 10) + text("빌려주기", 820, 960, 50, ORANGE),
     {"type": "slideR", "at": 3.4}),
    ("interest", pill("+ 이자", 820, 1080, 56, GREEN), {"type": "stamp", "at": 5.4, "anchor": [820, 1080]}),
])

# S16 정리: 은행이 하는 일 다섯 가지 ---------------------------------------------------------
ROLES = [("맡아 주기", GREEN), ("빌려주기", ORANGE), ("바꿔 주기", "#3b82c4"), ("보내 주기", RED), ("지폐", GOLD_D)]
s16 = [("bg", bg_cream(), {"type": "none"}),
       ("title", text("오늘 은행이 하는 일", 540, 440, 76), {"type": "pop", "at": 0.0, "anchor": [540, 410]})]
for i, (name, col) in enumerate(ROLES):
    y = 590 + i * 140
    s16.append((f"r{i + 1}", card(170, y - 55, 740, 110, stroke=col, sw=6, rx=30) + f'<circle cx="250" cy="{y}" r="34" fill="{col}"/>'
                + text(str(i + 1), 250, y + 16, 42, WHITE) + text(name, 320, y + 20, 56, INK, "start"),
                {"type": "slideR", "at": 0.3 + i * 0.7}))
scene("S16", 94, 102, s16)

# S17 퀴즈: bankrupt -----------------------------------------------------------------------
broken = (f'<path d="M260 1000 L520 1000 L540 1034 L260 1034 Z" fill="{BROWN}"/>'
          f'<path d="M560 1012 L820 990 L826 1024 L566 1046 Z" fill="{BROWN}"/>'
          f'<rect x="300" y="1034" width="26" height="150" fill="{BROWN}"/>'
          f'<rect x="760" y="1040" width="26" height="150" fill="{BROWN}" transform="rotate(12 773 1040)"/>'
          f'<path d="M530 980 L548 1010 L536 1040 L552 1062" fill="none" stroke="{RED}" stroke-width="8"/>')
scene("S17", 102, 112, [
    ("bg", bg_cream(), {"type": "none"}),
    ("badge", pill("퀴즈", 540, 420, 64, ORANGE), {"type": "pop", "at": 0.0, "anchor": [540, 420]}),
    ("question", text("bankrupt(파산)의 어원은?", 540, 600, 66), {"type": "pop", "at": 0.3, "anchor": [540, 570]}),
    ("broken", broken, {"type": "drop", "at": 3.0}),
    ("answer", pill("banca rotta = 부서진 탁자", 540, 800, 60, GREEN), {"type": "stamp", "at": 3.4, "anchor": [540, 800]}),
    ("story", text("이야기로 전해져요", 540, 1280, 46, MUTED), {"type": "fade", "at": 6.4}),
])

# S18 구독 CTA ---------------------------------------------------------------------
button = (f'<rect x="290" y="760" width="500" height="170" rx="85" fill="{RED}"/>'
          f'<path d="M405 795 C375 795 368 825 368 850 L360 880 H450 L442 850 C442 825 435 795 405 795 Z M392 890 a13 13 0 0 0 26 0 Z" fill="{WHITE}"/>'
          + text("구독", 600, 878, 92, WHITE))
finger = (f'<path d="M700 905 V1010 C700 1040 740 1060 770 1060 H820 C850 1060 870 1030 870 1000 V960 C870 945 845 940 835 955 '
          f'C835 935 810 930 800 948 C800 930 775 925 765 945 V905 C765 880 700 880 700 905 Z" fill="#f6d2b3" stroke="{INK}" stroke-width="6"/>')
scene("S18", 112, 120, [
    ("bg", bg_cream(), {"type": "none"}),
    ("title", text("은행의 역사, 재밌으셨나요?", 540, 560, 62), {"type": "pop", "at": 0.0, "anchor": [540, 535]}),
    ("button", button, {"type": "pop", "at": 4.2, "anchor": [540, 845]}),
    ("finger", finger, {"type": "tap", "at": 5.0, "anchor": [785, 980]}),
    ("prev", text("지난 편: 예금 vs 적금", 540, 1130, 50, MUTED), {"type": "fade", "at": 5.4}),
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
