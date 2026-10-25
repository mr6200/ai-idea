"""Full 150 s timeline: per-scene part animations (S01-S18) and subtitle cues."""
import json
import os

ROOT = os.path.dirname(os.path.abspath(__file__))

S01_S03 = [
    {"id": "S01", "start": 0, "end": 4, "parts": [
        {"name": "bg", "anim": {"type": "none"}},
        {"name": "label", "anim": {"type": "fade", "at": 0.0}},
        {"name": "sparkles", "anim": {"type": "fade", "at": 0.5}},
        {"name": "paper", "anim": {"type": "pop", "at": 0.15, "anchor": [540, 745]}, "idle": "bob"},
        {"name": "callout", "anim": {"type": "pop", "at": 0.9, "anchor": [862, 430]}},
        {"name": "cap1", "anim": {"type": "pop", "at": 1.3, "anchor": [537, 1168]}},
        {"name": "cap2", "anim": {"type": "fade", "at": 1.9}},
    ]},
    {"id": "S02", "start": 4, "end": 9, "parts": [
        {"name": "bg", "anim": {"type": "none"}},
        {"name": "label", "anim": {"type": "none"}},
        {"name": "title1", "anim": {"type": "fade", "at": 0.0}},
        {"name": "title2", "anim": {"type": "pop", "at": 0.2, "anchor": [541, 545]}},
        {"name": "stack", "anim": {"type": "growY", "at": 0.4, "anchor": [310, 1180], "dur": 4.0, "ease": "accel"}},
        {"name": "arrow", "anim": {"type": "growY", "at": 0.4, "anchor": [505, 1180], "dur": 4.0, "ease": "accel"}},
        {"name": "timeline", "anim": {"type": "wipeD", "at": 0.6, "dur": 3.4}},
        {"name": "row1", "anim": {"type": "slideR", "at": 1.0}},
        {"name": "chak1", "anim": {"type": "pop", "at": 1.0, "anchor": [218, 1336]}},
        {"name": "row2", "anim": {"type": "slideR", "at": 2.0}},
        {"name": "chak2", "anim": {"type": "pop", "at": 2.0, "anchor": [501, 1291]}},
        {"name": "row3", "anim": {"type": "slideR", "at": 2.9}},
        {"name": "chak3", "anim": {"type": "pop", "at": 2.9, "anchor": [822, 1330]}},
        {"name": "row4", "anim": {"type": "stamp", "at": 3.8, "anchor": [700, 1142]}},
    ]},
    {"id": "S03", "start": 9, "end": 12, "zoomOut": True, "parts": [
        {"name": "bg", "anim": {"type": "none"}},
        {"name": "earth", "anim": {"type": "none"}},
        {"name": "column", "anim": {"type": "growY", "at": 0.2, "anchor": [540, 1520], "dur": 1.0, "ease": "decel"}},
        {"name": "moon", "anim": {"type": "pop", "at": 0.0, "anchor": [540, 420]}},
        {"name": "dist", "anim": {"type": "pop", "at": 1.25, "anchor": [775, 845]}},
        {"name": "caption", "anim": {"type": "stamp", "at": 1.5, "anchor": [540, 1210]}},
    ]},
]

# (start, end, text) in comp seconds; "\n" splits lines
CUES = [
    (0.1, 3.3, "두께 0.1mm 종이를\n42번 접으면"),
    (3.3, 5.0, "어디까지 닿을까요?"),
    (9.6, 10.7, "정답은… 달입니다"),
    (10.7, 12.0, "이게 바로\n‘복리’의 힘이에요"),
    (12.2, 15.6, "단리는 원금에만\n이자가 붙습니다"),
    (15.6, 19.8, "복리는 이자에도\n이자가 붙죠"),
    (20.1, 24.2, "100만 원을 연 7%로 굴리면\n첫해엔 7만 원 차이"),
    (24.2, 27.8, "별거 아닌 것 같죠?"),
    (28.2, 31.2, "그런데 10년이 지나면"),
    (31.2, 34.8, "복리 쪽은 거의 두 배,\n약 197만 원이 됩니다"),
    (35.2, 39.0, "돈이 두 배가 되는 시간을\n바로 계산하는 방법"),
    (39.0, 42.8, "72를 수익률로\n나누면 돼요"),
    (43.2, 47.5, "연 7%면 약 10년,\n연 10%면 약 7년"),
    (47.5, 54.8, "시간이 길어질수록\n두 배, 네 배, 여덟 배로"),
    (55.2, 58.5, "두 사람이 있습니다"),
    (58.5, 62.8, "누가 더 많이\n모았을까요?"),
    (63.2, 67.4, "A는 25살부터 매년 360만 원\n딱 10년만 넣고 멈췄어요"),
    (67.4, 69.7, "총 3,600만 원"),
    (69.7, 73.9, "B는 35살부터 매년 360만 원\n30년 동안 꾸준히"),
    (73.9, 76.1, "총 1억 800만 원"),
    (76.2, 80.0, "둘 다 연 7%로\n65살까지 굴렸다면?"),
    (80.0, 87.8, "10년 먼저 시작한 A가\n끝까지 앞서갑니다"),
    (88.2, 90.4, "B는 약 3억 4천만 원"),
    (90.4, 92.6, "그런데 A는…\n약 3억 7,900만 원"),
    (92.6, 94.8, "차이는 단 하나,\n10년 먼저 시작한 것"),
    (95.2, 100.0, "워런 버핏의\n재산 대부분은"),
    (100.0, 104.8, "65세 이후에\n쌓였습니다"),
    (105.2, 109.5, "진짜 비밀은 70년 넘게\n멈추지 않은 시간"),
    (109.5, 114.8, "처음엔 평평하다가\n어느 순간 하늘로 꺾입니다"),
    (115.2, 119.0, "복리는 돈에만\n통하는 게 아닙니다"),
    (119.0, 124.8, "매일 1%씩 나아지면\n1년 뒤 약 37.8배"),
    (125.2, 130.0, "매일 1%씩 나빠지면\n0.03배로 줄어들어요"),
    (130.0, 134.8, "공부, 운동, 습관도\n똑같이 쌓입니다"),
    (135.2, 139.5, "필요한 건 큰돈이 아니라\n일찍 시작하는 용기"),
    (139.5, 144.8, "가장 좋은 때는 10년 전,\n두 번째는 바로 지금"),
    (145.2, 149.8, "더 많은 지식이 궁금하다면\n구독해 주세요"),
]

IDLE = {("S09", "charA"), ("S09", "charB"), ("S17", "paper"), ("S15", "runner")}


def build():
    with open(os.path.join(ROOT, "manifest_s04_s18.json")) as f:
        rest = json.load(f)
    for sc in rest:
        for p in sc["parts"]:
            if (sc["id"], p["name"]) in IDLE:
                p["idle"] = "bob"
    scenes = S01_S03 + rest
    for a, b in zip(scenes, scenes[1:]):
        assert a["end"] == b["start"], (a["id"], b["id"])
    assert scenes[-1]["end"] == 150
    data = {"duration": 150, "fps": 30, "width": 1080, "height": 1920,
            "scenes": scenes, "cues": [{"start": s, "end": e, "text": t} for s, e, t in CUES]}
    with open(os.path.join(ROOT, "manifest.json"), "w") as f:
        json.dump(data, f, ensure_ascii=False, indent=1)
    return data


if __name__ == "__main__":
    d = build()
    print(len(d["scenes"]), "scenes,", len(d["cues"]), "cues")
