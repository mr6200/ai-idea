"""Full 57 s timeline: scene part animations from gen_scenes.py plus subtitle cues."""
import json
import os

ROOT = os.path.dirname(os.path.abspath(__file__))

# (start, end, text) in comp seconds; "\n" splits lines
CUES = [
    (0.1, 3.4, "사막 바닥에 그려진 거대한 그림,\n그런데 땅에서는 알아보기 어려워요"),
    (3.5, 5.9, "높은 곳에 올라가야\n비로소 모양이 드러나죠"),
    (6.3, 8.6, "페루 남부 사막의\n나스카 라인이에요"),
    (8.7, 11.4, "약 2,000년 전 나스카 사람들이\n그린 것으로 보여요"),
    (11.5, 15.2, "원숭이 그림은 길이 93미터,\n콘도르는 130미터가 넘어요"),
    (15.6, 17.5, "그리는 방법은\n의외로 간단했어요"),
    (17.6, 20.7, "땅을 덮은 붉은 돌을 걷어 내\n밝은 흙을 드러낸 거죠"),
    (20.8, 23.4, "비가 거의 오지 않는 사막이라\n지금까지 남아 있어요"),
    (23.8, 27.8, "그림이 널리 알려진 건 1930년대,\n비행기가 그 위를 날면서부터예요"),
    (28.2, 32.7, "그리고 2024년, 일본 연구팀이\nAI로 항공 사진을 분석했더니"),
    (32.8, 35.4, "6개월 만에\n새 그림 303개를 찾아냈어요"),
    (35.5, 39.0, "알려진 그림이 430개에서\n733개로 늘어난 거죠"),
    (39.1, 42.6, "새로 찾은 그림은 대부분 작고,\n옛 오솔길 옆에 있었어요"),
    (43.0, 44.2, "그런데 왜 그렸을까요?"),
    (44.3, 47.1, "별을 보는 달력이라는 설은\n지금은 의심받고 있고"),
    (47.2, 49.7, "물과 풍요를 비는\n의식의 길이었다는 설명이 많아요"),
    (50.1, 52.1, "정답은 아직\n사막 위에 숨어 있어요"),
    (52.2, 54.7, "더 많은 미스터리가 궁금하다면\n구독해 주세요"),
]

IDLE = set()
DURATION = 57


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
