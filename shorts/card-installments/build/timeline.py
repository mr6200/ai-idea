"""Full 90 s timeline: scene part animations from gen_scenes.py plus subtitle cues."""
import json
import os

ROOT = os.path.dirname(os.path.abspath(__file__))

# (start, end, text) in comp seconds; "\n" splits lines
CUES = [
    (0.1, 2.6, "무이자 할부,\n카드사는 손해일까요?"),
    (2.6, 4.8, "이자도 안 받는데\n왜 해줄까요?"),
    (5.0, 8.4, "120만 원을\n3개월 무이자로 사면"),
    (8.4, 11.8, "매달 40만 원,\n이자는 0원이에요"),
    (12.0, 15.6, "그런데 가게는 며칠 뒤\n120만 원을 다 받아요"),
    (15.6, 18.8, "카드사가 먼저\n돈을 내주는 거죠"),
    (19.0, 22.4, "3개월 동안 빌려준 돈의 이자는"),
    (22.4, 25.8, "카드사가 대신 떠안아요.\n일부는 가게가 나눠 내고요"),
    (26.0, 29.4, "그래도 해주는 이유는\n미끼이기 때문이에요"),
    (29.4, 32.8, "무이자가 있으면\n그 카드를 더 많이 쓰게 되니까요"),
    (33.0, 36.4, "카드를 쓸 때마다\n가게는 수수료를 내요"),
    (36.4, 39.8, "이 가맹점 수수료가\n카드사의 기본 수입이에요"),
    (40.0, 43.6, "진짜 수익은 따로 있어요.\n이자가 붙는 할부"),
    (43.6, 47.8, "카드사 7곳이 지난해 할부 수수료로\n번 돈만 약 3조 6천억 원"),
    (48.0, 51.4, "리볼빙과 카드론도\n연 10%가 넘는 이자를 받아요"),
    (51.4, 54.8, "무이자로 들어와서,\n이자로 남는 거죠"),
    (55.0, 58.6, "그런데 금리가 오르자\n무이자 기간이 확 줄었어요"),
    (58.6, 62.8, "2022년 말엔 최장 12개월,\n요즘은 2~3개월이 대부분"),
    (63.0, 66.6, "카드사가 돈을 빌려 오는\n비용이 커졌기 때문이에요"),
    (66.6, 69.8, "무이자는 결국\n카드사의 마케팅 비용이에요"),
    (70.0, 73.6, "퀴즈! 300만 원을\n6개월 무이자로 사면 매달 얼마?"),
    (73.6, 76.4, "정답은 50만 원!"),
    (76.6, 79.8, "단, 무이자가 끝나면\n수수료가 붙는지 꼭 확인하세요"),
    (80.2, 84.6, "무이자는 공짜가 아니라\n카드사의 미끼예요"),
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
