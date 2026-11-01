"""Check every narration line for awkward TTS before rendering; writes tts_report.md.

Per cue (the clip exactly as gen_narration.py places it, pauses already trimmed):
  text   - a sentence ending in one syllable ("다리, 일.") gets drawn out by Chirp 3 HD;
           the spoken form shows how numbers are read
  audio  - pauses longer than PAUSE_WARN, syllables held longer than SYL_WARN (Whisper word times),
           speed-up needed to fit the subtitle window
  heard  - a local Whisper (small) transcript compared with the line; low similarity means a word
           was misread or swallowed
Needs faster-whisper (pip install faster-whisper; the model downloads from huggingface.co).
    python tts_check.py            -> prints a summary, writes tts_report.md, exits 1 on any warning
"""
import difflib
import json
import os
import re
import subprocess
import sys

import numpy as np

import gen_narration as g

ROOT = os.path.dirname(os.path.abspath(__file__))
PAUSE_WARN = 0.35   # s, a pause inside a line longer than this sounds like a stop
SYL_WARN = 0.42     # s per syllable, a word held longer than this sounds drawn out
SIM_WARN = 0.85     # transcript similarity below this means something was misheard
SPEED_WARN = 1.12   # atempo factor above this sounds rushed
ONE_SYLLABLE_END = re.compile(r"(?:^|[\s,])([가-힣])[.!?](?=\s|$)")


def plain(s):
    """Hangul, letters and digits only, for comparing what was said with what was heard."""
    return re.sub(r"[^0-9A-Za-z가-힣]", "", s)


def syllables(word):
    """Spoken syllables in a Whisper word: Hangul plus digits and % as they are read (6% = 육 퍼센트)."""
    return len(re.findall(r"[가-힣0-9]", word)) + 2 * word.count("%")


def pauses(x, hop=480, floor=0.01):
    rms = np.sqrt(np.mean(x[:len(x) // hop * hop].reshape(-1, hop) ** 2, axis=1))
    out, run, start = [], 0, 0
    for i, loud in enumerate(rms > floor):
        if loud:
            if run:
                out.append((start * hop / g.SR, run * hop / g.SR))
            run = 0
        else:
            if run == 0:
                start = i
            run += 1
    return out


def windows(cues, duration):
    """Same placement rule as gen_narration.main: the time each clip may take before speeding up."""
    out = []
    for i, c in enumerate(cues):
        nxt = cues[i + 1]["start"] + g.LAG if i + 1 < len(cues) else duration - 0.3
        out.append(nxt - c["start"] - g.GAP)
    return out


def main():
    from faster_whisper import WhisperModel
    model = WhisperModel("small", device="cpu", compute_type="int8")
    with open(os.path.join(ROOT, "manifest.json")) as f:
        m = json.load(f)
    cues = m["cues"]
    rows, warnings = [], 0
    for c, avail in zip(cues, windows(cues, m["duration"])):
        text = c["text"].replace("\n", " ")
        spoken = g.spoken(c["text"]).replace("\n", " ")
        x = g.read_wav(g.synthesize(g.spoken(c["text"])))
        dur = len(x) / g.SR
        notes = []
        for mt in ONE_SYLLABLE_END.finditer(text):
            notes.append(f"한 글자 문장 끝 「{mt.group(1)}」")
        long_pauses = [(at, length) for at, length in pauses(x) if length > PAUSE_WARN and 0.05 < at < dur - 0.3]
        for at, length in long_pauses:
            # a period inside a line is fine as a beat unless it really leaves a long gap
            why = " (줄 안의 마침표)" if re.search(r"\.\s+\S", text) else ""
            notes.append(f"긴 쉼 {length:.2f}초 ({at:.1f}초 지점){why}")
        pcm = subprocess.run(["ffmpeg", "-v", "error", "-f", "s16le", "-ar", str(g.SR), "-ac", "1", "-i", "-",
                              "-ar", "16000", "-f", "s16le", "-"],
                             input=(np.clip(x, -1, 1) * 32767).astype("<i2").tobytes(), capture_output=True).stdout
        segs, _ = model.transcribe(np.frombuffer(pcm, "<i2").astype(np.float32) / 32768, language="ko",
                                   beam_size=5, word_timestamps=True)
        segs = list(segs)
        heard = "".join(s.text for s in segs).strip()
        for s in segs:
            for w in s.words:
                syl = syllables(w.word)
                if syl and (w.end - w.start) / syl > SYL_WARN and w is not s.words[-1]:
                    notes.append(f"끄는 말 「{w.word.strip()}」 {(w.end - w.start) / syl:.2f}초/음절")
        # Whisper writes numbers as digits, so compare with the subtitle and with the spoken form
        sim = max(difflib.SequenceMatcher(None, plain(t), plain(heard)).ratio() for t in (text, spoken))
        if sim < SIM_WARN:
            notes.append(f"받아쓰기 불일치 {sim:.2f}")
        speed = dur / avail
        if speed > SPEED_WARN:
            notes.append(f"빨리 감기 {speed:.2f}배")
        warnings += bool(notes)
        rows.append((c["start"], text, spoken, heard, dur, avail, sim, notes))

    lines = ["# TTS 검사 결과", "",
             f"기준: 줄 안 쉼 > {PAUSE_WARN}초, 음절당 > {SYL_WARN}초, 받아쓰기 유사도 < {SIM_WARN}, 빨리 감기 > {SPEED_WARN}배, "
             "한 글자 문장 끝", "",
             f"경고 {warnings}줄 / 전체 {len(rows)}줄", "",
             "| 시각 | 자막 | 읽는 말 (숫자 읽기) | 받아쓰기 (Whisper) | 길이/여유 | 유사도 | 경고 |", "|---|---|---|---|---|---|---|"]
    for start, text, spoken, heard, dur, avail, sim, notes in rows:
        say = spoken if spoken != text else "—"
        lines.append(f"| {start:.1f} | {text} | {say} | {heard} | {dur:.2f}/{avail:.2f} | {sim:.2f} | {'; '.join(notes) or '없음'} |")
    with open(os.path.join(ROOT, "tts_report.md"), "w") as f:
        f.write("\n".join(lines) + "\n")
    for start, text, *_, notes in rows:
        if notes:
            print(f"{start:5.1f}  {text}  ->  {'; '.join(notes)}")
    print(f"{warnings} of {len(rows)} lines with warnings; see tts_report.md")
    sys.exit(1 if warnings else 0)


if __name__ == "__main__":
    main()
