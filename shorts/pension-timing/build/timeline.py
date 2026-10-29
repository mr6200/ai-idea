"""Full 90 s timeline: scene part animations from gen_scenes.py plus subtitle cues."""
import json
import os

ROOT = os.path.dirname(os.path.abspath(__file__))

# (start, end, text) in comp seconds; "\n" splits lines
CUES = [
    (0.1, 2.6, "국민연금, 일찍 받을까\n늦게 받을까?"),
    (2.6, 4.8, "답은 몇 살까지\n사느냐에 달렸어요"),
    (5.0, 8.4, "1969년생부터 국민연금은\n65세에 받아요"),
    (8.4, 11.8, "하지만 60세로 당기거나\n70세까지 늦출 수도 있죠"),
    (12.0, 15.4, "당겨 받으면 1년에 6%씩,\n5년이면 30%가 깎이고"),
    (15.4, 18.8, "늦춰 받으면 1년에 7.2%씩,\n5년이면 36%가 늘어요"),
    (19.0, 22.4, "월 100만 원이라면\n60세부터는 70만 원"),
    (22.4, 25.8, "65세부터는 100만 원,\n70세부터는 136만 원이에요"),
    (26.0, 29.4, "그럼 받은 돈을\n다 더해 볼까요?"),
    (29.4, 32.8, "물가나 이자는 빼고\n단순하게 계산해요"),
    (33.0, 36.8, "일찍 받으면 처음엔\n5년 먼저 받아 앞서지만"),
    (36.8, 40.8, "약 77세가 되면\n65세부터 받은 사람에게 역전돼요"),
    (41.0, 44.4, "늦게 받으면\n기다린 5년만큼 뒤처지다가"),
    (44.4, 47.8, "약 84세부터\n앞서기 시작해요"),
    (48.0, 51.4, "65세 한국인은 평균\n21.7년을 더 살아요"),
    (51.4, 54.8, "약 87세까지니까, 평균만 보면\n늦게 받는 쪽이 유리하죠"),
    (55.0, 58.4, "하지만 건강이 걱정되거나\n당장 생활비가 급하다면"),
    (58.4, 61.8, "일찍 받는 게\n나을 수도 있어요"),
    (62.0, 65.8, "주의할 점! 연금 같은 소득이\n1년에 2,000만 원을 넘으면"),
    (65.8, 69.8, "건강보험 피부양자에서 빠져\n건보료를 내야 할 수 있어요"),
    (70.0, 73.6, "퀴즈! 당겨 받아 깎인 연금,\n65세가 지나면 원래대로 돌아올까?"),
    (73.6, 76.6, "정답은 X!"),
    (76.6, 79.8, "한 번 깎인 금액은\n평생 그대로예요"),
    (80.2, 84.6, "내 건강과 생활비를 따져\n받는 나이를 골라 보세요"),
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
