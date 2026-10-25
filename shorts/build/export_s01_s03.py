"""Split the hand-drawn S01-S03 VectorCraft documents into full-frame PNG layers."""
import json
import os
import subprocess

ROOT = os.path.dirname(os.path.abspath(__file__))
SCENES = os.path.join(ROOT, "..", "scenes")

# object ids per part, read from inspect_document of each scene
PARTS = {
    "S01": ("S01_hook_paper", {
        "bg": [2, 3, 4], "label": [19, 16], "paper": [5, 6], "callout": [8, 9, 20, 11],
        "sparkles": [12, 13, 14], "cap1": [17], "cap2": [18],
    }),
    "S02": ("S02_fold_montage", {
        "bg": [2], "label": [17, 18], "title1": [19], "title2": [20], "stack": [3, 4, 5], "arrow": [6],
        "timeline": [7, 8], "row1": [10, 11], "row2": [12, 13], "row3": [14, 15], "row4": [16, 9],
        "chak1": [21], "chak2": [22], "chak3": [23],
    }),
    "S03": ("S03_moon_reveal", {
        "bg": [2, 19, 4], "moon": [7, 8], "column": [5, 6], "earth": [9, 10, 11],
        "dist": [12, 13, 14, 15], "caption": [16, 17, 18],
    }),
}

for sid, (fname, parts) in PARTS.items():
    every = sorted({i for ids in parts.values() for i in ids})
    out_dir = os.path.join(ROOT, "parts", sid)
    os.makedirs(out_dir, exist_ok=True)
    for name, ids in parts.items():
        hide = [i for i in every if i not in ids]
        cmd = ["vectorcraft-cli", "run", "--in", os.path.join(SCENES, fname + ".vectorcraft"),
               "--cmd", "layer.setProps", "--params", json.dumps({"ids": hide, "visible": False}),
               "--export", os.path.join(out_dir, name + ".png")]
        r = subprocess.run(cmd, capture_output=True, text=True)
        if r.returncode != 0:
            raise SystemExit(f"{sid}/{name}: {r.stdout}{r.stderr}")
    print(sid, len(parts), "parts")
