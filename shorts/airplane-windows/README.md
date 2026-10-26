# 비행기 창문은 왜 둥글까? — YouTube Shorts (9편)

1분 30초 · 1080×1920 · 30fps 지식 쇼츠. 금융이 아닌 첫 주제이자 **설계도+팝아트 스타일**의 첫 편.

| 파일 | 내용 |
|---|---|
| `script.md` | 대본, 사실 확인 (코멧 사고, 여압, 금속 피로, 창문 숨구멍) |
| `storyboard.html` / `.png` | 12컷 콘티 (장면 그림·모션·내레이션) |
| `scenes/` | 장면별 벡터 원본(`.vectorcraft`)과 미리보기 PNG |
| `audio/narration-preview.mp3` | 내레이션 미리 듣기 (Google Cloud TTS `ko-KR-Chirp3-HD-Charon`, 1.2배속, 쉼표 쉼, 25문장) |
| `thumbnail/` | 썸네일 (1080×1920) |
| `youtube-metadata.md` | 제목·설명·태그 |
| `video/airplane-windows-shorts.mp4` | 완성 영상 (1:30, H.264 Main, −14.1 LUFS) |
| `video/airplane-windows.ecproj` | EffectCraft 프로젝트 (장면별 프리컴프 + Main) |

## 다시 만들기

```bash
shorts/airplane-windows/build/build_all.sh --render
```

## 8편에서 바꾼 점

- 스타일 전면 교체: 남색 설계도 모눈 배경 + 팝아트(굵은 검은 테두리, 폭발 별, 말풍선, 망점, 햇살 무늬). 자세한 규칙은 `shorts/WORKFLOW.md`의 「설계도+팝아트 스타일」
- 폰트: 제목 Black Han Sans, 감탄사·말풍선 Jua, 설명·자막 Do Hyeon (`shorts/fonts/`, `build_all.sh`가 설치)
- 자막 카드: 흰 박스 + 검은 8px 테두리 + 검은 그림자, 도현 58px
- AI 배경(RunPod) 없음: 배경은 `gen_scenes.py`의 `bg()`가 그림. `compose_bg.py` 삭제
- 진행 막대 노랑, 상단 고지 문구 없음
