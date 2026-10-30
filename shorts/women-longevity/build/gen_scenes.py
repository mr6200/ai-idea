"""Overlay parts for all 12 scenes of the women-longevity Short (1080x1920) plus the scene manifest.

Style (episode 17): realistic documentary. The bottom layer of every scene is AI documentary
footage (Seedream still animated by WAN 2.2, prepared by prep_footage.py as parts/Sxx/video.mp4);
on top sit a soft dark top/bottom shade, a small yellow topic label, Black Han Sans headlines and
lower-third cards (dark glass box + yellow bar, Do Hyeon). Subtitles are white Do Hyeon with a dark
outline over the bottom shade (gen_subtitles.py).

Each part becomes its own full-frame SVG so the exported PNG layers line up in EffectCraft.
A manifest records the timing and animation hints.
"""
import json
import os

W, H = 1080, 1920
OUT = os.path.dirname(os.path.abspath(__file__))
SVG = os.path.join(OUT, "svg")
LABEL = "인체의 신비 · 수명"

HEAD = "Black Han Sans"
FONT = "Do Hyeon"  # notes, cards and subtitles

WHITE, GREY = "#ffffff", "#d9d9d9"
GOLD, RED, TEAL = "#f2c14e", "#e4572e", "#5ec2b7"
INK = "#111111"


def text_width(s, size):
    w = 0.0
    for ch in s:
        if ord(ch) > 0x2E80:
            w += size * 0.92
        elif ch == " ":
            w += size * 0.3
        else:
            w += size * 0.56
    return w


def text(s, x, y, size, fill=WHITE, anchor="middle", font=FONT, extra=""):
    assert text_width(s, size) < 1000, f"text too wide: {s}"
    s = s.replace("&", "&amp;").replace("<", "&lt;")
    return (f'<text x="{x}" y="{y}" font-family="{font}" font-size="{size}" fill="{fill}" '
            f'text-anchor="{anchor}" {extra}>{s}</text>')


def head(s, x, y, size, fill=WHITE, anchor="middle"):
    """Headline: Black Han Sans with a soft dark outline so it reads over moving footage."""
    return text(s, x, y, size, fill, anchor, HEAD,
                'stroke="#000" stroke-opacity="0.55" stroke-width="7" paint-order="stroke" stroke-linejoin="round"')


def svg(body):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">'
            f'<rect x="0" y="0" width="{W}" height="{H}" fill="#000000" fill-opacity="0"/>{body}</svg>')


def shade():
    """Dark gradient at the top (label, headline) and bottom (subtitles) of the footage."""
    return ('<defs><linearGradient id="top" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#000" stop-opacity="0.62"/>'
            '<stop offset="1" stop-color="#000" stop-opacity="0"/></linearGradient>'
            '<linearGradient id="bot" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#000" stop-opacity="0"/>'
            '<stop offset="1" stop-color="#000" stop-opacity="0.78"/></linearGradient></defs>'
            f'<rect width="{W}" height="720" fill="url(#top)"/><rect y="1180" width="{W}" height="740" fill="url(#bot)"/>'
            + text(LABEL, 540, 200, 36, GOLD, extra='letter-spacing="6"'))


def lower(small, big, y=1210, w=None, big_fill=WHITE, size=54):
    """Lower-third card: dark glass box with a yellow bar, a small caption and a big line."""
    w = w or max(text_width(small, 34), text_width(big, size)) + 110
    x = 70
    return (f'<rect x="{x}" y="{y}" width="{w:.0f}" height="150" rx="12" fill="#000" fill-opacity="0.5"/>'
            f'<rect x="{x + 12}" y="{y + 14}" width="9" height="122" fill="{GOLD}"/>'
            + text(small, x + 44, y + 54, 34, GREY, "start")
            + text(big, x + 44, y + 122, size, big_fill, "start"))


def pill(s, cx, cy, size=48, fill=GOLD, fg=INK):
    w = text_width(s, size) + 70
    return (f'<rect x="{cx - w / 2:.0f}" y="{cy - size * 0.9:.0f}" width="{w:.0f}" height="{size * 1.8:.0f}" rx="{size * 0.9:.0f}" fill="{fill}"/>'
            + text(s, cx, cy + size * 0.35, size, fg))


def glass(x, y, w, h):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="16" fill="#000" fill-opacity="0.5"/>'


def bar(label, value, frac, y, color, x=120, full=700, unit=""):
    """Horizontal value bar: label above, bar with the value at its end (wiped in left to right)."""
    return (text(label, x, y - 18, 40, GREY, "start")
            + f'<rect x="{x}" y="{y}" width="{full * frac:.0f}" height="64" rx="10" fill="{color}"/>'
            + text(value + unit, x + full * frac + 20, y + 50, 52, WHITE, "start"))


