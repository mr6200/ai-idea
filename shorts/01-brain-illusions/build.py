#!/usr/bin/env python3
"""
유튜브 쇼츠 #01 "당신의 뇌가 매일 당신을 속이는 3가지 착각" 자동 제작 파이프라인.

단계:
  1. 대본 → Edge TTS 음성(ko-KR-SunHiNeural) + 단어 타이밍
  2. 장면 HTML → Playwright(Chromium) 로 2x 해상도 PNG 렌더링
  3. 배경음(신스 패드 + 비트) numpy 합성, 내레이션에 맞춰 더킹
  4. ffmpeg: 장면별 줌 + 슬라이드 전환 + 오디오 합성 → short_nosub.mp4
  5. 단어 하이라이트 ASS 자막 생성 → short.mp4 (번인), subtitles.srt
  6. 썸네일 PNG

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

SCENES = [
    dict(id="hook", icon="brain", badge="매일 겪는 3가지 착각", num=None,
         head=["당신의 뇌는", "지금도 당신을", "<em>속이고 있다</em>"], sub="99%가 눈치채지 못합니다",
         accent="#ff4d6d", accent2="#7c3aed",
         tts="당신의 뇌는 지금 이 순간에도 당신을 속이고 있습니다. 매일 겪지만 아무도 눈치채지 못하는 세 가지 착각, 지금 공개합니다."),
    dict(id="one", icon="car", badge="착각 1 / 3", num="1",
         head=["바더-마인호프", "<em>현상</em>"], sub="새 차를 사면 같은 차만 보이는 이유",
         accent="#38bdf8", accent2="#2563eb",
         tts="첫 번째, 바더 마인호프 현상. 새 차를 사면 갑자기 도로에 같은 차가 가득 보이죠? 차가 늘어난 게 아닙니다. 뇌가 방금 배운 것만 골라서 보여주는 겁니다."),
    dict(id="two", icon="tv", badge="착각 2 / 3", num="2",
         head=["자이가르닉", "<em>효과</em>"], sub="드라마가 결정적 순간에 끝나는 이유",
         accent="#a78bfa", accent2="#db2777",
         tts="두 번째, 자이가르닉 효과. 드라마가 왜 꼭 결정적인 순간에 끝날까요? 뇌는 끝내지 못한 일을 완료한 일보다 훨씬 오래 기억합니다. 그래서 다음 화를 참을 수 없는 거죠."),
    dict(id="three", icon="tag", badge="착각 3 / 3", num="3",
         head=["앵커링", "<em>효과</em>"], sub=None, price=("99,000원", "39,000원"),
         accent="#fbbf24", accent2="#f97316",
         tts="세 번째, 앵커링 효과. 정가 9만 9천 원에 줄을 긋고, 3만 9천 원. 6만 원을 아꼈다고 느끼시죠? 하지만 뇌는 처음 본 숫자에 닻을 내렸을 뿐입니다."),
    dict(id="outro", icon="chat", badge="당신은 몇 개?", num=None,
         head=["오늘 몇 개나", "<em>당하셨나요?</em>"], sub="댓글로 알려주세요 👇", cta="팔로우하면 다음 착각도 알려드려요",
         accent="#34d399", accent2="#0ea5e9",
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


# ---------------------------------------------------------------- 2. 장면 렌더링
CSS = """
@font-face{font-family:'NSKR';src:url('file://%(font)s');font-weight:100 900;}
*{margin:0;padding:0;box-sizing:border-box}
html,body{width:1080px;height:1920px;overflow:hidden;background:#0b0f1e;font-family:'NSKR',sans-serif;color:#fff}
body{position:relative}
.blob{position:absolute;border-radius:50%%;filter:blur(90px);opacity:.65}
.b1{width:780px;height:780px;left:-220px;top:120px;background:%(accent)s}
.b2{width:720px;height:720px;right:-240px;top:980px;background:%(accent2)s}
.grid{position:absolute;inset:0;background-image:linear-gradient(rgba(255,255,255,.045) 1px,transparent 1px),linear-gradient(90deg,rgba(255,255,255,.045) 1px,transparent 1px);background-size:90px 90px;mask-image:radial-gradient(circle at 50%% 45%%,#000 30%%,transparent 75%%);-webkit-mask-image:radial-gradient(circle at 50%% 45%%,#000 30%%,transparent 75%%)}
.vignette{position:absolute;inset:0;background:radial-gradient(ellipse at 50%% 50%%,transparent 55%%,rgba(0,0,0,.55) 100%%)}
.wrap{position:absolute;inset:0;display:flex;flex-direction:column;align-items:center;text-align:center;padding-top:240px}
.badge{display:inline-flex;align-items:center;gap:14px;padding:16px 38px;border-radius:999px;background:rgba(255,255,255,.1);border:2px solid rgba(255,255,255,.22);font-size:40px;font-weight:700;letter-spacing:1px;backdrop-filter:blur(10px)}
.badge .dot{width:16px;height:16px;border-radius:50%%;background:%(accent)s;box-shadow:0 0 18px %(accent)s}
.iconwrap{position:relative;margin-top:44px;width:380px;height:380px;display:flex;align-items:center;justify-content:center}
.iconwrap::before{content:'';position:absolute;inset:0;border-radius:50%%;background:radial-gradient(circle,%(accent)s55,transparent 68%%)}
.iconwrap img{width:280px;height:280px;filter:drop-shadow(0 24px 40px rgba(0,0,0,.55))}
.num{position:absolute;right:-10px;top:10px;width:120px;height:120px;border-radius:50%%;background:%(accent)s;color:#0b0f1e;font-size:72px;font-weight:900;display:flex;align-items:center;justify-content:center;box-shadow:0 10px 30px rgba(0,0,0,.4);border:6px solid #0b0f1e}
h1{margin-top:36px;font-size:%(hsize)spx;line-height:1.14;font-weight:900;letter-spacing:-3px;text-shadow:0 10px 40px rgba(0,0,0,.5)}
h1 em{font-style:normal;color:%(accent)s}
.sub{margin-top:28px;font-size:52px;font-weight:500;color:rgba(255,255,255,.82);letter-spacing:-1px}
.price{margin-top:34px;display:flex;align-items:center;gap:34px;font-weight:900}
.price .old{font-size:70px;color:rgba(255,255,255,.55);text-decoration:line-through;text-decoration-color:#ff4d6d;text-decoration-thickness:8px}
.price .arrow{font-size:60px;color:rgba(255,255,255,.6)}
.price .new{font-size:104px;color:%(accent)s;text-shadow:0 0 40px %(accent)s88}
.cta{margin-top:40px;padding:22px 52px;border-radius:24px;background:%(accent)s;color:#0b0f1e;font-size:44px;font-weight:900;box-shadow:0 14px 40px %(accent)s66}
.brand{position:absolute;bottom:90px;left:0;right:0;text-align:center;font-size:30px;font-weight:700;letter-spacing:6px;color:rgba(255,255,255,.35)}
"""


def scene_html(s):
    hsize = 112 if len(s["head"]) >= 3 else 126
    css = CSS % dict(font=FONT, accent=s["accent"], accent2=s["accent2"], hsize=hsize)
    head = "<br>".join(s["head"])
    num = f'<div class="num">{s["num"]}</div>' if s.get("num") else ""
    sub = f'<div class="sub">{s["sub"]}</div>' if s.get("sub") else ""
    price = ""
    if s.get("price"):
        o, n = s["price"]
        price = f'<div class="price"><span class="old">{o}</span><span class="arrow">→</span><span class="new">{n}</span></div>'
    cta = f'<div class="cta">{s["cta"]}</div>' if s.get("cta") else ""
    icon = (ASSETS / "icons" / f"{s['icon']}.svg").as_uri()
    return f"""<!doctype html><html lang="ko"><head><meta charset="utf-8"><style>{css}</style></head><body>
<div class="blob b1"></div><div class="blob b2"></div><div class="grid"></div><div class="vignette"></div>
<div class="wrap">
  <div class="badge"><span class="dot"></span>{s['badge']}</div>
  <div class="iconwrap"><img src="{icon}">{num}</div>
  <h1>{head}</h1>{sub}{price}{cta}
</div>
<div class="brand">BRAIN HACKS</div>
</body></html>"""


THUMB_HTML = """<!doctype html><html lang="ko"><head><meta charset="utf-8"><style>%(css)s
.wrap{padding-top:250px}
.iconwrap{margin-top:40px}
.top{font-size:66px;font-weight:700;color:rgba(255,255,255,.9);letter-spacing:-1px}
h1{font-size:196px;line-height:1.02;margin-top:30px;letter-spacing:-8px}
.three{display:inline-block;color:#0b0f1e;background:#ffd400;padding:0 34px;border-radius:30px;transform:rotate(-3deg);box-shadow:0 20px 50px rgba(0,0,0,.45)}
.iconwrap{margin-top:40px;width:560px;height:560px}
.iconwrap img{width:430px;height:430px}
.bottom{margin-top:30px;padding:26px 60px;border-radius:999px;background:#ff2d55;font-size:62px;font-weight:900;letter-spacing:-1px;box-shadow:0 18px 50px rgba(255,45,85,.5)}
</style></head><body>
<div class="blob b1"></div><div class="blob b2"></div><div class="grid"></div><div class="vignette"></div>
<div class="wrap">
  <div class="top">99%%가 매일 당하는</div>
  <h1>뇌의 착각<br><span class="three">3가지</span></h1>
  <div class="iconwrap"><img src="%(icon)s"></div>
  <div class="bottom">당신도 지금 속고 있다</div>
</div>
<div class="brand">BRAIN HACKS</div>
</body></html>"""


def render_scenes():
    pages = []
    for s in SCENES:
        p = WORK / f"{s['id']}.html"
        p.write_text(scene_html(s), encoding="utf-8")
        pages.append((p, WORK / f"{s['id']}.png", 2))
    css = CSS % dict(font=FONT, accent="#ff4d6d", accent2="#7c3aed", hsize=120)
    th = WORK / "thumbnail.html"
    th.write_text(THUMB_HTML % dict(css=css, icon=(ASSETS / "icons" / "brain.svg").as_uri()), encoding="utf-8")
    pages.append((th, OUT / "thumbnail.png", 1))
    js = WORK / "render.js"
    js.write_text("""
const { chromium } = require('playwright');
const jobs = JSON.parse(process.argv[2]);
(async () => {
  const browser = await chromium.launch();
  for (const [html, png, scale] of jobs) {
    const ctx = await browser.newContext({ viewport: { width: 1080, height: 1920 }, deviceScaleFactor: scale });
    const page = await ctx.newPage();
    await page.goto('file://' + html, { waitUntil: 'networkidle' });
    await page.evaluate(() => document.fonts.ready);
    await page.waitForTimeout(150);
    await page.screenshot({ path: png, type: 'png' });
    await ctx.close();
    console.log('rendered', png);
  }
  await browser.close();
})();
""")
    run(["node", js, json.dumps([[str(a), str(b), c] for a, b, c in pages])], cwd=str(WORK))


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


def mix_audio(total):
    n = int(total * SR)
    voice = np.zeros(n, dtype=np.float32)
    for s in SCENES:
        i0 = int(s["voice_at"] * SR)
        a = s["audio"]
        voice[i0:i0 + len(a)] += a[: n - i0]
    voice *= 0.89 / max(1e-6, np.abs(voice).max())
    music = make_music(total)
    # 더킹: 음성 구간에서 배경음 감소
    envv = np.convolve(np.abs(voice), np.ones(int(0.25 * SR)) / int(0.25 * SR), mode="same")
    duck = 1 - 0.55 * np.clip(envv / 0.08, 0, 1)
    mix = voice + music * duck * 0.9
    mix = np.clip(mix, -0.98, 0.98)
    wav = WORK / "mix.wav"
    run(["ffmpeg", "-y", "-v", "error", "-f", "f32le", "-ar", str(SR), "-ac", "1", "-i", "-", "-c:a", "pcm_s16le", str(wav)],
        input=mix.astype(np.float32).tobytes())
    run(["ffmpeg", "-y", "-v", "error", "-f", "f32le", "-ar", str(SR), "-ac", "1", "-i", "-", "-c:a", "libmp3lame", "-q:a", "2", str(OUT / "voice.mp3")],
        input=voice.astype(np.float32).tobytes())
    return wav


# ---------------------------------------------------------------- 4. 영상 합성
def build_video(total, wav):
    cmd = ["ffmpeg", "-y", "-v", "error", "-stats"]
    fc = []
    for i, s in enumerate(SCENES):
        cmd += ["-i", str(WORK / f"{s['id']}.png")]
        frames = int(round(s["clip"] * FPS))
        if i % 2 == 0:
            z = f"1+0.09*on/{frames}"
        else:
            z = f"1.09-0.09*on/{frames}"
        fc.append(f"[{i}:v]zoompan=z='{z}':d={frames}:x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':s={W}x{H}:fps={FPS},"
                  f"format=yuv420p,setpts=PTS-STARTPTS[v{i}]")
    cmd += ["-i", str(wav)]
    prev = "v0"
    transitions = ["slideup", "slideup", "slideleft", "slideup", "smoothleft"]
    for i in range(1, len(SCENES)):
        off = SCENES[i]["start"] - TRANS
        outl = f"x{i}" if i < len(SCENES) - 1 else "vout"
        fc.append(f"[{prev}][v{i}]xfade=transition={transitions[i % len(transitions)]}:duration={TRANS}:offset={off:.3f}[{outl}]")
        prev = outl
    nosub = OUT / "short_nosub.mp4"
    cmd += ["-filter_complex", ";".join(fc), "-map", "[vout]", "-map", f"{len(SCENES)}:a",
            "-c:v", "libx264", "-preset", "medium", "-crf", "18", "-pix_fmt", "yuv420p", "-r", str(FPS),
            "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", "-t", f"{total:.3f}", str(nosub)]
    run(cmd)
    return nosub


# ---------------------------------------------------------------- 5. 자막
def chunk_words(words, maxlen=12):
    chunks, cur = [], []
    for w in words:
        cand = " ".join(x["w"] for x in cur + [w])
        if cur and len(cand) > maxlen:
            chunks.append(cur); cur = []
        cur.append(w)
        if w["w"][-1] in ".?!," and len(" ".join(x["w"] for x in cur)) >= 5:
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
Style: Sub,Noto Sans KR,74,&H00FFFFFF,&H00FFFFFF,&H00120C1E,&H9A000000,1,0,0,0,100,100,-1,0,1,8,4,2,50,50,440,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
    ev, srt, idx = [], [], 1
    for s in SCENES:
        base = s["voice_at"]
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
    render_scenes()
    wav = mix_audio(total)
    nosub = build_video(total, wav)
    ass = build_subtitles(total)
    final = burn(nosub, ass)
    print("done:", final)


if __name__ == "__main__":
    main()
