#!/usr/bin/env python3
"""spec.json -> 1080x1920 실사 쇼츠 영상(mp4).

  - 사진마다 Ken Burns(천천히 패닝/줌) 효과
  - 문장 단위 TTS 나레이션(edge-tts, 무료) + 정확히 싱크된 큰 자막
  - 상단 숙소 정보(순위 배지, 숙소명, 위치, 가격 칩), 장면 전환 크로스페이드
  - 선택: BGM (파일 경로 또는 "synth" = 잔잔한 자체 생성 패드)

usage: python build_short.py projects/<name> [--preview]
"""
import argparse
import asyncio
import hashlib
import json
import math
import os
import re
import subprocess
import sys
import wave
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

W, H, FPS = 1080, 1920, 30
SR = 24000                      # 오디오 샘플레이트
GAP = 0.12                      # 문장 사이 쉼(초)
XFADE = 0.25                    # 장면 전환 크로스페이드(초)
ROOT = Path(__file__).resolve().parent
YELLOW = (255, 214, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)


# ---------------------------------------------------------------- fonts / text
def font(kind, size):
    if kind == "title":
        return ImageFont.truetype(str(ROOT / "fonts/BlackHanSans-Regular.ttf"), size)
    f = ImageFont.truetype(str(ROOT / "fonts/NotoSansKR-VF.ttf"), size)
    try:
        f.set_variation_by_axes([{"bold": 700, "black": 900, "medium": 500}.get(kind, 400)])
    except Exception:
        pass
    return f


def rich_words(para):
    """'*강조*' 표시를 해석해 단어 목록 [[(조각, 강조여부), ...], ...] 으로."""
    words, hl = [[]], False
    for ch in para:
        if ch == "*":
            hl = not hl
            continue
        if ch == " ":
            if words[-1]:
                words.append([])
            continue
        w = words[-1]
        if w and w[-1][1] == hl:
            w[-1] = (w[-1][0] + ch, hl)
        else:
            w.append((ch, hl))
    return [w for w in words if w]


def layout(text, f, max_w):
    space = f.getlength(" ")
    lines = []
    for para in text.split("\n"):
        cur, cur_w = [], 0.0
        for word in rich_words(para):
            ww = sum(f.getlength(p) for p, _ in word)
            if cur and cur_w + space + ww > max_w:
                lines.append((cur, cur_w))
                cur, cur_w = [], 0.0
            cur_w += (space if cur else 0) + ww
            cur.append(word)
        lines.append((cur, cur_w))
    return lines


