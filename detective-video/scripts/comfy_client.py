"""ComfyUI API로 Wan 2.2 워크플로를 실행하는 클라이언트.

- 기준이미지: Wan2.2 T2V A14B (high/low noise 2단계)로 1프레임만 생성 = 텍스트->이미지
- 립싱크:    Wan2.2 S2V 14B (기준이미지 + 음성 -> 말하는 영상), 77프레임씩 이어붙여 대사 길이만큼 생성

ComfyUI 주소는 COMFY_URL (기본 http://127.0.0.1:8188). 모델 파일 이름은 환경변수로 바꿀 수 있습니다.
"""
import json
import math
import os
import time
import urllib.parse
import urllib.request
import uuid
from pathlib import Path

COMFY_URL = os.environ.get("COMFY_URL", "http://127.0.0.1:8188")

T2V_HIGH = os.environ.get("WAN22_T2V_HIGH", "wan2.2_t2v_high_noise_14B_fp16.safetensors")
T2V_LOW = os.environ.get("WAN22_T2V_LOW", "wan2.2_t2v_low_noise_14B_fp16.safetensors")
S2V_MODEL = os.environ.get("WAN22_S2V", "wan2.2_s2v_14B_fp8_scaled.safetensors")
TEXT_ENCODER = os.environ.get("WAN22_TEXT_ENCODER", "umt5_xxl_fp8_e4m3fn_scaled.safetensors")
VAE = os.environ.get("WAN22_VAE", "wan_2.1_vae.safetensors")
AUDIO_ENCODER = os.environ.get("WAN22_AUDIO_ENCODER", "wav2vec2_large_english_fp16.safetensors")

S2V_FPS = 16
S2V_CHUNK = 77  # S2V 한 번에 만드는 프레임 수

NEGATIVE = ("blurry, low quality, distorted face, deformed, extra fingers, bad anatomy, watermark, text, "
            "subtitles, overexposed, static, worst quality, jpeg artifacts, cartoon, anime")


def _request(path, data=None, headers=None):
    req = urllib.request.Request(COMFY_URL + path, data=data, headers=headers or {})
    with urllib.request.urlopen(req, timeout=120) as r:
        return r.read()


def upload(path):
    """input 폴더로 파일 업로드 (이미지/오디오 모두 /upload/image 사용)."""
    path = Path(path)
    boundary = uuid.uuid4().hex
    body = (f"--{boundary}\r\nContent-Disposition: form-data; name=\"image\"; filename=\"{path.name}\"\r\n"
            f"Content-Type: application/octet-stream\r\n\r\n").encode() + path.read_bytes() + \
           f"\r\n--{boundary}\r\nContent-Disposition: form-data; name=\"overwrite\"\r\n\r\ntrue\r\n--{boundary}--\r\n".encode()
    res = json.loads(_request("/upload/image", body, {"Content-Type": f"multipart/form-data; boundary={boundary}"}))
    return res["name"]


def run(workflow, poll=5):
    """워크플로를 큐에 넣고 끝날 때까지 기다린 뒤 출력 파일 목록을 돌려준다."""
    prompt_id = json.loads(_request("/prompt", json.dumps({"prompt": workflow}).encode(),
                                    {"Content-Type": "application/json"}))["prompt_id"]
    while True:
        hist = json.loads(_request(f"/history/{prompt_id}"))
        if prompt_id in hist:
            entry = hist[prompt_id]
            status = entry.get("status", {})
            if status.get("status_str") == "error":
                msgs = [m for m in status.get("messages", []) if m[0] == "execution_error"]
                raise RuntimeError(f"ComfyUI 실행 오류: {json.dumps(msgs, ensure_ascii=False)[:2000]}")
            files = []
            for out in entry.get("outputs", {}).values():
                for key in ("images", "gifs", "videos"):
                    files += out.get(key, [])
            return files
        time.sleep(poll)


def download(file_info, dst):
    q = urllib.parse.urlencode({"filename": file_info["filename"], "subfolder": file_info.get("subfolder", ""),
                                "type": file_info.get("type", "output")})
    Path(dst).write_bytes(_request(f"/view?{q}"))


