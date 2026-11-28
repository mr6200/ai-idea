"""Overlay parts for the 12 scenes of the Stonehenge Short (1080x1920) plus the scene manifest.

Style (mystery series, episode 11): realistic documentary built on real photos of Stonehenge, a Welsh bluestone,
the Preseli Hills and the Altar Stone (photos/, CC BY / CC BY-SA, marked 「실제 사진」 with author and licence),
WAN 2.2 clips for S01 (hook), S06 (hauling a bluestone) and S12 (ending) and Seedream stills for S08 and S10; on
top sit a soft dark top/bottom shade, a small series label, Black Han Sans headlines and lower-third cards (dark
glass box + gold bar, Do Hyeon). Subtitles are white Do Hyeon with a dark outline (gen_subtitles.py).

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


def archive(src, z=(100, 106), pan=(0, 0)):
    """Bottom layer for a real archive image photos/<src> (public domain / CC BY / CC BY-SA, credited in
    script.md and the video description): shown whole over a blurred copy, with a very slow zoom."""
    return ("still", "", {"type": "kenburns", "src": "photos/" + src, "z": list(z), "pan": list(pan)})


def real_tag(s):
    """「실제 자료 · 연도」 tag that marks a real archive image apart from the AI scenes (shrinks to fit long
    author / licence credits)."""
    size = 36
    while text_width(s, size) > 900 and size > 24:
        size -= 1
    w = text_width(s, size) + 56
    return (f'<rect x="{540 - w / 2:.0f}" y="252" width="{w:.0f}" height="58" rx="29" fill="#000" fill-opacity="0.6" '
            f'stroke="{GOLD}" stroke-width="3"/>' + text(s, 540, 281 + size * 0.33, size, GOLD))


def photo(src, z=(104, 114), pan=(0, 0)):
    """Bottom layer for a non-video scene: Seedream still footage/cand/<src>.jpg moved by a slow Ken Burns
    camera (zoom z0 -> z1 %, drift pan px over the whole scene; dur is filled in from the scene length)."""
    return ("still", "", {"type": "kenburns", "src": src, "z": list(z), "pan": list(pan)})


def static(name, body):
    return (name, body, {"type": "none"})


# scene timing in seconds (a WAN clip is about 5 s)
S = {
    "S01": (0.0, 6.75), "S02": (6.75, 9.85), "S03": (9.85, 17.35), "S04": (17.35, 19.95), "S05": (19.95, 25.25),
    "S06": (25.25, 29.15), "S07": (29.15, 34.75), "S08": (34.75, 41.55), "S09": (41.55, 47.35),
    "S10": (47.35, 51.25), "S11": (51.25, 54.65), "S12": (54.65, 60.0),
}

OUTLINE = 'stroke="#000" stroke-opacity="0.8" stroke-width="8" paint-order="stroke"'

SCENES = {
    "S01": [video("S01"), static("shade", shade()),
            ("t1", head("5,000년 전 거대한 돌", 540, 340, 90), {"type": "pop", "at": 0.15, "anchor": [540, 310]}),
            ("t2", head("스톤헨지", 540, 490, 130, GOLD), {"type": "stamp", "at": 3.3, "anchor": [540, 450]})],
    "S02": [archive("overview.jpg", z=(100, 108)), static("shade", shade()),
            ("tag", real_tag("실제 사진 · 스톤헨지 (DeFacto, CC BY-SA 4.0)"), {"type": "fade", "at": 0.1}),
            ("q", lower("영국 솔즈베리 평원", "대부분 이 근처 돌이 아니다", y=1150), {"type": "slideL", "at": 0.3})],
    "S03": [archive("sarsen.jpg", z=(100, 108)), static("shade", shade()),
            ("tag", real_tag("실제 사진 · 바깥쪽 사센석 (Diego Delso, CC BY-SA 4.0)"), {"type": "fade", "at": 0.1}),
            ("w", lower("사센석 (큰 돌)", "하나에 20톤 안팎", y=1150), {"type": "slideL", "at": 0.3}),
            ("src", pill("2020년 분석 · 약 25km 북쪽 숲에서", 540, 1070, 46, RED, WHITE), {"type": "stamp", "at": 3.2, "anchor": [540, 1070]})],
    "S04": [archive("bluestone.jpg", z=(100, 108)), static("shade", shade()),
            ("tag", real_tag("실제 사진 · 웨일스 블루스톤 (전시, -JvL-, CC BY 2.0)"), {"type": "fade", "at": 0.1}),
            ("b", lower("블루스톤 (안쪽 작은 돌)", "더 먼 곳에서 왔다", y=1150), {"type": "slideL", "at": 0.3})],
    "S05": [archive("carn_goedog.jpg", z=(100, 108)), static("shade", shade()),
            ("tag", real_tag("실제 사진 · 웨일스 프레셀리 산 칸 고에독 (ceridwen, CC BY-SA 2.0)"), {"type": "fade", "at": 0.1}),
            ("d", lower("웨일스 프레셀리 산", "200km 넘게 · 채석장 흔적 발견", y=1150), {"type": "slideL", "at": 0.3})],
    "S06": [video("S06"), static("shade", shade()),
            ("m", lower("블루스톤 하나 약 3톤 (AI 재현)", "썰매와 통나무로 끌었다는 설명", y=300), {"type": "slideL", "at": 0.2})],
    "S07": [archive("altar.jpg", z=(100, 108)), static("shade", shade()),
            ("tag", real_tag("실제 사진 · 제단석 (The Stones of Stonehenge, CC BY 4.0)"), {"type": "fade", "at": 0.1}),
            ("t", head("2024년 반전", 540, 470, 96, GOLD), {"type": "pop", "at": 0.3, "anchor": [540, 440]}),
            ("a", lower("가운데 깔린 제단석", "무게 약 6톤", y=1150), {"type": "slideL", "at": 3.3})],
    "S08": [photo("S08_d", z=(104, 112)), static("shade", shade()),
            ("s", lower("제단석의 고향 (AI 재현)", "700km 넘게 떨어진 스코틀랜드 북동쪽", y=300), {"type": "slideL", "at": 0.2}),
            ("how", pill("배로? 땅으로? 아직 모름", 540, 1080, 50, RED, WHITE), {"type": "stamp", "at": 4.0, "anchor": [540, 1080]})],
    "S09": [archive("solstice.jpg", z=(100, 108)), static("shade", shade()),
            ("tag", real_tag("실제 사진 · 해 뜨는 스톤헨지 (Taro Taylor, CC BY 2.0)"), {"type": "fade", "at": 0.1}),
            ("q", head("왜 먼 데서?", 540, 470, 96, GOLD), {"type": "pop", "at": 0.2, "anchor": [540, 440]}),
            ("sun", lower("하짓날 해 뜨는 방향", "그에 맞춰 돌을 세움", y=1150), {"type": "slideL", "at": 2.5})],
    "S10": [photo("S11_b", z=(104, 112)), static("shade", shade()),
            ("u", lower("하나의 해석 (AI 재현)", "먼 곳 사람들이 돌을 가져와 하나로", y=300), {"type": "slideL", "at": 0.2})],
    "S11": [archive("nightfall.jpg", z=(100, 108)), static("shade", shade()),
            ("tag", real_tag("실제 사진 · 해 진 뒤의 스톤헨지 (R J Higginson, CC BY 3.0)"), {"type": "fade", "at": 0.1}),
            ("m", lower("아직 풀리지 않은 것", "누가, 어떻게 옮겼을까", y=1150), {"type": "slideL", "at": 0.3})],
    "S12": [video("S13"), static("shade", shade()),
            ("t", head("스톤헨지", 540, 340, 110, GOLD), {"type": "pop", "at": 0.15, "anchor": [540, 300]}),
            ("sub", pill("구독하고 다음 미스터리 보기", 540, 490, 50, RED, WHITE), {"type": "pop", "at": 0.4, "anchor": [540, 490]})],
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
