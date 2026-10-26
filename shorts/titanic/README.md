# 타이타닉은 왜 가라앉았을까? — YouTube Shorts (12편)

**1분 10초** · 1080×1920 · 30fps 지식 쇼츠. 빈티지 포스터 + AI 동판화 스타일 두 번째 편, 「RunPod으로 영상미 있게」(사용자 요청).

| 파일 | 내용 |
|---|---|
| `script.md` | 대본, 사실 확인 (방수 칸, 빙산, 구명보트, 사망자, 1914년 규칙, 1985년 발견) |
| `storyboard.html` / `.png` | 10컷 콘티 (장면 그림·모션·내레이션) |
| `scenes/` | 장면별 벡터 원본(`.vectorcraft`)과 미리보기 PNG (AI 그림 포함) |
| `build/ai_bg/` | 장면별 AI 동판화 10장 (RunPod 서버리스 SDXL 30단계, 장면마다 2장 그려 고름) |
| `audio/narration-preview.mp3` | 내레이션 미리 듣기 (Google Cloud TTS `ko-KR-Chirp3-HD-Charon`, 1.2배속, 쉼표 쉼, 21문장) |
| `thumbnail/` | 썸네일 (1080×1920) |
| `youtube-metadata.md` | 제목·설명·태그 |
| `video/titanic-shorts.mp4` | 완성 영상 (1:10, H.264 Main, −13.8 LUFS) |
| `video/titanic.ecproj` | EffectCraft 프로젝트 (장면별 프리컴프 + Main) |

## 다시 만들기

```bash
shorts/titanic/build/build_all.sh --render
```

AI 그림을 다시 그리려면 `build/gen_backgrounds.py`의 프롬프트를 고치고 `ai_bg/Sxx.png`를 지운 뒤 `gen_backgrounds_runpod.py`를 돌립니다 (순서는 `shorts/four-percent-rule/README.md`, 쓰고 나면 엔드포인트·템플릿 삭제).

## 11편에서 바꾼 점 (영상미)

- AI 그림을 장면의 맨 아래 **따로 움직이는 층**(`ai`)으로 분리: `compose_bg.py`가 세피아로 바꿔 `parts/Sxx/ai.png`에 쓰고, `gen_effectcraft.py`의 `kenburns` 동작이 장면 내내 천천히 확대·축소·이동 (장면마다 `ai(dur, z, pan)`으로 방향을 다르게)
- 종이 덧칠을 62% → 34%로 옅게 (위쪽은 제목이 읽히게 그라데이션 85%), 그림·글은 종이 카드 위에
- 옛날 필름 효과 `film.png` (비네트·입자·긁힘)를 모든 장면 위, 자막 아래에 깔고 불투명도가 살짝 깜박임
- AI 그림은 장면마다 2장(씨앗 100+n, 200+n) 그려 더 나은 쪽 선택
- 배경음악을 단조 발라드(Am–F–C–E, 76 BPM)로, 하이햇 빼고 킥 줄임
- 길이 70초: `timeline.py` `DURATION = 70`, `gen_audio.py` `DUR = 70` (마지막 마디 여유 버퍼), 퀴즈·클릭 효과음 시각 이동
- 그림 도우미: 여객선 옆모습 `ship()`(부러진 모습 포함), 16칸 단면 `compartments()`(물 차오름·기울기), 빙산 `iceberg()`, 구명보트 `lifeboat()`, 막대 `bar()`, 바다 밑 잔해 `wreck()`
- 내레이션 읽기: "2시간 40분" → "두 시간 사십 분", "16개의" → "열여섯 개의", "20척" → "스무 척", "4천 m" → "사천 미터"
