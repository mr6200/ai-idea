#!/usr/bin/env python3
"""
유튜브 쇼츠 #01 "당신의 뇌가 매일 당신을 속이는 3가지 착각" 자동 제작 파이프라인.

단계:
  1. 대본 → Edge TTS 음성(ko-KR-SunHiNeural) + 단어 타이밍
  2. 실사 사진 배경 + Three.js 3D 오브젝트 + 모션 텍스트 장면(assets/scene.html)을
     Playwright(Chromium/WebGL) 로 프레임 단위 렌더링 (assets/render.js, 병렬)
  3. 배경음(신스 패드 + 비트) numpy 합성, 내레이션에 맞춰 더킹
  4. ffmpeg: 프레임 시퀀스 + 오디오 합성 → short_nosub.mp4
  5. 단어 하이라이트 ASS 자막 생성 → short.mp4 (번인), subtitles.srt
  6. 썸네일 PNG (assets/thumbnail.html)

실행: python3 build.py   (의존: ffmpeg(libass), playwright+chromium, edge-tts, pillow, numpy)
"""
import asyncio, json, os, shutil, subprocess, sys, urllib.request
from pathlib import Path

import numpy as np

# edge-tts 는 certifi 번들을 직접 읽으므로, 프록시 환경이면 CA 번들 경로를 넘겨준다.
if os.environ.get("SSL_CERT_FILE"):
    import certifi
    certifi.where = lambda: os.environ["SSL_CERT_FILE"]
import edge_tts

ROOT = Path(__file__).resolve().parent
ASSETS, WORK, OUT = ROOT / "assets", ROOT / "work", ROOT / "output"
FONT_DIR = ASSETS / "fonts"
FONT = FONT_DIR / "NotoSansKR.ttf"
FONT_URL = "https://raw.githubusercontent.com/google/fonts/main/ofl/notosanskr/NotoSansKR%5Bwght%5D.ttf"

W, H, FPS = 1080, 1920, 30
VOICE, RATE = "ko-KR-SunHiNeural", "+10%"
TRANS = 0.45          # 장면 전환 길이(초)
LEAD, TAIL = 0.30, 0.55   # 장면 시작 후 음성까지 / 음성 후 여백
LAST_HOLD = 1.3
INTRO = 1.5           # 영상 맨 앞 썸네일 노출 시간(초)

SCENES = [
    dict(id="hook", photo="brain_fill", bg_level=0.55, icon="brain", badge="매일 겪는 3가지 착각", num=None,
         head=["당신의 뇌는", "지금도 당신을", "<em>속이고 있다</em>"], sub="99%가 눈치채지 못합니다",
         accent="#ff4d6d", accent2="#7c3aed",
         tts="당신의 뇌는 지금 이 순간에도 당신을 속이고 있습니다. 매일 겪지만 아무도 눈치채지 못하는 세 가지 착각, 지금 공개합니다."),
    dict(id="one", photo="car", icon="car", badge="착각 1 / 3", num="1",
         head=["바더-마인호프", "<em>현상</em>"], sub="새 차를 사면 같은 차만 보이는 이유",
         accent="#38bdf8", accent2="#2563eb",
         tts="첫 번째, 바더 마인호프 현상. 새 차를 사면 갑자기 도로에 같은 차가 가득 보이죠? 차가 늘어난 게 아닙니다. 뇌가 방금 배운 것만 골라서 보여주는 겁니다."),
    dict(id="two", photo="tv", icon="tv", badge="착각 2 / 3", num="2",
         head=["자이가르닉", "<em>효과</em>"], sub="드라마가 결정적 순간에 끝나는 이유",
         accent="#a78bfa", accent2="#db2777",
         tts="두 번째, 자이가르닉 효과. 드라마가 왜 꼭 결정적인 순간에 끝날까요? 뇌는 끝내지 못한 일을 완료한 일보다 훨씬 오래 기억합니다. 그래서 다음 화를 참을 수 없는 거죠."),
    dict(id="three", photo="sale", icon="tag", badge="착각 3 / 3", num="3",
         head=["앵커링", "<em>효과</em>"], sub=None, price=("99,000원", "39,000원"),
         accent="#fbbf24", accent2="#f97316",
         tts="세 번째, 앵커링 효과. 정가 9만 9천 원에 줄을 긋고, 3만 9천 원. 6만 원을 아꼈다고 느끼시죠? 하지만 뇌는 처음 본 숫자에 닻을 내렸을 뿐입니다."),
    dict(id="outro", photo="hand", icon="chat", badge="당신은 몇 개?", num=None,
         head=["오늘 몇 개나", "<em>당하셨나요?</em>"], sub="댓글로 알려주세요 👇", cta="팔로우하면 다음 착각도 알려드려요",
         accent="#4ade80", accent2="#0ea5e9",
         tts="오늘 당신은 몇 개나 당하셨나요? 댓글로 알려주세요. 팔로우하면 다음 착각도 알려드릴게요."),
]


