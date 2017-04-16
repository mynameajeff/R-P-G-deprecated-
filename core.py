import pygame, time, random
from pygame import gfxdraw
from pygame.locals import *

show = True
playG = True
tileWid=15
tileHei=15

mapno = 0
mapbool = True

gmoscr = False

def bch(bcc):
    global BATTLE_CH
    BATTLE_CH = random.randint(bcc,20)
bch(1)
randenem = random.randint(0,3)

info_text = [
"This is a little project made with pygame, trying to be a Roguelike.",
"Coded entirely by mynameajeff."
]

#~~~~~~~~~~~~~~ Map Load ~~~~~~~~~~~~~~
tileWid=15
tileHei=15
def mP(file): #MapParse
    global nl
    count3=0
    lvl,nl = [],[]
    for line in iter(open("level/"+file+'.lvl')):
        lvl.append(line.split(" "))
        count3+=1
    for count2 in range(count3):
        try: nl+= lvl[count2]
        except: pass
        count2+=1
        try: nl.remove("\n")
        except:pass
def mR(mapPosX,mapPosY,tch): #MapRender
    x2 = 0
    y = 25
    counter = 0
    for x in range(len(nl)):
        if nl[counter] == "1":
            cR(x2+mapPosX,y+mapPosY,tileWid+tch,tileHei,(100,100,100))
        elif nl[counter] == "2":
            cR(x2+mapPosX,y+mapPosY,tileWid+tch,tileHei,(100,0,0))
        elif nl[counter] == "3":
            cR(x2+mapPosX,y+mapPosY,tileWid+tch,tileHei,(0,0,100))
        elif nl[counter] == "4":
            cR(x2+mapPosX,y+mapPosY,tileWid+tch,tileHei,(0,100,0))
        elif nl[counter] == "5":
            cR(x2+mapPosX,y+mapPosY,tileWid+tch,tileHei,(120,120,255))
        elif nl[counter] == "-": #BlackBox
            cR(x2+mapPosX,y+mapPosY,tileWid+tch,tileHei,(0,0,0))
        elif nl[counter] == "+": #NextLine
            x2=-tileWid
            y+=tileHei
        x2+=tch
        x2+=tileWid
        counter+=1
        if counter > len(nl):
            break
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
class button:
    def __init__(self,text,posX,posY,WidX,HeiY,innerColour,outerColour):
        self.text = text
        self.posX = posX
        self.posY = posY
        self.WidX = WidX
        self.HeiY = HeiY
        self.ic = innerColour
        self.oc = outerColour

    def Draw(self,textsize,textX,textY,size,checkBool,ic2,oc2):
        if checkBool == True:
            self.ic = ic2
            self.oc = oc2

        cR(self.posX,self.posY,self.WidX,self.HeiY,(self.ic,self.ic,self.ic))
        cR(self.posX+size,self.posY+size,self.WidX-(size*2),self.HeiY-(size*2),(self.oc,self.oc,self.oc))
        cT(self.text,textX,textY,"munro", textsize, (100,100,100))

    def Collision(self,x,y,fCall,*args):
        if self.posX+self.WidX > x > self.posX:
            if self.posY+self.HeiY > y > self.posY: fCall(*args)