def draw_rich(img, text, f, cx, top, max_w, color=WHITE, hl=YELLOW, stroke=8,
              line_gap=1.22, shadow=True, align="center"):
    """중앙(또는 좌측) 정렬 강조 텍스트를 그린다. 그려진 높이를 반환."""
    lines = layout(text, f, max_w)
    lh = f.size * line_gap
    layer = Image.new("RGBA", img.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    space = f.getlength(" ")
    for i, (words, lw) in enumerate(lines):
        x = cx - lw / 2 if align == "center" else cx
        y = top + i * lh
        for word in words:
            for piece, is_hl in word:
                d.text((x, y), piece, font=f, fill=hl if is_hl else color,
                       stroke_width=stroke, stroke_fill=BLACK)
                x += f.getlength(piece)
            x += space
    if shadow:
        a = layer.getchannel("A").filter(ImageFilter.GaussianBlur(10))
        sh = Image.new("RGBA", img.size, (0, 0, 0, 0))
        sh.putalpha(a.point(lambda v: int(v * 0.55)))
        img.alpha_composite(sh, (0, 8))
    img.alpha_composite(layer)
    return len(lines) * lh


def strip_marks(s):
    return s.replace("*", "").replace("\n", " ")


# ---------------------------------------------------------------- overlays
def gradient(img, y0, y1, a0, a1):
    d = ImageDraw.Draw(img)
    for y in range(y0, y1):
        t = (y - y0) / max(1, y1 - y0 - 1)
        d.line([(0, y), (W, y)], fill=(0, 0, 0, int(a0 + (a1 - a0) * t)))


def pill(img, xy, text, f, bg, fg, pad=(26, 12), radius=None):
    d = ImageDraw.Draw(img)
    x, y = xy
    l, t, r, b = d.textbbox((0, 0), text, font=f)
    w, h = r - l + pad[0] * 2, b - t + pad[1] * 2
    d.rounded_rectangle([x, y, x + w, y + h], radius=radius or h // 2, fill=bg)
    d.text((x + pad[0] - l, y + pad[1] - t), text, font=f, fill=fg)
    return w, h


def header_overlay(scene, spec):
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    gradient(img, 0, 640, 170, 0)
    gradient(img, 980, H, 0, 175)

    if "hook" in scene or "outro" in scene:
        box = scene.get("hook") or scene.get("outro")
        gradient(img, 0, H, 70, 70)  # 전체 살짝 어둡게
        top_y = 560 if "hook" in scene else 620
        if box.get("top"):
            draw_rich(img, box["top"], font("black", 64), W / 2, top_y, 960, stroke=6)
        draw_rich(img, box["big"], font("title", 150), W / 2, top_y + 120, 980, stroke=12)
        if scene.get("footer"):
            f = font("bold", 40)
            d = ImageDraw.Draw(img)
            tw = d.textlength(scene["footer"], font=f)
            pill(img, (int(W / 2 - tw / 2 - 30), 1250), scene["footer"], f,
                 (255, 255, 255, 230), BLACK, pad=(30, 16))
        return img

    hotel = spec.get("hotels", {}).get(scene.get("hotel"))
    if not hotel:
        return img
    x = 80
    y = 170
    if hotel.get("badge"):
        _, bh = pill(img, (x, y), hotel["badge"], font("title", 52), YELLOW, BLACK, pad=(30, 14))
        y += bh + 22
    name_f = font("title", 104)
    while name_f.getlength(hotel["name"]) > W - 160 and name_f.size > 60:
        name_f = font("title", name_f.size - 4)
    draw_rich(img, hotel["name"], name_f, x, y, W - 160, align="left", stroke=7)
    y += int(name_f.size * 1.2)
    if hotel.get("place"):
        draw_rich(img, hotel["place"], font("bold", 44), x + 4, y, W - 160, align="left",
                  stroke=4, shadow=False)
        y += 76
    cx = x
    chip_f = font("bold", 38)
    for chip in hotel.get("chips", []):
        cw, ch = pill(img, (cx, y), chip, chip_f, (255, 255, 255, 235), (20, 20, 20), pad=(24, 12))
        cx += cw + 14
    if hotel.get("chips") and spec.get("price_note"):
        draw_rich(img, spec["price_note"], font("medium", 28), x + 4, y + 82, W, align="left",
                  stroke=3, shadow=False)
    return img


def caption_overlay(text):
    """자막 이미지(잘라낸 RGBA)와 붙일 위치."""
    img = Image.new("RGBA", (W, 700), (0, 0, 0, 0))
    draw_rich(img, text, font("title", 88), W / 2, 60, 920, stroke=10)
    bbox = img.getbbox() or (0, 0, 1, 1)
    crop = img.crop(bbox)
    return crop, (bbox[0], 1080 + bbox[1])   # 자막 영역 시작 y≈1140


# ---------------------------------------------------------------- Ken Burns
class Shot:
    def __init__(self, path, idx, focus=None, motion="auto"):
        im = Image.open(path).convert("RGB")
        # 출력 대비 1.25배 정도 해상도로 미리 줄여서 속도 확보
        scale = max(W * 1.35 / im.width, H * 1.15 / im.height)
        if scale < 1:
            im = im.resize((round(im.width * scale), round(im.height * scale)), Image.LANCZOS)
        self.im = im
        iw, ih = im.size
        aspect = W / H
        # 화면 비율(9:16)을 덮는 최대 사각형
        if iw / ih > aspect:
            bh = ih
            bw = ih * aspect
        else:
            bw = iw
            bh = iw / aspect
        fx = 0.5 if focus is None else focus
        if motion == "auto":
            motion = "pan" if iw / ih > 0.9 else "zoom"
        d = 1 if idx % 2 == 0 else -1
        if motion == "pan":
            travel = min(iw - bw * 0.95, iw * 0.22)
            c0 = fx * iw - d * travel / 2
            c1 = fx * iw + d * travel / 2
            s0, s1 = 1.0 * 0.97, 0.92 * 0.97
        else:
            c0 = c1 = fx * iw
            s0, s1 = 1.0, 0.86
        self.rects = []
        for c, s in ((c0, s0), (c1, s1)):
            w, h = bw * s, bh * s
            cx = min(max(c, w / 2), iw - w / 2)
            cy = ih / 2
            self.rects.append((cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2))

    def frame(self, p):
        p = max(0.0, min(1.0, p))
        e = p * 0.85 + (0.5 - 0.5 * math.cos(math.pi * p)) * 0.15   # 거의 등속 + 살짝 이징
        r = [a + (b - a) * e for a, b in zip(*self.rects)]
        return self.im.transform((W, H), Image.Transform.EXTENT, r, Image.Resampling.BILINEAR)


# ---------------------------------------------------------------- audio
def ssl_patch():
    ca = os.environ.get("SSL_CERT_FILE")
    if ca and os.path.exists(ca):
        import ssl
        import edge_tts.communicate as c
        c._SSL_CTX = ssl.create_default_context(cafile=ca)


async def tts_all(jobs, voice, rate):
    import edge_tts
    for text, out in jobs:
        if out.exists() and out.stat().st_size > 0:
            continue
        for attempt in range(4):
            try:
                await edge_tts.Communicate(text, voice, rate=rate).save(str(out))
                break
            except Exception as e:
                if attempt == 3:
                    raise
                print(f"  TTS 재시도 ({e})")
                await asyncio.sleep(2 * (attempt + 1))


def load_pcm(mp3, wav):
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(mp3), "-ac", "1", "-ar", str(SR),
                    "-sample_fmt", "s16", str(wav)], check=True)
    with wave.open(str(wav)) as w:
        a = np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16).astype(np.float32) / 32768
    # 앞뒤 무음 정리 (40ms 여유)
    idx = np.where(np.abs(a) > 0.01)[0]
    if len(idx):
        pad = int(0.04 * SR)
        a = a[max(0, idx[0] - pad): idx[-1] + pad]
    return a


