"""Generate SVG parts for all 12 scenes of the card-installments Short (1080x1920).

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
LABEL = "지식 쇼츠 · 무이자 할부"

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


from verify_numbers import FEE_2024, FEE_2025, MONTHS, PRICE  # noqa: E402

BLUE = "#3b82c4"


def credit_card(cx, cy, w=420, color=BLUE, label=""):
    h = w * 0.63
    return (f'<rect x="{cx - w / 2 + 10}" y="{cy - h / 2 + 12}" width="{w}" height="{h}" rx="28" fill="{INK}" fill-opacity="0.25"/>'
            f'<rect x="{cx - w / 2}" y="{cy - h / 2}" width="{w}" height="{h}" rx="28" fill="{color}"/>'
            f'<rect x="{cx - w / 2 + 40}" y="{cy - h / 2 + 70}" width="{w * 0.18}" height="{h * 0.22}" rx="8" fill="{GOLD}"/>'
            f'<path d="M{cx - w / 2 + 40} {cy + h * 0.25} H{cx + w / 2 - 40}" stroke="{WHITE}" stroke-width="10" stroke-dasharray="40 18" stroke-opacity="0.8"/>'
            + (text(label, cx + w * 0.18, cy - h / 2 + 105, w * 0.11, WHITE) if label else ""))


def company(cx, base, s=1.0, name="카드사"):
    def p(v):
        return v * s
    return (f'<rect x="{cx - p(150):.0f}" y="{base - p(330):.0f}" width="{p(300):.0f}" height="{p(330):.0f}" rx="{p(14):.0f}" fill="{WHITE}" stroke="{INK}" stroke-width="6"/>'
            + "".join(f'<rect x="{cx - p(110) + c * p(80):.0f}" y="{base - p(290) + r * p(70):.0f}" width="{p(50):.0f}" height="{p(40):.0f}" fill="#cfe6df"/>'
                      for r in range(3) for c in range(3))
            + f'<rect x="{cx - p(170):.0f}" y="{base - p(390):.0f}" width="{p(340):.0f}" height="{p(70):.0f}" rx="{p(14):.0f}" fill="{BLUE}"/>'
            + text(name, cx, base - p(340), 44 * s, WHITE))


def shop(cx, base, s=1.0):
    def p(v):
        return v * s
    stripes = "".join(f'<rect x="{cx - p(170) + i * p(68):.0f}" y="{base - p(300):.0f}" width="{p(34):.0f}" height="{p(70):.0f}" fill="{RED}"/>' for i in range(5))
    return (f'<rect x="{cx - p(170):.0f}" y="{base - p(300):.0f}" width="{p(340):.0f}" height="{p(70):.0f}" fill="{WHITE}"/>' + stripes
            + f'<rect x="{cx - p(150):.0f}" y="{base - p(230):.0f}" width="{p(300):.0f}" height="{p(230):.0f}" fill="{WHITE}" stroke="{INK}" stroke-width="6"/>'
            + f'<rect x="{cx - p(40):.0f}" y="{base - p(150):.0f}" width="{p(80):.0f}" height="{p(150):.0f}" fill="{BROWN_D}"/>'
            + text("가게", cx, base - p(170), 40 * s, INK))


BROWN_D = "#8a5a3b"

# S01 무이자 할부, 카드사는 손해? -----------------------------------------------------------
scene("S01", 0, 5, [
    ("bg", bg_cream(), {"type": "none"}),
    ("title", text("무이자 할부", 540, 450, 90) + text("카드사는 손해?", 540, 570, 96, ORANGE), {"type": "pop", "at": 0.0, "anchor": [540, 510]}),
    ("card", credit_card(540, 880, 480), {"type": "pop", "at": 0.3, "anchor": [540, 880]}),
    ("stamp", pill("무이자", 700, 760, 64, RED), {"type": "stamp", "at": 1.0, "anchor": [700, 760]}),
    ("why", text("왜 해줄까?", 540, 1210, 80, INK), {"type": "pop", "at": 2.6, "anchor": [540, 1180]}),
])

# S02 120만 원을 3개월로 -------------------------------------------------------------------


def month_box(i, amount):
    x = 150 + i * 270
    return card(x, 760, 240, 220, stroke=GREEN, sw=6, rx=30) + text(f"{i + 1}개월", x + 120, 830, 44, MUTED) + text(amount, x + 120, 930, 62, GREEN)


scene("S02", 5, 12, [
    ("bg", bg_cream(), {"type": "none"}),
    ("price", pill(f"{PRICE // 10000}만 원 · {MONTHS}개월 무이자", 540, 450, 60, INK), {"type": "pop", "at": 0.0, "anchor": [540, 450]}),
    ("m1", month_box(0, f"{PRICE // MONTHS // 10000}만"), {"type": "pop", "at": 3.4, "anchor": [270, 870]}),
    ("m2", month_box(1, f"{PRICE // MONTHS // 10000}만"), {"type": "pop", "at": 3.8, "anchor": [540, 870]}),
    ("m3", month_box(2, f"{PRICE // MONTHS // 10000}만"), {"type": "pop", "at": 4.2, "anchor": [810, 870]}),
    ("zero", pill("이자 0원", 540, 1150, 80, GREEN), {"type": "stamp", "at": 5.2, "anchor": [540, 1150]}),
])

# S03 가게는 며칠 뒤 다 받는다 -------------------------------------------------------------
scene("S03", 12, 19, [
    ("bg", bg_cream(company(260, 1150, 0.9) + shop(820, 1150, 0.9)), {"type": "none"}),
    ("title", text("가게는 며칠 뒤", 540, 450, 80) + text("120만 원을 다 받는다", 540, 560, 70, ORANGE), {"type": "pop", "at": 0.0, "anchor": [540, 500]}),
    ("pay", arrow(420, 900, 660, 900, GREEN, 14) + bill(540, 790, 260, "120만", 40), {"type": "slideR", "at": 1.0}),
    ("first", pill("카드사가 먼저 내줌", 540, 1260, 56, BLUE), {"type": "stamp", "at": 3.8, "anchor": [540, 1260]}),
])

# S04 이자는 카드사가 떠안는다 ----------------------------------------------------------------
scene("S04", 19, 26, [
    ("bg", bg_cream(company(540, 1150, 1.0)), {"type": "none"}),
    ("title", text("3개월 이자는 누가?", 540, 450, 80), {"type": "pop", "at": 0.0, "anchor": [540, 420]}),
    ("coins", coin(300, 640, 70, "이자", 30) + coin(540, 610, 70, "이자", 30) + coin(780, 640, 70, "이자", 30), {"type": "drop", "at": 1.6}),
    ("eat", pill("카드사가 떠안음", 540, 1250, 62, RED), {"type": "stamp", "at": 3.4, "anchor": [540, 1250]}),
    ("shop", text("일부는 가게가 나눠 냄", 540, 1350, 40, MUTED), {"type": "fade", "at": 4.8}),
])

# S05 미끼 ---------------------------------------------------------------------------
hook = (f'<path d="M540 520 V900 C540 1020 700 1020 700 920" fill="none" stroke="{INK}" stroke-width="14" stroke-linecap="round"/>'
        f'<path d="M700 920 L670 950" stroke="{INK}" stroke-width="14" stroke-linecap="round"/>')
scene("S05", 26, 33, [
    ("bg", bg_cream(), {"type": "none"}),
    ("hook", hook, {"type": "drop", "at": 0.0}),
    ("bait", pill("무이자", 620, 1080, 70, RED), {"type": "pop", "at": 0.6, "anchor": [620, 1080]}),
    ("name", text("미끼!", 300, 760, 120, ORANGE), {"type": "stamp", "at": 1.6, "anchor": [300, 720]}),
    ("more", pill("그 카드를 더 많이 쓰게", 540, 1260, 54, INK), {"type": "fade", "at": 3.4}),
])

# S06 가맹점 수수료 ----------------------------------------------------------------------
scene("S06", 33, 40, [
    ("bg", bg_cream(shop(250, 1100, 0.9) + company(830, 1100, 0.9)), {"type": "none"}),
    ("title", text("결제할 때마다", 540, 450, 80), {"type": "pop", "at": 0.0, "anchor": [540, 420]}),
    ("fee", arrow(410, 860, 670, 860, ORANGE, 14) + coin(540, 780, 70, "수수료", 26), {"type": "slideR", "at": 0.8}),
    ("base", pill("가맹점 수수료 = 기본 수입", 540, 1250, 52, ORANGE), {"type": "stamp", "at": 3.6, "anchor": [540, 1250]}),
])

# S07 할부 수수료 3조 6천억 ------------------------------------------------------------------
B7, U7 = 1150, 110  # baseline, px per 조 원
scene("S07", 40, 48, [
    ("bg", bg_cream(f'<path d="M180 {B7} H900" stroke="{INK}" stroke-width="6" stroke-linecap="round"/>'
                    + text("2024년", 380, B7 + 58, 46) + text("2025년", 700, B7 + 58, 46)), {"type": "none"}),
    ("title", text("진짜 수익은", 540, 440, 76) + text("이자가 붙는 할부", 540, 550, 80, RED), {"type": "pop", "at": 0.0, "anchor": [540, 495]}),
    ("b24", f'<rect x="290" y="{B7 - 8 - FEE_2024 / 1e12 * U7:.0f}" width="180" height="{FEE_2024 / 1e12 * U7:.0f}" rx="16" fill="{MUTED}" fill-opacity="0.7"/>'
     + text("3.46조", 380, B7 - 8 - FEE_2024 / 1e12 * U7 - 24, 52, MUTED), {"type": "growY", "at": 3.8, "anchor": [380, B7 - 8], "dur": 0.6, "ease": "decel"}),
    ("b25", f'<rect x="610" y="{B7 - 8 - FEE_2025 / 1e12 * U7:.0f}" width="180" height="{FEE_2025 / 1e12 * U7:.0f}" rx="16" fill="{RED}"/>'
     + text("약 3조 6천억", 700, B7 - 8 - FEE_2025 / 1e12 * U7 - 24, 52, RED), {"type": "growY", "at": 4.4, "anchor": [700, B7 - 8], "dur": 0.6, "ease": "decel"}),
    ("who", text("카드사 7곳 할부 수수료 수익", 540, 1290, 40, MUTED), {"type": "fade", "at": 4.8}),
])

# S08 리볼빙·카드론 -------------------------------------------------------------------------
scene("S08", 48, 55, [
    ("bg", bg_cream(), {"type": "none"}),
    ("r", pill("리볼빙", 330, 520, 70, INK), {"type": "pop", "at": 0.2, "anchor": [330, 520]}),
    ("l", pill("카드론", 750, 520, 70, INK), {"type": "pop", "at": 0.6, "anchor": [750, 520]}),
    ("rate", text("연 10%+", 540, 840, 190, RED) + text("이자", 540, 960, 70, MUTED), {"type": "stamp", "at": 1.6, "anchor": [540, 780]}),
    ("flow", pill("무이자로 들어와서", 540, 1130, 52, GREEN) + pill("이자로 남는다", 540, 1250, 56, RED), {"type": "fade", "at": 3.4}),
])

# S09 12개월 → 2~3개월 -----------------------------------------------------------------------
B9, U9 = 1150, 38
scene("S09", 55, 63, [
    ("bg", bg_cream(f'<path d="M180 {B9} H900" stroke="{INK}" stroke-width="6" stroke-linecap="round"/>'
                    + text("2022년 말", 380, B9 + 58, 46) + text("요즘", 700, B9 + 58, 46)), {"type": "none"}),
    ("title", text("금리가 오르자", 540, 440, 80) + text("무이자 기간이 확!", 540, 550, 76, RED), {"type": "pop", "at": 0.0, "anchor": [540, 495]}),
    ("b1", f'<rect x="290" y="{B9 - 8 - 12 * U9}" width="180" height="{12 * U9}" rx="16" fill="{GREEN}"/>'
     + text("최장 12개월", 380, B9 - 8 - 12 * U9 - 24, 46, GREEN), {"type": "growY", "at": 3.6, "anchor": [380, B9 - 8], "dur": 0.6, "ease": "decel"}),
    ("b2", f'<rect x="610" y="{B9 - 8 - 3 * U9}" width="180" height="{3 * U9}" rx="16" fill="{RED}"/>'
     + text("2~3개월", 700, B9 - 8 - 3 * U9 - 24, 52, RED), {"type": "growY", "at": 5.4, "anchor": [700, B9 - 8], "dur": 0.4, "ease": "decel"}),
])

# S10 조달 비용 + 마케팅 비용 ------------------------------------------------------------------
scene("S10", 63, 70, [
    ("bg", bg_cream(), {"type": "none"}),
    ("title", text("카드사가 돈을", 540, 450, 80) + text("빌려 오는 비용", 540, 560, 80, ORANGE), {"type": "pop", "at": 0.0, "anchor": [540, 505]}),
    ("up", arrow(540, 1000, 540, 700, RED, 22) + text("증가", 640, 870, 80, RED, "start"), {"type": "slideU", "at": 1.2}),
    ("mkt", pill("무이자 = 마케팅 비용", 540, 1200, 62, INK), {"type": "stamp", "at": 3.8, "anchor": [540, 1200]}),
])

# S11 퀴즈 ---------------------------------------------------------------------------
spots = [(140 + i * 66, 1010 + (i % 3) * 14) for i in range(13)] + [(60 + (i % 2) * 22, 820 + i * 50) for i in range(6)] \
    + [(990 + (i % 2) * 22, 820 + i * 50) for i in range(6)]
scene("S11", 70, 80, [
    ("bg", bg_cream(), {"type": "none"}),
    ("badge", pill("퀴즈", 540, 420, 64, ORANGE), {"type": "pop", "at": 0.0, "anchor": [540, 420]}),
    ("question", text("300만 원, 6개월 무이자", 540, 590, 74) + text("매달 얼마?", 540, 700, 84), {"type": "pop", "at": 0.3, "anchor": [540, 640]}),
    ("answer", pill("= 50만 원", 540, 920, 110, GREEN), {"type": "stamp", "at": 3.6, "anchor": [540, 920]}),
    ("confetti", confetti_at(spots), {"type": "drop", "at": 3.8}),
    ("check", pill("무이자 끝나면 수수료 확인!", 540, 1220, 52, RED), {"type": "fade", "at": 6.6}),
])

# S12 무이자는 미끼 + 구독 ---------------------------------------------------------------------
button = (f'<rect x="290" y="900" width="500" height="170" rx="85" fill="{RED}"/>'
          f'<path d="M405 935 C375 935 368 965 368 990 L360 1020 H450 L442 990 C442 965 435 935 405 935 Z M392 1030 a13 13 0 0 0 26 0 Z" fill="{WHITE}"/>'
          + text("구독", 600, 1018, 92, WHITE))
finger = (f'<path d="M700 1045 V1150 C700 1180 740 1200 770 1200 H820 C850 1200 870 1170 870 1140 V1100 C870 1085 845 1080 835 1095 '
          f'C835 1075 810 1070 800 1088 C800 1070 775 1065 765 1085 V1045 C765 1020 700 1020 700 1045 Z" fill="#f6d2b3" stroke="{INK}" stroke-width="6"/>')
scene("S12", 80, 90, [
    ("bg", bg_cream(), {"type": "none"}),
    ("msg", text("무이자는 공짜가 아니라", 540, 470, 70) + text("카드사의 미끼", 540, 590, 96, RED), {"type": "pop", "at": 0.2, "anchor": [540, 530]}),
    ("button", button, {"type": "pop", "at": 4.8, "anchor": [540, 985]}),
    ("finger", finger, {"type": "tap", "at": 5.6, "anchor": [785, 1120]}),
    ("prev", text("지난 편: 이자에 붙는 세금", 540, 1260, 48, MUTED), {"type": "fade", "at": 6.0}),
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
