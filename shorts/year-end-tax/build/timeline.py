"""Full 60 s timeline (thumbnail intro added at render): scene part animations from gen_scenes.py plus subtitle cues."""
import json
import os

ROOT = os.path.dirname(os.path.abspath(__file__))

# (start, end, text) in comp seconds; "\n" splits lines
CUES = [
    (0.1, 1.8, "연말정산은 1월에\n하는 거 아니에요?"),
    (1.9, 4.3, "사실 승부는\n12월 31일에 끝나요"),
    (4.4, 6.5, "1월엔 이미 쓴 돈을\n정리만 하거든요"),
    (6.8, 10.4, "첫째, 12월 18일까지 열리는\n홈택스 연말정산 미리보기"),
    (10.5, 13.3, "9월까지 쓴 카드값으로\n예상 환급액을 보여 줘요"),
    (13.4, 15.6, "토해낼 것 같으면\n아직 손쓸 시간이 있죠"),
    (15.9, 21.1, "둘째, 연금저축과 IRP는\n12월 31일까지 넣은 돈만\n올해 공제예요"),
    (21.2, 24.5, "합쳐서 900만 원까지,\n최대 16.5%를 돌려받아요"),
    (24.8, 26.7, "셋째, 고향사랑기부제"),
    (26.8, 29.5, "10만 원을 내면 10만 원을\n세금으로 돌려받고"),
    (29.6, 31.7, "3만 원어치\n답례품까지 받아요"),
    (32.0, 35.2, "단, 내야 할 세금이 있어야\n돌려받을 수 있어요"),
    (35.5, 39.4, "퀴즈! 고향사랑기부로\n10만 원을 내고 다 돌려받으면\n실제 부담은?"),
    (40.3, 42.7, "정답은, 부담 0원이에요!"),
    (42.8, 44.7, "오히려 답례품만큼\n이득이죠"),
    (45.1, 48.2, "연금저축 입금과 기부는\n12월 31일이 마감이에요"),
    (48.3, 51.2, "더 많은 돈 이야기가 궁금하다면\n구독해 주세요"),
]

IDLE = set()
DURATION = 54  # ends about 2.5 s after the last line (60 s is the maximum)


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
