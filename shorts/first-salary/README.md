# 24편 · 첫 월급 받으면 꼭 해야 할 3가지 (45초 · 웹툰풍)

- 45초 + 맨 앞 썸네일 1초 (60초는 최대 길이, 마지막 말 뒤 약 2.5초에서 끝냄), 6장면, TTS `ko-KR-Chirp3-HD-Charon` 1.2배속
- 23편 `shorts/salary-3days/`를 틀로 씀 (같은 웹툰 스타일, **같은 캐릭터** `CHAR`가 이어서 등장)
- 대본 · 사실 확인 · TTS 검사: `script.md` / 업로드 정보: `youtube-metadata.md` / 콘티: `storyboard.html` · `.png`
- 완성 영상: `video/first-salary-shorts.mp4`, 썸네일: `thumbnail/thumbnail.png`

## 이번 편 메모

- **흐름 상자 `flow()`:** 왼쪽에서 오른쪽으로 상자와 화살표를 잇는 도우미 (월급 → 저축 → 쓰기)
- **"딱 3가지" 목록형:** 제목에 ①②③을 붙여 장면마다 한 가지씩
- **TTS:** 한 글자로 끝나는 「750만 원!」을 「750만 원이에요!」로, 「연말정산 카드」를 「연말정산에서 카드」로 (`script.md`)
- 썸네일 제목이 인물 얼굴을 가려 두 줄로 줄이고 위로 올림

## RunPod 사용액

Seedream 4.0 그림 6장 = 약 $0.16. 잔액은 완성 보고에 적음.

## 다시 만들기

```
cd build && ./build_all.sh --render
```
