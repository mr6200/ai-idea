"""Full 60 s timeline: scene part animations from gen_scenes.py plus subtitle cues."""
import json
import os

ROOT = os.path.dirname(os.path.abspath(__file__))

# (start, end, text) in comp seconds; "\n" splits lines
CUES = [
    (0.1, 3.4, "1518년 여름, 한 여성이\n거리에서 춤을 추기 시작했어요"),
    (3.5, 5.7, "그런데 며칠이 지나도\n멈추지 못했죠"),
    (6.1, 9.5, "프랑스 스트라스부르,\n당시엔 신성 로마 제국의 도시였어요"),
    (9.6, 12.1, "며칠 만에 30명이 넘게\n따라 추기 시작했고"),
    (12.2, 15.1, "8월엔 50명에서 400명까지\n늘었다는 기록이 있어요"),
    (15.5, 17.5, "시 의회의 대처는\n더 놀라웠어요"),
    (17.6, 20.3, "의사들은 실컷 춤을 춰서\n털어 내야 한다고 했고"),
    (20.4, 22.8, "의회는 회관을 내주고\n악사까지 불러 줬죠"),
    (22.9, 25.7, "하지만 오히려 더 늘자,\n결국 춤을 금지했어요"),
    (26.1, 30.1, "9월, 사람들을 성인의 성지로 보내\n기도하게 하자 잦아들었다고 해요"),
    (30.2, 32.7, "죽은 사람이 있었는지는\n지금도 논쟁 중이에요"),
    (33.1, 34.6, "그럼 원인은 뭐였을까요?"),
    (34.7, 38.4, "곡물 곰팡이 중독설은\n며칠씩 춤출 수 없다는 반론이 많고"),
    (38.5, 42.4, "굶주림과 병에 지친 사람들의\n집단 심리 현상이라는 설명이\n많이 꼽혀요"),
    (42.8, 45.8, "비슷한 춤 전염병은\n중세 유럽에 여러 번 있었어요"),
    (45.9, 50.5, "1374년 아헨에서 시작된 춤은\n쾰른과 스트라스부르까지 번졌고"),
    (50.6, 55.1, "1278년엔 다리 위에서 춤추던\n약 200명 때문에 다리가\n무너졌다는 기록도 있죠"),
    (55.5, 57.9, "더 많은 미스터리가 궁금하다면\n구독해 주세요"),
]

IDLE = set()
DURATION = 60


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
