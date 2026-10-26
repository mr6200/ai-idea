"""Prompts for the AI scene paintings (3D clay), drawn by gen_backgrounds_runpod.py into ai_bg/.

compose_bg.py keeps the colours and makes each image the slowly drifting bottom layer of the scene.
"""
import os

ROOT = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(ROOT, "ai_bg")
STYLE = ("3d claymation render, cute plasticine clay figures, soft studio lighting, pastel teal and warm colors, "
         "miniature diorama, tilt-shift, calm empty space in the middle, no text")
NEGATIVE = "text, letters, words, numbers, watermark, logo, signature, blurry, deformed, extra fingers, ugly, scary"

SCENES = {
    "S01": "a korean man in his early sixties on his last day at the office holding a small box, a wall calendar behind him",
    "S02": "an office farewell party for a retiring older employee, colleagues clapping, flowers and a cake",
    "S03": "an older korean man reading a letter at a kitchen table, a piggy bank and a calendar nearby",
    "S04": "an older couple standing at the edge of a small cliff with a gap to the other side, a long road ahead",
    "S05": "an older couple at a dining table with a pile of bills and a calculator, warm lamp light",
    "S06": "an older man picking a small fruit from a young tree too early, a basket at his feet",
    "S07": "an older woman putting coins into a big glass savings jar, cozy living room",
    "S08": "a cute small house with a garden, an older couple waving from the door, sunny day",
    "S09": "an older man working happily in a small cafe making coffee, apron, morning light",
    "S10": "an older couple walking across a sturdy wooden bridge with four pillars over a small river",
    "S11": "a colorful quiz show stage with spotlights and two podiums, confetti",
    "S12": "an older korean couple walking hand in hand on a park path at sunset, autumn trees",
}
