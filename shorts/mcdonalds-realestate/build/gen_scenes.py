"""Generate SVG parts for all 8 scenes of the mcdonalds-realestate Short (60 s) (1080x1920).

Style (episode 13 on): 3D clay AI paintings mixed with a minimal infographic. Each scene's bottom
layer is a clay painting (Seedream 4.0 via RunPod, gen_backgrounds_seedream.py) (ai_bg/Sxx.png) that drifts slowly (kenburns); over it a teal
gradient carries the Jua headline, and the numbers sit on off-white infographic cards with big
Black Han Sans figures, a teal/red palette and Do Hyeon labels. Subtitles use Do Hyeon.

Each scene is a list of parts; each part becomes its own full-frame SVG so the exported PNG
layers line up in EffectCraft. A manifest records the timing and animation hints.
"""
import json
import os

W, H = 1080, 1920
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "svg")
LABEL = "지식 쇼츠 · 돈과 생활"

# fonts
HEAD, NUM, NOTE = "Jua", "Black Han Sans", "Do Hyeon"
FONT = NOTE  # subtitles

# palette
TEAL, TEAL_D = "#1f7a6d", "#2f5d6a"
RED, INK, CARD = "#e4572e", "#1d1d1f", "#f5f3ee"
YELLOW, WHITE, PLUM = "#ffd166", "#ffffff", "#3a2a4a"


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


def text(s, x, y, size, fill=INK, anchor="middle", font=NOTE, extra=""):
    assert text_width(s, size) < 1000, f"text too wide: {s}"
    s = s.replace("&", "&amp;").replace("<", "&lt;")
    return (f'<text x="{x}" y="{y}" font-family="{font}" font-size="{size}" '
            f'fill="{fill}" text-anchor="{anchor}" {extra}>{s}</text>')


def head(s, x, y, size, fill=WHITE, anchor="middle"):
    """Clay-friendly headline: Jua with a thick plum outline."""
    return text(s, x, y, size, fill, anchor, HEAD, f'stroke="{PLUM}" stroke-width="12" paint-order="stroke" stroke-linejoin="round"')


def num(s, x, y, size, fill=INK, anchor="middle"):
    return text(s, x, y, size, fill, anchor, NUM)


def pill(s, cx, cy, size=38, bg=YELLOW, fg=PLUM, font=HEAD):
    w = text_width(s, size) + 70
    h = size * 1.8
    return (f'<rect x="{cx - w / 2:.1f}" y="{cy - h / 2:.1f}" width="{w:.1f}" height="{h:.1f}" rx="{h / 2:.1f}" fill="{bg}"/>'
            + text(s, cx, cy + size * 0.36, size, fg, "middle", font))


def card(x, y, w, h, fill=CARD, rx=34):
    """Infographic card: off-white, rounded, soft drop shadow."""
    return (f'<rect x="{x + 6}" y="{y + 12}" width="{w}" height="{h}" rx="{rx}" fill="#000000" fill-opacity="0.18"/>'
            f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{fill}" fill-opacity="0.96"/>')


def tag(s, cx, cy, size=44, bg=INK, fg=WHITE):
    """Flat label chip (infographic)."""
    w = text_width(s, size) + 60
    return (f'<rect x="{cx - w / 2:.1f}" y="{cy - size * 0.85:.1f}" width="{w:.1f}" height="{size * 1.7:.1f}" rx="14" fill="{bg}"/>'
            + text(s, cx, cy + size * 0.36, size, fg, "middle", NOTE))


def svg(body):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">'
            f'<rect x="0" y="0" width="{W}" height="{H}" fill="#000000" fill-opacity="0"/>{body}</svg>')


def bg():
    """Teal gradient at the top for the headline, a soft one at the bottom for the subtitle, label pill."""
    return (f'<defs><linearGradient id="top" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{TEAL_D}" stop-opacity="0.85"/>'
            f'<stop offset="1" stop-color="{TEAL_D}" stop-opacity="0"/></linearGradient>'
            f'<linearGradient id="bot" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{TEAL_D}" stop-opacity="0"/>'
            f'<stop offset="1" stop-color="{TEAL_D}" stop-opacity="0.55"/></linearGradient></defs>'
            f'<rect x="0" y="0" width="{W}" height="720" fill="url(#top)"/>'
            f'<rect x="0" y="1300" width="{W}" height="620" fill="url(#bot)"/>'
            + pill(LABEL, 540, 200))


def ai(dur, z=(106, 116), pan=(0, 0)):
    """Bottom layer: the scene's clay painting (written by compose_bg.py) with a slow camera move."""
    return ("ai", "", {"type": "kenburns", "dur": dur, "z": z, "pan": pan})


# ---------------------------------------------------------------- scenes
scenes = []