def synth_bgm(seconds):
    """잔잔한 코드 패드 + 플럭 아르페지오 (저작권 걱정 없는 자체 생성 BGM)."""
    t = np.arange(int(seconds * SR)) / SR
    out = np.zeros_like(t)
    bpm = 96
    bar = 4 * 60 / bpm
    prog = [[60, 64, 67, 71], [57, 60, 64, 67], [53, 57, 60, 64], [55, 59, 62, 65]]  # Cmaj7 Am7 Fmaj7 G7
    hz = lambda m: 440 * 2 ** ((m - 69) / 12)
    n_bars = int(seconds / bar) + 1
    for b in range(n_bars):
        chord = prog[b % 4]
        s, e = int(b * bar * SR), min(len(t), int((b + 1) * bar * SR))
        if s >= len(t):
            break
        tt = t[s:e] - t[s]
        env = np.minimum(1, tt / 0.6) * np.minimum(1, (bar - tt) / 0.4)
        for m in chord:
            f = hz(m - 12)
            out[s:e] += env * 0.06 * (np.sin(2 * np.pi * f * tt) + 0.3 * np.sin(2 * np.pi * 2 * f * tt + 1))
        out[s:e] += env * 0.08 * np.sin(2 * np.pi * hz(chord[0] - 24) * tt)
        step = 60 / bpm / 2
        for k in range(8):
            ps = s + int(k * step * SR)
            pe = min(e, ps + int(0.5 * SR))
            if ps >= e:
                break
            pt = t[ps:pe] - t[ps]
            note = chord[[0, 2, 1, 3, 2, 1, 3, 2][k]] + 12
            out[ps:pe] += 0.05 * np.exp(-pt * 7) * np.sin(2 * np.pi * hz(note) * pt)
    fade = int(1.5 * SR)
    out[:fade] *= np.linspace(0, 1, fade)
    out[-fade:] *= np.linspace(1, 0, fade)
    return out / (np.max(np.abs(out)) + 1e-9) * 0.9