def chrom(cx, cy, letter, color=WHITE, broken=False, size=200):
    """A sex chromosome drawn as its letter in a ring; broken adds a red crack."""
    out = (f'<circle cx="{cx}" cy="{cy}" r="{size * 0.72:.0f}" fill="#000" fill-opacity="0.45" stroke="{color}" stroke-width="6"/>'
           + text(letter, cx, cy + size * 0.36, size, color, font=HEAD))
    if broken:
        out += (f'<path d="M{cx - 70} {cy - 90} L{cx - 10} {cy - 20} L{cx - 40} {cy + 10} L{cx + 60} {cy + 100}" '
                f'fill="none" stroke="{RED}" stroke-width="16" stroke-linecap="round" stroke-linejoin="round"/>')
    return out


def check(cx, cy, s=1.0, color=TEAL):
    return (f'<circle cx="{cx}" cy="{cy}" r="{46 * s:.0f}" fill="{color}"/>'
            f'<path d="M{cx - 22 * s:.0f} {cy} L{cx - 5 * s:.0f} {cy + 18 * s:.0f} L{cx + 24 * s:.0f} {cy - 18 * s:.0f}" fill="none" '
            f'stroke="{INK}" stroke-width="{10 * s:.0f}" stroke-linecap="round" stroke-linejoin="round"/>')


def heart(cx, cy, s=1.0):
    p = lambda x, y: f"{cx + x * s:.0f} {cy + y * s:.0f}"
    return (f'<path d="M{p(0, 70)} C{p(-120, -10)} {p(-80, -110)} {p(0, -50)} C{p(80, -110)} {p(120, -10)} {p(0, 70)} Z" '
            f'fill="{RED}" stroke="{WHITE}" stroke-width="6"/>')


def pulse(x, y, w=520, color=TEAL):
    pts = [(0, 0), (0.3, 0), (0.36, -60), (0.42, 70), (0.48, -110), (0.54, 40), (0.6, 0), (1, 0)]
    d = " ".join(f"{'M' if i == 0 else 'L'}{x + w * a:.0f} {y + b}" for i, (a, b) in enumerate(pts))
    return f'<path d="{d}" fill="none" stroke="{color}" stroke-width="9" stroke-linecap="round" stroke-linejoin="round"/>'


def shield(cx, cy, s=1.0):
    p = lambda x, y: f"{cx + x * s:.0f} {cy + y * s:.0f}"
    return (f'<path d="M{p(0, -90)} L{p(75, -60)} L{p(70, 20)} C{p(60, 70)} {p(20, 90)} {p(0, 100)} C{p(-20, 90)} {p(-60, 70)} {p(-70, 20)} L{p(-75, -60)} Z" '
            f'fill="#000" fill-opacity="0.45" stroke="{WHITE}" stroke-width="7"/>'
            f'<path d="M{cx} {cy - 34 * s:.0f} V{cy + 40 * s:.0f} M{cx - 26 * s:.0f} {cy + 14 * s:.0f} L{cx} {cy + 42 * s:.0f} L{cx + 26 * s:.0f} {cy + 14 * s:.0f}" '
            f'fill="none" stroke="{RED}" stroke-width="12" stroke-linecap="round" stroke-linejoin="round"/>')


def video(*clips):
    """Bottom layer: the scene's documentary footage, prepared by prep_footage.py from these clips."""
    return ("video", "", {"type": "video", "clips": list(clips)})


def static(name, body):
    return (name, body, {"type": "none"})


# scene timing in seconds; scene length is end - start (a scene that runs past 5.4 s plays its clip slower)
S = {
    "S01": (0.0, 5.0), "S02": (5.0, 13.6), "S03": (13.6, 20.6), "S04": (20.6, 27.0),
    "S05": (27.0, 33.6), "S06": (33.6, 39.6), "S07": (39.6, 47.0), "S08": (47.0, 54.4),
    "S09": (54.4, 60.8), "S10": (60.8, 68.0), "S11": (68.0, 79.4), "S12": (79.4, 90.0),
}