#~~~~~~~~~~~~~~ Items Handler Sys ~~~~~~~~~~~~~~
class Item:
    def __init__(self):
        self.iWid = tileWid #itemWid
        self.iHei = tileHei #itemHei
        self.it1 = 1
        self.it2 = 1
        self.d2 = []
        self.d=[]
        self.x2z=0

    def drawcall(self,iX2,iY2,typebl): #largo
        iX = (15 * iX2)-5;iY = (15 * iY2)+10

        if self.it2 == self.it1 and typebl == 1: cR(iX,iY,self.iWid,self.iHei,(0,0,255))
        elif self.it2 == self.it1 and typebl == 2: cR(iX,iY,self.iWid,self.iHei,(0,100,255))
        else: del iX2,iY2#iX2 = None;iY2 = None
        try:
            if char.cX+(char.csize/15) > iX2 >= char.cX:
                if char.cY+(char.csize/15) > iY2 >= char.cY:
                    if typebl==1: self.drawcallext1()
                    else: self.drawcallext2()
                    self.it2+=1
                    
        except: pass

    def drawcallext1(self):
        char.csize+=15
        print("mcdonalds collected")
        
    def drawcallext2(self):
        if char.hp >= (char.hpmax-40): char.hp = char.hpmax
        else: char.hp+=40
        print("health collected")

    def randomitem(self,itemamount):
        for x in range(itemamount):
            self.d.append(random.randint(15,42))#n1 x 15 42
            self.d.append(random.randint(1,30))#n2 y 1 30
            self.d.append(random.randint(1,2))
            self.d2.append(Item())
            self.x2z+=3

itemclass = Item()

def r(Run):
    itemclass.randomitem(10)
    x3s=0
    for x in range(Run):
        itemclass.d2[x].drawcall(itemclass.d[x3s],itemclass.d[x3s+1],itemclass.d[x3s+2])
        x3s+=3
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~~~~~~~~~~~~~~ Char  Handler Sys ~~~~~~~~~~~~~~
class Player:
    def __init__(self,colour):
        self.hpmax = 100
        self.hp = 100 #health
        self.csize = 15 #size of character
        self.lvl = 1 #current level
        self.lvlN = 25 #xp for next level
        self.xp = 0 #experience points
        self.dmgM = 1 #damage multiplier
        self.c = colour #colour of the character

        self.cX = 17 #char.cX 255
        self.cY = 6 #char.cY 90

    def Calc(self):
        while self.xp >= self.lvlN:
            print("Level Up!")
            self.lvl += 1
            self.xp -= self.lvlN
            self.lvlN = round(self.lvlN * 1.5)
            self.hp = round(self.hp * 1.75)
            self.hpmax = round(self.hpmax * 1.75)
            self.dmgM *= 2

    def HP(self,hpX,hpY,enemi):
        xrloop = 0
        cR(hpX,hpY,75,10,(255,0,0))
        cT(str(self.hp-enemi.totalDmgDealt),hpX+79,hpY-2,"freesans",11,(0,0,0))
        for x in range(self.hp-enemi.totalDmgDealt):
            cR(hpX+xrloop,hpY,75/self.hpmax,10,(0,255,0))
            xrloop+=75/self.hpmax
    def HPch(self,enemi):
        global gmoscr
        self.hp-=enemi.totalDmgDealt
        if self.xp < 0: char.xp = 0
        if self.hp < 1: 
            time.sleep(0.1)
            gmoscr = True
        return self.hp

    def drawcall(self):
        cX = (15 * self.cX)-5;cY = (15 * self.cY)+10
        cR(cX,cY,self.csize,self.csize,self.c)
        
