"""Overlay parts for the 13 scenes of the pyramids Short (1080x1920) plus the scene manifest.

Style (mystery series, episode 9): realistic documentary built on real photos of Giza, Chichen Itza, Palenque,
Teotihuacan and Cholula (photos/, CC0 / CC BY / CC BY-SA, marked 「실제 사진」 with author and licence), WAN 2.2
clips for S01 (hook), S05 (Mesoamerican ceremony) and S13 (ending) and Seedream stills for the rest; on top sit
a soft dark top/bottom shade, a small series label, Black Han Sans headlines and lower-third cards (dark glass
box + gold bar, Do Hyeon). Subtitles are white Do Hyeon with a dark outline (gen_subtitles.py).

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
    "S01": (0.0, 6.8), "S02": (6.8, 12.05), "S03": (12.05, 15.2), "S04": (15.2, 19.35), "S05": (19.35, 22.85),
    "S06": (22.85, 27.2), "S07": (27.2, 34.55), "S08": (34.55, 38.55), "S09": (38.55, 44.95), "S10": (44.95, 47.8),
    "S11": (47.8, 50.45), "S12": (50.45, 55.75), "S13": (55.75, 61.0),
}

OUTLINE = 'stroke="#000" stroke-opacity="0.8" stroke-width="8" paint-order="stroke"'

SCENES = {
    "S01": [video("S01"), static("shade", shade()),
            ("t1", head("이집트 vs 멕시코", 540, 340, 104), {"type": "pop", "at": 0.15, "anchor": [540, 300]}),
            ("t2", head("피라미드의 차이", 540, 490, 124, GOLD), {"type": "stamp", "at": 0.8, "anchor": [540, 450]})],
    "S02": [archive("giza_khufu.jpg", z=(100, 108)), static("shade", shade()),
            ("tag", real_tag("실제 사진 · 기자 대피라미드 (Douwe C. van der Zee, CC BY-SA)"), {"type": "fade", "at": 0.1}),
            ("shape", lower("차이 ① 모양", "이집트 · 매끈한 면 + 뾰족한 꼭대기", y=1150), {"type": "slideL", "at": 1.6})],
    "S03": [archive("kukulcan.jpg", z=(100, 108)), static("shade", shade()),
            ("tag", real_tag("실제 사진 · 치첸이트사 엘 카스티요 (Kos Nina, CC0)"), {"type": "fade", "at": 0.1}),
            ("shape", lower("멕시코", "계단식 + 평평한 꼭대기 · 신전", y=1150), {"type": "slideL", "at": 0.3})],
    "S04": [archive("giza_all.jpg", z=(100, 108)), static("shade", shade()),
            ("tag", real_tag("실제 사진 · 기자의 피라미드 (Ricardo Liberato, CC BY-SA 2.0)"), {"type": "fade", "at": 0.1}),
            ("use", lower("차이 ② 쓰임", "이집트 · 파라오의 무덤", y=1150), {"type": "slideL", "at": 2.0})],
    "S05": [video("S07"), static("shade", shade()),
            ("use", lower("멕시코 (AI 재현)", "꼭대기에 신전 · 피라미드 앞에서 제사", y=300), {"type": "slideL", "at": 0.2})],
    "S06": [archive("pakal_tomb.jpg", z=(100, 108)), static("shade", shade()),
            ("tag", real_tag("실제 사진 · 팔렝케 비문의 신전 (Lousanroj, CC BY-SA 3.0)"), {"type": "fade", "at": 0.1}),
            ("exc", lower("예외 · 1952년", "피라미드 속 파칼 왕의 무덤 발견", y=1150), {"type": "slideL", "at": 0.4})],
    "S07": [archive("teo_avenue.jpg", z=(100, 108)), static("shade", shade()),
            ("tag", real_tag("실제 사진 · 테오티우아칸 (Burkhard Mücke, CC BY-SA 4.0)"), {"type": "fade", "at": 0.1}),
            ("age", lower("차이 ③ 시대 · 기자 약 4,500년 전", "태양의 피라미드 약 1,800년 전", y=1150), {"type": "slideL", "at": 2.1})],
    "S08": [archive("cholula_model.jpg", z=(100, 108)), static("shade", shade()),
            ("tag", real_tag("실제 사진 · 촐룰라 피라미드 모형 (AlejandroLinaresGarcia, CC BY-SA)"), {"type": "fade", "at": 0.1}),
            ("layer", lower("멕시코의 짓는 법", "옛 피라미드 위에 새 층을 덧씌워 키움", y=1150), {"type": "slideL", "at": 0.3})],
    "S09": [archive("cholula.jpg", z=(100, 108)), static("shade", shade()),
            ("tag", real_tag("실제 사진 · 촐룰라 피라미드 (Diego Delso, CC BY-SA 3.0)"), {"type": "fade", "at": 0.1}),
            ("age", lower("촐룰라 피라미드", "기원전 3세기부터 약 1,000년 동안 쌓음", y=1150), {"type": "slideL", "at": 0.3}),
            ("big", pill("부피 세계 1위 · 약 445만 세제곱미터", 540, 520, 46, RED, WHITE), {"type": "stamp", "at": 2.9, "anchor": [540, 520]})],
    "S10": [archive("cholula.jpg", z=(112, 124), pan=(60, 80)), static("shade", shade()),
            ("tag", real_tag("실제 사진 · 촐룰라 피라미드 (Diego Delso, CC BY-SA 3.0)"), {"type": "fade", "at": 0.1}),
            ("church", pill("언덕 위 교회 · 스페인 정복 뒤에 세움", 540, 1180, 46), {"type": "pop", "at": 0.4, "anchor": [540, 1180]})],
    "S11": [photo("S16_a", z=(104, 112)), static("shade", shade()),
            ("q", head("왜 둘 다 피라미드?", 540, 340, 100, GOLD), {"type": "pop", "at": 0.15, "anchor": [540, 300]})],
    "S12": [photo("S16_b", z=(104, 112), pan=(0, 30)), static("shade", shade()),
            ("why", lower("아래는 넓게, 위는 좁게 (유력한 설명)", "높이 쌓아도 무너지지 않는 모양", y=300), {"type": "slideL", "at": 0.2})],
    "S13": [video("S18"), static("shade", shade()),
            ("t", head("닮은 듯 다른 두 피라미드", 540, 340, 88, GOLD), {"type": "pop", "at": 0.15, "anchor": [540, 300]}),
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
