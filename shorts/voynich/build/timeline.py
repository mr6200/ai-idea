"""Full 58 s timeline: scene part animations from gen_scenes.py plus subtitle cues."""
import json
import os

ROOT = os.path.dirname(os.path.abspath(__file__))

# (start, end, text) in comp seconds; "\n" splits lines
CUES = [
    (0.1, 2.7, "600년 된 책 한 권,\n그런데 아무도 읽지 못해요"),
    (2.8, 4.8, "세상에 없는 글자로\n가득하거든요"),
    (5.2, 7.0, "보이니치 필사본이라고 불러요"),
    (7.1, 10.9, "1912년 고서 수집가\n윌프리드 보이니치가 사들이며 알려졌죠"),
    (11.0, 14.5, "양피지를 조사해 보니\n1400년대 초에 만든 것이었어요"),
    (14.6, 18.9, "약 240쪽, 단어는 3만 8천 개쯤인데\n그 뜻을 아는 사람이 없어요"),
    (19.3, 21.1, "책 속엔 이상한 그림이\n가득해요"),
    (21.2, 22.9, "세상에서 찾을 수 없는 식물들,"),
    (23.0, 24.6, "별자리 같은 둥근 무늬,"),
    (24.7, 26.7, "초록빛 물에 몸을 담근\n여인들까지"),
    (26.8, 29.9, "약병 그림 옆에는\n요리법 같은 짧은 글들도 있죠"),
    (30.3, 35.2, "17세기 편지엔 황제 루돌프 2세가\n금화 600두카트에 샀다는\n말도 적혀 있죠"),
    (35.3, 38.9, "미국 최고의 암호 해독가\n윌리엄 프리드먼도 끝내 풀지 못했어요"),
    (39.3, 41.6, "누군가 꾸며 낸\n가짜라는 주장도 있지만,"),
    (41.7, 44.7, "글자 배열엔 진짜 언어 같은\n규칙이 있다는 분석도 있어요"),
    (44.8, 48.3, "해독했다는 주장은 여러 번 나왔지만,\n인정받은 건 하나도 없어요"),
    (48.7, 52.4, "600년 넘게 아무도 읽지 못한 책,\n여러분이라면 풀 수 있을까요?"),
    (52.8, 55.3, "더 많은 미스터리가 궁금하다면\n구독해 주세요"),
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
