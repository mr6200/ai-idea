"""Full 60 s timeline (thumbnail intro added at render): scene part animations from gen_scenes.py plus subtitle cues."""
import json
import os

ROOT = os.path.dirname(os.path.abspath(__file__))

# (start, end, text) in comp seconds; "\n" splits lines
CUES = [
    (0.1, 1.8, "연말정산은 1월에\n하는 거 아니에요?"),
    (1.9, 4.3, "사실 승부는\n12월 31일에 끝나요"),
    (4.4, 6.5, "1월엔 이미 쓴 돈을\n정리만 하거든요"),
    (6.8, 9.3, "첫째, 홈택스\n연말정산 미리보기"),
    (9.4, 12.1, "9월까지 쓴 카드값으로\n예상 환급액을 보여 줘요"),
    (12.2, 14.4, "토해낼 것 같으면\n아직 손쓸 시간이 있죠"),
    (14.8, 19.9, "둘째, 연금저축과 IRP는\n12월 31일까지 넣은 돈만\n올해 공제예요"),
    (20.0, 23.3, "합쳐서 900만 원까지,\n최대 16.5%를 돌려받아요"),
    (23.6, 25.5, "셋째, 고향사랑기부제"),
    (25.6, 28.3, "10만 원을 내면 10만 원을\n세금으로 돌려받고"),
    (28.4, 30.5, "3만 원어치\n답례품까지 받아요"),
    (30.8, 34.0, "단, 내야 할 세금이 있어야\n돌려받을 수 있어요"),
    (34.4, 38.3, "퀴즈! 고향사랑기부로\n10만 원을 내고 다 돌려받으면\n실제 부담은?"),
    (39.1, 41.6, "정답은, 부담 0원이에요!"),
    (41.7, 43.6, "오히려 답례품만큼\n이득이죠"),
    (43.9, 47.0, "올해 남은 공제,\n12월 31일이 마감이에요"),
    (47.1, 50.0, "더 많은 돈 이야기가 궁금하다면\n구독해 주세요"),
]

IDLE = set()
DURATION = 53  # ends about 2.5 s after the last line (60 s is the maximum)


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
