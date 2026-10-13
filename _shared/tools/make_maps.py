from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageChops
import math, random
import numpy as np
S=64; K=S/32; W,H=40,26
F="/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
FS="/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
def font(sz,f=F): return ImageFont.truetype(f,int(sz*K))
WOOD=(104,72,46); WOOD2=(70,48,30); STONE=(72,74,82); STONE2=(52,54,62)
OUT=(14,16,26); WALL=(24,18,15); DOOR=(150,104,52)
def P(x,y): return (x*S,y*S)
def _w(w): return max(1,int(round(w*K)))

def rect(d,x1,y1,x2,y2,fill,outline=None,w=1):
    d.rectangle([x1*S,y1*S,x2*S,y2*S],fill=fill,outline=outline,width=_w(w))

def _jit(c,rnd,a):
    v=rnd.randint(-a,a); return tuple(max(0,min(255,x+v)) for x in c)

def floor(d,r,kind):
    x1,y1,x2,y2=r
    rnd=random.Random(int(x1*7+y1*13))
    if kind=="wood":
        # planks 0.5 square wide, running left-right, with staggered butt joints
        for yy in range(int(y1*2),int(y2*2)):
            py=yy*S/2; col=_jit(WOOD,rnd,10)
            rect(d,x1,yy/2,x2,yy/2+.5,col)
            d.line([x1*S,py,x2*S,py],fill=(40,26,16),width=_w(1.4))
            d.line([x1*S,py+_w(1.5),x2*S,py+_w(1.5)],fill=_jit((126,92,60),rnd,4),width=1)
            xx=x1*S+rnd.randint(20,200)
            while xx<x2*S:
                d.line([xx,py,xx,py+S/2],fill=(40,26,16),width=_w(1.2))
                for nx in (xx-6*K,xx+6*K): d.ellipse([nx-1.5*K,py+S/4-1.5*K,nx+1.5*K,py+S/4+1.5*K],fill=(46,32,20))
                xx+=rnd.randint(180,420)
            for _ in range(int((x2-x1)*1.2)):  # grain
                gx=x1*S+rnd.random()*(x2-x1)*S; gy=py+rnd.random()*S/2
                d.line([gx,gy,gx+rnd.randint(14,60)*K/2,gy],fill=_jit(WOOD2,rnd,6),width=1)
    else:
        rect(d,x1,y1,x2,y2,STONE2)
        for yy in range(int(y1),int(y2)):
            off=0 if yy%2==0 else .5
            xx=x1-off
            while xx<x2:
                wd=1.0
                a,b=max(xx,x1),min(xx+wd,x2)
                if b>a:
                    rect(d,a,yy,b,yy+1,_jit(STONE,rnd,9))
                    d.rectangle([a*S,yy*S,b*S,(yy+1)*S],outline=(30,31,38),width=_w(1.6))
                    if rnd.random()<.25: d.line([a*S+8*K,yy*S+10*K,a*S+22*K,yy*S+18*K],fill=(42,44,52),width=1)
                xx+=wd

def shadow_rect(d,x1,y1,x2,y2,off=.12):
    pass

def walls(d,rooms,doors,secret=None,show_secret=False):
    for r in rooms: wall_box(d,r)
    for dr in doors: door(d,dr)
    if show_secret and secret:
        for dr in secret: door(d,dr,secret=True)

def wall_box(d,r):
    d.rectangle([r[0]*S,r[1]*S,r[2]*S,r[3]*S],outline=WALL,width=_w(11))
    d.rectangle([r[0]*S+_w(5),r[1]*S+_w(3),r[2]*S-_w(5),r[3]*S-_w(5)],outline=(84,70,60),width=1)

