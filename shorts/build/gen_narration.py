"""Narration track from Google Cloud Text-to-Speech, one clip per subtitle cue.

Reads the API key from GOOGLE_TTS_API_KEY. Clips are cached in tts/ so a rebuild
does not call the API again unless the text or voice changes. Each clip is
placed at its cue start; a clip longer than its window is sped up with ffmpeg
atempo (pitch kept) so it never runs into the next cue.
"""
import base64
import hashlib
import json
import os
import subprocess
import urllib.request
import wave

import numpy as np

ROOT = os.path.dirname(os.path.abspath(__file__))
CACHE = os.path.join(ROOT, "tts")
VOICE = "ko-KR-Chirp3-HD-Charon"
RATE = 1.08
SR = 48000
GAP = 0.08

# spoken forms where the on-screen text reads badly aloud
SPOKEN = {
    "0.1mm": "0.1밀리미터",
    "‘복리’": "복리",
    "A는": "에이는",
    "A가": "에이가",
    "B는": "비는",
    "…": ",",
}


def spoken(text):
    s = text.replace("\n", " ")
    for k, v in SPOKEN.items():
        s = s.replace(k, v)
    return s


def synthesize(text):
    key = hashlib.sha1(f"{VOICE}|{RATE}|{text}".encode()).hexdigest()[:16]
    path = os.path.join(CACHE, f"{key}.wav")
    if os.path.exists(path):
        return path
    body = json.dumps({
        "input": {"text": text},
        "voice": {"languageCode": "ko-KR", "name": VOICE},
        "audioConfig": {"audioEncoding": "LINEAR16", "sampleRateHertz": SR, "speakingRate": RATE},
    }).encode()
    req = urllib.request.Request(
        "https://texttospeech.googleapis.com/v1/text:synthesize", data=body,
        headers={"Content-Type": "application/json", "X-Goog-Api-Key": os.environ["GOOGLE_TTS_API_KEY"]})
    with urllib.request.urlopen(req, timeout=60) as r:
        audio = base64.b64decode(json.load(r)["audioContent"])
    os.makedirs(CACHE, exist_ok=True)
    with open(path, "wb") as f:
        f.write(audio)
    return path


def read_wav(path):
    with wave.open(path) as w:
        assert w.getframerate() == SR and w.getsampwidth() == 2, path
        x = np.frombuffer(w.readframes(w.getnframes()), "<i2").astype(np.float32) / 32768
        if w.getnchannels() == 2:
            x = x.reshape(-1, 2).mean(axis=1)
    # trim leading/trailing silence
    idx = np.where(np.abs(x) > 0.01)[0]
    return x[max(0, idx[0] - 480): idx[-1] + 2400] if len(idx) else x


def tempo(x, factor):
    src = os.path.join(CACHE, "_tmp_in.wav")
    dst = os.path.join(CACHE, "_tmp_out.wav")
    write_wav(src, x)
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", src, "-filter:a", f"atempo={factor:.4f}", dst], check=True)
    y = read_wav(dst)
    os.remove(src)
    os.remove(dst)
    return y


def write_wav(path, x, channels=1):
    pcm = (np.clip(x, -1, 1) * 32767).astype("<i2")
    with wave.open(path, "wb") as w:
        w.setnchannels(channels)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes(pcm.tobytes())


def main():
    with open(os.path.join(ROOT, "manifest.json")) as f:
        m = json.load(f)
    cues = m["cues"]
    track = np.zeros(int(m["duration"] * SR))
    report = []
    for i, c in enumerate(cues):
        clip = read_wav(synthesize(spoken(c["text"])))
        nxt = cues[i + 1]["start"] if i + 1 < len(cues) else m["duration"] - 0.3
        avail = nxt - c["start"] - GAP
        dur = len(clip) / SR
        if dur > avail:
            clip = tempo(clip, dur / avail)
        s = int(c["start"] * SR)
        track[s:s + len(clip)] += clip[:len(track) - s]
        report.append((c["start"], dur, avail))
    track *= 0.85 / max(1e-6, np.max(np.abs(track)))
    write_wav(os.path.join(ROOT, "narration.wav"), track)
    sped = [r for r in report if r[1] > r[2]]
    print(f"{len(cues)} clips, voice {VOICE}; {len(sped)} sped up, max factor "
          f"{max([r[1] / r[2] for r in sped], default=1):.2f}")


if __name__ == "__main__":
    main()
