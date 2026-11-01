"""Full 60 s timeline (thumbnail intro added at render): scene part animations from gen_scenes.py plus subtitle cues."""
import json
import os

ROOT = os.path.dirname(os.path.abspath(__file__))

# (start, end, text) in comp seconds; "\n" splits lines
CUES = [
    (0.1, 3.4, "연말정산 때 최대 148만 원을\n돌려받는 통장이 있다면?"),
    (3.5, 4.6, "바로 연금저축이에요"),
    (4.8, 8.6, "연금저축은 한 해 600만 원,\nIRP와 합치면 900만 원까지"),
    (8.8, 12.8, "넣은 돈의 13.2%나 16.5%를\n세금에서 깎아 줘요"),
    (13.0, 17.4, "연봉 5,500만 원 이하라면 16.5%,\n그보다 많으면 13.2%예요"),
    (17.6, 21.0, "월 50만 원씩 600만 원을 넣으면\n최대 99만 원을 돌려받아요"),
    (21.2, 24.0, "세금을 내는 직장인이나\n자영업자에게 특히 유리해요"),
    (24.2, 26.6, "노후까지 오래 묶어 둘 수 있다면\n더 좋고요"),
    (26.8, 30.6, "하지만 55세 전에 깨면\n기타소득세 16.5%를 내야 해요"),
    (30.8, 32.9, "돌려받은 세금보다\n더 낼 수도 있어요"),
    (33.0, 34.9, "낸 세금이 없다면\n돌려받을 것도 없고요"),
    (35.2, 38.8, "퀴즈! 55세 이후 연금으로 받으면\n세금은 얼마일까?"),
    (39.6, 42.6, "정답은, 3.3에서 5.5%예요!"),
    (42.8, 44.8, "나이가 많을수록\n세율이 낮아져요"),
    (45.2, 47.6, "내 소득과 계획에 맞는지\n먼저 따져 보세요"),
    (48.0, 50.6, "더 많은 돈 이야기가 궁금하다면\n구독해 주세요"),
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