def door(d,dr,secret=False):
    x1,y1,x2,y2=dr[:4]
    col=(170,80,140) if secret else DOOR
    horiz=(y1==y2)
    if horiz:
        d.rectangle([x1*S+2*K,y1*S-6*K,x2*S-2*K,y1*S+6*K],fill=(120,84,52),outline=(40,26,16),width=_w(2))
        d.line([(x1+x2)*S/2,y1*S-6*K,(x1+x2)*S/2,y1*S+6*K],fill=(40,26,16),width=_w(1.5))
        d.ellipse([x2*S-9*K,y1*S-2*K,x2*S-5*K,y1*S+2*K],fill=(210,170,70))
    else:
        d.rectangle([x1*S-6*K,y1*S+2*K,x1*S+6*K,y2*S-2*K],fill=(120,84,52),outline=(40,26,16),width=_w(2))
        d.line([x1*S-6*K,(y1+y2)*S/2,x1*S+6*K,(y1+y2)*S/2],fill=(40,26,16),width=_w(1.5))
        d.ellipse([x1*S-2*K,y2*S-9*K,x1*S+2*K,y2*S-5*K],fill=(210,170,70))
    if secret:
        d.line([x1*S,y1*S,x2*S,y2*S],fill=col,width=_w(3))

def hearth(d,x,y,w,h,gold=False):
    rect(d,x,y,x+w,y+h,(58,50,48),(15,12,10),3)
    rect(d,x+.2,y+.2,x+w-.2,y+h-.2,(12,8,8))
    cx,cy=(x+w/2)*S,(y+h/2)*S
    for i,(rr,c) in enumerate(((.28,(150,60,20)),(.18,(230,130,40)),(.09,(255,210,110)))):
        e=rr*S*max(w,h)*1.6; d.ellipse([cx-e,cy-e,cx+e,cy+e],fill=c)
    if gold: d.rectangle([x*S+4*K,y*S+4*K,(x+w)*S-4*K,(y+h)*S-4*K],outline=(210,170,70),width=_w(2))

def stairs(d,x1,y1,x2,y2,horiz=True,label=None,dm=False):
    rect(d,x1,y1,x2,y2,(128,112,92),(30,24,20),2)
    if horiz:
        n=int((y2-y1)*3)
        for i in range(1,n):
            yy=(y1+i/3)*S; d.line([x1*S,yy,x2*S,yy],fill=(60,50,42),width=_w(2)); d.line([x1*S,yy+_w(2),x2*S,yy+_w(2)],fill=(160,142,118),width=1)
    else:
        n=int((x2-x1)*3)
        for i in range(1,n):
            xx=(x1+i/3)*S; d.line([xx,y1*S,xx,y2*S],fill=(60,50,42),width=_w(2)); d.line([xx+_w(2),y1*S,xx+_w(2),y2*S],fill=(160,142,118),width=1)

def label(d,txt,x,y,sz=17,col=(235,225,200)):
    f=font(sz)
    for dx,dy in ((-1,0),(1,0),(0,1),(0,-1),(1,1),(-1,-1)):
        d.text((x*S+dx*K,y*S+dy*K),txt,font=f,fill=(10,8,8),anchor="mm")
    d.text((x*S,y*S),txt,font=f,fill=col,anchor="mm")

def hazard(d,x,y,txt):
    r=13*K
    d.ellipse([x*S-r,y*S-r,x*S+r,y*S+r],fill=(170,36,36),outline=(255,220,200),width=_w(2))
    d.text((x*S,y*S),txt,font=font(13,FS),fill=(255,255,255),anchor="mm")

def grid(d):
    for i in range(W+1):
        d.line([i*S,0,i*S,H*S],fill=(170,170,170,) if i%5==0 else (112,112,112),width=1)
    for j in range(H+1):
        d.line([0,j*S,W*S,j*S],fill=(170,170,170) if j%5==0 else (112,112,112),width=1)

