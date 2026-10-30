"""Synthesize the BGM and SFX track for the hidden-money Short (60 s, 48 kHz stereo WAV) from the manifest.

Everything is generated here with numpy, so there are no licensing questions.
"""
import json
import os
import wave

import numpy as np

ROOT = os.path.dirname(os.path.abspath(__file__))
SR = 48000
DUR = 60.0
rng = np.random.default_rng(42)


def env(n, attack=0.005, decay=0.3):
    t = np.arange(n) / SR
    a = np.clip(t / attack, 0, 1)
    return a * np.exp(-t / decay)


def tone(freq, dur, decay, harmonics=((1, 1.0), (4, 0.25), (10, 0.06))):
    n = int(dur * SR)
    t = np.arange(n) / SR
    out = np.zeros(n)
    for mult, amp in harmonics:
        out += amp * np.sin(2 * np.pi * freq * mult * t) * np.exp(-t / (decay / mult ** 0.5))
    return out * env(n, 0.003, 10)


def noise(dur):
    return rng.standard_normal(int(dur * SR))


def lowpass(x, cutoff):
    a = np.exp(-2 * np.pi * cutoff / SR)
    y = np.empty_like(x)
    acc = 0.0
    for i, v in enumerate(x):
        acc = (1 - a) * v + a * acc
        y[i] = acc
    return y


def midi(n):
    return 440.0 * 2 ** ((n - 69) / 12)


# ---------------------------------------------------------------- BGM
def bgm():
    # a few seconds of headroom: the last bar may start just before DUR and is trimmed below
    out = np.zeros(int((DUR + 5) * SR))
    bpm = 96
    beat = 60 / bpm
    bar = beat * 4
    # Cmaj7 - Am7 - Fmaj7 - G6, voiced around middle C
    chords = [[60, 64, 67, 71], [57, 60, 64, 67], [53, 57, 60, 64], [55, 59, 62, 64]]
    roots = [36, 33, 29, 31]
    arp = [0, 2, 1, 3, 2, 1, 3, 2]
    pluck = {}
    t = 0.0
    i = 0
    while t < DUR:
        ch = chords[i % 4]
        for k, idx in enumerate(arp):
            st = t + k * beat / 2
            note = ch[idx] + (12 if k in (3, 6) else 0)
            if note not in pluck:
                pluck[note] = tone(midi(note), 0.9, 0.35)
            s = int(st * SR)
            seg = pluck[note] * (0.16 if k % 2 == 0 else 0.11)
            out[s:s + len(seg)] += seg[:len(out) - s]
        # bass on beats 1 and 3
        for b in (0, 2):
            s = int((t + b * beat) * SR)
            seg = tone(midi(roots[i % 4]), 1.2, 0.5, ((1, 1.0), (2, 0.3))) * 0.22
            out[s:s + len(seg)] += seg[:len(out) - s]
        # soft kick + hat
        for b in range(4):
            s = int((t + b * beat) * SR)
            if b in (0, 2):
                n = int(0.18 * SR)
                tt = np.arange(n) / SR
                k = np.sin(2 * np.pi * (50 + 70 * np.exp(-tt * 30)) * tt) * np.exp(-tt * 18) * 0.25
                out[s:s + n] += k[:len(out) - s]
            for h in (0, 0.5):
                hs = int((t + (b + h) * beat) * SR)
                hn = noise(0.03) * env(int(0.03 * SR), 0.001, 0.008) * 0.025
                out[hs:hs + len(hn)] += hn[:len(out) - hs]
        t += bar
        i += 1
    out = out[:int(DUR * SR)]
    # warm it up and fade the ends
    out = 0.7 * lowpass(out, 3800) + 0.3 * out
    fade = np.ones_like(out)
    fi, fo = int(1.0 * SR), int(3.0 * SR)
    fade[:fi] = np.linspace(0, 1, fi)
    fade[-fo:] = np.linspace(1, 0, fo)
    return out * fade


# ---------------------------------------------------------------- SFX
def sfx_pop():
    n = int(0.09 * SR)
    t = np.arange(n) / SR
    return np.sin(2 * np.pi * (900 * np.exp(-t * 25) + 300) * t) * np.exp(-t * 40) * 0.35


def sfx_whoosh(dur=0.45):
    x = lowpass(noise(dur), 1800)
    n = len(x)
    e = np.sin(np.linspace(0, np.pi, n)) ** 2
    return x * e * 0.5


def sfx_fold():
    x = lowpass(noise(0.07), 3000) * env(int(0.07 * SR), 0.001, 0.02) * 0.9
    n = int(0.12 * SR)
    t = np.arange(n) / SR
    th = np.sin(2 * np.pi * 120 * t) * np.exp(-t * 35) * 0.4
    y = np.zeros(n)
    y[:len(x)] += x
    return y + th


def sfx_ding(f=1568):
    return tone(f, 1.4, 0.5, ((1, 1.0), (2.76, 0.4), (5.4, 0.15))) * 0.3


