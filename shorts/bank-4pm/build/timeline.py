"""Full 60 s timeline (thumbnail intro added at render): scene part animations from gen_scenes.py plus subtitle cues."""
import json
import os

ROOT = os.path.dirname(os.path.abspath(__file__))

# (start, end, text) in comp seconds; "\n" splits lines
CUES = [
    (0.1, 1.9, "은행은 왜 4시면\n문을 닫을까요?"),
    (2.0, 3.6, "직원들이 일찍 퇴근하는 걸까요?"),
    (3.7, 4.8, "사실은 정반대예요"),
    (5.0, 7.6, "셔터가 내려가면 그때부터\n진짜 마감이 시작돼요"),
    (7.8, 10.8, "은행원들은 그날 오간 현금을\n1원까지 맞춰 봐야 하거든요"),
    (11.3, 14.0, "안 맞으면 하루치 거래 내역을\n하나하나 다시 살펴요"),
    (14.2, 17.8, "수표와 세금 정리, 대출 서류까지,\n밤늦게 끝나는 날도 있죠"),
    (18.0, 21.2, "코로나 때는 9시 반부터\n3시 반까지로 줄었다가"),
    (21.4, 24.6, "2023년 1월에\n다시 9시부터 4시로 돌아왔어요"),
    (24.8, 27.0, "그런데 내년 4월부터는\n문을 30분 늦게 열어요"),
    (27.2, 30.0, "오전 9시 반에 열고,\n닫는 시간은 그대로 4시예요"),
    (30.4, 33.6, "퀴즈! 4시가 넘어 급한 은행 일은\n어디로 가야 할까?"),
    (34.4, 36.1, "정답은, 탄력점포예요!"),
    (36.3, 39.4, "저녁이나 주말에도 여는 점포를\n은행연합회에서 찾을 수 있어요"),
    (40.0, 42.4, "오늘도 4시 이후, 은행은\n불이 켜져 있어요"),
    (42.8, 45.2, "더 많은 돈 이야기가 궁금하다면\n구독해 주세요"),
]

IDLE = set()
DURATION = 48  # ends about 2.5 s after the last line (60 s is the maximum)


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