def ball(d,cx,cy,r,fill):
    d.ellipse([(cx-r)*S+3*K,(cy-r)*S+4*K,(cx+r)*S+3*K,(cy+r)*S+4*K],fill=(10,8,8))  # shadow
    d.ellipse([(cx-r)*S,(cy-r)*S,(cx+r)*S,(cy+r)*S],fill=fill,outline=(15,10,10),width=_w(2))
    hl=tuple(min(255,c+50) for c in fill[:3])
    d.ellipse([(cx-r*.5)*S,(cy-r*.6)*S,(cx-r*.05)*S,(cy-r*.15)*S],fill=hl)


def statue(d,cx,cy,facing,pose=0):
    """Top-down stone statue on a square plinth. facing=(dx,dy) direction it looks."""
    im=d._image; L=int(2.2*S); c=L//2
    lay=Image.new("RGBA",(L,L),(0,0,0,0)); g=ImageDraw.Draw(lay)
    # plinth (not rotated look: drawn then rotated with the layer, fine)
    p=int(.58*S)
    g.rectangle([c-p,c-p,c+p,c+p],fill=(96,98,104,255),outline=(30,30,36,255),width=_w(2))
    g.rectangle([c-p+4*K,c-p+4*K,c+p-4*K,c+p-4*K],outline=(138,140,148,255),width=_w(1.5))
    stone=(176,178,184,255); dark=(112,114,122,255); hi=(214,216,222,255)
    # shoulders / torso (wide ellipse), arms by pose, head, hair
    g.ellipse([c-.46*S,c-.2*S,c+.46*S,c+.24*S],fill=stone,outline=dark,width=_w(2))
    arms={0:((-.5,-.05,-.2,-.5),(.5,-.05,.2,-.5)),   # both hands raised forward
          1:((-.52,.1,-.3,-.42),(.5,-.1,.5,.32)),    # one raised, one at side
          2:((-.5,-.1,-.5,.32),(.5,-.1,.5,.32)),     # arms at sides
          3:((-.46,0,-.1,-.5),(.46,0,.46,-.1))}[pose%4]
    for (x1,y1,x2,y2) in arms:
        g.line([c+x1*S,c+y1*S,c+x2*S,c+y2*S],fill=stone,width=_w(11))
        g.ellipse([c+x2*S-6*K,c+y2*S-6*K,c+x2*S+6*K,c+y2*S+6*K],fill=hi)
    g.ellipse([c-.2*S,c-.2*S,c+.2*S,c+.2*S],fill=hi,outline=dark,width=_w(2))     # head
    g.pieslice([c-.2*S,c-.2*S,c+.2*S,c+.2*S],200,340,fill=dark)                    # hair at the back
    g.polygon([(c-3*K,c-.2*S+2*K),(c+3*K,c-.2*S+2*K),(c,c-.2*S-5*K)],fill=hi)       # nose
    ang=math.degrees(math.atan2(-facing[0],-facing[1]))
    lay=lay.rotate(ang,resample=Image.BICUBIC)
    sh=Image.new('RGBA',lay.size,(0,0,0,0)); ImageDraw.Draw(sh).rectangle([c-p+6*K,c-p+8*K,c+p+6*K,c+p+8*K],fill=(0,0,0,150)); sh=sh.rotate(ang,resample=Image.BICUBIC,center=(c-6*K,c-8*K)) if False else sh
    im.paste(sh,(int(cx*S-c),int(cy*S-c)),sh)
    im.paste(lay,(int(cx*S-c),int(cy*S-c)),lay)

def furn(d,x1,y1,x2,y2,fill=(60,40,28)):
    d.rectangle([x1*S+4*K,y1*S+5*K,x2*S+4*K,y2*S+5*K],fill=(8,6,6))  # drop shadow
    rect(d,x1,y1,x2,y2,fill,(20,14,10),2)
    d.line([x1*S+2*K,y1*S+2*K,x2*S-2*K,y1*S+2*K],fill=tuple(min(255,c+40) for c in fill),width=_w(2))
    d.line([x1*S+2*K,y1*S+2*K,x1*S+2*K,y2*S-2*K],fill=tuple(min(255,c+25) for c in fill),width=_w(2))

