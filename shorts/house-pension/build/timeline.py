"""Full 90 s timeline: scene part animations from gen_scenes.py plus subtitle cues."""
import json
import os

ROOT = os.path.dirname(os.path.abspath(__file__))

# (start, end, text) in comp seconds; "\n" splits lines
CUES = [
    (0.1, 2.6, "집은 있는데\n현금이 없다면?"),
    (2.6, 4.8, "집으로 월급을\n받는 방법이 있어요"),
    (5.0, 8.4, "바로 주택연금.\n집을 담보로 매달 연금을 받아요"),
    (8.4, 11.8, "그러면서 그 집에\n계속 살 수 있죠"),
    (12.0, 15.4, "가입 조건은 부부 중 한 명이\n만 55세 이상"),
    (15.4, 18.8, "집값은 공시가격\n12억 원 이하예요"),
    (19.0, 22.4, "그럼 얼마나 받을까요?\n72세, 4억 원 집이라면"),
    (22.4, 25.8, "매달 약 133만 원을\n평생 받아요"),
    (26.0, 29.4, "나이가 많을수록,\n집값이 비쌀수록 더 받아요"),
    (29.4, 32.8, "올해 3월부터는\n평균 3% 넘게 올랐죠"),
    (33.0, 36.8, "장점은? 부부 중 한 명이\n먼저 떠나도"),
    (36.8, 40.8, "남은 배우자가 같은 금액을\n계속 받아요"),
    (41.0, 44.4, "집값이 떨어져도\n연금은 그대로"),
    (44.4, 47.8, "나라가 지급을\n책임지거든요"),
    (48.0, 51.4, "나중에 집을 팔아 정산할 때\n돈이 남으면 자녀에게"),
    (51.4, 54.8, "모자라도 자녀에게\n청구하지 않아요"),
    (55.0, 58.4, "하지만 단점도 있어요.\n받은 연금에 이자가 붙어서"),
    (58.4, 61.8, "집을 물려주기는\n어려워질 수 있죠"),
    (62.0, 65.8, "집값이 올라도\n연금은 늘지 않고"),
    (65.8, 69.8, "중간에 그만두면\n받은 돈과 이자를 갚아야 해요"),
    (70.0, 73.6, "퀴즈! 해지하고 같은 집으로\n바로 다시 가입할 수 있을까?"),
    (73.6, 76.6, "정답은 X!"),
    (76.6, 79.8, "같은 집으로는\n3년 동안 다시 못 해요"),
    (80.2, 84.6, "집 한 채가 노후 월급이 되는\n주택연금, 꼼꼼히 따져 보세요"),
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
