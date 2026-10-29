"""Full 90 s timeline: scene part animations from gen_scenes.py plus subtitle cues."""
import json
import os

ROOT = os.path.dirname(os.path.abspath(__file__))

# (start, end, text) in comp seconds; "\n" splits lines
CUES = [
    (0.1, 2.6, "국민연금, 낸 돈보다\n더 받을 수 있을까?"),
    (2.6, 4.8, "기금이 바닥난다는데,\n손해 아닐까요?"),
    (5.0, 8.4, "올해부터 보험료율이\n오르기 시작했어요"),
    (8.4, 11.8, "해마다 조금씩 올라서\n2033년에는 13%가 돼요"),
    (12.0, 15.4, "대신 받는 돈의 비율인\n소득대체율은 43%로 올랐죠"),
    (15.4, 18.8, "더 내고 더 받는\n개혁이에요"),
    (19.0, 22.4, "그럼 받는 돈을\n낸 돈으로 나눠 볼까요?"),
    (22.4, 25.8, "이 비율을\n수익비라고 불러요"),
    (26.0, 29.4, "평균 소득자라면 개혁 뒤에도\n낸 돈의 약 1.6에서 2배"),
    (29.4, 32.8, "젊은 세대일수록\n조금 낮아지긴 해요"),
    (33.0, 36.8, "어떻게 더 줄 수 있을까요?\n첫째, 매년 물가만큼 올라요"),
    (36.8, 40.8, "올해도\n2.1% 올랐죠"),
    (41.0, 44.4, "둘째, 직장인은 보험료 절반을\n회사가 내 줘요"),
    (44.4, 47.8, "셋째, 소득이 적을수록\n더 많이 돌려받는 구조예요"),
    (48.0, 51.4, "그럼 기금이 바닥나면\n어떻게 될까요?"),
    (51.4, 54.8, "개혁으로 소진 시점은\n2064년쯤으로 늦춰졌어요"),
    (55.0, 58.4, "그리고 이제 법에, 국가가\n지급을 보장한다고 적혔어요"),
    (58.4, 61.8, "2026년 1월부터\n시행됐죠"),
    (62.0, 65.8, "정리하면, 낸 돈보다\n더 받는 구조예요"),
    (65.8, 69.8, "오랫동안 꾸준히 낼수록\n더 유리하고요"),
    (70.0, 73.6, "퀴즈! 국민연금 수령액은\n매년 무엇에 맞춰 오를까?"),
    (73.6, 76.6, "정답은 물가!"),
    (76.6, 79.8, "소비자물가 상승률만큼\n올라요"),
    (80.2, 84.6, "노후 준비의 첫걸음,\n국민연금부터 챙겨 보세요"),
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
