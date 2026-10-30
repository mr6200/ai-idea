# 지식 쇼츠 제작 순서 (복리의 마법 기준)

이 문서는 다른 세션에서 같은 방식으로 이어서 작업하기 위한 정리입니다.
저장소: `mr6200/ai-idea` · 브랜치: `claude/shorts-workflow-hyy56a` (1·2편), `ccr-78413b83-erbceh` (3편부터) · 작업 폴더: `shorts/`

| 편 | 폴더 | 상태 |
|---|---|---|
| 1. 복리의 마법 | `shorts/` (루트에 바로 있음) | 완성 |
| 2. 72의 법칙 | `shorts/rule-of-72/` | 완성 |
| 3. 4%의 법칙 | `shorts/four-percent-rule/` | 완성 |
| 4. 적립식 vs 거치식 | `shorts/dca-vs-lump/` | 완성 |
| 5. 예금 vs 적금 | `shorts/deposit-vs-savings/` | 완성 |
| 5. 은행은 언제 어떻게 처음 생겼을까? | `shorts/bank-origins/` | 완성 (2분 규격 첫 편) |
| 6. 은행은 어떻게 돈을 벌까? | `shorts/how-banks-earn/` | 완성 (1분 30초 시험) |
| 7. 이자에 붙는 세금 | `shorts/interest-tax/` | 완성 (1분 30초) |
| 8. 무이자 할부, 카드사는 손해일까? | `shorts/card-installments/` | 완성 (1분 30초) |
| 9. 비행기 창문은 왜 둥글까? | `shorts/airplane-windows/` | 완성 (1분 30초, 설계도+팝아트 스타일 첫 편) |
| 10. 비행기 타면 귀가 먹먹한 이유 | `shorts/ear-pressure/` | 완성 (1분 30초, 표제란 없는 첫 편) |
| 11. 엘리베이터 줄이 끊어지면 추락할까? | `shorts/elevator-safety/` | 완성 (1분 30초, 빈티지 포스터 + AI 동판화 배경 스타일) |
| 12. 타이타닉은 왜 가라앉았을까? | `shorts/titanic/` | 완성 (**1분 10초**, 빈티지 + AI 그림 켄 번즈·필름 효과) |
| 13. 60세 퇴직, 연금은 65세? | `shorts/retirement-gap/` | 완성 (1분 30초, 3D 클레이 AI + 인포그래픽) |
| 14. 국민연금, 일찍 받을까 늦게 받을까? | `shorts/pension-timing/` | 완성 (1분 30초, 13편 후속, 같은 스타일) |
| 15. 국민연금, 낸 돈보다 더 받을까? | `shorts/pension-return/` | 완성 (1분 30초, 노후 준비 3편, TTS 검사 첫 편) |
| ~~16. 주택연금, 집 한 채로 매달 얼마 받을까?~~ | `shorts/house-pension/` | **폐기** (사용자, 2026-10-30) — 16편은 새 주제로 다시. 썸네일 인트로·TTS 검사기 개선은 이 폴더의 `build/`를 틀로 씀 |
| 16. 신호등은 왜 빨강·노랑·초록일까? | `shorts/traffic-light/` | 완성 (1분 30초 + 썸네일 1.5초, 빈티지 + AI 동판화, 12편 빈티지 + 최신 자동화 합침) |
| 17. 여자는 왜 더 오래 살까? | `shorts/women-longevity/` | 완성 (1분 30초 + 썸네일 1.5초, **실사 다큐**: Seedream 사진 → WAN 2.2 영상) |
| 18. 로또 1등은 정말 망할까? | `shorts/lotto-winners/` | 완성 (**60초 + 썸네일 1초** 첫 편, 3D 클레이 AI(Seedream) + 인포그래픽) |
| 19. 편의점 1+1, 정말 이득일까? | `shorts/convenience-deals/` | 완성 (60초 + 썸네일 1초, 18편과 같은 스타일) |

## 0. 환경 준비

