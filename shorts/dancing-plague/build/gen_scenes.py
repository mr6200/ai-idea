"""Overlay parts for the 11 scenes of the dancing-plague Short (1080x1920) plus the scene manifest.

Style (mystery series, episode 5): realistic documentary with real archive images. The bottom layer of every
scene is either a real public-domain print (photos/: an old print of the 1518 Strasbourg dancers and two
Molenbeek dancing-pilgrims pictures after Bruegel, marked 「실제 옛 그림」), a WAN 2.2 clip for the key scenes
(S01 hook, S05 musicians, S11 ending) or a Seedream still moved by a slow Ken Burns camera; on top sit a soft
dark top/bottom shade, a small series label, Black Han Sans headlines and lower-third cards (dark glass box +
gold bar, Do Hyeon). Subtitles are white Do Hyeon with a dark outline over the bottom shade (gen_subtitles.py).

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


# scene timing in seconds (a WAN clip is about 5 s and may be slowed up to about 1.2x here)
S = {
    "S01": (0.0, 5.9), "S02": (5.9, 9.55), "S03": (9.55, 15.4), "S04": (15.4, 20.35), "S05": (20.35, 25.9),
    "S06": (25.9, 33.0), "S07": (33.0, 38.45), "S08": (38.45, 42.6), "S09": (42.6, 50.55), "S10": (50.55, 55.3),
    "S11": (55.3, 60.0),
}

OUTLINE = 'stroke="#000" stroke-opacity="0.8" stroke-width="8" paint-order="stroke"'

SCENES = {
    "S01": [video("S01"), static("shade", shade()),
            ("t1", head("1518년 여름", 540, 340, 96), {"type": "pop", "at": 0.15, "anchor": [540, 300]}),
            ("t2", head("멈출 수 없는 춤", 540, 490, 124, GOLD), {"type": "stamp", "at": 0.8, "anchor": [540, 450]})],
    "S02": [archive("strasbourg_1518_old.jpg", z=(100, 108)), static("shade", shade()),
            ("tag", real_tag("실제 옛 그림 · 1518년 스트라스부르의 춤 (작가 미상)"), {"type": "fade", "at": 0.1})],
    "S03": [photo("S02_a", z=(104, 112), pan=(0, 30)), static("shade", shade()),
            ("n", lower("1518년 7월 · 스트라스부르", "며칠 만에 30명 넘게 → 8월엔 50~400명", y=300), {"type": "slideL", "at": 0.2})],
    "S04": [photo("S04_a", z=(104, 112)), static("shade", shade()),
            ("rx", lower("시 의회와 의사들의 처방", "「춤을 춰서 털어 내라」", y=300), {"type": "slideL", "at": 2.2})],
    "S05": [video("S05"), static("shade", shade()),
            ("hall", pill("회관을 내주고 악사까지", 540, 330, 50), {"type": "pop", "at": 0.2, "anchor": [540, 330]}),
            ("ban", pill("결국 춤 금지", 540, 470, 64, RED, WHITE), {"type": "stamp", "at": 2.7, "anchor": [540, 470]})],
    "S06": [photo("S07_a", z=(104, 112), pan=(0, -30)), static("shade", shade()),
            ("end", lower("1518년 9월 · 성 비투스 성지로", "빨간 신발을 신고 기도하자 잦아듦", y=300), {"type": "slideL", "at": 0.2}),
            ("dead", pill("사망자가 있었는지는 논쟁 중", 540, 540, 46, RED, WHITE), {"type": "stamp", "at": 4.3, "anchor": [540, 540]})],
    "S07": [photo("S09_d", z=(102, 112)), static("shade", shade()),
            ("q", head("원인은?", 540, 340, 110, GOLD), {"type": "pop", "at": 0.1, "anchor": [540, 300]}),
            ("ergot", lower("가설 ① 맥각(곡물 곰팡이) 중독", "며칠씩 춤추긴 어렵다는 반론이 많음", y=1150), {"type": "slideL", "at": 1.7})],
    "S08": [photo("S10_a", z=(104, 112), pan=(-20, 0)), static("shade", shade()),
            ("psy", lower("가설 ② 집단 심리 현상", "굶주림 · 병 · 공포가 겹친 시기", y=300), {"type": "slideL", "at": 0.1})],
    "S09": [archive("molenbeek_engraving.jpg", z=(100, 108), pan=(0, 40)), static("shade", shade()),
            ("tag", real_tag("실제 옛 판화 · 1642년 (브뤼헐의 1564년 그림)"), {"type": "fade", "at": 0.1})],
    "S10": [archive("molenbeek_painting.jpg", z=(100, 110)), static("shade", shade()),
            ("tag", real_tag("실제 옛 그림 · 아들 브뤼헐 「몰렌베이크의 춤」"), {"type": "fade", "at": 0.1})],
    "S11": [video("S12"), static("shade", shade()),
            ("t", head("멈추지 않은 춤의 수수께끼", 540, 340, 84, GOLD), {"type": "pop", "at": 0.15, "anchor": [540, 300]}),
            ("sub", pill("구독하고 다음 미스터리 보기", 540, 490, 50, RED, WHITE), {"type": "pop", "at": 0.3, "anchor": [540, 490]})],
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
