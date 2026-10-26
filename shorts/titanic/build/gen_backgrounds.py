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
    "S01": "the RMS Titanic at night on a calm dark ocean, a huge iceberg looming ahead, stars in the sky",
    "S02": "a great four-funnel ocean liner departing Southampton harbour in 1912, crowds waving on the dock, smoke",
    "S03": "giant ship hull under construction inside a steel gantry at a Belfast shipyard, workers and cranes",
    "S04": "night sea, a tall iceberg right beside the hull of a great ocean liner, cold mist, moonlight",
    "S05": "flooded lower corridor of an old ocean liner, sea water rushing through a doorway, hanging lamps",
    "S06": "wooden lifeboats being lowered from the deck of a great ocean liner at night, davits and ropes",
    "S07": "a great ocean liner sinking bow first at night, stern rising from the sea, lifeboats in the foreground",
    "S08": "a small patrol ship sailing among icebergs in the north atlantic, 1914, calm sea",
    "S09": "a rusty shipwreck bow resting on the deep ocean floor, searchlight beam from a small submersible, darkness",
    "S10": "a great four-funnel ocean liner sailing toward the sunset on a calm sea, majestic, seagulls",
}
