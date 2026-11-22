"""Full 62 s timeline: scene part animations from gen_scenes.py plus subtitle cues."""
import json
import os

ROOT = os.path.dirname(os.path.abspath(__file__))

# (start, end, text) in comp seconds; "\n" splits lines
CUES = [
    (0.1, 3.6, "피라미드보다 7,000년이나 앞서\n거대한 돌기둥을 세운 사람들이 있어요"),
    (3.7, 6.7, "농사도 짓기 전이었죠.\n튀르키예의 괴베클리 테페예요"),
    (7.0, 11.1, "1963년 조사단은 이 언덕을\n중세 무덤 터로 여기고 지나쳤어요"),
    (11.4, 16.4, "1994년, 독일 고고학자가\n그 돌이 T자 기둥이라는 걸 알아봤죠"),
    (16.7, 19.1, "파 보니 돌기둥들이\n원을 그리며 둘러서 있었어요"),
    (19.2, 23.0, "가운데 큰 기둥은 높이 5.5미터,\n무게는 10톤 가까이 돼요"),
    (23.3, 26.5, "기둥엔 여우와 멧돼지, 뱀 같은\n동물이 새겨져 있고"),
    (26.8, 30.3, "어떤 기둥엔 팔과 손까지 새겨져\n사람을 나타낸 것처럼 보여요"),
    (30.6, 34.6, "지어진 건 약 1만 1,600년 전,\n스톤헨지보다도 6,000년 넘게 앞서요"),
    (34.9, 39.1, "글자도, 바퀴도, 금속 도구도 없던\n사냥꾼과 채집민이 해낸 거예요"),
    (39.4, 40.8, "그럼 왜 지었을까요?"),
    (40.9, 44.4, "발굴자는 여러 무리가 모여\n잔치와 의식을 벌이던 신전이라고 봤어요"),
    (44.7, 47.8, "또 사람들을 먹이려다\n농사가 시작됐을지도 모른다고 했죠"),
    (48.1, 52.7, "하지만 최근엔 집과\n물 저장고 흔적도 나와\n사람들이 이곳에 살았다는 주장도 있어요"),
    (53.0, 56.1, "누가, 왜 지었는지는\n아직도 수수께끼예요"),
    (56.4, 59.3, "더 많은 미스터리가 궁금하다면\n구독해 주세요"),
]

IDLE = set()
DURATION = 62


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
