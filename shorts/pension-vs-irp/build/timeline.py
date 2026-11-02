"""Full 60 s timeline (thumbnail intro added at render): scene part animations from gen_scenes.py plus subtitle cues."""
import json
import os

ROOT = os.path.dirname(os.path.abspath(__file__))

# (start, end, text) in comp seconds; "\n" splits lines
CUES = [
    (0.1, 3.4, "연금저축과 IRP,\n둘 다 세금을 돌려주는데"),
    (3.5, 4.8, "뭐가 다를까요?"),
    (5.0, 7.6, "두 통장을 합치면\n900만 원까지 세액공제돼요"),
    (7.8, 10.2, "연금저축 혼자서는\n600만 원까지만 되고요"),
    (10.4, 12.4, "첫째, 가입 자격이 달라요"),
    (12.6, 15.4, "연금저축은 누구나 되지만,\nIRP는 소득이 있어야 해요"),
    (15.6, 19.9, "둘째, 돈 꺼내기, 연금저축은\n필요한 만큼 일부만 뺄 수 있어요"),
    (20.0, 23.4, "IRP는 집 구입 같은 사유가 없으면\n통째로 해지해야 해요"),
    (23.6, 27.6, "셋째, IRP는 주식 같은 위험자산을\n70%까지만 담을 수 있어요"),
    (27.8, 29.8, "이런 제한이 없는 건\n연금저축펀드예요"),
    (30.0, 33.2, "대신 IRP는 퇴직금을 받아\n연금으로 굴리는 통장도 돼요"),
    (33.8, 37.4, "퀴즈! 연금저축에만\n900만 원을 넣으면\n얼마까지 공제될까?"),
    (38.2, 40.4, "정답은, 600만 원까지예요!"),
    (40.6, 43.8, "그래서 남은 300만 원은\nIRP로 채우는 경우가 많아요"),
    (44.2, 48.4, "중간에 쓸 수도 있다면\n연금저축부터, 더 채우고 싶다면\nIRP를 더하세요"),
    (48.8, 51.4, "더 많은 돈 이야기가 궁금하다면\n구독해 주세요"),
]

IDLE = set()
DURATION = 54  # ends about 2.5 s after the last line (no padding to 60 s, user request)


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
