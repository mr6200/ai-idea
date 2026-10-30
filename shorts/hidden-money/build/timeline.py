"""Full 60 s timeline (thumbnail intro added at render): scene part animations from gen_scenes.py plus subtitle cues."""
import json
import os

ROOT = os.path.dirname(os.path.abspath(__file__))

# (start, end, text) in comp seconds; "\n" splits lines
CUES = [
    (0.1, 3.1, "지금 내 이름으로 된 돈이\n어딘가 잠자고 있다면?"),
    (3.2, 4.8, "생각보다\n많을 수 있어요"),
    (5.0, 8.4, "주인을 못 찾은 숨은 금융자산,\n무려 18조 4천억 원이에요"),
    (8.6, 11.0, "작년 6월 기준이고,\n해마다 늘고 있죠"),
    (11.2, 13.8, "잠자는 예금이 7조 5천억 원으로\n가장 많고"),
    (14.0, 17.6, "안 찾은 보험금 5조 8천억,\n카드포인트도 2조 9천억 원이에요"),
    (17.8, 20.6, "예금은 어카운트인포에서 내 이름의\n계좌를 한 번에 볼 수 있어요"),
    (20.8, 24.6, "1년 넘게 안 쓴 50만 원 이하 계좌는\n바로 옮기고 해지까지 돼요"),
    (24.8, 29.0, "보험금은\n내보험찾아줌 사이트에서,\n몰랐던 중도보험금이 나오기도 해요"),
    (29.4, 33.8, "카드포인트는 1포인트에 1원,\n한꺼번에 계좌로 받을 수 있어요"),
    (34.0, 36.8, "그냥 두면 사라져요,\n해마다 약 800억 원어치가요"),
    (37.0, 40.4, "퀴즈! 5년 넘게 잠든 휴면예금,\n이제 못 찾을까?"),
    (41.4, 43.4, "정답은, 찾을 수 있어요!"),
    (43.6, 47.2, "서민금융진흥원으로 넘어가도\n원래 주인은 기한 없이 돌려받아요"),
    (47.6, 49.6, "오늘 5분만 내서\n조회해 보세요"),
    (50.4, 53.6, "더 많은 돈 이야기가 궁금하다면\n구독해 주세요"),
]

IDLE = set()
DURATION = 60


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
