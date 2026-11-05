# 새 세션용 쇼츠 제작 안내서 (26편부터)

> **2026-11-05 바뀐 규칙 (사용자 요청, 세계의 미스터리 1화 `shorts/mary-celeste/`부터, 아래 내용보다 우선):**
> 1. 썸네일을 만들기 **전에 제목을 사용자에게 묻는다.** 내 추천 후보 3~4개를 함께 보여 주고(AskUserQuestion), 고른 제목을 썸네일 문구 · 유튜브 제목에 쓴다.
> 2. **퀴즈를 넣지 않는다.** 그 자리에 주제에 맞는 내용을 더 보충한다 (드럼롤 · 정답 효과음도 뺌).
> 3. 길이는 **썸네일 1.5초를 포함해 1분 안팎** (`INTRO=1.5`). 꼭 60초에 맞출 필요는 없다.
> 4. **AI 영상은 중요한 장면(훅 · 마무리 등) 3~4개에만** WAN 2.2를 쓰고, 나머지는 Seedream 사진 + 켄 번즈(`gen_effectcraft.py`의 `kenburns` 애니메이션, 12편 방식). 한 장면에 클립 2개를 잇지 않는다. 목표 비용 한 편 약 $1.5 (클립 $0.30 × 3~4 + 사진 $0.027 × 장면 수 × 2). 실사 다큐 틀은 `shorts/mary-celeste/` (2026-11-05 사용자 요청, 미스터리 2화부터)

다른 세션에서 새 주제로 지식 쇼츠를 만들 때 이 파일 하나만 읽고 바로 시작할 수 있도록, 25편까지 해 온 순서와 방식을 지금 규격 기준으로 정리했습니다 (2026-11-05).
지난 편들의 자세한 내력은 `shorts/WORKFLOW.md`, 작업 규칙은 저장소 맨 위 `CLAUDE.md`에 있습니다.

---

## 0. 시작 전에 꼭 확인

