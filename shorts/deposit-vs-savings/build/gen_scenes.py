"""Generate SVG parts for all 18 scenes of the deposit-vs-savings Short (1080x1920).

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
LABEL = "지식 쇼츠 · 예금 vs 적금"

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


from verify_numbers import after_tax, deposit_interest, savings_interest  # noqa: E402

DEP, SAV = deposit_interest(12_000_000, 0.03), savings_interest(1_000_000, 0.035)


def product(x0, y0, name, rate, color, w=420, h=300):
    return (card(x0, y0, w, h, stroke=color, sw=8, rx=40) + text(name, x0 + w / 2, y0 + 105, 66, color)
            + text(rate, x0 + w / 2, y0 + 225, 84, INK))


def bank(cx, base, s=1.0):
    def p(v):
        return v * s
    cols = "".join(f'<rect x="{cx + p(dx) - p(18):.0f}" y="{base - p(200):.0f}" width="{p(36):.0f}" height="{p(170):.0f}" fill="{WHITE}" stroke="{INK}" stroke-width="5"/>'
                   for dx in (-120, -40, 40, 120))
    return (f'<path d="M{cx - p(190):.0f} {base - p(210):.0f} L{cx:.0f} {base - p(320):.0f} L{cx + p(190):.0f} {base - p(210):.0f} Z" fill="{GREEN}" stroke="{INK}" stroke-width="6" stroke-linejoin="round"/>'
            + cols + f'<rect x="{cx - p(200):.0f}" y="{base - p(30):.0f}" width="{p(400):.0f}" height="{p(30):.0f}" fill="{INK}"/>'
            + text("은행", cx, base - p(240), 40 * s, WHITE))


# S01 예금 3% vs 적금 3.5% ------------------------------------------------------------
scene("S01", 0, 5, [
    ("bg", bg_cream(), {"type": "none"}),
    ("title", text("목돈 1,200만 원", 540, 450, 84), {"type": "pop", "at": 0.0, "anchor": [540, 420]}),
    ("dep", product(90, 600, "예금", "연 3%", GREEN), {"type": "slideL", "at": 0.6}),
    ("sav", product(570, 600, "적금", "연 3.5%", ORANGE), {"type": "slideR", "at": 1.6}),
    ("q", pill("어디에 넣을까?", 540, 1100, 72, RED), {"type": "stamp", "at": 3.4, "anchor": [540, 1100]}),
])

# S02 금리 높은 적금? → 예금 승 --------------------------------------------------------
scene("S02", 5, 10, [
    ("bg", bg_cream(product(330, 560, "적금", "연 3.5%", ORANGE)), {"type": "none"}),
    ("up", arrow(880, 820, 880, 620, ORANGE, 14) + text("금리 높다!", 880, 580, 46, ORANGE), {"type": "fade", "at": 0.2}),
    ("but", text("그런데 1년 뒤 이자는", 540, 1000, 60, MUTED), {"type": "fade", "at": 2.2}),
    ("win", pill("예금이 더 많다!", 540, 1150, 80, GREEN), {"type": "stamp", "at": 3.0, "anchor": [540, 1150]}),
])

# S03 왜? ----------------------------------------------------------------------------
scene("S03", 10, 14, [
    ("bg", bg_cream(), {"type": "none"}),
    ("title", text("금리 높은 적금이", 540, 450, 76), {"type": "pop", "at": 0.0, "anchor": [540, 420]}),
    ("why", f'<circle cx="540" cy="830" r="260" fill="{ORANGE}"/>' + text("왜?", 540, 900, 210, WHITE), {"type": "pop", "at": 0.4, "anchor": [540, 830]}),
    ("lose", text("질까요?", 540, 1230, 90), {"type": "stamp", "at": 1.6, "anchor": [540, 1200]}),
])

# S04 예금 = 한 번에 ---------------------------------------------------------------------
scene("S04", 14, 22, [
    ("bg", bg_cream(bank(760, 960, 0.9)), {"type": "none"}),
    ("title", text("예금", 540, 450, 100, GREEN) + text("목돈을 한 번에 맡기기", 540, 550, 52, MUTED), {"type": "pop", "at": 0.0, "anchor": [540, 480]}),
    ("money", bill(280, 820, 340, "1,200만", 52), {"type": "slideL", "at": 0.6}),
    ("bar", text("1년 내내 이자", 540, 1060, 50, GREEN) + f'<rect x="140" y="1090" width="800" height="70" rx="20" fill="{GREEN}"/>'
     + text("12달", 540, 1140, 44, WHITE), {"type": "wipeL", "at": 4.2, "dur": 1.2}),
])

# S05 적금 = 매달 ---------------------------------------------------------------------
CAL = (150, 640, 195, 150)


def cal_row(r):
    out = ""
    for c in range(4):
        m = r * 4 + c
        x, y = CAL[0] + c * CAL[2], CAL[1] + r * CAL[3]
        out += (card(x + 8, y + 8, CAL[2] - 16, CAL[3] - 16, stroke=ORANGE, sw=4, rx=20) + text(f"{m + 1}월", x + CAL[2] / 2, y + 58, 34, MUTED)
                + text("100만", x + CAL[2] / 2, y + 112, 44, ORANGE))
    return out


scene("S05", 22, 30, [
    ("bg", bg_cream(), {"type": "none"}),
    ("title", text("적금", 540, 450, 100, ORANGE) + text("매달 나눠 넣기", 540, 550, 52, MUTED), {"type": "pop", "at": 0.2, "anchor": [540, 480]}),
    ("row1", cal_row(0), {"type": "wipeL", "at": 3.6, "dur": 0.8}),
    ("row2", cal_row(1), {"type": "wipeL", "at": 4.4, "dur": 0.8}),
    ("row3", cal_row(2), {"type": "wipeL", "at": 5.2, "dur": 0.8}),
])

# S06–S07 이자가 붙는 기간: 12달 → 1달 계단 --------------------------------------------
B6, UH, X6, DX = 1180, 46, 150, 66  # baseline, px per month, first bar x, spacing


def stairs(highlight=()):
    out = f'<path d="M110 {B6} H970" stroke="{INK}" stroke-width="6" stroke-linecap="round"/>'
    for k in range(12):
        n = 12 - k
        x = X6 + k * DX
        col = RED if k in highlight else ORANGE
        out += f'<rect x="{x}" y="{B6 - 6 - n * UH}" width="{DX - 14}" height="{n * UH}" rx="10" fill="{col}" fill-opacity="0.85"/>'
    out += text("1월", X6 + (DX - 14) / 2, B6 + 50, 34, MUTED) + text("12월", X6 + 11 * DX + (DX - 14) / 2, B6 + 50, 34, MUTED)
    return out


scene("S06", 30, 42, [
    ("bg", bg_cream(text("넣은 달별로 이자 받는 기간", 540, 1300, 44, MUTED)), {"type": "none"}),
    ("title", text("비밀은 이자 기간", 540, 440, 84), {"type": "pop", "at": 0.0, "anchor": [540, 410]}),
    ("bars", stairs(), {"type": "wipeL", "at": 0.8, "dur": 2.0, "ease": "linear"}),
    ("first", pill("12달", X6 + 26, B6 - 6 - 12 * UH - 50, 44, RED), {"type": "stamp", "at": 3.6, "anchor": [X6 + 26, B6 - 6 - 12 * UH - 50]}),
    ("last", pill("1달", X6 + 11 * DX + 26, B6 - 6 - 3 * UH - 50, 44, RED) + arrow(X6 + 11 * DX + 26, B6 - 6 - 3 * UH - 10, X6 + 11 * DX + 26, B6 - 6 - UH - 10, RED, 6),
     {"type": "stamp", "at": 8.0, "anchor": [X6 + 11 * DX + 26, B6 - 6 - 3 * UH - 50]}),
])
avg_y = B6 - 6 - 6.5 * UH
scene("S07", 42, 50, [
    ("bg", bg_cream(stairs()), {"type": "none"}),
    ("title", text("평균하면?", 540, 440, 84), {"type": "pop", "at": 0.0, "anchor": [540, 410]}),
    ("avg", f'<path d="M110 {avg_y} H970" stroke="{GREEN}" stroke-width="10" stroke-dasharray="30 18"/>'
     + pill("평균 6.5달", 760, avg_y - 160, 56, GREEN), {"type": "wipeL", "at": 0.6, "dur": 1.0}),
    ("half", pill("금리 절반 효과!", 540, 1300, 60, RED), {"type": "stamp", "at": 4.4, "anchor": [540, 1300]}),
])

# S08 22만 7,500원 ----------------------------------------------------------------------
scene("S08", 50, 58, [
    ("bg", bg_cream(), {"type": "none"}),
    ("title", pill("연 3.5% 적금 · 1년", 540, 450, 60, ORANGE), {"type": "pop", "at": 0.0, "anchor": [540, 450]}),
    ("formula", text("100만 × 3.5% × 6.5", 540, 760, 92), {"type": "pop", "at": 3.2, "anchor": [540, 720]}),
    ("result", card(100, 880, 880, 280, stroke=ORANGE, sw=8, rx=44) + text("1년 이자", 540, 970, 50, MUTED)
     + text(f"{SAV:,.0f}원", 540, 1100, 116, ORANGE), {"type": "stamp", "at": 5.0, "anchor": [540, 1020]}),
])

# S09 1.9% → 예금 36만 원 --------------------------------------------------------------
scene("S09", 58, 69, [
    ("bg", bg_cream(), {"type": "none"}),
    ("sav", card(90, 380, 900, 280, rx=40) + text("적금 이자 ÷ 1,200만 원", 540, 470, 50, MUTED) + text("약 1.9%", 540, 610, 120, ORANGE),
     {"type": "pop", "at": 0.2, "anchor": [540, 520]}),
    ("dep", card(90, 760, 900, 420, stroke=GREEN, sw=8, rx=44) + text("예금 연 3%", 540, 860, 60, GREEN)
     + text("1,200만 × 3%", 540, 980, 72) + text(f"= {DEP / 10000:.0f}만 원", 540, 1120, 100, GREEN), {"type": "slideR", "at": 3.6}),
])

# S10 막대 비교 + 5.5% ----------------------------------------------------------------
B10, U10 = 1000, 0.0011
scene("S10", 69, 80, [
    ("bg", bg_cream(f'<path d="M150 {B10} H930" stroke="{INK}" stroke-width="6" stroke-linecap="round"/>'
                    + text("예금 3%", 360, B10 + 58, 46) + text("적금 3.5%", 720, B10 + 58, 46)), {"type": "none"}),
    ("dep", f'<rect x="265" y="{B10 - 8 - DEP * U10:.0f}" width="190" height="{DEP * U10:.0f}" rx="16" fill="{GREEN}"/>'
     + text("36만", 360, B10 - 8 - DEP * U10 - 24, 60, GREEN), {"type": "growY", "at": 0.3, "anchor": [360, B10 - 8], "dur": 0.6, "ease": "decel"}),
    ("sav", f'<rect x="625" y="{B10 - 8 - SAV * U10:.0f}" width="190" height="{SAV * U10:.0f}" rx="16" fill="{ORANGE}"/>'
     + text("22.75만", 720, B10 - 8 - SAV * U10 - 24, 60, ORANGE), {"type": "growY", "at": 0.9, "anchor": [720, B10 - 8], "dur": 0.6, "ease": "decel"}),
    ("diff", pill("+13만 원", 360, 440, 56, RED), {"type": "stamp", "at": 2.0, "anchor": [360, 440]}),
    ("need", card(100, 1110, 880, 200, stroke=ORANGE, sw=6, rx=40) + text("적금이 이기려면", 540, 1185, 46, MUTED)
     + text("약 5.5%", 540, 1280, 84, ORANGE), {"type": "pop", "at": 3.8, "anchor": [540, 1210]}),
])

# S11 세금 15.4% -----------------------------------------------------------------------
scene("S11", 80, 90, [
    ("bg", bg_cream(), {"type": "none"}),
    ("title", text("이자에 붙는 세금", 540, 440, 80), {"type": "pop", "at": 0.2, "anchor": [540, 410]}),
    ("tax", f'<circle cx="540" cy="780" r="230" fill="{RED}"/>' + text("15.4%", 540, 830, 140, WHITE), {"type": "stamp", "at": 2.0, "anchor": [540, 780]}),
    ("parts", pill("소득세 14%", 320, 1140, 50, INK) + text("+", 540, 1158, 60, INK) + pill("지방소득세 1.4%", 770, 1140, 44, INK),
     {"type": "fade", "at": 4.8}),
])

# S12 세후 ---------------------------------------------------------------------------


def tax_row(y, name, color, before, after):
    return (card(90, y - 130, 900, 260, stroke=color, sw=6, rx=40) + text(name, 160, y - 50, 50, color, "start")
            + text(before, 920, y - 50, 50, MUTED, "end")
            + f'<path d="M{920 - text_width(before, 50):.0f} {y - 66} H920" stroke="{MUTED}" stroke-width="5"/>'
            + text("세후", 160, y + 75, 44, MUTED, "start") + text(after, 920, y + 80, 84, color, "end"))


scene("S12", 90, 100, [
    ("bg", bg_cream(), {"type": "none"}),
    ("title", text("세금 떼면", 540, 440, 84), {"type": "pop", "at": 0.0, "anchor": [540, 410]}),
    ("dep", tax_row(700, "예금", GREEN, "36만 원", f"{after_tax(DEP):,.0f}원"), {"type": "slideR", "at": 0.4}),
    ("sav", tax_row(1030, "적금", ORANGE, f"{SAV:,.0f}원", f"{after_tax(SAV):,.0f}원"), {"type": "slideR", "at": 4.8}),
])

# S13 적금은 손해? → 모으는 습관 ---------------------------------------------------------
checks = ""
for i in range(12):
    x, y = 210 + (i % 6) * 132, 700 + (i // 6) * 150
    checks += (f'<circle cx="{x}" cy="{y}" r="52" fill="{GREEN}"/>'
               f'<path d="M{x - 22} {y} L{x - 6} {y + 18} L{x + 24} {y - 16}" fill="none" stroke="{WHITE}" stroke-width="10" stroke-linecap="round" stroke-linejoin="round"/>')
scene("S13", 100, 110, [
    ("bg", bg_cream(), {"type": "none"}),
    ("title", text("적금은 손해일까?", 540, 440, 80), {"type": "pop", "at": 0.0, "anchor": [540, 410]}),
    ("no", pill("아니에요!", 540, 580, 60, INK), {"type": "stamp", "at": 3.0, "anchor": [540, 580]}),
    ("checks", checks, {"type": "wipeL", "at": 4.0, "dur": 1.6, "ease": "linear"}),
    ("habit", pill("모으는 습관", 540, 1110, 72, GREEN), {"type": "stamp", "at": 6.8, "anchor": [540, 1110]}),
])

# S14 목돈은 예금, 매달은 적금 -----------------------------------------------------------


def rule_card(y, cond, name, color):
    return (card(90, y - 120, 900, 240, stroke=color, sw=8, rx=44) + text(cond, 150, y + 20, 56, INK, "start")
            + arrow(560, y, 650, y, MUTED, 8) + text(name, 930, y + 34, 96, color, "end"))


scene("S14", 110, 117, [
    ("bg", bg_cream(), {"type": "none"}),
    ("title", text("이렇게 쓰세요", 540, 440, 84), {"type": "pop", "at": 0.0, "anchor": [540, 410]}),
    ("dep", rule_card(720, "목돈이 있으면", "예금", GREEN), {"type": "slideL", "at": 0.2}),
    ("sav", rule_card(1010, "매달 모으면", "적금", ORANGE), {"type": "slideR", "at": 3.2}),
])

# S15 주의: 중도해지, 예금자보호 1억 --------------------------------------------------------
shield = (f'<path d="M230 1000 L330 960 L430 1000 V1080 C430 1140 380 1180 330 1200 C280 1180 230 1140 230 1080 Z" fill="{GREEN}"/>'
          f'<path d="M290 1080 L320 1110 L375 1050" fill="none" stroke="{WHITE}" stroke-width="12" stroke-linecap="round" stroke-linejoin="round"/>')
scene("S15", 117, 128, [
    ("bg", bg_cream(), {"type": "none"}),
    ("title", text("알아두세요", 540, 440, 84), {"type": "pop", "at": 0.0, "anchor": [540, 410]}),
    ("cancel", card(90, 560, 900, 280, stroke=RED, sw=8, rx=44) + text("중도 해지하면", 540, 670, 56, MUTED)
     + text("약속한 금리 X", 540, 790, 84, RED), {"type": "pop", "at": 0.4, "anchor": [540, 700]}),
    ("protect", card(90, 900, 900, 360, stroke=GREEN, sw=8, rx=44) + shield + text("예금자보호", 470, 1010, 50, MUTED, "start")
     + text("1억 원", 470, 1130, 110, GREEN, "start") + text("금융회사별 · 원금+이자", 470, 1210, 36, MUTED, "start"),
     {"type": "pop", "at": 4.8, "anchor": [540, 1080]}),
])

# S16 정리 ---------------------------------------------------------------------------
scene("S16", 128, 136, [
    ("bg", bg_cream(), {"type": "none"}),
    ("badge", pill("정리", 540, 430, 64, ORANGE), {"type": "pop", "at": 0.0, "anchor": [540, 430]}),
    ("main", card(80, 560, 920, 300, stroke=ORANGE, sw=8, rx=44) + text("적금 이자는", 540, 660, 56, MUTED)
     + text("금리의 약 절반", 540, 790, 96, ORANGE), {"type": "pop", "at": 0.4, "anchor": [540, 710]}),
    ("use", card(80, 920, 920, 300, rx=44) + text("목돈은", 300, 1040, 50, MUTED) + text("예금", 300, 1160, 100, GREEN)
     + text("매달은", 780, 1040, 50, MUTED) + text("적금", 780, 1160, 100, ORANGE), {"type": "pop", "at": 4.0, "anchor": [540, 1070]}),
])

# S17 퀴즈 ---------------------------------------------------------------------------
spots = [(140 + i * 66, 1010 + (i % 3) * 14) for i in range(13)] + [(60 + (i % 2) * 22, 820 + i * 50) for i in range(6)] \
    + [(990 + (i % 2) * 22, 820 + i * 50) for i in range(6)]
scene("S17", 136, 146, [
    ("bg", bg_cream(), {"type": "none"}),
    ("badge", pill("퀴즈", 540, 420, 64, ORANGE), {"type": "pop", "at": 0.0, "anchor": [540, 420]}),
    ("question", text("월 10만 원, 연 6% 적금", 540, 580, 70) + text("1년 이자는?", 540, 680, 76), {"type": "pop", "at": 0.3, "anchor": [540, 620]}),
    ("formula", text("10만 × 6% × 6.5", 540, 860, 90), {"type": "pop", "at": 1.6, "anchor": [540, 825]}),
    ("answer", pill("= 3만 9천 원", 540, 1060, 96, GREEN), {"type": "stamp", "at": 3.2, "anchor": [540, 1060]}),
    ("confetti", confetti_at(spots), {"type": "drop", "at": 3.4}),
    ("tip", text("세금 떼면 약 3만 3천 원", 540, 1250, 50, MUTED), {"type": "fade", "at": 6.2}),
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
    ("prev", text("지난 편: 적립식 vs 거치식", 540, 1130, 50, MUTED), {"type": "fade", "at": 1.6}),
    ("disclaimer", text("※ 예시 금리 · 단리 기준. 실제 상품은 상품설명서를 확인하세요", 540, 1290, 28, MUTED), {"type": "fade", "at": 1.8}),
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
