import json, os, subprocess
from concurrent.futures import ThreadPoolExecutor
URL="https://api.runpod.ai/v2/seedream-v4-t2i/runsync"
SUBJ="a young korean office worker looking at a smartphone banking app in shock as banknotes and coins fly away out of the phone"
P={
 "webtoon": SUBJ+", korean webtoon style digital illustration, clean bold line art, flat cel shading, bright pastel colors, expressive anime face with sweat drop, speed lines background, vertical 9:16, no text, no letters",
 "pixel": SUBJ+", retro 16-bit pixel art, video game scene, limited color palette, crisp pixels, dithering, night city room, vertical 9:16, no text, no letters, no numbers",
 "collage": SUBJ+", mixed media paper collage art, torn magazine paper cutouts, halftone photo pieces, kraft paper texture, tape and staples, risograph colors, vertical 9:16, no readable text",
}
NEG="text, letters, words, numbers, watermark, logo, signature, deformed, extra fingers"
def draw(k):
    body={"input":{"prompt":P[k],"negative_prompt":NEG,"size":"1080*1920","seed":2401,"enable_safety_checker":True}}
    r=subprocess.run(["curl","-sS","-m","300","-X","POST",URL,"-H",f"Authorization: Bearer {os.environ['RUNPOD_API_KEY']}","-H","Content-Type: application/json","-d",json.dumps(body)],capture_output=True,text=True)
    res=json.loads(r.stdout)
    subprocess.run(["curl","-sS","-o",f"{k}.jpg",res["output"]["result"]],check=True)
    return k, res["output"].get("cost")
with ThreadPoolExecutor(3) as ex:
    for x in ex.map(draw,P): print(x)
