# 은행은 언제 어떻게 처음 생겼을까? — YouTube Shorts (6편)

2분 · 1080×1920 · 30fps 지식 쇼츠. 6편부터 규격(120초, TTS 1.2배속)으로 만든 첫 편.

| 파일 | 내용 |
|---|---|
| `script.md` | 대본, 사실 확인 표 (메소포타미아 → 그리스 → 이탈리아 → 런던) |
| `storyboard.html` / `.png` | 18컷 콘티 (장면 그림·모션·내레이션) |
| `scenes/` | 장면별 벡터 원본(`.vectorcraft`)과 미리보기 PNG (AI 배경 포함) |
| `build/ai_bg/` | 장면별 AI 배경 18장 (RunPod 서버리스 GPU, SDXL 30단계) |
| `audio/narration-preview.mp3` | 내레이션 미리 듣기 (Google Cloud TTS `ko-KR-Chirp3-HD-Charon`, 1.2배속, 36문장) |
| `thumbnail/` | 썸네일 (1080×1920) |
| `youtube-metadata.md` | 제목·설명·태그 |
| `video/bank-origins-shorts.mp4` | 완성 영상 (2:00, H.264 Main, −14.4 LUFS) |
| `video/bank-origins.ecproj` | EffectCraft 프로젝트 (장면별 프리컴프 + Main) |

## 다시 만들기

```bash
shorts/bank-origins/build/build_all.sh --render
```

순서와 각 스크립트는 3편(`shorts/four-percent-rule/README.md`)과 같습니다. 숫자 계산이 없는 편이라 `verify_numbers.py`는 없습니다.

## 5편에서 바꾼 점

- 길이 120초: `timeline.py`의 `DURATION = 120`, `gen_audio.py`의 `DUR = 120.0`, 장면 18개를 4~10초로 다시 배분
- TTS 속도: `gen_narration.py`의 `RATE = 1.2`
- 상단 고지 문구 없음 (계산·금리가 나오지 않는 역사 편)
- 그림 도우미 추가: 지구라트, 점토판, 곡식 자루, 탁자, 그리스 기둥, 금괴, 보관증
