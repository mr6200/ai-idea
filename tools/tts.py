#!/usr/bin/env python3
"""대본 → 음성트랙.

대본 파일의 비어 있지 않은 줄 하나를 한 문장(컷)으로 보고 줄마다 음성을 만든 뒤,
문장 사이에 쉼을 넣어 하나의 음성트랙으로 이어 붙인다. Effectcraft에서 씬 타이밍을
맞출 수 있도록 각 줄의 시작/끝 시간을 timings.json에 남긴다.

엔진
  google : Google Cloud Text-to-Speech. 아래 인증 중 하나가 필요.
  local  : sherpa-onnx 오프라인 한국어 모델(품질 낮음, 파이프라인 확인용).
  auto   : Google 인증이 있으면 google, 없으면 local (기본값).

Google 인증 (위에서부터 먼저 찾은 것을 쓴다)
  GOOGLE_TTS_API_KEY             API 키
  GOOGLE_ADC_JSON                ADC JSON 내용 자체 (authorized_user 또는 service_account).
                                 `gcloud auth application-default login`이 만든
                                 application_default_credentials.json을 그대로 넣으면 된다.
  GOOGLE_APPLICATION_CREDENTIALS ADC JSON 파일 경로, 또는 gcloud 기본 ADC 파일
  GOOGLE_CLOUD_PROJECT           과금·할당량 프로젝트 ID. ADC JSON에 quota_project_id가
                                 없을 때 필요.

예시
  python3 tools/tts.py script.txt -o out/voice
  python3 tools/tts.py script.txt --voice ko-KR-Neural2-C --rate 1.05 --gap 0.4
"""
import argparse
import base64
import json
import os
import subprocess
import sys
import tarfile
import urllib.request
from pathlib import Path

GOOGLE_URL = "https://texttospeech.googleapis.com/v1/text:synthesize"
LOCAL_MODEL = "vits-mimic3-ko_KO-kss_low"
LOCAL_MODEL_URL = (
    "https://github.com/k2-fsa/sherpa-onnx/releases/download/tts-models/"
    f"{LOCAL_MODEL}.tar.bz2"
)
SAMPLE_RATE = 24000
SCOPES = ["https://www.googleapis.com/auth/cloud-platform"]


class GoogleAuth:
    """API 키 또는 ADC로 요청 URL과 헤더를 만든다."""

    def __init__(self, key=None, creds=None, project=None):
        self.key, self.creds, self.project = key, creds, project

    @classmethod
    def from_env(cls):
        if key := os.environ.get("GOOGLE_TTS_API_KEY"):
            return cls(key=key)
        try:
            import google.auth
            from google.auth.exceptions import DefaultCredentialsError
        except ImportError:
            return None
        project = os.environ.get("GOOGLE_CLOUD_PROJECT")
        if raw := os.environ.get("GOOGLE_ADC_JSON"):
            creds, _ = google.auth.load_credentials_from_dict(json.loads(raw), scopes=SCOPES)
        else:
            try:
                creds, default_project = google.auth.default(scopes=SCOPES)
            except DefaultCredentialsError:
                return None
            project = project or default_project
        project = project or getattr(creds, "quota_project_id", None)
        if not project:
            sys.exit("ADC를 찾았지만 프로젝트를 알 수 없습니다. GOOGLE_CLOUD_PROJECT를 설정하세요.")
        return cls(creds=creds, project=project)

    def describe(self):
        return "API 키" if self.key else f"ADC, 프로젝트 {self.project}"

    def request(self, url):
        headers = {"Content-Type": "application/json"}
        if self.key:
            return f"{url}?key={self.key}", headers
        from google.auth.exceptions import RefreshError
        from google.auth.transport.requests import Request

        if not self.creds.valid:
            try:
                self.creds.refresh(Request())
            except RefreshError as e:
                sys.exit(f"ADC 토큰 갱신 실패 (다시 로그인해 ADC JSON을 새로 받아야 할 수 있음): {e}")
        headers["Authorization"] = f"Bearer {self.creds.token}"
        headers["x-goog-user-project"] = self.project
        return url, headers


def google_tts(text, out_wav, voice, rate, pitch, auth):
    body = {
        "input": {"text": text},
        "voice": {"languageCode": voice[:5], "name": voice},
        "audioConfig": {
            "audioEncoding": "LINEAR16",
            "sampleRateHertz": SAMPLE_RATE,
            "speakingRate": rate,
        },
    }
    # Chirp3-HD 음성은 pitch를 받지 않는다.
    if "Chirp" not in voice:
        body["audioConfig"]["pitch"] = pitch
    url, headers = auth.request(GOOGLE_URL)
    req = urllib.request.Request(url, data=json.dumps(body).encode(), headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            audio = base64.b64decode(json.load(r)["audioContent"])
    except urllib.error.HTTPError as e:
        sys.exit(f"Google TTS 오류 {e.code}: {e.read().decode()[:500]}")
    out_wav.write_bytes(audio)


class LocalTTS:
    def __init__(self, cache_dir, rate):
        import sherpa_onnx

        d = cache_dir / LOCAL_MODEL
        if not d.exists():
            cache_dir.mkdir(parents=True, exist_ok=True)
            archive = cache_dir / f"{LOCAL_MODEL}.tar.bz2"
            print(f"로컬 모델 다운로드: {LOCAL_MODEL_URL}")
            urllib.request.urlretrieve(LOCAL_MODEL_URL, archive)
            with tarfile.open(archive) as t:
                t.extractall(cache_dir)
            archive.unlink()
        vits = sherpa_onnx.OfflineTtsVitsModelConfig(
            model=str(d / "ko_KO-kss_low.onnx"),
            tokens=str(d / "tokens.txt"),
            data_dir=str(d / "espeak-ng-data"),
        )
        cfg = sherpa_onnx.OfflineTtsConfig(
            model=sherpa_onnx.OfflineTtsModelConfig(vits=vits, num_threads=4)
        )
        self.tts = sherpa_onnx.OfflineTts(cfg)
        self.rate = rate

    def __call__(self, text, out_wav):
        import soundfile as sf

        a = self.tts.generate(text, sid=0, speed=self.rate)
        if not len(a.samples):
            sys.exit(f"로컬 TTS가 빈 음성을 반환했습니다: {text!r}")
        sf.write(str(out_wav), a.samples, a.sample_rate)


def duration(path):
    out = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "csv=p=0", str(path)],
        capture_output=True, text=True, check=True,
    )
    return float(out.stdout)


