# 세계의 미스터리 2화 · 이스터섬 모아이 석상의 비밀 (58초 · 실사 다큐)

- 본편 58초 + 맨 앞 썸네일 1.5초, 10장면 · 17문장, TTS `ko-KR-Chirp3-HD-Charon` 1.2배속
- 1화 `shorts/mary-celeste/`를 틀로 씀 (같은 실사 다큐 스타일 · 글씨 · 음악)
- 대본 · 사실 확인 · TTS 검사: `script.md` / 업로드 정보: `youtube-metadata.md` / 콘티: `storyboard.html` · `.png`
- 완성 영상: `video/moai-walk-shorts.mp4`, 썸네일: `thumbnail/thumbnail.png`

## 이번 편에 적용한 사용자 규칙

- 썸네일 전에 제목을 물어봄 (추천 후보 4개 → 사용자가 「이스터섬 모아이 석상의 비밀」로 정함)
- 퀴즈 없음, 썸네일 1.5초 포함 1분 안팎 (59.5초)
- **AI 영상은 중요한 3장면만** (S01 훅 · S07 걷기 실험 · S10 마무리), 나머지 7장면은 사진 + 켄 번즈 → RunPod 약 $1.41
- 화면 맨 위 라벨에 편 번호 없음 (「세계의 미스터리」만)

## 새로 만든 것

- **사진 장면 `photo(src, z, pan)`** (`gen_scenes.py`): `footage/cand/<src>.jpg`를 영상과 같은 색으로 보정해 `parts/Sxx/still.png`로 쓰고(`prep_footage.py`), EffectCraft `kenburns` 애니메이션으로 장면 내내 천천히 확대(z0 → z1 %) · 이동(pan px). 장면 길이는 `gen_scenes.py`가 채움
- **영상 장면 `video(clip)`**: 클립 이름과 장면 번호가 달라도 됨 (S07 장면 = `footage/S06.mp4`, S10 = `footage/S08.mp4`)
- **사진 재사용:** 실험 준비(S06, 사진)와 걷는 석상(S07, 영상)은 같은 사진에서, S09는 S03의 다른 후보 사진 → 추가 비용 없음
- `gen_footage.py video`는 `VIDEO`에 적은 장면만 영상으로 만듦

## 이번 편 메모

- Seedream이 세로 구도에서 비탈 사진을 자꾸 옆으로 눕혀 그림 → 「eye-level, 세 머리를 가까이」로 바꿔 해결 (프롬프트에 "upright portrait composition"만으로는 부족)
- 숫자 읽기: `SPOKEN`에 「3,500km」 · 「4미터」, `NATIVE_COUNTERS`에 「명」(열여덟 명)
- 「복제 석상」은 받아쓰기가 계속 틀려 「모형 석상」으로
- S03 카드가 모아이 얼굴을 가려 몸통 쪽(y=990 · 1170)으로 내림

## RunPod 사용액

Seedream 사진 19장 약 $0.51 + WAN 2.2 클립 3개 $0.90 = **약 $1.41**. 잔액은 완성 보고에 적음.

## 다시 만들기

```
cd build && ./build_all.sh --render
```

`footage/`의 클립과 사진은 커밋되어 있어 RunPod 없이 다시 빌드됩니다.
