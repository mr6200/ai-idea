# 국민연금, 낸 돈보다 더 받을까? — YouTube Shorts (15편)

1분 30초 · 1080×1920 · 30fps 지식 쇼츠. 노후 준비 시리즈 3편, 13·14편과 같은 **3D 클레이 AI + 미니멀 인포그래픽** 스타일. **TTS 검사**(`build/tts_check.py`)를 처음 넣은 편.

| 파일 | 내용 |
|---|---|
| `script.md` | 대본, TTS 검사로 고친 문장, 사실 확인 (2026년 10월 기준) |
| `build/tts_report.md` | TTS 검사 결과 (줄마다 읽는 말·받아쓰기·길이·경고) |
| `storyboard.html` / `.png` | 12컷 콘티 (장면 그림·모션·내레이션) |
| `scenes/` | 장면별 벡터 원본(`.vectorcraft`)과 미리보기 PNG (AI 그림 포함) |
| `build/ai_bg/` | 장면별 AI 클레이 그림 12장 (RunPod 서버리스 SDXL 30단계, 장면마다 2장 그려 고름) |
| `audio/narration-preview.mp3` | 내레이션 미리 듣기 (Google Cloud TTS `ko-KR-Chirp3-HD-Charon`, 1.2배속, 쉼표 쉼, 25문장) |
| `thumbnail/` | 썸네일 (1080×1920) |
| `youtube-metadata.md` | 제목·설명·태그·챕터 |
| `video/pension-return-shorts.mp4` | 완성 영상 (1:30, H.264 Main, −14.2 LUFS) |
| `video/pension-return.ecproj` | EffectCraft 프로젝트 (장면별 프리컴프 + Main) |

## 다시 만들기

```bash
pip install faster-whisper          # TTS 검사용 (처음 한 번, 모델은 huggingface.co에서 받음)
python3 shorts/pension-return/build/tts_check.py    # 경고가 있으면 문장을 고치고 다시
shorts/pension-return/build/build_all.sh --render
```

## TTS 검사 (`build/tts_check.py`)

`gen_narration.py`가 실제로 영상에 넣는 클립(쉼 줄인 상태)을 줄마다 검사합니다.

- 글자: 한 글자로 끝나는 문장(「다리, 일.」), 줄 안의 마침표(긴 쉼), 숫자를 어떻게 읽는지(`SPOKEN`·숫자 읽기 결과를 표에 보여 줌)
- 소리: 0.35초가 넘는 쉼, 음절당 0.42초가 넘게 끄는 말(Whisper 단어 시각, 숫자·%는 읽는 음절 수로 계산), 자막 자리보다 1.12배 넘게 빨리 감아야 하는 줄
- 받아쓰기: 로컬 Whisper(small, CPU)로 다시 받아써 원문·읽는 말과 비교, 유사도 0.80 미만이면 경고 (Google Speech-to-Text는 이 키로 막혀 있음)
- 결과는 `tts_report.md`, 경고가 있으면 종료 코드 1
