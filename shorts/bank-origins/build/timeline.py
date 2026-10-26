"""Full 120 s timeline: scene part animations from gen_scenes.py plus subtitle cues."""
import json
import os

ROOT = os.path.dirname(os.path.abspath(__file__))

# (start, end, text) in comp seconds; "\n" splits lines
CUES = [
    (0.1, 2.6, "은행은 처음부터\n있었을까요?"),
    (2.6, 4.8, "아니요, 시작은\n곡식 창고였어요"),
    (5.0, 8.8, "은행이 생기기까지,\n4천 년의 이야기"),
    (9.0, 12.4, "약 4천 년 전\n메소포타미아"),
    (12.4, 15.8, "신전과 궁전에\n곡식과 은을 맡겼어요"),
    (16.0, 19.4, "맡긴 사람은 점토판에\n기록을 받았고"),
    (19.4, 22.8, "남는 곡식은\n농부에게 빌려줬어요"),
    (23.0, 25.8, "갚을 땐 이자를 붙여서"),
    (25.8, 28.8, "함무라비 법전은\n이자 상한까지 정했죠"),
    (29.0, 32.4, "동전이 생기자\n고대 그리스에선"),
    (32.4, 35.8, "탁자에 앉은 환전상이\n돈을 바꿔 주다가"),
    (36.0, 38.8, "돈을 맡아 주고"),
    (38.8, 41.8, "빌려주는 일까지\n맡았어요"),
    (42.0, 45.4, "중세 이탈리아에서도\n환전상은 탁자에서 일했어요"),
    (45.4, 48.8, "탁자를 이탈리아어로\n'방코'라고 해요"),
    (49.0, 51.8, "여기서 '뱅크'라는\n말이 나왔죠"),
    (51.8, 54.8, "은행의 이름은\n탁자였던 셈이에요"),
    (55.0, 58.4, "1397년 피렌체에서\n메디치 은행이 문을 열고"),
    (58.4, 61.8, "멀리 떨어진 도시로\n어음 한 장으로 돈을 보냈어요"),
    (62.0, 65.0, "1472년에 세운\n몬테 데이 파스키 은행은"),
    (65.0, 67.8, "지금도 영업 중인\n가장 오래된 은행이에요"),
    (68.0, 71.4, "17세기 런던에선\n금을 금세공업자에게 맡기고"),
    (71.4, 74.8, "맡겼다는\n보관증을 받았어요"),
    (75.0, 77.8, "그런데 이 보관증을"),
    (77.8, 80.8, "금 대신 돈처럼\n주고받기 시작했어요"),
    (81.0, 83.8, "지폐가 태어난 순간이죠"),
    (83.8, 86.8, "1661년 스웨덴에선\n유럽 첫 은행권이 나왔어요"),
    (87.0, 90.4, "금세공업자들은 사람들이\n한꺼번에 찾지 않는 걸 알고"),
    (90.4, 93.8, "맡은 돈 일부를 빌려주고\n이자를 받았어요"),
    (94.0, 97.4, "정리하면, 맡아 주기,\n빌려주기, 바꿔 주기"),
    (97.4, 101.6, "보내 주기, 그리고 지폐.\n오늘 은행이 하는 일 그대로예요"),
    (102.0, 105.0, "퀴즈! 파산을 뜻하는\n'뱅크럽트'의 어원은?"),
    (105.0, 108.0, "부서진 탁자,\n'방카 로타'!"),
    (108.2, 111.8, "빚을 못 갚은 환전상의 탁자를\n부쉈다는 이야기가 전해져요"),
    (112.4, 116.0, "은행의 역사,\n재밌으셨나요?"),
    (116.2, 119.8, "더 많은 지식이 궁금하다면\n구독해 주세요"),
]

IDLE = set()
DURATION = 120


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
