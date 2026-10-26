# 예금 vs 적금 — YouTube Shorts (5편)

2분 30초 · 1080×1920 · 30fps 지식 쇼츠. 은행 예·적금을 다루는 첫 편.

| 파일 | 내용 |
|---|---|
| `script.md` | 대본, 숫자 검증표, 사실 확인 (적금 이자 계산법, 이자소득세 15.4%, 예금자보호 1억 원) |
| `storyboard.html` / `.png` | 18컷 콘티 (장면 그림·모션·내레이션) |
| `scenes/` | 장면별 벡터 원본(`.vectorcraft`)과 미리보기 PNG (AI 배경 포함) |
| `build/ai_bg/` | 장면별 AI 배경 18장 (RunPod 서버리스 GPU, SDXL 30단계) |
| `audio/narration-preview.mp3` | 내레이션 미리 듣기 (Google Cloud TTS `ko-KR-Chirp3-HD-Charon`, 40문장) |
| `thumbnail/` | 썸네일 (1080×1920) |
| `youtube-metadata.md` | 제목·설명·태그 |
| `video/deposit-vs-savings-shorts.mp4` | 완성 영상 (2:30, H.264 Main, −14.0 LUFS) |
| `video/deposit-vs-savings.ecproj` | EffectCraft 프로젝트 (장면별 프리컴프 + Main) |

## 다시 만들기

```bash
shorts/deposit-vs-savings/build/build_all.sh --render   # 렌더 약 11분
```

순서와 각 스크립트는 3편(`shorts/four-percent-rule/README.md`)과 같습니다. AI 배경을 다시 그리는 RunPod 순서도 3편 README에 있습니다.

## 4편에서 바꾼 점

- `verify_numbers.py`의 `deposit_interest` · `savings_interest` · `after_tax`를 `gen_scenes.py`가 그대로 불러 화면 숫자를 그림
- 내레이션 읽기: "6.5달치" → "6.5개월치", 줄바꿈 뒤 "= " → 쉼표
- 상단 고지 문구: "예시 금리 · 1년 만기 단리 기준" (0–117초)