| 항목 | 상태 / 필요한 것 |
|---|---|
| EffectCraft, VectorCraft | MCP 도구 + CLI(`effectcraft-cli`, `vectorcraft-cli`)가 설치돼 있음 |
| EffectCraft 스크립트 | MCP의 `run_script`는 막혀 있음 → `effectcraft-cli script`로 실행 |
| Google Cloud TTS | 환경 변수 `GOOGLE_TTS_API_KEY` (설정됨) |
| Google Drive | 커넥터 연결됨. 텍스트 문서만 올리기 쉽고, 영상·이미지는 GitHub 링크 메모로 남김 |
| Drive 직접 업로드(선택) | `GDRIVE_CLIENT_ID` / `GDRIVE_CLIENT_SECRET` / `GDRIVE_REFRESH_TOKEN`을 환경에 넣으면 큰 파일도 업로드 가능 (아직 미설정) |
| OpenAI 이미지 | 사용 불가 (`api.openai.com` 차단, 키 없음) |
| AI 이미지 (오픈소스) | SDXL + SDXL-Lightning을 CPU에서 실행 (2편부터). 네트워크 허용: `huggingface.co`, `*.hf.co`, `download.pytorch.org`. GPU 없음 → 장당 약 5분, bfloat16으로 메모리 약 11GB (fp32는 메모리 부족으로 죽음) |
| RunPod (GPU) | `RUNPOD_API_KEY` 설정됨. Pod 웹 주소는 막혀 있어 서버리스 엔드포인트로 배경 생성 (`four-percent-rule/README.md`의 순서). 쓰고 나면 엔드포인트·템플릿 삭제 |
| Newtake | 사용하지 않음 (사용자 요청) |
| 한글 글꼴 | 기본은 WenQuanYi Zen Hei뿐 → `shorts/fonts/`의 Black Han Sans·Do Hyeon·Jua·Nanum Pen(OFL)을 `~/.fonts`에 복사해 사용 (`build_all.sh`가 설치) |

## 1. 기획

1. **대본** — 주제·길이(2분 30초)에 맞춰 7개 구간으로 작성, 숫자는 직접 계산해 검증표를 붙임
   → `shorts/compound-interest-script.md`
2. **콘티** — 18컷, 컷마다 9:16 썸네일 스케치·시간·화면·모션·내레이션·효과음.
   HTML로 만들고 Chromium(playwright)으로 PNG 렌더
   → `shorts/compound-interest-storyboard.html` / `.png`

## 2. 그림 (VectorCraft)

3. **S01–S03** — VectorCraft MCP 도구(draw_shape / draw_path / add_text)로 직접 그림
   → `shorts/scenes/S01_hook_paper.vectorcraft` 등
4. **S04–S18** — `build/gen_scenes.py`가 장면마다 움직일 부품을 SVG로 작성하고,
   `vectorcraft-cli convert`로 1080×1920 투명 PNG 레이어(`build/parts/Sxx/*.png`)와
   장면 원본(`scenes/Sxx.vectorcraft`)으로 변환
5. **S01–S03 레이어 분리** — `build/export_s01_s03.py`가 오브젝트를 숨겨 가며 부품 PNG로 내보냄
6. 레이아웃 확인 — 장면 PNG를 한 장의 시트로 모아 겹침·넘침을 눈으로 확인하고 수정

### AI 배경 (2편부터)

- `build/gen_backgrounds.py`가 장면마다 일러스트 배경을 그려 `build/ai_bg/`에 저장(커밋함). 글자는 넣지 않음
- `build/compose_bg.py`가 배경을 살짝 흐리게 한 뒤 반투명 크림 덮개(`BG_WASH` 0.58) 아래에 깔아 숫자·그래프가 잘 읽히게 함
- 파이썬 가상환경은 스크래치 폴더에 따로 만듦: `pip install torch diffusers transformers accelerate safetensors peft`
  (PyTorch CPU 전용 인덱스는 프록시 문제로 실패할 수 있음 → 일반 PyPI 판을 써도 CPU에서 동작)
- 3편부터는 RunPod 서버리스 GPU로 생성 (`build/gen_backgrounds_runpod.py`, 장당 약 11초, 18장 약 $0.03).
- GPU가 있는 사용자 PC에서 Claude Code를 돌리면 장당 몇 초. 그림만 PC에서 만들어 푸시하고 조립·렌더는 클라우드에서 해도 됨

## 3. 타임라인·자막·소리

7. **타임라인** — `build/timeline.py`: 장면 시간, 부품별 애니메이션(pop / fade / slide / growY / wipe / stamp / spin),
   자막 36개 → `build/manifest.json`
