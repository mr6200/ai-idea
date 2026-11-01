# 22편 · 연금저축 vs IRP, 뭐가 다를까? (60초 · 3D 클레이 AI + 인포그래픽)

- 60초 + 맨 앞 썸네일 1초, 8장면, TTS `ko-KR-Chirp3-HD-Charon` 1.2배속
- 21편 `shorts/pension-savings/` 후속 (사용자 선택), 같은 틀
- 대본 · 사실 확인 · TTS 검사: `script.md` / 업로드 정보: `youtube-metadata.md` / 콘티: `storyboard.html` · `.png`
- 완성 영상: `video/pension-vs-irp-shorts.mp4`, 썸네일: `thumbnail/thumbnail.png`

## 이번 편 메모

- **비교 카드 `versus()`:** 주제 칩 + 왼쪽 연금저축 / 오른쪽 IRP 두 칸. 비교형 주제에 다시 쓸 수 있음 (`build/gen_scenes.py`)
- **퀴즈는 정답이 하나여야 함:** "세액공제를 꽉 채우려면?"은 IRP에만 900만 원을 넣어도 정답이라 → "연금저축에만 900만 원이면 공제는?"(600만 원)으로 바꿈
- **TTS 검사기 개선:** 영문 대문자를 1음절로 세도록 `syllables()` 수정 (「IRP는」 오경고 해결)
- **AI 그림의 엉터리 영어:** "TAX REPIENT", "BANK BANK"가 그려져 두 장면을 다시 그림. 프롬프트에 "no papers with writing", "no signs"를 넣음

## RunPod 사용액

Seedream 4.0 그림 10장 (8장 + 다시 그림 2장) = 약 $0.27. 잔액은 완성 보고에 적음.

## 다시 만들기

```
cd build && ./build_all.sh --render
```
