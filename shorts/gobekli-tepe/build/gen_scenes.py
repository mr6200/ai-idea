"""Overlay parts for the 13 scenes of the Göbekli Tepe Short (1080x1920) plus the scene manifest.

Style (mystery series, episode 10): realistic documentary built on real photos of Göbekli Tepe (photos/, CC BY /
CC BY-SA, marked 「실제 사진」 with author and licence), WAN 2.2 clips for S01 (hook), S08 (moving a pillar) and
S13 (ending) and Seedream stills for S07, S09 and S10; on top sit a soft dark top/bottom shade, a small series
label, Black Han Sans headlines and lower-third cards (dark glass box + gold bar, Do Hyeon). Subtitles are white
Do Hyeon with a dark outline (gen_subtitles.py).

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
    "S01": (0.0, 6.85), "S02": (6.85, 11.25), "S03": (11.25, 16.55), "S04": (16.55, 23.15), "S05": (23.15, 26.65),
    "S06": (26.65, 30.45), "S07": (30.45, 34.75), "S08": (34.75, 39.25), "S09": (39.25, 44.55), "S10": (44.55, 47.95),
    "S11": (47.95, 52.85), "S12": (52.85, 56.25), "S13": (56.25, 62.0),
}

OUTLINE = 'stroke="#000" stroke-opacity="0.8" stroke-width="8" paint-order="stroke"'

SCENES = {
    "S01": [video("S01"), static("shade", shade()),
            ("t1", head("피라미드보다 7,000년 앞선", 540, 340, 84), {"type": "pop", "at": 0.15, "anchor": [540, 310]}),
            ("t2", head("괴베클리 테페", 540, 490, 124, GOLD), {"type": "stamp", "at": 3.8, "anchor": [540, 450]})],
    "S02": [archive("landscape.jpg", z=(100, 108)), static("shade", shade()),
            ("tag", real_tag("실제 사진 · 괴베클리 테페 언덕 (Radosław Botev, CC BY 3.0)"), {"type": "fade", "at": 0.1}),
            ("find", lower("1963년 첫 조사", "중세 무덤 터로 보고 지나침", y=1150), {"type": "slideL", "at": 0.4})],
    "S03": [archive("pillars_c.jpg", z=(100, 108)), static("shade", shade()),
            ("tag", real_tag("실제 사진 · 발굴된 T자 돌기둥 (Klaus-Peter Simon, CC BY-SA 3.0)"), {"type": "fade", "at": 0.1}),
            ("who", lower("1994년 · 독일 고고학자 클라우스 슈미트", "묻혀 있던 돌 = T자 돌기둥", y=1150), {"type": "slideL", "at": 0.4})],
    "S04": [archive("site_circles.jpg", z=(100, 108)), static("shade", shade()),
            ("tag", real_tag("실제 사진 · 원을 그리며 선 돌기둥 (Zhengan, CC BY-SA 4.0)"), {"type": "fade", "at": 0.1}),
            ("ring", lower("발굴 결과", "돌기둥이 원을 그리며 둘러섬", y=1150), {"type": "slideL", "at": 0.3}),
            ("big", pill("가운데 기둥 · 높이 5.5m · 10톤 가까이", 540, 1080, 46, RED, WHITE), {"type": "stamp", "at": 2.8, "anchor": [540, 1080]})],
    "S05": [archive("reliefs.jpg", z=(100, 108)), static("shade", shade()),
            ("tag", real_tag("실제 사진 · 기둥의 동물 조각 (Klaus-Peter Simon, CC BY-SA 3.0)"), {"type": "fade", "at": 0.1}),
            ("ani", lower("기둥에 새긴 동물", "여우 · 멧돼지 · 뱀 · 새 등", y=1150), {"type": "slideL", "at": 0.3})],
    "S06": [archive("arm_fox.jpg", z=(100, 108)), static("shade", shade()),
            ("tag", real_tag("실제 사진 · 팔과 여우가 새겨진 기둥 (Guérin Nicolas, CC BY-SA 3.0)"), {"type": "fade", "at": 0.1}),
            ("arm", lower("사람을 닮은 기둥", "옆면에 팔과 손이 새겨짐", y=1150), {"type": "slideL", "at": 0.3})],
    "S07": [photo("S07_e", z=(104, 112)), static("shade", shade()),
            ("age", lower("약 1만 1,600년 전 (AI 재현)", "스톤헨지보다 6,000년 넘게 앞섬", y=300), {"type": "slideL", "at": 0.2})],
    "S08": [video("S08"), static("shade", shade()),
            ("no", lower("글자 · 바퀴 · 금속 도구 없음 (AI 재현)", "사냥 · 채집하던 사람들이 세움", y=300), {"type": "slideL", "at": 0.2})],
    "S09": [photo("S09_a", z=(104, 112)), static("shade", shade()),
            ("q", head("왜 지었을까?", 540, 340, 100, GOLD), {"type": "pop", "at": 0.15, "anchor": [540, 300]}),
            ("idea", lower("발굴자 슈미트의 생각 (AI 재현)", "여러 무리가 모여 의식을 치른 신전", y=1150), {"type": "slideL", "at": 1.7})],
    "S10": [photo("S10_a", z=(104, 112), pan=(0, 30)), static("shade", shade()),
            ("farm", lower("슈미트의 가설 (AI 재현)", "모인 사람을 먹이려다 농사가 시작?", y=300), {"type": "slideL", "at": 0.2})],
    "S11": [archive("pillars_c.jpg", z=(112, 122), pan=(-60, 40)), static("shade", shade()),
            ("tag", real_tag("실제 사진 · 괴베클리 테페 (Klaus-Peter Simon, CC BY-SA 3.0)"), {"type": "fade", "at": 0.1}),
            ("new", lower("최근 발굴", "집 · 물 저장고 흔적 → 사람이 살았다?", y=1150), {"type": "slideL", "at": 0.4})],
    "S12": [archive("roof2023.jpg", z=(100, 108)), static("shade", shade()),
            ("tag", real_tag("실제 사진 · 지붕을 씌운 오늘의 유적 (Bjelica, CC BY 4.0)"), {"type": "fade", "at": 0.1}),
            ("now", lower("2018년 유네스코 세계유산", "누가, 왜 지었는지는 아직 수수께끼", y=1150), {"type": "slideL", "at": 0.3})],
    "S13": [video("S13"), static("shade", shade()),
            ("t", head("괴베클리 테페", 540, 340, 100, GOLD), {"type": "pop", "at": 0.15, "anchor": [540, 300]}),
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
