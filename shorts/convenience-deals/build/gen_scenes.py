"""Generate SVG parts for all 8 scenes of the convenience-deals Short (60 s) (1080x1920).

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


def cross(cx, cy, w, h):
    return (f'<path d="M{cx - w / 2} {cy - h / 2} L{cx + w / 2} {cy + h / 2} M{cx + w / 2} {cy - h / 2} L{cx - w / 2} {cy + h / 2}" '
            f'stroke="{RED}" stroke-width="18" stroke-linecap="round"/>')


def can(cx, cy, color, s=1.0, label=""):
    """A drink can: body, top rim and a label band."""
    w, h = 110 * s, 200 * s
    return (f'<rect x="{cx - w / 2:.0f}" y="{cy - h / 2:.0f}" width="{w:.0f}" height="{h:.0f}" rx="{18 * s:.0f}" fill="{color}" stroke="{PLUM}" stroke-width="5"/>'
            f'<rect x="{cx - w / 2 + 8 * s:.0f}" y="{cy - h / 2 - 10 * s:.0f}" width="{w - 16 * s:.0f}" height="{16 * s:.0f}" rx="6" fill="#d9d9d9" stroke="{PLUM}" stroke-width="4"/>'
            f'<rect x="{cx - w / 2:.0f}" y="{cy - 22 * s:.0f}" width="{w:.0f}" height="{44 * s:.0f}" fill="{WHITE}" fill-opacity="0.85"/>'
            + (text(label, cx, cy + 14 * s, 34 * s, PLUM, font=HEAD) if label else ""))


def bars(rows, y0, full=560, x=300):
    """Price comparison bars: (label, value text, fraction, colour)."""
    out = ""
    for i, (label, value, frac, col) in enumerate(rows):
        y = y0 + i * 150
        out += (text(label, x - 30, y + 58, 50, INK, "end")
                + f'<rect x="{x}" y="{y}" width="{full * frac:.0f}" height="80" rx="16" fill="{col}"/>'
                + num(value, x + full * frac + 20, y + 62, 56, col, "start"))
    return out


# S01 1+1, 무조건 이득? ------------------------------------------------------------------------------
scene("S01", 0, 4.4, [
    ai(4.4, (104, 116), (0, 30)),
    ("bg", bg(), {"type": "none"}),
    ("title", head("편의점 1+1,", 540, 400, 120) + head("무조건 이득일까?", 540, 540, 104, YELLOW), {"type": "pop", "at": 0.0, "anchor": [540, 470]}),
    ("cans", can(400, 1110, RED, 1.3) + num("+", 540, 1140, 100, PLUM) + can(680, 1110, RED, 1.3), {"type": "pop", "at": 0.6, "anchor": [540, 1110]}),
    ("free", pill("하나는 공짜?", 680, 1320, 52, YELLOW, PLUM), {"type": "stamp", "at": 2.4, "anchor": [680, 1320]}),
])

# S02 반값 · 그런데 정가는? -----------------------------------------------------------------------------
scene("S02", 4.4, 11.2, [
    ai(6.8, (114, 104), (-30, 0)),
    ("bg", bg(), {"type": "none"}),
    ("title", head("1+1 = 반값", 540, 430, 120), {"type": "pop", "at": 0.0, "anchor": [540, 410]}),
    ("half", card(110, 600, 860, 380) + text("한 개 값에 두 개", 540, 690, 50, INK) + num("개당 50% 할인", 540, 870, 110, TEAL), {"type": "pop", "at": 0.4, "anchor": [540, 790]}),
    ("but", pill("그런데 정가는?", 540, 1180, 60, RED, WHITE), {"type": "stamp", "at": 3.8, "anchor": [540, 1180]}),
])

# S03 편의점이 약 37% 더 비쌌다 -------------------------------------------------------------------------------
scene("S03", 11.2, 18.6, [
    ai(7.4, (106, 118), (30, -20)),
    ("bg", bg(), {"type": "none"}),
    ("title", head("같은 상품 10개 총액", 540, 430, 96), {"type": "pop", "at": 0.0, "anchor": [540, 410]}),
    ("cmp", card(90, 580, 900, 460) + text("한국소비자원 조사 (2020년)", 540, 660, 40, INK)
     + bars([("마트", "19,972원", 0.73 * 0.8, TEAL), ("편의점", "27,325원", 1.0 * 0.8, RED)], 730, 520, 270), {"type": "wipeL", "at": 0.4, "dur": 1.6}),
    ("pct", pill("편의점이 약 37% 더 비쌈", 540, 1130, 56, RED, WHITE), {"type": "stamp", "at": 3.0, "anchor": [540, 1130]}),
    ("same", pill("1+1이어도 마트와 큰 차이 없을 수도", 540, 1270, 42, PLUM, WHITE), {"type": "fade", "at": 4.0}),
])

# S04 2+1의 함정 -------------------------------------------------------------------------------------------
scene("S04", 18.6, 24.0, [
    ai(5.4, (112, 104), (0, 30)),
    ("bg", bg(), {"type": "none"}),
    ("title", head("2+1은 더 조심", 540, 430, 116), {"type": "pop", "at": 0.0, "anchor": [540, 410]}),
    ("three", card(110, 600, 860, 460) + text("세 개를 다 사야 할인", 540, 690, 50, INK)
     + can(330, 870, TEAL, 1.2) + can(540, 870, TEAL, 1.2) + can(750, 870, TEAL, 1.2, "공짜"), {"type": "pop", "at": 0.4, "anchor": [540, 830]}),
    ("twice", pill("하나만 필요했다면 = 돈 2배", 540, 1180, 52, RED, WHITE), {"type": "stamp", "at": 3.4, "anchor": [540, 1180]}),
])

# S05 공짜의 힘 ------------------------------------------------------------------------------------------
choc = lambda cx, cy, col, price, lab: (card(cx - 170, cy - 200, 340, 400) + f'<circle cx="{cx}" cy="{cy - 50}" r="70" fill="{col}" stroke="{PLUM}" stroke-width="5"/>'
                                         + text(lab, cx, cy + 70, 40, INK) + num(price, cx, cy + 150, 64, RED))
scene("S05", 24.0, 32.8, [
    ai(8.8, (104, 116), (-30, 20)),
    ("bg", bg(), {"type": "none"}),
    ("title", head("공짜의 힘", 540, 430, 120), {"type": "pop", "at": 0.0, "anchor": [540, 410]}),
    ("exp", text("미국 MIT 실험 (2007년)", 540, 530, 44, WHITE), {"type": "fade", "at": 0.3}),
    ("pair", choc(330, 820, "#8b5a2b", "1센트", "보통 초콜릿") + choc(750, 820, "#3b2416", "15센트", "고급 초콜릿"), {"type": "pop", "at": 2.4, "anchor": [540, 820]}),
    # both prices drop by one cent: 1 -> free, 15 -> 14 (the version in Ariely's write-up)
    ("zero", f'<rect x="200" y="905" width="260" height="90" rx="20" fill="{CARD}"/>' + num("공짜!", 330, 975, 72, TEAL)
     + f'<rect x="620" y="905" width="260" height="90" rx="20" fill="{CARD}"/>' + num("14센트", 750, 975, 64, RED), {"type": "stamp", "at": 4.0, "anchor": [540, 950]}),
    ("more", pill("공짜를 고른 사람 크게 늘어", 540, 1170, 52, RED, WHITE), {"type": "stamp", "at": 5.6, "anchor": [540, 1170]}),
])

# S06 행사 직전 가격 인상 -------------------------------------------------------------------------------------
scene("S06", 32.8, 41.2, [
    ai(8.4, (110, 120), (0, -30)),
    ("bg", bg(), {"type": "none"}),
    ("title", head("값 올리고 1+1?", 540, 430, 110), {"type": "pop", "at": 0.0, "anchor": [540, 410]}),
    ("oil", card(110, 590, 860, 440) + tag("참기름 한 병", 540, 670, 44, TEAL) + num("4,750원", 330, 840, 80, INK) + num("→", 540, 840, 80, PLUM)
     + num("9,500원", 760, 840, 80, RED) + text("값을 두 배로 올린 뒤 1+1", 540, 960, 48, INK), {"type": "pop", "at": 0.6, "anchor": [540, 810]}),
    ("fine", pill("공정위, 대형마트 4곳 과징금 (2016년)", 540, 1170, 46, RED, WHITE), {"type": "stamp", "at": 5.8, "anchor": [540, 1170]}),
])

# S07 퀴즈: 2+1은 몇 % 할인? ---------------------------------------------------------------------------------
choices = "".join(card(130 + i * 280, 760, 240, 200) + num(w, 250 + i * 280, 885, 76, INK) for i, w in enumerate(("50%", "33%", "25%")))
scene("S07", 41.2, 50.4, [
    ai(9.2, (106, 120), (0, -30)),
    ("bg", bg(), {"type": "none"}),
    ("badge", pill("퀴즈", 540, 340, 56, RED, WHITE), {"type": "pop", "at": 0.0, "anchor": [540, 340]}),
    ("question", head("2+1으로 사면", 540, 490, 96) + head("개당 몇 % 할인?", 540, 610, 96, YELLOW), {"type": "pop", "at": 0.3, "anchor": [540, 550]}),
    ("choices", choices, {"type": "pop", "at": 0.8, "anchor": [540, 860]}),
    ("answer", f'<rect x="402" y="748" width="276" height="224" rx="40" fill="none" stroke="{RED}" stroke-width="12"/>' + pill("정답 · 약 33%", 540, 1060, 56, RED, WHITE),
     {"type": "stamp", "at": 4.0, "anchor": [540, 860]}),
    ("why", pill("세 개를 두 개 값에", 540, 1230, 46, TEAL, WHITE), {"type": "fade", "at": 6.6}),
])

# S08 마무리 + 구독 --------------------------------------------------------------------------------------
finger = (f'<path d="M700 1145 V1250 C700 1280 740 1300 770 1300 H820 C850 1300 870 1270 870 1240 V1200 C870 1185 845 1180 835 1195 '
          f'C835 1175 810 1170 800 1188 C800 1170 775 1165 765 1185 V1145 C765 1120 700 1120 700 1145 Z" fill="#f6d2b3" stroke="{PLUM}" stroke-width="6"/>')
scene("S08", 50.4, 60.0, [
    ai(9.6, (110, 100), (0, 0)),
    ("bg", bg(), {"type": "none"}),
    ("look", head("필요한 만큼만,", 540, 430, 100) + head("한 개 가격 따지기", 540, 560, 100, YELLOW), {"type": "pop", "at": 0.2, "anchor": [540, 500]}),
    ("button", pill("구독하기", 540, 1080, 80, RED, WHITE), {"type": "pop", "at": 3.6, "anchor": [540, 1080]}),
    ("finger", finger, {"type": "tap", "at": 4.2, "anchor": [785, 1220]}),
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
