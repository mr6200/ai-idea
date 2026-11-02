"""Prompts for the AI scene illustrations (Korean webtoon), drawn by gen_backgrounds_seedream.py into ai_bg/ (episode 24, first salary; same character as episode 23). One character described the same way in every prompt.

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
    "S01": f"{CHAR} jumping with joy looking at a smartphone salary notification, confetti and sparkles, bright office",
    "S02": f"{CHAR} putting money into a sturdy emergency savings box with a small umbrella on top, rainy window behind, cozy room",
    "S03": f"{CHAR} smiling at a smartphone while coins automatically flow from the phone into a big piggy bank, morning light",
    "S04": f"{CHAR} holding two plastic cards, one blue and one red, comparing them with a thoughtful face, balance scale on the desk",
    "S05": f"{CHAR} thinking hard with a hand on the chin on a quiz show stage, question marks floating, spotlights",
    "S06": f"{CHAR} smiling confidently next to a growing stack of coins and a piggy bank, sunrise city view through the window",
}






