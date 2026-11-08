"""Full 58 s timeline: scene part animations from gen_scenes.py plus subtitle cues."""
import json
import os

ROOT = os.path.dirname(os.path.abspath(__file__))

# (start, end, text) in comp seconds; "\n" splits lines
CUES = [
    (0.1, 4.2, "1947년, 미군이 직접\n「비행접시를 회수했다」고 발표했어요"),
    (4.6, 8.0, "미국 뉴멕시코의 한 목장에서\n이상한 잔해가 발견됐거든요"),
    (8.1, 11.6, "은박지 같은 조각과 고무,\n종이, 나무 막대들이었죠"),
    (12.0, 16.0, "그날 지역 신문 1면 제목도\n「비행접시를 잡았다」였죠"),
    (16.1, 17.7, "그런데 하루 만에\n말이 바뀌었어요"),
    (17.8, 20.2, "잔해는 그저\n기상 관측 풍선이라는 거예요"),
    (20.6, 25.7, "사건은 30년 넘게 잊혔다가,\n1978년 당시 장교의 인터뷰로\n되살아났어요"),
    (25.8, 28.3, "이어서 외계인 시신을 봤다는\n이야기까지 퍼졌죠"),
    (28.7, 32.1, "결국 1994년,\n미 공군이 조사 보고서를 냈어요"),
    (32.2, 35.4, "잔해의 정체는 「프로젝트 모굴」,\n비밀 풍선 작전이었어요"),
    (35.5, 38.8, "풍선에 소리 감지기를 달아\n소련의 핵실험을 엿들으려 했죠"),
    (38.9, 42.3, "기상 풍선이라고 둘러댄 건\n비밀 작전을 감추려던 거였대요"),
    (42.7, 48.0, "1997년 보고서는\n외계인 시신 이야기도 낙하 시험용\n인형을 착각한 거라고 했죠"),
    (48.4, 50.5, "그래도 로스웰은 지금\nUFO 마을로 불려요"),
    (50.6, 52.4, "여러분은\n어느 쪽을 믿나요?"),
    (52.5, 55.0, "더 많은 미스터리가 궁금하다면\n구독해 주세요"),
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