8. **자막 카드** — `build/gen_subtitles.py`: 자막을 반투명 카드 PNG로 (y=1480, 쇼츠 하단 UI 위)
9. **내레이션** — `build/gen_narration.py`: 자막 문장마다 Google Cloud TTS `ko-KR-Chirp3-HD-Charon`
   - 숫자는 한글로 풀어서 보냄 (3,600만 → 삼천육백만, 25살 → 스물다섯 살, 42번 → 마흔두 번)
   - 문장이 길면 최대 0.35초까지 자막보다 늦게 시작, 그래도 넘치면 atempo로 약간 빠르게
   - `build/tts/`에 캐시 (git 제외)
10. **BGM·효과음** — `build/gen_audio.py`: numpy로 로파이 마림바 BGM과 효과음 합성,
    내레이션 구간에서 BGM 자동 감소(덕킹) → `build/audio.wav` (git 제외)

## 4. 조립·렌더 (EffectCraft)

11. **프로젝트 조립** — `build/gen_effectcraft.py`가 `build.jsx`를 만들고
    `effectcraft-cli script build.jsx --empty --save-as ../video/compound-interest.ecproj`
    - 장면마다 프리컴프, 부품 레이어에 expression으로 모션
    - 와이프는 Linear Wipe (270° = 왼→오, 180° = 아래→위, 0° = 위→아래), 진행률은 부품의 실제 영역에 맞춤
    - Main 컴프: 장면 순서 배치, 자막, 상단 진행 막대, "연 7% 가정" 문구, 카운터 텍스트, 오디오 2개(BGM+효과음, 내레이션)
12. **테스트 프레임** — `effectcraft-cli render-frame`으로 여러 시점을 뽑아 시트로 확인
13. **렌더** — `effectcraft-cli render --format h264 --audio on` (약 17분),
    ffmpeg로 −14 LUFS 정규화 + H.264 Main + faststart
    → `shorts/video/compound-interest-shorts.mp4`
    - 소리만 바뀌었을 때는 `--format wav`로 오디오만 렌더하고 영상 스트림은 복사(-c:v copy)해서 다시 합침

한 번에 전부 다시 만들기: `shorts/build/build_all.sh --render`

## 5. 업로드 준비물

14. **썸네일** — `build/gen_thumbnail.py` → `shorts/thumbnail/thumbnail.png` (1080×1920)
15. **제목·설명·태그** — `shorts/youtube-metadata.md`
16. **브라우저 플레이어** — https://claude.ai/artifact/4X1sJxdGGyUv3Wo1kpm72z (웹용 압축본, 구간 바로가기)

## 6. 전달

17. Google Drive 「복리의 마법 쇼츠」 폴더(id `13pq1Rpo-BD7anVeYfYg30VEEplezJ6Ff`)
    - 올린 것: 대본, 제목·설명·태그(구글 문서), 영상 링크 메모, 썸네일 링크 메모
    - 영상·썸네일 파일 자체는 커넥터 한계로 GitHub 링크로 대신함
18. 모든 결과물은 커밋해서 위 브랜치에 푸시

## 7. 겪은 문제와 해결

| 문제 | 해결 |
|---|---|
| 앱에서 MP4 미리보기 안 됨 | moov를 앞으로(faststart), H.264 Main으로 재인코딩 |
| 와이프가 늦게 시작 | 전체 화면 기준이라 생기는 문제 → 부품 bbox로 진행률 보정 |
| 자막이 장면 하단 요소와 겹침 | 자막 y=1480으로 내리고 겹치는 요소를 위로 |
| TTS가 "3,600만"을 "삼 육백만"으로 읽음 | 숫자를 한글로 바꿔서 TTS에 전달 |
| 음량이 −14가 아니라 −15.8 LUFS로 나옴 (2편) | 1회 loudnorm 뒤에 +1.8dB와 리미터 추가 (`build_all.sh`) |
| "1, 2, 3"처럼 나열한 숫자를 붙여 읽음 (2편) | 숫자 정규식에서 쉼표를 천 단위(`1,000`)일 때만 숫자로 취급 |
| Python에 playwright 없음 (2편) | 콘티 PNG는 Node의 playwright로 스크린샷 (`gen_storyboard.py`) |
| 큰 파일 Drive 업로드 불가 | GitHub 링크 메모. 근본 해결은 Drive API 인증 정보 등록 |

