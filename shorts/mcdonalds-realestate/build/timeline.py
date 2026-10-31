"""Full 60 s timeline (thumbnail intro added at render): scene part animations from gen_scenes.py plus subtitle cues."""
import json
import os

ROOT = os.path.dirname(os.path.abspath(__file__))

# (start, end, text) in comp seconds; "\n" splits lines
CUES = [
    (0.1, 3.5, "맥도날드는 햄버거로\n돈을 가장 많이 벌까요?"),
    (3.6, 4.8, "놀랍게도\n아니에요"),
    (5.0, 7.4, "맥도날드 매장 대부분은\n가맹점이에요"),
    (7.6, 10.2, "본사는 가맹점에서\n로열티와 임대료를 받죠"),
    (10.4, 12.8, "그런데 그중 더 큰 건\n로열티가 아니라 임대료예요"),
    (13.0, 16.6, "2024년 임대료만 약 100억 달러,\n로열티보다 두 배 가까이 많죠"),
    (16.8, 20.0, "비결은 1950년대,\n한 재무 담당자의 아이디어였어요"),
    (20.2, 24.4, "본사가 매장 땅을 사거나 빌린 뒤\n점주에게 더 비싸게 빌려주는 거죠"),
    (24.6, 26.8, "점주는 매출의 일정 비율을\n임대료로 내요"),
    (27.0, 30.4, "햄버거가 잘 팔릴수록\n본사 임대료도 오르는 구조예요"),
    (30.8, 32.6, "영화 「파운더」를 보면\n이런 대사가 나와요"),
    (32.8, 36.0, "우리는 햄버거가 아니라\n부동산 사업을 하는 겁니다"),
    (36.8, 40.0, "퀴즈! 맥도날드 본사가\n직접 운영하는 매장은 몇 %일까?"),
    (41.0, 43.0, "정답은, 약 5%예요!"),
    (43.2, 45.6, "나머지 95%는\n모두 가맹점이랍니다"),
    (46.6, 50.2, "다음에 맥도날드를 보면,\n그 땅 주인을 떠올려 보세요"),
    (50.6, 53.4, "더 많은 돈 이야기가 궁금하다면\n구독해 주세요"),
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
