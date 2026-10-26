"""Full 90 s timeline: scene part animations from gen_scenes.py plus subtitle cues."""
import json
import os

ROOT = os.path.dirname(os.path.abspath(__file__))

# (start, end, text) in comp seconds; "\n" splits lines
CUES = [
    (0.1, 2.6, "비행기만 타면\n귀가 먹먹하죠?"),
    (2.6, 4.8, "범인은\n귀 속 공기예요"),
    (5.0, 8.4, "고막 안쪽에는 중이라는\n작은 공기 방이 있어요"),
    (8.4, 11.8, "평소엔 고막 안팎의\n기압이 같아요"),
    (12.0, 15.4, "그런데 비행기 안은\n땅보다 기압이 낮아요"),
    (15.4, 18.8, "높이 2,400m 산 위와\n비슷한 수준이에요"),
    (19.0, 22.4, "기압이 바뀌면\n고막 안팎의 압력이 달라져요"),
    (22.4, 25.8, "고막이 밀려 팽팽해지면\n소리가 먹먹해져요"),
    (26.0, 29.4, "해결사는 귀와 코 뒤를 잇는\n가는 통로, 이관이에요"),
    (29.4, 32.8, "이관은 평소엔\n닫혀 있어요"),
    (33.0, 36.8, "침을 꿀꺽 삼키거나 하품하면\n이관이 잠깐 열려요"),
    (36.8, 40.8, "공기가 드나들며\n뻥 하고 풀리죠"),
    (41.0, 44.4, "올라갈 땐 귀 속 공기가\n저절로 빠져나가요"),
    (44.4, 47.8, "그래서 이륙 때는\n비교적 괜찮아요"),
    (48.0, 51.4, "내려갈 땐 공기가\n귀 속으로 들어가야 하는데"),
    (51.4, 54.8, "이관이 잘 안 열려서\n착륙 때 더 아파요"),
    (55.0, 58.4, "그러니 착륙 전엔 침 삼키기,\n하품, 껌, 물 마시기"),
    (58.4, 61.8, "코를 막고 살살\n콧바람을 불어도 돼요"),
    (62.0, 65.8, "아기는 이관이 좁아서\n더 힘들어해요"),
    (65.8, 69.8, "이착륙 때 젖병이나\n쪽쪽이로 삼키게 해 주세요"),
    (70.0, 73.6, "퀴즈! 착륙 때 잠들어 있으면\n귀가 더 아플까?"),
    (73.6, 76.6, "정답은 O!\n더 아플 수 있어요"),
    (76.6, 79.8, "자는 동안엔 침을\n덜 삼키기 때문이에요"),
    (80.2, 84.6, "다음 비행 때 귀가 먹먹하면\n꿀꺽 삼켜 보세요"),
    (84.8, 89.8, "더 많은 지식이 궁금하다면\n구독해 주세요"),
]

IDLE = set()
DURATION = 90


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