def finish(im,glows,dm):
    """Light pools from hearths, grain noise, vignette."""
    w,h=im.size
    a=np.asarray(im.convert("RGB")).astype(np.float32)
    rng=np.random.default_rng(7)
    a+=rng.normal(0,3.2,a.shape[:2])[:,:,None]            # film grain
    yy,xx=np.mgrid[0:h,0:w].astype(np.float32)
    light=np.zeros((h,w),np.float32)
    for gx,gy in glows:
        dist=np.hypot(xx-gx*S,yy-gy*S)/(S*7.5)
        light+=np.clip(1-dist,0,1)**2
    light=np.clip(light,0,1)
    warm=np.stack([light*34,light*17,light*2],-1)
    a=a+warm                                               # warm pools
    vig=np.hypot((xx-w/2)/(w/2),(yy-h/2)/(h/2))
    a*= (1-0.28*np.clip(vig-.55,0,1)**1.4*1.6)[:,:,None]   # vignette
    return Image.fromarray(np.clip(a,0,255).astype(np.uint8))

# ----------------- GROUND -----------------
def ground(dm):
    im=Image.new("RGB",(W*S,H*S),OUT); d=ImageDraw.Draw(im)
    rooms={"Kitchen":(2,2,12,14),"Dining Room":(12,2,28,14),"Study":(28,2,38,14),
     "Servant's Passage":(2,14,6,24),"Cloakroom":(6,14,14,24),"Entry Hall":(14,14,26,24),"Drawing Room":(26,14,38,24)}
    for n,r in rooms.items():
        if n in ("Kitchen","Dining Room"):
            rect(d,r[0],r[1],r[2],r[3],(30,32,44))
            for hx in range(int(r[0]*S),int(r[2]*S),24): d.line([hx,r[1]*S,hx+(r[3]-r[1])*S,r[3]*S],fill=(44,46,60),width=2)
        else: floor(d,r,"wood")
    # rugs
    rect(d,16,16,22,22,(112,38,44),(48,16,20),3); rect(d,16.35,16.35,21.65,21.65,None,(212,170,90),2); rect(d,16.6,16.6,21.4,21.4,None,(70,24,30),1)
    for i in range(6):
        for j in range(6):
            if (i+j)%2==0: rect(d,17+i*.67-.2,17+j*.67-.2,17+i*.67+.2,17+j*.67+.2,(96,30,38))
    # study shelves
    for yy in (3,): furn(d,28.5,2.4,37.5,3.4,(60,38,24))
    furn(d,28.2,3.5,29.2,13,(60,38,24)); furn(d,34,7,36,9,(80,56,36))
    # drawing: statues, piano
    for i,(sx,sy) in enumerate(((29,16.5),(33,16),(36,19),(30,22),(34,22))): statue(d,sx,sy,(32.5-sx,19.5-sy),i)
    furn(d,31,18.5,34,20.5,(30,24,24))
    # entry
    ball(d,20,19,1.2,(200,170,80)) if dm else None
    # cloakroom racks
    furn(d,6.5,14.5,13.5,15.5,(70,50,40))
    # stairs
    stairs(d,22,15,26,23,horiz=True)  # grand stair up
    stairs(d,2,20,6,24,horiz=True)    # down
    # hearths
    hearth(d,14,21,1,2)           # entry
    hearth(d,37,7,1,2)            # study
    hearth(d,37,18,1,2)           # drawing
    doors=[(19,24,21,24),(19,14,21,14),(12,7,12,9),(28,7,28,9),(26,18,26,20),(14,18,14,20),(6,18,6,20),(3,14,5,14)]
    walls(d,list(rooms.values()),doors)
    # house outer weight
    d.rectangle([2*S,2*S,38*S,24*S],outline=WALL,width=int(10*K))
    if dm:
        grid(d)
        for n,r in rooms.items():
            if n in ("Kitchen","Dining Room"): continue
            oy={"Dining Room":-3.6,"Entry Hall":-3.6,"Drawing Room":-3.6,"Servant's Passage":-2.5,"Kitchen":-1.2}.get(n,0)
            label(d,n,(r[0]+r[2])/2-(2 if n=="Entry Hall" else 0),(r[1]+r[3])/2+oy,17 if n!="Servant's Passage" else 11)
        label(d,"UP",24,22.4,16); label(d,"DOWN",4,23.4,11); pass
        label(d,"THE McTAVERN",20,6.5,22,(230,200,120)); label(d,"separate scene: Dining Room + Kitchen",20,8,13,(200,200,220)); label(d,"(rooms need not line up; the house is a stage set)",20,9.2,11,(170,170,190))
        label(d,"front door (storm)",20,23.4,10,(200,200,230)); label(d,"chandelier",20,17.6,10,(30,20,10))
        # secret passages
        for pts in (((32,24),(32,25.1),(4,25.1),(4,24)),):
            d.line([P(*p) for p in pts],fill=(200,70,150),width=int(4*K))
            label(d,"S1 secret passage: Drawing Room <-> Servant's Passage",18,25.55,10,(230,120,190))
        hazards=[("G1",24,17),("G2",20,19),("G5",33,7),("G6",33,21.5),("G7",4,16),("G8",5,21)]
        for h in hazards: hazard(d,h[1],h[2],h[0])
        d.line([P(36,3),P(36.8,3.8)],fill=(200,70,150),width=int(4*K)); label(d,"S2",36,3.8,12,(230,120,190))
    else:
        pass
    return im

