"""Full 58 s timeline: scene part animations from gen_scenes.py plus subtitle cues."""
import json
import os

ROOT = os.path.dirname(os.path.abspath(__file__))

# (start, end, text) in comp seconds; "\n" splits lines
CUES = [
    (0.1, 4.0, "히말라야 해발 4,500m가 넘는 곳,\n얼음이 녹으면 드러나는 호수가 있어요"),
    (4.1, 5.9, "물속엔 수백 명의 뼈가\n잠겨 있죠"),
    (6.3, 9.1, "인도의 루프쿤드,\n일명 해골 호수예요"),
    (9.5, 13.1, "1942년 산림 감시원이\n이 뼈를 발견했을 때,"),
    (13.2, 16.3, "영국 당국은 숨어든\n일본군이 아닐까 걱정했대요"),
    (16.4, 18.3, "하지만 뼈는 훨씬\n오래된 것이었죠"),
    (18.4, 20.5, "지금까지 나온 유해는\n300명이 넘어요"),
    (20.9, 24.2, "오랫동안은 이 사람들이\n한꺼번에 숨졌다고 봤어요"),
    (24.3, 27.4, "순례 행렬이 큰 우박 폭풍을\n만났다는 전설도 유명했죠"),
    (27.8, 31.2, "그런데 2019년,\n38명의 DNA를 분석하자"),
    (31.3, 32.7, "뜻밖의 결과가\n나왔어요"),
    (33.0, 36.0, "23명은 남아시아 사람으로\n800년 무렵에 숨졌는데,"),
    (36.1, 39.3, "14명은 지중해 동부 사람으로\n1800년 무렵에 숨졌어요"),
    (39.4, 41.3, "한 명은 동남아시아\n사람이었고요"),
    (41.4, 45.2, "약 1,000년 차이를 두고,\n서로 다른 사람들이\n같은 호수에서 숨진 거죠"),
    (45.6, 49.0, "이 호수 곁으로는 지금도\n12년마다 큰 순례 행렬이 지나가요"),
    (49.3, 53.1, "하지만 지중해 사람들이\n왜 이 높은 곳까지 왔는지는\n아직 아무도 몰라요"),
    (53.5, 55.9, "더 많은 미스터리가 궁금하다면\n구독해 주세요"),
]

IDLE = set()
DURATION = 58


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
