# 국민연금, 일찍 받을까 늦게 받을까? — YouTube Shorts (14편)

1분 30초 · 1080×1920 · 30fps 지식 쇼츠. 13편 「60세 퇴직, 연금은 65세?」의 후속편, 같은 **3D 클레이 AI + 미니멀 인포그래픽** 스타일.

| 파일 | 내용 |
|---|---|
| `script.md` | 대본, 숫자 검증(역전 나이 계산), 사실 확인 (2026년 10월 기준) |
| `storyboard.html` / `.png` | 12컷 콘티 (장면 그림·모션·내레이션) |
| `scenes/` | 장면별 벡터 원본(`.vectorcraft`)과 미리보기 PNG (AI 그림 포함) |
| `build/ai_bg/` | 장면별 AI 클레이 그림 12장 (RunPod 서버리스 SDXL 30단계, 장면마다 2장 그려 고름) |
| `audio/narration-preview.mp3` | 내레이션 미리 듣기 (Google Cloud TTS `ko-KR-Chirp3-HD-Charon`, 1.2배속, 쉼표 쉼, 25문장) |
| `thumbnail/` | 썸네일 (1080×1920) |
| `youtube-metadata.md` | 제목·설명·태그·챕터 |
| `video/pension-timing-shorts.mp4` | 완성 영상 (1:30, H.264 Main) |
| `video/pension-timing.ecproj` | EffectCraft 프로젝트 (장면별 프리컴프 + Main) |

## 다시 만들기

```bash
shorts/pension-timing/build/build_all.sh --render
```

연금·건보료 기준은 바뀔 수 있으므로 다시 렌더하기 전에 `script.md`의 사실 확인 표를 최신 기준으로 다시 확인합니다.

## 13편에서 바꾼 점

- 누적 수령액 그래프 도우미: `chart_axes()`(가로 60~90세, 세로 받은 돈 합계), `chart_line(plan)`(60세 70% · 65세 100% · 70세 136%), `legend(*plans)`, 역전 지점 `cross(age, total, label, col, dx)`
- 월 수령액 막대 `amounts()`, 13편 전용 도우미(`timeline`, `age_table`, `bridge`, `coins`)는 뺌
- 내레이션 읽기: "정답은 X!" → "정답은, 아니다!", "2,000만 원" → "이천만 원", "21.7년" → "이십일 점 칠 년"