## 사실 확인 (3편부터)

- 대본의 연구·통계 인용은 웹 검색으로 2곳 이상에서 확인하고 `script.md` 끝에 확인 표(내용 · 결과 · 근거)를 붙임
- 이 환경은 논문 PDF·위키백과 등 직접 접속이 막혀 있음 → 검색 결과 요약으로 대조하고, 그 사실을 표에 적음
- 단정이 과한 문장("계속 불어난다" 등)도 고침

## 2분 규격 (「은행의 탄생」부터, 2026-10-26 사용자 요청)

| 항목 | 「예금 vs 적금」까지 | 「은행의 탄생」부터 |
|---|---|---|
| 영상 길이 | 2분 30초 (150초) | **2분 (120초)** |
| 내용 | 18장면 · 자막 약 40문장 | **그대로** (줄이지 않음) |
| TTS 속도 | `gen_narration.py`의 `RATE = 1.08` | **`RATE = 1.2`** (Google TTS `speakingRate`) |

- 「예금 vs 적금」 대본을 120초 · 1.2배속으로 시험해 보니 말하는 시간 약 85초, 39문장 중 1문장만 추가로 1.11배 빨라짐 → 같은 분량이 2분에 들어감
- 1.2배속에서 `ko-KR-Chirp3-HD-Charon`은 초당 약 7음절. 자막 구간 길이는 (읽는 말 음절 수 ÷ 7) + 0.3초 정도로 잡으면 속도 보정이 거의 생기지 않음
- 바꿔야 할 곳:
  - `timeline.py`: `DURATION = 120`, `CUES` 시간 (150초 기준 시각 × 0.8로 시작해 다듬기)
  - `gen_scenes.py`: 장면 시작·끝 시각과 각 부품의 `at` (장면 평균 약 6.7초, 마지막 S18은 3~4초)
  - `gen_audio.py`: `DUR = 120.0`, 손으로 넣은 효과음 시각
  - `gen_narration.py`: `RATE = 1.2`
  - `gen_effectcraft.py`: 상단 고지 문구의 `inPoint`/`outPoint`
- 빌드 뒤 `gen_narration.py`의 출력 "N sped up, max factor"가 1.15를 넘으면 그 문장의 자막 구간을 늘리거나 문장을 다듬음

### 쉼표에서 쉬기 (「은행의 탄생」에서 수정, `bank-origins/build/gen_narration.py`)

- 문제: 일반 텍스트로 보내면 Chirp 3 HD가 쉼표를 무시하고 띄어 읽기를 스스로 정해 "은행의 / 역사 재밌으셨나요?"처럼 어색하게 끊음 (파형 측정: 쉼표 자리 쉼 0초)
- 해결: TTS에 `input.markup`으로 보내고 쉼표마다 `[pause short]`를 넣음 (`markup()`), 그리고 한 문장 안의 쉼을 최대 0.22초로 줄임 (`shorten_pauses()`, `MAX_PAUSE`)
  - `[pause short]`만 쓰면 1.2배속에서 약 0.5초, SSML `<break>`는 길이를 줘도 0.7~0.9초라 너무 김
- 쉬는 자리를 바꾸려면 자막 문장의 쉼표 위치를 바꾸면 됨 (쉼표 = 짧은 쉼). 쉬면 안 되는 곳에는 쉼표를 쓰지 않음
- 다음 편부터는 이 `gen_narration.py`를 그대로 복사해서 씀

### 썸네일 인트로 (16편부터, 사용자 요청)

완성 영상 맨 앞에 썸네일을 1.5초(무음) 붙인다. `build_all.sh`의 `INTRO=1.5`와 렌더 마무리 ffmpeg(`concat`)가 처리하므로 `--render` 한 번으로 끝난다. 영상 길이는 본편 + 1.5초, 설명란 챕터와 장면 표 시간도 1.5초씩 늦춘다(초는 내림). 틀은 `shorts/house-pension/build/build_all.sh`.

### 60초 규격 (18편부터, 2026-10-30 사용자 요청)

