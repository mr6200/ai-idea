"""Emit build.jsx: the EffectCraft project for the whole Short.

One precomp per scene (its PNG parts animated with expressions), a main comp
that sequences them and adds subtitles, progress bar, counters and audio.
Run with:  effectcraft-cli script build.jsx --empty --save-as ../video/elevator-safety.ecproj
"""
import json
import os

from PIL import Image

ROOT = os.path.dirname(os.path.abspath(__file__))
PARTS = os.path.join(ROOT, "parts")


def ease_expr(kind):
    return {
        "linear": "p",
        "accel": "p*p",
        "decel": "1-(1-p)*(1-p)",
    }.get(kind, "(p<0.5?2*p*p:1-Math.pow(-2*p+2,2)/2)")


def content_span(path, kind):
    """Fraction of the frame, along the wipe direction, where the layer's pixels sit."""
    x0, y0, x1, y1 = Image.open(path).getbbox()
    if kind == "wipeL":
        return x0 / 1080, x1 / 1080
    if kind == "wipeU":
        return (1920 - y1) / 1920, (1920 - y0) / 1920
    return y0 / 1920, y1 / 1920


def anim_exprs(a, idle, path=None):
    """Return {prop: expression} plus static anchor/position and wipe settings."""
    t = a["type"]
    at = a.get("at", 0.0)
    dur = a.get("dur", 0.6)
    anc = a.get("anchor", [540, 960])
    ex, static, wipe = {}, {}, None
    show = f"time<{at}?0:100"
    bob = f"+Math.sin((time-{at})*2.4)*7" if idle else ""
    if t == "none":
        return ex, static, wipe
    if t in ("pop", "growY", "stamp", "spin", "tap"):
        static["anchor"] = anc
        static["position"] = anc
        ex["position"] = f"[{anc[0]}, {anc[1]}{bob}]" if idle else None
    if t == "pop":
        ex["scale"] = f"var t=time-{at}; var s=t<0?0:100*(1-Math.exp(-7*t)*Math.cos(11*t)); [s,s]"
        ex["opacity"] = show
    elif t == "fade":
        ex["opacity"] = f"var p=(time-{at})/0.45; p<0?0:(p>1?100:100*p)"
    elif t in ("slideL", "slideR", "slideU", "drop"):
        dx, dy = {"slideL": (-800, 0), "slideR": (800, 0), "slideU": (0, 500), "drop": (0, -650)}[t]
        ex["position"] = (f"var t=Math.max(0,time-{at}); var e=1-Math.exp(-7*t)*Math.cos(9*t); "
                          f"[540+{dx}*(1-e), 960+{dy}*(1-e){bob}]")
        ex["opacity"] = show
    elif t == "growY":
        ex["scale"] = f"var p=Math.min(1,Math.max(0,(time-{at})/{dur})); p={ease_expr(a.get('ease'))}; [100, 100*p]"
        ex["opacity"] = show
    elif t in ("wipeL", "wipeU", "wipeD"):
        angle = {"wipeL": 270, "wipeU": 180, "wipeD": 0}[t]
        lo, hi = content_span(path, t)
        wipe = (angle, f"var p=Math.min(1,Math.max(0,(time-{at})/{dur})); p={ease_expr(a.get('ease'))}; "
                       f"100*(1-({lo:.4f}+p*{hi - lo:.4f}))")
        ex["opacity"] = show
    elif t == "stamp":
        ex["scale"] = (f"var t=time-{at}; var s=t<0?0:(t<0.12?300-1666*t:100+12*Math.exp(-10*(t-0.12))*Math.sin(30*(t-0.12))); [s,s]")
        ex["opacity"] = f"time<{at}?0:Math.min(100,(time-{at})/0.06*100)"
    elif t == "spin":
        ex["rotation"] = f"Math.max(0,time-{at})*{a.get('speed', 90)}"
        ex["opacity"] = show
    elif t == "tap":
        ex["scale"] = f"var t=time-{at}; var k=t<0?0:Math.abs(Math.sin(t*5)); var s=t<0?0:100-10*k; [s,s]"
    ex = {k: v for k, v in ex.items() if v}
    return ex, static, wipe