def sfx_coin():
    a = tone(2093, 0.5, 0.18, ((1, 1.0), (2.4, 0.5))) * 0.22
    b = tone(2637, 0.5, 0.18, ((1, 1.0), (2.4, 0.5))) * 0.22
    out = np.zeros(int(0.6 * SR))
    out[:len(a)] += a
    s = int(0.06 * SR)
    out[s:s + len(b)] += b[:len(out) - s]
    return out


def sfx_stamp():
    n = int(0.25 * SR)
    t = np.arange(n) / SR
    thump = np.sin(2 * np.pi * (70 + 60 * np.exp(-t * 40)) * t) * np.exp(-t * 14) * 0.55
    crack = lowpass(noise(0.25), 2500) * np.exp(-t * 50) * 0.3
    return thump + crack


def sfx_riser(dur):
    n = int(dur * SR)
    t = np.arange(n) / SR
    f = 200 + 600 * (t / dur) ** 2
    ph = 2 * np.pi * np.cumsum(f) / SR
    return np.sin(ph) * (t / dur) ** 1.5 * 0.12


def sfx_ticks(dur, rate=12):
    out = np.zeros(int(dur * SR))
    k = tone(3000, 0.03, 0.006, ((1, 1.0),)) * 0.18
    for i in range(int(dur * rate)):
        s = int(i / rate * SR)
        out[s:s + len(k)] += k[:len(out) - s]
    return out


def sfx_drumroll(dur):
    out = np.zeros(int(dur * SR))
    hit = lowpass(noise(0.05), 2500) * env(int(0.05 * SR), 0.001, 0.015)
    t = 0.0
    while t < dur:
        s = int(t * SR)
        g = 0.15 + 0.35 * t / dur
        out[s:s + len(hit)] += hit[:len(out) - s] * g
        t += 0.045
    return out


def sfx_pen(dur):
    x = noise(dur)
    x = x - lowpass(x, 2500)
    n = len(x)
    mod = 0.5 + 0.5 * np.abs(np.sin(np.linspace(0, 18, n)))
    return x * mod * 0.12


def sfx_click():
    n = int(0.05 * SR)
    t = np.arange(n) / SR
    return np.sin(2 * np.pi * 1800 * t) * np.exp(-t * 120) * 0.4


COIN_PARTS = {("S01", "coins")}


def main():
    with open(os.path.join(ROOT, "manifest.json")) as f:
        m = json.load(f)
    track = bgm() * 0.55
    fx = np.zeros_like(track)

    def put(t, clip, gain=1.0):
        s = int(t * SR)
        if s >= len(fx):
            return
        e = min(len(fx), s + len(clip))
        fx[s:e] += clip[:e - s] * gain

    for sc in m["scenes"]:
        for p in sc["parts"]:
            a = p["anim"]
            if a["type"] == "none":
                continue
            t = sc["start"] + a.get("at", 0)
            key = (sc["id"], p["name"])
            if key in COIN_PARTS:
                put(t, sfx_coin())
            elif a["type"] == "pop":
                put(t, sfx_pop())
            elif a["type"] in ("slideL", "slideR", "slideU", "drop"):
                put(t, sfx_whoosh(0.35), 0.6)
            elif a["type"] == "stamp":
                put(t, sfx_stamp())
            elif a["type"] in ("wipeL", "wipeU") and a.get("dur", 0.6) > 1.5:
                put(t, sfx_riser(a["dur"]))
            elif a["type"] == "growY":
                put(t, sfx_ticks(a.get("dur", 0.6)), 0.8)
    # hand-placed cues
    put(0.05, sfx_whoosh(0.5), 0.5)                                  # opening
    put(40.5, sfx_drumroll(0.9))                                     # quiz countdown
    put(41.4, sfx_ding(2093))                                        # answer
    for k in range(3):
        put(51.4 + k * 0.4, sfx_click(), 1.0)                        # subscribe taps
    # duck the music (not the SFX) under the narration, when gen_narration.py has run
    nar = os.path.join(ROOT, "narration.wav")
    if os.path.exists(nar):
        with wave.open(nar) as w:
            v = np.frombuffer(w.readframes(w.getnframes()), "<i2").astype(np.float32) / 32768
        v = np.abs(np.pad(v, (0, max(0, len(track) - len(v))))[:len(track)])
        hop = int(0.02 * SR)
        frames = v[:len(v) // hop * hop].reshape(-1, hop).max(axis=1)
        active = (frames > 0.03).astype(np.float32)
        # 150 ms attack/release smoothing, then upsample back to samples
        k = np.ones(15) / 15
        active = np.clip(np.convolve(active, k, mode="same") * 2, 0, 1)
        gain = 1 - 0.55 * np.repeat(active, hop)
        gain = np.pad(gain, (0, len(track) - len(gain)), constant_values=1)
        track = track * gain
    mix = track + fx
    peak = np.max(np.abs(mix))
    mix = np.tanh(mix / peak * 1.2) * 0.42
    st = np.stack([mix, mix * 0.98], axis=1)
    pcm = (st * 32767).astype("<i2")
    out = os.path.join(ROOT, "audio.wav")
    with wave.open(out, "wb") as w:
        w.setnchannels(2)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes(pcm.tobytes())
    print("wrote", out, f"{len(mix) / SR:.1f}s")


if __name__ == "__main__":
    main()