조회수가 기대보다 낮아 **60초 + 썸네일 1초**로 줄이고 주제는 돈 · 생활로 정함. 틀은 `shorts/lotto-winners/`.
- `timeline.py`의 `DURATION = 60`, `gen_audio.py`의 `DUR = 60.0`과 손으로 넣은 효과음 시각, `build_all.sh`의 `INTRO=1.0`
- 장면 8개 안팎, 문장 17개 안팎(1.2배속으로 말하는 시간 약 40초), 퀴즈 + 구독 약 18초
- 챕터는 10초 이상 규칙 때문에 4개쯤으로 묶음
- 가격 · 날짜 같은 숫자 문장은 TTS 검사 뒤 Whisper medium으로 꼭 다시 들어 봄 (19편: 「4,750원 참기름을」 → 「4790원」, 「4,750원에서」로 바꿔 해결). 「1+1」 같은 기호는 `SPOKEN`에 읽는 말을 넣음
- 클레이 그림은 Seedream 4.0 공개 엔드포인트로 (`gen_backgrounds_seedream.py`, 장당 $0.027, 엔드포인트 생성 · 삭제 없음)

### TTS 검사 (15편부터, 사용자 요청)

렌더 전에 `build/tts_check.py`를 돌려 `tts_report.md`의 경고를 모두 살핀다. 경고가 없어도 유사도 0.95 미만 줄은 받아쓰기를 읽어 뜻이 바뀌게 들리는지 본다(16편: 「색약인」→「세계적인」 0.86). 받아쓰기가 이상한데 TTS가 맞게 읽는지 헷갈리면 Whisper `medium`으로 그 줄만 다시 받아써 본다 (17편: small은 「색맹」→「생랭」, 「갓난아기」→「간단하기」, medium은 「생맹」·「갓난아기」 — 실제 발음은 [생맹] · [간난아기], 사용자 지적). (`pip install faster-whisper` 필요, 모델은 huggingface.co). 한 글자 문장 끝, 줄 안의 마침표, 0.35초 넘는 쉼, 끄는 말, Whisper 받아쓰기 불일치, 빨리 감기를 잡는다. 15편에서 잡은 예: 「오래, 꾸준히」가 「올해 꾸준히」로 들림 → 「오랫동안 꾸준히」. 자세한 내용은 `shorts/pension-return/README.md`.

### 챕터 (13편부터, 사용자 요청)

`youtube-metadata.md` 설명란에 「⏱ 챕터」(시간 + 주요 내용)를 넣고, 아래에 장면별 시간·주요 내용 표를 붙인다. 유튜브 챕터 규칙(첫 줄 0:00, 챕터마다 10초 이상, 3개 이상)에 맞게 7~8초 장면은 둘씩 묶는다. 쇼츠 화면엔 챕터 바가 안 보이고 설명란 목록으로만 보인다.
설명란 부분은 **줄마다 빈 줄을 넣는다** — Drive 업로드(마크다운 → 구글 문서)와 GitHub 미리보기가 한 줄 바꿈을 무시해 챕터·목록이 한 문단으로 붙는다 (15편에서 사용자 지적, 13~15편 수정).

### 한 글자 문장 끝 피하기 (13편에서 수정)

"네 번째 다리, 일."처럼 문장이 한 글자로 끝나면 Chirp 3 HD가 그 글자를 0.5초쯤 길게 끌고 뒤에 긴 쉼을 넣어 어색하게 들린다 (숫자 "1"처럼 들리기도 함). "일하는 소득,"처럼 두 단어 이상으로 늘리고, 줄 안에서 이어지는 말이면 마침표 대신 쉼표를 쓴다 (마침표 뒤 쉼은 약 0.7초, 쉼표는 0.22초로 줄여짐).

## 1분 30초 시험 (6편, 2026-10-26 사용자 요청)

- 이유: 유튜브 통계에서 중도 이탈이 많음 → 길이를 줄여 5편(2분)과 시청 지속률을 비교
- 길이 90초 (`timeline.py`의 `DURATION = 90`, `gen_audio.py`의 `DUR = 90.0`), TTS는 1.2배 그대로
- 속도를 더 올리지 않고 **내용을 덜어냄**: 장면 18개 → 12개 안팎, 자막 약 28문장, 주제 하나에 곁가지 최소
- 퀴즈 + 구독 요청은 합쳐서 15~20초 이내
- 첫 2초 안에 질문이나 반전을 보여줌 (훅)

## 주제 고르기 (8편부터, 조회수 감소 대응)

