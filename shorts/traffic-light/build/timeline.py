"""Full 90 s timeline: scene part animations from gen_scenes.py plus subtitle cues."""
import json
import os

ROOT = os.path.dirname(os.path.abspath(__file__))

# (start, end, text) in comp seconds; "\n" splits lines
CUES = [
    (0.1, 2.6, "신호등은 왜\n빨강, 노랑, 초록일까요?"),
    (2.6, 4.8, "시작은\n기차였어요"),
    (5.0, 8.4, "1868년 영국 런던 국회의사당 앞,\n세계 첫 신호등이 섰어요"),
    (8.4, 11.8, "철도 신호를 본뜬 팔이 있었고,\n밤엔 가스등을 켰죠"),
    (12.0, 15.4, "경찰관이 손으로 움직였는데,\n한 달도 안 돼서"),
    (15.4, 18.8, "새어 나온 가스가 폭발했어요.\n경찰관이 다쳤죠"),
    (19.0, 22.4, "그 색은 철도에서 왔어요.\n초기 기차 신호는"),
    (22.4, 25.8, "빨강은 멈춤,\n흰색은 출발이었어요"),
    (26.0, 29.4, "그런데 흰빛은 밤에\n별빛이나 가로등과 헷갈렸고"),
    (29.4, 32.8, "빨간 유리가 빠지면\n흰빛으로 보여 위험했죠"),
    (33.0, 36.8, "그래서 출발은 초록,\n주의 신호는 노랑으로 바뀌었어요"),
    (36.8, 40.8, "빨강은 피와 불처럼\n오래전부터 위험의 색이었고요"),
    (41.0, 44.4, "흔히 빨강이 안개를\n잘 뚫는다고 하지만"),
    (44.4, 47.8, "사실 안개는 모든 색을\n비슷하게 흩어요"),
    (48.0, 51.4, "1914년 미국 클리블랜드에\n첫 전기 신호등이 생겼는데"),
    (51.4, 54.8, "빨강과 초록,\n두 색뿐이었어요"),
    (55.0, 58.4, "1920년 디트로이트의 경찰관\n윌리엄 포츠가"),
    (58.4, 61.8, "노란색을 더한\n세 가지 색깔의 신호등을 만들었죠"),
    (62.0, 65.8, "요즘 초록불은 살짝\n푸른빛을 띠기도 해요"),
    (65.8, 69.8, "색깔 구별이 어려운 사람도\n알아보기 쉽게 하려는 거죠"),
    (70.0, 73.6, "퀴즈! 세로 신호등의 빨간불은\n항상 어디에 있을까?"),
    (73.6, 76.6, "정답은 맨 위쪽이에요!"),
    (76.6, 79.8, "색 대신 위치로도\n알 수 있게 한 거예요"),
    (80.2, 84.6, "다음에 신호등을 보면,\n색과 위치를 살펴보세요"),
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
