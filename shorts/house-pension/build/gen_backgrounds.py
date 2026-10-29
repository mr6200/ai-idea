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
    "S01": "an older korean couple sitting in their cozy house looking at an empty wallet, a calendar on the wall",
    "S02": "a cute small korean house with a garden and a mailbox, coins flowing from the roof like a little fountain",
    "S03": "an older korean man at a bank counter talking with a friendly clerk, documents on the desk",
    "S04": "an older korean woman opening a letter with a happy surprised face at the dining table",
    "S05": "a row of small clay houses of different sizes on a shelf, small to large, warm light",
    "S06": "an older korean couple holding hands on a sofa in their living room, family photos on the wall",
    "S07": "a sturdy clay house on a hill in a storm, the house standing safe and warm with lights on",
    "S08": "an older korean couple and their adult children having dinner together in a cozy home",
    "S09": "a stack of coins slowly growing next to a small house model on a desk, an hourglass beside it",
    "S10": "an older korean man thinking at a crossroads sign in a garden, one path to a house",
    "S11": "a colorful quiz show stage with spotlights and two podiums, confetti",
    "S12": "an older korean couple drinking tea on the porch of their small house at sunset, flowers",
}
