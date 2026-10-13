"""McTavern overlay (transparent, 1498x1236). Coordinates are measured on the actual McTavern map image.
The map art itself is third-party and is never stored in the public repo."""
from PIL import Image, ImageDraw, ImageFont
import sys
W,H=1498,1236
SX=W/1501.0; SY=H/1240.0
def c(x,y): return (int(x*SX),int(y*SY))
F="/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"; FS="/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
def f(s,p=F): return ImageFont.truetype(p,s)
im=Image.new("RGBA",(W,H),(0,0,0,0)); d=ImageDraw.Draw(im)
def lab(t,p,sz=26,col=(255,240,200,255),anchor="mm"):
    for dx,dy in ((-2,0),(2,0),(0,2),(0,-2),(2,2),(-2,-2)): d.text((p[0]+dx,p[1]+dy),t,font=f(sz),fill=(10,8,8,255),anchor=anchor)
    d.text(p,t,font=f(sz),fill=col,anchor=anchor)
def haz(i,p):
    r=24; d.ellipse([p[0]-r,p[1]-r,p[0]+r,p[1]+r],fill=(170,36,36,235),outline=(255,225,205,255),width=3)
    d.text(p,i,font=f(22,FS),fill=(255,255,255,255),anchor="mm")
def ring(p,col,r=44,w=6):
    d.ellipse([p[0]-r,p[1]-r,p[0]+r,p[1]+r],outline=col,width=w)
GOLD=(250,215,110,255); PINK=(235,140,200,255)
hearth=c(100,495); ring(hearth,(240,200,90,255),46,6); lab("REFUGE HEARTH",(hearth[0]+120,hearth[1]-66),22,GOLD); lab("hearth token here",(hearth[0]+110,hearth[1]+66),18,GOLD)
lab("THE McTAVERN",c(770,560),34); lab("Mordax's stage",c(185,125),22)
lab("Kitchen",c(1270,870),30); lab("Servants' quarters",c(215,890),24)
p=c(990,832); ring(p,(230,120,190,255),38,5); lab("S3 stair to Wine Cellar (secret)",(p[0]-40,p[1]+56),18,PINK)
kh=c(1368,1105); ring(kh,(240,200,90,255),40,5); lab("Kitchen hearth",(kh[0]-70,kh[1]+58),18,GOLD)
for name,pt,off in (("to Entry Hall",c(965,95),(0,48)),("to Study",c(92,330),(80,0)),("to Drawing Room",c(1418,330),(-110,0)),("to Servant's Passage",c(435,772),(0,-48))):
    ring(pt,(210,160,80,255),30,4); lab(name,(pt[0]+off[0],pt[1]+off[1]),18)
for i,pt in [("T1",c(900,598)),("T2",c(700,752)),("T3",c(790,392)),("T4",c(1250,1010)),("T5",c(1375,930)),("T6",c(165,215))]: haz(i,pt)
im.save("Session1_McTavern_Overlay.png")
if len(sys.argv)>1:   # local alignment check only; never saved to the repo
    bg=Image.open(sys.argv[1]).convert("RGBA").resize((W,H)); bg.alpha_composite(im); bg.convert("RGB").resize((1000,int(1000*H/W))).save(sys.argv[2])