def run(cmd, **kw):
    print("$", " ".join(str(c) for c in cmd)[:300])
    subprocess.run([str(c) for c in cmd], check=True, **kw)


def ensure_font():
    if not FONT.exists():
        FONT_DIR.mkdir(parents=True, exist_ok=True)
        print("downloading Noto Sans KR ...")
        urllib.request.urlretrieve(FONT_URL, FONT)


# ---------------------------------------------------------------- 1. TTS
async def tts_one(text, mp3, meta):
    c = edge_tts.Communicate(text, VOICE, rate=RATE, boundary="WordBoundary")
    words = []
    with open(mp3, "wb") as f:
        async for ch in c.stream():
            if ch["type"] == "audio":
                f.write(ch["data"])
            elif ch["type"] == "WordBoundary":
                words.append(dict(t=ch["offset"] / 1e7, d=ch["duration"] / 1e7, w=ch["text"]))
    # 구두점 복원: 원문 공백 분리 토큰 수가 같으면 원문 토큰으로 표시
    src = text.split()
    if len(src) == len(words):
        for w, s in zip(words, src):
            w["w"] = s
    meta.write_text(json.dumps(words, ensure_ascii=False, indent=1), encoding="utf-8")


def decode_audio(path):
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", str(path), "-f", "f32le", "-ac", "1", "-ar", "44100", "-"],
                         check=True, capture_output=True).stdout
    return np.frombuffer(raw, dtype=np.float32).copy()


def make_voice():
    WORK.mkdir(exist_ok=True)
    loop = asyncio.new_event_loop()
    for s in SCENES:
        mp3, meta = WORK / f"{s['id']}.mp3", WORK / f"{s['id']}.json"
        if not (mp3.exists() and meta.exists()):
            print("TTS", s["id"])
            loop.run_until_complete(tts_one(s["tts"], mp3, meta))
        s["words"] = json.loads(meta.read_text(encoding="utf-8"))
        s["audio"] = decode_audio(mp3)
        # 앞뒤 무음 다듬기
        a = s["audio"]; thr = 0.01
        idx = np.where(np.abs(a) > thr)[0]
        s["audio"] = a[: idx[-1] + int(0.08 * 44100)] if len(idx) else a
        s["vdur"] = len(s["audio"]) / 44100
    # 타임라인
    t = 0.0
    for i, s in enumerate(SCENES):
        s["start"] = t
        s["voice_at"] = t + LEAD
        t = s["voice_at"] + s["vdur"] + (LAST_HOLD if i == len(SCENES) - 1 else TAIL)
    total = t
    for i, s in enumerate(SCENES):
        nxt = SCENES[i + 1]["start"] if i + 1 < len(SCENES) else total
        s["clip"] = nxt - s["start"] + (TRANS if i + 1 < len(SCENES) else 0)
    return total


# ---------------------------------------------------------------- 2. 장면 렌더링 (Three.js 프레임 시퀀스)
def word_time(s, prefix):
    """장면 s 의 단어 중 prefix 로 시작하는 첫 단어의 (음성 시작 기준) 시각."""
    for w in s["words"]:
        if w["w"].startswith(prefix):
            return round(w["t"] + LEAD, 2)
    return 1.0