def main():
    with open(os.path.join(ROOT, "manifest.json")) as f:
        m = json.load(f)
    js = [
        "var P = app.project;",
        "function imp(p){ return P.importFile(new ImportOptions(new File(p))); }",
        "function tg(L){ return L.property('ADBE Transform Group'); }",
        "function setText(L, size, color, font){ var tp=L.property('ADBE Text Properties').property('ADBE Text Document');"
        " var d=tp.value; d.font=font||'WenQuanYi Zen Hei'; d.fontSize=size; d.fillColor=color;"
        " try{ d.justification=ParagraphJustification.CENTER_JUSTIFY; }catch(e){} tp.setValue(d); return tp; }",
        f"var main = P.items.addComp('Main', {m['width']}, {m['height']}, 1, {m['duration']}, {m['fps']});",
        "main.bgColor = [0.937, 0.886, 0.769];",
    ]
    for sc in m["scenes"]:
        sid, dur = sc["id"], sc["end"] - sc["start"]
        cv = f"c_{sid}"
        js.append(f"var {cv} = P.items.addComp('{sid}', 1080, 1920, 1, {dur + 0.2}, 30);")
        # add bottom-first so the first part listed ends up at the bottom
        for p in sc["parts"]:
            path = os.path.join(PARTS, sid, p["name"] + ".png")
            assert os.path.exists(path), path
            ex, static, wipe = anim_exprs(p["anim"], p.get("idle"), path)
            js.append(f"(function(){{ var L={cv}.layers.add(imp('{path}')); L.name='{p['name']}'; L.moveToBeginning(); var T=tg(L);")
            if "anchor" in static:
                js.append(f" T.property('ADBE Anchor Point').setValue({static['anchor']});"
                          f" T.property('ADBE Position').setValue({static['position']});")
            for prop, match in (("scale", "ADBE Scale"), ("opacity", "ADBE Opacity"),
                                ("position", "ADBE Position"), ("rotation", "ADBE Rotate Z")):
                if prop in ex:
                    js.append(f" T.property('{match}').expression={json.dumps(ex[prop])};")
            if wipe:
                js.append(" var W=L.property('ADBE Effect Parade').addProperty('ADBE Linear Wipe');"
                          f" W.property('ADBE Linear Wipe-0002').setValue({wipe[0]});"
                          f" W.property('ADBE Linear Wipe-0003').setValue(6);"
                          f" W.property('ADBE Linear Wipe-0001').expression={json.dumps(wipe[1])};")
            js.append("})();")
        # place the scene in main; push-in over the scene, a short settle at the cut
        if sc.get("zoomOut"):
            scale = "var t=time-inPoint; var s=t<1.2?100+90*Math.pow(1-t/1.2,3):100; [s,s]"
        else:
            scale = f"var t=time-inPoint; var s=100+2.5*t/{dur}+(t<0.25?3*(1-t/0.25):0); [s,s]"
        js.append(f"(function(){{ var L=main.layers.add({cv}); L.startTime={sc['start']}; L.outPoint={sc['end']};"
                  f" L.moveToEnd(); tg(L).property('ADBE Scale').expression={json.dumps(scale)}; }})();")
    # subtitles on top of the scenes
    for i, c in enumerate(m["cues"]):
        path = os.path.join(PARTS, "subs", f"sub{i:02d}.png")
        js.append(f"(function(){{ var L=main.layers.add(imp('{path}')); L.startTime={c['start']}; L.inPoint={c['start']};"
                  f" L.outPoint={c['end']}; var T=tg(L); T.property('ADBE Anchor Point').setValue([540,1480]);"
                  " T.property('ADBE Position').setValue([540,1480]);"
                  " T.property('ADBE Scale').expression='var t=time-inPoint; var s=t<0.15?92+8*t/0.15:100; [s,s]';"
                  " T.property('ADBE Opacity').expression='var t=time-inPoint, r=outPoint-time; Math.min(100, t/0.12*100, r/0.1*100)'; })();")
    js += [
        # progress bar along the top edge
        "(function(){ var L=main.layers.addSolid([0.659,0.157,0.118], 'progress', 1080, 12, 1); var T=tg(L);"
        " T.property('ADBE Anchor Point').setValue([0,0]); T.property('ADBE Position').setValue([0,0]);"
        " T.property('ADBE Scale').expression='[100*time/thisComp.duration, 100]'; })();",
        f"(function(){{ var L=main.layers.add(imp('{os.path.join(ROOT, 'audio.wav')}')); L.name='music+sfx'; L.moveToEnd(); }})();",
        f"(function(){{ var L=main.layers.add(imp('{os.path.join(ROOT, 'narration.wav')}')); L.name='narration'; L.moveToEnd(); }})();",
        "writeLn('layers in main: ' + main.numLayers + ', items: ' + P.numItems);",
    ]
    with open(os.path.join(ROOT, "build.jsx"), "w") as f:
        f.write("\n".join(js) + "\n")
    print("wrote build.jsx", len(js), "lines")


if __name__ == "__main__":
    main()
