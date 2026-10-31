# 3분 형사 추리극 영상 제작 파이프라인 (RunPod)

> **결론: 가능합니다.** 대본 → 인물 기준이미지 → 대사 음성 → 립싱크 영상 → 편집(자막·BGM)까지
> 이 폴더의 스크립트로 RunPod GPU 한 대에서 처리합니다.

## 무엇을 만드나

| 항목 | 내용 |
|---|---|
| 작품 | **「예약된 알리바이」** — 갤러리 대표 살인사건, 취조실 심문극 (`story/episode01.yaml`) |
| 길이 | 약 3분 (30컷 + 타이틀/엔딩) |
| 인물 | 3명: 형사 **강도윤**, 용의자 **한서진**, 신참 형사 **오민규** |
| 구도 | 한 컷에 한 사람만 나오는 대화 구도 (shot / reverse-shot) |
| 출력 | 1920×1080, 25fps, 한글 자막 입힘, H.264 + AAC (유튜브 권장 형식) |

## 인물·배경이 바뀌지 않게 하는 방법

일관성이 이 파이프라인의 핵심입니다. "매 컷마다 새로 그리기"를 하지 않습니다.

1. **인물마다 기준이미지 1장만 만듭니다.** (`refs/detective.png` 등)
   세 인물 프롬프트에 같은 `setting`(취조실 묘사)을 붙여 같은 공간처럼 보이게 합니다.
2. **그 인물의 모든 컷은 같은 기준이미지에서 출발합니다.** 립싱크 모델(InfiniteTalk)은
   이미지를 *움직이게* 할 뿐 새로 그리지 않으므로 얼굴·옷·배경이 그대로 유지됩니다.
   컷마다 기준이미지에서 새로 시작하기 때문에 긴 영상에서 생기는 색감 변화나 얼굴 변형도 쌓이지 않습니다.
3. **표정 변형(선택)** 은 FLUX Kontext로 기준이미지를 *편집*해서 만듭니다
   ("표정만 바꾸고 나머지는 그대로"). 결과가 어색하면 지우면 되고, 그러면 기준이미지를 씁니다.

```
story/episode01.yaml ─┬─▶ 01 FLUX.1-dev ──▶ refs/<인물>.png (기준이미지, 직접 선택)
                      │                        └─▶ 02 FLUX Kontext ──▶ refs/<인물>_<표정>.png (선택)
                      ├─▶ 03 edge-tts ──▶ output/tts/<컷>.wav  (+컷 길이)
                      └─▶ 04 InfiniteTalk(기준이미지 + 음성) ──▶ output/lipsync/<컷>.mp4
                                         05 ffmpeg ──▶ output/final.mp4 + subtitles.srt
```

## 1. RunPod 준비

| 설정 | 권장값 |
|---|---|
| GPU | **A100 80GB** 또는 **H100** (RTX 4090 / A6000도 `--low-vram` 으로 가능하지만 많이 느림) |
| 템플릿 | `RunPod PyTorch` 계열 (CUDA 12.1 이상, Ubuntu) |
| Network Volume | **200GB 이상**, `/workspace` 에 마운트 (모델이 약 120GB) |
| Container Disk | 30GB |

