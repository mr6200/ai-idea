"""Full 60 s timeline (thumbnail intro added at render): scene part animations from gen_scenes.py plus subtitle cues."""
import json
import os

ROOT = os.path.dirname(os.path.abspath(__file__))

# (start, end, text) in comp seconds; "\n" splits lines
CUES = [
    (0.1, 2.7, "월급날 들어온 돈,\n3일 만에 텅 빈 적 있나요?"),
    (2.8, 3.9, "단순히 기분 탓이 아니에요"),
    (4.0, 6.6, "월급이 들어오자마자\n빠져나갈 돈들이 줄을 서 있거든요"),
    (6.8, 10.4, "월세와 관리비, 대출 이자,\n보험료와 통신비까지"),
    (10.6, 14.2, "자동이체가 월급날 바로 뒤에\n몰려 있는 경우가 많죠"),
    (14.4, 16.8, "그리고 가장 큰 건 카드값이에요"),
    (17.0, 19.4, "이번 달 월급으로\n지난달 쓴 돈을 메우는 셈이죠"),
    (19.6, 23.6, "실제로 우리나라 가구는\n쓸 수 있는 돈의 약 69%를 소비해요"),
    (23.8, 25.4, "그럼 어떻게 해야 할까요?"),
    (25.6, 28.0, "월급날, 저축할 돈부터\n먼저 떼어 놓으세요"),
    (28.2, 30.8, "통장을 생활비와\n고정 지출로 나누면\n돈의 흐름이 보여요"),
    (31.0, 34.6, "퀴즈! 카드 결제일이 14일이면\n언제 쓴 돈이 청구될까?"),
    (35.4, 37.6, "정답은, 지난달 1일부터 말일까지!"),
    (37.8, 40.6, "카드사마다 조금 다르니\n앱에서 꼭 확인해 보세요"),
    (41.0, 42.8, "다음 월급은\n사흘보다 오래 버텨 봐요"),
    (43.2, 45.6, "더 많은 돈 이야기가 궁금하다면\n구독해 주세요"),
]

IDLE = set()
DURATION = 48  # ends about 2.5 s after the last line (60 s is the maximum)


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
