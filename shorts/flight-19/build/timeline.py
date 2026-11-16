"""Full 61 s timeline: scene part animations from gen_scenes.py plus subtitle cues."""
import json
import os

ROOT = os.path.dirname(os.path.abspath(__file__))

# (start, end, text) in comp seconds; "\n" splits lines
CUES = [
    (0.1, 5.0, "1945년 12월, 미 해군 폭격기 다섯 대가\n훈련 비행 중 통째로 사라졌어요"),
    (5.1, 8.7, "플로리다 기지를 떠난 어벤저 폭격기,\n탄 사람은 14명이었죠"),
    (9.1, 11.6, "얼마 뒤, 편대장의\n다급한 교신이 들어와요"),
    (11.7, 13.4, "「나침반이 둘 다 고장 났다」"),
    (13.8, 16.1, "편대는 방향을 잃고\n바다 위를 헤맸어요"),
    (16.2, 20.0, "날은 어두워지고 파도는 거세졌고,\n저녁 무렵 교신이 끊겼죠"),
    (20.4, 24.3, "구조 비행정이 13명을 태우고 떴지만,\n이 비행기도 돌아오지 않았어요"),
    (24.4, 27.8, "근처 유조선은 그날 밤\n하늘에서 불길을 봤다고 보고했죠"),
    (27.9, 31.5, "닷새 동안 넓은 바다를 뒤졌지만\n잔해는 하나도 찾지 못했어요"),
    (31.6, 34.4, "모두 27명,\n돌아온 사람은 없었어요"),
    (34.5, 38.3, "이 사건은 훗날, 버뮤다 삼각지대\n전설의 대표 사례가 돼요"),
    (38.4, 41.6, "하지만 해군 조사는 길을 잃고\n연료가 떨어졌을 거라고 봤어요"),
    (41.7, 45.5, "처음엔 편대장의 실수라고 했다가,\n나중에 원인 불명으로 고쳤죠"),
    (45.6, 48.5, "구조기는 연료 증기로\n폭발 사고가 나던 기종이었고요"),
    (48.8, 52.5, "보험사와 해안 경비대는 이 바다가\n다른 곳보다 위험하지 않다고 해요"),
    (52.6, 55.2, "다만 여섯 대의 비행기는\n지금도 발견되지 않았어요"),
    (55.6, 58.0, "더 많은 미스터리가 궁금하다면\n구독해 주세요"),
]

IDLE = set()
DURATION = 61


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