def write_timeline(total):
    scenes = []
    for s in SCENES:
        cues = {}
        if s["id"] == "three":
            cues = dict(strike_at=word_time(s, "줄을"), new_at=word_time(s, "3만"))
        if s["id"] == "outro":
            cues = dict(cta_at=word_time(s, "팔로우"))
        scenes.append(dict(id=s["id"], photo=s["photo"], bg_level=s.get("bg_level"), accent=s["accent"], badge=s["badge"], num=s.get("num"),
                           head=s["head"], sub=s.get("sub"), price=s.get("price"), cta=s.get("cta"),
                           start=round(s["start"], 3), voice_at=round(s["voice_at"], 3), cues=cues))
    tl = dict(total=round(total, 3), fps=FPS, scenes=scenes)
    html = (ASSETS / "scene.html").read_text(encoding="utf-8").replace("__TIMELINE__", json.dumps(tl, ensure_ascii=False))
    (WORK / "scene.html").write_text(html, encoding="utf-8")
    (WORK / "timeline.json").write_text(json.dumps(tl, ensure_ascii=False, indent=1), encoding="utf-8")


def render_frames(total, workers=3):
    frames = WORK / "frames"
    n = int(round(total * FPS))
    run(["node", ASSETS / "render.js", "frames", ROOT, "work/scene.html", frames, n, FPS, workers])
    return frames, n


def render_thumbnail():
    run(["node", ASSETS / "render.js", "still", ROOT, "assets/thumbnail.html", OUT / "thumbnail.png"])


# ---------------------------------------------------------------- 3. 배경음
SR = 44100
NOTE = {"A2": 110.0, "C3": 130.81, "D3": 146.83, "E3": 164.81, "F3": 174.61, "G3": 196.0,
        "A3": 220.0, "C4": 261.63, "D4": 293.66, "E4": 329.63, "F4": 349.23, "G4": 392.0}
CHORDS = [["A2", "A3", "C4", "E4"], ["F3", "A3", "C4", "F4"], ["C3", "G3", "C4", "E4"], ["G3", "G3", "B3", "D4"]]
NOTE["B3"] = 246.94
BPM = 92


def make_music(total):
    n = int(total * SR) + SR
    out = np.zeros(n, dtype=np.float32)
    beat = 60 / BPM
    chord_len = beat * 8
    t_all = np.arange(n) / SR
    # 패드
    k = 0
    pos = 0.0
    while pos < total + 1:
        chord = CHORDS[k % len(CHORDS)]
        seg = slice(int(pos * SR), min(n, int((pos + chord_len) * SR)))
        t = t_all[seg] - pos
        env = np.minimum(1, t / 0.9) * np.minimum(1, (chord_len - t) / 1.2)
        env = np.clip(env, 0, 1)
        pad = np.zeros_like(t)
        for note in chord:
            f = NOTE[note]
            for det in (-0.4, 0.4):
                pad += np.sin(2 * np.pi * (f + det) * t) * 0.6
                pad += np.sin(2 * np.pi * (2 * f + det) * t) * 0.12
        out[seg] += pad * env * 0.035
        pos += chord_len
        k += 1
    # 소프트 킥 + 하이햇
    b = 0
    while b * beat < total + 1:
        i0 = int(b * beat * SR)
        tk = np.arange(int(0.22 * SR)) / SR
        kick = np.sin(2 * np.pi * (45 + 90 * np.exp(-tk * 28)) * tk) * np.exp(-tk * 14)
        seg = out[i0:i0 + len(tk)]
        seg += kick[: len(seg)] * (0.22 if b % 2 == 0 else 0.16)
        if b % 2 == 1:
            th = np.arange(int(0.05 * SR)) / SR
            rng = np.random.default_rng(b)
            hat = rng.standard_normal(len(th)) * np.exp(-th * 90) * 0.035
            seg = out[i0:i0 + len(th)]
            seg += hat[: len(seg)]
        b += 1
    # 페이드 아웃
    fo = int(1.5 * SR)
    end = int(total * SR)
    out[end - fo:end] *= np.linspace(1, 0, fo)
    out[end:] = 0
    return out[:end]


