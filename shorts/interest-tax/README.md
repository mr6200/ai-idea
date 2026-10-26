# 이자에 붙는 세금 — YouTube Shorts (7편)

1분 30초 · 1080×1920 · 30fps 지식 쇼츠. 6편과 같은 1분 30초 규격.

| 파일 | 내용 |
|---|---|
| `script.md` | 대본, 숫자 검증표, 사실 확인 (2026년 10월 세법 기준) |
| `storyboard.html` / `.png` | 12컷 콘티 (장면 그림·모션·내레이션) |
| `scenes/` | 장면별 벡터 원본(`.vectorcraft`)과 미리보기 PNG (AI 배경 포함) |
| `build/ai_bg/` | 장면별 AI 배경 12장 (RunPod 서버리스 GPU, SDXL 30단계) |
| `audio/narration-preview.mp3` | 내레이션 미리 듣기 (Google Cloud TTS `ko-KR-Chirp3-HD-Charon`, 1.2배속, 쉼표 쉼, 26문장) |
| `thumbnail/` | 썸네일 (1080×1920) |
| `youtube-metadata.md` | 제목·설명·태그 |
| `video/interest-tax-shorts.mp4` | 완성 영상 (1:30, H.264 Main, −14.6 LUFS) |
| `video/interest-tax.ecproj` | EffectCraft 프로젝트 (장면별 프리컴프 + Main) |

## 다시 만들기

```bash
shorts/interest-tax/build/build_all.sh --render
```

순서와 각 스크립트는 3편(`shorts/four-percent-rule/README.md`)과 같습니다.

## 6편에서 바꾼 점

- 내레이션 읽기: "ISA" → "아이에스에이"
- 상단 고지 문구: "2026년 10월 세법 기준 · 가입 전 확인 필수" (5–70초)
- 세법은 자주 바뀌므로 다시 렌더하기 전에 `script.md`의 사실 확인 표를 최신 기준으로 다시 확인
