"""Full 60 s timeline (thumbnail intro added at render): scene part animations from gen_scenes.py plus subtitle cues."""
import json
import os

ROOT = os.path.dirname(os.path.abspath(__file__))

# (start, end, text) in comp seconds; "\n" splits lines
CUES = [
    (0.1, 2.7, "로또 1등에 당첨되면\n결국 다 망한다?"),
    (2.8, 4.2, "정말 그럴까요?"),
    (4.4, 8.6, "1등 확률은 814만분의 1,\n평균 당첨금은 약 20억 원"),
    (8.8, 11.8, "세금을 떼면\n약 13억 7천만 원을 받아요"),
    (12.0, 15.4, "당첨자 70%가 파산한다는 말,\n들어 보셨죠?"),
    (15.6, 17.8, "그런데 이 숫자는\n근거가 없어요"),
    (18.0, 21.8, "출처로 알려진 미국 재단이\n자기 연구가 아니라고 밝혔거든요"),
    (22.0, 24.8, "스웨덴 연구에선\n큰돈에 당첨된 사람들이"),
    (25.0, 27.8, "10년이 넘게 지나도\n삶의 만족도가 더 높았어요"),
    (28.0, 31.0, "반대로 미국 플로리다에선\n1억 원 안팎을 받은 사람들이"),
    (31.2, 33.8, "파산을 막지 못하고\n몇 년 미뤘을 뿐이었죠"),
    (34.0, 36.8, "결국 돈의 크기보다\n쓰는 방법이 중요한 거예요"),
    (37.0, 41.6, "우리나라 1등 당첨자는\n35%가 집부터 사겠다고 답했어요"),
    (42.0, 45.4, "퀴즈! 로또 1등 당첨금,\n언제까지 찾아가야 할까?"),
    (46.4, 48.6, "정답은, 1년이에요!"),
    (48.8, 51.4, "기한이 지나면\n복권기금으로 넘어가요"),
    (53.4, 56.4, "더 많은 돈 이야기가 궁금하다면\n구독해 주세요"),
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
