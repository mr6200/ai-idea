"""Generate SVG parts for all 12 scenes of the pension-return Short (1080x1920).

Style (episode 13 on): 3D clay AI paintings mixed with a minimal infographic. Each scene's bottom
layer is a RunPod clay painting (ai_bg/Sxx.png) that drifts slowly (kenburns); over it a teal
gradient carries the Jua headline, and the numbers sit on off-white infographic cards with big
Black Han Sans figures, a teal/red palette and Do Hyeon labels. Subtitles use Do Hyeon.

Each scene is a list of parts; each part becomes its own full-frame SVG so the exported PNG
layers line up in EffectCraft. A manifest records the timing and animation hints.
"""
import json
import os

W, H = 1080, 1920
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "svg")
LABEL = "지식 쇼츠 · 노후 준비 3"

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


def rate_steps():
    """Contribution rate 9% (2025) rising 0.5%p a year to 13% (2033)."""
    out = ""
    for i in range(9):
        rate = 9 + 0.5 * i
        h = (rate - 7) * 70
        x = 150 + i * 88
        hi = i in (0, 1, 8)
        out += f'<rect x="{x}" y="{1180 - h:.0f}" width="64" height="{h:.0f}" rx="10" fill="{TEAL if hi else "#9cc9c1"}"/>'
        if hi:
            out += num(f"{rate:g}%", x + 32, 1160 - h, 40, TEAL if i else INK)
        out += text(f"{25 + i}", x + 32, 1230, 30, INK)
    return out


def ratio_bars():
    """Paid 1 vs received about 1.6~2 (average earner, after the reform: 1.65~2.09 by generation)."""
    return (f'<rect x="230" y="{1180 - 160}" width="200" height="160" rx="18" fill="{INK}"/>' + num("1", 330, 1000, 70, INK) + text("낸 돈", 330, 1235, 44, INK)
            + f'<rect x="650" y="{1180 - 336}" width="200" height="336" rx="18" fill="{TEAL}"/>'
            + f'<rect x="650" y="{1180 - 256}" width="200" height="4" fill="{WHITE}"/>'
            + num("약 1.6~2", 750, 820, 62, TEAL) + text("받는 돈", 750, 1235, 44, INK))


def fund_timeline():
    pts = [(2056, "개혁 전", RED, 230), (2064, "개혁 후", TEAL, 540), (2071, "수익률 높으면", TEAL, 850)]
    out = f'<path d="M150 1000 H930" stroke="{INK}" stroke-width="8" stroke-linecap="round"/>'
    for year, label, col, x in pts:
        out += (f'<circle cx="{x}" cy="1000" r="26" fill="{col}" stroke="{PLUM}" stroke-width="5"/>'
                + num(f"{year}", x, 940, 64, col) + text(label, x, 1080, 40, INK))
    return out + f'<path d="M300 860 Q385 800 470 860" fill="none" stroke="{TEAL}" stroke-width="8"/><path d="M452 842 L472 862 L446 870" fill="none" stroke="{TEAL}" stroke-width="8" stroke-linecap="round"/>'


# S01 낸 돈보다 더? --------------------------------------------------------------------------
scene("S01", 0, 5, [
    ai(5, (104, 118), (0, 30)),
    ("bg", bg(), {"type": "none"}),
    ("title", head("국민연금,", 540, 400, 110) + head("낸 돈보다 더 받을까?", 540, 540, 100, YELLOW), {"type": "pop", "at": 0.0, "anchor": [540, 470]}),
    ("coins", card(110, 760, 860, 420) + coins(330, 1110, 4) + text("낸 돈", 330, 860, 46, INK) + coins(750, 1110, 9, TEAL) + text("받는 돈?", 750, 860, 46, INK),
     {"type": "pop", "at": 0.8, "anchor": [540, 970]}),
    ("worry", pill("기금 바닥난다던데?", 540, 1260, 48, RED, WHITE), {"type": "stamp", "at": 2.6, "anchor": [540, 1260]}),
])

# S02 보험료율 9% → 13% ------------------------------------------------------------------------
scene("S02", 5, 12, [
    ai(7, (114, 104), (-30, 0)),
    ("bg", bg(), {"type": "none"}),
    ("title", head("보험료율이 오른다", 540, 430, 96), {"type": "pop", "at": 0.0, "anchor": [540, 410]}),
    ("steps", card(90, 600, 900, 720) + text("해마다 0.5%포인트씩", 540, 690, 46, INK) + rate_steps(), {"type": "wipeL", "at": 0.4, "dur": 3.0}),
    ("goal", pill("2033년 13%", 540, 1310, 52, RED, WHITE), {"type": "stamp", "at": 4.0, "anchor": [540, 1310]}),
])

