"""Prompts for the AI scene illustrations (Korean webtoon), drawn by gen_backgrounds_seedream.py into ai_bg/ (episode 23, salary gone in three days). One character described the same way in every prompt.

compose_bg.py keeps the colours and makes each image the slowly drifting bottom layer of the scene.
The infographic cards sit in the middle of the frame, so the prompts ask for the subject low or to the side.
"""
import os

ROOT = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(ROOT, "ai_bg")
CHAR = "the same young korean office worker man with short black hair, white shirt and navy tie"
STYLE = ("korean webtoon style digital illustration, clean bold line art, flat cel shading, bright pastel colors, "
         "expressive anime face, vertical 9:16 composition, no text, no letters, no numbers, no speech bubbles")
NEGATIVE = "text, letters, words, numbers, speech bubble, watermark, logo, signature, blurry, deformed, extra fingers, realistic photo, 3d render"

SCENES = {
    "S01": f"{CHAR} looking at a smartphone banking app in shock as banknotes and coins fly away out of the phone, speed lines background",
    "S02": f"{CHAR} holding an empty wallet while flying envelopes with little wings queue up and fly out of it, office background",
    "S03": f"{CHAR} staring at a very long paper credit card bill unrolling to the floor, sweat drops, dramatic purple background",
    "S04": f"{CHAR} sitting sadly on a nearly empty piggy bank, a few coins around, soft evening light in a small studio apartment",
    "S05": f"{CHAR} confidently putting money into three colorful envelopes on a desk, sparkles, bright morning light",
    "S06": f"{CHAR} thinking hard next to a credit card and a blank calendar page with an empty grid and no numbers, question marks floating, quiz show lights",
    "S07": f"{CHAR} smiling happily and holding a full wallet at the end of the month, calendar on the wall, warm cozy room",
}