def t2i_workflow(prompt, width, height, seed, steps=20, cfg=3.5, prefix="ref"):
    """Wan2.2 T2V A14B로 1프레임 = 정지 이미지 생성."""
    half = steps // 2
    return {
        "1": {"class_type": "UNETLoader", "inputs": {"unet_name": T2V_HIGH, "weight_dtype": "fp8_e4m3fn"}},
        "2": {"class_type": "UNETLoader", "inputs": {"unet_name": T2V_LOW, "weight_dtype": "fp8_e4m3fn"}},
        "3": {"class_type": "ModelSamplingSD3", "inputs": {"model": ["1", 0], "shift": 8.0}},
        "4": {"class_type": "ModelSamplingSD3", "inputs": {"model": ["2", 0], "shift": 8.0}},
        "5": {"class_type": "CLIPLoader", "inputs": {"clip_name": TEXT_ENCODER, "type": "wan"}},
        "6": {"class_type": "CLIPTextEncode", "inputs": {"clip": ["5", 0], "text": prompt}},
        "7": {"class_type": "CLIPTextEncode", "inputs": {"clip": ["5", 0], "text": NEGATIVE}},
        "8": {"class_type": "VAELoader", "inputs": {"vae_name": VAE}},
        "9": {"class_type": "EmptyHunyuanLatentVideo",
              "inputs": {"width": width, "height": height, "length": 1, "batch_size": 1}},
        "10": {"class_type": "KSamplerAdvanced", "inputs": {
            "model": ["3", 0], "add_noise": "enable", "noise_seed": seed, "steps": steps, "cfg": cfg,
            "sampler_name": "euler", "scheduler": "simple", "positive": ["6", 0], "negative": ["7", 0],
            "latent_image": ["9", 0], "start_at_step": 0, "end_at_step": half,
            "return_with_leftover_noise": "enable"}},
        "11": {"class_type": "KSamplerAdvanced", "inputs": {
            "model": ["4", 0], "add_noise": "disable", "noise_seed": seed, "steps": steps, "cfg": cfg,
            "sampler_name": "euler", "scheduler": "simple", "positive": ["6", 0], "negative": ["7", 0],
            "latent_image": ["10", 0], "start_at_step": half, "end_at_step": 10000,
            "return_with_leftover_noise": "disable"}},
        "12": {"class_type": "VAEDecode", "inputs": {"samples": ["11", 0], "vae": ["8", 0]}},
        "13": {"class_type": "SaveImage", "inputs": {"images": ["12", 0], "filename_prefix": prefix}},
    }


def s2v_chunks(duration):
    return max(1, math.ceil(duration * S2V_FPS / S2V_CHUNK))


def s2v_workflow(prompt, image_name, audio_name, duration, width, height, seed,
                 steps=20, cfg=6.0, prefix="lipsync"):
    """Wan2.2 S2V: 첫 77프레임 생성 후 Extend 노드로 대사 길이만큼 이어붙인다."""
    wf = {
        "1": {"class_type": "UNETLoader", "inputs": {"unet_name": S2V_MODEL, "weight_dtype": "default"}},
        "2": {"class_type": "ModelSamplingSD3", "inputs": {"model": ["1", 0], "shift": 8.0}},
        "3": {"class_type": "CLIPLoader", "inputs": {"clip_name": TEXT_ENCODER, "type": "wan"}},
        "4": {"class_type": "CLIPTextEncode", "inputs": {"clip": ["3", 0], "text": prompt}},
        "5": {"class_type": "CLIPTextEncode", "inputs": {"clip": ["3", 0], "text": NEGATIVE}},
        "6": {"class_type": "VAELoader", "inputs": {"vae_name": VAE}},
        "7": {"class_type": "LoadImage", "inputs": {"image": image_name}},
        "8": {"class_type": "LoadAudio", "inputs": {"audio": audio_name}},
        "9": {"class_type": "AudioEncoderLoader", "inputs": {"audio_encoder_name": AUDIO_ENCODER}},
        "10": {"class_type": "AudioEncoderEncode", "inputs": {"audio_encoder": ["9", 0], "audio": ["8", 0]}},
        "11": {"class_type": "WanSoundImageToVideo", "inputs": {
            "positive": ["4", 0], "negative": ["5", 0], "vae": ["6", 0], "width": width, "height": height,
            "length": S2V_CHUNK, "batch_size": 1, "audio_encoder_output": ["10", 0], "ref_image": ["7", 0]}},
        "12": {"class_type": "KSampler", "inputs": {
            "model": ["2", 0], "seed": seed, "steps": steps, "cfg": cfg, "sampler_name": "uni_pc",
            "scheduler": "simple", "positive": ["11", 0], "negative": ["11", 1], "latent_image": ["11", 2],
            "denoise": 1.0}},
    }
    latent = ["12", 0]
    for i in range(1, s2v_chunks(duration)):
        ext, ks, cat = f"ext{i}", f"ks{i}", f"cat{i}"
        wf[ext] = {"class_type": "WanSoundImageToVideoExtend", "inputs": {
            "positive": ["4", 0], "negative": ["5", 0], "vae": ["6", 0], "length": S2V_CHUNK,
            "video_latent": latent, "audio_encoder_output": ["10", 0], "ref_image": ["7", 0]}}
        wf[ks] = {"class_type": "KSampler", "inputs": {
            "model": ["2", 0], "seed": seed + i, "steps": steps, "cfg": cfg, "sampler_name": "uni_pc",
            "scheduler": "simple", "positive": [ext, 0], "negative": [ext, 1], "latent_image": [ext, 2],
            "denoise": 1.0}}
        wf[cat] = {"class_type": "LatentConcat", "inputs": {"samples1": latent, "samples2": [ks, 0], "dim": "t"}}
        latent = [cat, 0]
    wf["90"] = {"class_type": "VAEDecode", "inputs": {"samples": latent, "vae": ["6", 0]}}
    wf["91"] = {"class_type": "VHS_VideoCombine", "inputs": {
        "images": ["90", 0], "audio": ["8", 0], "frame_rate": S2V_FPS, "loop_count": 0,
        "filename_prefix": prefix, "format": "video/h264-mp4", "pix_fmt": "yuv420p", "crf": 17,
        "save_metadata": False, "trim_to_audio": False, "pingpong": False, "save_output": True}}
    return wf


