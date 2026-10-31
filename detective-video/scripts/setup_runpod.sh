#!/usr/bin/env bash
# RunPod Pod 최초 1회 설정. 모든 것을 /workspace(네트워크 볼륨)에 설치하므로
# Pod를 껐다 켜도 다시 받을 필요가 없습니다.
#
#   export HF_TOKEN=hf_xxx            # FLUX.1-dev / Kontext 라이선스 동의한 계정의 토큰
#   bash scripts/setup_runpod.sh            # 전부
#   bash scripts/setup_runpod.sh img        # 이미지/음성 환경만
#   bash scripts/setup_runpod.sh talk       # 립싱크 환경만
set -euo pipefail

WS=/workspace
PROJECT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
export HF_HOME=$WS/hf-cache
export HF_HUB_ENABLE_HF_TRANSFER=1
WHAT=${1:-all}

apt-get update -qq && apt-get install -y -qq ffmpeg fonts-nanum python3-venv git >/dev/null
fc-cache -f >/dev/null

if [[ -z "${HF_TOKEN:-}" ]]; then
  echo "HF_TOKEN 이 필요합니다 (FLUX 모델은 Hugging Face에서 라이선스 동의 후 받을 수 있음)." >&2
  exit 1
fi

# ---- 1) 기준이미지 / 표정변형 / TTS 환경 (FLUX, edge-tts) ----
if [[ $WHAT == all || $WHAT == img ]]; then
  python3 -m venv $WS/venv-img
  $WS/venv-img/bin/pip install -q --upgrade pip
  $WS/venv-img/bin/pip install -q -r "$PROJECT_DIR/requirements-img.txt"
  $WS/venv-img/bin/hf download black-forest-labs/FLUX.1-dev --exclude "flux1-dev.safetensors" "ae.safetensors"
  $WS/venv-img/bin/hf download black-forest-labs/FLUX.1-Kontext-dev --exclude "flux1-kontext-dev.safetensors" "ae.safetensors"
fi

# ---- 2) 립싱크 환경 (InfiniteTalk = Wan2.1 I2V 14B + 오디오 조건) ----
if [[ $WHAT == all || $WHAT == talk ]]; then
  [[ -d $WS/InfiniteTalk ]] || git clone https://github.com/MeiGen-AI/InfiniteTalk.git $WS/InfiniteTalk
  python3 -m venv $WS/venv-talk
  PIP=$WS/venv-talk/bin/pip
  $PIP install -q --upgrade pip
  $PIP install -q torch==2.4.1 torchvision==0.19.1 torchaudio==2.4.1 --index-url https://download.pytorch.org/whl/cu121
  $PIP install -q xformers==0.0.28 --index-url https://download.pytorch.org/whl/cu121
  $PIP install -q "misaki[en]" ninja psutil packaging wheel huggingface_hub[cli] hf_transfer
  $PIP install -q flash_attn==2.7.4.post1 --no-build-isolation
  $PIP install -q -r $WS/InfiniteTalk/requirements.txt
  $PIP install -q librosa

  W=$WS/InfiniteTalk/weights
  HF=$WS/venv-talk/bin/hf
  $HF download Wan-AI/Wan2.1-I2V-14B-480P --local-dir $W/Wan2.1-I2V-14B-480P
  $HF download TencentGameMate/chinese-wav2vec2-base --local-dir $W/chinese-wav2vec2-base
  $HF download TencentGameMate/chinese-wav2vec2-base model.safetensors --revision refs/pr/1 --local-dir $W/chinese-wav2vec2-base
  $HF download MeiGen-AI/InfiniteTalk --include "single/*" --local-dir $W/InfiniteTalk
  # 고속 모드(--fast)용 LoRA (선택)
  $HF download vrgamedevgirl84/Wan14BT2VFusioniX FusionX_LoRa/Wan2.1_I2V_14B_FusionX_LoRA.safetensors --local-dir $W/tmp-lora \
    && mv $W/tmp-lora/FusionX_LoRa/Wan2.1_I2V_14B_FusionX_LoRA.safetensors $W/ \
    || echo "FusionX LoRA 다운로드 실패 - --fast 없이 사용하세요"
fi

echo
echo "설치 완료. 다음 단계는 README.md 의 '제작 순서'를 따르세요."
