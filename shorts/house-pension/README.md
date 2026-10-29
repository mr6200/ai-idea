# 주택연금, 집 한 채로 매달 얼마 받을까? — YouTube Shorts (16편)

1분 30초(+ 맨 앞 썸네일 1.5초 = 91.5초) · 1080×1920 · 30fps 지식 쇼츠. 노후 준비 시리즈 4편, 13~15편과 같은 **3D 클레이 AI + 미니멀 인포그래픽** 스타일.

| 파일 | 내용 |
|---|---|
| `script.md` | 대본, TTS 검사로 고친 문장, 사실 확인 (2026년 10월 기준) |
| `build/tts_report.md` | TTS 검사 결과 (줄마다 읽는 말·받아쓰기·길이·경고) |
| `storyboard.html` / `.png` | 12컷 콘티 (장면 그림·모션·내레이션) |
| `scenes/` | 장면별 벡터 원본(`.vectorcraft`)과 미리보기 PNG (AI 그림 포함) |
| `build/ai_bg/` | 장면별 AI 클레이 그림 12장 (RunPod 서버리스 SDXL 30단계, 장면마다 2장 그려 고름) |
| `audio/narration-preview.mp3` | 내레이션 미리 듣기 (Google Cloud TTS `ko-KR-Chirp3-HD-Charon`, 1.2배속, 쉼표 쉼, 25문장) |
| `thumbnail/` | 썸네일 (1080×1920) |
| `youtube-metadata.md` | 제목·설명·태그·챕터 |
| `video/house-pension-shorts.mp4` | 완성 영상 (1:30, H.264 Main, −14.6 LUFS) |
| `video/house-pension.ecproj` | EffectCraft 프로젝트 (장면별 프리컴프 + Main) |

## 다시 만들기

```bash
python3 shorts/house-pension/build/tts_check.py    # 경고가 있으면 문장을 고치고 다시
shorts/house-pension/build/build_all.sh --render
```

## 15편에서 바꾼 점

- 그림 도우미: 집 `house()`, 사람 `person()`, 집값 하락 vs 연금 일정 그래프 `price_vs_pension()`, 받은 돈 + 이자 막대 `debt_bars()`
- 영상 맨 앞에 썸네일을 1.5초 붙임 (사용자 요청): `build_all.sh`의 `INTRO=1.5`, 렌더 마무리 ffmpeg에서 무음으로 이어 붙임. 설명란 챕터 시간도 1.5초씩 늦춤
- TTS 검사기: 줄 안의 마침표는 실제 쉼이 0.35초를 넘을 때만 경고, 받아쓰기 유사도 기준 0.85
