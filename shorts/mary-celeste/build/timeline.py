"""Full 61 s timeline: scene part animations from gen_scenes.py plus subtitle cues."""
import json
import os

ROOT = os.path.dirname(os.path.abspath(__file__))

# (start, end, text) in comp seconds; "\n" splits lines
CUES = [
    (0.1, 3.9, "1872년 대서양 한가운데,\n유령선이 발견됐어요"),
    (4.0, 6.1, "배는 멀쩡한데\n사람만 사라졌죠"),
    (6.5, 9.8, "12월 4일, 지나던 배가\n홀로 떠도는 배를 만났어요"),
    (9.9, 11.4, "올라가 보니\n아무도 없었어요"),
    (11.8, 14.7, "선장과 아내, 두 살 딸까지\n열 명이 사라졌어요"),
    (14.8, 17.8, "그런데 배에는 여섯 달 치\n식량과 물이 그대로"),
    (17.9, 20.9, "짐칸의 술통 1,701개도\n거의 그대로였어요"),
    (21.3, 24.7, "따뜻한 찻잔이 남아 있었다는\n이야기, 들어 보셨나요?"),
    (24.8, 26.3, "사실 그런 기록은\n없어요"),
    (26.4, 30.7, "셜록 홈스 작가 코난 도일의\n1884년 소설과 함께 퍼진 이야기죠"),
    (31.1, 33.1, "정말 없어진 건\n작은 구명보트 하나,"),
    (33.2, 35.3, "그리고 항해 도구와\n배 서류들이었어요"),
    (35.4, 37.8, "스스로 배를 버리고\n떠났을 가능성이 크다는 뜻이죠"),
    (38.2, 41.6, "당시 법정은 살인을 의심하고\n배를 꼼꼼히 조사했어요"),
    (41.7, 44.7, "하지만 석 달 넘게 따져 봐도\n범죄 흔적은 찾지 못했죠"),
    (45.1, 47.4, "짐칸엔 바닷물이\n1미터 넘게 차 있었고"),
    (47.5, 50.2, "새어 나온 술 냄새에 폭발을\n걱정했다는 추측도 있어요"),
    (50.3, 52.5, "그리고 열 명은\n끝내 돌아오지 않았어요"),
    (52.9, 55.5, "150년이 지난 지금도\n풀리지 않은 수수께끼예요"),
    (55.6, 58.1, "더 많은 미스터리가 궁금하다면\n구독해 주세요"),
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