- 설명형 주제(세금 제도, 은행 구조)는 조회수가 떨어짐 → 첫 2초에 "어? 진짜?" 하게 만드는 주제로
- 잘 먹히는 유형: 상식과 어긋나는 숫자, 실제 사람·사건 이야기, 오해 바로잡기, 생활과 바로 연결되는 소재
- 제목·썸네일은 질문형·반전형 ("무이자 할부, 카드사는 손해일까?"), 첫 장면은 인사 없이 질문이나 놀라운 숫자부터
- 후보 목록: 비트코인 피자, 10원 동전 제조원가, 짜장면 값으로 보는 물가, 로또 당첨자 파산 오해, 짐바브웨 100조 달러, 커피값 30년

## 설계도+팝아트 스타일 (9편부터 기본, 2026-10-26 사용자 요청)

사용자가 기존 크림색+AI 배경 스타일이 단조롭다고 해서 예시 4종(설계도·팝아트·네온·신문) 중 **설계도와 팝아트를 섞은 스타일**로 정했습니다. 앞으로 모든 편을 이 스타일로 만듭니다. 기준 코드: `shorts/airplane-windows/build/gen_scenes.py`의 도우미 함수.

| 요소 | 규칙 |
|---|---|
| 배경 | 남색 `#0f4c8a` + 설계도 모눈(40px 가는 선, 200px 굵은 선, `#e8f4ff`) + 모서리 망점(시안). `bg()`. **오른쪽 아래 도면 표제란(`DWG. 0NN · 지식 쇼츠`)은 넣지 않음** (9편에만 있음, 사용자 요청으로 10편부터 뺌 → 복사 후 `bg()`에서 표제란 두 줄 삭제) |
| 강조 장면 | 훅·사건·퀴즈엔 파란 햇살 무늬 `bg(burst=(x, y))` (`#2f86dc`, 불투명도 0.45) |
| 그림 | 설계도 선화: 흰 선 `#e8f4ff` 8px, 하늘색 면 `#4cc9f0`, 치수선·주석은 시안 `#7fd3ff` (`dim()`) |
| 팝 장식 | 굵은 검은 테두리 `#111`, 노랑 `#ffd400`, 빨강 `#e63946`, 폭발 별 `burst_star()`, 말풍선 `bubble()`, 검은 그림자 알약 `pill()`·상자 `panel()`, 의성어 `popword()` (기울임) |
| 글꼴 | 제목 **Black Han Sans**(흰색/노랑, 검은 외곽선 `head()`), 감탄사·말풍선·알약 **Jua**, 주석 **Do Hyeon**, 자막 **Do Hyeon** (사용자 지정) |
| 자막 카드 | 흰 상자 + 검은 8px 테두리 + 검은 그림자(10,12 어긋남), 도현 58px 검은 글자, 중심 y=1480 |
| 상단 라벨 | 노란 알약 `지식 쇼츠 · 주제` (y=200) |
| 진행 막대 | 노랑 `[1.0, 0.831, 0.0]`, Main 배경색 남색 |
| AI 배경 | 쓰지 않음 (RunPod 불필요). `compose_bg.py`도 없음 |
| 배치 | 자막 카드(2줄이면 y≈1380–1580)와 겹치지 않게 장면 요소는 **y≈1360 위**에 둠. 자막 카드를 얹은 장면 시트로 확인 |

## 빈티지 포스터 + AI 동판화 스타일 (11편, 2026-10-26 사용자 선택)

사용자가 「다른 스타일」을 원해 예시 10종(직접 그림 A–D, RunPod AI 그림 E–J)을 보여 주고, **A 빈티지 포스터 + E AI 동판화**를 섞기로 함. 앞으로 계속 쓸지는 완성본을 본 뒤 사용자가 정함 (정해지기 전까지 기본은 설계도+팝아트).
규칙과 도우미는 `shorts/elevator-safety/README.md`의 「스타일」, 코드는 `shorts/elevator-safety/build/gen_scenes.py`.