# S03 소득대체율 43% ------------------------------------------------------------------------------
scene("S03", 12, 19, [
    ai(7, (106, 116), (30, -20)),
    ("bg", bg(), {"type": "none"}),
    ("title", head("받는 비율도 올랐다", 540, 430, 96), {"type": "pop", "at": 0.0, "anchor": [540, 410]}),
    ("rate", card(110, 620, 860, 460) + tag("소득대체율", 540, 710, 48, TEAL) + num("43%", 540, 930, 200, TEAL) + text("2026년 이후 가입 기간부터", 540, 1030, 40, INK),
     {"type": "pop", "at": 0.4, "anchor": [540, 850]}),
    ("more", pill("더 내고 더 받는 개혁", 540, 1200, 52, RED, WHITE), {"type": "stamp", "at": 3.6, "anchor": [540, 1200]}),
])

# S04 수익비 = 받는 돈 ÷ 낸 돈 -------------------------------------------------------------------------
scene("S04", 19, 26, [
    ai(7, (110, 120), (0, 40)),
    ("bg", bg(), {"type": "none"}),
    ("title", head("받는 돈 ÷ 낸 돈", 540, 430, 100), {"type": "pop", "at": 0.0, "anchor": [540, 410]}),
    ("eq", card(110, 640, 860, 420) + num("받는 돈", 300, 800, 80, TEAL) + num("÷", 540, 800, 80, INK) + num("낸 돈", 780, 800, 80, INK)
     + f'<path d="M180 870 H900" stroke="{INK}" stroke-width="5"/>' + num("= 수익비", 540, 990, 100, RED), {"type": "pop", "at": 0.4, "anchor": [540, 850]}),
    ("note", pill("1보다 크면 낸 돈보다 더", 540, 1200, 46, PLUM, WHITE), {"type": "stamp", "at": 3.6, "anchor": [540, 1200]}),
])

# S05 수익비 약 1.6~2.1배 ---------------------------------------------------------------------------------
scene("S05", 26, 33, [
    ai(7, (116, 106), (0, -30)),
    ("bg", bg(), {"type": "none"}),
    ("title", head("평균 소득자라면?", 540, 430, 100), {"type": "pop", "at": 0.0, "anchor": [540, 410]}),
    ("bars", card(110, 600, 860, 700) + text("개혁 후 수익비 (정부·학회 추계)", 540, 680, 40, INK) + ratio_bars(), {"type": "wipeU", "at": 0.4, "dur": 1.6}),
    ("young", pill("젊을수록 조금 낮아요", 540, 1290, 46, RED, WHITE), {"type": "stamp", "at": 3.6, "anchor": [540, 1290]}),
])

# S06 이유 ① 물가 연동 -----------------------------------------------------------------------------------
scene("S06", 33, 41, [
    ai(8, (104, 114), (-30, 20)),
    ("bg", bg(), {"type": "none"}),
    ("title", head("이유 ① 물가만큼 올라요", 540, 430, 90), {"type": "pop", "at": 0.0, "anchor": [540, 410]}),
    ("idx", card(110, 620, 860, 380) + text("매년 소비자물가 상승률만큼", 540, 710, 46, INK) + num("연금액 ↑", 540, 880, 130, TEAL), {"type": "pop", "at": 0.4, "anchor": [540, 810]}),
    ("y2026", card(110, 1040, 860, 220) + text("2026년", 360, 1170, 56, INK) + num("+2.1%", 700, 1180, 110, RED), {"type": "slideU", "at": 3.8}),
])

# S07 이유 ② 회사 절반 · ③ 재분배 ---------------------------------------------------------------------------
scene("S07", 41, 48, [
    ai(7, (112, 104), (20, 0)),
    ("bg", bg(), {"type": "none"}),
    ("title", head("이유 ② · ③", 540, 430, 100), {"type": "pop", "at": 0.0, "anchor": [540, 410]}),
    ("half", card(110, 620, 860, 300) + tag("직장인", 540, 700, 44, TEAL) + num("보험료 절반은 회사", 540, 850, 80, INK), {"type": "slideL", "at": 0.4}),
    ("share", card(110, 960, 860, 300) + tag("소득 재분배", 540, 1040, 44, TEAL) + num("적게 벌수록 더 돌려받아요", 540, 1190, 62, RED), {"type": "slideR", "at": 3.4}),
])

# S08 기금 소진 시점 -------------------------------------------------------------------------------------
scene("S08", 48, 55, [
    ai(7, (106, 118), (0, -40)),
    ("bg", bg(), {"type": "none"}),
    ("title", head("기금이 바닥나면?", 540, 430, 100), {"type": "pop", "at": 0.0, "anchor": [540, 410]}),
    ("tl", card(90, 640, 900, 560) + text("기금 소진 전망", 540, 730, 46, INK) + fund_timeline(), {"type": "wipeL", "at": 3.4, "dur": 1.8}),
])