# ----------------- UPPER -----------------
def upper(dm):
    im=Image.new("RGB",(W*S,H*S),OUT); d=ImageDraw.Draw(im)
    rooms={"Trophy Room":(2,2,12,14),"Portrait Gallery":(12,2,28,8),"Upper Hall":(12,8,28,24),"Master Bedroom":(28,2,38,14),
      "Guest Room 1":(2,14,12,19),"Guest Room 2":(2,19,12,24),"Guest Room 3":(28,14,38,19),"Guest Room 4":(28,19,38,24)}
    for n,r in rooms.items(): floor(d,r,"wood")
    rect(d,13,10,27,14,(70,50,90),(40,28,60),3)
    # trophy cases
    for i in range(4):
        rect(d,3+i*2.3,3,4.7+i*2.3,4.2,(120,150,170),(30,40,50),2)
        rect(d,3+i*2.3,12,4.7+i*2.3,13.2,(120,150,170),(30,40,50),2)
    rect(d,3,6,5,10,(120,150,170),(30,40,50),2); rect(d,9,6,11,10,(120,150,170),(30,40,50),2)
    # gallery frames
    for i in range(7): rect(d,13.2+i*2.1,2.2,14.6+i*2.1,2.9,(160,120,60),(40,30,10),2)
    # master bed
    furn(d,33,3,37,7,(110,40,50)); furn(d,29,3,30.5,5,(60,40,30))
    for (bx,by) in ((3,15),(3,20),(30,15),(30,20)): furn(d,bx,by,bx+3,by+2,(100,80,90))
    stairs(d,22,15,26,23,horiz=True)
    hearth(d,6,2,2,1); hearth(d,19,2,2,1); hearth(d,37,7,1,2)
    doors=[(19,8,21,8),(12,9,12,11),(12,16,12,18),(12,21,12,23),(28,16,28,18),(28,21,28,23)]
    master=[(28,9,28,11)]
    walls(d,list(rooms.values()),doors+master)
    d.rectangle([2*S,2*S,38*S,24*S],outline=WALL,width=int(10*K))
    if dm:
        grid(d)
        for n,r in rooms.items():
            label(d,n,(r[0]+r[2])/2,(r[1]+r[3])/2+(3 if n=="Upper Hall" else 0),16 if "Guest" not in n else 13)
        label(d,"DOWN",24,19,16)
        label(d,"locked (key: Ashford)",28.1,10,10,(255,200,120))
        d.line([P(36,3),P(36.8,3.8)],fill=(200,70,150),width=int(4*K)); label(d,"S2 secret passage to Study",33.4,10.5,11,(230,120,190))
        for h in [("U1",7,5.5),("U2",25,5),("U3",8,12.5),("U4",20,14)]: hazard(d,h[1],h[2],h[0])
    return im

