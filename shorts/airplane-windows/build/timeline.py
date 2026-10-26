"""Full 90 s timeline: scene part animations from gen_scenes.py plus subtitle cues."""
import json
import os

ROOT = os.path.dirname(os.path.abspath(__file__))

# (start, end, text) in comp seconds; "\n" splits lines
CUES = [
    (0.1, 2.6, "비행기 창문은\n왜 다 둥글까요?"),
    (2.6, 4.8, "네모면 안 되는\n이유가 있어요"),
    (5.0, 8.4, "높은 하늘은\n공기가 아주 희박해요"),
    (8.4, 11.8, "그래서 기내에 공기를 채우면\n풍선처럼 안에서 밀어요"),
    (12.0, 15.4, "이륙하면 동체가 살짝 부풀고,\n착륙하면 줄어들어요"),
    (15.4, 18.8, "이게 비행할 때마다\n반복되죠"),
    (19.0, 22.4, "그런데 구멍이 네모나면,\n힘이 어디로 갈까요?"),
    (22.4, 25.8, "각진 모서리로\n힘이 몰려요"),
    (26.0, 29.4, "종이를 접었다 폈다 하면\n결국 찢어지죠"),
    (29.4, 32.8, "금속도 힘을 계속 받으면\n금이 가요. 금속 피로예요"),
    (33.0, 36.8, "1954년, 세계 첫 제트 여객기\n코멧이 하늘에서 부서졌어요"),
    (36.8, 40.8, "석 달 사이에\n두 대나요"),
    (41.0, 44.4, "조사팀은 동체를\n통째로 물탱크에 넣고"),
    (44.4, 47.8, "압력을 넣었다 뺐다\n수천 번 반복했어요"),
    (48.0, 51.4, "결국 각진 구멍 모서리에서\n금이 시작됐어요"),
    (51.4, 54.8, "그 뒤로 비행기 구멍의\n모서리는 둥글어졌죠"),
    (55.0, 58.4, "둥근 모서리는 힘을\n고르게 나눠 받아요"),
    (58.4, 61.8, "그래서 창문도\n둥글게 만드는 거예요"),
    (62.0, 65.8, "네모난 창문은\n모서리에 힘이 몰리고"),
    (65.8, 69.8, "둥근 창문은\n힘을 고르게 나눠요"),
    (70.0, 73.6, "퀴즈! 창문 아래\n작은 구멍의 정체는?"),
    (73.6, 76.6, "정답은 숨구멍!"),
    (76.6, 79.8, "유리 사이 압력을 맞춰\n바깥 유리가 힘을 받게 해요"),
    (80.2, 84.6, "다음에 비행기 타면\n창문 모서리를 봐 주세요"),
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