Hugging Face 준비:
- [FLUX.1-dev](https://huggingface.co/black-forest-labs/FLUX.1-dev) 와 [FLUX.1-Kontext-dev](https://huggingface.co/black-forest-labs/FLUX.1-Kontext-dev) 페이지에서 라이선스 동의
- Settings → Access Tokens 에서 Read 토큰 발급

Pod 터미널(또는 Jupyter 터미널)에서:

```bash
cd /workspace
git clone https://github.com/mr6200/ai-idea.git
cd ai-idea/detective-video

export HF_TOKEN=hf_xxxxxxxx
bash scripts/setup_runpod.sh        # 최초 1회, 모델 다운로드 포함 (네트워크 속도에 따라 30분~1시간)
```

> Pod를 멈췄다 다시 켜도 `/workspace` 에 다 남아 있으므로 설치는 한 번만 하면 됩니다.
> 단, `apt` 로 설치한 ffmpeg·한글 폰트는 컨테이너 디스크에 있으므로 재시작 후에는 아래만 다시 실행하세요:
> `apt-get update && apt-get install -y ffmpeg fonts-nanum`

## 2. 제작 순서

```bash
cd /workspace/ai-idea/detective-video
IMG=/workspace/venv-img/bin/python
export HF_HOME=/workspace/hf-cache

# ① 음성 먼저 → 실제 영상 길이 확인 (GPU 불필요, 몇 초)
$IMG scripts/03_tts.py
#    "예상 영상 길이: 3분 ..." 이 출력됩니다. 길거나 짧으면 대본(yaml)을 고치고 다시.

# ② 기준이미지 후보 생성 → 직접 보고 고르기
$IMG scripts/01_make_refs.py -n 4
#    refs/candidates/ 의 이미지를 Jupyter 파일 브라우저로 열어 보고 마음에 드는 seed 선택
$IMG scripts/01_make_refs.py --pick detective=1102 suspect=2201 rookie=3303

# ③ (선택) 표정 변형
$IMG scripts/02_make_variants.py

# ④ 애니매틱 미리보기: 정지화면 + 음성 + 자막으로 3분 전체 흐름 확인
$IMG scripts/05_assemble.py
#    output/final.mp4 를 다운로드해서 확인 → 대사/순서 수정은 이 단계에서!

# ⑤ 립싱크: 한 컷으로 품질·소요시간 먼저 확인 후 전체
$IMG scripts/04_lipsync.py --only s01
$IMG scripts/04_lipsync.py                  # 나머지 전부 (이미 만든 컷은 건너뜀)
#    빠르게: --fast (가속 LoRA, 8스텝)   메모리 부족: --low-vram   고화질: --size infinitetalk-720

# ⑥ 최종 편집
$IMG scripts/05_assemble.py --bgm assets/bgm.mp3
```

> `04_lipsync.py` 는 내부적으로 `/workspace/venv-talk` 의 파이썬으로 InfiniteTalk를 실행합니다.
> 경로가 다르면 `INFINITETALK_DIR`, `INFINITETALK_PYTHON` 환경변수로 바꿀 수 있습니다.

**특정 컷만 다시 만들기** (예: s07 대사를 고쳤을 때)

```bash
$IMG scripts/03_tts.py --only s07
$IMG scripts/04_lipsync.py --only s07 --force
$IMG scripts/05_assemble.py
```

## 3. 시간·비용 감각

- 립싱크가 대부분의 시간을 씁니다. 3분 = 약 4,500프레임이고, 컷마다 14B 모델을 새로 불러오므로
  A100 기준 **수 시간** 단위로 잡는 게 안전합니다. `--fast` 를 쓰면 크게 줄어듭니다.
- 정확한 수치는 GPU·설정마다 다르므로 **⑤의 `--only s01` 결과 시간 × 컷 수** 로 미리 계산하세요.
- 작업이 없을 때는 Pod를 **Stop** 해 두면 GPU 요금이 나가지 않습니다(볼륨 보관료만 발생).
- 오래 걸리는 작업은 `nohup $IMG scripts/04_lipsync.py > lipsync.log 2>&1 &` 로 돌리면
  브라우저를 닫아도 계속됩니다. 중간에 끊겨도 다시 실행하면 이어서 진행합니다.

## 4. 대본 바꾸기 / 다음 화 만들기

`story/episode01.yaml` 을 복사해 수정하고 모든 명령에 `--story story/episode02.yaml` 을 붙이면 됩니다.

- `characters.*.prompt` : 인물 외모 (영어가 더 잘 됨)
- `characters.*.voice` : edge-tts 한국어 음성 — `ko-KR-InJoonNeural`(남), `ko-KR-SunHiNeural`(여),
  `ko-KR-HyunsuMultilingualNeural`(남). `rate`, `pitch` 로 인물별 차이를 줍니다.
- `shots[].expr` : `nervous / angry / shocked / defeated / smirk` (또는 `expressions` 에 직접 추가)
- `shots[].action` : 립싱크 모델에 주는 동작·감정 힌트
- **같은 인물을 다음 화에서도 쓰려면** `refs/*.png` 를 그대로 두세요. 시리즈 내내 같은 얼굴이 유지됩니다.

## 5. 유튜브 업로드

`youtube_metadata.md` 에 제목·설명·태그 초안과 체크리스트가 있습니다. 꼭 확인할 것:

- 업로드 화면의 **"변경되거나 합성된 콘텐츠" → 예** (사실적인 AI 인물이므로 표시 의무)
- BGM 은 YouTube 오디오 보관함 등 저작권 문제 없는 곡만
- 수익화를 생각한다면 사용하는 모델·음성의 라이선스를 직접 확인하세요
  (FLUX.1-dev는 모델 자체가 비상업 라이선스이고, 생성 결과물의 상업적 사용 조건은 라이선스 문서를 확인 / edge-tts는 Microsoft 온라인 서비스를 쓰는 비공식 도구).
  상업용이 걱정되면 TTS를 상업 라이선스 음성 서비스로 바꾸고 `output/tts/*.wav` 만 교체하면 나머지는 그대로 동작합니다.

## 문제 해결

| 증상 | 해결 |
|---|---|
| FLUX 다운로드 401/403 | HF 모델 페이지에서 라이선스 동의 + `HF_TOKEN` 확인 |
| 립싱크 중 CUDA OOM | `--low-vram`, 그래도 안 되면 더 큰 GPU |
| 입 모양이 어색함 | 기준이미지에서 얼굴이 충분히 크고 정면에 가까워야 함 → 후보를 다시 고르기 |
| 컷마다 미세하게 흔들림 | 정상 범위의 머리 움직임. `talk_prompt` 의 `static camera` 유지 |
| 자막 글자가 네모(□) | `apt-get install -y fonts-nanum && fc-cache -f` |
| 한 컷만 이상함 | 그 컷만 `--only sXX --force` 로 재생성 (seed 를 바꾸려면 `--extra "--base_seed 7"`) |
