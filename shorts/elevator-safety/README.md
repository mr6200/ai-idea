# 엘리베이터 줄이 끊어지면 추락할까? — YouTube Shorts (11편)

1분 30초 · 1080×1920 · 30fps 지식 쇼츠. **빈티지 포스터 + AI 동판화 배경** 스타일 첫 편 (사용자가 예시 A·E를 섞어 고름).

| 파일 | 내용 |
|---|---|
| `script.md` | 대본, 사실 확인 (오티스 시연 연도, 줄 가닥 수, 조속기·비상정지장치, 1945년 기록, 점프 퀴즈) |
| `storyboard.html` / `.png` | 12컷 콘티 (장면 그림·모션·내레이션) |
| `scenes/` | 장면별 벡터 원본(`.vectorcraft`)과 미리보기 PNG (AI 배경 포함) |
| `build/ai_bg/` | 장면별 AI 동판화 배경 12장 (RunPod 서버리스 GPU, SDXL 30단계) |
| `audio/narration-preview.mp3` | 내레이션 미리 듣기 (Google Cloud TTS `ko-KR-Chirp3-HD-Charon`, 1.2배속, 쉼표 쉼, 25문장) |
| `thumbnail/` | 썸네일 (1080×1920) |
| `youtube-metadata.md` | 제목·설명·태그 |
| `video/elevator-safety-shorts.mp4` | 완성 영상 (1:30, H.264 Main) |
| `video/elevator-safety.ecproj` | EffectCraft 프로젝트 (장면별 프리컴프 + Main) |

## 다시 만들기

```bash
shorts/elevator-safety/build/build_all.sh --render
```

AI 배경을 다시 그리려면 `build/gen_backgrounds.py`의 프롬프트를 고치고 `ai_bg/Sxx.png`를 지운 뒤 `gen_backgrounds_runpod.py`를 돌립니다 (순서는 `shorts/four-percent-rule/README.md`, 쓰고 나면 엔드포인트·템플릿 삭제).

## 스타일 (빈티지 포스터 + AI 동판화)

- 배경: AI 동판화(`ai_bg/`)를 `compose_bg.py`가 세피아 한 톤(#2b1d14 → #f3e7cc)으로 바꾸고 살짝 흐리게 깔고, 그 위에 반투명 누런 종이(#efe2c4, 62%) + 위쪽 그라데이션 + 갈색 비네트 + 이중 테두리
- 상단 라벨: 빨간 리본(#a8281e) `ribbon()`
- 글꼴: 나눔명조 ExtraBold(제목, 종이색 외곽선) / Bold(설명·자막) — `shorts/fonts/`
- 그림: 잉크 선(#2b1d14) + 세로 해칭 `hatch()`, 겨자색(#c9912e) 강조, 빨간 도장 `seal()`, 이중 테두리 종이 카드 `card()`·`note()`, 두 줄 구분선 `rule()`
- 자막 카드: 종이색 상자 + 이중 잉크 테두리, 나눔명조 Bold 54px
- 진행 막대 빨강, Main 배경색 종이색
- 그림 도우미: 엘리베이터 칸 `car()`, 톱니 레일 `rails()`, 끊어지는 줄 `snap()`, 실크해트 신사 `gentleman()`, 걸쇠 그림 `pawl_diagram()`, 도르래 `sheave()`, 쐐기 `wedge_gear()`, 빌딩 `building()`, 폭격기 `bomber()`
