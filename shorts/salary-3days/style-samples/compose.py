import os, subprocess, random
from PIL import Image
W,H=1080,1920
def esc(s): return s.replace("&","&amp;").replace("<","&lt;")
def T(s,x,y,size,fill="#111",font="Do Hyeon",anchor="middle",extra=""):
    if font=="Nanum Pen" and not extra:
        size=int(size*1.3); extra=f'stroke="{fill}" stroke-width="{max(3,size//28)}" stroke-linejoin="round"'
    return f'<text x="{x}" y="{y}" font-family="{font}" font-size="{size}" fill="{fill}" text-anchor="{anchor}" {extra}>{esc(s)}</text>'
def render(name, body, base=None, bg=None):
    svg=f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}"><rect width="{W}" height="{H}" fill="{bg or "#000"}" fill-opacity="{1 if bg else 0}"/>{body}</svg>'
    open(name+".svg","w").write(svg)
    subprocess.run(["vectorcraft-cli","convert",name+".svg",name+"_ov.png"],check=True,capture_output=True)
    ov=Image.open(name+"_ov.png").convert("RGBA")
    if base:
        im=Image.open(base).convert("RGB").resize((W,H)).convert("RGBA")
        ov=Image.alpha_composite(im,ov)
    ov.convert("RGB").save(name+".png")

# ---- A. 웹툰
stroke='stroke="#111" stroke-width="12" paint-order="stroke" stroke-linejoin="round"'
A=('<rect x="24" y="24" width="1032" height="1872" fill="none" stroke="#111" stroke-width="14" rx="8"/>'
   + T("월급, 왜", 540, 230, 120, "#fff", "Black Han Sans", extra=stroke)
   + T("3일 만에 사라질까?", 540, 370, 108, "#ffe14d", "Black Han Sans", extra=stroke)
   # speech bubble with tail
   + '<path d="M600 560 Q600 470 760 470 H960 Q1040 470 1040 560 V640 Q1040 720 960 720 H820 L760 800 L770 720 H760 Q600 720 600 640 Z" fill="#fff" stroke="#111" stroke-width="8"/>'
   + T("어?! 내 월급", 820, 580, 54, "#111", "Jua") + T("어디 갔어?!", 820, 660, 54, "#e63946", "Jua")
   + T("털썩", 180, 1180, 90, "#e63946", "Jua", extra='stroke="#fff" stroke-width="10" paint-order="stroke" transform="rotate(-12 180 1180)"')
   # caption box
   + '<rect x="110" y="1400" width="860" height="170" rx="20" fill="#fff" stroke="#111" stroke-width="8"/>'
   + T("월급날 들어온 돈,", 540, 1470, 58) + T("어디로 갔을까요?", 540, 1545, 58))
render("A_webtoon", A, "webtoon.jpg")

# ---- B. 픽셀
px='style="font-family:Black Han Sans" stroke="#000" stroke-width="0"'
def shadowtext(s,x,y,size,fill):
    return T(s,x+8,y+8,size,"#000","Black Han Sans")+T(s,x,y,size,fill,"Black Han Sans")
hp="".join(f'<rect x="{300+i*44}" y="560" width="36" height="44" fill="{"#3ddc84" if i<3 else "#333"}"/>' for i in range(12))
B=('<rect x="40" y="120" width="1000" height="360" fill="#000" fill-opacity="0.55"/>'
   + shadowtext("월급, 왜", 540, 250, 116, "#ffd400") + shadowtext("3일 만에 사라질까?", 540, 400, 100, "#ffffff")
   + '<rect x="120" y="530" width="840" height="104" fill="#000" stroke="#fff" stroke-width="8"/>'
   + T("잔고", 210, 600, 48, "#fff", "Black Han Sans") + hp
   + shadowtext("-12,000", 860, 760, 64, "#ff4d4d")
   # RPG dialog box
   + '<rect x="70" y="1370" width="940" height="230" fill="#0b1a4a" stroke="#fff" stroke-width="10"/>'
   + '<rect x="86" y="1386" width="908" height="198" fill="none" stroke="#7fb2ff" stroke-width="4"/>'
   + T("월급날 들어온 돈,", 130, 1460, 60, "#fff", anchor="start") + T("어디로 갔을까요? ▼", 130, 1545, 60, "#fff", anchor="start"))
render("B_pixel", B, "pixel.jpg")

# ---- C. 콜라주 (ransom-note title)
random.seed(4)
cols=["#ffd400","#ffffff","#ff6b6b","#7ed6df","#f8a5c2","#c7ecee"]
def ransom(s,cx,y,size):
    out=""; w=size*0.95; x=cx-len(s)*w/2+w/2
    for ch in s:
        if ch==" ": x+=w*0.6; continue
        c=random.choice(cols); r=random.uniform(-8,8); f=random.choice(["Black Han Sans","Jua","Do Hyeon"])
        out+=(f'<g transform="rotate({r:.1f} {x:.0f} {y})"><rect x="{x-w/2+4:.0f}" y="{y-size*0.85:.0f}" width="{w-8:.0f}" height="{size*1.1:.0f}" fill="{c}" stroke="#111" stroke-width="3"/>'
              + T(ch,x,y,size*0.86,"#111",f)+'</g>')
        x+=w
    return out
