# 복리의 마법 — YouTube Shorts

2분 30초 · 1080×1920 · 30fps 지식 쇼츠.

| 파일 | 내용 |
|---|---|
| `compound-interest-script.md` | 대본 |
| `compound-interest-storyboard.html` / `.png` | 18컷 콘티 |
| `scenes/` | 씬별 벡터 원본(`.vectorcraft`)과 미리보기 PNG |
| `video/compound-interest-shorts.mp4` | 완성 영상 |
| `video/compound-interest.ecproj` | EffectCraft 프로젝트 (씬별 프리컴프 + Main) |
| `build/` | 재생성 파이프라인 |

## 다시 만들기

```bash
shorts/build/build_all.sh --render
```

1. `gen_scenes.py` — S04–S18의 애니메이션 파트를 SVG로 작성
2. `vectorcraft-cli convert` — 파트를 1080×1920 투명 PNG 레이어로, 씬을 `.vectorcraft`로 변환
3. `export_s01_s03.py` — VectorCraft에서 직접 그린 S01–S03을 레이어별로 분리
4. `timeline.py` — 씬 타이밍·애니메이션·자막 큐를 `manifest.json`으로 합침
5. `gen_subtitles.py` — 자막 카드를 VectorCraft로 렌더링
6. `gen_narration.py` — 자막 문장마다 Google Cloud TTS(`ko-KR-Chirp3-HD-Charon`)로 내레이션 생성, 자막 시간에 배치 (`GOOGLE_TTS_API_KEY` 필요, `tts/`에 캐시)
7. `gen_audio.py` — BGM(로파이 마림바)과 효과음을 numpy로 합성하고 내레이션 구간에서 BGM을 낮춤(덕킹)
8. `gen_effectcraft.py` → `build.jsx` — EffectCraft 프로젝트를 스크립트로 조립
9. EffectCraft 렌더 → ffmpeg로 음량 정규화(−14 LUFS)·faststart

## 알아둘 점

- 내레이션은 자막 문장을 그대로 읽습니다. 목소리를 바꾸려면 `gen_narration.py`의 `VOICE`를 바꾸고 다시 빌드하세요. 오디오 파일(`audio.wav`, `narration.wav`, `tts/`)은 git에서 제외되며 빌드 때 다시 만들어집니다.
- 글꼴은 WenQuanYi Zen Hei입니다. Pretendard 등으로 바꾸려면 `gen_scenes.py`의 `FONT`와 `gen_effectcraft.py`의 `setText` 기본값을 바꾸고 다시 빌드하세요.
- 캐릭터 A·B는 OpenAI 이미지 모델을 쓸 수 없어 벡터로 직접 그렸습니다.
- S13의 버핏 관련 문구는 공개 전에 출처를 확인하세요.
