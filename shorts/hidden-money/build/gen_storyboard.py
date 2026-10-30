"""Storyboard sheet (HTML + PNG) built from the scene art, motion hints and subtitle cues."""
import html
import json
import os
import subprocess

ROOT = os.path.dirname(os.path.abspath(__file__))
EP = os.path.dirname(ROOT)

MOTION = {"pop": "팝", "fade": "페이드", "slideL": "왼쪽에서", "slideR": "오른쪽에서", "slideU": "아래에서",
          "drop": "떨어짐", "growY": "자라남", "wipeL": "와이프 →", "wipeU": "와이프 ↑", "wipeD": "와이프 ↓",
          "stamp": "도장", "spin": "회전", "tap": "탭", "kenburns": "카메라 이동"}


def mmss(t):
    return f"{int(t) // 60}:{int(t) % 60:02d}"


def main():
    with open(os.path.join(ROOT, "manifest.json")) as f:
        m = json.load(f)
    cards = []
    for sc in m["scenes"]:
        lines = [c["text"].replace("\n", " ") for c in m["cues"] if sc["start"] <= c["start"] < sc["end"]]
        moves = [f"{p['name']} {MOTION[p['anim']['type']]} {p['anim'].get('at', 0):.1f}s"
                 for p in sc["parts"] if p["anim"]["type"] != "none"]
        cards.append(
            f'<div class="card"><img src="scenes/{sc["id"]}.png" alt="{sc["id"]}">'
            f'<div><div class="no">{sc["id"]}<span>{mmss(sc["start"])}–{mmss(sc["end"])} · {sc["end"] - sc["start"]}초</span></div>'
            f'<div class="row"><b>모션</b>{html.escape(", ".join(moves))}</div>'
            f'<div class="row nar"><b>내레이션</b>{html.escape(" / ".join(lines))}</div></div></div>')
    page = f"""<!doctype html>
<html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>숨은 돈 콘티</title>
<style>
  :root {{ --bg:#f5f3ee; --card:#fff; --ink:#1d1d1f; --muted:#2f5d6a; --line:#d8d3c8; }}
  body {{ margin:0; background:var(--bg); color:var(--ink); font-family:"Do Hyeon","WenQuanYi Zen Hei","Noto Sans KR",sans-serif; }}
  header {{ padding:28px 32px 8px; }} h1 {{ margin:0 0 6px; font-size:28px; }}
  .meta {{ color:var(--muted); font-size:14px; line-height:1.6; }}
  .grid {{ display:grid; grid-template-columns:repeat(3, 1fr); gap:14px; padding:12px 32px 32px; }}
  .card {{ background:var(--card); border:1px solid var(--line); border-radius:16px; padding:12px;
          display:grid; grid-template-columns:112px 1fr; gap:12px; }}
  .card img {{ width:112px; height:199px; border-radius:6px; display:block; }}
  .no {{ font-weight:700; font-size:15px; }} .no span {{ color:var(--muted); font-weight:400; font-size:12px; margin-left:6px; }}
  .row {{ font-size:12.5px; line-height:1.5; margin-top:5px; }} .row b {{ color:var(--muted); margin-right:4px; }}
  .nar {{ background:#e6f2ef; border-radius:6px; padding:5px 7px; }}
  @media (max-width:900px) {{ .grid {{ grid-template-columns:1fr; padding:12px 16px; }} header {{ padding:20px 16px 4px; }} }}
</style></head><body>
<header><h1>내 통장에 잠자는 숨은 돈 — 8컷 콘티</h1>
<div class="meta">1분 (+ 썸네일 1초) · 1080×1920 · 30fps · 자막 카드 y=1480 · 내레이션 ko-KR-Chirp3-HD-Charon · 지식 쇼츠 19편 · 3D 클레이 AI(Seedream 4.0) + 인포그래픽</div></header>
<div class="grid">{''.join(cards)}</div></body></html>"""
    out = os.path.join(EP, "storyboard.html")
    with open(out, "w") as f:
        f.write(page)
    # Playwright is installed for Node, so the PNG is taken with a short Node script
    shot = ("const {chromium}=require('playwright');(async()=>{const b=await chromium.launch();"
            "const p=await b.newPage({viewport:{width:1400,height:900}});await p.goto(process.argv[1]);"
            "await p.waitForTimeout(300);await p.screenshot({path:process.argv[2],fullPage:true});await b.close();})();")
    subprocess.run(["node", "-e", shot, "file://" + out, os.path.join(EP, "storyboard.png")], check=True)
    print("wrote", out)


if __name__ == "__main__":
    main()
