"""Prompts for the AI scene paintings (cinematic vintage engraving), drawn by gen_backgrounds_runpod.py into ai_bg/.

compose_bg.py tones each image sepia and makes it the slowly drifting bottom layer of the scene.
"""
import os

ROOT = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(ROOT, "ai_bg")
STYLE = ("19th century engraving illustration, cinematic composition, dramatic lighting, cross-hatching ink lines, "
         "sepia tones, aged paper texture, highly detailed, no text")
NEGATIVE = ("text, letters, words, numbers, watermark, logo, signature, bodies, drowning people, blood, gore, "
            "blurry, deformed, modern ship, color photo")

SCENES = {
    "S01": "a busy victorian london street crossing at dusk with horse carriages and gas street lamps",
    "S02": "the houses of parliament and big ben in 1868 london, horse-drawn carriages on a cobbled road",
    "S03": "a victorian police constable in a tall helmet beside a tall signal pillar on a london street, smoke",
    "S04": "a steam locomotive at a 19th century railway station platform with a signalman holding a lantern",
    "S05": "a railway line at night under a starry sky, distant signal lamps and town lights",
    "S06": "a foggy victorian street at night with blurred lamps glowing through the mist",
    "S07": "a busy american city intersection in 1914 with early automobiles and streetcars, cleveland",
    "S08": "a 1920s detroit downtown street with ford model t cars and a policeman directing traffic from a tower",
    "S09": "a modern city crosswalk with pedestrians waiting at the curb, calm evening",
    "S10": "a quiet town square with an old clock tower and a single traffic light post",
    "S11": "an ornate vintage theater stage with spotlights and velvet curtains",
    "S12": "a city street at sunset with cars stopped at a crossing, warm light",
}
