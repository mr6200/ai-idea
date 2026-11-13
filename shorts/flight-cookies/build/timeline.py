"""Full 60 s timeline (thumbnail intro added at render): scene part animations from gen_scenes.py plus subtitle cues."""
import json
import os

ROOT = os.path.dirname(os.path.abspath(__file__))

# (start, end, text) in comp seconds; "\n" splits lines
CUES = [
    (0.1, 3.1, "비행기표, 쿠키를 지우면\n싸진다는 말 들어 봤죠?"),
    (3.2, 6.3, "검색할수록 비싸진다는\n그 소문, 사실일까요?"),
    (6.4, 8.4, "결론부터 말하면,\n아니에요"),
    (8.8, 12.2, "올해 네덜란드 시장 감독 기관이\n항공권 값을 조사했어요"),
    (12.3, 15.3, "쿠키를 지우거나 기기를 바꿔도\n값은 달라지지 않았어요"),
    (15.4, 18.1, "스카이스캐너도 쿠키는\n가격과 상관없다고 밝혔죠"),
    (18.4, 20.6, "그럼 다시 볼 때마다\n값이 왜 오를까요?"),
    (20.7, 23.6, "같은 비행기 자리에도\n가격 단계가 여러 개 있거든요"),
    (23.7, 26.6, "싼 단계가 다 팔리면\n다음 단계 가격이 열려요"),
    (26.9, 30.1, "자리 하나 값은 판매 기간 동안\n30번 넘게 바뀌어요"),
    (30.2, 33.8, "세 장 중 한 장은 평균보다\n40% 넘게 비싸게 팔리죠"),
    (34.1, 36.3, "다만 앞으로는\n달라질 수도 있어요"),
    (36.4, 40.3, "AI로 사람마다 값을 다르게 매기는\n맞춤 가격이 늘 거라는 전망이에요"),
    (40.6, 44.1, "자, 퀴즈! 이 조사에서 항공권 값이\n크게 오르기 시작한 때는?"),
    (45.0, 47.4, "정답은, 출발 두 달쯤 전이에요!"),
    (47.5, 49.4, "그 전에 가격 알림을\n켜 두는 게 좋아요"),
    (49.8, 52.4, "쿠키 대신 타이밍,\n그게 진짜 꿀팁이에요"),
    (52.5, 55.2, "더 많은 돈 이야기가 궁금하다면\n구독해 주세요"),
]

IDLE = set()
DURATION = 58  # ends about 2.5 s after the last line (60 s is the maximum)


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
