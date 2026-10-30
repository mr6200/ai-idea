"""Prompts for the AI scene paintings (3D clay), drawn by gen_backgrounds_seedream.py into ai_bg/ (episode 19, convenience-store 1+1 deals).

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
    "S01": "a cheerful korean young man in a bright convenience store holding two identical drink bottles with a big smile, colorful shelves",
    "S02": "a convenience store drink fridge full of colorful bottles and cans with promotion stickers with no text, cozy night street outside",
    "S03": "a large supermarket aisle with a shopping cart on one side and a tiny convenience store on the other side, comparing, miniature diorama",
    "S04": "a confused clay woman at a convenience store counter holding three snack bags while needing only one, thinking pose",
    "S05": "two chocolates on a small market stand table, a plain small chocolate and a fancy truffle, curious clay customers looking",
    "S06": "a plain brown glass oil bottle with a blank label on a supermarket shelf, a price tag being swapped by a sneaky clay store clerk, magnifying glass on the floor",
    "S07": "a quiz show stage with three podiums and a big convenience store snack display, spotlights, confetti",
    "S08": "a clay person carefully reading a receipt next to a small shopping basket with one item, cozy kitchen table, warm light",
}

