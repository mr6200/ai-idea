"""Full 90 s timeline: scene part animations from gen_scenes.py plus subtitle cues."""
import json
import os

ROOT = os.path.dirname(os.path.abspath(__file__))

# (start, end, text) in comp seconds; "\n" splits lines
CUES = [
    (0.1, 2.6, "은행은 어떻게\n돈을 벌까요?"),
    (2.6, 4.8, "내 예금에\n이자까지 주면서요"),
    (5.0, 7.8, "비밀은 금리 차이"),
    (7.8, 10.8, "예금은 3%에 받고,\n대출은 5%에 빌려줘요"),
    (11.0, 14.6, "1억 원을 맡기면\n은행이 주는 이자는 300만 원"),
    (14.6, 18.8, "그 돈을 빌려주고\n받는 이자는 500만 원"),
    (19.0, 21.6, "차이 200만 원이\n은행 몫"),
    (21.6, 24.8, "이걸 예대마진이라고 해요"),
    (25.0, 28.4, "그래서 은행은 예금을\n금고에 쌓아 두지 않아요"),
    (28.4, 31.8, "일부만 남기고,\n나머지는 빌려주죠"),
    (32.0, 35.8, "2025년 국내 은행이\n이자로 번 돈은 약 60조 원"),
    (35.8, 40.8, "수수료 같은 다른 수익은\n7조 6천억 원"),
    (41.0, 43.8, "10원을 벌면\n약 9원이 이자에서"),
    (43.8, 46.8, "은행은 결국\n이자 장사인 셈이에요"),
    (47.0, 50.6, "그럼 은행은\n무조건 남을까요?"),
    (50.6, 54.8, "빌려준 돈을 못 받으면\n그대로 손해예요"),
    (55.0, 58.4, "그래서 대출 전에\n신용과 담보를 꼼꼼히 보고"),
    (58.4, 61.8, "위험할수록\n금리를 높게 받아요"),
    (62.0, 65.4, "정리하면, 은행은\n돈을 싸게 빌려서"),
    (65.4, 69.8, "비싸게 빌려주는 가게예요"),
    (70.0, 73.6, "퀴즈! 예금 3%, 대출 6%,\n1억 원이면 은행 몫은?"),
    (73.6, 76.4, "정답은 300만 원!"),
    (76.6, 79.8, "금리 차이 3%가\n은행의 수입이죠"),
    (80.2, 84.6, "내 예금이 누군가의\n대출이 되는 거예요"),
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
