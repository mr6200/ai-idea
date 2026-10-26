"""Prompts for the AI scene backgrounds (vintage engraving), drawn by gen_backgrounds_runpod.py into ai_bg/.

compose_bg.py tones each image sepia and lays it under the translucent paper layer of the scene.
"""
import os

ROOT = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(ROOT, "ai_bg")
STYLE = ("19th century engraving illustration, vintage poster, cross-hatching ink lines, sepia and cream paper, "
         "aged paper texture, calm empty space in the middle, no text")
NEGATIVE = "text, letters, words, numbers, watermark, logo, signature, people falling, blood, gore, blurry, deformed, color photo"

SCENES = {
    "S01": "an old elevator car hanging in a tall vertical elevator shaft, dramatic perspective looking up",
    "S02": "the 1854 New York Crystal Palace exhibition hall with iron and glass dome, crowd of people in top hats",
    "S03": "a wooden elevator platform on guide rails in a grand exhibition hall, crowd watching",
    "S04": "machine workshop with gears, springs and iron rails on a workbench",
    "S05": "new york city skyline with tall buildings and skyscrapers, early 1900s",
    "S06": "elevator machine room with a large pulley wheel and many steel cables",
    "S07": "victorian machinery with a large spinning wheel and flyweights, engine room",
    "S08": "close view of iron guide rails inside an elevator shaft, rivets and brackets",
    "S09": "bottom of an elevator shaft with large springs and pistons, dim light",
    "S10": "empire state building towering over 1940s new york city, fog",
    "S11": "inside an old ornate elevator cabin with brass details and a folding gate",
    "S12": "grand art deco elevator lobby with ornate brass elevator doors",
}
