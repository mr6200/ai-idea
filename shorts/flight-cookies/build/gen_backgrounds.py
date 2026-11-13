"""Prompts for the AI scene illustrations (semi-realistic action webtoon, episode 26 on), drawn by gen_backgrounds_seedream.py into ai_bg/ (flight prices and browser cookies; same character as episodes 23-26). One character described the same way in every prompt.

compose_bg.py keeps the colours and makes each image the slowly drifting bottom layer of the scene.
The infographic cards sit in the middle of the frame, so the prompts ask for the subject low or to the side.
"""
import os

ROOT = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(ROOT, "ai_bg")
CHAR = "the same young korean office worker man with short black hair, white shirt and navy tie"
STYLE = ("semi-realistic action fantasy webtoon style, dramatic cinematic lighting, rim light, saturated colors, detailed rendering, "
         "dynamic angle, vertical 9:16 composition, no text, no letters, no numbers, no speech bubbles")
NEGATIVE = "text, letters, words, numbers, speech bubble, watermark, logo, brand name, signature, blurry, deformed, extra fingers, photo, 3d render"

SCENES = {
    "S01": f"{CHAR} sitting at a laptop late at night, his face in the middle of the frame, shocked face lit by the screen, the screen shows only a simple airplane icon and an abstract rising red arrow, dark room, no text on screen",
    "S02": f"{CHAR} standing in the lower part of the frame staring at a giant chocolate chip cookie floating in the air and crumbling into glowing pixels, dramatic blue light, night city",
    "S03": f"{CHAR} standing in the aisle of an empty airplane cabin in the lower part of the frame, rows of seats glowing in three different colors green yellow and red from front to back, dramatic cabin lighting",
    "S04": f"{CHAR} in the lower part of the frame at an airport window looking at his phone, glowing abstract zigzag price line hologram floating above him with no numbers, airplane taking off outside at dusk, no signs",
    "S05": f"{CHAR} in the lower part of the frame being scanned by a huge glowing futuristic AI hologram eye made of light, blue and purple neon light, mysterious atmosphere",
    "S06": f"{CHAR} thinking hard on a quiz show stage, hand on chin, question marks floating, spotlights",
    "S07": f"{CHAR} in the lower right of the frame smiling and pulling a small suitcase through a bright airport terminal, airplane outside big windows at golden sunset, no signboards, no writing anywhere",
}