SCENES = {
    "S01": [video("S01"), static("shade", shade()),
            ("t1", head("여자는 왜", 540, 360, 118), {"type": "pop", "at": 0.15, "anchor": [540, 320]}),
            ("t2", head("더 오래 살까?", 540, 500, 128, GOLD), {"type": "pop", "at": 0.6, "anchor": [540, 460]}),
            ("q", pill("몸속에 숨은 비밀", 540, 1250, 46), {"type": "fade", "at": 2.4})],
    "S02": [video("S02"), static("shade", shade()),
            # the grandmothers' faces sit around y 800-1000, so the numbers go above them and the stamp below
            ("title", head("한국인 기대수명", 540, 330, 100), {"type": "pop", "at": 0.1, "anchor": [540, 290]}),
            ("src", text("2024년 생명표 · 국가데이터처", 540, 400, 36, GREY), {"type": "fade", "at": 0.4}),
            ("box", glass(80, 440, 920, 330), {"type": "fade", "at": 0.3}),
            ("f", bar("여자", "86.6", 86.6 / 100, 510, GOLD, unit="세"), {"type": "wipeL", "at": 1.2, "dur": 1.2}),
            ("m", bar("남자", "80.8", 80.8 / 100, 640, TEAL, unit="세"), {"type": "wipeL", "at": 2.4, "dur": 1.2}),
            ("world", text("세계 거의 모든 나라에서 여자가 더 길어요", 540, 750, 34, GREY), {"type": "fade", "at": 5.8}),
            ("gap", pill("차이 5.8년", 540, 1270, 62, RED, WHITE), {"type": "stamp", "at": 4.7, "anchor": [540, 1270]})],
    "S03": [video("S03"), static("shade", shade()),
            ("title", head("첫째 · 염색체", 540, 420, 110), {"type": "pop", "at": 0.1, "anchor": [540, 380]}),
            ("x1", chrom(370, 1060, "X", GOLD, size=170), {"type": "pop", "at": 1.6, "anchor": [370, 1060]}),
            ("x2", chrom(710, 1060, "X", GOLD, size=170), {"type": "pop", "at": 1.9, "anchor": [710, 1060]}),
            ("tag", text("여자의 성염색체 XX · 같은 X가 두 개", 540, 510, 40, GREY), {"type": "fade", "at": 2.2}),
            ("crack", chrom(370, 1060, "X", GOLD, True, size=170), {"type": "fade", "at": 3.8}),
            ("ok", check(800, 960, 1.0) + text("대신해요", 710, 1250, 50, TEAL, extra='stroke="#000" stroke-opacity="0.8" stroke-width="8" paint-order="stroke"'), {"type": "pop", "at": 5.2, "anchor": [710, 1060]})],
    "S04": [video("S04"), static("shade", shade()),
            ("title", head("남자는 XY", 540, 420, 116), {"type": "pop", "at": 0.1, "anchor": [540, 380]}),
            ("x", chrom(400, 880, "X", TEAL, True), {"type": "pop", "at": 0.6, "anchor": [400, 880]}),
            ("y", chrom(690, 900, "Y", WHITE, size=140), {"type": "pop", "at": 0.9, "anchor": [690, 900]}),
            ("none", text("대신할 X가 없어요", 540, 1110, 48, RED), {"type": "fade", "at": 1.6}),
            ("tag", lower("X염색체 유전 질환", "색맹 · 혈우병 → 남자에게 많아요"), {"type": "slideL", "at": 3.0})],
    "S05": [video("S05"), static("shade", shade()),
            ("title", head("둘째 · 호르몬", 540, 420, 110), {"type": "pop", "at": 0.1, "anchor": [540, 380]}),
            ("e", pill("에스트로겐", 540, 560, 52), {"type": "pop", "at": 1.6, "anchor": [540, 560]}),
            ("heart", heart(540, 880, 1.3), {"type": "pop", "at": 3.6, "anchor": [540, 880]}),
            ("beat", pulse(280, 1060), {"type": "wipeL", "at": 3.9, "dur": 1.0}),
            ("tag", lower("여성호르몬 에스트로겐", "혈관을 부드럽게 → 심장 보호"), {"type": "slideL", "at": 4.2})],
    "S06": [video("S06"), static("shade", shade()),
            ("t", pill("테스토스테론", 540, 320, 56, RED, WHITE), {"type": "pop", "at": 0.6, "anchor": [540, 320]}),
            ("shield", shield(870, 860, 1.1), {"type": "pop", "at": 2.0, "anchor": [870, 860]}),
            ("tag", lower("남성호르몬", "면역력을 떨어뜨릴 수 있어요"), {"type": "slideL", "at": 2.4})],
    "S07": [video("S07"), static("shade", shade()),
            ("title", head("조선 내시의 수명", 540, 420, 104), {"type": "pop", "at": 0.1, "anchor": [540, 380]}),
            ("src", text("환관 족보 속 81명 분석 · 2012년 연구", 540, 500, 38, GREY), {"type": "fade", "at": 0.5}),
            ("box", glass(80, 900, 920, 360), {"type": "fade", "at": 0.6}),
            ("eu", bar("내시", "약 70", 70 / 100, 990, GOLD, unit="세"), {"type": "wipeL", "at": 1.3, "dur": 1.2}),
            ("ya", bar("같은 시대 양반 남자", "51~56", 56 / 100, 1140, TEAL, unit="세"), {"type": "wipeL", "at": 3.6, "dur": 1.0}),
            ("gap", pill("14~19년 더", 540, 650, 58, RED, WHITE), {"type": "stamp", "at": 5.0, "anchor": [540, 650]})],
    "S08": [video("S08"), static("shade", shade()),
            ("title", head("마지막 · 생활 습관", 540, 420, 104), {"type": "pop", "at": 0.1, "anchor": [540, 380]}),
            ("src", text("현재 흡연율 · 2023년 국민건강통계", 540, 500, 38, GREY), {"type": "fade", "at": 0.5}),
            ("box", glass(80, 900, 920, 360), {"type": "fade", "at": 1.4}),
            ("m", bar("남자", "32.4", 32.4 / 40, 990, RED, full=640, unit="%"), {"type": "wipeL", "at": 2.0, "dur": 1.0}),
            ("f", bar("여자", "6.3", 6.3 / 40, 1140, GOLD, full=640, unit="%"), {"type": "wipeL", "at": 2.8, "dur": 0.6}),
            ("x5", pill("5배 넘게", 540, 650, 58, RED, WHITE), {"type": "stamp", "at": 3.4, "anchor": [540, 650]})],
    "S09": [video("S09"), static("shade", shade()),
            ("title", head("아기 때부터", 540, 420, 112), {"type": "pop", "at": 0.1, "anchor": [540, 380]}),
            ("tag", lower("갓난아기 생존", "여자아이가 더 잘 살아남아요"), {"type": "slideL", "at": 1.4}),
            ("tag2", lower("기근 · 전염병 속 7개 집단 분석 (2018년)", "그때도 여자가 더 오래 살았어요", y=1000), {"type": "slideL", "at": 3.2})],
    "S10": [video("S10"), static("shade", shade()),
            ("title", head("오래 살지만…", 540, 420, 112), {"type": "pop", "at": 0.1, "anchor": [540, 380]}),
            ("tag", lower("여자의 노년", "아픈 채 지내는 기간도 더 길어요"), {"type": "slideL", "at": 1.6}),
            ("h", pill("오래보다 건강하게", 540, 1080, 52), {"type": "pop", "at": 4.0, "anchor": [540, 1080]})],
    "S11": [video("S11", "S11b"), static("shade", shade()),
            ("quiz", head("QUIZ", 540, 430, 150, GOLD), {"type": "stamp", "at": 0.1, "anchor": [540, 380]}),
            ("q", head("새는 누가 더 오래 살까?", 540, 560, 76), {"type": "fade", "at": 0.6}),
            ("ab", pill("암컷", 400, 700, 50, "#000", WHITE) + pill("수컷", 680, 700, 50, "#000", WHITE), {"type": "pop", "at": 1.4, "anchor": [540, 700]}),
            ("ans", pill("정답 · 수컷", 540, 700, 84, RED, WHITE), {"type": "stamp", "at": 4.6, "anchor": [540, 700]}),
            ("tag", lower("새의 성염색체", "수컷 ZZ · 암컷 ZW (사람과 반대)"), {"type": "slideL", "at": 6.6})],
    "S12": [video("S12", "S12b"), static("shade", shade()),
            ("title", head("건강하게 오래", 540, 420, 112), {"type": "pop", "at": 0.1, "anchor": [540, 380]}),
            ("c1", check(220, 980, 0.9) + text("금연", 290, 1000, 60, WHITE, "start"), {"type": "pop", "at": 1.2, "anchor": [300, 980]}),
            ("c2", check(560, 980, 0.9) + text("건강검진", 630, 1000, 60, WHITE, "start"), {"type": "pop", "at": 2.0, "anchor": [700, 980]}),
            ("sub", pill("구독하고 더 알아보기", 540, 1250, 52, RED, WHITE), {"type": "pop", "at": 5.0, "anchor": [540, 1250]})],
}


def main():
    manifest = []
    for sid, parts in SCENES.items():
        start, end = S[sid]
        d = os.path.join(SVG, sid)
        os.makedirs(d, exist_ok=True)
        full = ""
        entry = {"id": sid, "start": start, "end": end, "parts": []}
        for name, body, anim in parts:
            if anim["type"] != "video":
                with open(os.path.join(d, f"{name}.svg"), "w") as f:
                    f.write(svg(body))
                full += body
            entry["parts"].append({"name": name, "anim": anim})
        with open(os.path.join(d, "_full.svg"), "w") as f:
            f.write(svg(full))
        manifest.append(entry)
    with open(os.path.join(OUT, "manifest_scenes.json"), "w") as f:
        json.dump(manifest, f, ensure_ascii=False, indent=1)
    print(len(manifest), "scenes")


if __name__ == "__main__":
    main()