def write_wav(path, a):
    a = np.clip(a, -1, 1)
    with wave.open(str(path), "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes((a * 32767).astype(np.int16).tobytes())


# ---------------------------------------------------------------- main
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("project")
    ap.add_argument("--preview", action="store_true", help="장면별 미리보기 PNG만 생성")
    args = ap.parse_args()

    proj = Path(args.project)
    spec = json.loads((proj / "spec.json").read_text(encoding="utf-8"))
    build = proj / "build"
    out_dir = proj / "output"
    build.mkdir(exist_ok=True)
    out_dir.mkdir(exist_ok=True)
    voice, rate = spec.get("voice", "ko-KR-SunHiNeural"), spec.get("rate", "+10%")

    # 1) 문장별 TTS
    scenes = spec["scenes"]
    jobs = []
    for sc in scenes:
        sc["lines"] = [l if isinstance(l, dict) else {"text": l} for l in sc["lines"]]
        for ln in sc["lines"]:
            say = ln.get("say") or strip_marks(ln["text"])
            key = hashlib.md5(f"{voice}|{rate}|{say}".encode()).hexdigest()[:12]
            ln["mp3"] = build / f"tts_{key}.mp3"
            jobs.append((say, ln["mp3"]))
    print("TTS 생성 중...")
    ssl_patch()
    asyncio.run(tts_all(jobs, voice, rate))

    # 2) 타임라인 + 오디오
    t = 0.0
    voice_parts = []
    for sc in scenes:
        sc["start"] = t
        for ln in sc["lines"]:
            pcm = load_pcm(ln["mp3"], ln["mp3"].with_suffix(".wav"))
            ln["start"], ln["end"] = t, t + len(pcm) / SR
            voice_parts.append((t, pcm))
            t = ln["end"] + GAP
        t += sc.get("hold", 0.15)
        sc["end"] = t
    total = t + 0.3
    voice_track = np.zeros(int(total * SR) + SR)
    for st, pcm in voice_parts:
        s = int(st * SR)
        voice_track[s:s + len(pcm)] += pcm
    voice_track = voice_track[:int(total * SR)]
    mix = voice_track * 0.95
    if spec.get("bgm"):
        if spec["bgm"] == "synth":
            bgm = synth_bgm(total)
        else:
            tmp = build / "bgm.wav"
            subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-stream_loop", "-1", "-i",
                            str(proj / spec["bgm"]), "-t", f"{total}", "-ac", "1", "-ar", str(SR), str(tmp)],
                           check=True)
            with wave.open(str(tmp)) as w:
                bgm = np.frombuffer(w.readframes(w.getnframes()), np.int16).astype(np.float32) / 32768
            fade = int(1.5 * SR)
            bgm[-fade:] *= np.linspace(1, 0, fade)
        bgm = np.pad(bgm, (0, max(0, len(mix) - len(bgm))))[:len(mix)]
        # 나레이션 중엔 BGM 살짝 줄이기(덕킹)
        env = np.convolve(np.abs(voice_track), np.ones(SR // 5) / (SR // 5), mode="same")
        duck = 1 - 0.45 * np.clip(env / 0.05, 0, 1)
        mix = mix + bgm * spec.get("bgm_volume", 0.1) * duck
    write_wav(build / "audio.wav", mix)
    print(f"길이: {total:.1f}초")

    # 3) 이미지/오버레이 준비
    for i, sc in enumerate(scenes):
        sc["shot"] = Shot(proj / "images" / f"{sc['image']}.jpg", i, sc.get("focus"), sc.get("motion", "auto"))
        sc["header"] = header_overlay(sc, spec)
        for ln in sc["lines"]:
            ln["cap"] = caption_overlay(ln["text"]) if sc.get("captions", True) else None

    def render(time_s):
        idx = next((i for i, s in enumerate(scenes) if s["start"] <= time_s < s["end"]), len(scenes) - 1)
        sc = scenes[idx]
        p = (time_s - sc["start"]) / (sc["end"] - sc["start"])
        frame = sc["shot"].frame(p).convert("RGBA")
        if idx > 0 and time_s - sc["start"] < XFADE:
            prev = scenes[idx - 1]
            pf = prev["shot"].frame(1.0).convert("RGBA")
            pf.alpha_composite(prev["header"])
            a = (time_s - sc["start"]) / XFADE
            frame.alpha_composite(sc["header"])
            frame = Image.blend(pf, frame, a)
        else:
            frame.alpha_composite(sc["header"])
        cur = None
        for ln in sc["lines"]:
            if ln["start"] - 0.05 <= time_s:
                cur = ln
        if cur and cur["cap"]:
            cap, (cx, cy) = cur["cap"]
            age = time_s - (cur["start"] - 0.05)
            if age < 0.14:            # 팝 애니메이션
                k = age / 0.14
                s = 0.82 + 0.18 * (1 - (1 - k) ** 3)
                cw, ch = cap.size
                c2 = cap.resize((max(1, int(cw * s)), max(1, int(ch * s))), Image.BILINEAR)
                alpha = c2.getchannel("A").point(lambda v: int(v * min(1, k * 1.6)))
                c2.putalpha(alpha)
                frame.alpha_composite(c2, (int(cx + cw * (1 - s) / 2), int(cy + ch * (1 - s) / 2)))
            else:
                frame.alpha_composite(cap, (cx, cy))
        return frame.convert("RGB")

    if args.preview:
        for i, sc in enumerate(scenes):
            tm = sc["lines"][-1]["start"] + 0.5
            render(tm).save(out_dir / f"preview_{i:02d}.jpg", quality=88)
        print(f"미리보기 저장: {out_dir}")
        return

    # 4) 렌더링 → ffmpeg
    out = out_dir / f"{proj.name}.mp4"
    n = int(total * FPS)
    enc = subprocess.Popen([
        "ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}",
        "-r", str(FPS), "-i", "-", "-i", str(build / "audio.wav"),
        "-c:v", "libx264", "-preset", "medium", "-crf", "19", "-pix_fmt", "yuv420p",
        "-c:a", "aac", "-b:a", "192k", "-shortest", "-movflags", "+faststart", str(out)],
        stdin=subprocess.PIPE)
    for i in range(n):
        enc.stdin.write(render(i / FPS).tobytes())
        if i % (FPS * 5) == 0:
            print(f"  렌더링 {i / FPS:5.1f}s / {total:.1f}s", flush=True)
    enc.stdin.close()
    enc.wait()

    # 5) 업로드용 설명(출처 표기 포함)
    credits = json.loads((proj / "credits.json").read_text(encoding="utf-8")) if (proj / "credits.json").exists() else []
    used = {sc["image"] for sc in scenes}
    lines = [spec.get("title", ""), "", " ".join(spec.get("hashtags", [])), "",
             "※ 가격은 날짜·시즌·환율에 따라 달라질 수 있어요.", "", "📷 사진 출처"]
    for c in credits:
        if c["key"] in used:
            lines.append(f"- {c['title']} / {c.get('artist') or 'unknown'} / {c.get('license', '')} {c.get('page', '')}".rstrip())
    lines += ["", "🎙 나레이션: Microsoft Edge TTS"]
    (out_dir / "description.txt").write_text("\n".join(lines), encoding="utf-8")
    print(f"완료: {out}")


if __name__ == "__main__":
    main()
