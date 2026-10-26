# 지식 쇼츠 제작 순서 (복리의 마법 기준)

이 문서는 다른 세션에서 같은 방식으로 이어서 작업하기 위한 정리입니다.
저장소: `mr6200/ai-idea` · 브랜치: `claude/shorts-workflow-hyy56a` (1·2편), `ccr-78413b83-erbceh` (3편) · 작업 폴더: `shorts/`

| 편 | 폴더 | 상태 |
|---|---|---|
| 1. 복리의 마법 | `shorts/` (루트에 바로 있음) | 완성 |
| 2. 72의 법칙 | `shorts/rule-of-72/` | 완성 |
| 3. 4%의 법칙 | `shorts/four-percent-rule/` | 완성 |

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
| 한글 글꼴 | 환경에 있는 것은 WenQuanYi Zen Hei뿐 |

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

## 다음 쇼츠를 만들 때

2편부터는 **편마다 폴더를 따로** 둡니다 (1편 빌드를 덮어쓰지 않도록).
`shorts/rule-of-72/`가 가장 깔끔한 틀입니다. 18장면 모두 `gen_scenes.py` 코드로 그리고, 콘티도 장면 그림에서 자동으로 만듭니다.

1. `shorts/rule-of-72/`를 새 폴더로 복사 (`build/svg`, `build/parts`, `scenes`, `video`, `tts`는 빼고)
2. 새 주제로 `script.md` 작성 — 숫자는 파이썬으로 직접 계산해 검증표를 붙임
3. `gen_scenes.py`의 `LABEL`과 S01–S18 정의, `timeline.py`의 `CUES`를 새 내용으로 교체
4. `gen_narration.py`의 `SPOKEN` (화면 글자 → 읽는 말), `gen_audio.py`의 `COIN_PARTS`와 수동 효과음 시각,
   `gen_effectcraft.py`의 장면별 카운터와 상단 고지 문구를 새 내용에 맞춤
5. `build_all.sh`의 프로젝트·영상 파일 이름 변경 후 `build_all.sh --render`
6. 장면 PNG 시트 → Main 프레임 시트로 겹침 확인 → 썸네일·메타데이터 → Drive 업로드(편마다 새 폴더)
