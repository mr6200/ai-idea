# 비행기표, 쿠키 지우면 싸질까? (58초 · 웹툰풍 액션 세미리얼)

- 58초 + 맨 앞 썸네일 1초 (60초는 최대 길이, 마지막 말 뒤 약 2.5초에서 끝냄), 7장면, TTS `ko-KR-Chirp3-HD-Charon` 1.2배속
- `shorts/credit-vs-debit/`을 틀로 씀 (액션 세미리얼 그림체, 같은 직장인 캐릭터 `CHAR`, 어두운 자막 상자)
- 대본 · 사실 확인 · TTS 검사: `script.md` / 업로드 정보: `youtube-metadata.md` / 콘티: `storyboard.html` · `.png`
- 완성 영상: `video/flight-cookies-shorts.mp4`, 썸네일: `thumbnail/thumbnail.png`

## 이번 편 메모

- **팩트체크형:** 훅에서 바로 "결론부터, 아니에요"를 말하고, 근거(2026년 ACM 조사) → 진짜 이유(가격 단계) → 숫자 → 앞으로의 전망 순
- **계단 그림 `step()`:** 아래에서 위로 넓어지는 가격 단계 상자 (S03, `wipeU`)
- **부품 이름 주의:** 장면 부품 이름을 `ai`로 지으면 배경 그림 레이어(`ai`)와 겹쳐 그 장면의 제목 · 부품이 사라짐 → `aiprice`로 바꿈
- **S01 다시 그림:** 인물이 화면 아래에 있어 얼굴이 자막에 가림 → 프롬프트를 "his face in the middle of the frame"으로
- **얼굴 가림:** S05 알약 · 안내를 위로(y=500, 630), 썸네일 말풍선을 왼쪽으로
- **TTS:** 「좌석」 → 「자리」, 「가격 칸」 → 「가격 단계」, 퀴즈 앞에 「자,」, AI → 「에이아이」 (`script.md`)

## RunPod 사용액

Seedream 4.0 그림 8장 = 약 $0.22. 잔액은 완성 보고에 적음.

## 다시 만들기

```
cd build && ./build_all.sh --render
```
