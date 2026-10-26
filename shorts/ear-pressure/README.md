# 비행기 타면 귀가 먹먹한 이유 — YouTube Shorts (10편)

1분 30초 · 1080×1920 · 30fps 지식 쇼츠. 설계도+팝아트 스타일 두 번째 편, 9편(비행기 창문)과 이어지는 기압 이야기.

| 파일 | 내용 |
|---|---|
| `script.md` | 대본, 사실 확인 (기내 기압, 이관, 이륙·착륙 차이, 아기, 수면) |
| `storyboard.html` / `.png` | 12컷 콘티 (장면 그림·모션·내레이션) |
| `scenes/` | 장면별 벡터 원본(`.vectorcraft`)과 미리보기 PNG |
| `audio/narration-preview.mp3` | 내레이션 미리 듣기 (Google Cloud TTS `ko-KR-Chirp3-HD-Charon`, 1.2배속, 쉼표 쉼, 25문장) |
| `thumbnail/` | 썸네일 (1080×1920) |
| `youtube-metadata.md` | 제목·설명·태그 |
| `video/ear-pressure-shorts.mp4` | 완성 영상 (1:30, H.264 Main) |
| `video/ear-pressure.ecproj` | EffectCraft 프로젝트 (장면별 프리컴프 + Main) |

## 다시 만들기

```bash
shorts/ear-pressure/build/build_all.sh --render
```

## 9편에서 바꾼 점

- 오른쪽 아래 도면 표제란(「DWG. 0NN · 지식 쇼츠」) 삭제 (사용자 요청)
- 그림 도우미 추가: 귀 단면 설계도 `ear()` (고막 밀림·이관 열림/닫힘), 팝아트 귀 `ear_icon()`, 비행기 `plane_icon()`
- 내레이션 읽기: "정답은 O!" → "정답은, 그렇다!", "2,400m" → "2,400미터", "이착륙" → "이륙과 착륙"
