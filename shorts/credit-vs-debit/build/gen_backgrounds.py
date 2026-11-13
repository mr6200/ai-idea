"""Prompts for the AI scene illustrations (semi-realistic action webtoon, episode 26 on), drawn by gen_backgrounds_seedream.py into ai_bg/ (credit card vs debit card; same character as episodes 23-25). One character described the same way in every prompt.

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

CARDS = "two blank plastic payment cards, one blue and one red, with no text, no numbers and no logos"
SCENES = {
    "S01": f"{CHAR} standing in the lower half of the frame holding up {CARDS}, one in each hand, comparing them with a puzzled face, city street at dusk behind him",
    "S02": f"{CHAR} standing upright in the lower part of the frame, looking down at a glowing smartphone in his hands, blue screen light on his face, abstract glowing upward arrow shapes floating above him, night office, upright portrait orientation",
    "S03": f"{CHAR} sitting at his desk in the lower part of the frame with a confident smile, giving a thumbs up, a glowing golden shield of light rising behind him, evening office, plain blank screens",
    "S04": f"{CHAR} standing upright in the lower part of the frame at a cafe counter, smiling, holding up a plain red card, golden sparkles and gold coins flying around him, warm light, upright portrait orientation",
    "S05": f"{CHAR} in the lower part of the frame raising his fist like a hero, dramatic backlight, wind blowing his tie, rooftop at sunset, blue light glowing around his hand",
    "S06": f"{CHAR} in the lower part of the frame frozen in alarm as a dark shadowy chain wraps around a blank red payment card in his hand, ominous red light",
    "S07": f"{CHAR} thinking hard on a quiz show stage, hand on chin, question marks floating, spotlights",
    "S08": f"{CHAR} in the lower right of the frame smiling and walking home on a quiet night street, hands in pockets, warm street lights, no signboards, no writing anywhere",
}







