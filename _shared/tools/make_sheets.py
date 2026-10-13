"""Cartographer-style reference sheets (framed, legend, hazard key, scale, compass) from the VTT maps."""
import sys, os, math, random
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import make_maps as M
S=M.S; K=M.K
SER="/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SERB="/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SERI="/usr/share/fonts/truetype/dejavu/DejaVuSerif-Italic.ttf"
def F(sz,p=SERB):
    try: return ImageFont.truetype(p,int(sz*K))
    except OSError: return ImageFont.truetype(SERB,int(sz*K))
INK=(52,36,24); PARCH=(226,208,170); RED=(150,40,36)
MAR=3*S; PANEL=13*S

KEYS={
 "Ground":("Ravensmoor Manor","Ground Floor",[
  ("G1","Grand stair: creaking treads, then a broken tread"),("G2","Chandelier: swings, drops, crashes (Entry hearth gutters)"),
  ("G5","Study shelves: tip, then slide shut on the bookcase"),("G6","Drawing Room statues: move when unwatched; Twins' game"),
  ("G7","Servant's Passage flagstones: loose, then a 10-ft drop"),("G8","Wet stair: slip, then icy for an hour"),
  ("T1-T6","The McTavern hazards: see the Hazard Key")]),
 "Upper":("Ravensmoor Manor","Upper Floor",[
  ("U1","Trophy cases: pressure plates; the Collector arrives"),("U2","Portrait Gallery boards: eyes follow, then flash (Wis)"),
  ("U3","Party's own items on display: the Collector takes extra"),("U4","Upper Hall rug: slip, grapple, difficult terrain")]),
 "Cellar":("Ravensmoor Manor","The Cellar",[
  ("C1","Sunken tier: slip, fall, then floods"),("C2","Wine racks: tip and pin; block the stair"),
  ("C3","Pantry cold: Chilled stacks, then frozen"),("C4","Furnace catwalk (set piece): plank, then collapse into the pit"),
  ("C5","Steam vent: burn, then the room fills"),("C6","Hidden Chamber cold: Chilled; the door seals")]),
}

def wrap(d,text,font,maxw):
    words=text.split(); lines=[]; cur=""
    for w in words:
        t=(cur+" "+w).strip()
        if d.textlength(t,font=font)<=maxw: cur=t
        else: lines.append(cur); cur=w
    if cur: lines.append(cur)
    return lines

def compass(d,cx,cy,r):
    for ang in range(0,360,45):
        a=math.radians(ang); long=(ang%90==0)
        rr=r if long else r*.62
        tip=(cx+math.sin(a)*rr,cy-math.cos(a)*rr)
        l=(cx+math.sin(a-.28)*r*.22,cy-math.cos(a-.28)*r*.22); rt=(cx+math.sin(a+.28)*r*.22,cy-math.cos(a+.28)*r*.22)
        d.polygon([tip,l,(cx,cy)],fill=INK if long else (110,84,60)); d.polygon([tip,rt,(cx,cy)],fill=(226,208,170),outline=INK)
    d.ellipse([cx-r*1.12,cy-r*1.12,cx+r*1.12,cy+r*1.12],outline=INK,width=int(2*K))
    d.text((cx,cy-r*1.32),"N",font=F(20),fill=INK,anchor="mm")

def scalebar(d,x,y,squares=5,unit=5):
    for i in range(squares*2):
        d.rectangle([x+i*S/2,y,x+(i+1)*S/2,y+10*K],fill=INK if i%2==0 else PARCH,outline=INK,width=int(1.5*K))
    for i in range(squares+1):
        d.text((x+i*S,y+24*K),str(i*unit),font=F(11),fill=INK,anchor="mm")
    d.text((x+squares*S+30*K,y+24*K),"feet",font=F(11,SERI),fill=INK,anchor="lm")