char = Player((120,240,68))
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~~~~~~~~~~~~~~ Enemy Handler Sys ~~~~~~~~~~~~~~
class Enemy:
    totalDmgTaken = 0 #to the enemy
    totalDmgDealt = 0
    def __init__(self, strength, xpout, gearband, lutband, enemC, textMov, HPmax, width):
        self.xpout = xpout
        self.str = strength
        self.pX = 250
        self.pY = 180
        self.gb = gearband
        self.lb = lutband
        self.enemC = enemC
        self.textMov = textMov
        self.HPmax = HPmax
        self.w = width
    def EnemInfo(self,name): #250,180
        cR(self.pX,self.pY,80,195,self.enemC) #ENEM 80
        cT(name,265-self.textMov,140,"munro",20,(200,200,200))

    def HP(self): #The enemies health bar.
        xrloop = 0
        cR(self.pX-1,self.pY-20,81,10,(255,0,0))
        cT(str(self.HPmax-self.totalDmgTaken),self.pX+84,self.pY-22,"freesans",11,(0,0,0))
        for x in range(self.HPmax-self.totalDmgTaken):
            cR(self.pX+xrloop,self.pY-20,80/self.HPmax,10,(0,255,0))
            xrloop+=80/self.HPmax

    def HPch(self,enem,enemi):
        global battle,rnem
        # hpcurrent - random number [0 to yourDamage(with chance of crit)]
        self.totalDmgTaken+= (100*char.dmgM)
        if self.totalDmgTaken >= self.HPmax:
            cR(0,0,Swidth,Sheight,(0,0,0))
            char.xp+= self.xpout
            char.Calc()
            try:print("\nYou Win! You killed the",enem.split("an ")[1])
            except:print("\nYou Win! You killed the",enem.split("a ")[1])
            rnem = True
            bch(1)
            mP("btl")
            char.HPch(enemi)
            Enems()
            battle = False

    def HPch2(self,enem,enemi):
        global battle,rnem

        cR(0,0,Swidth,Sheight,(0,0,0))
        print("you pussied out of the fight.")
        rnem = True
        bch(1)
        mP("btl")
        char.HPch(enemi)
        Enems()
        battle = False

    def AI(self,enem,enemi):
        global battle,rnem
        attackpwr = random.randint(0,self.str)

        if self.totalDmgTaken < self.HPmax:
            if attackpwr == 0:
                try:print("The",enem.split("an ")[1],"missed when attacking you!")
                except:print("The",enem.split("a ")[1],"missed when attacking you!")

            else:
                self.totalDmgDealt +=(3*attackpwr)
                try:print("The",enem.split("an ")[1],"has attacked you for",(3*attackpwr),"damage!")
                except:print("The",enem.split("a ")[1],"has attacked you for",(3*attackpwr),"damage!")

                if self.totalDmgDealt >= char.hp:
                    cR(0,0,Swidth,Sheight,(0,0,0))
                    try:print("The",enem.split("an ")[1],"has defeated you!")
                    except:print("The",enem.split("a ")[1],"has defeated you!")
                    rnem = True
                    bch(0)
                    mP("btl")
                    char.HPch(enemi)
                    Enems()
                    battle = False
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def Enems():
    global Imp,Orc,Gremlin,Goblin,ObjEList
    Imp = Enemy(2,10,"Destitute Gear","Destitute Loot",(25,120,25),0,500,80)
    Orc = Enemy(5,25,"Poor Gear","Destitute Loot",(85,120,25),0,800,80)
    Gremlin = Enemy(8,35,"Poor Gear","Poor Loot",(45,120,55),14,1200,80)
    Goblin = Enemy(12,22,"Decent Gear","Poor Loot",(65,120,65),10,1400,80)
    
    Gremloblin = Enemy(15,64,"Hard Scales","Decent Loot",(125,120,125),25,3000,80)
    ObjEList = [Imp,Orc,Gremlin,Goblin]


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#Basic Draw Functions(Calls)

def cR(x, y, width, height, color): #colorRect
    pygame.draw.rect(screen, color, (x,y,width,height))

def cB(x, y, radius, color): #colorBall
    pygame.gfxdraw.filled_circle(screen,x,y,radius-1,color)
    pygame.gfxdraw.aacircle(screen,x,y,radius-1,color)

def cT(text, x, y, font, fsize, color): #colorText
    myfont = pygame.font.Font("fonts/"+font+".ttf", fsize)
    msg = myfont.render(text, 1, color)
    screen.blit(msg, (x,y))
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#Situation DrawSpace Func Callers
EnemL = ["an Imp","an Orc","a Gremlin","a Goblin"]
boolist = [False] * 4 #bt0,bt1,bt2,bt3
descrip = ["weak but can be strong in numbers.",
    "the imp's tougher brother.",
    "not as weak as you may think.",
    "the toughest normal enemy in the first area."]

def gameover():
    cR(0,0,Swidth,Sheight,(0,0,0))
    cT("GAME OVER",(Swidth/2)-120,(Sheight/2)-40,"freesans",40,(255,255,255))