# ----------------- CELLAR -----------------
def cellar(dm):
    im=Image.new("RGB",(W*S,H*S),OUT); d=ImageDraw.Draw(im)
    rooms={"Wine Cellar":(2,2,14,24),"Furnace Room":(14,2,26,12),"Pantry":(14,12,26,24),"Hidden Chamber":(26,2,36,10)}
    for n,r in rooms.items():
        if n=="Hidden Chamber" and not dm: continue
        floor(d,r,"stone")
    # wine racks
    for i in range(3):
        furn(d,3,6+i*5,5,9+i*5,(70,40,30)); furn(d,11,6+i*5,13,9+i*5,(70,40,30))
    # tier steps (elevation) in wine cellar: lower middle section
    rect(d,5,12.5,11,16,(60,62,70),(25,25,30),2)
    # pantry hanging figures
    for (fx,fy) in ((17,15),(20,14),(23,15),(18,19),(22,20),(24,17)): ball(d,fx,fy,.5,(190,190,200)); d.line([P(fx,fy-.5),P(fx,fy-1.5)],fill=(40,40,40),width=2)
    # boiler pit + catwalk
    rect(d,18,5,24,10,(35,18,16),(10,6,6),3); 
    rect(d,17,4,25,5,(120,100,60),(40,30,15),2); rect(d,17,10,25,11,(120,100,60),(40,30,15),2)
    rect(d,17,4,18,11,(120,100,60),(40,30,15),2)  # catwalk west
    ball(d,21,7.5,1.2,(200,70,30))
    rect(d,19,2,23,3,(140,140,150),(30,30,35),2)  # damper panel
    stairs(d,2,20,6,24,horiz=True); stairs(d,2,3,5,6,horiz=False)
    doors=[(14,6,14,8),(14,16,14,18),(19,12,21,12)]
    sec=[(26,5,26,7)]
    walls(d,[r for n,r in rooms.items() if n!="Hidden Chamber" or dm],doors,sec,show_secret=dm)
    if not dm:
        # secret door looks like wall
        pass
    d.rectangle([2*S,2*S,26*S,24*S],outline=WALL,width=int(10*K))
    if dm:
        grid(d)
        for n,r in rooms.items(): label(d,n,(r[0]+r[2])/2,(r[1]+r[3])/2+(4 if n=="Wine Cellar" else 0),16)
        label(d,"UP to Servant's Passage",4,19,10); label(d,"UP to Kitchen (S3)",3.5,6.7,10)
        label(d,"damper panel",21,2.5,10,(30,30,30))
        label(d,"boiler pit",21,7.5,12,(255,220,170))
        label(d,"sunken (steps)",8,14.2,11)
        label(d,"secret door",26,4.5,10,(230,120,190))
        for h in [("C1",8,13),("C2",4,17),("C3",20,21),("C4",21,4.5),("C5",17,9),("C6",33,8)]: hazard(d,h[1],h[2],h[0])
    return im

if __name__=="__main__":
    import sys
    OUTD=sys.argv[1] if len(sys.argv)>1 else "."
    GLOW={"Ground":[(14.6,22),(37.4,8),(37.4,19)],"Upper":[(7,2.6),(20,2.6),(37.4,8)],"Cellar":[(21,7.5)]}
    for name,fn in (("Ground",ground),("Upper",upper),("Cellar",cellar)):
        for dm,tag in ((True,"DM"),(False,"Players")):
            im=finish(fn(dm),GLOW[name],dm)
            im.save(f"{OUTD}/Session1_{name}_{tag}.png",optimize=True)
    print("ok")