def intro_sfx(n):
    """썸네일 인트로용 라이저(노이즈 스윕) + 컷 시점의 임팩트 붐."""
    out = np.zeros(n, dtype=np.float32)
    rng = np.random.default_rng(7)
    L = int(INTRO * SR); t = np.arange(L) / SR
    noise = rng.standard_normal(L).astype(np.float32)
    # 간단한 원폴 로우패스 → 점점 열리는 느낌
    y = np.zeros(L, dtype=np.float32); a = 0.0
    cut = 0.02 + 0.25 * (t / INTRO) ** 2
    for i in range(L):
        a += cut[i] * (noise[i] - a); y[i] = a
    out[:L] += y * (0.02 + 0.16 * (t / INTRO) ** 2.2)
    tb = np.arange(int(0.9 * SR)) / SR
    boom = np.sin(2 * np.pi * (38 + 120 * np.exp(-tb * 18)) * tb) * np.exp(-tb * 4.5) * 0.7
    boom += rng.standard_normal(len(tb)).astype(np.float32) * np.exp(-tb * 40) * 0.25
    out[L:L + len(tb)] += boom[: max(0, min(len(tb), n - L))]
    return out


def mix_audio(total):
    n = int((total + INTRO) * SR)
    voice = np.zeros(n, dtype=np.float32)
    for s in SCENES:
        i0 = int((s["voice_at"] + INTRO) * SR)
        a = s["audio"]
        voice[i0:i0 + len(a)] += a[: n - i0]
    voice *= 0.89 / max(1e-6, np.abs(voice).max())
    music = np.zeros(n, dtype=np.float32)
    m = make_music(total); music[int(INTRO * SR):int(INTRO * SR) + len(m)] = m[: n - int(INTRO * SR)]
    music[: int(INTRO * SR)] = 0
    # 더킹: 음성 구간에서 배경음 감소
    envv = np.convolve(np.abs(voice), np.ones(int(0.25 * SR)) / int(0.25 * SR), mode="same")
    duck = 1 - 0.55 * np.clip(envv / 0.08, 0, 1)
    mix = voice + music * duck * 0.9 + intro_sfx(n)
    mix = np.clip(mix, -0.98, 0.98)
    wav = WORK / "mix.wav"
    run(["ffmpeg", "-y", "-v", "error", "-f", "f32le", "-ar", str(SR), "-ac", "1", "-i", "-", "-c:a", "pcm_s16le", str(wav)],
        input=mix.astype(np.float32).tobytes())
    run(["ffmpeg", "-y", "-v", "error", "-f", "f32le", "-ar", str(SR), "-ac", "1", "-i", "-", "-c:a", "libmp3lame", "-q:a", "2", str(OUT / "voice.mp3")],
        input=voice.astype(np.float32).tobytes())
    return wav


# ---------------------------------------------------------------- 4. 영상 합성
def build_video(total, wav, frames):
    nosub = OUT / "short_nosub.mp4"
    zoom = f"(1+0.07*t/{INTRO})"
    fc = (f"[0:v]scale=w='trunc(1080*{zoom}/2)*2':h='trunc(1920*{zoom}/2)*2':eval=frame,crop=1080:1920,setsar=1,format=yuv420p[intro];"
          f"[1:v]setsar=1,format=yuv420p[main];[intro][main]concat=n=2:v=1:a=0[v]")
    run(["ffmpeg", "-y", "-v", "error", "-stats",
         "-loop", "1", "-framerate", str(FPS), "-t", f"{INTRO:.3f}", "-i", str(OUT / "thumbnail.png"),
         "-framerate", str(FPS), "-i", str(frames / "%05d.jpg"), "-i", str(wav),
         "-filter_complex", fc, "-map", "[v]", "-map", "2:a",
         "-c:v", "libx264", "-preset", "medium", "-crf", "18", "-pix_fmt", "yuv420p", "-r", str(FPS),
         "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", "-t", f"{total + INTRO:.3f}", str(nosub)])
    return nosub


# ---------------------------------------------------------------- 5. 자막
def chunk_words(words, maxlen=9):
    chunks, cur = [], []
    for w in words:
        cand = " ".join(x["w"] for x in cur + [w])
        if cur and len(cand) > maxlen:
            chunks.append(cur); cur = []
        cur.append(w)
        last = w["w"][-1]
        if last in ".?!" or (last == "," and len(" ".join(x["w"] for x in cur)) >= 5):
            chunks.append(cur); cur = []
    if cur:
        chunks.append(cur)
    return chunks