IT_BASE = os.environ.get("IT_BASE_MODEL", "Wan2_1-I2V-14B-480p_fp8_e4m3fn_scaled_KJ.safetensors")
IT_MODEL = os.environ.get("IT_MODEL", "Wan2_1-InfiniTetalk-Single_fp16.safetensors")
IT_LORA = os.environ.get("IT_LORA", "lightx2v_I2V_14B_480p_cfg_step_distill_rank64_bf16.safetensors")
IT_TEXT_ENCODER = os.environ.get("IT_TEXT_ENCODER", "umt5-xxl-enc-bf16.safetensors")
IT_FPS = 25


def infinitetalk_workflow(prompt, image_name, audio_name, duration, width, height, seed,
                          steps=6, prefix="infinitetalk"):
    """InfiniteTalk (ComfyUI-WanVideoWrapper): 기준이미지 + 음성 -> 말하는 영상, 25fps.

    lightx2v 증류 LoRA로 6스텝 / cfg 1. 81프레임 창을 9프레임씩 겹쳐 대사 길이만큼 이어서 생성한다.
    """
    num_frames = math.ceil(duration * IT_FPS) + 1
    return {
        "1": {"class_type": "WanVideoBlockSwap", "inputs": {
            "blocks_to_swap": 20, "offload_img_emb": False, "offload_txt_emb": False,
            "use_non_blocking": True, "vace_blocks_to_swap": 0, "prefetch_blocks": 1, "block_swap_debug": False}},
        "2": {"class_type": "WanVideoLoraSelect", "inputs": {"lora": IT_LORA, "strength": 1.0, "low_mem_load": False, "merge_loras": False}},
        "3": {"class_type": "MultiTalkModelLoader", "inputs": {"model": IT_MODEL}},
        "4": {"class_type": "WanVideoModelLoader", "inputs": {
            "model": IT_BASE, "base_precision": "bf16", "quantization": "fp8_e4m3fn_scaled",
            "load_device": "offload_device", "attention_mode": "sageattn",
            "block_swap_args": ["1", 0], "lora": ["2", 0], "multitalk_model": ["3", 0], "rms_norm_function": "default"}},
        "5": {"class_type": "WanVideoVAELoader", "inputs": {"model_name": VAE, "precision": "bf16", "use_cpu_cache": False, "verbose": False}},
        "6": {"class_type": "CLIPVisionLoader", "inputs": {"clip_name": "clip_vision_h.safetensors"}},
        "7": {"class_type": "LoadImage", "inputs": {"image": image_name}},
        "8": {"class_type": "ImageResizeKJv2", "inputs": {
            "image": ["7", 0], "width": width, "height": height, "upscale_method": "lanczos",
            "keep_proportion": "stretch", "pad_color": "0, 0, 0", "crop_position": "center", "divisible_by": 16,
            "device": "cpu"}},
        "9": {"class_type": "WanVideoClipVisionEncode", "inputs": {
            "clip_vision": ["6", 0], "image_1": ["8", 0], "strength_1": 1.0, "strength_2": 1.0,
            "crop": "center", "combine_embeds": "average", "force_offload": True, "tiles": 0, "ratio": 0.5}},
        "10": {"class_type": "WanVideoTextEncodeCached", "inputs": {
            "model_name": IT_TEXT_ENCODER, "precision": "bf16", "positive_prompt": prompt,
            "negative_prompt": NEGATIVE, "quantization": "disabled", "use_disk_cache": False, "device": "gpu"}},
        "11": {"class_type": "LoadAudio", "inputs": {"audio": audio_name}},
        "12": {"class_type": "Wav2VecModelLoader", "inputs": {
            "model": "wav2vec2-chinese-base_fp16.safetensors", "base_precision": "fp16", "load_device": "main_device"}},
        "13": {"class_type": "MultiTalkWav2VecEmbeds", "inputs": {
            "wav2vec_model": ["12", 0], "audio_1": ["11", 0], "normalize_loudness": True,
            "num_frames": num_frames, "fps": IT_FPS, "audio_scale": 1.0, "audio_cfg_scale": 1.0,
            "multi_audio_type": "para", "add_noise_floor": False, "smooth_transients": False}},
        "14": {"class_type": "WanVideoImageToVideoMultiTalk", "inputs": {
            "vae": ["5", 0], "width": width, "height": height, "frame_window_size": 81, "motion_frame": 9,
            "force_offload": False, "colormatch": "disabled", "start_image": ["8", 0], "tiled_vae": False,
            "clip_embeds": ["9", 0], "mode": "infinitetalk", "output_path": ""}},
        "15": {"class_type": "WanVideoSampler", "inputs": {
            "model": ["4", 0], "image_embeds": ["14", 0], "text_embeds": ["10", 0], "multitalk_embeds": ["13", 0],
            "steps": steps, "cfg": 1.0, "shift": 11.0, "seed": seed, "force_offload": True,
            "scheduler": "dpm++_sde", "riflex_freq_index": 0, "denoise_strength": 1.0, "batched_cfg": False,
            "rope_function": "comfy", "start_step": 0, "end_step": -1, "add_noise_to_samples": True}},
        "16": {"class_type": "WanVideoPassImagesFromSamples", "inputs": {"samples": ["15", 0]}},
        "17": {"class_type": "VHS_VideoCombine", "inputs": {
            "images": ["16", 0], "audio": ["11", 0], "frame_rate": IT_FPS, "loop_count": 0,
            "filename_prefix": prefix, "format": "video/h264-mp4", "pix_fmt": "yuv420p", "crf": 17,
            "save_metadata": False, "trim_to_audio": False, "pingpong": False, "save_output": True}},
    }