def sheet(name):
    fn={"Ground":M.ground,"Upper":M.upper,"Cellar":M.cellar}[name]
    im=M.finish(fn(True),M.GLOW[name],True) if hasattr(M,"GLOW") else fn(True)
    W=im.size[0]+2*MAR+PANEL; H=im.size[1]+2*MAR
    rng=np.random.default_rng(3)
    base=np.zeros((H,W,3),np.float32)+np.array(PARCH,np.float32)
    base+=rng.normal(0,5,(H,W))[:,:,None]
    yy,xx=np.mgrid[0:H,0:W]
    v=np.hypot((xx-W/2)/(W/2),(yy-H/2)/(H/2)); base*=(1-.22*np.clip(v-.5,0,1)**1.3)[:,:,None]
    for _ in range(14):   # faint stains
        cx,cy,r=rng.integers(0,W),rng.integers(0,H),rng.integers(60,260)
        base-= (np.clip(1-np.hypot(xx-cx,yy-cy)/r,0,1)**2*rng.uniform(4,12))[:,:,None]
    sh=Image.fromarray(np.clip(base,0,255).astype(np.uint8)); d=ImageDraw.Draw(sh)
    # map with frame
    d.rectangle([MAR-int(9*K),MAR-int(9*K),MAR+im.size[0]+int(9*K),MAR+im.size[1]+int(9*K)],outline=INK,width=int(3*K))
    sh.paste(im,(MAR,MAR))
    d.rectangle([MAR-int(4*K),MAR-int(4*K),MAR+im.size[0]+int(4*K),MAR+im.size[1]+int(4*K)],outline=INK,width=int(1.5*K))
    # edge ticks and coordinates (5-ft squares; numbers every 5 squares = 25 ft)
    for i in range(M.W+1):
        x=MAR+i*S; L=10*K if i%5==0 else 5*K
        d.line([x,MAR-9*K-L,x,MAR-9*K],fill=INK,width=int(1.5*K)); d.line([x,MAR+im.size[1]+9*K,x,MAR+im.size[1]+9*K+L],fill=INK,width=int(1.5*K))
        if i%5==0: d.text((x,MAR-9*K-L-12*K),str(i*5),font=F(11),fill=INK,anchor="mm")
    for j in range(M.H+1):
        y=MAR+j*S; L=10*K if j%5==0 else 5*K
        d.line([MAR-9*K-L,y,MAR-9*K,y],fill=INK,width=int(1.5*K))
        if j%5==0: d.text((MAR-9*K-L-14*K,y),str(j*5),font=F(11),fill=INK,anchor="mm")
    # title cartouche
    kind,title,haz=KEYS[name]
    px=MAR+im.size[0]+MAR; pw=PANEL-MAR
    d.rectangle([px,MAR,px+pw,MAR+int(2.8*S)],outline=INK,width=int(3*K)); d.rectangle([px+6*K,MAR+6*K,px+pw-6*K,MAR+int(2.8*S)-6*K],outline=INK,width=int(1.2*K))
    d.text((px+pw/2,MAR+.75*S),kind.upper(),font=F(15),fill=INK,anchor="mm")
    d.text((px+pw/2,MAR+1.5*S),title,font=F(28),fill=RED,anchor="mm")
    d.text((px+pw/2,MAR+2.3*S),"The Reveler's Stage  -  DM reference",font=F(11,SERI),fill=INK,anchor="mm")
    # legend
    y=MAR+int(3.4*S)
    d.text((px,y),"LEGEND",font=F(16),fill=INK,anchor="lm"); d.line([px,y+14*K,px+pw,y+14*K],fill=INK,width=int(1.5*K)); y+=int(.9*S)
    def row(draw,label):
        nonlocal y
        draw(px+.5*S,y); d.text((px+1.25*S,y),label,font=F(12,SER),fill=INK,anchor="lm"); y+=int(.78*S)
    row(lambda x,yy_: (d.rectangle([x-.4*S,yy_-6*K,x+.4*S,yy_+6*K],fill=(120,84,52),outline=(40,26,16),width=int(2*K))),"Door")
    row(lambda x,yy_: (d.rectangle([x-.4*S,yy_-6*K,x+.4*S,yy_+6*K],fill=(120,84,52),outline=(170,80,140),width=int(2*K)),d.line([x-.4*S,yy_-6*K,x+.4*S,yy_+6*K],fill=(170,80,140),width=int(3*K))),"Secret door or passage (DM only)")
    row(lambda x,yy_: (d.rectangle([x-.4*S,yy_-.3*S,x+.4*S,yy_+.3*S],fill=(128,112,92),outline=(30,24,20),width=int(2*K)),[d.line([x-.4*S,yy_-.3*S+i*.2*S,x+.4*S,yy_-.3*S+i*.2*S],fill=(60,50,42),width=int(2*K)) for i in range(1,3)]),"Stairs (up or down as labelled)")
    row(lambda x,yy_: (d.rectangle([x-.3*S,yy_-.3*S,x+.3*S,yy_+.3*S],fill=(58,50,48),outline=(15,12,10),width=int(3*K)),d.ellipse([x-.14*S,yy_-.14*S,x+.14*S,yy_+.14*S],fill=(230,130,40))),"Hearth (Night Clock: goes out at 1:00, 3:00, 4:30)")
    row(lambda x,yy_: (d.ellipse([x-13*K,yy_-13*K,x+13*K,yy_+13*K],fill=(170,36,36),outline=(255,220,200),width=int(2*K)),d.text((x,yy_),"G1",font=F(10,M.FS),fill=(255,255,255),anchor="mm")),"Hazard pip (key below; 3 strikes, shared)")
    row(lambda x,yy_: (d.rectangle([x-.3*S,yy_-.3*S,x+.3*S,yy_+.3*S],fill=(96,98,104),outline=(30,30,36),width=int(2*K)),d.ellipse([x-.18*S,yy_-.18*S,x+.18*S,yy_+.18*S],fill=(214,216,222))),"Statue on a plinth")
    row(lambda x,yy_: d.rectangle([x-.4*S,yy_-.22*S,x+.4*S,yy_+.22*S],fill=(60,40,28),outline=(20,14,10),width=int(2*K)),"Furniture")
    y+=int(.2*S)
    d.text((px,y),"HAZARD KEY",font=F(16),fill=INK,anchor="lm"); d.line([px,y+14*K,px+pw,y+14*K],fill=INK,width=int(1.5*K)); y+=int(1.0*S)
    f=F(11.5,SER)
    for hid,txt in haz:
        d.ellipse([px+2*K,y-11*K,px+24*K,y+11*K],fill=(170,36,36),outline=(255,220,200),width=int(1.5*K))
        d.text((px+13*K,y),hid if len(hid)<=2 else "T",font=F(9 if len(hid)>2 else 10,M.FS),fill=(255,255,255),anchor="mm")
        lines=wrap(d,(hid+": " if len(hid)>2 else "")+txt,f,pw-40*K)
        for k,l in enumerate(lines): d.text((px+34*K,y+k*17*K-(len(lines)-1)*8*K),l,font=f,fill=INK,anchor="lm")
        y+=int(max(.66*S,len(lines)*17*K+10*K))
    # compass and scale
    compass(d,px+pw-2.0*S,H-MAR-1.7*S,1.0*S)
    scalebar(d,px+.3*S,H-MAR-1.55*S)
    d.text((px+.3*S,H-MAR-.3*S),"One square = 5 ft.  North is up.",font=F(11,SERI),fill=INK,anchor="lm")
    return sh

if __name__=="__main__":
    out=sys.argv[1] if len(sys.argv)>1 else "."
    for n in ("Ground","Upper","Cellar"):
        sheet(n).convert("RGB").save(f"{out}/Session1_{n}_DM_Sheet.png",optimize=True)
    print("ok")
