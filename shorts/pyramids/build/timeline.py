"""Full 61 s timeline: scene part animations from gen_scenes.py plus subtitle cues."""
import json
import os

ROOT = os.path.dirname(os.path.abspath(__file__))

# (start, end, text) in comp seconds; "\n" splits lines
CUES = [
    (0.1, 3.4, "서로 만난 적도 없는 두 문명이\n똑같이 피라미드를 쌓았어요"),
    (3.5, 6.6, "이집트와 멕시코,\n그런데 자세히 보면 완전히 달라요"),
    (7.0, 8.3, "첫째, 모양이에요"),
    (8.4, 12.0, "이집트 피라미드는 원래 면이 매끈하고\n꼭대기가 뾰족했죠"),
    (12.1, 15.0, "멕시코 피라미드는 계단식이고,\n꼭대기가 평평해요"),
    (15.4, 17.1, "둘째, 쓰임이 달라요"),
    (17.2, 19.3, "이집트 피라미드는\n파라오의 무덤이었고"),
    (19.4, 22.8, "멕시코 피라미드는 꼭대기에 신전을 올려\n제사를 지내던 곳이었죠"),
    (22.9, 27.0, "다만 멕시코 팔렝케에선\n피라미드 속 왕의 무덤이\n발견되기도 했어요"),
    (27.4, 29.2, "셋째, 시대가 달라요"),
    (29.3, 34.4, "기자의 대피라미드는 약 4,500년 전,\n태양의 피라미드는\n약 1,800년 전에 지어졌어요"),
    (34.7, 38.5, "멕시코에선 옛 피라미드 위에\n새 층을 덧씌워 키우기도 했죠"),
    (38.6, 41.3, "그렇게 1,000년 넘게 쌓은 게\n촐룰라 피라미드예요"),
    (41.4, 44.9, "부피로는 이집트를 제치고\n세계에서 가장 큰 피라미드죠"),
    (45.0, 47.6, "지금은 언덕처럼 보여서\n꼭대기엔 교회가 서 있어요"),
    (48.0, 50.4, "그런데 왜 둘 다 피라미드였을까요?"),
    (50.5, 55.5, "돌과 흙으로 높이 쌓으려면\n아래가 넓고 위가 좁은 모양이\n가장 튼튼하다는 설명이 많아요"),
    (55.9, 58.8, "더 많은 미스터리가 궁금하다면\n구독해 주세요"),
]

IDLE = set()
DURATION = 61


def build():
    with open(os.path.join(ROOT, "manifest_scenes.json")) as f:
        scenes = json.load(f)
    for sc in scenes:
        for p in sc["parts"]:
            if (sc["id"], p["name"]) in IDLE:
                p["idle"] = "bob"
    for a, b in zip(scenes, scenes[1:]):
        assert a["end"] == b["start"], (a["id"], b["id"])
    assert scenes[-1]["end"] == DURATION
    for (s, e, _), nxt in zip(CUES, CUES[1:] + [(DURATION, 0, "")]):
        assert s < e <= nxt[0], (s, e)
    data = {"duration": DURATION, "fps": 30, "width": 1080, "height": 1920,
            "scenes": scenes, "cues": [{"start": s, "end": e, "text": t} for s, e, t in CUES]}
    with open(os.path.join(ROOT, "manifest.json"), "w") as f:
        json.dump(data, f, ensure_ascii=False, indent=1)
    return data


if __name__ == "__main__":
    d = build()
    print(len(d["scenes"]), "scenes,", len(d["cues"]), "cues")
