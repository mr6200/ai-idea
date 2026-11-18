"""Overlay parts for the 15 scenes of the voynich Short (1080x1920) plus the scene manifest.

Style (mystery series, episode 8): realistic documentary built mostly on real public-domain images: pages of
the Voynich manuscript (Beinecke Library MS 408), a photo of Wilfrid Voynich and a portrait of Rudolf II
(photos/, marked 「실제 자료」). WAN 2.2 clips for S01 (hook), S11 (codebreakers) and S15 (ending), Seedream
stills moved by a slow Ken Burns camera for the rest; on top sit a soft dark top/bottom shade, a small series
label, Black Han Sans headlines and lower-third cards (dark glass box + gold bar, Do Hyeon). Subtitles are white
Do Hyeon with a dark outline over the bottom shade (gen_subtitles.py).

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
    "S01": (0.0, 5.0), "S02": (5.0, 7.05), "S03": (7.05, 10.95), "S04": (10.95, 14.55), "S05": (14.55, 19.2),
    "S06": (19.2, 22.95), "S07": (22.95, 24.65), "S08": (24.65, 26.75), "S09": (26.75, 30.1), "S10": (30.1, 35.25),
    "S11": (35.25, 39.1), "S12": (39.1, 44.75), "S13": (44.75, 48.55), "S14": (48.55, 52.6), "S15": (52.6, 58.0),
}

OUTLINE = 'stroke="#000" stroke-opacity="0.8" stroke-width="8" paint-order="stroke"'

SCENES = {
    "S01": [video("S01"), static("shade", shade()),
            ("t1", head("600년 동안", 540, 340, 100), {"type": "pop", "at": 0.15, "anchor": [540, 300]}),
            ("t2", head("아무도 못 읽은 책", 540, 490, 112, GOLD), {"type": "stamp", "at": 0.8, "anchor": [540, 450]})],
    "S02": [archive("page_flowers.jpg", z=(100, 108)), static("shade", shade()),
            ("tag", real_tag("실제 자료 · 보이니치 필사본 (예일대 바이네키 도서관)"), {"type": "fade", "at": 0.1})],
    "S03": [archive("wilfrid_voynich.jpg", z=(100, 106)), static("shade", shade()),
            ("tag", real_tag("실제 사진 · 윌프리드 보이니치 (1920년 무렵)"), {"type": "fade", "at": 0.1})],
    "S04": [photo("S04_a", z=(104, 112)), static("shade", shade()),
            ("c14", lower("2009년 · 미국 애리조나대 탄소 연대 측정", "양피지는 1404~1438년", y=300), {"type": "slideL", "at": 0.3})],
    "S05": [archive("page_text.jpg", z=(100, 110), pan=(0, 40)), static("shade", shade()),
            ("tag", real_tag("실제 자료 · 글만 가득한 페이지"), {"type": "fade", "at": 0.1}),
            ("n", lower("약 240쪽 · 단어 약 3만 8천 개", "뜻을 아는 사람이 없음", y=1150), {"type": "slideL", "at": 0.5})],
    "S06": [archive("page_plant.jpg", z=(100, 108)), static("shade", shade()),
            ("tag", real_tag("실제 자료 · 정체를 알 수 없는 식물 그림"), {"type": "fade", "at": 0.1})],
    "S07": [archive("page_rosettes.jpg", z=(100, 110)), static("shade", shade()),
            ("tag", real_tag("실제 자료 · 둥근 무늬 그림 (펼침 페이지)"), {"type": "fade", "at": 0.1})],
    "S08": [archive("page_bathing.jpg", z=(100, 108)), static("shade", shade()),
            ("tag", real_tag("실제 자료 · 초록 물속의 여인들"), {"type": "fade", "at": 0.1})],
    "S09": [archive("page_jars.jpg", z=(100, 108), pan=(0, 40)), static("shade", shade()),
            ("tag", real_tag("실제 자료 · 약병 그림과 짧은 글"), {"type": "fade", "at": 0.1})],
    "S10": [archive("rudolf2.jpg", z=(100, 106)), static("shade", shade()),
            ("tag", real_tag("옛 그림 · 황제 루돌프 2세 (한스 폰 아헨)"), {"type": "fade", "at": 0.1}),
            ("claim", lower("1665년 무렵 마르치의 편지", "「루돌프 2세가 600두카트에 샀다」", y=1150), {"type": "slideL", "at": 0.5})],
    "S11": [video("S11"), static("shade", shade()),
            ("wf", lower("윌리엄 프리드먼 · 미국의 전설적 암호 해독가", "끝내 해독 실패", y=300), {"type": "slideL", "at": 0.3})],
    "S12": [photo("S01_b", z=(104, 112), pan=(0, 30)), static("shade", shade()),
            ("hoax", lower("가설 ① 누군가 꾸며 낸 가짜", "가설 ② 알 수 없는 언어 · 암호", y=300), {"type": "slideL", "at": 0.2}),
            ("rule", pill("글자 배열엔 언어 같은 규칙", 540, 560, 46), {"type": "pop", "at": 2.7, "anchor": [540, 560]})],
    "S13": [photo("S04_b", z=(104, 112)), static("shade", shade()),
            ("none", pill("해독 주장 여러 번 · 인정된 것 없음", 540, 330, 50, RED, WHITE), {"type": "stamp", "at": 0.3, "anchor": [540, 330]})],
    "S14": [photo("S16_b", z=(104, 112)), static("shade", shade()),
            ("t", head("600년의 수수께끼", 540, 340, 104, GOLD), {"type": "pop", "at": 0.15, "anchor": [540, 300]})],
    "S15": [video("S16"), static("shade", shade()),
            ("t", head("당신이라면 풀 수 있을까?", 540, 340, 84, GOLD), {"type": "pop", "at": 0.15, "anchor": [540, 300]}),
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
