"""Prompts for the AI scene illustrations (semi-realistic action webtoon, episode 26 on), drawn by gen_backgrounds_seedream.py into ai_bg/ (year-end tax settlement: what to do before 31 December; same character as episodes 23-27). One character described the same way in every prompt.

compose_bg.py keeps the colours and makes each image the slowly drifting bottom layer of the scene.
The infographic cards sit in the middle of the frame, so the prompts ask for the subject low or to the side.
"""
import os

ROOT = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(ROOT, "ai_bg")
CHAR = "the same young korean office worker man with short black hair, white shirt and navy tie"
STYLE = ("semi-realistic action fantasy webtoon style, dramatic cinematic lighting, rim light, saturated colors, detailed rendering, "
         "dynamic angle, vertical 9:16 composition, no text, no letters, no numbers, no speech bubbles")
NEGATIVE = "text, letters, words, numbers, speech bubble, watermark, logo, brand name, signature, blurry, deformed, extra fingers, photo, 3d render"

SCENES = {
    "S01": f"{CHAR} sitting upright at his office desk in December, his face in the middle of the frame, startled expression, snow falling outside the window behind him, warm desk lamp, upright portrait orientation",
    "S02": f"{CHAR} at home late at night in the lower part of the frame looking at a laptop, glowing golden coins and an abstract receipt hologram with no writing floating up from the screen, cozy room",
    "S03": f"{CHAR} with his face in the middle of the frame dropping glowing golden coins into a large shining piggy bank, dramatic golden light rays, dark blue background",
    "S04": f"{CHAR} in the lower part of the frame smiling and holding a plain wooden gift box full of red apples with a red ribbon and no labels, beautiful korean countryside village with rice fields and mountains behind him, golden autumn light",
    "S05": f"{CHAR} with his face in the middle of the frame raising his hand in a stop gesture with a serious face, red warning light glowing behind him, dark office",
    "S06": f"{CHAR} thinking hard on a quiz show stage, hand on chin, question marks floating, spotlights",
    "S07": f"{CHAR} in the lower right of the frame smiling on a city rooftop on new year's eve, colorful fireworks bursting in the night sky, no signboards, no writing anywhere",
}







