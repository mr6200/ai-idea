# 무이자 할부, 카드사는 손해일까? — YouTube Shorts (8편)

1분 30초 · 1080×1920 · 30fps 지식 쇼츠. 조회수 회복을 위해 생활 밀착형·질문형 주제로 바꾼 첫 편.

| 파일 | 내용 |
|---|---|
| `script.md` | 대본, 숫자 검증표, 사실 확인 (카드사 수익 구조, 2026년 10월 기준) |
| `storyboard.html` / `.png` | 12컷 콘티 (장면 그림·모션·내레이션) |
| `scenes/` | 장면별 벡터 원본(`.vectorcraft`)과 미리보기 PNG (AI 배경 포함) |
| `build/ai_bg/` | 장면별 AI 배경 12장 (RunPod 서버리스 GPU, SDXL 30단계) |
| `audio/narration-preview.mp3` | 내레이션 미리 듣기 (Google Cloud TTS `ko-KR-Chirp3-HD-Charon`, 1.2배속, 쉼표 쉼, 25문장) |
| `thumbnail/` | 썸네일 (1080×1920) |
| `youtube-metadata.md` | 제목·설명·태그 |
| `video/card-installments-shorts.mp4` | 완성 영상 |
| `video/card-installments.ecproj` | EffectCraft 프로젝트 (장면별 프리컴프 + Main) |

## 다시 만들기

```bash
shorts/card-installments/build/build_all.sh --render
```

순서와 각 스크립트는 3편(`shorts/four-percent-rule/README.md`)과 같습니다.

## 7편에서 바꾼 점

- 내레이션 읽기: "이자는 0원이에요" → "이자는 한 푼도 없어요" ("영원"으로 들리지 않게), `곳`을 고유어 숫자 단위에 추가 ("7곳" → "일곱 곳"), "2~3개월" → "두세 달"
- 상단 고지 문구: "2026년 10월 기준 · 카드사·가맹점마다 다름" (40–70초)
- 그림 도우미 추가: 신용카드, 카드사 건물, 가게
