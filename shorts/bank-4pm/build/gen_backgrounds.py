"""Prompts for the AI scene illustrations (Korean webtoon), drawn by gen_backgrounds_seedream.py into ai_bg/ (episode 25, why banks close at 4; same character as episodes 23-24). One character described the same way in every prompt.

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

TELLER = "a friendly korean bank teller woman in a navy uniform vest"
SCENES = {
    "S01": f"{CHAR} running up in shock to a bank branch entrance as a metal shutter comes down in the late afternoon, plain wall above the shutter with no signboard at all, no writing anywhere",
    "S02": f"{TELLER} counting stacks of banknotes carefully at a closed teller counter after hours, money counting machine, warm office lights",
    "S03": f"{TELLER} and a colleague working late at night in a bank office with piles of documents and checks, city lights through the window",
    "S04": f"{CHAR} wearing a face mask waiting in a bank lobby with a big wall clock with no numbers, other customers in masks, calm daylight",
    "S05": f"{CHAR} waiting in front of closed glass bank doors in the morning holding a coffee, looking at his wristwatch, blank doors with no signs",
    "S06": f"{CHAR} thinking hard on a quiz show stage, question marks floating, spotlights",
    "S07": f"night city street with a small office building whose windows are still brightly lit, no signboards, no writing anywhere, {CHAR} walking past and looking up at it with a smile",
}







