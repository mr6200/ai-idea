"""Prompts for the AI scene paintings (3D clay), drawn by gen_backgrounds_seedream.py into ai_bg/ (episode 21, pension savings account).

compose_bg.py keeps the colours and makes each image the slowly drifting bottom layer of the scene.
The infographic cards sit in the middle of the frame, so the prompts ask for the subject low or to the side.
"""
import os

ROOT = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(ROOT, "ai_bg")
STYLE = ("3d claymation render, cute plasticine clay figures, soft studio lighting, pastel teal and warm colors, "
         "miniature diorama, tilt-shift, vertical 9:16 composition, no text, no letters, no numbers")
NEGATIVE = "text, letters, words, numbers, watermark, logo, signature, blurry, deformed, extra fingers, ugly, scary"

SCENES = {
    "S01": "a happy clay office worker receiving a shower of coins from a big envelope at a desk, year-end tax season, cozy office",
    "S02": "a clay person putting coins into a cute retirement savings jar labeled with no text, a calendar and calculator on the table",
    "S03": "a clay person using a big calculator with coins stacked beside it, receipts on a wooden table, warm light",
    "S04": "a clay office worker and a small shop owner smiling side by side, each holding a piggy bank, sunny street",
    "S05": "a clay person hesitating while about to smash a piggy bank with a hammer, warning cones around, dramatic light",
    "S06": "a quiz show stage with three podiums and a giant hourglass, spotlights, confetti",
    "S07": "an elderly clay couple relaxing on a porch with tea and a piggy bank, sunset garden, peaceful",
}



