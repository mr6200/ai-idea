"""Overlay parts for the 11 scenes of the roswell Short (1080x1920) plus the scene manifest.

Style (mystery series, episode 4): realistic documentary with real archive images. The bottom layer of every
scene is either a real public-domain archive image (photos/: the 1947 front page, the 1995 and 1997 USAF
reports and the Mogul balloon diagram, marked 「실제 자료」), a WAN 2.2 clip for the key scenes (S01 hook,
S08 balloon train, S11 ending) or a Seedream still moved
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


def archive(src, z=(100, 106), pan=(0, 0)):
    """Bottom layer for a real archive image photos/<src> (public domain / CC BY / CC BY-SA, credited in
    script.md and the video description): shown whole over a blurred copy, with a very slow zoom."""
    return ("still", "", {"type": "kenburns", "src": "photos/" + src, "z": list(z), "pan": list(pan)})


def real_tag(s):
    """「실제 자료 · 연도」 tag that marks a real archive image apart from the AI scenes."""
    w = text_width(s, 36) + 56
    return (f'<rect x="{540 - w / 2:.0f}" y="252" width="{w:.0f}" height="58" rx="29" fill="#000" fill-opacity="0.6" '
            f'stroke="{GOLD}" stroke-width="3"/>' + text(s, 540, 293, 36, GOLD))


def photo(src, z=(104, 114), pan=(0, 0)):
    """Bottom layer for a non-video scene: Seedream still footage/cand/<src>.jpg moved by a slow Ken Burns
    camera (zoom z0 -> z1 %, drift pan px over the whole scene; dur is filled in from the scene length)."""
    return ("still", "", {"type": "kenburns", "src": src, "z": list(z), "pan": list(pan)})


def static(name, body):
    return (name, body, {"type": "none"})


# scene timing in seconds (a WAN clip is about 5 s and may be slowed up to about 1.1x here)
S = {
    "S01": (0.0, 4.4), "S02": (4.4, 11.85), "S03": (11.85, 16.05), "S04": (16.05, 20.4), "S05": (20.4, 28.5),
    "S06": (28.5, 32.15), "S07": (32.15, 38.85), "S08": (38.85, 42.5), "S09": (42.5, 48.2), "S10": (48.2, 52.45),
    "S11": (52.45, 58.0),
}

OUTLINE = 'stroke="#000" stroke-opacity="0.8" stroke-width="8" paint-order="stroke"'

SCENES = {
    "S01": [video("S01"), static("shade", shade()),
            ("t1", head("1947년 미군 발표", 540, 360, 96), {"type": "pop", "at": 0.15, "anchor": [540, 320]}),
            ("t2", head("「비행접시 회수」", 540, 510, 124, GOLD), {"type": "stamp", "at": 0.8, "anchor": [540, 470]})],
    # the rancher crouches in the upper half, the debris lies below him
    "S02": [photo("S02_a", z=(104, 114), pan=(0, 40)), static("shade", shade()),
            ("where", lower("1947년 6월 · 뉴멕시코 코로나 근처 목장", "목장 주인 맥 브라젤이 잔해 발견", y=1150), {"type": "slideL", "at": 0.3}),
            ("what", pill("은박지 · 고무 · 종이 · 나무 막대 · 테이프", 540, 1060, 42), {"type": "pop", "at": 3.8, "anchor": [540, 1060]})],
    "S03": [archive("front_page_1947.jpg", z=(100, 110), pan=(0, 60)), static("shade", shade()),
            ("tag", real_tag("실제 신문 · 1947년 7월 8일"), {"type": "fade", "at": 0.1})],
    "S04": [photo("S04_a", z=(104, 112)), static("shade", shade()),
            ("balloon", pill("하루 만에 → 「기상 관측 풍선」", 540, 1180, 54, RED, WHITE), {"type": "stamp", "at": 1.8, "anchor": [540, 1180]})],
    "S05": [photo("S05_a", z=(104, 112), pan=(-20, 0)), static("shade", shade()),
            ("revive", lower("30년 넘게 잊힌 사건 · 1978년 재조명", "당시 장교 제시 마셀의 인터뷰", y=300), {"type": "slideL", "at": 0.3}),
            ("bodies", lower("1980년 책부터", "「외계인 시신」 이야기가 덧붙음", y=470), {"type": "slideL", "at": 5.4})],
    "S06": [archive("report_1995.jpg"), static("shade", shade()),
            ("tag", real_tag("실제 자료 · 미 공군 보고서 (1995년 발간)"), {"type": "fade", "at": 0.1})],
    "S07": [archive("mogul_train_1995.png", z=(100, 108), pan=(0, -40)), static("shade", shade()),
            ("tag", real_tag("실제 자료 · 보고서 속 모굴 풍선 사진"), {"type": "fade", "at": 0.1})],
    "S08": [video("S08"), static("shade", shade()),
            ("mogul", lower("프로젝트 모굴 · 1947년 6월 4일 띄운 4번 비행", "소련 핵실험 소리를 엿듣는 극비 풍선", y=1150), {"type": "slideL", "at": 0.3})],
    "S09": [archive("report_1997.jpg"), static("shade", shade()),
            ("tag", real_tag("실제 자료 · 미 공군 보고서 「사건 종결」 1997년"), {"type": "fade", "at": 0.1})],
    "S10": [photo("S10_b", z=(104, 112), pan=(0, 30)), static("shade", shade()),
            ("t", head("지금은 「UFO 마을」", 540, 360, 100, GOLD), {"type": "pop", "at": 0.15, "anchor": [540, 320]}),
            ("town", lower("로스웰 · UFO 박물관(1991) · UFO 축제(1995~)", "해마다 관광객 약 9만 명", y=470), {"type": "slideL", "at": 0.5})],
    "S11": [video("S10"), static("shade", shade()),
            ("t", head("풍선일까, 외계인일까", 540, 340, 96, GOLD), {"type": "pop", "at": 0.15, "anchor": [540, 300]}),
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