# S09 국가 지급 보장 -------------------------------------------------------------------------------------
stamp = (f'<circle cx="790" cy="1010" r="110" fill="none" stroke="{RED}" stroke-width="10"/>'
         f'<circle cx="790" cy="1010" r="90" fill="none" stroke="{RED}" stroke-width="4"/>' + text("보장", 790, 1035, 64, RED, "middle", HEAD))
scene("S09", 55, 62, [
    ai(7, (114, 104), (-20, 20)),
    ("bg", bg(), {"type": "none"}),
    ("title", head("법에 적힌 약속", 540, 430, 100), {"type": "pop", "at": 0.0, "anchor": [540, 410]}),
    ("law", card(110, 620, 860, 560) + tag("국민연금법 제3조의2", 540, 710, 44, TEAL) + text("국가는 연금 급여의", 540, 830, 56, INK) + text("안정적·지속적 지급을", 540, 910, 56, INK)
     + text("보장한다 (취지)", 380, 990, 56, INK), {"type": "pop", "at": 0.4, "anchor": [540, 900]}),
    ("stamp", stamp, {"type": "stamp", "at": 1.8, "anchor": [790, 1010]}),
    ("when", pill("2026년 1월 시행", 540, 1260, 48, RED, WHITE), {"type": "stamp", "at": 3.6, "anchor": [540, 1260]}),
])

# S10 정리 ---------------------------------------------------------------------------------------------
scene("S10", 62, 70, [
    ai(8, (104, 114), (0, 30)),
    ("bg", bg(), {"type": "none"}),
    ("title", head("정리하면", 540, 430, 110), {"type": "pop", "at": 0.0, "anchor": [540, 410]}),
    ("a", card(110, 620, 860, 280) + text("낸 돈보다 더 받는 구조", 540, 740, 56, INK) + num("수익비 1 이상", 540, 850, 64, TEAL), {"type": "slideL", "at": 0.4}),
    ("b", card(110, 950, 860, 280) + text("오랫동안 꾸준히 낼수록", 540, 1070, 56, INK) + num("더 유리", 540, 1180, 70, RED), {"type": "slideR", "at": 3.8}),
])

# S11 퀴즈: 무엇에 맞춰 오를까? ---------------------------------------------------------------------------
choices = "".join(card(130 + i * 280, 780, 240, 200) + num(w, 250 + i * 280, 900, 64, INK) for i, w in enumerate(("월급", "물가", "금리")))
scene("S11", 70, 80, [
    ai(10, (106, 120), (0, -30)),
    ("bg", bg(), {"type": "none"}),
    ("badge", pill("퀴즈", 540, 340, 56, RED, WHITE), {"type": "pop", "at": 0.0, "anchor": [540, 340]}),
    ("question", head("연금액은 매년", 540, 490, 90) + head("무엇에 맞춰 오를까?", 540, 600, 90, YELLOW), {"type": "pop", "at": 0.3, "anchor": [540, 545]}),
    ("choices", choices, {"type": "pop", "at": 0.8, "anchor": [540, 880]}),
    ("answer", f'<rect x="402" y="768" width="276" height="224" rx="40" fill="none" stroke="{RED}" stroke-width="12"/>' + pill("정답 · 물가", 540, 1080, 56, RED, WHITE),
     {"type": "stamp", "at": 3.6, "anchor": [540, 880]}),
    ("why", pill("소비자물가 상승률만큼", 540, 1250, 46, TEAL, WHITE), {"type": "fade", "at": 6.6}),
])

# S12 마무리 + 구독 ---------------------------------------------------------------------------------------
finger = (f'<path d="M700 1145 V1250 C700 1280 740 1300 770 1300 H820 C850 1300 870 1270 870 1240 V1200 C870 1185 845 1180 835 1195 '
          f'C835 1175 810 1170 800 1188 C800 1170 775 1165 765 1185 V1145 C765 1120 700 1120 700 1145 Z" fill="#f6d2b3" stroke="{PLUM}" stroke-width="6"/>')
scene("S12", 80, 90, [
    ai(10, (110, 100), (0, 0)),
    ("bg", bg(), {"type": "none"}),
    ("look", head("노후 준비 첫걸음,", 540, 430, 96) + head("국민연금부터", 540, 560, 110, YELLOW), {"type": "pop", "at": 0.2, "anchor": [540, 500]}),
    ("button", pill("구독하기", 540, 1080, 80, RED, WHITE), {"type": "pop", "at": 4.8, "anchor": [540, 1080]}),
    ("finger", finger, {"type": "tap", "at": 5.6, "anchor": [785, 1220]}),
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
