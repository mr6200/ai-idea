"""Overlay parts for the 8 scenes of the mary-celeste Short (1080x1920) plus the scene manifest.

Style (mystery series, episode 1): realistic historical documentary. The bottom layer of every scene is
AI documentary footage (Seedream still animated by WAN 2.2, prepared by prep_footage.py as parts/Sxx/video.mp4);
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
LABEL = "세계의 미스터리 · 1화"

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


def static(name, body):
    return (name, body, {"type": "none"})


# scene timing in seconds; scenes with two clips cut at prep_footage.SPLIT
S = {
    "S01": (0.0, 6.3), "S02": (6.3, 11.6), "S03": (11.6, 21.1), "S04": (21.1, 30.9),
    "S05": (30.9, 38.0), "S06": (38.0, 44.9), "S07": (44.9, 52.7), "S08": (52.7, 61.0),
}

OUTLINE = 'stroke="#000" stroke-opacity="0.8" stroke-width="8" paint-order="stroke"'

SCENES = {
    # the ship fills the upper half, so the headline sits on the sea below it
    "S01": [video("S01"), static("shade", shade()),
            ("t1", head("사람만 사라진", 540, 1110, 104), {"type": "pop", "at": 0.15, "anchor": [540, 1070]}),
            ("t2", head("유령선", 540, 1290, 170, GOLD), {"type": "stamp", "at": 0.7, "anchor": [540, 1230]}),
            ("tag", text("메리 셀레스트호 · 1872년", 540, 300, 48, WHITE, extra=OUTLINE), {"type": "fade", "at": 1.0})],
    "S02": [video("S02"), static("shade", shade()),
            ("tag", lower("1872년 12월 4일 · 발견", "아조레스 제도와 포르투갈 사이", y=1150), {"type": "slideL", "at": 0.3}),
            ("none", pill("탄 사람 0명", 540, 330, 56, RED, WHITE), {"type": "stamp", "at": 3.7, "anchor": [540, 330]})],
    "S03": [video("S03", "S03b"), static("shade", shade()),
            # the doll and bunk are mid-frame; cards stay in the top band
            ("who", lower("사라진 사람 10명", "선장 · 아내 · 두 살 딸 + 선원 7명", y=300), {"type": "slideL", "at": 0.3}),
            ("food", lower("배에 남아 있던 것", "약 6개월 치 식량과 물", y=480), {"type": "slideL", "at": 3.3}),
            ("cargo", pill("술통 1,701개 · 빈 통은 9개뿐", 540, 740, 44), {"type": "pop", "at": 6.4, "anchor": [540, 740]})],
    "S04": [video("S04", "S04b"), static("shade", shade()),
            ("t", head("따뜻한 찻잔?", 540, 380, 120), {"type": "pop", "at": 0.15, "anchor": [540, 340]}),
            ("no", pill("기록에 없어요", 540, 560, 64, RED, WHITE), {"type": "stamp", "at": 3.8, "anchor": [540, 560]}),
            ("doyle", lower("1884년 · 코난 도일의 단편소설", "배 이름도 「마리 셀레스트」로 바꿈", y=720), {"type": "slideL", "at": 5.5})],
    "S05": [video("S05", "S05b"), static("shade", shade()),
            ("t", head("정말 사라진 것", 540, 380, 110), {"type": "pop", "at": 0.15, "anchor": [540, 340]}),
            ("boat", pill("작은 구명보트", 540, 560, 62, RED, WHITE), {"type": "stamp", "at": 0.6, "anchor": [540, 560]}),
            ("rest", pill("항해 도구 · 배 서류 대부분", 540, 720, 46), {"type": "pop", "at": 2.4, "anchor": [540, 720]})],
    # the judge's back fills the bottom of the frame; cards stay in the top band
    "S06": [video("S06"), static("shade", shade()),
            ("court", lower("1872년 12월 ~ 1873년 · 지브롤터 법정", "살인 의심 → 배를 꼼꼼히 조사", y=300), {"type": "slideL", "at": 0.3}),
            ("none", pill("범죄 흔적 없음", 540, 548, 66, RED, WHITE), {"type": "stamp", "at": 4.0, "anchor": [540, 548]})],
    "S07": [video("S07"), static("shade", shade()),
            ("t", head("남은 단서", 540, 380, 120), {"type": "pop", "at": 0.15, "anchor": [540, 340]}),
            ("water", lower("짐칸에 찬 바닷물", "약 1.1m (3.5피트)", y=470), {"type": "slideL", "at": 0.5}),
            ("theory", lower("여러 가설 · 아무것도 확인되지 않음", "펌프 고장 · 알코올 증기 · 해상 지진", y=1150), {"type": "slideL", "at": 2.8})],
    "S08": [video("S08"), static("shade", shade()),
            ("t1", head("150년 넘게", 540, 380, 110), {"type": "pop", "at": 0.15, "anchor": [540, 340]}),
            ("t2", head("풀리지 않은 수수께끼", 540, 520, 90, GOLD), {"type": "pop", "at": 0.7, "anchor": [540, 480]}),
            ("sub", pill("구독하고 다음 미스터리 보기", 540, 1250, 50, RED, WHITE), {"type": "pop", "at": 3.2, "anchor": [540, 1250]})],
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
            if anim["type"] != "video":
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
