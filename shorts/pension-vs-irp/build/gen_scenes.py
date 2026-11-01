"""Generate SVG parts for all 8 scenes of the pension-vs-irp Short (60 s) (1080x1920).

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


def versus(topic, left, right, y=600, h=420, lcol=TEAL, rcol=RED, size=56):
    """Two-column comparison card: topic chip on top, 연금저축 on the left, IRP on the right."""
    out = card(90, y, 900, h) + tag(topic, 540, y + 80, 44, PLUM)
    out += f'<path d="M540 {y + 140} V{y + h - 40}" stroke="{INK}" stroke-opacity="0.15" stroke-width="4"/>'
    out += text("연금저축", 315, y + 200, 44, lcol, font=HEAD) + text("IRP", 765, y + 200, 48, rcol, font=HEAD)
    for i, line in enumerate(left):
        out += num(line, 315, y + 290 + i * 76, size, INK)
    for i, line in enumerate(right):
        out += num(line, 765, y + 290 + i * 76, size, INK)
    return out


def jar(cx, cy, label, col):
    return (f'<rect x="{cx - 130}" y="{cy - 150}" width="260" height="300" rx="60" fill="{CARD}" stroke="{PLUM}" stroke-width="8"/>'
            f'<rect x="{cx - 90}" y="{cy - 190}" width="180" height="50" rx="16" fill="{col}" stroke="{PLUM}" stroke-width="6"/>'
            + coins(cx, cy + 110, 4) + text(label, cx, cy - 40, 52, col, font=HEAD))


# S01 연금저축 vs IRP ---------------------------------------------------------------------------------
scene("S01", 0, 4.8, [
    ai(4.8, (104, 116), (0, 30)),
    ("bg", bg(), {"type": "none"}),
    ("title", head("연금저축 vs IRP", 540, 400, 110) + head("뭐가 다를까?", 540, 540, 110, YELLOW), {"type": "pop", "at": 0.0, "anchor": [540, 470]}),
    ("names", pill("연금저축", 300, 1250, 56, TEAL, WHITE) + num("vs", 540, 1275, 80, PLUM) + pill("IRP", 780, 1250, 56, RED, WHITE), {"type": "pop", "at": 0.8, "anchor": [540, 1250]}),
])

# S02 세액공제 한도 -----------------------------------------------------------------------------------
scene("S02", 4.8, 10.4, [
    ai(5.6, (114, 104), (-30, 0)),
    ("bg", bg(), {"type": "none"}),
    ("title", head("세액공제는 합쳐서", 540, 430, 104), {"type": "pop", "at": 0.0, "anchor": [540, 410]}),
    ("total", card(110, 600, 860, 300) + text("연금저축 + IRP", 540, 690, 50, INK) + num("900만 원", 540, 840, 130, RED), {"type": "pop", "at": 0.3, "anchor": [540, 750]}),
    ("solo", pill("연금저축 혼자는 600만 원까지", 540, 1000, 52, TEAL, WHITE), {"type": "stamp", "at": 3.0, "anchor": [540, 1000]}),
])

# S03 가입 자격 ------------------------------------------------------------------------------------------
scene("S03", 10.4, 15.6, [
    ai(5.2, (106, 118), (30, -20)),
    ("bg", bg(), {"type": "none"}),
    ("title", head("① 가입 자격", 540, 430, 116), {"type": "pop", "at": 0.0, "anchor": [540, 410]}),
    ("vs", versus("누가 가입할 수 있나", ["누구나"], ["소득 있는", "사람만"]), {"type": "pop", "at": 0.4, "anchor": [540, 810]}),
])

# S04 돈 꺼내기 ------------------------------------------------------------------------------------------
scene("S04", 15.6, 23.6, [
    ai(8.0, (112, 104), (0, 30)),
    ("bg", bg(), {"type": "none"}),
    ("title", head("② 돈 꺼내기", 540, 430, 116), {"type": "pop", "at": 0.0, "anchor": [540, 410]}),
    ("vs", versus("중간에 꺼낼 때", ["일부만", "인출 가능"], ["사유 없으면", "전액 해지"], h=500, size=52), {"type": "wipeL", "at": 0.4, "dur": 4.4}),
    ("tax", pill("공제받은 돈을 빼면 둘 다 16.5% 세금", 540, 1180, 44, PLUM, WHITE), {"type": "fade", "at": 5.4}),
])

# S05 투자 제한 ------------------------------------------------------------------------------------------
scene("S05", 23.6, 30.0, [
    ai(6.4, (104, 116), (-30, 20)),
    ("bg", bg(), {"type": "none"}),
    ("title", head("③ 투자 제한", 540, 430, 116), {"type": "pop", "at": 0.0, "anchor": [540, 410]}),
    ("vs", versus("주식 같은 위험자산", ["제한 없음", "(연금저축펀드)"], ["70%까지", "(30%는 안전자산)"], h=500, size=50), {"type": "wipeL", "at": 0.4, "dur": 3.6}),
])

# S06 IRP의 장점: 퇴직금 ------------------------------------------------------------------------------------
scene("S06", 30.0, 33.6, [
    ai(3.6, (110, 120), (0, -30)),
    ("bg", bg(), {"type": "none"}),
    ("title", head("IRP만의 장점", 540, 430, 110), {"type": "pop", "at": 0.0, "anchor": [540, 410]}),
    ("ret", card(110, 980, 860, 300) + tag("퇴직금을 받는 통장", 540, 1070, 46, RED) + text("연금으로 나눠 받으면 퇴직소득세도 줄어요", 540, 1200, 44, INK),
     {"type": "pop", "at": 0.3, "anchor": [540, 1130]}),
])

# S07 퀴즈: 연금저축에만 900만 원이면? ---------------------------------------------------------------------
choices = "".join(card(110 + i * 300, 760, 260, 200) + num(w, 240 + i * 300, 885, 64, INK) for i, w in enumerate(("300만", "600만", "900만")))
scene("S07", 33.6, 44.0, [
    ai(10.4, (106, 120), (0, -30)),
    ("bg", bg(), {"type": "none"}),
    ("badge", pill("퀴즈", 540, 340, 56, RED, WHITE), {"type": "pop", "at": 0.0, "anchor": [540, 340]}),
    ("question", head("연금저축에만 900만 원", 540, 490, 88) + head("공제는 얼마까지?", 540, 610, 96, YELLOW), {"type": "pop", "at": 0.3, "anchor": [540, 550]}),
    ("choices", choices, {"type": "pop", "at": 0.8, "anchor": [540, 860]}),
    ("answer", f'<rect x="398" y="748" width="284" height="224" rx="40" fill="none" stroke="{RED}" stroke-width="12"/>' + pill("정답 · 600만 원", 540, 1060, 56, RED, WHITE),
     {"type": "stamp", "at": 3.8, "anchor": [540, 860]}),
    ("why", pill("남은 300만 원은 IRP로", 540, 1230, 48, TEAL, WHITE), {"type": "fade", "at": 8.0}),
])

# S08 마무리 + 구독 --------------------------------------------------------------------------------------
finger = (f'<path d="M700 1145 V1250 C700 1280 740 1300 770 1300 H820 C850 1300 870 1270 870 1240 V1200 C870 1185 845 1180 835 1195 '
          f'C835 1175 810 1170 800 1188 C800 1170 775 1165 765 1185 V1145 C765 1120 700 1120 700 1145 Z" fill="#f6d2b3" stroke="{PLUM}" stroke-width="6"/>')
scene("S08", 44.0, 60.0, [
    ai(16.0, (110, 100), (0, 0)),
    ("bg", bg(), {"type": "none"}),
    ("look", head("중간에 쓸 돈이면 연금저축", 540, 430, 80) + head("더 채우려면 + IRP", 540, 560, 96, YELLOW), {"type": "pop", "at": 0.2, "anchor": [540, 500]}),
    ("button", pill("구독하기", 540, 1250, 80, RED, WHITE), {"type": "pop", "at": 4.6, "anchor": [540, 1250]}),
    ("finger", f'<g transform="translate(0 170)">{finger}</g>', {"type": "tap", "at": 5.2, "anchor": [785, 1390]}),
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
