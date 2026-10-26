"""Full 70 s timeline: scene part animations from gen_scenes.py plus subtitle cues."""
import json
import os

ROOT = os.path.dirname(os.path.abspath(__file__))

# (start, end, text) in comp seconds; "\n" splits lines
CUES = [
    (0.1, 3.0, "침몰하지 않는 배, 타이타닉은\n왜 가라앉았을까요?"),
    (3.0, 4.8, "단 2시간 40분 만에요"),
    (5.0, 8.6, "1912년 4월, 당시 세계 최대 여객선\n타이타닉이 첫 항해에 나섰어요"),
    (8.6, 11.8, "사람들은 거의 가라앉지 않는\n배라고 불렀죠"),
    (12.0, 15.4, "배 밑은 벽으로 나뉜\n16개의 방수 칸"),
    (15.4, 18.8, "앞쪽 네 칸까지는\n물이 차도 버티게 만들었죠"),
    (19.0, 22.4, "그런데 4월 14일 밤,\n빙산에 옆구리가 긁혔어요"),
    (22.4, 25.8, "물이 들어온 칸은 여섯 칸.\n한계를 넘은 거예요"),
    (26.0, 29.4, "문제는 칸막이 벽 꼭대기가\n뚫려 있었다는 것"),
    (29.4, 32.8, "앞이 가라앉자 물이\n얼음틀처럼 다음 칸으로 넘쳤어요"),
    (33.0, 36.4, "구명보트는 20척,\n1,178명분뿐이었어요"),
    (36.4, 39.8, "배에는 2,200명이 넘게\n타고 있었는데 말이죠"),
    (40.0, 43.4, "결국 배는 둘로 부러져\n바다 밑으로 사라졌어요"),
    (43.4, 46.8, "약 1,500명이\n돌아오지 못했죠"),
    (47.0, 50.4, "이 사고 뒤 모든 승객이 탈\n구명보트를 싣게 됐고"),
    (50.4, 53.8, "빙산을 지켜보는\n국제 빙산 순찰대도 생겼어요"),
    (54.0, 57.6, "퀴즈! 타이타닉은 사고 뒤\n몇 년 만에 발견됐을까?"),
    (57.6, 60.0, "정답은 73년!"),
    (60.0, 61.8, "1985년, 4천 m 바다 밑에서요"),
    (62.2, 66.0, "가라앉지 않는 배는 없다,\n타이타닉이 남긴 교훈이에요"),
    (66.2, 69.8, "더 많은 지식이 궁금하다면\n구독해 주세요"),
]

IDLE = set()
DURATION = 70


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
