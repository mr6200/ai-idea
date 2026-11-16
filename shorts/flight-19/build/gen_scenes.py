"""Overlay parts for the 14 scenes of the flight-19 Short (1080x1920) plus the scene manifest.

Style (mystery series, episode 6): realistic documentary with real archive images. The bottom layer of every
scene is either a real archive image (photos/: US Navy / Coast Guard photos of the same aircraft types and a
CC BY route map, marked 「실제 사진」), a WAN 2.2 clip for the key scenes (S01 hook, S05 storm, S14 ending) or a
Seedream still moved by a slow Ken Burns camera; on top sit a soft dark top/bottom shade, a small series label,
Black Han Sans headlines and lower-third cards (dark glass box + gold bar, Do Hyeon). Subtitles are white
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
    "S01": (0.0, 5.05), "S02": (5.05, 8.9), "S03": (8.9, 13.6), "S04": (13.6, 16.15), "S05": (16.15, 20.2),
    "S06": (20.2, 24.35), "S07": (24.35, 27.85), "S08": (27.85, 34.45), "S09": (34.45, 41.65), "S10": (41.65, 45.55),
    "S11": (45.55, 48.6), "S12": (48.6, 52.55), "S13": (52.55, 55.4), "S14": (55.4, 61.0),
}

OUTLINE = 'stroke="#000" stroke-opacity="0.8" stroke-width="8" paint-order="stroke"'

SCENES = {
    # the planes fill the lower two thirds, the storm clouds the top
    "S01": [video("S01"), static("shade", shade()),
            ("t1", head("1945년 12월 5일", 540, 340, 92), {"type": "pop", "at": 0.15, "anchor": [540, 300]}),
            ("t2", head("사라진 폭격기 5대", 540, 480, 116, GOLD), {"type": "stamp", "at": 0.8, "anchor": [540, 440]})],
    "S02": [archive("avengers_1942.jpg", z=(100, 108)), static("shade", shade()),
            ("tag", real_tag("실제 사진 · 같은 기종 어벤저 (1942년, 미 해군)"), {"type": "fade", "at": 0.1})],
    "S03": [photo("S03_a", z=(104, 114), pan=(-30, 0)), static("shade", shade()),
            ("who", lower("플라이트 19 · 편대장 찰스 테일러 중위", "「나침반이 둘 다 고장 났다」", y=1150), {"type": "slideL", "at": 2.6})],
    "S04": [photo("S04_a", z=(104, 110)), static("shade", shade()),
            ("lost", pill("방향을 잃은 편대", 540, 330, 54, RED, WHITE), {"type": "stamp", "at": 0.3, "anchor": [540, 330]})],
    "S05": [video("S05"), static("shade", shade()),
            ("night", lower("해가 진 뒤 · 거친 바다", "저녁 무렵 마지막 교신", y=300), {"type": "slideL", "at": 0.2})],
    "S06": [archive("pbm5_mariner_1945.jpg", z=(100, 108)), static("shade", shade()),
            ("tag", real_tag("실제 사진 · 같은 기종 PBM-5 마리너 (미 해군)"), {"type": "fade", "at": 0.1})],
    "S07": [photo("S07_d", z=(104, 112), pan=(0, -20)), static("shade", shade()),
            ("fire", lower("밤 9시 15분 무렵 · 유조선의 보고", "하늘의 불길, 약 10분 동안", y=300), {"type": "slideL", "at": 0.2})],
    "S08": [photo("S08_a", z=(104, 112)), static("shade", shade()),
            ("search", lower("닷새 동안의 수색", "배와 비행기 수백 대 · 잔해 없음", y=300), {"type": "slideL", "at": 0.2}),
            ("n", pill("폭격기 14명 + 구조기 13명 = 27명", 540, 560, 46, RED, WHITE), {"type": "stamp", "at": 3.9, "anchor": [540, 560]})],
    "S09": [archive("flight19_map.png", z=(100, 108)), static("shade", shade()),
            ("tag", real_tag("비행 경로 지도 · CC BY 2.5 (Anynobody · Moriori)"), {"type": "fade", "at": 0.1})],
    "S10": [photo("S04_b", z=(106, 112)), static("shade", shade()),
            ("navy", lower("해군 조사 보고서 (약 500쪽)", "편대장 실수 → 「원인 불명」", y=1150), {"type": "slideL", "at": 0.2})],
    "S11": [archive("pbm_takeoff.jpg", z=(100, 108)), static("shade", shade()),
            ("tag", real_tag("실제 사진 · PBM 마리너 (미 해안 경비대)"), {"type": "fade", "at": 0.1})],
    "S12": [photo("S10_a", z=(104, 112), pan=(0, 30)), static("shade", shade()),
            ("safe", lower("로이즈 보험 · 미 해안 경비대", "다른 바다보다 위험하지 않음", y=300), {"type": "slideL", "at": 0.2})],
    "S13": [photo("S11_b", z=(104, 110)), static("shade", shade()),
            ("six", pill("비행기 6대 · 지금도 미발견", 540, 330, 56, RED, WHITE), {"type": "stamp", "at": 0.3, "anchor": [540, 330]})],
    "S14": [video("S11"), static("shade", shade()),
            ("t", head("바다는 아직 답이 없다", 540, 340, 92, GOLD), {"type": "pop", "at": 0.15, "anchor": [540, 300]}),
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