- AI 배경은 RunPod 서버리스로 장면마다 1장 (프롬프트 `gen_backgrounds.py`), `compose_bg.py`가 세피아 한 톤으로 바꿔 반투명 종이 아래 깜
- 글꼴은 나눔명조(제목 800, 설명·자막 700). 자막도 명조 (A 예시 그대로)
- AI는 「줄이 끊어지는 순간」 같은 구체적 동작을 잘 못 그림 → AI는 분위기 배경만, 설명 그림은 직접 그림
- 12편(1분 10초)부터 영상미 강화: AI 그림을 따로 움직이는 층(켄 번즈), 옅은 종이 덧칠, 옛날 필름 효과, 장면마다 AI 2장 중 선택, 단조 음악. 자세한 내용은 `shorts/titanic/README.md`. 70초로 만들 땐 `timeline.py`·`gen_audio.py`의 길이와 효과음 시각을 바꿈

## 3D 클레이 AI + 인포그래픽 스타일 (13편, 2026-10-26 사용자 선택)

은퇴·돈 주제용 예시 4종(수채화 AI, 인포그래픽, 다이어리 손글씨, 클레이 AI) 중 **인포그래픽 + 클레이 AI**를 섞음. 규칙과 도우미는 `shorts/retirement-gap/README.md`의 「스타일」.

- 12편의 켄 번즈 구조(`compose_bg.py`가 `parts/Sxx/ai.png`를 씀, `gen_effectcraft.py`의 `kenburns`)를 그대로 쓰고, 세피아 대신 색 그대로, 필름 대신 옅은 비네트
- RunPod 엔드포인트를 막 만든 직후 `/run`이 500을 돌려줄 수 있음 → 요청마다 재시도하고 만든 뒤 20초쯤 기다림

## 실사 다큐 스타일 (17편, 2026-10-30 사용자 요청)

사용자가 「RunPod으로 실사 다큐 느낌」을 원했고 SDXL 얼굴이 어색하다고 해서 WAN 2.2 영상으로 만듦. 규칙·순서·비용은 `shorts/women-longevity/README.md`.

- RunPod **공개 엔드포인트**(요청당 요금, 엔드포인트 생성·삭제 없음): Seedream 4.0 T2I `seedream-v4-t2i` ($0.027/장, `size: "1080*1920"`) → WAN 2.2 I2V 720p `wan-2-2-i2v-720` ($0.30/5초, `size: "720*1280"`, `num_inference_steps` 필수). runsync가 IN_PROGRESS를 돌려주면 `/status/{id}`로 기다림 (`gen_footage.py`)
- 얼굴 품질은 시작 사진이 정함 → 장면마다 사진 2장 중 골라서 영상으로. Seedream이 가끔 옆으로 누운 구도를 그리니 꼭 확인
- EffectCraft는 mp4 레이어를 그대로 가져옴. 클립(5.4초)을 장면 길이에 맞게 느리게 + `minterpolate` (`prep_footage.py`). 10초 넘는 장면은 클립 2개
- 오버레이는 사진을 보고 **얼굴을 가리지 않는 자리**에 둠. 시험 프레임 시트로 확인
- 한 편 약 $5 (이전 스타일은 몇 센트) → 다음 편 스타일은 사용자에게 확인

## 다음 쇼츠를 만들 때

2편부터는 **편마다 폴더를 따로** 둡니다 (앞 편 빌드를 덮어쓰지 않도록).
10편부터는 `shorts/ear-pressure/`가 틀입니다 (설계도+팝아트 스타일, 표제란 없음, 1분 30초, 12장면).

1. 최근 편의 `build/*.py`, `build/build_all.sh`, `.gitignore`를 새 폴더로 복사 (`svg`, `parts`, `scenes`, `video`, `tts`는 빼고)
2. 새 주제로 `script.md` 작성 — 사실 확인 표를 붙임 (숫자가 있으면 `verify_numbers.py`로 검증표도)
3. `gen_scenes.py`의 `LABEL`, S01–S12 정의, `timeline.py`의 `CUES`를 새 내용으로 교체 (90초)
4. `gen_narration.py`의 `SPOKEN`, `gen_audio.py`의 `COIN_PARTS`와 수동 효과음 시각, `gen_thumbnail.py`, `gen_storyboard.py`의 제목을 새 내용에 맞춤
5. `build_all.sh`의 프로젝트·영상 파일 이름 변경 후 `build_all.sh --render`
6. 자막 카드를 얹은 장면 시트 → 완성 영상 프레임 시트로 겹침 확인 → 썸네일·메타데이터 → Drive 업로드(편마다 새 폴더)
