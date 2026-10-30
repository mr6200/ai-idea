# 18편 · 로또 1등은 정말 망할까? (60초 · 3D 클레이 AI + 인포그래픽)

- **60초 + 맨 앞 썸네일 1초** (18편부터 사용자 지정, 조회수 회복용), 8장면, TTS `ko-KR-Chirp3-HD-Charon` 1.2배속
- 대본 · 사실 확인 · TTS 검사: `script.md` / 업로드 정보: `youtube-metadata.md` / 콘티: `storyboard.html` · `.png`
- 완성 영상: `video/lotto-winners-shorts.mp4`, 썸네일: `thumbnail/thumbnail.png`

## 15편과 달라진 점

| 항목 | 15편 | 18편 |
|---|---|---|
| 길이 | 90초 + 썸네일 1.5초 | **60초 + 썸네일 1초** (`build_all.sh`의 `INTRO=1.0`, `timeline.py`의 `DURATION = 60`, `gen_audio.py`의 `DUR = 60.0`) |
| 장면 | 12 | 8 (장면당 5~11초) |
| 클레이 그림 | SDXL 서버리스 (엔드포인트를 만들고 지움) | **Seedream 4.0 공개 엔드포인트** (`gen_backgrounds_seedream.py`, 장당 $0.027, 1080×1920 바로, 만들고 지울 것 없음). 품질이 훨씬 좋음 |
| TTS 검사 | small 모델 | small로 검사 → 이상한 줄은 **medium으로 다시 받아써서** 진짜 잘못 읽는지 확인 (17편부터) |

## 60초 규격 메모

- 1.2배속에서 말하는 시간 약 40초, 문장 17개. 문장 사이를 0.2초 띄우고 퀴즈 정답 앞에 1초 쉼
- 퀴즈 + 구독은 약 18초 (42~60초)
- 챕터는 10초 이상 규칙 때문에 4개로 묶음

## RunPod 사용액

Seedream 4.0 그림 8장 = 약 $0.22. 잔액은 완성 보고에 적음.

## 다시 만들기

```
cd build && ./build_all.sh --render
```

`ai_bg/`의 그림은 커밋되어 있어 RunPod 없이 다시 빌드됩니다.