tape=lambda x,y,r: f'<rect x="{x}" y="{y}" width="200" height="56" fill="#fff8d6" fill-opacity="0.8" transform="rotate({r} {x+100} {y+28})"/>'
C=(ransom("월급, 왜",540,260,118) + ransom("3일 만에 사라질까?",540,420,92)
   + tape(80,90,-14)+tape(800,80,12)
   # torn paper subtitle strip
   + '<path d="M80 1400 L140 1390 L220 1405 L320 1392 L420 1404 L540 1390 L660 1405 L760 1392 L880 1404 L1000 1394 L1000 1590 L900 1600 L780 1588 L660 1602 L540 1590 L420 1602 L300 1588 L180 1600 L80 1590 Z" fill="#fffdf3" stroke="#111" stroke-width="3"/>'
   + T("월급날 들어온 돈,", 540, 1475, 58, "#111", "Nanum Pen") + T("어디로 갔을까요?", 540, 1550, 64, "#e63946", "Nanum Pen")
   + tape(60,1370,-20)+tape(860,1560,15))
render("C_collage", C, "collage.jpg")

# ---- D. 화이트보드 (hand-drawn)
mk='fill="none" stroke="#1d1d1f" stroke-width="9" stroke-linecap="round" stroke-linejoin="round"'
blue='fill="none" stroke="#1565c0" stroke-width="9" stroke-linecap="round" stroke-linejoin="round"'
red='fill="none" stroke="#d32f2f" stroke-width="9" stroke-linecap="round" stroke-linejoin="round"'
def bill(x,y,r):
    return (f'<g transform="rotate({r} {x} {y})"><rect x="{x-70}" y="{y-38}" width="140" height="76" rx="6" fill="#e8f5e9" stroke="#2e7d32" stroke-width="7"/>'
            f'<circle cx="{x}" cy="{y}" r="20" fill="none" stroke="#2e7d32" stroke-width="6"/>'
            f'<path d="M{x-70} {y-20} q-50 -40 -90 -10 M{x+70} {y-20} q50 -40 90 -10" fill="none" stroke="#1d1d1f" stroke-width="7" stroke-linecap="round"/></g>')
D=('<rect width="1080" height="1920" fill="#fbfbf7"/>'
   + T("월급, 왜", 540, 260, 130, "#1d1d1f", "Nanum Pen")
   + T("3일 만에 사라질까?", 540, 400, 120, "#d32f2f", "Nanum Pen")
   + f'<path d="M260 440 Q540 470 820 438" {red}/>'
   # stick figure with phone
   + f'<circle cx="400" cy="900" r="70" {mk}/><path d="M375 885 h2 M425 885 h2" {mk}/><ellipse cx="400" cy="935" rx="16" ry="20" {mk}/>'
   + f'<path d="M400 970 V1210 M400 1040 L500 1000 M400 1040 L300 1110 M400 1210 L330 1330 M400 1210 L470 1330" {mk}/>'
   + f'<rect x="490" y="930" width="80" height="140" rx="12" {blue}/>'
   + f'<path d="M455 800 l-20 -30 M400 790 v-36 M345 800 l20 -30" {mk}/>'
   + bill(720,780,-12) + bill(860,640,10) + bill(700,560,-6)
   + f'<path d="M580 950 Q650 880 690 820" {blue}/><path d="M672 838 L692 818 L700 846" {blue}/>'
   + T("내 월급…", 760, 1050, 64, "#1565c0", "Nanum Pen")
   + f'<path d="M120 1390 H960" fill="none" stroke="#1d1d1f" stroke-width="3" stroke-dasharray="4 14" stroke-linecap="round"/>'
   + T("월급날 들어온 돈,", 540, 1480, 70, "#1d1d1f", "Nanum Pen") + T("어디로 갔을까요?", 540, 1570, 76, "#1d1d1f", "Nanum Pen")
   # marker in corner
   + '<g transform="rotate(-30 900 1750)"><rect x="840" y="1730" width="200" height="40" rx="10" fill="#d32f2f"/><path d="M1040 1735 L1080 1750 L1040 1765 Z" fill="#333"/></g>')
render("D_whiteboard", D)

sh=Image.new('RGB',(4*360+50,640+20),'#222')
for i,n in enumerate(("A_webtoon","B_pixel","C_collage","D_whiteboard")):
    sh.paste(Image.open(n+".png").resize((360,640)),(10+i*370,10))
sh.save("styles_sheet.png")
print("ok")
