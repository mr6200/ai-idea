"""Overlay parts for the 10 scenes of the moai-walk Short (1080x1920) plus the scene manifest.

Style (mystery series, episode 2): realistic documentary. The bottom layer of every scene is AI documentary
footage: a WAN 2.2 clip for the key scenes (S01 hook, S07 walking test, S10 ending) and a Seedream still moved
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


# scene timing in seconds (a WAN clip is about 5 s and may be slowed up to about 1.3x)
S = {
    "S01": (0.0, 4.4), "S02": (4.4, 7.75), "S03": (7.75, 13.3), "S04": (13.3, 20.9), "S05": (20.9, 26.95),
    "S06": (26.95, 33.25), "S07": (33.25, 39.4), "S08": (39.4, 46.9), "S09": (46.9, 52.25), "S10": (52.25, 58.0),
}

OUTLINE = 'stroke="#000" stroke-opacity="0.8" stroke-width="8" paint-order="stroke"'

SCENES = {
    # the moai stand in the upper half, so the headline sits on the grass below them
    "S01": [video("S01"), static("shade", shade()),
            ("t1", head("수십 톤 석상을", 540, 1110, 104), {"type": "pop", "at": 0.15, "anchor": [540, 1070]}),
            ("t2", head("어떻게 옮겼을까?", 540, 1270, 120, GOLD), {"type": "pop", "at": 0.7, "anchor": [540, 1230]})],
    "S02": [photo("S02_d", z=(102, 116)), static("shade", shade()),
            ("tag", lower("이스터섬 (라파누이) · 칠레 영토", "남미 대륙에서 약 3,500km", y=300), {"type": "slideL", "at": 0.3})],
    "S03": [photo("S03_a", z=(106, 114), pan=(0, 40)), static("shade", shade()),
            # the moai's face fills the top half and a hiker stands at the bottom right: cards go on its body
            ("n", lower("섬의 석상 「모아이」", "천 개 가까이 (조사마다 887~962개)", y=990), {"type": "slideL", "at": 0.2}),
            ("size", lower("평균 크기 · 가장 큰 것은 높이 약 10m", "높이 약 4m · 무게 약 12.5톤", y=1170), {"type": "slideL", "at": 2.9})],
    "S04": [photo("S04_e", z=(104, 112), pan=(-30, 0)), static("shade", shade()),
            ("q", lower("채석장 · 라노 라라쿠 화산", "모아이 대부분(약 94%)을 여기서 깎음", y=300), {"type": "slideL", "at": 0.2}),
            ("far", pill("섬 곳곳 바닷가까지 · 몇 km", 540, 560, 46), {"type": "pop", "at": 3.9, "anchor": [540, 560]})],
    "S05": [photo("S05_b", z=(108, 116), pan=(0, -30)), static("shade", shade()),
            ("t", head("섬의 전설", 540, 330, 104, GOLD), {"type": "pop", "at": 0.15, "anchor": [540, 290]}),
            ("quote", text("“모아이는 스스로 걸어갔다”", 540, 450, 60, WHITE, extra=OUTLINE), {"type": "fade", "at": 0.6}),
            ("old", lower("오랫동안의 통설", "통나무 · 썰매에 눕혀 끌었다", y=990), {"type": "slideL", "at": 2.6})],
    "S06": [photo("S06_a", z=(104, 112), pan=(0, 30)), static("shade", shade()),
            ("t", lower("2012년 · 고고학자들의 실험", "모형 석상 약 4톤 · 밧줄 3개", y=1180), {"type": "slideL", "at": 0.3})],
    "S07": [video("S06"), static("shade", shade()),
            ("how", pill("좌우로 번갈아 당기면 → 한 걸음씩", 540, 1180, 44), {"type": "pop", "at": 0.4, "anchor": [540, 1180]}),
            ("res", pill("18명 · 40분 · 100m", 540, 1300, 62, RED, WHITE), {"type": "stamp", "at": 3.5, "anchor": [540, 1300]})],
    "S08": [photo("S07_b", z=(104, 114), pan=(0, -40)), static("shade", shade()),
            ("study", lower("2025년 연구 · 옛길 위 모아이 62개", "밑동이 넓고 앞으로 5~15° 기울어짐", y=300), {"type": "slideL", "at": 0.2}),
            ("road", pill("옛길 · 폭 약 4.5m, 가운데가 오목", 540, 560, 44), {"type": "pop", "at": 4.0, "anchor": [540, 560]})],
    "S09": [photo("S03_b", z=(110, 102), pan=(0, 0)), static("shade", shade()),
            ("t", head("걷는 석상의 전설", 540, 330, 96), {"type": "pop", "at": 0.15, "anchor": [540, 290]}),
            ("debate", pill("유력하지만 아직 논쟁 중인 가설", 540, 480, 46, RED, WHITE), {"type": "stamp", "at": 3.2, "anchor": [540, 480]})],
    "S10": [video("S08"), static("shade", shade()),
            ("t", head("전설일까, 과학일까", 540, 330, 96, GOLD), {"type": "pop", "at": 0.15, "anchor": [540, 290]}),
            ("sub", pill("구독하고 다음 미스터리 보기", 540, 480, 50, RED, WHITE), {"type": "pop", "at": 0.5, "anchor": [540, 480]})],
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