| 항목 | 내용 |
|---|---|
| 저장소 · 브랜치 | `mr6200/ai-idea`. 쇼츠 파일은 **`ccr-78413b83-erbceh` 브랜치에만 있음** (`main`에는 없음). 새 세션 브랜치가 다르면 먼저 `git fetch origin ccr-78413b83-erbceh` 후 그 내용을 가져와서(`git merge origin/ccr-78413b83-erbceh` 또는 그 브랜치에서 작업) 시작 |
| 소통 | 진행 상황 · 중간 보고 · 완성 보고는 **한글** |
| PR | 사용자가 요청할 때만 만듦 |
| 다음 편 번호 | **26편** |
| 길이 | 본편 **최대 60초** + 맨 앞 썸네일 **1초**. 내용이 일찍 끝나면 채우지 말고 마지막 말 뒤 약 2.5초(구독 버튼 탭)에서 끝냄. 23~25편은 45~48초 |
| 주제 | 돈 · 생활. "와, 진짜?" 하는 반전 · 질문형 · 이야기형. 첫 2초에 질문이나 놀라운 사실 |
| 화면 스타일 | **웹툰풍 틀 + 액션 세미리얼 그림체** (26편부터, 사용자 선택, `shorts/webtoon-styles/4_action.png`). 같은 직장인 캐릭터 유지 |
| TTS | Google Cloud TTS `ko-KR-Chirp3-HD-Charon`, `RATE = 1.2` |
| 환경 변수 | `GOOGLE_TTS_API_KEY`, `RUNPOD_API_KEY` (둘 다 설정돼 있어야 함) |
| 도구 | `vectorcraft-cli`, `effectcraft-cli`, ffmpeg, Python, `faster-whisper`(TTS 검사), Chromium/Playwright(콘티 PNG) |
| 글꼴 | `shorts/fonts/`의 Black Han Sans(제목) · Do Hyeon(자막) · Jua(말풍선 · 효과음) · Nanum Pen. `build_all.sh`가 `~/.fonts`에 설치 (컨테이너가 다시 시작되면 사라지므로 매번 설치됨) |
| 전달 | Google Drive 커넥터 (없으면 업로드 못 했다고 알리고 https://claude.ai/customize/connectors 에서 연결 후 새 세션을 열어 달라고 안내) |

---

## 1. 주제 정하기

- 사용자가 주제를 주면 그대로, "다음 주제 정하자"면 후보 3~4개를 질문(AskUserQuestion)으로 보여 주고 고르게 함
- 이미 만든 주제(`shorts/WORKFLOW.md` 맨 위 표)와 겹치지 않게
- 폐기된 주제: 편의점 1+1, 주택연금 (흥미가 적다는 이유) → 설명형 · 계산형보다 반전 · 이야기형
- 영어 폴더 이름을 정함 (예: `shorts/bank-4pm/`)

## 2. 새 폴더 만들기 (25편을 틀로)

```bash
cd shorts
mkdir -p NEW/build
cp bank-4pm/build/*.py bank-4pm/build/build_all.sh NEW/build/
cp bank-4pm/.gitignore NEW/
```
`ai_bg/`, `parts/`, `svg/`, `tts/`, `scenes/`, `video/`는 복사하지 않음 (새로 만들어짐).
`build_all.sh`와 `gen_effectcraft.py` 안의 `bank-4pm` 이름을 새 폴더 이름으로 모두 바꿈.

## 3. 사실 확인 → 대본

1. 웹 검색으로 영상에 넣을 숫자 · 날짜 · 주장을 하나하나 확인 (자료 2개 이상 대조). 일부 사이트는 프록시에서 막히니 검색 결과로 대조
2. 공식 근거가 없는 것은 영상에서 **단정하지 않음** (25편: "왜 하필 4시인가"는 근거가 없어 말하지 않음)
3. "내년", "올해" 같은 표현은 기준 연도를 `script.md`에 적어 둠
4. 구성 (7장면 안팎, 문장 15~17개):
   - 훅(질문) → 본론 2~4장면 → **퀴즈**(정답이 하나만 되게, 보기 3개) → 마무리 + "더 많은 돈 이야기가 궁금하다면 구독해 주세요"
5. 문장은 자막 한 줄 약 15글자, 두 줄까지 (`\n`으로 나눔)

## 4. 파일별로 고칠 것 (`NEW/build/`)

| 파일 | 고칠 것 |
|---|---|
| `timeline.py` | `CUES = [(시작, 끝, "자막\n두 줄"), ...]`, `DURATION` = 마지막 자막 끝 + 약 2.8초 (정수) |
| `gen_scenes.py` | 장면 S01~S07의 시작 · 끝 시각과 겹쳐 얹는 그림(제목 `head()`, 카드 `card()`, 알약 `pill()`, 말풍선 `bubble()`, 효과음 `sfx()`, 폭발 `burst()`, 영업시간 `hours()`, 흐름 `flow()`). 장면 시각은 서로 이어지고 마지막 끝 = `DURATION` |
| `gen_backgrounds.py` | `CHAR`(같은 캐릭터, 그대로), `STYLE`(아래 5장), 장면별 프롬프트 `SCENES` |
| `gen_backgrounds_seedream.py` | `SEED`를 편마다 새 값으로 (25편 2600 → 26편 2700 등) |
| `gen_narration.py` | `SPOKEN`(읽기 어려운 기호 → 읽는 말, 예: `"1+1": "원 플러스 원"`), `NATIVE_COUNTERS`(살 · 번 · 달 · 곳 · 시는 고유어 숫자) |
| `gen_audio.py` | `DUR = DURATION`, 퀴즈 드럼롤 · 정답 딩 · 구독 클릭 효과음 시각 |
| `gen_thumbnail.py` | 썸네일 제목(두 줄, 얼굴을 가리지 않게) · 말풍선 · 효과음 |
| `gen_storyboard.py` | 콘티 제목 · 편 번호 · 길이 |
| `build_all.sh` | 폴더 · 파일 이름 (`INTRO=1.0` 그대로) |

## 5. AI 그림 (RunPod Seedream 4.0)

- 공개 엔드포인트 `https://api.runpod.ai/v2/seedream-v4-t2i/runsync`, 장당 **$0.027**, 크기 `"1080*1920"`. 엔드포인트를 만들거나 지울 필요 없음
- Python urllib은 프록시에서 403 → **curl로 호출** (`gen_backgrounds_seedream.py`가 이미 그렇게 함)
- 실행: `cd NEW/build && python3 gen_backgrounds_seedream.py` → `ai_bg/S01.png …`
- 다시 그리기: 그 그림을 지우고 `python3 gen_backgrounds_seedream.py S03 --seed 1` (seed에 100·N을 더함)
- **액션 세미리얼 `STYLE`** (26편부터):
  ```
  semi-realistic action fantasy webtoon style, dramatic cinematic lighting, rim light, saturated colors,
  detailed rendering, dynamic angle, vertical 9:16 composition, no text, no letters, no numbers, no speech bubbles
  ```
- `CHAR` = "the same young korean office worker man with short black hair, white shirt and navy tie" (모든 프롬프트에 똑같이). 다른 인물도 고정 설명으로 (25편 `TELLER`)
- 그림을 **모두 눈으로 확인**하고 이런 것이 있으면 다시 그림:
  - 간판 · 문 위 엉터리 글씨(영어 · 한글 · 한자) → 프롬프트에 "plain wall with no signboard, no writing anywhere"
  - 실제 회사 로고 (20편 맥도날드)
  - 퀴즈 숫자와 헷갈리는 숫자 (23편 달력 「16」)
  - 돌아간 그림, 손가락 이상

## 6. 글씨 얹기 (웹툰 틀, 액션 세미리얼 색)

- 칸 테두리(검정 16px) + 위쪽 라벨 칩 「지식 쇼츠 · 돈과 생활」 (`bg()`)
- 제목: Black Han Sans, 흰 글씨 + 강조 줄은 노랑/주황 `#ffb703`, 외곽선은 짙은 보라 `#2b1055` (그림이 진해서 대비 확인)
- 효과음: Jua, 주황 `#ff5400` + 흰 외곽선, 살짝 기울임
- 말풍선: 흰 풍선 + 검은 테두리 + 꼬리, 인물 옆 빈 곳
- 자막(`gen_subtitles.py`): 웹툰 대사 상자, 도현 58px. 액션 세미리얼은 어두운 상자 `#14141f` + 노랑 테두리 · 글씨 (예시 `shorts/webtoon-styles/compose.py`의 `4_action`). 한 줄 폭 제한 assert(`text_width + 90 < 1020`)에 걸리면 줄을 나눔
- **얼굴을 가리지 않게** — 웹툰은 인물이 커서 가림이 잦음. 카드는 위(y≈440) 또는 아래로, 퀴즈 보기는 얼굴 아래(y≈780부터)

## 7. 빌드 · TTS 검사 · 시험 프레임

```bash
cd NEW/build
bash build_all.sh                 # 렌더 없이 프로젝트까지 (그림 → 자막 → TTS → 소리 → .ecproj)
python3 tts_check.py              # tts_report.md 생성, 경고가 있으면 exit 1
```

**TTS 검사 규칙**
- `tts_report.md`의 경고(줄 안 쉼 > 0.35초, 음절당 > 0.42초, 유사도 < 0.85, **빨리 감기 > 1.12배**, 한 글자 문장 끝)를 모두 살핌
- 받아쓰기(Whisper small)가 이상하면 그 줄을 **Whisper medium**으로 다시 받아써 봄. small · medium **둘 다** 틀리면 문장을 바꿈, small만 틀리면 그대로
- 자주 고친 예: 한 글자 문장 끝(「원!」 → 「원이에요!」), 약어(「공정위는」 → 「공정거래위원회가」), 비슷하게 들리는 말(「갚는」 → 「메우는」, 「3일보다」 → 「사흘보다」), 날짜(「6월」 → 「유월」), 시각(「4시」 → 「네 시」, `NATIVE_COUNTERS`)
- 실제 발음이 표기와 다른 말은 TTS가 맞을 수 있음 (색맹 [생맹], 갓난아기 [간난아기] — 사용자 지적). 헷갈리면 medium으로 확인
- **빨리 감기 연쇄**: 앞 줄 말이 길어 다음 줄이 늦게 시작하면 뒤 줄들이 빨라짐 → 자막 시각을 뒤로 넓히고 필요하면 `DURATION`을 늘림
- 고친 내용은 `script.md`의 「TTS 검사」 표에 적음

**시험 프레임** (렌더 전에 꼭)
```bash
for t in 2 8 15 23 29 33 37 44; do
  effectcraft-cli render-frame --project ../video/NEW.ecproj --comp Main --time $t --max-side 540 --out $SCRATCH/f_$t.png
done
```
겹친 글씨가 얼굴을 가리는지, 글씨가 잘 읽히는지 보고 `gen_scenes.py`를 고친 뒤 다시 `bash build_all.sh`.

## 8. 렌더

렌더는 6~7분 걸리므로 배경으로 돌리고 로그를 기다림:
```bash
cd NEW/build
(bash build_all.sh --render > render.log 2>&1; echo "finished: $?" >> render.log)   # run_in_background
until grep -q "^finished:" render.log; do sleep 10; done; tail -3 render.log
```
결과: `NEW/video/NEW-shorts.mp4` (썸네일 1초 + 본편, −14 LUFS 정규화, H.264 Main, faststart).
확인: `ffprobe`로 길이(본편 + 1초), loudnorm 요약(약 −14 LUFS, True Peak −1.5 근처), 6초 간격 프레임 시트로 전체 훑기. `render.log`는 지우고 커밋.

## 9. 문서 (`NEW/`)

| 파일 | 내용 (틀: `shorts/bank-4pm/`) |
|---|---|
| `script.md` | 길이 · 편 번호 · 스타일 · 기준 날짜, 장면별 「화면」 + 내레이션, **TTS 검사 표**, **사실 확인 표**(영상 속 내용 / 확인 결과 / 근거), AI 그림 장수 · 비용 |
| `youtube-metadata.md` | 추천 제목(#shorts) + 후보 3개, 설명(📌 다루는 것, ⏱ 챕터, 📚 참고, ※ 안내 문구 "교육 목적의 일반 정보 · 영상 속 인물은 AI로 그린 그림"), 해시태그, 태그, 장면별 챕터 표 |
| `README.md` | 길이 · 장면 수 · TTS, 틀로 쓴 편, 이번 편 메모(새 도우미, 고친 문제), RunPod 사용액, 다시 만들기 명령 |

**챕터 규칙**
- 모든 시간은 본편보다 **+1초**(썸네일), 초는 내림
- 설명란 챕터: 첫 줄 `0:00`, 챕터마다 **10초 이상**, 3~4개로 장면을 묶음
- 설명란은 **줄마다 빈 줄**을 넣음 (Drive · GitHub에서 한 줄 바꿈이 무시되어 붙어 버림)

그리고 저장소 문서 갱신:
- `shorts/WORKFLOW.md` 맨 위 표에 한 줄 추가 (+ 새로 배운 점이 있으면 해당 절에)
- `CLAUDE.md`의 쇼츠 제작 항목에 「26편 「제목」(`shorts/NEW/`) …」 메모, 「기존 폴더」 목록에 Drive 폴더 id

## 10. Google Drive

1. 새 폴더 만들기: `mcp__Google_Drive__create_file` (title 「짧은 이름 쇼츠」, contentMimeType `application/vnd.google-apps.folder`)
2. 그 폴더에 문서 3개 (`contentMimeType: text/markdown` → 구글 문서로 변환):
   - 「제목 — 유튜브 업로드 정보」 (`youtube-metadata.md` 내용)
   - 「제목 — 대본 · 사실 확인」 (`script.md` 요약)
   - 「짧은 이름 쇼츠 — 영상 파일 링크 (GitHub)」: 영상 · 썸네일 · 콘티 · 대본 · 폴더의 GitHub 링크 (`https://github.com/mr6200/ai-idea/blob/<브랜치>/shorts/NEW/...`)
3. 영상 · 이미지 같은 큰 파일은 커넥터로 못 올리므로 링크 메모로 대신하고 사용자에게 그렇게 했다고 말함. 중간 산출물(시험 렌더 등)은 올리지 않음
4. 폴더 id를 `CLAUDE.md`에 적음

## 11. 커밋 · 푸시 · 전달

```bash
git add CLAUDE.md shorts/WORKFLOW.md shorts/NEW
git commit -m "26편 「제목」 쇼츠 완성 (NN초 + 썸네일 1초, 웹툰풍 액션 세미리얼)"
git push -u origin <브랜치>      # 네트워크 오류면 2·4·8·16초 간격으로 재시도
```
그다음 `SendUserFile`로 완성 영상 · 썸네일 · 콘티(storyboard.png)를 보냄.

## 12. RunPod 보고 (완성 보고에 꼭)

```bash
K="$RUNPOD_API_KEY"
curl -s -H "Content-Type: application/json" -H "Authorization: Bearer $K" https://api.runpod.io/graphql \
  -d '{"query":"{ myself { clientBalance currentSpendPerHr } }"}'                     # 잔액
curl -s -H "Authorization: Bearer $K" https://rest.runpod.io/v1/endpoints              # 남은 엔드포인트 (비어 있어야 함)
curl -s -H "Authorization: Bearer $K" https://rest.runpod.io/v1/pods                   # 파드
curl -s -H "Authorization: Bearer $K" "https://rest.runpod.io/v1/billing/pods?bucketSize=day"
```
- 보고: **이번 편 사용액**(그림 장수 × $0.027) · **남은 잔액** · 남은 엔드포인트 없음
- 파드 `360qr47tgkg9qo`(incredible_rose_gazelle)와 10월 네트워크 볼륨은 이 작업에서 만든 것이 아님 → **건드리지 않고 비용만 보고**
- 잔액은 반영이 늦을 수 있음 (방금 쓴 금액이 안 빠졌으면 "반영 전"이라고 적음)
- 25편 완성 뒤 잔액 약 $30.29, 그 뒤 그림체 예시 5장 약 $0.14 사용

## 13. 완성 보고 (한글)

- 영상 길이 · 스타일 · 흐름 요약
- 사실 확인에서 뺀 것 · 단정하지 않은 것, 나중에 고쳐야 할 표현(연도 등)
- TTS · 화면에서 고친 것
- 전달: 커밋 · 푸시, Drive 폴더 링크와 올린 문서, 영상은 GitHub 링크로 대신한 점
- RunPod: 사용액 · 잔액 · 남은 엔드포인트 없음 · 남의 파드 상태

---

## 자주 겪은 문제

| 문제 | 해결 |
|---|---|
| 글꼴이 없어 글씨가 깨짐 | 컨테이너가 다시 시작됨 → `build_all.sh`가 다시 설치 (`cp shorts/fonts/*.ttf ~/.fonts && fc-cache -f`) |
| 렌더 중 컨테이너 재시작 | 다시 렌더 (배경 실행 + `finished:` 줄로 끝 확인) |
| 자막 폭 assert 실패 | 자막을 두 줄(필요하면 세 줄)로 나눔 |
| `timeline.py`를 정규식으로 고치다 `\n`이 깨짐 | 치환에 lambda를 쓰거나 파일을 다시 씀 |
| 그림 속 엉터리 글씨 · 로고 | 프롬프트에 no signboard / no writing, 다시 그림 (`--seed N`) |
| 겹친 글씨가 얼굴을 가림 | 시험 프레임으로 확인 후 위치 옮김 |
| 숫자를 이상하게 읽음 (「3,600만」 → 「삼 육백만」) | `gen_narration.py`가 숫자를 한글로 바꿔 TTS에 보냄. 새 단위는 `SPOKEN`/`NATIVE_COUNTERS`에 추가 |
| 일부 뉴스 · 공공 사이트 접속 차단 | 웹 검색 결과로 여러 자료 대조, `script.md`에 그렇게 적음 |
| `git push` 실패 | 네트워크 오류면 재시도 (2 · 4 · 8 · 16초) |

## 새 세션에 붙여 넣을 첫 메시지 예시

```
shorts/NEW_SESSION_GUIDE.md를 먼저 읽고(브랜치 ccr-78413b83-erbceh에 있음),
그 순서대로 26편 쇼츠를 만들어 주세요. 주제는 「○○○」 (또는: 주제 후보부터 골라 주세요).
스타일은 웹툰풍 + 액션 세미리얼 그림체, 60초 이내 + 썸네일 1초.
```
