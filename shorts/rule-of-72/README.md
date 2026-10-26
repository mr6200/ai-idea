# 72의 법칙 — YouTube Shorts

2분 30초 · 1080×1920 · 30fps 지식 쇼츠. 「복리의 마법」(`shorts/`) 후속편.

| 파일 | 내용 |
|---|---|
| `script.md` | 대본과 숫자 검증표 |
| `storyboard.html` / `.png` | 18컷 콘티 (장면 그림·모션·내레이션) |
| `scenes/` | 장면별 벡터 원본(`.vectorcraft`)과 미리보기 PNG |
| `thumbnail/` | 썸네일 (1080×1920) |
| `youtube-metadata.md` | 제목·설명·태그 |
| `video/rule-of-72-shorts.mp4` | 완성 영상 |
| `video/rule-of-72.ecproj` | EffectCraft 프로젝트 (장면별 프리컴프 + Main) |
| `build/` | 다시 만드는 파이프라인 |

## 다시 만들기

```bash
shorts/rule-of-72/build/build_all.sh --render
```

1편과 같은 파이프라인이지만, 이번에는 S01–S18 모두 `gen_scenes.py` 코드로 그립니다
(MCP로 직접 그린 장면이 없어서 `export_s01_s03.py` 단계가 없음).

1. `gen_scenes.py` — 18개 장면의 부품 SVG + `manifest_scenes.json`
2. `vectorcraft-cli convert` — 부품을 1080×1920 투명 PNG 레이어로, 장면을 `.vectorcraft`로
3. `compose_bg.py` — `build/ai_bg/`의 AI 배경을 반투명 크림 바탕 아래에 깔아 `parts/Sxx/bg.png`와 장면 미리보기를 만듦
4. `timeline.py` — 자막 큐 38개를 합쳐 `manifest.json`
5. `gen_storyboard.py`, `gen_thumbnail.py` — 콘티와 썸네일
6. `gen_subtitles.py` — 자막 카드
7. `gen_narration.py` — Google Cloud TTS 내레이션 (`GOOGLE_TTS_API_KEY`, `tts/`에 캐시)
8. `gen_audio.py` — BGM·효과음 합성, 내레이션 구간 덕킹
9. `gen_effectcraft.py` → `build.jsx` → EffectCraft 프로젝트, 렌더, ffmpeg 정규화

## 1편에서 바꾼 점

- 내레이션 숫자 읽기: `1, 2, 3`처럼 쉼표로 나열한 숫자를 하나로 붙여 읽지 않도록 정규식 수정,
  `÷` → "나누기", `=` → 쉼표
- EffectCraft 카운터: S03 스톱워치 아래 `0.0초 → 3.0초`
- 상단 고지 문구: "연 1회 복리 기준 · 세금·수수료 미반영" (5–128초)

## AI 배경 (`build/gen_backgrounds.py`)

- 모델: SDXL 1.0 + SDXL-Lightning 4단계 LoRA (둘 다 CreativeML Open RAIL++-M, 상업 이용 가능)
- 장면마다 프롬프트 1개, 시드 고정(100 + 장면 번호). 만든 그림은 `build/ai_bg/`에 커밋해 두므로 보통 빌드에서는 다시 그리지 않음
- 다시 그리려면 torch·diffusers·transformers·accelerate·peft가 있는 가상환경에서
  `python gen_backgrounds.py S05` (해당 `ai_bg/S05.png`를 먼저 지움). CPU에서 장당 약 5분, 메모리 약 11GB(bfloat16)
- 네트워크 허용 필요: `huggingface.co`, `*.hf.co` (모델 파일은 hf.co CDN에서 내려받음)
- 그림에는 글자를 넣지 않음 — 한글·숫자는 지금처럼 벡터 레이어로 얹음
- 배경이 내용보다 튀지 않도록 `gen_scenes.py`의 `BG_WASH`(크림 덮개 불투명도)와 `compose_bg.py`의 블러로 조절
