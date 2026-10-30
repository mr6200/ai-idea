"""Prompts for the AI scene paintings (3D clay), drawn by gen_backgrounds_seedream.py into ai_bg/ (episode 19, hidden money).

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
    "S01": "a cute pink piggy bank sleeping with a sleep mask on a cozy bed of coins under a sofa, a curious clay person peeking at it with a flashlight",
    "S02": "a giant mountain of golden coins and banknotes in a quiet vault with a small clay person looking up in awe",
    "S03": "four treasure chests of different colors half open on a table, coins and cards inside, warm light",
    "S04": "a clay person on a sofa looking at a smartphone surrounded by floating bank passbooks and bank cards",
    "S05": "a clay person opening a forgotten gift box full of coins under a big pastel umbrella, cozy room",
    "S06": "colorful credit cards turning into a stream of coins flowing into a piggy bank on a desk",
    "S07": "a quiz show stage with two podiums, a big hourglass and a calendar, spotlights, confetti",
    "S08": "a happy clay person holding a smartphone with coins popping out, cozy living room, warm light",
}

