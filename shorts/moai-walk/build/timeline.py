"""Full 58 s timeline: scene part animations from gen_scenes.py plus subtitle cues."""
import json
import os

ROOT = os.path.dirname(os.path.abspath(__file__))

# (start, end, text) in comp seconds; "\n" splits lines
CUES = [
    (0.1, 4.1, "바퀴도, 큰 가축도 없던 섬,\n이 거대한 석상은 어떻게 옮겼을까요?"),
    (4.5, 7.7, "남미에서 3,500km 떨어진\n외딴섬, 이스터섬"),
    (7.8, 10.5, "이곳엔 모아이라는 석상이\n천 개 가까이 서 있어요"),
    (10.6, 13.0, "높이는 평균 4미터,\n무게는 12톤이 넘어요"),
    (13.4, 17.1, "대부분은 화산 라노 라라쿠에서\n바위를 깎아 만들었어요"),
    (17.2, 20.6, "그리고 섬 곳곳의 바닷가까지\n몇 킬로미터를 옮겼죠"),
    (21.0, 23.4, "섬에는 모아이가 스스로\n걸어갔다는 전설이 있어요"),
    (23.5, 26.7, "학자들은 오랫동안 통나무나 썰매에\n눕혀 끌었다고 생각했죠"),
    (27.1, 30.1, "그런데 2012년,\n고고학자들이 직접 실험해 봤어요"),
    (30.2, 33.2, "약 4톤짜리 모형 석상을 세워\n밧줄 세 개를 묶고"),
    (33.3, 36.6, "양옆에서 번갈아 당기자,\n석상이 좌우로 흔들리며 앞으로!"),
    (36.7, 39.1, "18명이 40분 만에\n100미터를 옮겼어요"),
    (39.5, 43.3, "2025년 연구는 옛길 위에\n남은 모아이 62개를 살폈는데"),
    (43.4, 46.6, "밑동이 넓고 앞으로 살짝 기운,\n걷기 좋은 모양이었어요"),
    (47.0, 50.0, "전설 속 걷는 석상은\n운반 방법이었을지도 몰라요"),
    (50.1, 52.2, "다만 모든 학자가\n동의하는 건 아니에요"),
    (52.3, 54.8, "더 많은 미스터리가 궁금하다면\n구독해 주세요"),
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
