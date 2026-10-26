"""Full 90 s timeline: scene part animations from gen_scenes.py plus subtitle cues."""
import json
import os

ROOT = os.path.dirname(os.path.abspath(__file__))

# (start, end, text) in comp seconds; "\n" splits lines
CUES = [
    (0.1, 2.6, "예금 이자 100만 원,\n다 내 돈일까요?"),
    (2.6, 4.8, "아니요, 15만 4천 원은\n세금이에요"),
    (5.0, 8.0, "이자에는\n15.4% 세금이 붙어요"),
    (8.0, 10.8, "소득세 14%에,\n지방소득세 1.4%"),
    (11.0, 14.4, "은행이 이자를 줄 때\n미리 떼고 줘요"),
    (14.4, 17.8, "그래서 통장엔\n84만 6천 원이 들어와요"),
    (18.0, 21.4, "이자와 배당이\n1년에 2천만 원을 넘으면"),
    (21.4, 24.8, "다른 소득과 합쳐\n세금을 더 낼 수도 있어요"),
    (25.0, 27.8, "세금을 줄이는 방법은\n없을까요?"),
    (27.8, 30.8, "대표적인 두 가지가 있어요"),
    (31.0, 33.8, "첫째, ISA 계좌"),
    (33.8, 37.6, "이익 200만 원까지 세금이 없고,\n서민형은 400만 원"),
    (37.6, 40.8, "넘는 부분도\n9.9%만 내요"),
    (41.0, 43.8, "단, 3년은 유지해야 해요"),
    (43.8, 46.8, "중간에 깨면\n혜택이 사라져요"),
    (47.0, 50.6, "둘째, 농협, 신협, 새마을금고 같은\n상호금융"),
    (50.6, 54.8, "조합원이 되면\n3천만 원까지 세금이 1.4%"),
    (55.0, 58.6, "다만 2026년부터\n소득이 높은 준조합원은"),
    (58.6, 61.8, "세금이 조금씩 늘어요"),
    (62.0, 65.6, "정리하면,\n이자에는 15.4%"),
    (65.6, 69.8, "ISA와 상호금융으로\n세금을 줄일 수 있어요"),
    (70.0, 73.4, "퀴즈! 이자 50만 원,\n세금 떼면 얼마?"),
    (73.4, 76.4, "정답은 42만 3천 원!"),
    (76.6, 79.8, "7만 7천 원이 세금이죠"),
    (80.2, 84.6, "가입 전엔 상품설명서로\n세금 조건을 꼭 확인하세요"),
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
