# 체크카드만 쓰면 손해일까? (49초 · 웹툰풍 액션 세미리얼)

- 49초 + 맨 앞 썸네일 1초 (60초는 최대 길이, 마지막 말 뒤 약 2.5초에서 끝냄), 8장면, TTS `ko-KR-Chirp3-HD-Charon` 1.2배속
- `shorts/bank-4pm/`을 틀로 씀. 그림체는 **액션 세미리얼** 첫 편 (`shorts/webtoon-styles/4_action.png`), 같은 직장인 캐릭터 `CHAR`
- 대본 · 사실 확인 · TTS 검사: `script.md` / 업로드 정보: `youtube-metadata.md` / 콘티: `storyboard.html` · `.png`
- 완성 영상: `video/credit-vs-debit-shorts.mp4`, 썸네일: `thumbnail/thumbnail.png`

## 이번 편 메모

- **액션 세미리얼 색:** 제목 외곽선 짙은 보라 `NAVY #2b1055`, 강조 글씨 주황 노랑 `YELLOW #ffb703`, 효과음 주황 `ORANGE #ff5400`. 자막은 어두운 상자 `#14141f` + 주황 노랑 테두리 · 그림자, 흰 글씨 (`gen_subtitles.py`)
- **그림 다시 그리기 5장:** 옆으로 누운 그림(S02 · S04, 프롬프트에 "standing upright … upright portrait orientation"), 그림 속 글씨(S03 「Pay now」 버튼, S05 카드 위 글씨) → 버튼 · 카드를 빼고 다른 동작으로, S08 어색한 카드 → 빼고 손을 주머니에
- **얼굴 가림:** 액션 그림은 인물이 크고 가운데라 S01 말풍선(왼쪽 위로), S02 흐름표(위로), S04 알약(위로), S07 퀴즈 보기(y=860부터, 간격 140)를 옮김
- **TTS:** 「할인과 적립도」 → 「할인이나 포인트 적립도」, 「올가을부터」 → 「이번 가을부터」 (`script.md`)
- **자막 시각:** 실제 TTS 길이를 재서 자막 시각을 다시 배치 (처음 어림 52초 → 49초)
- **시간이 지나면 고칠 것:** "이번 가을부터"(2026년 9~10월 시행), 리볼빙 평균 금리(2026년 7월)

## RunPod 사용액

Seedream 4.0 그림 13장 = 약 $0.35. 잔액은 완성 보고에 적음.

## 다시 만들기

```
cd build && ./build_all.sh --render
```
