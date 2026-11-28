# 세계의 미스터리 11화 · 스톤헨지 돌은 어디서 왔을까? (60초 · 실사 다큐 + 실제 사진)

- 본편 60초 + 맨 앞 썸네일 1.5초, 12장면 · 17문장, TTS `ko-KR-Chirp3-HD-Charon` 1.2배속
- 10화 `shorts/gobekli-tepe/`를 틀로 씀 (영상 요청 번호 저장 · `archive()` · `real_tag()` · `photo()`)
- 대본 · 사실 확인 · 사진 출처 · TTS 검사: `script.md` / 업로드 정보: `youtube-metadata.md` / 콘티: `storyboard.html` · `.png`
- 완성 영상: `video/stonehenge-shorts.mp4`, 썸네일: `thumbnail/thumbnail.png`

## 이번 편에 적용한 사용자 규칙

- 주제는 추천 후보 4개 중 사용자가 고름
- 실제 사진 7장면 (CC BY · CC BY-SA, 화면과 설명란에 작가 · 라이선스), AI 영상 3장면, AI 사진 2장면
- 썸네일 전에 제목을 물어봄 → 「스톤헨지 돌은 어디서 왔을까?」
- 퀴즈 없음, 썸네일 포함 61.5초, 화면 위 라벨에 편 번호 없음

## 이번 편 메모

- 이야기 순서를 돌의 거리순(25km → 200km 넘게 → 700km 넘게)으로 짜서 마지막 반전(2024년 제단석)으로 이어지게 함
- Seedream이 길게 누운 물체(썰매 위 돌, 뗏목)를 그리면 그림 전체가 옆으로 눕는 일이 잦음 → 프롬프트 맨 앞에 「Upright vertical portrait photo, eye-level view, horizon level across the frame, sky at the top」을 넣으니 바로 섬
- 위키미디어가 요청 횟수 제한(429)으로 사진 하나를 계속 막아서, 같은 사진의 원래 출처(geograph.org.uk)에서 받음 (라이선스 같음)
- 「사센석」은 TTS · 받아쓰기 모두 어색해서 정식 표기 「사르센석」을 씀. 「20톤 안팎」은 [토난팍]으로 이어 읽혀 「20톤쯤」으로 바꿈

## RunPod 사용액

AI 사진 13장 약 $0.35 + WAN 2.2 클립 3개 $0.90 = **약 $1.25**. 잔액은 완성 보고에 적음. 잔액은 $13.76 → $12.21로 $1.55가 줄어, 계산보다 약 $0.30 더 나감 (원인 미확인: 사용 내역 REST API에 이 환경에서 연결되지 않았고, 남은 엔드포인트 · 파드 · 네트워크 볼륨은 없음).

## 다시 만들기

```
cd build && ./build_all.sh --render
```

`footage/`(AI 클립 · 사진)와 `photos/`(실제 사진)는 커밋되어 있어 RunPod 없이 다시 빌드됩니다.
