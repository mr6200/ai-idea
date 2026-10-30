"""Full 90 s timeline: scene part animations from gen_scenes.py plus subtitle cues."""
import json
import os

ROOT = os.path.dirname(os.path.abspath(__file__))

# (start, end, text) in comp seconds; "\n" splits lines
CUES = [
    (0.1, 2.4, "여자는 왜 남자보다\n더 오래 살까요?"),
    (2.4, 4.8, "그 비밀은\n우리 몸속에 있어요"),
    (5.0, 9.6, "2024년 한국 기대수명은\n여자 86.6세, 남자 80.8세"),
    (9.6, 13.4, "차이는 5.8년, 세계 거의\n모든 나라에서 여자가 더 오래 살아요"),
    (13.6, 17.2, "첫째 비밀은 염색체,\n여자는 X염색체가 두 개예요"),
    (17.2, 20.4, "하나에 고장 난 유전자가 있어도\n다른 하나가 대신해 주죠"),
    (20.6, 23.4, "남자는 X가 하나뿐이라\n고장이 그대로 드러나요"),
    (23.4, 26.8, "색맹이나 혈우병이\n남자에게 훨씬 많은 이유예요"),
    (27.0, 30.4, "둘째 비밀은 호르몬,\n여성호르몬 에스트로겐은"),
    (30.4, 33.4, "혈관을 부드럽게 해서\n심장을 지켜 줘요"),
    (33.6, 37.4, "반대로 남성호르몬 테스토스테론은\n면역력을 떨어뜨릴 수 있어요"),
    (37.4, 39.4, "그래서 이런\n놀라운 기록도 있죠"),
    (39.6, 43.0, "조선 시대 내시들은\n평균 약 70세까지 살았어요"),
    (43.0, 46.8, "같은 시대 양반 남자보다\n14년에서 19년이나 길었죠"),
    (47.0, 51.6, "마지막 비밀은 생활 습관,\n남자 흡연율은 여자의 다섯 배가 넘어요"),
    (51.6, 54.2, "술을 마시는 사람도\n남자가 더 많아요"),
    (54.4, 57.4, "그런데 갓난아기 때부터\n여자아이가 더 잘 살아남아요"),
    (57.4, 60.6, "기근과 전염병 속에서도\n그랬다는 연구가 있어요"),
    (60.8, 64.4, "하지만 여자는 오래 사는 만큼\n아픈 채 지내는 기간도 더 길어요"),
    (64.4, 67.8, "그래서 오래 사는 것만큼\n건강하게 사는 게 중요하죠"),
    (68.0, 71.8, "퀴즈! 새는 암컷이 더 오래 살까,\n수컷이 더 오래 살까?"),
    (72.6, 74.6, "정답은, 수컷이에요!"),
    (74.6, 79.0, "새는 사람과 반대로, 수컷이\n똑같은 성염색체를 두 개 가졌거든요"),
    (79.6, 83.8, "남자분들, 금연과 건강검진부터\n챙겨 보세요"),
    (84.2, 89.8, "더 많은 지식이 궁금하다면\n구독해 주세요"),
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