LC_LORA = os.environ.get("LC_LORA", "longcat-avatar-dmd_lora.safetensors")
LC_VAE = os.environ.get("LC_VAE", "LongCat-Video-Avatar-vae.safetensors")
LC_WHISPER = os.environ.get("LC_WHISPER", "whisper-large-v3.safetensors")
LC_FPS = 25


def longcat_workflow(prompt, image_name, audio_name, seed, resolution="720p", block_num=1, prefix="longcat"):
    """LongCat-Video-Avatar 1.5 (ComfyUI-LongCat-Avatar 노드): Whisper-large-v3 음성 조건, 증류 LoRA 8스텝, 25fps.

    대사 길이에 맞춰 구간 수를 노드가 자동 계산한다. 텍스트 인코더는 ComfyUI의 umt5 fp8 (Load CLIP) 사용.
    """
    return {
        "1": {"class_type": "LongCat_Video_SM_Model", "inputs": {
            "inference_weight_mode": "official_int8_sharded", "attention_mode": "sageattn",
            "auto_download_missing_weights": True, "vae": LC_VAE, "lora": LC_LORA}},
        "2": {"class_type": "CLIPLoader", "inputs": {"clip_name": TEXT_ENCODER, "type": "wan"}},
        "3": {"class_type": "LongCat_Video_SM_Encode", "inputs": {
            "text_encoder_root": "LongCat-Video", "auto_download_missing_text_encoder": False,
            "offload_device": "cpu", "prompt": prompt, "negative_prompt": NEGATIVE, "clip": ["2", 0]}},
        "4": {"class_type": "LoadImage", "inputs": {"image": image_name}},
        "5": {"class_type": "LoadAudio", "inputs": {"audio": audio_name}},
        "6": {"class_type": "LongCat_Video_SM_WhisperModel", "inputs": {"audio_encoder": LC_WHISPER}},
        "7": {"class_type": "LongCat_Video_SM_Audio", "inputs": {
            "audio_encoder": ["6", 0], "audio": ["5", 0], "save_fps": LC_FPS, "audio_type": "para", "p_box": ""}},
        "8": {"class_type": "LongCat_Video_SM_Sampler", "inputs": {
            "model": ["1", 0], "te_cond": ["3", 0], "au_cond": ["7", 0], "stage_1": "ai2v",
            "resolution": resolution, "seed": seed, "steps": 8, "text_guidance_scale": 1.0,
            "audio_guidance_scale": 1.0, "ref_img_index": 10, "mask_frame_range": 3, "block_num": block_num,
            "mux_audio_path": "", "offload_device": "cpu", "debug_mode": False, "image": ["4", 0]}},
        "9": {"class_type": "VHS_VideoCombine", "inputs": {
            "images": ["8", 0], "audio": ["5", 0], "frame_rate": LC_FPS, "loop_count": 0,
            "filename_prefix": prefix, "format": "video/h264-mp4", "pix_fmt": "yuv420p", "crf": 17,
            "save_metadata": False, "trim_to_audio": False, "pingpong": False, "save_output": True}},
    }