def scene(sid, start, end, parts):
    scenes.append({"id": sid, "start": start, "end": end, "parts": parts})


def coins(cx, base, n, color=YELLOW):
    return "".join(f'<ellipse cx="{cx}" cy="{base - i * 24}" rx="90" ry="26" fill="{color}" stroke="{PLUM}" stroke-width="5"/>' for i in range(n))


def bars(rows, y0, full=520, x=300):
    """Horizontal value bars: (label, value text, fraction, colour)."""
    out = ""
    for i, (label, value, frac, col) in enumerate(rows):
        y = y0 + i * 150
        out += (text(label, x - 30, y + 56, 50, INK, "end")
                + f'<rect x="{x}" y="{y}" width="{full * frac:.0f}" height="80" rx="16" fill="{col}"/>'
                + num(value, x + full * frac + 18, y + 60, 54, INK if col == YELLOW else col, "start"))
    return out


def arrow(x1, y1, x2, y2, col=PLUM, w=10):
    import math
    a = math.atan2(y2 - y1, x2 - x1)
    p1 = (x2 - 34 * math.cos(a - 0.5), y2 - 34 * math.sin(a - 0.5))
    p2 = (x2 - 34 * math.cos(a + 0.5), y2 - 34 * math.sin(a + 0.5))
    return (f'<path d="M{x1} {y1} L{x2} {y2} M{p1[0]:.0f} {p1[1]:.0f} L{x2} {y2} L{p2[0]:.0f} {p2[1]:.0f}" '
            f'fill="none" stroke="{col}" stroke-width="{w}" stroke-linecap="round" stroke-linejoin="round"/>')


def box(cx, cy, label, col=TEAL, w=300, h=120, size=50):
    return (f'<rect x="{cx - w / 2}" y="{cy - h / 2}" width="{w}" height="{h}" rx="24" fill="{col}"/>'
            + text(label, cx, cy + size * 0.36, size, WHITE, font=HEAD))


# S01 햄버거로 돈 벌까? ------------------------------------------------------------------------------
scene("S01", 0, 5.0, [
    ai(5.0, (104, 116), (0, 30)),
    ("bg", bg(), {"type": "none"}),
    ("title", head("맥도날드는 햄버거로", 540, 400, 96) + head("돈을 벌까?", 540, 540, 120, YELLOW), {"type": "pop", "at": 0.0, "anchor": [540, 470]}),
    ("no", pill("놀랍게도 아니다", 540, 1250, 60, RED, WHITE), {"type": "stamp", "at": 3.6, "anchor": [540, 1250]}),
])

# S02 가맹점 → 로열티 + 임대료 --------------------------------------------------------------------------------
scene("S02", 5.0, 10.4, [
    ai(5.4, (114, 104), (-30, 0)),
    ("bg", bg(), {"type": "none"}),
    ("title", head("매장 대부분은 가맹점", 540, 430, 96), {"type": "pop", "at": 0.0, "anchor": [540, 410]}),
    ("flow", card(110, 600, 860, 520) + box(540, 700, "본사", PLUM, 280) + box(540, 1020, "가맹점", TEAL, 320)
     + arrow(400, 950, 400, 790, RED) + arrow(680, 950, 680, 790, RED)
     + text("로열티", 300, 880, 46, INK) + text("임대료", 780, 880, 46, RED, font=HEAD), {"type": "pop", "at": 0.4, "anchor": [540, 860]}),
])

# S03 임대료 > 로열티 -------------------------------------------------------------------------------------
scene("S03", 10.4, 16.8, [
    ai(6.4, (106, 118), (30, -20)),
    ("bg", bg(), {"type": "none"}),
    ("title", head("더 큰 돈은 임대료", 540, 430, 104), {"type": "pop", "at": 0.0, "anchor": [540, 410]}),
    ("bars", card(90, 600, 900, 440) + text("가맹점에서 받은 돈 (2024년 연차보고서)", 540, 680, 40, INK)
     + bars([("임대료", "100억 달러", 0.95 * 0.62, RED), ("로열티", "56억 달러", 0.53 * 0.62, TEAL)], 750, 600, 290),
     {"type": "wipeL", "at": 0.3, "dur": 1.8}),
    ("x2", pill("로열티의 두 배 가까이", 540, 1140, 56, RED, WHITE), {"type": "stamp", "at": 3.4, "anchor": [540, 1140]}),
])

