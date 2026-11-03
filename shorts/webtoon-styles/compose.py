"""Puts the same title / bubble / caption on each style sample and builds styles_sheet.png."""
import subprocess
from PIL import Image, ImageDraw, ImageFont
W, H = 1080, 1920
def esc(s): return s.replace("&", "&amp;").replace("<", "&lt;")
def T(s, x, y, size, fill="#111", font="Do Hyeon", extra=""):
    return f'<text x="{x}" y="{y}" font-family="{font}" font-size="{size}" fill="{fill}" text-anchor="middle" {extra}>{esc(s)}</text>'
def render(name, body, base):
    svg = f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}">{body}</svg>'
    open(name + ".svg", "w").write(svg)
    subprocess.run(["vectorcraft-cli", "convert", name + ".svg", name + "_ov.png"], check=True, capture_output=True)
    im = Image.open(base).convert("RGB").resize((W, H)).convert("RGBA")
    Image.alpha_composite(im, Image.open(name + "_ov.png").convert("RGBA")).convert("RGB").save(name + ".png")

# per style: (frame color, title colors, title stroke, bubble fill/stroke, sfx color, caption box, font for sfx/bubble)
S = {
    "1_watercolor": dict(frame="#8a6a5a", t1="#fff", t2="#ffe3b3", ts="#7a4a3a", bub="#fffaf2", bs="#8a6a5a", sfx="#e07a5f", cap="#fffaf2", cs="#8a6a5a", font="Nanum Pen", fs=1.35),
    "2_chibi": dict(frame="#111", t1="#fff", t2="#ffe14d", ts="#111", bub="#fff", bs="#111", sfx="#ff3b6b", cap="#fff", cs="#111", font="Jua", fs=1.0),
    "3_manga": dict(frame="#111", t1="#fff", t2="#fff", ts="#111", bub="#fff", bs="#111", sfx="#e63946", cap="#fff", cs="#111", font="Black Han Sans", fs=1.0),
    "4_action": dict(frame="#111", t1="#fff", t2="#ffb703", ts="#2b1055", bub="#fff", bs="#111", sfx="#ff5400", cap="#14141f", cs="#ffb703", font="Black Han Sans", fs=1.0),
    "5_simple": dict(frame="#333", t1="#333", t2="#ff6b6b", ts="#fff", bub="#fff", bs="#333", sfx="#ff6b6b", cap="#fff", cs="#333", font="Nanum Pen", fs=1.35),
}
for k, c in S.items():
    st = f'stroke="{c["ts"]}" stroke-width="13" paint-order="stroke" stroke-linejoin="round"'
    capt = "#ffb703" if k == "4_action" else "#111"
    f, fs = c["font"], c["fs"]
    body = (f'<rect x="24" y="24" width="1032" height="1872" fill="none" stroke="{c["frame"]}" stroke-width="14" rx="8"/>'
            + T("은행은 왜", 540, 230, 120, c["t1"], "Black Han Sans", st)
            + T("4시에 문 닫을까?", 540, 370, 108, c["t2"], "Black Han Sans", st)
            + f'<path d="M60 560 Q60 480 200 480 H400 Q480 480 480 560 V620 Q480 700 400 700 H330 L380 790 L270 700 H200 Q60 700 60 620 Z" fill="{c["bub"]}" stroke="{c["bs"]}" stroke-width="8"/>'
            + T("벌써 닫았어?!", 270, 610, int(56 * fs), "#111", f, "" if f != "Nanum Pen" else 'stroke="#111" stroke-width="2"')
            + T("철컥!", 860, 560, int(100 * fs), c["sfx"], "Jua" if f != "Nanum Pen" else f, f'stroke="#fff" stroke-width="10" paint-order="stroke" transform="rotate(10 860 560)"')
            + f'<rect x="118" y="1408" width="860" height="170" rx="20" fill="{c["cs"]}"/>'
            + f'<rect x="110" y="1400" width="860" height="170" rx="20" fill="{c["cap"]}" stroke="{c["cs"]}" stroke-width="8"/>'
            + T("은행은 왜 4시면", 540, 1470, 58, capt) + T("문을 닫을까요?", 540, 1545, 58, capt))
    render(k, body, k + ".jpg")

labels = ["① 수채화 감성", "② SD 개그(치비)", "③ 흑백 만화(스크린톤)", "④ 액션 세미리얼", "⑤ 심플 일상툰(인스타툰)"]
tw, th = 360, 640
sheet = Image.new("RGB", (tw * 5 + 60, th + 120), "#f4f1ea")
d = ImageDraw.Draw(sheet)
font = ImageFont.truetype(subprocess.run(["fc-match", "-f", "%{file}", "Do Hyeon"], capture_output=True, text=True).stdout, 34)
for i, k in enumerate(S):
    sheet.paste(Image.open(k + ".png").resize((tw, th)), (10 + i * (tw + 10), 10))
    d.text((10 + i * (tw + 10) + tw / 2, th + 60), labels[i], fill="#111", font=font, anchor="mm")
sheet.save("styles_sheet.png")
