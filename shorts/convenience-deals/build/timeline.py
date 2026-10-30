"""Full 60 s timeline (thumbnail intro added at render): scene part animations from gen_scenes.py plus subtitle cues."""
import json
import os

ROOT = os.path.dirname(os.path.abspath(__file__))

# (start, end, text) in comp seconds; "\n" splits lines
CUES = [
    (0.1, 3.0, "편의점 1+1,\n무조건 이득일까요?"),
    (3.0, 4.4, "계산해 보면\n생각과 달라요"),
    (4.6, 8.2, "1+1은 한 개 값에 두 개,\n반값에 사는 셈이죠"),
    (8.2, 11.2, "그런데 편의점 정가는\n대형마트보다 비싼 편이에요"),
    (11.2, 15.0, "같은 상품 10개를 사 보니\n편의점이 약 37% 더 비쌌죠"),
    (15.0, 18.4, "그래서 1+1이라도\n마트보다 크게 싸지 않을 수 있어요"),
    (18.6, 22.0, "2+1은 더 조심해야 해요,\n세 개를 다 사야 할인이거든요"),
    (22.0, 23.9, "하나만 필요했다면\n두 배를 쓴 셈이죠"),
    (24.0, 26.4, "그래도 끌리는 건\n공짜의 힘 때문이에요"),
    (26.4, 29.4, "미국 실험에서 초콜릿 값을\n1센트 내려 공짜로 만들자"),
    (29.4, 32.6, "더 좋은 초콜릿 대신\n공짜를 고른 사람이 크게 늘었어요"),
    (32.8, 38.6, "참기름 값을 4,750원에서\n9,500원으로 올리고\n1+1을 한 마트도 있었죠"),
    (38.6, 41.1, "공정거래위원회가\n대형마트 4곳에 과징금을 매겼죠"),
    (41.2, 44.4, "퀴즈! 2+1으로 사면\n한 개에 몇 % 할인일까?"),
    (45.2, 47.6, "정답은, 약 33%예요!"),
    (47.8, 50.2, "세 개를\n두 개 값에 사니까요"),
    (50.6, 53.2, "필요한 만큼만,\n한 개 가격을 따져 보세요"),
    (53.6, 56.6, "더 많은 돈 이야기가 궁금하다면\n구독해 주세요"),
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
