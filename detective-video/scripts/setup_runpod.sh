#!/usr/bin/env bash
# RunPod Pod 최초 1회 설정. 모든 것을 /workspace(네트워크 볼륨)에 설치하므로
# Pod를 껐다 켜도 다시 받을 필요가 없습니다.
#
#   export HF_TOKEN=hf_xxx            # FLUX.1-dev / Kontext 라이선스 동의한 계정의 토큰
#   bash scripts/setup_runpod.sh            # 전부
#   bash scripts/setup_runpod.sh img        # 이미지/음성 환경만
#   bash scripts/setup_runpod.sh talk       # 립싱크 환경만 (InfiniteTalk)
#   bash scripts/setup_runpod.sh wan22      # 립싱크 환경만 (Wan2.2-S2V-14B, 기본 엔진)
set -euo pipefail

WS=/workspace
PROJECT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
export HF_HOME=$WS/hf-cache
export HF_HUB_ENABLE_HF_TRANSFER=1
WHAT=${1:-all}

apt-get update -qq && apt-get install -y -qq ffmpeg fonts-nanum python3-venv git >/dev/null
fc-cache -f >/dev/null

if [[ -z "${HF_TOKEN:-}" && ( $WHAT == all || $WHAT == img ) ]]; then
  echo "HF_TOKEN 없음: FLUX.1-dev/Kontext 대신 토큰이 필요 없는 FLUX.1-schnell 을 받습니다 (표정 변형 단계는 사용 불가)." >&2
fi

# ---- 1) 기준이미지 / 표정변형 / TTS 환경 (FLUX, edge-tts) ----
if [[ $WHAT == all || $WHAT == img ]]; then
  python3 -m venv $WS/venv-img
  $WS/venv-img/bin/pip install -q --upgrade pip
  $WS/venv-img/bin/pip install -q -r "$PROJECT_DIR/requirements-img.txt"
  if [[ -n "${HF_TOKEN:-}" ]]; then
    $WS/venv-img/bin/hf download black-forest-labs/FLUX.1-dev --exclude "flux1-dev.safetensors" "ae.safetensors"
    $WS/venv-img/bin/hf download black-forest-labs/FLUX.1-Kontext-dev --exclude "flux1-kontext-dev.safetensors" "ae.safetensors"
  else
    $WS/venv-img/bin/hf download black-forest-labs/FLUX.1-schnell --exclude "flux1-schnell.safetensors" "ae.safetensors"
  fi
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

# ---- 3) 립싱크 환경 (Wan 2.2 S2V-14B: 이미지 + 음성 -> 말하는 영상) ----
if [[ $WHAT == all || $WHAT == wan22 ]]; then
  [[ -d $WS/Wan2.2 ]] || git clone https://github.com/Wan-Video/Wan2.2.git $WS/Wan2.2
  python3 -m venv $WS/venv-wan22
  PIP=$WS/venv-wan22/bin/pip
  $PIP install -q --upgrade pip
  $PIP install -q torch==2.5.1 torchvision==0.20.1 torchaudio==2.5.1 --index-url https://download.pytorch.org/whl/cu124
  $PIP install -q ninja psutil packaging wheel "huggingface_hub[cli]" hf_transfer
  # flash_attn 은 소스 빌드에 수 시간이 걸릴 수 있어 제외 (Wan은 없으면 PyTorch SDPA 사용)
  for req in requirements.txt requirements_s2v.txt; do
    if [[ -f $WS/Wan2.2/$req ]]; then
      grep -v -i flash_attn $WS/Wan2.2/$req > /tmp/wan22-$req
      $PIP install -q -r /tmp/wan22-$req
    fi
  done
  $WS/venv-wan22/bin/hf download Wan-AI/Wan2.2-S2V-14B --local-dir $WS/Wan2.2/Wan2.2-S2V-14B
fi

echo
echo "설치 완료. 다음 단계는 README.md 의 '제작 순서'를 따르세요."
