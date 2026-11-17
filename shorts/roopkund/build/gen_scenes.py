"""Overlay parts for the 12 scenes of the roopkund Short (1080x1920) plus the scene manifest.

Style (mystery series, episode 7): realistic documentary with real photos. The bottom layer of every scene is
either a real CC BY-SA photo of the lake (photos/, marked 「실제 사진」 with author and licence), a WAN 2.2 clip
for the key scenes (S01 hook, S06 hailstorm legend, S12 ending) or a Seedream still moved by a slow Ken Burns
camera; on top sit a soft dark top/bottom shade, a small series label, Black Han Sans headlines and
lower-third cards (dark glass box + gold bar, Do Hyeon). Subtitles are white Do Hyeon with a dark outline over
the bottom shade (gen_subtitles.py).

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


# scene timing in seconds (a WAN clip is about 5 s)
S = {
    "S01": (0.0, 6.1), "S02": (6.1, 9.3), "S03": (9.3, 16.35), "S04": (16.35, 20.7), "S05": (20.7, 24.25),
    "S06": (24.25, 27.6), "S07": (27.6, 32.85), "S08": (32.85, 39.35), "S09": (39.35, 45.4), "S10": (45.4, 49.15),
    "S11": (49.15, 53.3), "S12": (53.3, 58.0),
}

OUTLINE = 'stroke="#000" stroke-opacity="0.8" stroke-width="8" paint-order="stroke"'

SCENES = {
    "S01": [video("S01"), static("shade", shade()),
            ("t1", head("얼음 아래 잠든", 540, 340, 100), {"type": "pop", "at": 0.15, "anchor": [540, 300]}),
            ("t2", head("수백 명의 뼈", 540, 490, 124, GOLD), {"type": "stamp", "at": 0.8, "anchor": [540, 450]})],
    "S02": [archive("lake_2014.jpg", z=(100, 108)), static("shade", shade()),
            ("tag", real_tag("실제 사진 · 루프쿤드 호수 (2014, Schwiki, CC BY-SA 4.0)"), {"type": "fade", "at": 0.1})],
    "S03": [photo("S03_a", z=(104, 112), pan=(0, 30)), static("shade", shade()),
            ("find", lower("1942년 · 산림 감시원 하리 키샨 마드왈", "처음엔 「숨어든 일본군?」 걱정", y=1150), {"type": "slideL", "at": 0.3})],
    "S04": [archive("skeletons.jpg", z=(100, 108)), static("shade", shade()),
            ("tag", real_tag("실제 사진 · 호숫가의 유해 (Schwiki, CC BY-SA 4.0)"), {"type": "fade", "at": 0.1})],
    "S05": [photo("S05_a", z=(104, 112), pan=(0, -30)), static("shade", shade()),
            ("old", lower("오랫동안의 생각", "한꺼번에 숨진 순례 행렬?", y=300), {"type": "slideL", "at": 0.2})],
    "S06": [video("S06"), static("shade", shade()),
            ("hail", pill("우박 폭풍 전설", 540, 330, 56, RED, WHITE), {"type": "stamp", "at": 0.2, "anchor": [540, 330]})],
    "S07": [photo("S08_a", z=(104, 112)), static("shade", shade()),
            ("study", lower("2019년 · 국제 연구진 (네이처 커뮤니케이션스)", "38명의 뼈 · DNA와 연대 분석", y=300), {"type": "slideL", "at": 0.2})],
    "S08": [photo("S08_b", z=(106, 112)), static("shade", shade()),
            ("sa", lower("남아시아 계통 23명", "800년 무렵 · 여러 번에 걸쳐", y=300), {"type": "slideL", "at": 0.2}),
            ("med", lower("지중해 동부 계통 14명", "1800년 무렵 · 한 번에", y=470), {"type": "slideL", "at": 3.3})],
    "S09": [photo("S10_a", z=(104, 112), pan=(0, 30)), static("shade", shade()),
            ("sea", pill("동남아시아 계통 1명 · 1800년 무렵", 540, 330, 46), {"type": "pop", "at": 0.1, "anchor": [540, 330]}),
            ("gap", pill("약 1,000년 차이", 540, 470, 66, RED, WHITE), {"type": "stamp", "at": 2.1, "anchor": [540, 470]})],
    "S10": [archive("mystery_lake.jpg", z=(100, 108)), static("shade", shade()),
            ("tag", real_tag("실제 사진 · 얼어붙은 호수 (Shubhamrathod15, CC BY-SA)"), {"type": "fade", "at": 0.1}),
            ("raj", lower("난다 데비 라즈 자트 순례", "12년마다 호수 곁을 지남", y=1150), {"type": "slideL", "at": 0.4})],
    "S11": [photo("S10_b", z=(106, 114)), static("shade", shade()),
            ("t", head("왜 여기까지?", 540, 340, 110, GOLD), {"type": "pop", "at": 0.15, "anchor": [540, 300]})],
    "S12": [video("S12"), static("shade", shade()),
            ("t", head("호수는 아직 말이 없다", 540, 340, 92, GOLD), {"type": "pop", "at": 0.15, "anchor": [540, 300]}),
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
