"""Prompts for the AI scene paintings (3D clay), drawn by gen_backgrounds_seedream.py into ai_bg/ (episode 22, pension savings vs IRP).

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
    "S01": "two cute savings jars side by side on a table, one teal and one coral, a curious clay person comparing them with a magnifying glass, no text",
    "S02": "a clay person stacking coins into two piles that join into one big pile, a plain blank envelope nearby, cozy desk, no papers with writing",
    "S03": "a friendly clay bank clerk welcoming different customers at a counter, a student and an office worker, bright lobby with plain walls, no signs, no logos, no letters",
    "S04": "a clay person trying to take a few coins out of a savings jar while another jar is locked with a big padlock, cozy room",
    "S05": "a clay investor with a balance scale holding a stock chart on one side and a safe box on the other, desk with a laptop",
    "S06": "a retiring clay office worker holding a gift box with coins at a farewell party, colleagues clapping, warm office",
    "S07": "a quiz show stage with three podiums and a giant coin, spotlights, confetti",
    "S08": "a clay person happily dropping coins into two savings jars on a shelf, plants and warm light, cozy home",
}




