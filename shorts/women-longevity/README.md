# 17편 · 여자는 왜 더 오래 살까? (실사 다큐 스타일)

- 1분 30초 + 맨 앞 썸네일 1.5초, 12장면 · 14클립, TTS `ko-KR-Chirp3-HD-Charon` 1.2배속
- 대본 · 사실 확인 · TTS 검사: `script.md` / 업로드 정보: `youtube-metadata.md` / 콘티: `storyboard.html`·`.png`
- 완성 영상: `video/women-longevity-shorts.mp4`, 썸네일: `thumbnail/thumbnail.png`

## 스타일: 실사 다큐 (17편, 사용자 요청)

사용자가 「RunPod으로 실사 다큐 느낌」을 원했고, SDXL 시험 그림의 얼굴이 어색하다고 해서 **WAN 2.2 영상**으로 만들었습니다.

| 요소 | 규칙 |
|---|---|
| 배경 | 장면마다 AI 실사 영상. Seedream 4.0으로 세로 사진(1080×1920)을 그리고 WAN 2.2 I2V 720p로 5초 영상(720×1280, 30fps) |
| 색감 | 채도 0.86, 대비 1.05, 살짝 따뜻하게, 고운 움직이는 입자 (`prep_footage.py`의 `GRADE`), 옅은 비네트(`film.png`) |
| 위·아래 그늘 | 위 720px · 아래 740px 검은 그러데이션 (`shade()`) — 제목과 자막이 영상 위에서 읽히게 |
| 라벨 | 맨 위 노란 글자 `인체의 신비 · 수명` (y=200, 도현) |
| 제목 | Black Han Sans, 흰색/노랑 `#f2c14e`, 옅은 검은 테두리 (`head()`) |
| 숫자 카드 | 반투명 검은 상자 + 노란 세로 띠 + 도현 (`lower()`), 값 막대 (`bar()`), 빨간 알약 도장 (`pill()`) |
| 자막 | 흰 도현 58px + 검은 테두리 + 옅은 반투명 상자, 중심 y=1480 |
| 음악 | 잔잔한 패드 + 펠트 피아노 (Am–F–C–G, 70bpm), 효과음은 작게 |
| 배치 | **인물 얼굴을 가리지 않게** 사진을 보고 카드 위치를 장면마다 정함 (예: S02는 숫자를 위에, 도장을 아래에) |

## AI 영상 만들기 (`build/gen_footage.py`, RunPod Public Endpoints)

엔드포인트를 만들거나 지울 필요가 없는 공개 엔드포인트를 씁니다 (요청당 요금).

1. `python gen_footage.py images` — 장면마다 Seedream 4.0 사진 2장 (시드 1701·1702, 장당 $0.027) → `footage/cand/`
2. 사진을 보고 `PICK`에 고름 (얼굴·손·구도. Seedream이 가끔 옆으로 누운 구도를 그림 → S11·S12는 b)
3. `python gen_footage.py video` — WAN 2.2 I2V 720p, `size: "720*1280"`, 30스텝 ($0.30/클립, 약 3분, 6개씩 동시에) → `footage/Sxx.mp4`
4. `prep_footage.py`가 클립을 장면 길이에 맞게 느리게 하고(최대 1.6배, `minterpolate` 움직임 보간) 색을 입혀 `parts/Sxx/video.mp4`로 씀. S11·S12는 클립 2개를 `SPLIT` 초에서 이어 붙임
5. EffectCraft는 mp4를 레이어로 바로 가져옴 (`gen_effectcraft.py`의 `video` 부품)

- WAN 2.2는 사진을 움직이기만 하므로 얼굴 품질은 시작 사진이 정합니다. Flux Dev는 크기 값을 무시하고 정사각형만 줘서 Seedream을 씀
- 사극 인물(S07 내시)은 프롬프트에 "수염 없음"을 넣어도 수염을 그려서, 수염이 없는 처음 그림을 씀

## RunPod 사용액

| 항목 | 금액 |
|---|---|
| 스타일 시험 (SDXL 예시, Flux 사진, WAN 시험 클립 1개) | 약 $0.34 |
| Seedream 사진 29장 | 약 $0.78 |
| WAN 2.2 클립 14개 | 약 $4.20 |

잔액과 실제 차감액은 완성 보고에 적음.

## 다시 만들기

```
cd build && ./build_all.sh --render
```

`footage/`의 클립과 사진은 커밋되어 있어 RunPod 없이 다시 빌드됩니다. `parts/Sxx/video.mp4`는 빌드 때 다시 만들어짐 (git 제외).
