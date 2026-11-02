"""Full 60 s timeline (thumbnail intro added at render): scene part animations from gen_scenes.py plus subtitle cues."""
import json
import os

ROOT = os.path.dirname(os.path.abspath(__file__))

# (start, end, text) in comp seconds; "\n" splits lines
CUES = [
    (0.1, 2.7, "첫 월급, 받자마자\n뭐부터 해야 할까요?"),
    (2.8, 4.0, "딱 세 가지만 기억하세요"),
    (4.2, 6.6, "첫째, 비상금 통장부터 만드세요"),
    (6.8, 9.2, "생활비 3에서 6개월 치를\n따로 모아 두는 거예요"),
    (9.4, 11.6, "언제든 꺼낼 수 있는\n파킹통장에 두면 좋아요"),
    (11.8, 15.0, "둘째, 저축은 월급날\n자동이체로 먼저 하세요"),
    (15.2, 17.2, "쓰고 남은 돈을 모으면\n남는 돈이 없거든요"),
    (17.4, 19.4, "셋째, 카드는 나눠서 쓰세요"),
    (19.6, 23.4, "연말정산에서 카드 공제는\n총급여의 25%를 넘게\n쓴 부분부터예요"),
    (23.6, 26.8, "그다음부터는 공제율이 두 배인\n체크카드가 유리하죠"),
    (27.0, 30.6, "퀴즈! 총급여가 3천만 원이면\n얼마부터 카드 공제가 시작될까?"),
    (31.4, 33.2, "정답은, 750만 원이에요!"),
    (33.4, 36.2, "3천만 원의 25%를\n넘게 쓴 돈부터예요"),
    (36.6, 39.6, "첫 월급부터 습관을 만들면\n돈이 쌓이기 시작해요"),
    (40.0, 42.4, "더 많은 돈 이야기가 궁금하다면\n구독해 주세요"),
]

IDLE = set()
DURATION = 45  # ends about 2.5 s after the last line (60 s is the maximum)


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
