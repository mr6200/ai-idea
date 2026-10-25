"""Full 150 s timeline: scene part animations from gen_scenes.py plus subtitle cues."""
import json
import os

ROOT = os.path.dirname(os.path.abspath(__file__))

# (start, end, text) in comp seconds; "\n" splits lines
CUES = [
    (0.1, 2.6, "1,000만 원이\n2,000만 원 되려면"),
    (2.6, 4.9, "몇 년이 걸릴까요?"),
    (5.1, 7.6, "연 2% 예금이면 약 35년"),
    (7.6, 9.9, "연 8%면 약 9년이에요"),
    (10.1, 13.9, "이걸 계산기 없이\n3초 만에 푸는 법"),
    (14.2, 17.4, "바로 ‘72의 법칙’입니다"),
    (17.4, 21.8, "72를 수익률로 나누면\n돈이 두 배 되는 해가 나와요"),
    (22.2, 25.4, "연 6%면\n72 ÷ 6 = 12년"),
    (25.4, 28.6, "연 8%면\n72 ÷ 8 = 9년"),
    (28.6, 31.8, "연 12%면\n72 ÷ 12 = 6년"),
    (31.8, 34.8, "나눗셈 한 번이면 끝!"),
    (35.2, 38.6, "정말 맞을까요?\n실제로 계산해 봤습니다"),
    (38.6, 42.6, "연 6%는 실제 11.9년,\n연 8%는 9.0년"),
    (42.6, 46.8, "오차가 두 달도\n안 됩니다"),
    (47.2, 50.6, "그런데 왜 하필\n72일까요?"),
    (50.6, 54.8, "수학적으로 정확한 숫자는\n사실 69.3이에요"),
    (55.2, 59.6, "두 배는 자연로그 2,\n약 0.693에서 나오거든요"),
    (59.6, 63.6, "그런데 69.3으로\n암산할 수 있나요?"),
    (63.6, 67.8, "69.3 ÷ 7…\n벌써 머리가 아프죠"),
    (68.2, 72.4, "72는 1, 2, 3, 4, 6, 8, 9, 12로\n딱 나눠떨어집니다"),
    (72.4, 75.6, "게다가 수익률 8% 근처에선"),
    (75.6, 79.8, "69.3보다 72가\n오히려 더 정확해요"),
    (80.2, 83.8, "거꾸로도 쓸 수 있어요"),
    (83.8, 89.8, "10년 안에 두 배를 원하면\n72 ÷ 10 = 7.2%가 필요하죠"),
    (90.2, 94.6, "30살에 1,000만 원을\n연 8%로 굴리면"),
    (94.6, 99.8, "9년마다 두 배씩,\n66살엔 약 1억 6천만 원"),
    (100.2, 104.4, "72의 법칙은\n무서운 쪽에도 통합니다"),
    (104.4, 109.8, "물가가 매년 3% 오르면\n24년 뒤 내 돈 가치는 반토막"),
    (110.2, 114.2, "연 18% 이자의 빚은?"),
    (114.2, 119.8, "72 ÷ 18 = 4년,\n4년 만에 빚이 약 두 배"),
    (120.2, 124.6, "보너스! 세 배가 되는 해는\n114 ÷ 수익률"),
    (124.6, 127.8, "네 배는 144 ÷ 수익률"),
    (128.2, 131.8, "정리하면,\n숫자 72 하나로"),
    (131.8, 135.8, "두 배 시간, 필요한 수익률,\n물가와 빚의 무서움까지"),
    (136.2, 138.7, "퀴즈! 연 9%면?"),
    (138.7, 141.8, "정답은 8년!"),
    (142.2, 145.8, "오늘부터 72를\n기억해 보세요"),
    (146.2, 149.8, "더 많은 지식이 궁금하다면\n구독해 주세요"),
]

IDLE = {("S07", "person"), ("S17", "note")}
DURATION = 150


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
