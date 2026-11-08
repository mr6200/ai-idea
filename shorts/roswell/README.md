# 세계의 미스터리 4화 · 로스웰 사건의 진짜 정체 (58초 · 실사 다큐 + 실제 자료)

- 본편 58초 + 맨 앞 썸네일 1.5초, 11장면 · 16문장, TTS `ko-KR-Chirp3-HD-Charon` 1.2배속
- 3화 `shorts/nazca-lines/`를 틀로 씀
- 대본 · 사실 확인 · 사진 출처 · TTS 검사: `script.md` / 업로드 정보: `youtube-metadata.md` / 콘티: `storyboard.html` · `.png`
- 완성 영상: `video/roswell-shorts.mp4`, 썸네일: `thumbnail/thumbnail.png`

## 이번 편에 적용한 사용자 규칙

- **실제 자료 첫 편 (규칙 ⑥):** 실제 신문 1면 · 미 공군 보고서 표지 2개 · 모굴 풍선 사진 (모두 공공 영역, 출처는 `script.md` · 설명란)
- 썸네일 전에 제목을 물어봄 (추천 후보 4개 → 「로스웰 사건의 진짜 정체」)
- 퀴즈 없음, 썸네일 포함 59.5초, AI 영상은 3장면만, 화면 위 라벨에 편 번호 없음

## 새로 만든 것

- **실제 자료 장면 `archive(file)`** (`gen_scenes.py`): `build/photos/<file>`를 화면 안에 통째로 보이게 놓고(960×1060 칸, 위쪽 y=340부터), 뒤에는 같은 자료를 흐리고 어둡게 깔아 채움 (`prep_footage.archive_frame`). 색 보정은 하지 않음. 아주 느린 확대(100 → 106~110%)
- **「실제 자료」 표시 `real_tag(문구)`**: 라벨 아래 금색 테두리 알약 (y≈280)
- **낫표 읽지 않기:** `gen_narration.SPOKEN`에서 「 」를 지움 (자막에는 남김). Chirp가 낫표를 이상한 소리로 읽었음

## 실제 자료 구하기 (메모)

- 위키미디어 공용 API는 요청 횟수 제한(429)에 자주 걸림 → 한 번에 여러 파일을 묻고(`titles=A|B|C`, `prop=imageinfo`, `iiprop=url|extmetadata`), 실패하면 잠시 뒤 다시
- 내려받기는 `Special:FilePath/<파일>?width=1600` (curl에 일반 User-Agent), 429가 나면 `imageinfo`의 원본 주소(upload.wikimedia.org)로 직접
- 라이선스는 공용 표시만 믿지 말고 원 출처 설명도 읽음 (이번 편: 포트워스 잔해 사진은 공용 표시와 원 출처 도서관의 비상업 조건이 엇갈려 뺌)

## RunPod 사용액

Seedream 사진 12장 약 $0.32 + WAN 2.2 클립 3개 $0.90 = **약 $1.22**. 잔액은 완성 보고에 적음.

## 다시 만들기

```
cd build && ./build_all.sh --render
```

`footage/`(AI 클립 · 사진)와 `photos/`(실제 자료)는 커밋되어 있어 RunPod 없이 다시 빌드됩니다.