def normalize(src, dst):
    """엔진마다 다른 샘플레이트를 24kHz 모노로 맞춘다."""
    subprocess.run(
        ["ffmpeg", "-loglevel", "error", "-y", "-i", str(src),
         "-ar", str(SAMPLE_RATE), "-ac", "1", str(dst)],
        check=True,
    )


def main():
    p = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("script", type=Path, help="한 줄에 한 문장인 대본 텍스트")
    p.add_argument("-o", "--out", type=Path, default=Path("out/voice"))
    p.add_argument("--engine", choices=["auto", "google", "local"], default="auto")
    p.add_argument("--voice", default="ko-KR-Neural2-A",
                   help="Google 음성 이름 (예: ko-KR-Neural2-C, ko-KR-Chirp3-HD-Charon)")
    p.add_argument("--rate", type=float, default=1.0, help="말하기 속도")
    p.add_argument("--pitch", type=float, default=0.0, help="Google 전용, -20~20")
    p.add_argument("--gap", type=float, default=0.35, help="문장 사이 쉼(초)")
    args = p.parse_args()

    lines = [l.strip() for l in args.script.read_text(encoding="utf-8").splitlines()]
    lines = [l for l in lines if l and not l.startswith("#")]
    if not lines:
        sys.exit("대본에 읽을 줄이 없습니다.")

    auth = GoogleAuth.from_env() if args.engine != "local" else None
    engine = args.engine
    if engine == "auto":
        engine = "google" if auth else "local"
    if engine == "google" and not auth:
        sys.exit("Google 인증이 없습니다. GOOGLE_TTS_API_KEY 또는 GOOGLE_ADC_JSON을 설정하세요.")
    print(f"엔진: {engine}" +
          (f" ({args.voice}, {auth.describe()})" if engine == "google" else ""))

    line_dir = args.out / "lines"
    line_dir.mkdir(parents=True, exist_ok=True)
    local = None
    if engine == "local":
        local = LocalTTS(Path.home() / ".cache" / "tts-models", args.rate)

    timings, t = [], 0.0
    concat = []
    silence = args.out / "gap.wav"
    subprocess.run(
        ["ffmpeg", "-loglevel", "error", "-y", "-f", "lavfi",
         "-i", f"anullsrc=r={SAMPLE_RATE}:cl=mono", "-t", str(args.gap), str(silence)],
        check=True,
    )
    for i, text in enumerate(lines, 1):
        raw = line_dir / f"{i:03d}.raw.wav"
        wav = line_dir / f"{i:03d}.wav"
        if engine == "google":
            google_tts(text, raw, args.voice, args.rate, args.pitch, auth)
        else:
            local(text, raw)
        normalize(raw, wav)
        raw.unlink()
        d = duration(wav)
        timings.append({"index": i, "text": text, "file": str(wav.relative_to(args.out)),
                        "start": round(t, 3), "end": round(t + d, 3)})
        concat += [wav, silence]
        t += d + args.gap
        print(f"[{i:03d}] {d:5.2f}s  {text[:40]}")

    lst = args.out / "concat.txt"
    lst.write_text("".join(f"file '{f.resolve()}'\n" for f in concat[:-1]))
    track = args.out / "voice_track.wav"
    subprocess.run(
        ["ffmpeg", "-loglevel", "error", "-y", "-f", "concat", "-safe", "0",
         "-i", str(lst), "-c", "copy", str(track)],
        check=True,
    )
    subprocess.run(
        ["ffmpeg", "-loglevel", "error", "-y", "-i", str(track),
         "-b:a", "192k", str(args.out / "voice_track.mp3")],
        check=True,
    )
    lst.unlink()
    silence.unlink()

    meta = {"engine": engine, "voice": args.voice if engine == "google" else LOCAL_MODEL,
            "duration": round(duration(track), 3), "lines": timings}
    (args.out / "timings.json").write_text(json.dumps(meta, ensure_ascii=False, indent=2),
                                           encoding="utf-8")
    print(f"완료: {track} ({meta['duration']}s), {args.out / 'timings.json'}")


if __name__ == "__main__":
    main()