lmbtimer = 0
xoffset = 0

def BATTLE_draw(x,y,lmb):
    global randenem,mapbool,boolist,ObjEList,lmbtimer,output
    def DH_inner(c,boolist,tl,lmb):
        global lmbtimer
        BTLbtn.Draw(40,tl[loop],tl[loop+4],5,True,135,115)
        if lmb and lmbtimer <= 0:
            lmbtimer +=0.2
            for cloop in range(4):
                if c == cloop: boolist[cloop] = True
    def BTNfunc(btnno,enem,enemi):
        global battle,rnem,playG,output,charac,xoffset
        if btnno ==0:
            for enemloop in range(4):
                if enem == EnemL[enemloop]:
                    print("you attacked",enem,"for",(100*char.dmgM),"damage!")
                    ObjEList[enemloop].HPch(enem,ObjEList[enemloop])
                    ObjEList[enemloop].AI(enem,ObjEList[enemloop])

        elif btnno ==1: print("to be coded!")
        elif btnno ==2:
            for enemloop in range(4): 
                if enem == EnemL[enemloop]:
                    print(enem+",",descrip[enemloop])
        elif btnno ==3:
            for enemloop in range(4):
                if enem == EnemL[enemloop]:
                    ObjEList[enemloop].HPch2(enem,ObjEList[enemloop])
    y1 = [25,80,135,190]
    tl = [30,30,52,52,28,82,138,193]

    divL5 = ["Attack","Defend","Info","Run"]
    cR(0,0,Swidth,20,(128,128,128)) #creates gray bar at top of canvas
    cR(0,20,Swidth,Sheight,(185,185,185)) #creates main draw space
    cR(0,20,180,Sheight,(70,70,70)) #Contains buttons
    cR(175,20,5,Sheight,(90,90,90)) #Divider

    if mapno == 1 and mapbool == False:
        mP("btl")
        Enems()
        mapbool = True

    mR(175,95,5)

    charac = cR(Swidth-180-xoffset,Sheight-180,75,75,char.c) #CHAR

    cT("Battle Mode!",Swidth/2-18,2,"freesans",12,(0,0,0))

    for loop in range(4):
        if randenem == loop: 
            ObjEList[loop].EnemInfo(EnemL[loop])
            ObjEList[loop].HP()
            char.HP(Swidth-180,Sheight-200,ObjEList[loop])
        BTLbtn = button(divL5[loop],7,y1[loop],160,50,155,135)
        BTLbtn.Draw(40,tl[loop],tl[loop+4],5,False,135,115)
        BTLbtn.Collision(x,y,DH_inner,loop,boolist,tl,lmb)
        if boolist[loop] == True: BTNfunc(loop,EnemL[randenem],ObjEList[loop])
        boolist[loop] = False
        if lmbtimer > 0: lmbtimer-=0.01
    #print(lmbtimer)

def draw(charhp,charcsize,charlvl,charlvlN,charxp,chardmgM):
    global tileWid,tileHei,show,playG,output
    cR(0,0,640,20,(128,128,128)) #creates gray bar at top of canvas
    cR(0,20,Swidth,Sheight,(185,185,185)) #creates main draw space
    mR(220,0,0)
    cR(0,20,220,Sheight,(70,70,70))
    cR(215,20,5,Sheight,(90,90,90))

    alist1 = ["Health","Char Size","Level","Next","XP","DMG*",
        charhp,charcsize,charlvl,charlvlN,charxp,chardmgM]
    avar1 = 50
    for x in range(6):
        cT(alist1[x]+": "+str(alist1[x+6]),20,avar1,"munro",30,(100,100,100))
        avar1+=30
    r(10)
    char.drawcall()

