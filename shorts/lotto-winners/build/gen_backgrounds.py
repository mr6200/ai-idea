"""Prompts for the AI scene paintings (3D clay), drawn by gen_backgrounds_seedream.py into ai_bg/.

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
    "S01": "a surprised korean man jumping with joy holding a giant golden lottery ticket, confetti and coins flying, tiny city street",
    "S02": "a colorful lottery ball drawing machine with spinning balls on a small tv studio stage, spotlights",
    "S03": "a worried clay man reading a newspaper on a park bench, rumor speech bubbles floating above with no text, gloomy clouds",
    "S04": "a happy family in front of a red wooden swedish cottage by a lake, birch trees, sunny summer day",
    "S05": "a clay man standing by palm trees in florida holding an empty open wallet, a few coins falling out, sunset beach",
    "S06": "a smiling korean couple holding a house key in front of a new small apartment building, moving boxes",
    "S07": "a giant desk calendar and a lottery ticket on a table with a clock, quiz show spotlights, confetti",
    "S08": "a cute pink piggy bank sitting on a stack of coins next to a small notebook and a plant, cozy desk, warm light",
}
