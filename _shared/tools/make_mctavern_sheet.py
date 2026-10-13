"""Cartographer-style DM sheet for the McTavern (original map + overlay), 30 px = 5 ft assumed."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
from PIL import Image, ImageDraw
import make_sheets as MS
M=MS.M; S=MS.S; K=MS.K; F=MS.F; INK=MS.INK; RED=MS.RED
src=sys.argv[1]; out=sys.argv[2]
im=Image.open(src).convert("RGB")
f=2560/im.size[0]; im=im.resize((2560,int(im.size[1]*f)),Image.LANCZOS)
sq=30*f                                   # one 5-ft square in sheet pixels
MAR=MS.MAR; PANEL=MS.PANEL
W=im.size[0]+2*MAR+PANEL; H=im.size[1]+2*MAR
rng=np.random.default_rng(5)
base=np.zeros((H,W,3),np.float32)+np.array(MS.PARCH,np.float32)
base+=rng.normal(0,5,(H,W))[:,:,None]
yy,xx=np.mgrid[0:H,0:W]
v=np.hypot((xx-W/2)/(W/2),(yy-H/2)/(H/2)); base*=(1-.22*np.clip(v-.5,0,1)**1.3)[:,:,None]
for _ in range(14):
    cx,cy,r=rng.integers(0,W),rng.integers(0,H),rng.integers(60,260)
    base-=(np.clip(1-np.hypot(xx-cx,yy-cy)/r,0,1)**2*rng.uniform(4,12))[:,:,None]
sh=Image.fromarray(np.clip(base,0,255).astype(np.uint8)); d=ImageDraw.Draw(sh)
iw,ih=im.size
d.rectangle([MAR-9*K,MAR-9*K,MAR+iw+9*K,MAR+ih+9*K],outline=INK,width=int(3*K))
sh.paste(im,(MAR,MAR))
d.rectangle([MAR-4*K,MAR-4*K,MAR+iw+4*K,MAR+ih+4*K],outline=INK,width=int(1.5*K))
# faint 5-ft grid over the map
ov=Image.new("RGBA",(iw,ih),(0,0,0,0)); g=ImageDraw.Draw(ov)
n=0
while n*sq<iw: g.line([n*sq,0,n*sq,ih],fill=(255,255,255,38 if n%5 else 70),width=1); n+=1
n=0
while n*sq<ih: g.line([0,n*sq,iw,n*sq],fill=(255,255,255,38 if n%5 else 70),width=1); n+=1
sh.paste(ov,(MAR,MAR),ov)
# edge ticks in feet
n=0
while n*sq<=iw:
    x=MAR+n*sq; L=10*K if n%5==0 else 5*K
    d.line([x,MAR-9*K-L,x,MAR-9*K],fill=INK,width=int(1.5*K)); d.line([x,MAR+ih+9*K,x,MAR+ih+9*K+L],fill=INK,width=int(1.5*K))
    if n%5==0: d.text((x,MAR-9*K-L-12*K),str(n*5),font=F(11),fill=INK,anchor="mm")
    n+=1
n=0
while n*sq<=ih:
    y=MAR+n*sq; L=10*K if n%5==0 else 5*K
    d.line([MAR-9*K-L,y,MAR-9*K,y],fill=INK,width=int(1.5*K))
    if n%5==0: d.text((MAR-9*K-L-14*K,y),str(n*5),font=F(11),fill=INK,anchor="mm")
    n+=1
# panel
px=MAR+iw+MAR; pw=PANEL-MAR
d.rectangle([px,MAR,px+pw,MAR+int(2.8*S)],outline=INK,width=int(3*K)); d.rectangle([px+6*K,MAR+6*K,px+pw-6*K,MAR+int(2.8*S)-6*K],outline=INK,width=int(1.2*K))
d.text((px+pw/2,MAR+.75*S),"RAVENSMOOR MANOR",font=F(15),fill=INK,anchor="mm")
d.text((px+pw/2,MAR+1.5*S),"The McTavern",font=F(28),fill=RED,anchor="mm")
d.text((px+pw/2,MAR+2.3*S),"The Reveler's Stage  -  DM reference",font=F(11,MS.SERI),fill=INK,anchor="mm")
y=MAR+int(3.4*S)
d.text((px,y),"LEGEND",font=F(16),fill=INK,anchor="lm"); d.line([px,y+14*K,px+pw,y+14*K],fill=INK,width=int(1.5*K)); y+=int(.9*S)
def row(draw,label):
    global y
    draw(px+.5*S,y); d.text((px+1.25*S,y),label,font=F(12,MS.SER),fill=INK,anchor="lm"); y+=int(.78*S)
row(lambda x,yy_: d.ellipse([x-.3*S,yy_-.3*S,x+.3*S,yy_+.3*S],outline=(240,200,90),width=int(4*K)),"Hearth (gold ring): the refuge hearth never goes out")
row(lambda x,yy_: d.ellipse([x-.3*S,yy_-.3*S,x+.3*S,yy_+.3*S],outline=(230,120,190),width=int(4*K)),"Secret stair to the Wine Cellar (S3)")
row(lambda x,yy_: d.ellipse([x-.3*S,yy_-.3*S,x+.3*S,yy_+.3*S],outline=(210,160,80),width=int(3*K)),"Door or portal to another scene")
row(lambda x,yy_: (d.ellipse([x-13*K,yy_-13*K,x+13*K,yy_+13*K],fill=(170,36,36),outline=(255,220,200),width=int(2*K)),d.text((x,yy_),"T1",font=F(10,M.FS),fill=(255,255,255),anchor="mm")),"Hazard pip (key below; 3 strikes, shared)")
y+=int(.2*S)
d.text((px,y),"HAZARD KEY",font=F(16),fill=INK,anchor="lm"); d.line([px,y+14*K,px+pw,y+14*K],fill=INK,width=int(1.5*K)); y+=int(1.0*S)
fnt=F(11.5,MS.SER)
for hid,txt in [("T1","Bar floor: ale slick; slip, then difficult terrain"),("T2","Glass shelf behind the bar: collapses over the cellar stair"),
 ("T3","Oil lamps on the tables: tip, then fire spreads"),("T4","Kitchen flagstones: grease; slip, then scalding steam"),
 ("T5","Kitchen steam vent: burns; fills the Servant's Passage door"),("T6","Mordax's piano: dirge (Wis); or let Milo walk the keys")]:
    d.ellipse([px+2*K,y-11*K,px+24*K,y+11*K],fill=(170,36,36),outline=(255,220,200),width=int(1.5*K))
    d.text((px+13*K,y),hid,font=F(10,M.FS),fill=(255,255,255),anchor="mm")
    lines=MS.wrap(d,txt,fnt,pw-40*K)
    for k,l in enumerate(lines): d.text((px+34*K,y+k*17*K-(len(lines)-1)*8*K),l,font=fnt,fill=INK,anchor="lm")
    y+=int(max(.66*S,len(lines)*17*K+10*K))
MS.compass(d,px+pw-2.0*S,H-MAR-1.7*S,1.0*S)
x0=px+.3*S
for i in range(10):
    d.rectangle([x0+i*sq/2,H-MAR-1.55*S,x0+(i+1)*sq/2,H-MAR-1.55*S+10*K],fill=INK if i%2==0 else MS.PARCH,outline=INK,width=int(1.5*K))
for i in range(6): d.text((x0+i*sq,H-MAR-1.55*S+24*K),str(i*5),font=F(11),fill=INK,anchor="mm")
d.text((x0+5*sq+30*K,H-MAR-1.55*S+24*K),"feet",font=F(11,MS.SERI),fill=INK,anchor="lm")
d.text((x0,H-MAR-.3*S),"One square = 5 ft (30 px assumed).  North is up.",font=F(11,MS.SERI),fill=INK,anchor="lm")
sh.convert("RGB").save(out,optimize=True); print(sh.size)
