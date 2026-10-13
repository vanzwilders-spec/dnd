from PIL import Image, ImageDraw, ImageFont
W,H=1498,1236
k=1236/600.0; ox=37
def c(sx,sy): return (int((sx-ox)*k/ (1.0) *1.0/ (1.0)) if False else int((sx-ox)/ (600/1236.0)), int(sy/(600/1236.0)))
F="/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"; FS="/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
def f(s,p=F): return ImageFont.truetype(p,s)
im=Image.new("RGBA",(W,H),(0,0,0,0)); d=ImageDraw.Draw(im)
def lab(t,p,sz=26,col=(255,240,200,255),anchor="mm"):
    for dx,dy in ((-2,0),(2,0),(0,2),(0,-2)): d.text((p[0]+dx,p[1]+dy),t,font=f(sz),fill=(10,8,8,255),anchor=anchor)
    d.text(p,t,font=f(sz),fill=col,anchor=anchor)
def haz(id,p):
    r=24; d.ellipse([p[0]-r,p[1]-r,p[0]+r,p[1]+r],fill=(170,36,36,235),outline=(255,225,205,255),width=3)
    d.text(p,id,font=f(22,FS),fill=(255,255,255,255),anchor="mm")
def ring(p,col,r=44,w=6):
    d.ellipse([p[0]-r,p[1]-r,p[0]+r,p[1]+r],outline=col,width=w)

items={}
# refuge hearth token location (left wall nook)
hearth=c(112,292); ring(hearth,(240,200,90,255)); lab("REFUGE HEARTH",(hearth[0]+10,hearth[1]-62),22,(250,215,110,255)); lab("place hearth token here",(hearth[0]+10,hearth[1]+62),18,(250,215,110,255))
# room labels
lab("THE McTAVERN: Dining Room",c(400,200),34)
lab("Mordax's stage",c(125,70),22)
lab("Kitchen",c(650,400),30)
lab("Servants' quarters",c(135,540),24)
lab("bar",c(455,330),22)
# cellar stair (S3)
p=c(530,395); ring(p,(230,120,190,255),38,5); lab("S3 stair to Wine Cellar (secret)",(p[0],p[1]+52),18,(235,140,200,255))
# kitchen hearth
kh=c(700,528); ring(kh,(240,200,90,255),36,5); lab("Kitchen hearth",(kh[0]-5,kh[1]+48),18,(250,215,110,255))
# doors
for name,pt,off in (("to Entry Hall",c(505,48),(0,46)),("to Study",c(75,238),(70,-4)),("to Drawing Room",c(722,452),(-110,60)),("to Servant's Passage",c(300,562),(0,-46))):
    ring(pt,(210,160,80,255),30,4); lab(name,(pt[0]+off[0],pt[1]+off[1]),18)
# hazards (see Session1_Hazards.md)
H=[("T1",c(445,352)),("T2",c(420,372)),("T3",c(330,150)),("T4",c(610,455)),("T5",c(672,418)),("T6",c(115,95))]
for i,pt in H: haz(i,pt)
# 30px grid hint off; save
im.save("Session1_McTavern_Overlay.png")
# check composite on screenshot
bg=Image.open("/root/.claude/projects/-home-claude/fdf7333d-f120-5114-96b4-56f930e860eb/tool-results/mcp-remote-devices-blob-1791843884963-eqas3q.jpg").convert("RGBA")
scale=600/1236.0
ov=im.resize((int(1498*scale),600))
bg.alpha_composite(ov,(ox,0)); bg.convert("RGB").save("/tmp/mct_check.png")
print(hearth)
