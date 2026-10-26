# 은행은 어떻게 돈을 벌까? — YouTube Shorts (6편)

1분 30초 · 1080×1920 · 30fps 지식 쇼츠. 시청 지속률 비교를 위한 1분 30초 시험 편 (5편 「은행의 탄생」은 2분).

| 파일 | 내용 |
|---|---|
| `script.md` | 대본, 숫자 검증표, 사실 확인 (2025년 국내 은행 실적) |
| `storyboard.html` / `.png` | 12컷 콘티 (장면 그림·모션·내레이션) |
| `scenes/` | 장면별 벡터 원본(`.vectorcraft`)과 미리보기 PNG (AI 배경 포함) |
| `build/ai_bg/` | 장면별 AI 배경 12장 (RunPod 서버리스 GPU, SDXL 30단계) |
| `audio/narration-preview.mp3` | 내레이션 미리 듣기 (Google Cloud TTS `ko-KR-Chirp3-HD-Charon`, 1.2배속, 쉼표 쉼, 25문장) |
| `thumbnail/` | 썸네일 (1080×1920) |
| `youtube-metadata.md` | 제목·설명·태그 |
| `video/how-banks-earn-shorts.mp4` | 완성 영상 |
| `video/how-banks-earn.ecproj` | EffectCraft 프로젝트 (장면별 프리컴프 + Main) |

## 다시 만들기

```bash
shorts/how-banks-earn/build/build_all.sh --render
```

순서와 각 스크립트는 3편(`shorts/four-percent-rule/README.md`)과 같습니다.

## 5편(은행의 탄생)에서 바꾼 점

- 길이 90초: `timeline.py`의 `DURATION = 90`, `gen_audio.py`의 `DUR = 90.0`, 장면 12개, 자막 25문장
- `verify_numbers.py`에 예시 금리와 2025년 실적 수치를 두고 `gen_scenes.py`가 불러 씀
- 상단 고지 문구: "예시 금리 · 비용·세금 제외" (5–32초)
