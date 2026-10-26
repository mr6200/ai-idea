# 60세 퇴직, 연금은 65세? — YouTube Shorts (13편)

1분 30초 · 1080×1920 · 30fps 지식 쇼츠. **3D 클레이 AI + 미니멀 인포그래픽** 스타일 첫 편 (사용자가 예시 B·D를 섞어 고름).

| 파일 | 내용 |
|---|---|
| `script.md` | 대본, 숫자 검증, 사실 확인 (2026년 10월 기준: 정년, 수급 나이, 조기·연기연금, IRP, 주택연금) |
| `storyboard.html` / `.png` | 12컷 콘티 (장면 그림·모션·내레이션) |
| `scenes/` | 장면별 벡터 원본(`.vectorcraft`)과 미리보기 PNG (AI 그림 포함) |
| `build/ai_bg/` | 장면별 AI 클레이 그림 12장 (RunPod 서버리스 SDXL 30단계, 장면마다 2장 그려 고름) |
| `audio/narration-preview.mp3` | 내레이션 미리 듣기 (Google Cloud TTS `ko-KR-Chirp3-HD-Charon`, 1.2배속, 쉼표 쉼, 25문장) |
| `thumbnail/` | 썸네일 (1080×1920) |
| `youtube-metadata.md` | 제목·설명·태그 |
| `video/retirement-gap-shorts.mp4` | 완성 영상 (1:30, H.264 Main) |
| `video/retirement-gap.ecproj` | EffectCraft 프로젝트 (장면별 프리컴프 + Main) |

## 다시 만들기

```bash
shorts/retirement-gap/build/build_all.sh --render
```

연금·정년·세법은 자주 바뀌므로 다시 렌더하기 전에 `script.md`의 사실 확인 표를 최신 기준으로 다시 확인합니다. AI 그림을 다시 그리려면 `build/gen_backgrounds.py`의 프롬프트를 고치고 `ai_bg/Sxx.png`를 지운 뒤 `gen_backgrounds_runpod.py`를 돌립니다 (쓰고 나면 엔드포인트·템플릿 삭제).

## 스타일 (3D 클레이 AI + 인포그래픽)

- 바닥 층: RunPod 클레이 그림(색 그대로)을 12편과 같은 `kenburns`로 천천히 확대·이동 (`ai(dur, z, pan)`)
- 위 청록 그라데이션(#2f5d6a, 85%)에 제목 Jua(흰색/노랑 #ffd166, 자주색 #3a2a4a 외곽선), 아래 옅은 그라데이션
- 숫자는 미색 카드(#f5f3ee, 둥근 모서리, 그림자) `card()` 위에: 큰 숫자 Black Han Sans `num()`, 청록 #1f7a6d·빨강 #e4572e, 라벨 칩 `tag()`, 알약 `pill()`
- 자막 카드: 흰 둥근 상자 + 자주색 6px 테두리, 도현 58px
- 필름 효과 대신 옅은 청록 비네트 `film.png`, 진행 막대 청록
- 그림 도우미: 60→65 타임라인 `timeline()`, 출생연도별 수급 나이 표 `age_table()`, 네 기둥 다리 `bridge()`, 동전 `coins()`
- 효과음: 「1억 8천만 원」·주택연금 동전 장면에 동전 소리 (`COIN_PARTS`)
