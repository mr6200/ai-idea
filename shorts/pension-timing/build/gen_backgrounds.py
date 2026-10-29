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
    "S01": "an older korean man standing at a fork in a garden path, one sign pointing left and one pointing right, thinking",
    "S02": "an older korean man looking at a big wall calendar with a birthday cake on the table",
    "S03": "a small clay scale balancing two jars of coins, one shrinking and one growing, cozy desk",
    "S04": "three clay piggy banks of different sizes lined up on a wooden shelf, small to large",
    "S05": "an older couple stacking coins into tall piles on a kitchen table with a notebook",
    "S06": "a cute clay race on a winding track, one runner starting early far ahead, sunny park",
    "S07": "a patient older man waiting on a park bench beside a slowly growing tree full of fruit",
    "S08": "an older korean couple walking happily on a long path through blooming trees, far into the distance",
    "S09": "an older man at a doctor's office talking with a kind doctor, warm light",
    "S10": "an older woman reading a health insurance letter at a desk with glasses and a calculator",
    "S11": "a colorful quiz show stage with spotlights and two podiums, confetti",
    "S12": "an older korean couple drinking tea on a sunny balcony with plants, relaxed and smiling",
}
