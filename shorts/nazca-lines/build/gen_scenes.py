"""Overlay parts for the 10 scenes of the nazca-lines Short (1080x1920) plus the scene manifest.

Style (mystery series, episode 3): realistic documentary. The bottom layer of every scene is AI documentary
footage: a WAN 2.2 clip for the key scenes (S01 hook, S06 1930s plane, S10 ending) and a Seedream still moved
by a slow Ken Burns camera for the rest (prepared by prep_footage.py as parts/Sxx/video.mp4 or still.png);
on top sit a soft dark top/bottom shade, a small series label, Black Han Sans headlines and
lower-third cards (dark glass box + gold bar, Do Hyeon). Subtitles are white Do Hyeon with a dark
outline over the bottom shade (gen_subtitles.py).

Each part becomes its own full-frame SVG so the exported PNG layers line up in EffectCraft.
A manifest records the timing and animation hints.
"""
import json
import os

W, H = 1080, 1920
OUT = os.path.dirname(os.path.abspath(__file__))
SVG = os.path.join(OUT, "svg")
LABEL = "세계의 미스터리"  # no episode number on screen (user rule)

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


def video(*clips):
    """Bottom layer: the scene's documentary footage, prepared by prep_footage.py from these clips."""
    return ("video", "", {"type": "video", "clips": list(clips)})


def photo(src, z=(104, 114), pan=(0, 0)):
    """Bottom layer for a non-video scene: Seedream still footage/cand/<src>.jpg moved by a slow Ken Burns
    camera (zoom z0 -> z1 %, drift pan px over the whole scene; dur is filled in from the scene length)."""
    return ("still", "", {"type": "kenburns", "src": src, "z": list(z), "pan": list(pan)})


def static(name, body):
    return (name, body, {"type": "none"})


# scene timing in seconds (a WAN clip is about 5 s and may be slowed up to about 1.4x)
S = {
    "S01": (0.0, 6.2), "S02": (6.2, 11.45), "S03": (11.45, 15.4), "S04": (15.4, 20.75), "S05": (20.75, 23.6),
    "S06": (23.6, 28.0), "S07": (28.0, 35.45), "S08": (35.45, 42.8), "S09": (42.8, 50.0), "S10": (50.0, 57.0),
}

OUTLINE = 'stroke="#000" stroke-opacity="0.8" stroke-width="8" paint-order="stroke"'

SCENES = {
    # the hummingbird lies in the lower two thirds, so the headline sits in the top band
    "S01": [video("S01"), static("shade", shade()),
            ("t1", head("땅에선 안 보이는", 540, 360, 100), {"type": "pop", "at": 0.15, "anchor": [540, 320]}),
            ("t2", head("사막의 거대한 그림", 540, 500, 108, GOLD), {"type": "pop", "at": 0.7, "anchor": [540, 460]})],
    "S02": [photo("S03_b", z=(104, 114), pan=(0, 30)), static("shade", shade()),
            ("tag", lower("나스카 라인 · 페루 남부 사막", "기원전 500년 ~ 서기 500년 무렵", y=300), {"type": "slideL", "at": 0.3}),
            ("who", pill("나스카 사람들이 그린 것으로 봐요", 540, 560, 44), {"type": "pop", "at": 2.6, "anchor": [540, 560]})],
    "S03": [photo("S04_a", z=(106, 116)), static("shade", shade()),
            ("size", lower("그림 크기", "원숭이 93m × 58m · 콘도르 134m", y=1170), {"type": "slideL", "at": 0.3})],
    "S04": [photo("S05_a", z=(104, 112), pan=(0, -30)), static("shade", shade()),
            ("how", lower("그리는 방법 · 깊이 약 10~15cm", "붉은 돌을 걷어 밝은 흙을 드러냄", y=1150), {"type": "slideL", "at": 2.2})],
    "S05": [photo("S02_b", z=(102, 110)), static("shade", shade()),
            ("dry", lower("나스카 사막", "비가 거의 없고 바람도 약해 오래 남음", y=300), {"type": "slideL", "at": 0.2})],
    "S06": [video("S06"), static("shade", shade()),
            ("fly", lower("1920년대 후반 페루 고고학자가 처음 기록", "1930년대 비행기 승객들 눈에 띄며 유명해짐", y=1150), {"type": "slideL", "at": 0.3})],
    "S07": [photo("S07_a", z=(104, 112), pan=(20, 0)), static("shade", shade()),
            ("who", lower("2024년 · 일본 야마가타대학 + IBM", "AI로 항공 사진 분석 → 현장 조사", y=1150), {"type": "slideL", "at": 0.3}),
            ("n", pill("6개월 만에 새 그림 303개", 540, 330, 62, RED, WHITE), {"type": "stamp", "at": 4.9, "anchor": [540, 330]})],
    "S08": [photo("S07_b", z=(108, 116), pan=(0, 20)), static("shade", shade()),
            ("count", lower("알려진 그림 수", "430개 → 733개", y=300), {"type": "slideL", "at": 0.2}),
            ("small", pill("새 그림 대부분 작음 (평균 약 9m) · 오솔길 옆", 540, 505, 40), {"type": "pop", "at": 3.7, "anchor": [540, 505]})],
    "S09": [photo("S08_a", z=(104, 112), pan=(0, -30)), static("shade", shade()),
            ("q", head("왜 그렸을까?", 540, 340, 110, GOLD), {"type": "pop", "at": 0.15, "anchor": [540, 300]}),
            ("astro", lower("별자리 달력설 (1940년대~)", "지금은 의심받는 설명", y=440), {"type": "slideL", "at": 1.5}),
            ("water", lower("물 · 풍요를 비는 의식의 길", "많은 학자의 설명 · 아직 확정 아님", y=610), {"type": "slideL", "at": 4.4})],
    "S10": [video("S09"), static("shade", shade()),
            ("t", head("정답은 아직 사막 위에", 540, 340, 90, GOLD), {"type": "pop", "at": 0.15, "anchor": [540, 300]}),
            ("sub", pill("구독하고 다음 미스터리 보기", 540, 490, 50, RED, WHITE), {"type": "pop", "at": 2.3, "anchor": [540, 490]})],
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
            if anim["type"] == "kenburns":
                anim = dict(anim, dur=round(end - start + 0.2, 2))
            if anim["type"] not in ("video", "kenburns"):
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
