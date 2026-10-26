"""Generate SVG parts for all 18 scenes of the DCA-vs-lump-sum Short (1080x1920).

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
LABEL = "지식 쇼츠 · 적립식 vs 거치식"

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


# S01 1,200만 원이 생겼다 -------------------------------------------------------------
scene("S01", 0, 5, [
    ("bg", bg_cream(), {"type": "none"}),
    ("title", text("1,200만 원이", 540, 450, 84) + text("생겼어요!", 540, 570, 96, ORANGE), {"type": "pop", "at": 0.0, "anchor": [540, 510]}),
    ("money", bill(560, 900, 420, "", 56) + bill(540, 860, 420, "") + bill(520, 820, 420, "1,200만", 60),
     {"type": "drop", "at": 0.3}),
    ("q", pill("어떻게 넣지?", 540, 1180, 80, RED), {"type": "stamp", "at": 2.6, "anchor": [540, 1180]}),
])

# S02 갈림길 -------------------------------------------------------------------------
road = (f'<path d="M470 1300 L470 1000 Q470 900 300 820 L230 790 M610 1300 L610 1000 Q610 900 780 820 L850 790" '
        f'fill="none" stroke="{SHADOW}" stroke-width="0"/>'
        f'<path d="M440 1300 C440 1050 440 960 230 820 L330 760 C520 880 540 950 540 1000 C540 950 560 880 750 760 L850 820 '
        f'C640 960 640 1050 640 1300 Z" fill="{MUTED}" fill-opacity="0.35"/>'
        f'<path d="M540 1290 V1060" stroke="{WHITE}" stroke-width="10" stroke-dasharray="40 30"/>')
scene("S02", 5, 10, [
    ("bg", bg_cream(road), {"type": "none"}),
    ("title", text("어느 길로 갈까?", 540, 450, 80), {"type": "pop", "at": 0.0, "anchor": [540, 420]}),
    ("left", pill("한 번에", 260, 680, 64, ORANGE), {"type": "pop", "at": 0.2, "anchor": [260, 680]}),
    ("right", pill("12달 나눠서", 790, 680, 56, GREEN), {"type": "pop", "at": 2.6, "anchor": [790, 680]}),
])

# S03 적립식 vs 거치식 ----------------------------------------------------------------
scene("S03", 10, 14, [
    ("bg", bg_cream(), {"type": "none"}),
    ("title", text("투자자들의 오래된 고민", 540, 450, 70), {"type": "fade", "at": 0.0}),
    ("lump", pill("거치식", 540, 690, 96, ORANGE), {"type": "slideL", "at": 0.6}),
    ("vs", f'<circle cx="540" cy="880" r="90" fill="{INK}"/>' + text("VS", 540, 908, 80, WHITE), {"type": "stamp", "at": 1.6, "anchor": [540, 880]}),
    ("dca", pill("적립식", 540, 1070, 96, GREEN), {"type": "slideR", "at": 1.0}),
])

# S04 거치식 = 한 번에 -----------------------------------------------------------------
basket = (f'<path d="M250 980 L830 980 L770 1240 L310 1240 Z" fill="{WHITE}" stroke="{INK}" stroke-width="8" stroke-linejoin="round"/>'
          + text("투자", 540, 1150, 80, MUTED))
scene("S04", 14, 22, [
    ("bg", bg_cream(basket), {"type": "none"}),
    ("title", text("거치식", 540, 450, 100, ORANGE) + text("한 번에 다 넣기", 540, 550, 56, MUTED), {"type": "pop", "at": 0.0, "anchor": [540, 480]}),
    ("money", bill(540, 860, 400, "1,200만", 58), {"type": "drop", "at": 0.6}),
    ("today", pill("오늘 바로!", 820, 700, 56, RED), {"type": "stamp", "at": 4.0, "anchor": [820, 700]}),
])

# S05 적립식 = 나눠서 ----------------------------------------------------------------
CAL = (150, 640, 195, 150)  # x0, y0, cell w, cell h


def cal_row(r):
    out = ""
    for c in range(4):
        m = r * 4 + c
        x, y = CAL[0] + c * CAL[2], CAL[1] + r * CAL[3]
        out += (card(x + 8, y + 8, CAL[2] - 16, CAL[3] - 16, stroke=GREEN, sw=4, rx=20) + text(f"{m + 1}월", x + CAL[2] / 2, y + 58, 34, MUTED)
                + text("100만", x + CAL[2] / 2, y + 112, 44, GREEN))
    return out


scene("S05", 22, 30, [
    ("bg", bg_cream(), {"type": "none"}),
    ("title", text("적립식", 540, 450, 100, GREEN) + text("나눠서 넣기", 540, 550, 56, MUTED), {"type": "pop", "at": 0.2, "anchor": [540, 480]}),
    ("row1", cal_row(0), {"type": "wipeL", "at": 3.6, "dur": 0.8}),
    ("row2", cal_row(1), {"type": "wipeL", "at": 4.4, "dur": 0.8}),
    ("row3", cal_row(2), {"type": "wipeL", "at": 5.2, "dur": 0.8}),
    ("total", pill("매달 100만 원 × 12달", 540, 1200, 54, INK), {"type": "stamp", "at": 6.4, "anchor": [540, 1200]}),
])

# S06 평균 매입 단가: 가격과 산 주식 수 ------------------------------------------------
B6, U6 = 960, 0.03  # baseline, px per 원
G6 = [(250, "1월", 10000, 30), (540, "2월", 5000, 60), (830, "3월", 10000, 30)]
s06 = [
    ("bg", bg_cream(f'<path d="M110 {B6} H970" stroke="{INK}" stroke-width="6" stroke-linecap="round"/>'
                    + "".join(text(m, x, B6 + 56, 42, MUTED) for x, m, _, _ in G6)), {"type": "none"}),
    ("header", pill("매달 30만 원씩", 540, 440, 60, INK), {"type": "pop", "at": 0.0, "anchor": [540, 440]}),
]
for i, (x, _, p, n) in enumerate(G6):
    h = p * U6
    s06.append((f"bar{i + 1}", f'<rect x="{x - 80}" y="{B6 - 8 - h}" width="160" height="{h}" rx="16" fill="{MUTED}" fill-opacity="0.55"/>'
                + text(f"{p:,}원", x, B6 - 8 - h - 22, 46), {"type": "growY", "at": 3.4 + i * 0.8, "anchor": [x, B6 - 8], "dur": 0.5, "ease": "decel"}))
for i, (x, _, _, n) in enumerate(G6):
    s06.append((f"n{i + 1}", f'<circle cx="{x}" cy="1110" r="{58 + (n - 30) * 0.9}" fill="{GREEN}"/>' + text(f"{n}주", x, 1128, 48, WHITE),
                {"type": "pop", "at": 7.4 + i * 0.6, "anchor": [x, 1110]}))
s06.append(("total", pill("모두 120주", 540, 1260, 56, ORANGE), {"type": "stamp", "at": 9.6, "anchor": [540, 1260]}))
scene("S06", 30, 42, s06)

# S07 7,500원 vs 8,333원 ----------------------------------------------------------------
scene("S07", 42, 50, [
    ("bg", bg_cream(), {"type": "none"}),
    ("calc", text("90만 원 ÷ 120주", 540, 520, 80), {"type": "pop", "at": 0.2, "anchor": [540, 490]}),
    ("mine", card(100, 610, 880, 260, stroke=GREEN, sw=8, rx=44) + text("내 평균 단가", 540, 700, 50, MUTED) + text("7,500원", 540, 830, 120, GREEN),
     {"type": "stamp", "at": 2.4, "anchor": [540, 740]}),
    ("avg", card(180, 920, 720, 200, rx=40) + text("평균 주가", 540, 995, 44, MUTED) + text("8,333원", 540, 1085, 80, MUTED),
     {"type": "fade", "at": 3.8}),
    ("cheap", pill("더 싸게 샀다!", 540, 1230, 60, RED), {"type": "stamp", "at": 5.6, "anchor": [540, 1230]}),
])

# S08 쌀 때 많이, 비쌀 때 적게 ------------------------------------------------------


def buy_card(x0, price, n, color, line):
    out = card(x0, 580, 420, 600, rx=40) + text(line, x0 + 210, 670, 50, color) + pill(price, x0 + 210, 760, 44, INK)
    for i in range(n):
        out += coin(x0 + 210, 1110 - i * 42, 110)
    return out


scene("S08", 50, 58, [
    ("bg", bg_cream(), {"type": "none"}),
    ("title", text("같은 돈으로", 540, 450, 80), {"type": "pop", "at": 0.0, "anchor": [540, 420]}),
    ("cheap", buy_card(90, "5천 원", 6, GREEN, "쌀 때 많이"), {"type": "slideL", "at": 0.2}),
    ("dear", buy_card(570, "1만 원", 3, RED, "비쌀 때 적게"), {"type": "slideR", "at": 1.8}),
    ("auto", pill("저절로!", 540, 1260, 64, ORANGE), {"type": "stamp", "at": 4.2, "anchor": [540, 1260]}),
])

# S09 뱅가드 연구 ------------------------------------------------------------------------
scene("S09", 58, 69, [
    ("bg", bg_cream(), {"type": "none"}),
    ("title", text("적립식이 항상 이길까?", 540, 440, 76), {"type": "pop", "at": 0.0, "anchor": [540, 410]}),
    ("study", card(90, 580, 900, 300, stroke=GREEN, sw=6, rx=40) + text("뱅가드 연구", 540, 690, 80, GREEN)
     + text("세계 최대 운용사 중 하나", 540, 780, 44, MUTED) + text("2012 · 2023", 540, 845, 44, INK), {"type": "slideR", "at": 3.0}),
    ("us", pill("미국", 300, 1010, 56, INK), {"type": "pop", "at": 7.2, "anchor": [300, 1010]}),
    ("uk", pill("영국", 540, 1010, 56, INK), {"type": "pop", "at": 7.6, "anchor": [540, 1010]}),
    ("au", pill("호주", 780, 1010, 56, INK), {"type": "pop", "at": 8.0, "anchor": [780, 1010]}),
    ("years", text("수십 년 데이터", 540, 1160, 56, MUTED), {"type": "fade", "at": 8.6}),
])

# S10 3번 중 2번 ---------------------------------------------------------------------------
C10 = (540, 830)
dots = ""
for i, col in enumerate((ORANGE, ORANGE, MUTED)):
    x = 300 + i * 240
    dots += f'<circle cx="{x}" cy="{C10[1]}" r="100" fill="{col}"/>' + text("승" if col == ORANGE else "패", x, C10[1] + 30, 80, WHITE)
scene("S10", 69, 80, [
    ("bg", bg_cream(), {"type": "none"}),
    ("title", text("결과는?", 540, 440, 84), {"type": "pop", "at": 0.0, "anchor": [540, 410]}),
    ("who", pill("한 번에 넣기(거치식)", 540, 590, 54, ORANGE), {"type": "pop", "at": 0.6, "anchor": [540, 590]}),
    ("dots", dots, {"type": "pop", "at": 1.4, "anchor": list(C10)}),
    ("big", text("3번 중 2번 승", 540, 1050, 90, ORANGE), {"type": "stamp", "at": 2.4, "anchor": [540, 1020]}),
    ("again", pill("2023년 다시 분석해도 같은 결과", 540, 1220, 46, GREEN), {"type": "fade", "at": 4.0}),
])

# S11 오르는 시장, 쉬는 현금 -----------------------------------------------------------
pts11 = [(130 + i * 26, 1080 - i * 13 - 40 * math.sin(i * 0.9) - 25 * math.sin(i * 2.3)) for i in range(31)]
cash = coin(800, 1170, 80) + coin(800, 1130, 80) + coin(800, 1090, 80) + text("기다리는 돈", 800, 1270, 42, MUTED)
scene("S11", 80, 90, [
    ("bg", bg_cream(f'<path d="M130 620 V1110 H950" fill="none" stroke="{INK}" stroke-width="6" stroke-linecap="round"/>'), {"type": "none"}),
    ("title", text("시장은 오르는 때가 더 많다", 540, 440, 64), {"type": "pop", "at": 0.2, "anchor": [540, 420]}),
    ("line", f'<path d="{poly(pts11)}" fill="none" stroke="{ORANGE}" stroke-width="12" stroke-linecap="round" stroke-linejoin="round"/>',
     {"type": "wipeL", "at": 0.6, "dur": 2.6, "ease": "linear"}),
    ("cash", cash, {"type": "pop", "at": 4.8, "anchor": [800, 1130]}),
    ("zzz", text("Zzz", 905, 1040, 56, MUTED), {"type": "fade", "at": 5.6}),
])

# S12–S14 상황별 비교 (예시) ------------------------------------------------------------
from verify_numbers import SCENARIOS, dca, lump  # noqa: E402

BB, BU = 1250, 0.18  # bar baseline, px per 만 원
LX0, LX1, LY0, LY1 = 200, 880, 520, 700  # mini price chart box


def price_line(prices, color):
    lo, hi = 5000, 14000
    pts = [(LX0 + (LX1 - LX0) * i / 12, LY1 - (LY1 - LY0) * (p - lo) / (hi - lo)) for i, p in enumerate(prices)]
    return f'<path d="{poly(pts)}" fill="none" stroke="{color}" stroke-width="10" stroke-linecap="round" stroke-linejoin="round"/>'


def scenario(sid, start, end, title, key, win, win_color, at_bars, at_win):
    prices = SCENARIOS[key]
    vl, vd = lump(prices), dca(prices)
    bg = (f'<path d="M150 {BB} H930" stroke="{INK}" stroke-width="6" stroke-linecap="round"/>'
          + text("한 번에", 360, BB + 58, 46) + text("나눠서", 720, BB + 58, 46)
          + text("주가", LX0 - 20, LY0 + 10, 34, MUTED, "end") + text("12달", LX1, LY1 + 44, 34, MUTED, "end"))

    def bar(x, v, color, label):
        h = v * BU
        return (f'<rect x="{x - 95}" y="{BB - 8 - h:.0f}" width="190" height="{h:.0f}" rx="16" fill="{color}"/>'
                + text(label, x, BB - 8 - h - 24, 52, color))

    return scene(sid, start, end, [
        ("bg", bg_cream(bg), {"type": "none"}),
        ("title", text(title, 540, 440, 76), {"type": "pop", "at": 0.0, "anchor": [540, 410]}),
        ("line", price_line(prices, INK), {"type": "wipeL", "at": 0.4, "dur": 1.6, "ease": "linear"}),
        ("lump", bar(360, vl, ORANGE, f"{vl:,.0f}만"), {"type": "growY", "at": at_bars, "anchor": [360, BB - 8], "dur": 0.6, "ease": "decel"}),
        ("dca", bar(720, vd, GREEN, f"약 {round(vd, -1):,.0f}만"), {"type": "growY", "at": at_bars + 0.8, "anchor": [720, BB - 8], "dur": 0.6, "ease": "decel"}),
        ("win", pill(win, 540, 810, 54, win_color), {"type": "stamp", "at": at_win, "anchor": [540, 810]}),
    ])


scenario("S12", 90, 100, "① 계속 오르면", "up", "거치식 승리", ORANGE, 3.2, 7.2)
scenario("S13", 100, 110, "② 떨어졌다 회복하면", "v", "적립식 승리", GREEN, 3.2, 7.2)
scenario("S14", 110, 117, "③ 계속 떨어지면", "down", "적립식이 덜 잃음", GREEN, 1.0, 3.4)

# S15 확률 vs 마음 -----------------------------------------------------------------------


def verdict(x0, head, name, color):
    return card(x0, 580, 420, 380, stroke=color, sw=8, rx=44) + text(head, x0 + 210, 680, 52, MUTED) + text(name, x0 + 210, 840, 96, color)


scene("S15", 117, 128, [
    ("bg", bg_cream(), {"type": "none"}),
    ("title", text("그래서 정리하면", 540, 440, 80), {"type": "pop", "at": 0.0, "anchor": [540, 410]}),
    ("prob", verdict(90, "확률로는", "거치식", ORANGE), {"type": "slideL", "at": 0.4}),
    ("mind", verdict(570, "마음 편하기로는", "적립식", GREEN), {"type": "slideR", "at": 2.4}),
    ("key", pill("폭락해도 버틸 수 있나?", 540, 1120, 58, RED), {"type": "stamp", "at": 5.6, "anchor": [540, 1120]}),
])

# S16 월급 투자 -----------------------------------------------------------------------
env = (f'<rect x="120" y="760" width="360" height="240" rx="20" fill="{WHITE}" stroke="{INK}" stroke-width="8"/>'
       f'<path d="M120 770 L300 900 L480 770" fill="none" stroke="{INK}" stroke-width="8" stroke-linejoin="round"/>' + text("월급", 300, 975, 56, ORANGE))
scene("S16", 128, 136, [
    ("bg", bg_cream(), {"type": "none"}),
    ("title", text("월급으로 매달 넣는 건?", 540, 440, 72), {"type": "pop", "at": 0.0, "anchor": [540, 410]}),
    ("env", env, {"type": "pop", "at": 0.4, "anchor": [300, 880]}),
    ("arrow", arrow(520, 880, 640, 880, INK, 10), {"type": "wipeL", "at": 3.8, "dur": 0.4}),
    ("invest", coin(810, 880, 130, "투자", 56), {"type": "pop", "at": 4.2, "anchor": [810, 880]}),
    ("ok", pill("생기자마자 바로!", 540, 1180, 62, GREEN), {"type": "stamp", "at": 5.4, "anchor": [540, 1180]}),
])

# S17 퀴즈 ---------------------------------------------------------------------------
spots = [(140 + i * 66, 1010 + (i % 3) * 14) for i in range(13)] + [(60 + (i % 2) * 22, 820 + i * 50) for i in range(6)] \
    + [(990 + (i % 2) * 22, 820 + i * 50) for i in range(6)]
scene("S17", 136, 146, [
    ("bg", bg_cream(), {"type": "none"}),
    ("badge", pill("퀴즈", 540, 420, 64, ORANGE), {"type": "pop", "at": 0.0, "anchor": [540, 420]}),
    ("question", text("2만 원, 1만 원에", 540, 580, 76) + text("20만 원씩 사면?", 540, 680, 76), {"type": "pop", "at": 0.3, "anchor": [540, 620]}),
    ("formula", text("40만 원 ÷ 30주", 540, 860, 96), {"type": "pop", "at": 1.6, "anchor": [540, 825]}),
    ("answer", pill("= 13,333원", 540, 1060, 100, GREEN), {"type": "stamp", "at": 3.2, "anchor": [540, 1060]}),
    ("confetti", confetti_at(spots), {"type": "drop", "at": 3.4}),
    ("tip", text("평균 주가 15,000원보다 싸요", 540, 1250, 48, MUTED), {"type": "fade", "at": 6.2}),
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
    ("prev", text("지난 편: 4%의 법칙", 540, 1130, 50, MUTED), {"type": "fade", "at": 1.6}),
    ("disclaimer", text("※ 과거 데이터와 예시 계산이며 미래 수익을 보장하지 않습니다", 540, 1290, 28, MUTED), {"type": "fade", "at": 1.8}),
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