# S04 소네본의 아이디어 ------------------------------------------------------------------------------------
scene("S04", 16.8, 24.6, [
    ai(7.8, (112, 104), (0, 30)),
    ("bg", bg(), {"type": "none"}),
    ("title", head("1950년대의 아이디어", 540, 430, 100), {"type": "pop", "at": 0.0, "anchor": [540, 410]}),
    ("who", tag("재무 담당 해리 소네본", 540, 560, 44, PLUM), {"type": "fade", "at": 0.6}),
    ("steps", card(110, 640, 860, 560) + box(540, 730, "본사가 땅 · 건물 확보", TEAL, 640, 110, 48)
     + arrow(540, 800, 540, 880) + box(540, 950, "점주에게 더 비싸게 임대", RED, 640, 110, 48)
     + text("사거나 빌린 뒤 다시 빌려줌", 540, 1110, 44, INK), {"type": "wipeD", "at": 3.4, "dur": 1.4}),
])

# S05 매출 연동 임대료 ------------------------------------------------------------------------------------
scene("S05", 24.6, 30.8, [
    ai(6.2, (104, 116), (-30, 20)),
    ("bg", bg(), {"type": "none"}),
    ("title", head("임대료 = 매출 × %", 540, 430, 110), {"type": "pop", "at": 0.0, "anchor": [540, 410]}),
    ("rule", card(110, 600, 860, 380) + text("점주는 매출의 일정 비율을", 540, 700, 52, INK) + num("임대료로", 540, 820, 100, RED)
     + text("(최저 임대료도 있음)", 540, 920, 38, INK), {"type": "pop", "at": 0.4, "anchor": [540, 790]}),
    ("up", pill("잘 팔릴수록 본사 임대료 ↑", 540, 1120, 54, PLUM, WHITE), {"type": "stamp", "at": 3.0, "anchor": [540, 1120]}),
])

# S06 영화 「파운더」 대사 -----------------------------------------------------------------------------------
scene("S06", 30.8, 36.6, [
    ai(5.8, (110, 120), (0, -30)),
    ("bg", bg(), {"type": "none"}),
    ("title", head("영화 속 한마디", 540, 430, 110), {"type": "pop", "at": 0.0, "anchor": [540, 410]}),
    ("quote", card(110, 600, 860, 480) + text("“", 190, 720, 160, RED, font=NUM) + text("우리는 햄버거가 아니라", 540, 780, 60, INK, font=HEAD)
     + text("부동산 사업을 한다", 540, 880, 76, RED, font=HEAD) + text("영화 「파운더」(2016) 속 대사", 540, 1010, 40, INK),
     {"type": "pop", "at": 2.0, "anchor": [540, 840]}),
])

# S07 퀴즈: 직영점은 몇 %? ---------------------------------------------------------------------------------
choices = "".join(card(130 + i * 280, 760, 240, 200) + num(w, 250 + i * 280, 885, 76, INK) for i, w in enumerate(("5%", "50%", "95%")))
scene("S07", 36.6, 46.4, [
    ai(9.8, (106, 120), (0, -30)),
    ("bg", bg(), {"type": "none"}),
    ("badge", pill("퀴즈", 540, 340, 56, RED, WHITE), {"type": "pop", "at": 0.0, "anchor": [540, 340]}),
    ("question", head("본사가 직접 운영하는", 540, 490, 90) + head("매장은 몇 %?", 540, 610, 100, YELLOW), {"type": "pop", "at": 0.3, "anchor": [540, 550]}),
    ("choices", choices, {"type": "pop", "at": 0.8, "anchor": [540, 860]}),
    ("answer", f'<rect x="122" y="748" width="276" height="224" rx="40" fill="none" stroke="{RED}" stroke-width="12"/>' + pill("정답 · 약 5%", 540, 1060, 56, RED, WHITE),
     {"type": "stamp", "at": 4.4, "anchor": [260, 860]}),
    ("why", pill("나머지 약 95%는 가맹점 (2025년 말)", 540, 1230, 44, TEAL, WHITE), {"type": "fade", "at": 6.6}),
])

# S08 마무리 + 구독 --------------------------------------------------------------------------------------
finger = (f'<path d="M700 1145 V1250 C700 1280 740 1300 770 1300 H820 C850 1300 870 1270 870 1240 V1200 C870 1185 845 1180 835 1195 '
          f'C835 1175 810 1170 800 1188 C800 1170 775 1165 765 1185 V1145 C765 1120 700 1120 700 1145 Z" fill="#f6d2b3" stroke="{PLUM}" stroke-width="6"/>')
scene("S08", 46.4, 60.0, [
    ai(13.6, (110, 100), (0, 0)),
    ("bg", bg(), {"type": "none"}),
    ("look", head("햄버거 가게?", 540, 430, 110) + head("사실은 땅 주인", 540, 560, 110, YELLOW), {"type": "pop", "at": 0.2, "anchor": [540, 500]}),
    ("button", pill("구독하기", 540, 1080, 80, RED, WHITE), {"type": "pop", "at": 4.0, "anchor": [540, 1080]}),
    ("finger", finger, {"type": "tap", "at": 4.6, "anchor": [785, 1220]}),
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
