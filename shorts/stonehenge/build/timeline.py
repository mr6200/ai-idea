"""Full 60 s timeline: scene part animations from gen_scenes.py plus subtitle cues."""
import json
import os

ROOT = os.path.dirname(os.path.abspath(__file__))

# (start, end, text) in comp seconds; "\n" splits lines
CUES = [
    (0.1, 3.2, "5,000년 전, 수십 톤짜리 돌을\n세워 만든 곳이 있어요"),
    (3.3, 6.6, "영국의 스톤헨지예요.\n그런데 이 돌들, 어디서 왔을까요?"),
    (6.9, 9.7, "놀랍게도 대부분\n이 근처에서 난 돌이 아니에요"),
    (10.0, 13.3, "바깥쪽의 큰 돌은 사르센석,\n하나가 20톤쯤 돼요"),
    (13.4, 17.2, "2020년 성분을 분석해 보니\n약 25km 북쪽 숲에서 왔어요"),
    (17.5, 19.8, "안쪽의 작은 블루스톤은\n더 멀리서 왔어요"),
    (20.1, 25.1, "200km 넘게 떨어진 웨일스의 산,\n돌을 떼어 낸 채석장 흔적도 찾았죠"),
    (25.4, 29.0, "하나에 약 3톤,\n썰매와 통나무로\n끌어왔다는 설명이 많아요"),
    (29.3, 32.3, "그리고 2024년,\n가장 큰 반전이 나왔어요"),
    (32.4, 34.6, "가운데 깔린\n6톤짜리 제단석이"),
    (34.9, 38.6, "700km 넘게 떨어진\n스코틀랜드 북동쪽 돌이었던 거예요"),
    (38.7, 41.4, "배로 옮겼는지, 땅으로 끌었는지는\n아직 몰라요"),
    (41.7, 43.8, "왜 이렇게 먼 데서\n돌을 가져왔을까요?"),
    (43.9, 47.2, "스톤헨지는 하짓날\n해 뜨는 방향에 맞춰 세워졌어요"),
    (47.5, 51.1, "멀리 사는 사람들이 각자 돌을 가져와\n하나로 뭉쳤다는 해석도 있어요"),
    (51.4, 54.5, "누가, 어떻게 옮겼는지는\n여전히 수수께끼예요"),
    (54.8, 57.2, "더 많은 미스터리가 궁금하다면\n구독해 주세요"),
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
