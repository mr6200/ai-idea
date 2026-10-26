"""Full 90 s timeline: scene part animations from gen_scenes.py plus subtitle cues."""
import json
import os

ROOT = os.path.dirname(os.path.abspath(__file__))

# (start, end, text) in comp seconds; "\n" splits lines
CUES = [
    (0.1, 2.6, "엘리베이터 줄이 끊어지면,\n추락할까요?"),
    (2.6, 4.8, "정답은,\n거의 안 떨어져요"),
    (5.0, 8.4, "1854년 뉴욕 박람회에서\n오티스가 엘리베이터에 탔어요"),
    (8.4, 11.8, "그리고 외쳤죠.\n줄을 끊으시오!"),
    (12.0, 15.4, "줄이 끊어졌지만, 엘리베이터는\n몇 센티 만에 멈췄어요"),
    (15.4, 18.8, "모두 안전합니다!\n오티스의 안전장치였죠"),
    (19.0, 22.4, "비밀은 톱니 레일.\n줄이 팽팽하면 걸쇠가 접혀 있고"),
    (22.4, 25.8, "줄이 느슨해지면 걸쇠가\n튀어나와 톱니에 걸려요"),
    (26.0, 29.4, "이 발명 덕분에 사람들이\n안심하고 엘리베이터를 탔고"),
    (29.4, 32.8, "높은 빌딩이\n하늘로 올라갈 수 있었죠"),
    (33.0, 36.8, "요즘 엘리베이터 줄은\n한 가닥이 아니에요"),
    (36.8, 40.8, "보통 4~8가닥,\n하나가 끊겨도 나머지가 버텨요"),
    (41.0, 44.4, "너무 빨리 내려가면\n꼭대기의 조속기가 알아채요"),
    (44.4, 47.8, "속도를 넘는 순간\n비상 브레이크를 당기죠"),
    (48.0, 51.4, "그러면 쐐기가 레일을 꽉 물어\n엘리베이터를 세워요"),
    (51.4, 54.8, "오티스 걸쇠의\n현대판이에요"),
    (55.0, 58.4, "맨 아래엔 완충기가\n마지막 충격까지 받아 줘요"),
    (58.4, 61.8, "이렇게 네 겹의 안전장치가\n엘리베이터를 지켜요"),
    (62.0, 65.8, "1945년, 폭격기가 부딪힌\n엠파이어 스테이트 빌딩"),
    (65.8, 69.8, "줄 끊긴 엘리베이터가\n75층을 떨어졌지만 살아남았죠"),
    (70.0, 73.6, "퀴즈! 떨어지는 엘리베이터에서\n바닥 직전에 점프하면 살까?"),
    (73.6, 76.6, "정답은 X!\n효과가 거의 없어요"),
    (76.6, 79.8, "떨어지는 속도에 비해\n점프는 너무 약하거든요"),
    (80.2, 84.6, "그러니 엘리베이터 줄 걱정은\n이제 그만!"),
    (84.8, 89.8, "더 많은 지식이 궁금하다면\n구독해 주세요"),
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
