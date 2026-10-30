# (폐기) 편의점 1+1, 정말 이득일까? (60초 · 3D 클레이 AI + 인포그래픽)

- **사용자가 폐기** (2026-10-30, 흥미가 적을 것 같다는 이유). 19편 번호는 새 주제에 다시 씀. 빌드 · 검사 기록은 참고용으로 남김
- 60초 + 맨 앞 썸네일 1초, 8장면, TTS `ko-KR-Chirp3-HD-Charon` 1.2배속
- 18편 `shorts/lotto-winners/`를 틀로 씀 (같은 규격 · 스타일 · Seedream 클레이 그림)
- 대본 · 사실 확인 · TTS 검사: `script.md` / 업로드 정보: `youtube-metadata.md` / 콘티: `storyboard.html` · `.png`
- 완성 영상: `video/convenience-deals-shorts.mp4`, 썸네일: `thumbnail/thumbnail.png`

## 이번 편에서 배운 것

- **「1+1」 읽기:** TTS가 「일+1」로 읽음 → `gen_narration.py`의 `SPOKEN`에 「원 플러스 원」 · 「투 플러스 원」 추가. 뒤에 붙는 조사도 읽는 말에 맞춤 (「2+1**으로**」)
- **가격 숫자는 medium으로 꼭 다시 들어 보기:** 「4,750원 참기름을」은 medium이 「4790원」으로 받아씀 → 「4,750원**에서**」로 바꾸니 정확. 「공정위는」 → 「공정인은」도 「공정거래위원회가」로 해결
- **AI 그림 속 글자:** Seedream이 병 라벨에 한자를 그림 → 프롬프트에 "blank label"을 넣고 그 장면만 시드를 바꿔 다시 그림 (`gen_backgrounds_seedream.py S06 --seed 1`)
- 자막이 길면 3줄로 나눔 (카드 높이가 자동으로 늘어남)

## RunPod 사용액

Seedream 4.0 그림 9장 (8장 + S06 다시 그림) = 약 $0.24. 잔액은 완성 보고에 적음.

## 다시 만들기

```
cd build && ./build_all.sh --render
```