def fmt_ass(t):
    h = int(t // 3600); m = int(t % 3600 // 60); s = t % 60
    return f"{h}:{m:02d}:{s:05.2f}"


def fmt_srt(t):
    h = int(t // 3600); m = int(t % 3600 // 60); s = int(t % 60); ms = int(round((t - int(t)) * 1000))
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"


def build_subtitles(total):
    header = f"""[Script Info]
ScriptType: v4.00+
PlayResX: {W}
PlayResY: {H}
WrapStyle: 2
ScaledBorderAndShadow: yes

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Sub,Noto Sans KR,100,&H00FFFFFF,&H00FFFFFF,&H00120C1E,&H9A000000,1,0,0,0,100,100,-2,0,1,10,5,2,40,40,430,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
    ev, srt, idx = [], [], 1
    for s in SCENES:
        base = s["voice_at"] + INTRO
        chunks = chunk_words(s["words"])
        for ci, ch in enumerate(chunks):
            c_start = base + ch[0]["t"]
            if ci + 1 < len(chunks):
                c_end = base + chunks[ci + 1][0]["t"] - 0.02
            else:
                c_end = base + ch[-1]["t"] + ch[-1]["d"] + 0.35
            text = " ".join(x["w"] for x in ch)
            srt.append(f"{idx}\n{fmt_srt(c_start)} --> {fmt_srt(c_end)}\n{text}\n"); idx += 1
            for wi, w in enumerate(ch):
                w_start = base + w["t"] if wi else c_start
                w_end = base + ch[wi + 1]["t"] if wi + 1 < len(ch) else c_end
                parts = []
                for x in ch:
                    if x is w:
                        parts.append("{\\c&H00E5FF&}" + x["w"] + "{\\c&HFFFFFF&}")
                    else:
                        parts.append(x["w"])
                pop = "{\\fscx86\\fscy86\\t(0,110,\\fscx100\\fscy100)}" if wi == 0 else ""
                ev.append(f"Dialogue: 0,{fmt_ass(w_start)},{fmt_ass(w_end)},Sub,,0,0,0,,{pop}{' '.join(parts)}")
    ass = OUT / "subtitles.ass"
    ass.write_text(header + "\n".join(ev) + "\n", encoding="utf-8")
    (OUT / "subtitles.srt").write_text("\n".join(srt), encoding="utf-8")
    return ass


def burn(nosub, ass):
    final = OUT / "short.mp4"
    vf = f"ass={ass.relative_to(ROOT).as_posix()}:fontsdir={FONT_DIR.relative_to(ROOT).as_posix()}"
    run(["ffmpeg", "-y", "-v", "error", "-stats", "-i", str(nosub), "-vf", vf,
         "-c:v", "libx264", "-preset", "medium", "-crf", "18", "-pix_fmt", "yuv420p", "-c:a", "copy",
         "-movflags", "+faststart", str(final)], cwd=str(ROOT))
    return final


def main():
    ensure_font()
    OUT.mkdir(exist_ok=True); WORK.mkdir(exist_ok=True)
    total = make_voice()
    print("timeline:")
    for s in SCENES:
        print(f"  {s['id']:6s} start={s['start']:6.2f}  voice={s['voice_at']:6.2f}  vdur={s['vdur']:5.2f}  clip={s['clip']:5.2f}")
    print(f"  total = {total:.2f}s")
    write_timeline(total)
    if "--no-frames" not in sys.argv:
        if "--clean" in sys.argv:
            shutil.rmtree(WORK / "frames", ignore_errors=True)
        frames, n = render_frames(total, workers=int(os.environ.get("WORKERS", "3")))
    else:
        frames = WORK / "frames"
    render_thumbnail()
    wav = mix_audio(total)
    nosub = build_video(total, wav, frames)
    ass = build_subtitles(total)
    final = burn(nosub, ass)
    print("done:", final)


if __name__ == "__main__":
    main()
