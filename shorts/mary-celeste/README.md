# 세계의 미스터리 1화 · 메리 셀레스트호 (56초 · 실사 역사 다큐)

- 56초 + 맨 앞 썸네일 1초, 7장면 · 10클립 · 18문장, TTS `ko-KR-Chirp3-HD-Charon` 1.2배속
- **새 시리즈 「세계의 미스터리」 첫 편** (돈 · 생활 지식 쇼츠 26편 자리 대신, 사용자 요청)
- 17편 `shorts/women-longevity/`(실사 다큐, Seedream → WAN 2.2)를 틀로 쓰고, 25편 `shorts/bank-4pm/`의 최신 `gen_narration.py` · `tts_check.py`와 60초 규격(썸네일 1초)을 가져옴
- 대본 · 사실 확인 · TTS 검사: `script.md` / 업로드 정보: `youtube-metadata.md` / 콘티: `storyboard.html` · `.png`
- 완성 영상: `video/mary-celeste-shorts.mp4`, 썸네일: `thumbnail/thumbnail.png`

## 스타일: 실사 역사 다큐 (미스터리 시리즈)

| 요소 | 규칙 |
|---|---|
| 영상 | Seedream 4.0 세로 사진 → WAN 2.2 I2V 720p 5초 클립, 장면 길이에 맞춰 느리게 + 움직임 보간 (`prep_footage.py`) |
| 사진 톤 (`LOOK`) | 1870년대 고증, 흐린 바다 빛 · 안개, 청회색으로 채도 낮춤, 35mm 필름 입자. 사람은 뒷모습 · 손만 (실존 인물 얼굴 없음) |
| 라벨 | 맨 위 노란 글자 `세계의 미스터리 · 1화` |
| 글씨 | 17편과 같음: Black Han Sans 제목(흰색/노랑 `#f2c14e`), 반투명 검은 카드 + 노란 띠(`lower()`), 빨간 도장 알약 |
| 음악 | 어두운 단조 패드 Dm–B♭–Gm–A, 60bpm, 낮은 피아노 몇 음 (`gen_audio.py`) |

## 이번 편 메모

- **두 클립 장면:** S03(선장실 → 식량 창고), S04(찻잔 → 글 쓰는 손), S05(끊어진 밧줄 → 떠나가는 보트)는 `prep_footage.SPLIT` 초에서 이어 붙임
- **자막 시각 자동 배치:** TTS 실제 길이를 재서 `start = 앞 줄 끝 + 0.1초`, 끝 = 길이 + 0.25초로 배치 → 빨리 감기 0줄
- **AI 사진이 내용과 반대:** "구명보트가 없었다" 장면에 Seedream이 계속 보트를 그려, 끊어진 밧줄 클로즈업으로 구도를 바꿈. 창고 사진의 요즘 유리병도 다시 그림
- **숫자 읽기:** 「1,701개」가 「천칠백일개」로 읽혀 `SPOKEN`에 「천칠백한 개」 추가
- **썸네일 · 첫 화면 문구:** 10명에는 선장 가족이 들어 있어 「선원 10명」 대신 「배 위 10명」, 「사람만 사라진」으로 씀
- **겹침:** S03 카드 두 장이 같은 자리라 아래로 나눔, 퀴즈 정답 알약 뒤에 어두운 띠를 깔아 보기를 가림
- `faster-whisper`가 없으면 `pip install faster-whisper` (Whisper medium 확인은 오디오를 numpy로 넘김. 파일 경로로 넘기면 PyAV 버전 오류)

## RunPod 사용액

Seedream 사진 23장 약 $0.62 + WAN 2.2 클립 10개 $3.00 = **약 $3.62**. 잔액은 완성 보고에 적음.

## 다시 만들기

```
cd build && ./build_all.sh --render
```

`footage/`의 클립과 사진은 커밋되어 있어 RunPod 없이 다시 빌드됩니다. 다시 만들려면 `python3 gen_footage.py images|video [Sxx]` (비용 발생).
