from PIL import Image, ImageDraw, ImageFont
import math, random
S=32; W,H=40,26
F="/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
FS="/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
def font(sz,f=F): return ImageFont.truetype(f,sz)
WOOD=(92,66,44); WOOD2=(78,55,36); STONE=(64,66,74); STONE2=(54,56,64)
OUT=(22,26,38); WALL=(18,12,10); DOOR=(150,104,52)
def P(x,y): return (x*S,y*S)

def rect(d,x1,y1,x2,y2,fill,outline=None,w=1):
    d.rectangle([x1*S,y1*S,x2*S,y2*S],fill=fill,outline=outline,width=w)

def floor(d,r,kind):
    x1,y1,x2,y2=r
    base=WOOD if kind=="wood" else STONE
    alt=WOOD2 if kind=="wood" else STONE2
    rect(d,x1,y1,x2,y2,base)
    rnd=random.Random(int(x1*7+y1*13))
    if kind=="wood":
        for yy in range(int(y1*2),int(y2*2)):
            d.line([x1*S,yy*S/2,x2*S,yy*S/2],fill=alt,width=1)
        for yy in range(int(y1*2),int(y2*2)):
            xx=x1*S+rnd.randint(10,90)
            while xx<x2*S:
                d.line([xx,yy*S/2,xx,yy*S/2+S/2],fill=alt,width=1); xx+=rnd.randint(60,140)
    else:
        for xx in range(int(x1),int(x2)):
            for yy in range(int(y1),int(y2)):
                if (xx+yy)%2==0: rect(d,xx,yy,xx+1,yy+1,alt)
                if rnd.random()<.15: d.ellipse([xx*S+8,yy*S+8,xx*S+16,yy*S+14],fill=(60,62,68))

def walls(d,rooms,doors,secret=None,show_secret=False):
    for r in rooms: d.rectangle([r[0]*S,r[1]*S,r[2]*S,r[3]*S],outline=WALL,width=7)
    for dr in doors: door(d,dr)
    if show_secret and secret:
        for dr in secret: door(d,dr,secret=True)

def door(d,dr,secret=False):
    x1,y1,x2,y2=dr[:4]
    col=(150,60,120) if secret else DOOR
    horiz = (y1==y2)
    if horiz:
        d.line([x1*S+2,y1*S,x2*S-2,y1*S],fill=(112,80,55),width=11)
        d.rectangle([x1*S+2,y1*S-4,x2*S-2,y1*S+4],outline=col,width=2)
    else:
        d.line([x1*S,y1*S+2,x1*S,y2*S-2],fill=(112,80,55),width=11)
        d.rectangle([x1*S-4,y1*S+2,x1*S+4,y2*S-2],outline=col,width=2)
    if secret:
        d.line([x1*S,y1*S,x2*S,y2*S],fill=col,width=3)

def hearth(d,x,y,w,h,gold=False):
    rect(d,x,y,x+w,y+h,(40,34,32),(15,12,10),3)
    rect(d,x+.25,y+.25,x+w-.25,y+h-.25,(18,14,14))
    if gold: d.rectangle([x*S+4,y*S+4,(x+w)*S-4,(y+h)*S-4],outline=(210,170,70),width=2)

def stairs(d,x1,y1,x2,y2,horiz=True,label=None,dm=False):
    n=int((x2-x1)*2 if not horiz else (y2-y1)*2)
    rect(d,x1,y1,x2,y2,(120,105,85),(30,24,20),2)
    if horiz:
        for i in range(1,int((y2-y1)*2)): d.line([x1*S,(y1+i/2)*S,x2*S,(y1+i/2)*S],fill=(70,60,50),width=2)
    else:
        for i in range(1,int((x2-x1)*2)): d.line([(x1+i/2)*S,y1*S,(x1+i/2)*S,y2*S],fill=(70,60,50),width=2)

def label(d,txt,x,y,sz=17,col=(235,225,200)):
    f=font(sz)
    for dx,dy in ((-1,0),(1,0),(0,1),(0,-1)):
        d.text((x*S+dx,y*S+dy),txt,font=f,fill=(10,8,8),anchor="mm")
    d.text((x*S,y*S),txt,font=f,fill=col,anchor="mm")

def hazard(d,x,y,txt):
    r=13
    d.ellipse([x*S-r,y*S-r,x*S+r,y*S+r],fill=(170,36,36),outline=(255,220,200),width=2)
    d.text((x*S,y*S),txt,font=font(13,FS),fill=(255,255,255),anchor="mm")

def grid(d):
    for i in range(W+1):
        d.line([i*S,0,i*S,H*S],fill=(170,170,170) if i%5==0 else (112,112,112),width=1)
    for j in range(H+1):
        d.line([0,j*S,W*S,j*S],fill=(170,170,170) if j%5==0 else (112,112,112),width=1)

def ball(d,cx,cy,r,fill):
    d.ellipse([(cx-r)*S,(cy-r)*S,(cx+r)*S,(cy+r)*S],fill=fill,outline=(15,10,10),width=2)

def furn(d,x1,y1,x2,y2,fill=(60,40,28)):
    rect(d,x1,y1,x2,y2,fill,(20,14,10),2)

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
    rect(d,16,16,22,22,(110,40,44),(60,20,24),3)
    # study shelves
    for yy in (3,): furn(d,28.5,2.4,37.5,3.4,(60,38,24))
    furn(d,28.2,3.5,29.2,13,(60,38,24)); furn(d,34,7,36,9,(80,56,36))
    # drawing: statues, piano
    for (sx,sy) in ((29,16.5),(33,16),(36,19),(30,22),(34,22)): ball(d,sx,sy,.55,(170,170,175))
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
    d.rectangle([2*S,2*S,38*S,24*S],outline=WALL,width=10)
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
            d.line([P(*p) for p in pts],fill=(200,70,150),width=4)
            label(d,"S1 secret passage: Drawing Room <-> Servant's Passage",18,25.55,10,(230,120,190))
        hazards=[("G1",24,17),("G2",20,19),("G5",33,7),("G6",33,21.5),("G7",4,16),("G8",5,21)]
        for h in hazards: hazard(d,h[1],h[2],h[0])
        d.line([P(36,3),P(36.8,3.8)],fill=(200,70,150),width=4); label(d,"S2",36,3.8,12,(230,120,190))
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
    d.rectangle([2*S,2*S,38*S,24*S],outline=WALL,width=10)
    if dm:
        grid(d)
        for n,r in rooms.items():
            label(d,n,(r[0]+r[2])/2,(r[1]+r[3])/2+(3 if n=="Upper Hall" else 0),16 if "Guest" not in n else 13)
        label(d,"DOWN",24,19,16)
        label(d,"locked (key: Ashford)",28.1,10,10,(255,200,120))
        d.line([P(36,3),P(36.8,3.8)],fill=(200,70,150),width=4); label(d,"S2 secret passage to Study",33.4,10.5,11,(230,120,190))
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
    d.rectangle([2*S,2*S,26*S,24*S],outline=WALL,width=10)
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

for name,fn in (("Ground",ground),("Upper",upper),("Cellar",cellar)):
    fn(True).save(f"maps/Session1_{name}_DM.png")
    fn(False).save(f"maps/Session1_{name}_Players.png")
print("ok")
