"""Generate SVG parts for all 12 scenes of the interest-tax Short (1080x1920).

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
LABEL = "지식 쇼츠 · 이자와 세금"

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


from verify_numbers import ISA_FREE, ISA_FREE_LOW  # noqa: E402


def envelope(cx, cy, w, label):
    h = w * 0.62
    return (f'<rect x="{cx - w / 2}" y="{cy - h / 2}" width="{w}" height="{h}" rx="18" fill="{WHITE}" stroke="{INK}" stroke-width="8"/>'
            f'<path d="M{cx - w / 2} {cy - h / 2 + 10} L{cx} {cy + h * 0.08} L{cx + w / 2} {cy - h / 2 + 10}" fill="none" stroke="{INK}" stroke-width="8" stroke-linejoin="round"/>'
            + text(label, cx, cy + h * 0.38, 54, ORANGE))


def lock(cx, cy, label):
    return (f'<path d="M{cx - 80} {cy - 40} V{cy - 120} A80 80 0 0 1 {cx + 80} {cy - 120} V{cy - 40}" fill="none" stroke="{INK}" stroke-width="26"/>'
            f'<rect x="{cx - 140}" y="{cy - 50}" width="280" height="230" rx="30" fill="{GOLD}" stroke="{GOLD_D}" stroke-width="8"/>'
            + text(label, cx, cy + 100, 96, INK))


# S01 이자 100만 원, 다 내 돈? ----------------------------------------------------------
scene("S01", 0, 5, [
    ("bg", bg_cream(), {"type": "none"}),
    ("title", text("이자 100만 원", 540, 450, 84) + text("다 내 돈일까?", 540, 570, 96, ORANGE), {"type": "pop", "at": 0.0, "anchor": [540, 510]}),
    ("env", envelope(540, 860, 520, "이자 100만 원"), {"type": "pop", "at": 0.3, "anchor": [540, 860]}),
    ("tax", pill("15만 4천 원은 세금", 540, 1200, 64, RED),
     {"type": "stamp", "at": 2.8, "anchor": [540, 1200]}),
])

# S02 15.4% = 14% + 1.4% ------------------------------------------------------------------
scene("S02", 5, 11, [
    ("bg", bg_cream(), {"type": "none"}),
    ("title", text("이자에 붙는 세금", 540, 450, 80), {"type": "pop", "at": 0.0, "anchor": [540, 420]}),
    ("rate", f'<circle cx="540" cy="790" r="240" fill="{RED}"/>' + text("15.4%", 540, 845, 150, WHITE), {"type": "stamp", "at": 0.4, "anchor": [540, 790]}),
    ("parts", pill("소득세 14%", 320, 1150, 50, INK) + text("+", 540, 1168, 60, INK) + pill("지방소득세 1.4%", 770, 1150, 44, INK),
     {"type": "fade", "at": 3.0}),
])

# S03 미리 떼고 준다 -----------------------------------------------------------------------
scene("S03", 11, 18, [
    ("bg", bg_cream(), {"type": "none"}),
    ("title", text("은행이 미리 떼고 줘요", 540, 450, 76), {"type": "pop", "at": 0.0, "anchor": [540, 420]}),
    ("gross", card(90, 560, 900, 180, rx=40) + text("이자", 150, 615, 38, MUTED, "start") + text("100만 원", 930, 705, 76, INK, "end"),
     {"type": "slideR", "at": 0.4}),
    ("cut", card(90, 770, 900, 180, stroke=RED, sw=6, rx=40) + text("세금 (먼저 뗌)", 150, 825, 38, RED, "start")
     + text("− 15만 4천 원", 930, 915, 72, RED, "end"), {"type": "slideR", "at": 1.6}),
    ("net", card(90, 980, 900, 220, stroke=GREEN, sw=8, rx=44) + text("통장에 들어오는 돈", 150, 1040, 38, MUTED, "start")
     + text("84만 6천 원", 930, 1160, 90, GREEN, "end"), {"type": "stamp", "at": 3.4, "anchor": [540, 1090]}),
])

# S04 금융소득 2천만 원 --------------------------------------------------------------------
B4, LINE4 = 1180, 760
scene("S04", 18, 25, [
    ("bg", bg_cream(f'<path d="M150 {B4} H930" stroke="{INK}" stroke-width="6" stroke-linecap="round"/>'
                    + f'<path d="M150 {LINE4} H930" stroke="{RED}" stroke-width="6" stroke-dasharray="26 16"/>'
                    + text("1년 2천만 원", 160, LINE4 - 18, 40, RED, "start")
                    + text("이자 + 배당", 540, B4 + 60, 46)), {"type": "none"}),
    ("title", text("이자와 배당이 많으면?", 540, 450, 76), {"type": "pop", "at": 0.0, "anchor": [540, 420]}),
    ("low", f'<rect x="250" y="{B4 - 8 - 260}" width="200" height="260" rx="16" fill="{GREEN}"/>' + text("15.4%로 끝", 350, B4 - 8 - 290, 44, GREEN),
     {"type": "growY", "at": 0.4, "anchor": [350, B4 - 8], "dur": 0.6, "ease": "decel"}),
    ("high", f'<rect x="630" y="{B4 - 8 - 520}" width="200" height="520" rx="16" fill="{RED}"/>',
     {"type": "growY", "at": 2.0, "anchor": [730, B4 - 8], "dur": 0.8, "ease": "decel"}),
    ("sum", pill("다른 소득과 합산", 730, 600, 44, RED), {"type": "stamp", "at": 3.6, "anchor": [730, 600]}),
])

# S05 세금 줄이는 두 가지 -------------------------------------------------------------------


def num_card(y, n, label, color):
    return (card(120, y - 100, 840, 200, stroke=color, sw=8, rx=44) + f'<circle cx="240" cy="{y}" r="58" fill="{color}"/>'
            + text(str(n), 240, y + 24, 70, WHITE) + text(label, 340, y + 32, 90, color, "start"))


scene("S05", 25, 31, [
    ("bg", bg_cream(), {"type": "none"}),
    ("title", text("세금 줄이는 법", 540, 450, 88), {"type": "pop", "at": 0.0, "anchor": [540, 420]}),
    ("c1", num_card(700, 1, "ISA", GREEN), {"type": "slideL", "at": 2.8}),
    ("c2", num_card(960, 2, "상호금융", ORANGE), {"type": "slideR", "at": 3.4}),
])

# S06 ISA ---------------------------------------------------------------------------


def isa_row(y, left, right, color):
    return card(100, y - 75, 880, 150, rx=36) + text(left, 150, y + 16, 46, MUTED, "start") + text(right, 930, y + 22, 64, color, "end")


scene("S06", 31, 41, [
    ("bg", bg_cream(), {"type": "none"}),
    ("title", pill("① ISA 계좌", 540, 440, 72, GREEN), {"type": "pop", "at": 0.0, "anchor": [540, 440]}),
    ("r1", isa_row(640, f"이익 {ISA_FREE // 10000}만 원까지", "세금 0원", GREEN), {"type": "slideR", "at": 2.8}),
    ("r2", isa_row(830, f"서민형 {ISA_FREE_LOW // 10000}만 원까지", "세금 0원", GREEN), {"type": "slideR", "at": 5.2}),
    ("r3", isa_row(1020, "넘는 부분", "9.9%만", ORANGE), {"type": "slideR", "at": 6.8}),
])

# S07 3년 유지 -----------------------------------------------------------------------------
scene("S07", 41, 47, [
    ("bg", bg_cream(), {"type": "none"}),
    ("title", text("단, 3년은 유지", 540, 450, 84), {"type": "pop", "at": 0.0, "anchor": [540, 420]}),
    ("lock", lock(540, 820, "3년"), {"type": "pop", "at": 0.4, "anchor": [540, 820]}),
    ("break", pill("중간에 깨면 혜택 X", 540, 1180, 62, RED), {"type": "stamp", "at": 2.8, "anchor": [540, 1180]}),
])

# S08 상호금융 3천만 원 1.4% ------------------------------------------------------------------
scene("S08", 47, 55, [
    ("bg", bg_cream(), {"type": "none"}),
    ("title", pill("② 상호금융", 540, 440, 72, ORANGE), {"type": "pop", "at": 0.0, "anchor": [540, 440]}),
    ("signs", pill("농협", 260, 620, 56, GREEN) + pill("신협", 540, 620, 56, "#3b82c4") + pill("새마을금고", 830, 620, 48, RED),
     {"type": "pop", "at": 0.6, "anchor": [540, 620]}),
    ("deal", card(90, 760, 900, 360, stroke=ORANGE, sw=8, rx=44) + text("조합원이 되면", 540, 850, 50, MUTED)
     + text("3천만 원까지", 540, 960, 80, INK) + text("세금 1.4%", 540, 1080, 96, ORANGE), {"type": "stamp", "at": 3.8, "anchor": [540, 940]}),
])

# S09 2026년부터 고소득 준조합원은 세금 증가 -----------------------------------------------------
scene("S09", 55, 62, [
    ("bg", bg_cream(), {"type": "none"}),
    ("title", pill("2026년부터", 540, 440, 66, INK), {"type": "pop", "at": 0.0, "anchor": [540, 440]}),
    ("who", card(90, 580, 900, 260, rx=40) + text("소득이 높은", 540, 690, 60, MUTED) + text("준조합원은", 540, 790, 76, INK),
     {"type": "pop", "at": 0.6, "anchor": [540, 710]}),
    ("up", arrow(540, 1200, 540, 960, RED, 18) + text("세금 늘어남", 620, 1110, 70, RED, "start"), {"type": "slideU", "at": 3.6}),
])

# S10 정리 ---------------------------------------------------------------------------
scene("S10", 62, 70, [
    ("bg", bg_cream(), {"type": "none"}),
    ("badge", pill("정리", 540, 430, 64, ORANGE), {"type": "pop", "at": 0.0, "anchor": [540, 430]}),
    ("rate", card(80, 560, 920, 260, stroke=RED, sw=8, rx=44) + text("이자에는", 540, 650, 52, MUTED) + text("15.4%", 540, 780, 110, RED),
     {"type": "pop", "at": 0.4, "anchor": [540, 690]}),
    ("save", card(80, 880, 920, 300, rx=44) + text("세금 줄이기", 540, 970, 50, MUTED) + text("ISA", 300, 1110, 100, GREEN)
     + text("상호금융", 760, 1110, 90, ORANGE), {"type": "pop", "at": 3.6, "anchor": [540, 1030]}),
])

# S11 퀴즈 ---------------------------------------------------------------------------
spots = [(140 + i * 66, 1010 + (i % 3) * 14) for i in range(13)] + [(60 + (i % 2) * 22, 820 + i * 50) for i in range(6)] \
    + [(990 + (i % 2) * 22, 820 + i * 50) for i in range(6)]
scene("S11", 70, 80, [
    ("bg", bg_cream(), {"type": "none"}),
    ("badge", pill("퀴즈", 540, 420, 64, ORANGE), {"type": "pop", "at": 0.0, "anchor": [540, 420]}),
    ("question", text("이자 50만 원", 540, 590, 84) + text("세금 떼면 얼마?", 540, 700, 76), {"type": "pop", "at": 0.3, "anchor": [540, 640]}),
    ("formula", text("50만 − 7만 7천", 540, 870, 86), {"type": "pop", "at": 1.6, "anchor": [540, 835]}),
    ("answer", pill("= 42만 3천 원", 540, 1060, 96, GREEN), {"type": "stamp", "at": 3.4, "anchor": [540, 1060]}),
    ("confetti", confetti_at(spots), {"type": "drop", "at": 3.6}),
])

# S12 상품설명서 확인 + 구독 -------------------------------------------------------------------
button = (f'<rect x="290" y="900" width="500" height="170" rx="85" fill="{RED}"/>'
          f'<path d="M405 935 C375 935 368 965 368 990 L360 1020 H450 L442 990 C442 965 435 935 405 935 Z M392 1030 a13 13 0 0 0 26 0 Z" fill="{WHITE}"/>'
          + text("구독", 600, 1018, 92, WHITE))
finger = (f'<path d="M700 1045 V1150 C700 1180 740 1200 770 1200 H820 C850 1200 870 1170 870 1140 V1100 C870 1085 845 1080 835 1095 '
          f'C835 1075 810 1070 800 1088 C800 1070 775 1065 765 1085 V1045 C765 1020 700 1020 700 1045 Z" fill="#f6d2b3" stroke="{INK}" stroke-width="6"/>')
scene("S12", 80, 90, [
    ("bg", bg_cream(), {"type": "none"}),
    ("check", card(90, 400, 900, 300, stroke=GREEN, sw=8, rx=44) + text("가입 전엔", 540, 500, 56, MUTED)
     + text("상품설명서 확인!", 540, 630, 84, GREEN), {"type": "pop", "at": 0.2, "anchor": [540, 550]}),
    ("button", button, {"type": "pop", "at": 4.8, "anchor": [540, 985]}),
    ("finger", finger, {"type": "tap", "at": 5.6, "anchor": [785, 1120]}),
    ("prev", text("지난 편: 은행의 돈벌이", 540, 1260, 48, MUTED), {"type": "fade", "at": 6.0}),
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
