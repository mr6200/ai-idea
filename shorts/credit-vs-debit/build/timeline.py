"""Full 60 s timeline (thumbnail intro added at render): scene part animations from gen_scenes.py plus subtitle cues."""
import json
import os

ROOT = os.path.dirname(os.path.abspath(__file__))

# (start, end, text) in comp seconds; "\n" splits lines
CUES = [
    (0.1, 2.0, "체크카드만 쓰면\n무조건 이득일까요?"),
    (2.1, 4.4, "아껴 쓰기엔 좋지만,\n놓치는 게 있어요"),
    (4.7, 7.1, "신용점수는 빌린 돈을\n잘 갚았는지를 봐요"),
    (7.2, 10.4, "신용카드는 먼저 쓰고\n다음 달에 갚는 작은 빚이에요"),
    (10.8, 13.6, "그래서 제때 갚은 기록이\n믿을 만하다는 증거가 돼요"),
    (13.7, 16.9, "체크카드도 점수에 반영되지만,\n갚은 기록은 남지 않아요"),
    (17.2, 20.1, "할인이나 포인트 적립도\n대체로 신용카드가 더 커요"),
    (20.5, 23.0, "그런데 체크카드에도\n반가운 소식이 있어요"),
    (23.1, 27.1, "이번 가을부터 대출 이자를\n깎아 주는 카드 실적에\n체크카드도 들어가요"),
    (27.4, 29.6, "단, 신용카드에도\n함정이 있어요"),
    (29.9, 32.9, "퀴즈! 신용카드를 쓸 때\n가장 피해야 할 습관은?"),
    (33.8, 35.6, "정답은, 리볼빙이에요!"),
    (35.7, 39.6, "남은 카드값이 다음 달로 넘어가\n연 17%쯤 이자가 붙거든요"),
    (39.9, 43.3, "신용카드 한 장, 조금만 쓰고\n매달 다 갚는 게 정답이에요"),
    (43.4, 46.0, "더 많은 돈 이야기가 궁금하다면\n구독해 주세요"),
]

IDLE = set()
DURATION = 49  # ends about 2.5 s after the last line (60 s is the maximum)


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
