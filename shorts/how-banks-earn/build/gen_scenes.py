"""Generate SVG parts for all 12 scenes of the how-banks-earn Short (1080x1920).

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
LABEL = "지식 쇼츠 · 은행의 돈벌이"

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


from verify_numbers import DEP_RATE, DEPOSIT, LOAN_RATE, NET_INTEREST, NON_INTEREST  # noqa: E402


def bank(cx, base, s=1.0):
    def p(v):
        return v * s
    cols = "".join(f'<rect x="{cx + p(dx) - p(18):.0f}" y="{base - p(200):.0f}" width="{p(36):.0f}" height="{p(170):.0f}" fill="{WHITE}" stroke="{INK}" stroke-width="5"/>'
                   for dx in (-120, -40, 40, 120))
    return (f'<path d="M{cx - p(190):.0f} {base - p(210):.0f} L{cx:.0f} {base - p(320):.0f} L{cx + p(190):.0f} {base - p(210):.0f} Z" fill="{GREEN}" stroke="{INK}" stroke-width="6" stroke-linejoin="round"/>'
            + cols + f'<rect x="{cx - p(200):.0f}" y="{base - p(30):.0f}" width="{p(400):.0f}" height="{p(30):.0f}" fill="{INK}"/>'
            + text("은행", cx, base - p(240), 40 * s, WHITE))


# S01 은행은 어떻게 돈을 벌까? ---------------------------------------------------------
scene("S01", 0, 5, [
    ("bg", bg_cream(), {"type": "none"}),
    ("title", text("은행은 어떻게", 540, 450, 84) + text("돈을 벌까?", 540, 570, 100, ORANGE), {"type": "pop", "at": 0.0, "anchor": [540, 510]}),
    ("bank", bank(540, 1080, 1.1) + text("?", 790, 760, 140, RED), {"type": "pop", "at": 0.3, "anchor": [540, 900]}),
    ("pay", pill("예금 이자까지 주면서?", 540, 1230, 54, INK), {"type": "fade", "at": 2.6}),
])

# S02 금리 차이: 예금 3% / 대출 5% ------------------------------------------------------
scene("S02", 5, 11, [
    ("bg", bg_cream(bank(540, 1000, 0.8)), {"type": "none"}),
    ("title", text("비밀은 금리 차이", 540, 450, 84), {"type": "pop", "at": 0.0, "anchor": [540, 420]}),
    ("dep", pill("예금 3%로 받고", 280, 640, 50, GREEN) + arrow(280, 690, 420, 820, GREEN, 10), {"type": "slideL", "at": 2.8}),
    ("loan", pill("대출 5%로 빌려주고", 790, 640, 46, ORANGE) + arrow(660, 820, 790, 690, ORANGE, 10), {"type": "slideR", "at": 4.0}),
    ("gap", pill("+2%p", 540, 1140, 70, RED), {"type": "stamp", "at": 5.0, "anchor": [540, 1140]}),
])

# S03 1억 원: 주는 이자 300만 vs 받는 이자 500만 -----------------------------------------
paid, earned = DEPOSIT * DEP_RATE, DEPOSIT * LOAN_RATE
scene("S03", 11, 19, [
    ("bg", bg_cream(), {"type": "none"}),
    ("title", pill("1억 원으로 보면 (예시)", 540, 440, 56, INK), {"type": "pop", "at": 0.0, "anchor": [540, 440]}),
    ("pay", card(90, 560, 900, 260, stroke=GREEN, sw=6, rx=40) + text("예금자에게 주는 이자 (3%)", 540, 650, 46, MUTED)
     + text(f"{paid / 10000:,.0f}만 원", 540, 770, 100, GREEN), {"type": "slideL", "at": 0.4}),
    ("earn", card(90, 880, 900, 260, stroke=ORANGE, sw=6, rx=40) + text("대출자에게 받는 이자 (5%)", 540, 970, 46, MUTED)
     + text(f"{earned / 10000:,.0f}만 원", 540, 1090, 100, ORANGE), {"type": "slideR", "at": 3.6}),
])

# S04 차이 200만 원 = 예대마진 ------------------------------------------------------------
scene("S04", 19, 25, [
    ("bg", bg_cream(), {"type": "none"}),
    ("calc", text(f"{earned / 10000:,.0f}만 − {paid / 10000:,.0f}만", 540, 560, 90), {"type": "pop", "at": 0.0, "anchor": [540, 525]}),
    ("margin", f'<circle cx="540" cy="830" r="220" fill="{RED}"/>' + text(f"{(earned - paid) / 10000:,.0f}만 원", 540, 860, 100, WHITE),
     {"type": "stamp", "at": 0.8, "anchor": [540, 830]}),
    ("name", pill("예대마진", 540, 1170, 80, INK), {"type": "pop", "at": 2.8, "anchor": [540, 1170]}),
])

# S05 금고에 쌓아 두지 않는다 --------------------------------------------------------------
safe = (f'<rect x="120" y="640" width="360" height="460" rx="30" fill="#5d6470" stroke="{INK}" stroke-width="8"/>'
        f'<rect x="155" y="675" width="290" height="390" rx="20" fill="#3e444d"/>'
        + coin(300, 1020, 90) + text("일부만", 300, 900, 50, WHITE))
scene("S05", 25, 32, [
    ("bg", bg_cream(safe), {"type": "none"}),
    ("title", text("예금은 금고에?", 540, 450, 84), {"type": "pop", "at": 0.0, "anchor": [540, 420]}),
    ("out", arrow(500, 860, 640, 860, ORANGE, 12) + bill(820, 800, 280, "대출", 40) + bill(830, 960, 280, "대출", 40),
     {"type": "slideR", "at": 3.6}),
    ("rest", pill("나머지는 빌려준다", 540, 1230, 58, ORANGE), {"type": "stamp", "at": 4.4, "anchor": [540, 1230]}),
])

# S06 2025년 이자이익 vs 비이자이익 ---------------------------------------------------------
B6, U6 = 1180, 9.5  # baseline, px per 조 원
scene("S06", 32, 41, [
    ("bg", bg_cream(f'<path d="M150 {B6} H930" stroke="{INK}" stroke-width="6" stroke-linecap="round"/>'
                    + text("이자로 번 돈", 360, B6 + 60, 46) + text("수수료 등", 720, B6 + 60, 46)), {"type": "none"}),
    ("title", pill("2025년 국내 은행", 540, 440, 58, INK), {"type": "pop", "at": 0.0, "anchor": [540, 440]}),
    ("ni", f'<rect x="250" y="{B6 - 8 - NET_INTEREST * U6:.0f}" width="220" height="{NET_INTEREST * U6:.0f}" rx="18" fill="{ORANGE}"/>'
     + text("약 60조 원", 360, B6 - 8 - NET_INTEREST * U6 - 26, 60, ORANGE), {"type": "growY", "at": 0.6, "anchor": [360, B6 - 8], "dur": 0.8, "ease": "decel"}),
    ("nn", f'<rect x="610" y="{B6 - 8 - NON_INTEREST * U6:.0f}" width="220" height="{NON_INTEREST * U6:.0f}" rx="18" fill="{GREEN}"/>'
     + text("7조 6천억 원", 720, B6 - 8 - NON_INTEREST * U6 - 26, 52, GREEN), {"type": "growY", "at": 3.8, "anchor": [720, B6 - 8], "dur": 0.6, "ease": "decel"}),
])

# S07 10원 중 9원 ---------------------------------------------------------------------------
coins7 = "".join(coin(220 + (i % 5) * 160, 780 + (i // 5) * 170, 70, "이자" if i < 9 else "기타", 28,
                      color=GOLD if i < 9 else "#cfcfcf", edge=GOLD_D if i < 9 else "#9a9a9a") for i in range(10))
scene("S07", 41, 47, [
    ("bg", bg_cream(), {"type": "none"}),
    ("title", text("10원을 벌면", 540, 450, 84), {"type": "pop", "at": 0.0, "anchor": [540, 420]}),
    ("coins", coins7, {"type": "pop", "at": 0.4, "anchor": [540, 860]}),
    ("nine", pill("약 9원이 이자", 540, 1130, 70, ORANGE), {"type": "stamp", "at": 1.4, "anchor": [540, 1130]}),
    ("trade", text("결국 이자 장사", 540, 1280, 60, INK), {"type": "fade", "at": 2.8}),
])

# S08 못 받으면 손해 ------------------------------------------------------------------------
scene("S08", 47, 55, [
    ("bg", bg_cream(bank(300, 1040, 0.8)), {"type": "none"}),
    ("title", text("무조건 남을까?", 540, 450, 84), {"type": "pop", "at": 0.0, "anchor": [540, 420]}),
    ("gone", bill(780, 820, 300, "빌려준 돈", 34) + text("?", 940, 720, 110, RED), {"type": "slideR", "at": 3.6}),
    ("loss", pill("못 받으면 손해", 540, 1200, 70, RED), {"type": "stamp", "at": 5.2, "anchor": [540, 1200]}),
])

# S09 신용·담보 심사, 위험할수록 높은 금리 ---------------------------------------------------
lens = (f'<circle cx="300" cy="760" r="140" fill="{WHITE}" stroke="{INK}" stroke-width="14"/>'
        f'<path d="M400 860 L500 960" stroke="{INK}" stroke-width="28" stroke-linecap="round"/>'
        + text("신용", 300, 740, 52, GREEN) + text("담보", 300, 810, 52, ORANGE))
B9 = 1180
risk = (f'<path d="M560 {B9} H980" stroke="{INK}" stroke-width="6" stroke-linecap="round"/>'
        + "".join(f'<rect x="{590 + i * 130}" y="{B9 - 8 - h}" width="100" height="{h}" rx="12" fill="{c}"/>'
                  for i, (h, c) in enumerate(((140, GREEN), (240, ORANGE), (360, RED))))
        + text("낮음", 640, B9 + 50, 36, MUTED) + text("위험", 770, B9 + 50, 36, MUTED) + text("높음", 900, B9 + 50, 36, MUTED)
        + text("대출 금리", 770, 740, 44, INK))
scene("S09", 55, 62, [
    ("bg", bg_cream(), {"type": "none"}),
    ("title", text("그래서 꼼꼼히 심사", 540, 450, 80), {"type": "pop", "at": 0.0, "anchor": [540, 420]}),
    ("lens", lens, {"type": "pop", "at": 0.6, "anchor": [300, 760]}),
    ("risk", risk, {"type": "wipeL", "at": 3.4, "dur": 1.2}),
])

# S10 정리: 싸게 빌려 비싸게 빌려주는 가게 ------------------------------------------------------
shop = (bank(540, 980, 1.0) + pill("싸게 빌려서", 300, 1130, 44, GREEN) + pill("비싸게 빌려줌", 780, 1130, 44, ORANGE)
        + arrow(462, 1130, 598, 1130, INK, 8))
scene("S10", 62, 70, [
    ("bg", bg_cream(), {"type": "none"}),
    ("badge", pill("정리", 540, 430, 64, ORANGE), {"type": "pop", "at": 0.0, "anchor": [540, 430]}),
    ("shop", shop, {"type": "pop", "at": 0.4, "anchor": [540, 900]}),
    ("store", text("돈을 파는 가게", 540, 1280, 70, INK), {"type": "fade", "at": 3.4}),
])

# S11 퀴즈 ---------------------------------------------------------------------------
spots = [(140 + i * 66, 1010 + (i % 3) * 14) for i in range(13)] + [(60 + (i % 2) * 22, 820 + i * 50) for i in range(6)] \
    + [(990 + (i % 2) * 22, 820 + i * 50) for i in range(6)]
scene("S11", 70, 80, [
    ("bg", bg_cream(), {"type": "none"}),
    ("badge", pill("퀴즈", 540, 420, 64, ORANGE), {"type": "pop", "at": 0.0, "anchor": [540, 420]}),
    ("question", text("예금 3%, 대출 6%", 540, 580, 76) + text("1억 원이면 은행 몫은?", 540, 680, 70), {"type": "pop", "at": 0.3, "anchor": [540, 620]}),
    ("formula", text("1억 × (6% − 3%)", 540, 860, 86), {"type": "pop", "at": 1.6, "anchor": [540, 825]}),
    ("answer", pill("= 300만 원", 540, 1060, 100, GREEN), {"type": "stamp", "at": 3.6, "anchor": [540, 1060]}),
    ("confetti", confetti_at(spots), {"type": "drop", "at": 3.8}),
])

# S12 내 예금 = 누군가의 대출 + 구독 ----------------------------------------------------------
button = (f'<rect x="290" y="900" width="500" height="170" rx="85" fill="{RED}"/>'
          f'<path d="M405 935 C375 935 368 965 368 990 L360 1020 H450 L442 990 C442 965 435 935 405 935 Z M392 1030 a13 13 0 0 0 26 0 Z" fill="{WHITE}"/>'
          + text("구독", 600, 1018, 92, WHITE))
finger = (f'<path d="M700 1045 V1150 C700 1180 740 1200 770 1200 H820 C850 1200 870 1170 870 1140 V1100 C870 1085 845 1080 835 1095 '
          f'C835 1075 810 1070 800 1088 C800 1070 775 1065 765 1085 V1045 C765 1020 700 1020 700 1045 Z" fill="#f6d2b3" stroke="{INK}" stroke-width="6"/>')
scene("S12", 80, 90, [
    ("bg", bg_cream(), {"type": "none"}),
    ("link", text("내 예금이", 540, 470, 76) + text("누군가의 대출로", 540, 580, 84, ORANGE), {"type": "pop", "at": 0.2, "anchor": [540, 525]}),
    ("button", button, {"type": "pop", "at": 4.8, "anchor": [540, 985]}),
    ("finger", finger, {"type": "tap", "at": 5.6, "anchor": [785, 1120]}),
    ("prev", text("지난 편: 은행의 탄생", 540, 1260, 48, MUTED), {"type": "fade", "at": 6.0}),
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
