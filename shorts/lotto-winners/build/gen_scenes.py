"""Generate SVG parts for all 8 scenes of the lotto-winners Short (60 s) (1080x1920).

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


def balls(cx, cy, nums, r=62):
    """Lottery balls in a row, coloured like the real 6/45 ranges."""
    col = lambda n: "#f4b400" if n <= 10 else "#3b82f6" if n <= 20 else RED if n <= 30 else "#8a8a8a" if n <= 40 else "#3fae49"
    x0 = cx - (len(nums) - 1) * (r * 2 + 16) / 2
    return "".join(f'<circle cx="{x0 + i * (r * 2 + 16):.0f}" cy="{cy}" r="{r}" fill="{col(n)}" stroke="{PLUM}" stroke-width="5"/>'
                   + num(str(n), x0 + i * (r * 2 + 16), cy + r * 0.36, r, WHITE) for i, n in enumerate(nums))


def cross(cx, cy, w, h):
    return (f'<path d="M{cx - w / 2} {cy - h / 2} L{cx + w / 2} {cy + h / 2} M{cx + w / 2} {cy - h / 2} L{cx - w / 2} {cy + h / 2}" '
            f'stroke="{RED}" stroke-width="18" stroke-linecap="round"/>')


# S01 로또 1등 = 파산? ------------------------------------------------------------------------------
scene("S01", 0, 4.4, [
    ai(4.4, (104, 116), (0, 30)),
    ("bg", bg(), {"type": "none"}),
    ("title", head("로또 1등 되면", 540, 400, 110) + head("결국 다 망한다?", 540, 540, 104, YELLOW), {"type": "pop", "at": 0.0, "anchor": [540, 470]}),
    ("balls", balls(540, 1000, (3, 14, 22, 31, 38, 45), 60), {"type": "pop", "at": 0.6, "anchor": [540, 1000]}),
    ("really", pill("정말일까?", 540, 1230, 60, RED, WHITE), {"type": "stamp", "at": 2.8, "anchor": [540, 1230]}),
])

# S02 확률 · 당첨금 · 세금 ---------------------------------------------------------------------------------
scene("S02", 4.4, 12.0, [
    ai(7.6, (114, 104), (-30, 0)),
    ("bg", bg(), {"type": "none"}),
    ("title", head("1등의 숫자들", 540, 430, 104), {"type": "pop", "at": 0.0, "anchor": [540, 410]}),
    ("odds", card(110, 600, 860, 250) + tag("1등 확률", 540, 670, 42, TEAL) + num("814만분의 1", 540, 800, 96, INK), {"type": "slideL", "at": 0.3}),
    ("prize", card(110, 880, 860, 250) + tag("평균 1등 당첨금", 540, 950, 42, TEAL) + num("약 20억 원", 540, 1080, 96, INK), {"type": "slideR", "at": 2.2}),
    ("net", pill("세금 떼면 약 13.7억 원", 540, 1250, 56, RED, WHITE), {"type": "stamp", "at": 4.6, "anchor": [540, 1250]}),
    ("tax", text("3억 원까지 22% · 넘는 부분 33%", 540, 1350, 38, WHITE), {"type": "fade", "at": 5.0}),
])

# S03 70% 파산? 근거 없음 ---------------------------------------------------------------------------------
scene("S03", 12.0, 22.0, [
    ai(10, (106, 118), (30, -20)),
    ("bg", bg(), {"type": "none"}),
    ("title", head("당첨자 70%가 파산?", 540, 430, 96), {"type": "pop", "at": 0.0, "anchor": [540, 410]}),
    ("rumor", card(110, 600, 860, 360) + text("인터넷에 떠도는 통계", 540, 690, 44, INK) + num("70% 파산", 540, 860, 150, RED), {"type": "pop", "at": 0.4, "anchor": [540, 780]}),
    ("x", cross(540, 800, 620, 220), {"type": "stamp", "at": 3.8, "anchor": [540, 800]}),
    ("nope", pill("근거 없음", 540, 1010, 60, RED, WHITE), {"type": "stamp", "at": 4.2, "anchor": [540, 1010]}),
    ("src", card(110, 1080, 860, 230) + tag("출처로 알려진 미국 재단 (NEFE)", 540, 1150, 38, TEAL) + text("“우리 연구가 아니다” (2018)", 540, 1260, 52, INK),
     {"type": "slideU", "at": 6.0}),
])

# S04 스웨덴: 만족도 ↑ ------------------------------------------------------------------------------------
scene("S04", 22.0, 28.0, [
    ai(6, (112, 104), (0, 30)),
    ("bg", bg(), {"type": "none"}),
    ("title", head("스웨덴 연구", 540, 430, 110), {"type": "pop", "at": 0.0, "anchor": [540, 410]}),
    ("study", card(110, 620, 860, 520) + tag("큰 당첨자 · 5~22년 뒤 조사", 540, 700, 40, TEAL) + text("삶의 만족도", 540, 830, 60, INK)
     + num("↑ 계속 높았다", 540, 980, 100, TEAL) + text("10년 넘게 줄지 않음 (2020년 논문)", 540, 1080, 38, INK), {"type": "pop", "at": 0.5, "anchor": [540, 880]}),
])

# S05 플로리다: 파산을 미뤘을 뿐 ----------------------------------------------------------------------------
scene("S05", 28.0, 37.0, [
    ai(9, (104, 116), (-30, 20)),
    ("bg", bg(), {"type": "none"}),
    ("title", head("미국 플로리다 연구", 540, 430, 96), {"type": "pop", "at": 0.0, "anchor": [540, 410]}),
    ("study", card(110, 600, 860, 440) + tag("5만~15만 달러 당첨자", 540, 680, 40, TEAL) + text("약 7천만~2억 원", 540, 790, 48, INK)
     + num("파산을 몇 년", 540, 910, 84, RED) + num("미뤘을 뿐", 540, 1000, 84, RED), {"type": "pop", "at": 0.4, "anchor": [540, 820]}),
    ("src", text("2011년 논문 · 1993~2002년 당첨자", 540, 1090, 36, WHITE), {"type": "fade", "at": 1.0}),
    ("lesson", pill("돈의 크기보다 쓰는 방법", 540, 1230, 56, PLUM, WHITE), {"type": "stamp", "at": 6.2, "anchor": [540, 1230]}),
])

# S06 한국 1등 당첨자 35% 집 ----------------------------------------------------------------------------------
scene("S06", 37.0, 42.0, [
    ai(5, (110, 120), (0, -30)),
    ("bg", bg(), {"type": "none"}),
    ("title", head("우리나라 1등은?", 540, 430, 104), {"type": "pop", "at": 0.0, "anchor": [540, 410]}),
    ("survey", card(110, 620, 860, 480) + tag("1등 당첨자 설문 (2024년 공개)", 540, 700, 40, TEAL) + num("35%", 540, 920, 200, TEAL)
     + text("집 · 부동산부터 산다", 540, 1040, 56, INK), {"type": "pop", "at": 0.4, "anchor": [540, 860]}),
])

# S07 퀴즈: 언제까지 찾아가야 할까? ---------------------------------------------------------------------------
choices = "".join(card(130 + i * 280, 760, 240, 200) + num(w, 250 + i * 280, 880, 60, INK) for i, w in enumerate(("1개월", "1년", "평생")))
scene("S07", 42.0, 53.0, [
    ai(11, (106, 120), (0, -30)),
    ("bg", bg(), {"type": "none"}),
    ("badge", pill("퀴즈", 540, 340, 56, RED, WHITE), {"type": "pop", "at": 0.0, "anchor": [540, 340]}),
    ("question", head("1등 당첨금,", 540, 490, 90) + head("언제까지 찾아야 할까?", 540, 600, 86, YELLOW), {"type": "pop", "at": 0.3, "anchor": [540, 545]}),
    ("choices", choices, {"type": "pop", "at": 0.8, "anchor": [540, 860]}),
    ("answer", f'<rect x="402" y="748" width="276" height="224" rx="40" fill="none" stroke="{RED}" stroke-width="12"/>' + pill("정답 · 1년", 540, 1060, 56, RED, WHITE),
     {"type": "stamp", "at": 4.4, "anchor": [540, 860]}),
    ("why", pill("지나면 복권기금으로", 540, 1230, 46, TEAL, WHITE), {"type": "fade", "at": 6.8}),
])

# S08 마무리 + 구독 --------------------------------------------------------------------------------------
finger = (f'<path d="M700 1145 V1250 C700 1280 740 1300 770 1300 H820 C850 1300 870 1270 870 1240 V1200 C870 1185 845 1180 835 1195 '
          f'C835 1175 810 1170 800 1188 C800 1170 775 1165 765 1185 V1145 C765 1120 700 1120 700 1145 Z" fill="#f6d2b3" stroke="{PLUM}" stroke-width="6"/>')
scene("S08", 53.0, 60.0, [
    ai(7, (110, 100), (0, 0)),
    ("bg", bg(), {"type": "none"}),
    ("look", head("망하느냐는", 540, 430, 100) + head("쓰는 방법에 달렸다", 540, 560, 96, YELLOW), {"type": "pop", "at": 0.2, "anchor": [540, 500]}),
    ("button", pill("구독하기", 540, 1080, 80, RED, WHITE), {"type": "pop", "at": 3.4, "anchor": [540, 1080]}),
    ("finger", finger, {"type": "tap", "at": 4.0, "anchor": [785, 1220]}),
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