def INFO_draw(x,y,lmb):
    def INFO_f():
        btnInf.Draw(45,45,26,5,True,235,215)
        if lmb: bl2[1] = False

    cR(0,20,Swidth,Sheight,(185,185,185)) #creates main draw space
    cT(info_text[0],20,80,"freesans", 18, (100,100,100))
    cT(info_text[1],22,110,"freesans", 18, (100,100,100))

    btnInf = button("<==",20,25,Swidth/5,50,255,235)
    btnInf.Draw(45,45,26,5,False,235,215)
    btnInf.Collision(x,y,INFO_f)

bl2 = [False]*3#Start,Info,Exit

def TITLE_draw(x,y,lmb):
    def TH_inner(c,lmb):
        btn1.Draw(40,Swidth/3+itrMov[c],480/divL1[c],5,True,235,215)
        if lmb:
            if c ==0: bl2[0] = True
            elif c ==1: bl2[1] = True
            elif c ==2: bl2[2] = True;sys.exit()

    cR(0,0,640,20,(128,128,128)) #creates gray bar at top of canvas
    cR(0,20,Swidth,Sheight,(185,185,185)) #creates main draw space
    cT("RPG",Swidth/2-112,Sheight/6,"pxlvetica", 128, (100,100,100))

    BTN_names = ["Start","Info","Exit"]
    itrMov=[60,70,70]
    divL1 = [2,1.5,1.2]

    for loop in range(3):
        btn1 = button(BTN_names[loop],Swidth/3,Sheight/divL1[loop],Swidth/3,50,255,235)
        btn1.Draw(40,Swidth/3+itrMov[loop],480/divL1[loop],5,False,235,215)
        btn1.Collision(x,y,TH_inner,loop,lmb)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#Main Pygame Loop $#!@ (The boring/confusing stuff...)

def whichFunc(x,y,left):
    global mapno,mapbool,playG,rnem,randenem,battle

    if gmoscr == True:
        playG = True
        battle = False
        gameover()

    if BATTLE_CH == 0:
        if rnem == True: 
            randenem = random.randint(0,3)
            rnem = False
            battle = True
        elif rnem == False: pass
        playG = True
    if battle ==False and bl2[0] == True and gmoscr == False: 
        mapno = 0
        draw(char.hp,char.csize,char.lvl,char.lvlN,char.xp,char.dmgM)
    if battle ==True and bl2[0] ==True and gmoscr == False:
        mapno +=1
        playG = True #disables controls
        BATTLE_draw(x,y,left)
    else: playG = False

    if bl2[1] == True: INFO_draw(x,y,left)

    if bl2[0] == False and bl2[1] == False: TITLE_draw(x,y,left)

    if mapno == 0 and mapbool == True:
        mP("b")
        mapbool = False

def controls(x,y):
    csize2 = (char.csize/15)
    if event.key == pygame.K_UP:
        print("Y; U:",char.cY)
        if char.cY <= 1: char.cY=1
        else: char.cY-=1
        char.Calc()
        bch(0)

    elif event.key == pygame.K_DOWN:
        print("Y; D:",char.cY)
        if char.cY >=31-csize2: char.cY=31-csize2
        else: char.cY+=1
        char.Calc()
        bch(0)

    elif event.key == pygame.K_LEFT:
        print("X; L:",char.cX)
        if char.cX <= 15: char.cX=15
        else: char.cX-=1
        char.Calc()
        bch(0)

    elif event.key == pygame.K_RIGHT:
        print("X; R:",char.cX)
        if char.cX >=43-csize2: char.cX=43-csize2
        else: char.cX+=1
        char.Calc()
        bch(0)

Swidth,Sheight = 640,480

pygame.init()

screen = pygame.display.set_mode((Swidth,Sheight))
screen.set_alpha(None)
pygame.display.set_caption("RPG")
clock = pygame.time.Clock()
rnem = True
battle=False

while not bl2[2]:
    x,y = pygame.mouse.get_pos()
    left,m,right = pygame.mouse.get_pressed()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            bl2[2] = True
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == K_END:
                bl2[2] = True
                sys.exit()
            elif playG == False:
                controls(x,y)
    whichFunc(x,y,left)
    pygame.display.update()
    clock.tick(60)
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
