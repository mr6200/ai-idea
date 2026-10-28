"""Full 90 s timeline: scene part animations from gen_scenes.py plus subtitle cues."""
import json
import os

ROOT = os.path.dirname(os.path.abspath(__file__))

# (start, end, text) in comp seconds; "\n" splits lines
CUES = [
    (0.1, 2.8, "60세 퇴직인데,\n연금은 65세부터?"),
    (2.8, 4.8, "그 사이 5년,\n뭘로 살까요?"),
    (5.0, 8.4, "법으로 정한 정년은\n지금도 60세예요"),
    (8.4, 11.8, "65세 연장은 논의 중이지만,\n아직 정해지지 않았죠"),
    (12.0, 15.4, "그런데 국민연금은\n1969년생부터 65세에 받아요"),
    (15.4, 18.8, "출생연도에 따라\n61세에서 65세까지 달라요"),
    (19.0, 22.4, "월급은 끊기고\n연금은 아직인 5년"),
    (22.4, 25.8, "이걸 소득 크레바스,\n소득 절벽이라고 불러요"),
    (26.0, 29.4, "부부의 적정 생활비는\n한 달 약 300만 원"),
    (29.4, 32.8, "5년이면 무려\n1억 8천만 원이 필요해요"),
    (33.0, 36.8, "첫 번째 다리, 연금 당겨 받기.\n최대 5년 일찍 받을 수 있지만"),
    (36.8, 40.8, "1년에 6%씩,\n최대 30%가 평생 깎여요"),
    (41.0, 44.4, "두 번째 다리, 개인연금.\nIRP와 연금저축은 55세부터"),
    (44.4, 47.8, "퇴직금을 연금으로 나눠 받으면\n퇴직소득세도 30% 줄어요"),
    (48.0, 51.4, "세 번째 다리, 내 집.\n주택연금은 55세부터 가입돼요"),
    (51.4, 54.8, "집에 살면서\n매달 연금을 받는 거죠"),
    (55.0, 58.4, "네 번째 다리, 일하는 소득,\n재취업이나 작은 일거리라도"),
    (58.4, 61.8, "버는 만큼 모아 둔 돈을\n덜 꺼내 쓸 수 있어요"),
    (62.0, 65.8, "5년 다리는\n하나로는 부족해요"),
    (65.8, 69.8, "여러 개를 겹쳐서\n튼튼하게 받쳐 주세요"),
    (70.0, 73.6, "퀴즈! 국민연금을 5년 늦게 받으면\n얼마나 더 받을까?"),
    (73.6, 76.6, "정답은 36%!"),
    (76.6, 79.8, "1년에 7.2%씩\n늘어나거든요"),
    (80.2, 84.6, "은퇴 준비는\n5년 공백 메우기부터"),
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
