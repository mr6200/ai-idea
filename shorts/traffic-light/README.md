# 신호등은 왜 빨강·노랑·초록일까? — YouTube Shorts (16편)

1분 30초(+ 맨 앞 썸네일 1.5초) · 1080×1920 · 30fps 지식 쇼츠. **빈티지 포스터 + AI 동판화** 스타일 (12편 타이타닉과 같은 켄 번즈·옛날 필름 효과). 16편 「주택연금」을 폐기하고 새로 만든 16편.

| 파일 | 내용 |
|---|---|
| `script.md` | 대본, TTS 검사로 고친 문장, 사실 확인 |
| `build/tts_report.md` | TTS 검사 결과 |
| `storyboard.html` / `.png` | 12컷 콘티 |
| `scenes/` | 장면별 벡터 원본(`.vectorcraft`)과 미리보기 PNG (AI 그림 포함) |
| `build/ai_bg/` | 장면별 AI 동판화 12장 (RunPod 서버리스 SDXL 30단계, 장면마다 2장 그려 고름) |
| `audio/narration-preview.mp3` | 내레이션 미리 듣기 (`ko-KR-Chirp3-HD-Charon`, 1.2배속, 25문장) |
| `thumbnail/` | 썸네일 (1080×1920) |
| `youtube-metadata.md` | 제목·설명·태그·챕터 |
| `video/traffic-light-shorts.mp4` | 완성 영상 (썸네일 1.5초 + 1:30, H.264 Main, −14.6 LUFS) |
| `video/traffic-light.ecproj` | EffectCraft 프로젝트 |

## 다시 만들기

```bash
python3 shorts/traffic-light/build/tts_check.py
shorts/traffic-light/build/build_all.sh --render
```

## 만든 방식

- 12편(`shorts/titanic/build`)의 빈티지 장면 도우미·`compose_bg.py`(세피아 + 필름)·`gen_effectcraft.py`(켄 번즈 + 필름 깜박임)·자막·콘티를 쓰고, 16편 주택연금(`shorts/house-pension/build`)의 `build_all.sh`(썸네일 인트로)·`gen_audio.py`(90초)·`tts_check.py`를 합침
- 그림 도우미: 신호등 `signal()`(세로·가로, 켜진 색 선택), 등불 `lamp()`, 1868년 세마포어 신호 `semaphore()`, 철도 등불 `lantern()`(빨간 유리 빠진 모습 포함), 안개 `fog()`, 별 `star()`
