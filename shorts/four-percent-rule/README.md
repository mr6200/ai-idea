# 4%의 법칙 — YouTube Shorts (3편, 제작 중)

2분 30초 · 1080×1920 · 30fps 지식 쇼츠. 「복리의 마법」(`shorts/`) · 「72의 법칙」(`shorts/rule-of-72/`) 후속편.

| 파일 | 내용 | 상태 |
|---|---|---|
| `script.md` | 대본, 숫자 검증표, 사실 확인 출처 | 완료 |
| `storyboard.html` / `.png` | 18컷 콘티 (장면 그림·모션·내레이션) | 완료 |
| `scenes/` | 장면별 벡터 원본(`.vectorcraft`)과 미리보기 PNG | 완료 (AI 배경 포함) |
| `audio/narration-preview.mp3` | 내레이션 미리 듣기 (Google Cloud TTS `ko-KR-Chirp3-HD-Charon`, 42문장, 2:30) | 완료 |
| `build/ai_bg/` | 장면별 AI 배경 18장 (RunPod 서버리스 GPU, SDXL 30단계) | 완료 |
| 썸네일·자막 카드·BGM·EffectCraft 조립·렌더·메타데이터 | 2편 스크립트를 이 편에 맞게 고쳐야 함 | 남음 |

## 다시 만들기 (지금까지 된 단계)

```bash
shorts/four-percent-rule/build/build_all.sh
```

1. `verify_numbers.py` — 대본 숫자 재계산 (S12 순서 위험 그래프도 이 값을 그대로 씀)
2. `gen_scenes.py` → `vectorcraft-cli convert` — 18장면 부품 PNG와 장면 원본
3. `compose_bg.py` — `build/ai_bg/`가 있으면 배경을 깔고, 없으면 크림 바탕
4. `timeline.py` — 자막 큐 42개 → `manifest.json`
5. `gen_storyboard.py` — 콘티
6. `gen_narration.py` — 내레이션 (`GOOGLE_TTS_API_KEY`, `tts/`에 캐시) → `audio/narration-preview.mp3`

## 2편에서 바꾼 점

- 내레이션 읽기: `×` → "곱하기", `3~3.5%` → "3에서 3.5%", `·` → 띄어 읽기
- S12 그래프는 `verify_numbers.py`의 시뮬레이션 값으로 그림 (9억, 첫해 3,600만 원, 매년 2.5% 증액, 같은 수익률을 정순·역순으로)
- 공개 전 확인: 벤겐(1994)·트리니티 연구(1998)의 수치는 `script.md`의 출처 표로 다시 확인

## AI 배경 (RunPod, `build/gen_backgrounds_runpod.py`)

- 프롬프트는 `gen_backgrounds.py`의 `SCENES`를 그대로 쓰고, GPU에서는 SDXL 1.0을 30단계·CFG 6으로 돌려 금지어(글자·워터마크)가 적용됨
- 이 환경에서는 Pod 웹 주소(`*.proxy.runpod.net`)가 막혀 있어 **서버리스 엔드포인트**를 씀. 결과 그림은 작업 응답(base64)으로 받음
- 쓰는 법 (`RUNPOD_API_KEY` 필요):
  1. 템플릿: `POST https://rest.runpod.io/v1/templates` `{"name":"shorts-bg-comfyui-sdxl","imageName":"runpod/worker-comfyui:5.10.0-sdxl","isServerless":true,"containerDiskInGb":30}`
  2. 엔드포인트: `POST https://rest.runpod.io/v1/endpoints` `{"templateId":"<id>","gpuTypeIds":["NVIDIA GeForce RTX 4090","NVIDIA RTX A5000","NVIDIA L4"],"workersMin":0,"workersMax":1,"idleTimeout":10}`
  3. `RUNPOD_ENDPOINT_ID=<id> python3 gen_backgrounds_runpod.py` (첫 장 약 40초, 이후 장당 약 11초)
  4. 끝나면 `DELETE /v1/endpoints/<id>`, `DELETE /v1/templates/<id>`로 지움
- 3편 18장 비용: 약 $0.03
