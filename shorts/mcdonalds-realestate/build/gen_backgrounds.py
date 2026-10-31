"""Prompts for the AI scene paintings (3D clay), drawn by gen_backgrounds_seedream.py into ai_bg/ (episode 20, McDonald's real estate). No logos: the brand is named only in the overlay text.

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
    "S01": "a puzzled clay man holding a giant hamburger in front of a small burger shop with a plain teal and white striped awning, blank storefront with no letters and no symbols, small town street",
    "S02": "a miniature town with many identical small generic fast food restaurants with no logos, a big office building in the center",
    "S03": "a clay landlord with a big key ring collecting rent envelopes from a smiling burger shop owner at a counter, no logos",
    "S04": "a 1950s style clay businessman in a suit looking at a map with land plots and pins on a desk, vintage office, warm light",
    "S05": "a burger shop counter with a cash register full of coins and a chart going up on the wall, clay figures, no logos",
    "S06": "a cozy small movie theater with red seats and a glowing screen, a clay audience watching with popcorn",
    "S07": "a quiz show stage with three podiums and a giant hamburger model, spotlights, confetti",
    "S08": "a clay man standing proudly on a green land plot holding a deed, a small generic burger shop behind him with no logos, sunset",
}


