# 적립식 vs 거치식 — YouTube Shorts (4편)

2분 30초 · 1080×1920 · 30fps 지식 쇼츠. 「복리의 마법」 · 「72의 법칙」 · 「4%의 법칙」 후속편.

| 파일 | 내용 |
|---|---|
| `script.md` | 대본, 숫자 검증표, 사실 확인 (뱅가드 2012·2023 연구) |
| `storyboard.html` / `.png` | 18컷 콘티 (장면 그림·모션·내레이션) |
| `scenes/` | 장면별 벡터 원본(`.vectorcraft`)과 미리보기 PNG (AI 배경 포함) |
| `build/ai_bg/` | 장면별 AI 배경 18장 (RunPod 서버리스 GPU, SDXL 30단계, 약 $0.015) |
| `audio/narration-preview.mp3` | 내레이션 미리 듣기 (Google Cloud TTS `ko-KR-Chirp3-HD-Charon`, 40문장) |
| `thumbnail/` | 썸네일 (1080×1920) |
| `youtube-metadata.md` | 제목·설명·태그 |
| `video/dca-vs-lump-shorts.mp4` | 완성 영상 |
| `video/dca-vs-lump.ecproj` | EffectCraft 프로젝트 (장면별 프리컴프 + Main) |

## 다시 만들기

```bash
shorts/dca-vs-lump/build/build_all.sh --render   # 렌더 약 11분
```

순서와 각 스크립트는 3편(`shorts/four-percent-rule/README.md`)과 같습니다. AI 배경을 다시 그리는 RunPod 순서도 3편 README에 있습니다.

## 3편에서 바꾼 점

- `verify_numbers.py`의 `SCENARIOS`(예시 주가 경로)로 S12–S14 막대와 대본 금액을 함께 계산
- 내레이션 읽기: "12달" → "열두 달"(`달`을 고유어 숫자 단위에 추가), "1만 원" → "만 원", "vs" → "대"
- 상단 고지 문구: "예시 계산 · 세금·수수료·기다리는 돈의 이자 미반영" (30–117초)
