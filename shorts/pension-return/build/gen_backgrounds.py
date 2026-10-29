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
    "S01": "an older korean man holding a small jar of coins and looking curiously at a much bigger jar, cozy living room",
    "S02": "a young korean office worker looking at a payslip at a desk, a small staircase model on the desk",
    "S03": "a balance scale on a wooden table with coins on both sides, warm window light",
    "S04": "an older korean woman doing math with a big calculator and a notebook at a kitchen table",
    "S05": "two coin towers on a table, a short one and a tall one, an older couple smiling behind them",
    "S06": "a market stall with fruit and price tags, an older couple shopping happily",
    "S07": "a young office worker and a friendly boss shaking hands in a bright office, a piggy bank on the desk",
    "S08": "a large glass water tank slowly being filled from a tap, a calm older man watching, workshop",
    "S09": "a stately government building with columns, a big official stamp on a document in the foreground",
    "S10": "an older korean couple planting a small tree together in a garden, sunny day",
    "S11": "a colorful quiz show stage with spotlights and three podiums, confetti",
    "S12": "an older korean couple reading a newspaper together on a park bench, autumn leaves",
}
