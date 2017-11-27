import pygame, Player, pickle
import Enemies
from Player import weapon as weap
from random import randint as rand
import random as rander
from pygame.locals import *


global lcash, cash, weapon

#Load save data if available
try:
    f = open("Save.pickle",'r')
    data = pickle.load(f)
    f.close()
    weapon, lcash, rank, level, headnum, purchases, dlvls, name = data
    data = None
except ValueError:
    print 'Updating Save, please wait'
    f = open("Save.pickle",'r')
    data = pickle.load(f)
    f.close()
    weapon = 0
    lcash = 0
    rank = 0
    level = 1
    cash = 0
    purchases = None
    dlvls = None
    headnum = 1
    name = 'Player'
except:
    weapon = 0
    lcash = 0
    rank = 0
    level = 1
    cash = 0
    purchases = None
    dlvls = None
    headnum = 1
    data = None
    name = 'Player'
    print 'A problem occurred, please try again'

#Initializing game
pygame.init()

cashico = pygame.image.load("Images/Cash.png")
cashico = pygame.transform.scale(cashico,(70,70))
cashrect = cashico.get_rect()
cashrect.left = 5
cashrect.top = 0

helptext = "After clicking 'Play' on the main menu, select the number of enemies you want to fight and the number of kills needed to win. " \
           "You can toggle headshots only, but this increases the difficulty so it is recommended that you leave this off if you are new. " \
           "To play, use WASD or the arrow keys to move, aim and shoot with the mouse, and throw grenades by pressing 'F' but be careful, you have a limited number of grenades. " \
           "Certain guns have different size clips, your ammo and grenades are displayed in the bottom right of the screen. A minimap also is displayed in the top right. " \
           "Be careful about staying in one spot for too long, the more you shoot, the more the enemies will be attracted to your location. Good Luck!"

width = 900
height = 600

bwidth = 1800
bheight = 1200

#colors
BLACK = (0,0,0)
WHITE = (255,255,255)
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)
YELLOW = (255,255,0)

screen = pygame.display.set_mode((width,height),pygame.FULLSCREEN)
background=pygame.Surface((bwidth,bheight))
background=background.convert()
background.fill(BLACK)
backimg1 = pygame.image.load("Images/skill-desc_0003_bg.png")
v = float(bwidth)/backimg1.get_width()
h = int(backimg1.get_height()*v)
backimg1 = pygame.transform.scale(backimg1,(bwidth, h))
backimg2 = pygame.transform.scale(pygame.image.load("Images/skill-desc_0002_far-buildings.png"), (bwidth/2, h/2))
backimg3 = pygame.transform.scale(pygame.image.load("Images/skill-desc_0001_buildings.png"), (bwidth/2, h/2))
backimg4 = pygame.transform.scale(pygame.image.load("Images/skill-desc_0000_foreground.png"), (bwidth/2, h/2))

backsurf = pygame.Surface((bwidth,bheight))
backsurf.blit(backimg1,(0,0))
backsurf.blit(backimg2,(0,h/2))
backsurf.blit(backimg3,(0,h/2))
backsurf.blit(backimg4,(0,h/2))
backsurf.blit(backimg2,(bwidth/2,h/2))
backsurf.blit(backimg3,(bwidth/2,h/2))
backsurf.blit(backimg4,(bwidth/2,h/2))


weapons = [weap("Semi-Auto",10,200,8, 0,8,"USP","Images/USP.png",1,5,0),weap("Semi-Auto",25,250,10,0,7,"Glock","Images/Glock.PNG",4,5,80),weap("Full-Auto",8,130,25,3,15,"M27","Images/Machine Gun.png",8,3,100),weap("Shotgun",10,85,5,6,15,"Sawed-Off Shotgun","Images/Sawed-Off.png",12,3,100),weap("Sniper",55,500,5,20,35,"Intervention","Images/Intervention.png",16,15,200)]

global player
player = Player.player(100, height - 200)

#resets variables
def reset():
    global player, cash, weapon, headnum, lcash
    if purchases:
        for i, x in enumerate(purchases):
            weapons[i].purchased = x
    else:
        weapons[0].purchased = True
    if weapons[weapon].purchased:
        player.weapon = weapons[weapon]
    else:
        player.weapon = weapons[0]
    player.rank = rank
    player.level = level
    player.headnum = headnum
    player.set_head()
    player.name = name
    if dlvls:
        for i, x in enumerate(dlvls):
            weapons[i].dlvl = x
            weapons[i].damage += weapons[i].dinc * (weapons[i].dlvl - 1)
    cash = lcash

reset()

#gameplay function
def main(enenum, reqkills, htvar, frenum=False, difficulty=0):
    global player, cash
    player.reset(50, bheight - 70)
    player.clip = player.weapon.magsize
    breakout = False
    clock = pygame.time.Clock()
    xscroll=0
    yscroll=0
    walls=Map1
    bullets = []
    friendlies = []
    enemies = []
    ennum = enenum
    reqkills = reqkills
    victory = False
    kvar = False

    EnNames = ["Cyborg","Deathstroke","Master","Dalek","Vashta Nerada","Davros","Strax","Captain Cold","Ra's Al Ghul","Doomsday","The Emperor", "Heat Wave"]
    FrNames = ["K-9", "Spartan","Vibe","Wild Dog","Black Canary","Firestorm","Constantine","Friendly1","Friendly2","Friendly3"]

    if not frenum:
        #Spawns enemies
        if ennum < len(spawnpoints):
            sps = rander.sample(range(0,len(spawnpoints)-1),ennum)
        else:
            sps = range(0,len(spawnpoints))
            n = ennum - len(spawnpoints)
            sps += rander.sample(range(0,len(spawnpoints)-1),n)

        for i in sps:
            sx,sy = spawnpoints[i]
            enemies.append(Enemies.Enemy(sx,sy,100+(25 * difficulty),htvar,[player],False,difficulty,EnNames.pop(rand(0,len(EnNames)-1))))

        while len(enemies)<ennum:
            sx, sy = spawnpoints[rand(0, len(spawnpoints) - 1)]
            enemies.append(Enemies.Enemy(sx, sy, 100+(25 * difficulty),htvar,[player],False,difficulty,EnNames.pop(rand(0,len(EnNames)-1))))

    else:
        for i in range(1,ennum + 1):
            enemies.append(Enemies.Enemy(bwidth - (50*i),bheight - 70,100+(25 * difficulty),htvar,[player],False,difficulty,EnNames.pop(rand(0,len(EnNames)-1))))
        for i in range(2,frenum + 2):
            friendlies.append(Enemies.Enemy(50 * i,bheight -70,100+(25 * difficulty),htvar,enemies,True,difficulty,FrNames.pop(rand(0,len(FrNames)-1))))
            for e in enemies:
                e.enemylist += friendlies

    #Main gameloop
    while True:
        clock.tick(20)
        x = backimg1.get_height()
        background.blit(backsurf,(0,bheight-x))
        for i in walls:
            i.draw()

        #Draws enemies and their bullets
        poplist = []
        for f in friendlies:
            bpoplist = []
            for b in f.bullets:
                for i in range(0, 10):
                    if i < 6:
                        show = False
                    else:
                        show = True
                    a = b.draw(background, RED, walls, enemies, show)
                    if a:
                        bpoplist.append(b)
                        b.draw(background, RED, walls, enemies, True)
                        break
            for i in bpoplist:
                f.bullets.remove(i)
            if f.alive:
                f.draw(background, walls, RED, xscroll, yscroll)
            elif not f.alive:
                f.deadtimer = f.deadtimer - 1
                f.rect.y -= 1
                background.blit(f.skullsurf, f.rect)
                if f.deadtimer <= 0:
                    f.alive = True
                    f.health = f.starthealth
                    sx, sy = spawnpoints[rand(0, len(spawnpoints) - 1)]
                    f.rect = pygame.Rect(sx, sy, 30, 50)
            if f.health <= 0:
                poplist.append(f)
        for i in poplist:
            if i.alive:
                i.alive = False
                i.deadtimer = 70

        poplist = []
        for e in enemies:
            bpoplist = []
            for b in e.bullets:
                for i in range(0,10):
                    if i<6:
                        show = False
                    else:
                        show = True
                    a = b.draw(background,WHITE,walls,friendlies + [player],show)
                    if a:
                        bpoplist.append(b)
                        b.draw(background,WHITE,walls,friendlies + [player],True)
                        break
            for i in bpoplist:
                e.bullets.remove(i)
            if e.alive:
                viewables = e.cview(walls)
                if viewables and player in viewables and player.zone:
                    for ee in enemies:
                        ee.targets[player.zone] += 2
                e.draw(background,walls,WHITE,xscroll,yscroll)
            elif not e.alive:
                e.deadtimer = e.deadtimer - 1
                e.rect.y -= 1
                background.blit(e.skullsurf, e.rect)
                if e.deadtimer <=0:
                    e.alive = True
                    e.health = e.starthealth
                    sx, sy = spawnpoints[rand(0, len(spawnpoints) - 1)]
                    e.rect = pygame.Rect(sx, sy, 30, 50)
            if e.health<=0:
                poplist.append(e)
        for i in poplist:
            if i.alive:
                i.deaths += 1
                i.alive = False
                i.deadtimer = 70

        b = player.draw(background, RED, walls, xscroll, yscroll, spawnpoints, enemies,screen)
        if b and player.alive:
            bullets += b
        elif b and not player.alive:
            if player.rect.centerx > width / 2:
                xscroll = player.rect.centerx - (width / 2)
                if player.rect.centerx > (bwidth - (width / 2)):
                    xscroll = bwidth - width
            else:
                xscroll = 0
            if player.rect.centery > height / 2:
                yscroll = player.rect.centery - (height / 2)
                if player.rect.centery > (bheight - height / 2):
                    yscroll = bheight - height
            player.alive = True
            player.invintime = 30

        if player.health <= 0 and player.alive:
            for e in enemies:
                for i in range(0,len(e.targets)):
                    e.targets[i] = 0
            player.deaths += 1
            player.alive = False
            player.deadtime = 50
            player.curstreak = 0

        poplist = []
        for b in bullets:
            for i in range(0,25):
                if i<20:
                    show = False
                else:
                    show = True
                a = b.draw(background,RED,walls,enemies,show, player, True)
                if a:
                    poplist.append(b)
                    b.draw(background,RED,walls,enemies,True, player, False)
                    break
        for i in poplist:
            bullets.remove(i)

        if player.rect.centerx > width/2:
            xscroll = player.rect.centerx - (width/2)
            if player.rect.centerx > (bwidth-(width/2)):
                xscroll = bwidth - width
        if player.rect.centery > height/2:
            yscroll = player.rect.centery - (height/2)
            if player.rect.centery > (bheight-height/2):
                yscroll = bheight-height

        screen.blit(background, (-1*xscroll, -1*yscroll))
        font = pygame.font.Font(None,30)
        kt = font.render("KILLS: " + str(player.kills), 1, RED)
        ktp = kt.get_rect()
        ktp.left = 15
        ktp.top = 15
        screen.blit(kt,ktp)
        dt = font.render("DEATHS: " + str(player.deaths), 1, WHITE)
        dtp = dt.get_rect()
        dtp.left = 14
        dtp.top = ktp.bottom + 5
        screen.blit(dt,dtp)
        kst = font.render("KILLSTREAK: " +str(player.curstreak),1,YELLOW)
        kstp = kst.get_rect()
        kstp.left = 15
        kstp.top = dtp.bottom + 5
        screen.blit(kst,kstp)
        if player.killstreak > player.curstreak:
            klt = font.render("BEST: " + str(player.killstreak),1,YELLOW)
            kltp = klt.get_rect()
            kltp.left = 15
            kltp.top = kstp.bottom
            screen.blit(klt,kltp)

        minimap = background.copy()
        minimap = pygame.transform.scale(minimap,(150,100))
        minimap.set_alpha(150)
        screen.blit(minimap,(width - minimap.get_width() - 10, 20))

        for i in range(0,player.weapon.magsize):
            ccolor = (255,255,255)
            if i >= player.clip:
                ccolor = (120,120,120)
            pygame.draw.rect(screen,ccolor,((900-(5*(i+1))),(600 - 15),4,10))

        for i in range(0,player.grenmax):
            ccolor = (0,150,0)
            if i>=player.grenum:
                ccolor = (120,120,120)
            pygame.draw.circle(screen,ccolor,(900-(15*(i+1)),600 - 25),7)

        key = pygame.key.get_pressed()
        if kvar and not key[K_ESCAPE] and not key[K_p]:
            kvar = False
        if not kvar and (key[K_p] or key[K_ESCAPE]):
            kvar = True
            cover = pygame.Surface((width,height))
            cover.fill(BLACK)
            cover.set_alpha(150)
            screen.blit(cover,(0,0))
            font = pygame.font.Font(None, 100)
            pt = font.render('PAUSED',1,RED)
            ptp = pt.get_rect()
            ptp.centerx = width/2
            ptp.centery = height/2
            font = pygame.font.Font(None,50)
            qt = font.render('QUIT',1,YELLOW)
            qtp = qt.get_rect()
            qtp.centerx = width/2
            qtp.top = ptp.bottom + 20
            screen.blit(pt,ptp)
            screen.blit(qt,qtp)
            pygame.display.flip()
            while True:
                key = pygame.key.get_pressed()
                if not kvar and (key[K_ESCAPE] or key[K_p]):
                    break
                if kvar and not key[K_ESCAPE] and not key[K_p]:
                    kvar = False
                a,b,c = pygame.mouse.get_pressed()
                if a:
                    if qtp.collidepoint(pygame.mouse.get_pos()):
                        breakout = True
                if breakout:
                    break

                for event in pygame.event.get():
                    if event.type == QUIT:
                        save()
                        pygame.display.quit()
                        quit()
            kvar = True

        redscore = 0
        redscore += player.kills
        for i in friendlies:
            redscore += i.kills
        whiscore = 0
        for e in enemies:
            whiscore += e.kills

        font = pygame.font.Font(None,50)
        rt = font.render("RED: " + str(redscore),1,(255,0,0))
        wt = font.render("WHITE: " + str(whiscore),1,(255,255,255))
        wtp = wt.get_rect()
        rtp = rt.get_rect()
        rtp.centerx = width / 2
        rtp.top = 15
        wtp.centerx = width * 3 / 4
        wtp.top = rtp.top
        screen.blit(rt,rtp)
        screen.blit(wt,wtp)
        pygame.display.flip()

        if redscore >= reqkills:
            victory = True
            breakout = True
        elif whiscore >= reqkills:
            victory = False
            breakout = True

        for event in pygame.event.get():
            if event.type == QUIT:
                save()
                breakout = True

        if breakout:
            break
    timer = 3000
    starttime = timer

    if victory:
        text = "VICTORY!"
        color = GREEN
        multip = 2
    else:
        text = "DEFEAT"
        color = YELLOW
        multip = 1
    if htvar:
        multip += 1
    multip += difficulty/2.0

    player.rank += player.kills * multip
    player.rank += player.killstreak * multip
    cash += player.kills * multip
    cash += player.killstreak * multip
    cash = int(cash)
    while player.rank > int(5 * (player.level ** 1.5)):
        if player.rank > int(5 * (player.level ** 1.5)):
            player.rank -= int(5 * (player.level ** 1.5))
            player.level += 1
    while timer>0:
        timer -=1
        screen.fill(BLACK)
        fadesurf = pygame.Surface((width,height))
        font = pygame.font.Font(None,150)

        got = font.render(text,1,color)
        gotr = got.get_rect()
        gotr.centerx = width/2
        gotr.centery = height/2
        font = pygame.font.Font(None,65)
        rt = font.render("RED: " + str(redscore),1,(255,0,0))
        wt = font.render("WHITE: " + str(whiscore),1,(255,255,255))
        wtp = wt.get_rect()
        rtp = rt.get_rect()
        rtp.centerx = width / 3
        rtp.centery = height / 4
        wtp.centerx = width * 2 / 3
        wtp.centery = rtp.centery
        fadesurf.blit(rt,rtp)
        fadesurf.blit(wt,wtp)
        fadesurf.blit(got,gotr)
        sfont = pygame.font.Font(None, 30)
        x = 1
        t = sfont.render(player.name, 1, RED)
        t2 = sfont.render("Kills: " + str(player.kills), 1, RED)
        t3 = sfont.render("Deaths: " + str(player.deaths), 1, RED)
        tp = t.get_rect()
        t2p = t2.get_rect()
        t3p = t3.get_rect()
        tp.left = 10
        tp.top = height * 2/3 + (20 * (x-2))
        t2p.left = width * 1/6
        t2p.top = tp.top
        t3p.left = width /3
        t3p.top = tp.top
        fadesurf.blit(t,tp)
        fadesurf.blit(t2,t2p)
        fadesurf.blit(t3,t3p)

        if type(frenum) == int:
            x = 2
            for f in friendlies:
                t = sfont. render(f.name,1,RED)
                t2 = sfont.render("Kills: " + str(f.kills),1,RED)
                t3 = sfont.render("Deaths: " + str(f.deaths),1,RED)
                tp = t.get_rect()
                t2p = t2.get_rect()
                t3p = t3.get_rect()
                tp.left = 10
                tp.top = height * 2/3 + (20 * (x-2))
                t2p.left = width * 1/6
                t2p.top = tp.top
                t3p.left = width /3
                t3p.top = tp.top
                fadesurf.blit(t,tp)
                fadesurf.blit(t2,t2p)
                fadesurf.blit(t3,t3p)
                if f.Class == 0:
                    img = pygame.transform.scale(pygame.image.load("Images/USP.png"), (18, 18))
                    fadesurf.blit(img, (t3p.right + 3, t3p.top))
                elif f.Class == 1:
                    img = pygame.transform.scale(pygame.image.load("Images/Machine Gun.png"), (30, 16))
                    fadesurf.blit(img, (t3p.right + 3, t3p.top))
                elif f.Class == 2:
                    img = pygame.transform.scale(pygame.image.load("Images/Sawed-Off.png"), (30, 16))
                    fadesurf.blit(img, (t3p.right + 3, t3p.top))
                elif f.Class == 3:
                    img = pygame.transform.scale(pygame.image.load("Images/Intervention.png"), (30, 16))
                    fadesurf.blit(img, (t3p.right + 3, t3p.top))
                x += 1
        x = 1
        for f in enemies:
            t = sfont.render(f.name,1,WHITE)
            t2 = sfont.render("Kills: " + str(f.kills),1,WHITE)
            t3 = sfont.render("Deaths: " + str(f.deaths),1,WHITE)
            tp = t.get_rect()
            t2p = t2.get_rect()
            t3p = t3.get_rect()
            tp.left = width/2
            tp.top = height * 2/3 + (20 * (x-2))
            t2p.left = width * 2/3
            t2p.top = tp.top
            t3p.left = width *5/6
            t3p.top = tp.top
            fadesurf.blit(t,tp)
            fadesurf.blit(t2,t2p)
            fadesurf.blit(t3,t3p)
            if f.Class == 0:
                img = pygame.transform.scale(pygame.image.load("Images/USP.png"),(18,18))
                fadesurf.blit(img,(t3p.right + 3,t3p.top))
            elif f.Class == 1:
                img = pygame.transform.scale(pygame.image.load("Images/Machine Gun.png"),(30,16))
                fadesurf.blit(img,(t3p.right+3,t3p.top))
            elif f.Class == 2:
                img = pygame.transform.scale(pygame.image.load("Images/Sawed-Off.png"),(30,16))
                fadesurf.blit(img,(t3p.right+3,t3p.top))
            elif f.Class == 3:
                img = pygame.transform.scale(pygame.image.load("Images/Intervention.png"),(30,16))
                fadesurf.blit(img,(t3p.right+3,t3p.top))
            x += 1

        fadesurf.set_alpha(timer*15)
        screen.blit(fadesurf,(0,0))
        pygame.display.flip()
        a,b,c = pygame.mouse.get_pressed()
        if a and timer < starttime -100:
            break
        for event in pygame.event.get():
            if event.type == QUIT:
                save()
                pygame.display.quit()
                quit()

class wall():
    def __init__(self, x, y, width, height, color=(150,150,150)):
        self.rect = pygame.Rect(x, y, width, height)
        self.rect.left = x
        self.rect.top = bheight-y
        self.color = color

    def draw(self):
        pygame.draw.rect(background,self.color,self.rect)

Map1 = [wall(0,20,bwidth,20),wall(0,bheight,20,bheight),wall(0,bheight,bwidth,20),wall(bwidth-20,bheight,20,bheight),wall(300,140,300,30),wall(900,140,300,30),wall(1500,140,300,30),wall(0,260,300,30),wall(600,260,300,30),wall(1200,260,300,30),wall(885,260,30,150),wall(1185,260,30,290),wall(1000,360,100,100),wall(800,480,500,30),wall(1035,bheight,30,750),wall(600,610,20,260),wall(520,360,180,20),wall(520,610,180,20),wall(1480,610,20,260),wall(1400,360,180,20),wall(1400,610,180,20),wall(1580,480,220,30),wall(300,480,220,30)]
spawnpoints = [(390,670),(900,670),(900,1130),(1030,1010),(1030,790),(1170,670),(1650,670),(1630,1010),(1340,1130),(430,1130)]

def Menu():
    try:
        bfont = pygame.font.SysFont('silom',65)
        cfont = pygame.font.SysFont('georgia', 40)
        lfont = pygame.font.SysFont('arialblack', 70)
    except:
        bfont = pygame.font.Font(None, 65)
        cfont = pygame.blit.font.Font(None, 50)
        lfont = pygame.font.Font(None, 80)
    breakout = False
    cvar = False
    global player
    while True:
        screen.fill((60,0,0))
        screen.blit(cashico,cashrect)
        ct = cfont.render(str(cash),1,(0,180,0))
        ctp = ct.get_rect()
        ctp.centery = cashrect.centery
        ctp.left = cashrect.right
        screen.blit(ct,ctp)
        rt = lfont.render("LEVEL " + str(player.level),1,(0,255,0))
        rtp = rt.get_rect()
        rtp.centerx = width/2
        rtp.top = 0
        screen.blit(rt,rtp)
        pygame.draw.rect(screen,(100,100,100),(width/2 - 100, rtp.bottom, 200, 10))
        if player.rank:
            pygame.draw.rect(screen,(0,255,0),(width/2 - 100,rtp.bottom, (200*player.rank)/(5*(player.level**1.5)),10))
        pt = bfont.render("PLAY",1,(255,255,0))
        ptp = pt.get_rect()
        ptp.centerx = width/2
        ptp.centery = height*2/7
        st = bfont.render("SHOP",1,(255,255,0))
        stp = st.get_rect()
        stp.centerx = width/2
        stp.centery = height *3/7
        cut = bfont.render('CUSTOMIZE',1,(255,255,0))
        cutp = cut.get_rect()
        cutp.centerx = width/2
        cutp.centery = height *4/7
        ht = bfont.render("HELP",1,(255,255,0))
        htp = ht.get_rect()
        htp.centerx = width/2
        htp.centery = height * 5/7
        qt = bfont.render('QUIT',1,(255,255,0))
        qtp = qt.get_rect()
        qtp.centerx = width/2
        qtp.centery = height * 6 / 7
        pos = pygame.mouse.get_pos()
        if ptp.collidepoint(pos):
            pygame.draw.rect(screen,BLUE,ptp)
            a,b,c = pygame.mouse.get_pressed()
            if a and cvar:
                cvar = False
                Setup()
        if stp.collidepoint(pos):
            pygame.draw.rect(screen,BLUE,stp)
            a,b,c = pygame.mouse.get_pressed()
            if a and cvar:
                cvar = False
                Shop()
        if cutp.collidepoint(pos):
            pygame.draw.rect(screen,BLUE,cutp)
            a,b,c = pygame.mouse.get_pressed()
            if a and cvar:
                cvar = False
                Customize()
        if htp.collidepoint(pos):
            pygame.draw.rect(screen,BLUE,htp)
            a,b,c = pygame.mouse.get_pressed()
            if a and cvar:
                cvar = False
                Help()
        if qtp.collidepoint(pos):
            pygame.draw.rect(screen,BLUE,qtp)
            a,b,c = pygame.mouse.get_pressed()
            if a and cvar:
                save()
                pygame.display.quit()
                quit()

        a,b,c = pygame.mouse.get_pressed()
        if not a and not cvar:
            cvar = True

        screen.blit(pt,ptp)
        screen.blit(st,stp)
        screen.blit(cut,cutp)
        screen.blit(ht,htp)
        screen.blit(qt,qtp)
        r = pygame.Rect(10,200,300,500)
        font = pygame.font.Font(None,30)
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == QUIT:
                save()
                breakout = True

        if breakout:
            break

def drawText(surface, text, color, rect, font, aa=False, bkg=None):
    rect = Rect(rect)
    y = rect.top
    lineSpacing = -2

    # get the height of the font
    fontHeight = font.size("Tg")[1]

    while text:
        i = 1

        # determine if the row of text will be outside our area
        if y + fontHeight > rect.bottom:
            break

        # determine maximum width of line
        while font.size(text[:i])[0] < rect.width and i < len(text):
            i += 1

        # if we've wrapped the text, then adjust the wrap to the last word
        if i < len(text):
            i = text.rfind(" ", 0, i) + 1

        # render the line and blit it to the surface
        if bkg:
            image = font.render(text[:i], 1, color, bkg)
            image.set_colorkey(bkg)
        else:
            image = font.render(text[:i], aa, color)

        surface.blit(image, (rect.left, y))
        y += fontHeight + lineSpacing

        # remove the text we just blitted
        text = text[i:]

    return text

def Customize():
    global player
    breakout = False
    lfont = pygame.font.Font(None, 15)
    n = 4
    cvar = False
    while True:
        screen.fill((0,0,0))
        v = 1
        p = 1
        h =20
        w = width / (n + 1)
        iw = w * 5 / 6
        while True:
            a,b,c = pygame.mouse.get_pressed()
            if not a and not cvar:
                cvar = True
            try:
                if p > n:
                    p -= n
                    h += w
                img = pygame.image.load("Images/front" + str(v) + ".png")
                img = pygame.transform.scale(img, (iw,iw))
                rect = img.get_rect()
                rect.left = int((p-.5)*w)
                rect.top = h
                pos = pygame.mouse.get_pos()
                if player.level >= (v-1)*2:
                    if rect.collidepoint(pos):
                        pygame.draw.rect(screen,(255,255,255),rect, 10)
                        a,b,c = pygame.mouse.get_pressed()
                        if a and player.headnum != v and cvar:
                            cvar = False
                            player.headnum = v
                            player.set_head()
                    if v == player.headnum:
                        pygame.draw.rect(screen, (0,255,0),rect, 10)
                    screen.blit(img, rect)
                else:
                    screen.blit(img, rect)
                    lock = pygame.image.load("Images/Lock.png")
                    lock = pygame.transform.scale(lock,(rect.width,rect.height))
                    screen.blit(lock,rect)
                    lt = lfont.render("LEVEL " + str((v-1)*2),1,(255,0,0))
                    ltp = lt.get_rect()
                    ltp.centerx = rect.centerx
                    ltp.top = rect.bottom + 3
                    screen.blit(lt,ltp)

            except:
                break
            v += 1
            p += 1
        font = pygame.font.Font(None, 40)
        nbt = font.render('Nickname: ',1,WHITE)
        nt = font.render(player.name,1,WHITE)
        rt = font.render("AAAAAAAAAA",1,WHITE)
        rect = rt.get_rect()
        rect.bottom = height - 10
        rect.centerx = width/2
        nbtp = nbt.get_rect()
        nbtp.right = rect.left
        nbtp.bottom = height -10
        screen.blit(nbt,nbtp)
        pygame.draw.rect(screen,YELLOW,rect,2)
        screen.blit(nt,(rect.left + 4,rect.top + 2))

        bt = font.render("BACK",1,BLACK,WHITE)
        btp = bt.get_rect()
        btp.right = width -15
        btp.bottom = height - 15
        screen.blit(bt, btp)
        a,b,c = pygame.mouse.get_pressed()
        if btp.collidepoint(pygame.mouse.get_pos()) and a:
            if player.name == '':
                player.name = 'Player'
            break
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == QUIT:
                breakout = True
            if event.type == KEYDOWN:
                ret = ''
                if event.key == K_a:
                    ret = 'a'
                if event.key == K_b:
                    ret = 'b'
                if event.key == K_c:
                    ret = 'c'
                if event.key == K_d:
                    ret = 'd'
                if event.key == K_e:
                    ret = 'e'
                if event.key == K_f:
                    ret = 'f'
                if event.key == K_g:
                    ret = 'g'
                if event.key == K_h:
                    ret = 'h'
                if event.key == K_i:
                    ret = 'i'
                if event.key == K_j:
                    ret = 'j'
                if event.key == K_k:
                    ret = 'k'
                if event.key == K_l:
                    ret = 'l'
                if event.key == K_m:
                    ret = 'm'
                if event.key == K_n:
                    ret = 'n'
                if event.key == K_o:
                    ret = 'o'
                if event.key == K_p:
                    ret = 'p'
                if event.key == K_q:
                    ret = 'q'
                if event.key == K_r:
                    ret = 'r'
                if event.key == K_s:
                    ret = 's'
                if event.key == K_t:
                    ret = 't'
                if event.key == K_u:
                    ret = 'u'
                if event.key == K_v:
                    ret = 'v'
                if event.key == K_w:
                    ret = 'w'
                if event.key == K_x:
                    ret = 'x'
                if event.key == K_y:
                    ret = 'y'
                if event.key == K_z:
                    ret = 'z'
                if event.key == K_BACKSPACE:
                    player.name = player.name[0:len(ret)-1]
                #keys = pygame.key.get_pressed()
                if pygame.key.get_mods() & pygame.KMOD_SHIFT:
                    ret = ret.upper()
                if len(player.name)<10:
                    player.name += ret
        if breakout:
            break

def Help():
    breakout = False
    screen.fill((255,255,255))
    font = pygame.font.Font(None,50)
    rect = pygame.Rect(30,30,width-60,height - 100)
    drawText(screen,helptext,(0,0,0),rect,font)
    pygame.display.flip()
    rt = font.render("Click anywhere to return to the menu",1,(0,0,0))
    fadesurf = pygame.Surface((rt.get_width(),rt.get_height()))
    fadesurf.fill((255,255,255))
    rect = rt.get_rect()
    rect.centerx = width/2
    rect.bottom = height - 15
    cvar = False
    alpha = 255
    v = -3
    while True:
        alpha += v
        if alpha <0:
            alpha = 0
            v *= -1
        if alpha >255:
            alpha = 255
            v *= -1
        fadesurf.set_alpha(alpha)
        screen.blit(rt,rect)
        screen.blit(fadesurf,rect)
        a,b,c = pygame.mouse.get_pressed()
        if a and cvar:
            breakout = True
        if not a and not cvar:
            cvar = True
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == QUIT:
                breakout = True
        if breakout:
            break

def Setup():
    breakout = False
    enemies = 2
    friendlies = 0
    kills = 10
    cvar = True
    htvar = False
    deathmatch = False
    difficulty = 0
    difficulties = [["very easy",(0,255,0)],["easy",(0,175,0)],["normal",(200,200,0)],["hard",(175,0,0)],["insane",(255,0,0)]]
    while True:
        a,b,c = pygame.mouse.get_pressed()
        if not a:
            cvar = False
        screen.fill((0,0,0))
        font = pygame.font.Font(None,150)
        gst = font.render("GAME SETUP",1,GREEN)
        gstp = gst.get_rect()
        gstp.centerx = width/2
        gstp.top = 30
        screen.blit(gst, gstp)
        font = pygame.font.Font(None,50)
        ent = font.render('ENEMIES: ' + str(enemies),1,YELLOW)
        entp = ent.get_rect()
        entp.left = 40
        entp.centery = 200
        screen.blit(ent,entp)
        plt = font.render('+',1,GREEN)
        pltp = plt.get_rect()
        pltp.left = entp.right + 10
        pltp.centery = entp.centery
        mt = font.render('-',1,GREEN)
        mtp = mt.get_rect()
        mtp.left = pltp.right + 5
        mtp.centery = pltp.centery
        screen.blit(plt,pltp)
        screen.blit(mt,mtp)
        if deathmatch:
            fnt = font.render('Friendlies: ' + str(friendlies),1,YELLOW)
            fntp = fnt.get_rect()
            fntp.left = (width/2) + 40
            fntp.centery = 200
            screen.blit(fnt,fntp)
            plt = font.render('+',1,GREEN)
            pltp3 = plt.get_rect()
            pltp3.left = fntp.right + 10
            pltp3.centery = fntp.centery
            mt = font.render('-',1,GREEN)
            mtp3 = mt.get_rect()
            mtp3.left = pltp3.right + 5
            mtp3.centery = pltp3.centery
            screen.blit(plt,pltp3)
            screen.blit(mt,mtp3)
        kt = font.render("KILLS TO WIN: " + str(kills),1, YELLOW)
        ktp = kt.get_rect()
        ktp.left = 40
        ktp.top = entp.bottom +10
        pltp2 = plt.get_rect()
        pltp2.centery = ktp.centery
        pltp2.left = ktp.right + 10
        mtp2 = mt.get_rect()
        mtp2.centery = ktp.centery
        mtp2.left = pltp2.right + 5
        screen.blit(kt,ktp)
        screen.blit(mt,mtp2)
        screen.blit(plt,pltp2)

        ht = font.render("Headshot Damage Only",1,YELLOW)
        htp = ht.get_rect()
        htp.left = 40
        htp.top = ktp.bottom + 10
        t = "Off"
        if htvar:
            t = "On"
        htt = font.render(t,1,BLACK,WHITE)
        http = htt.get_rect()
        http.left = htp.right + 10
        http.centery=htp.centery
        screen.blit(ht,htp)
        screen.blit(htt,http)

        dt = font.render("Team Deathmatch",1,YELLOW)
        dtp = ht.get_rect()
        dtp.left = 40
        dtp.top = htp.bottom + 10
        t = "Off"
        if deathmatch:
            t = "On"
        dtt = font.render(t,1,BLACK,WHITE)
        dttp = dtt.get_rect()
        dttp.left = dtp.right + 10
        dttp.centery=dtp.centery
        screen.blit(dt,dtp)
        screen.blit(dtt,dttp)

        dift = font.render("Difficulty",1,YELLOW)
        diftp = dift.get_rect()
        diftp.left = 40
        diftp.top = dtp.bottom + 10
        left = font.render("<",1,WHITE)
        leftp = left.get_rect()
        leftp.left = diftp.right +15
        leftp.centery = diftp.centery
        difft = font.render(difficulties[difficulty][0],1,difficulties[difficulty][1])
        difftp = difft.get_rect()
        difftp.left = leftp.right
        difftp.centery = leftp.centery
        right = font.render(">",1,WHITE)
        rightp = right.get_rect()
        rightp.left = difftp.right
        rightp.centery = difftp.centery
        screen.blit(dift,diftp)
        screen.blit(left,leftp)
        screen.blit(difft,difftp)
        screen.blit(right,rightp)

        if leftp.collidepoint(pygame.mouse.get_pos()):
            a,b,c = pygame.mouse.get_pressed()
            if a and not cvar:
                cvar = True
                difficulty -= 1
                if difficulty < 0:
                    difficulty = len(difficulties)-1
        if rightp.collidepoint(pygame.mouse.get_pos()):
            a,b,c = pygame.mouse.get_pressed()
            if a and not cvar:
                cvar = True
                difficulty += 1
                if difficulty > len(difficulties)-1:
                    difficulty = 0
        if pltp.collidepoint(pygame.mouse.get_pos()):
            a,b,c = pygame.mouse.get_pressed()
            if a and not cvar:
                enemies +=1
                if enemies > 10:
                    enemies = 10
                cvar = True
        if mtp.collidepoint(pygame.mouse.get_pos()):
            a,b,c = pygame.mouse.get_pressed()
            if a and not cvar:
                enemies -= 1
                cvar = True
                if enemies <1:
                    enemies = 1
        if pltp2.collidepoint(pygame.mouse.get_pos()):
            a,b,c = pygame.mouse.get_pressed()
            if a and not cvar:
                kills += 5
                if kills > 100:
                    kills = 100
                cvar = True
        if mtp2.collidepoint(pygame.mouse.get_pos()):
            a,b,c = pygame.mouse.get_pressed()
            if a and not cvar:
                kills -= 5
                cvar = True
                if kills <5:
                    kills = 5
        if deathmatch and pltp3.collidepoint(pygame.mouse.get_pos()):
            a,b,c = pygame.mouse.get_pressed()
            if a and not cvar:
                cvar = True
                friendlies += 1
                if friendlies > 10:
                    friendlies = 10
        if deathmatch and mtp3.collidepoint(pygame.mouse.get_pos()):
            a,b,c = pygame.mouse.get_pressed()
            if a and not cvar:
                cvar = True
                friendlies -= 1
                if friendlies < 0:
                    friendlies = 0
        if http.collidepoint(pygame.mouse.get_pos()):
            a,b,c = pygame.mouse.get_pressed()
            if a and not cvar:
                htvar = not htvar
                cvar = True
        if dttp.collidepoint(pygame.mouse.get_pos()):
            a,b,c = pygame.mouse.get_pressed()
            if a and not cvar:
                cvar = True
                deathmatch = not deathmatch

        pt = font.render('PLAY',1,YELLOW)
        ptp = pt.get_rect()
        ptp.right = width - 20
        ptp.bottom = height - 20
        if ptp.collidepoint(pygame.mouse.get_pos()):
            pygame.draw.rect(screen,BLUE,ptp)
            a,b,c=pygame.mouse.get_pressed()
            if a:
                if not deathmatch:
                    friendlies = False
                main(enemies, kills, htvar,friendlies,difficulty)
                breakout = True
        screen.blit(pt,ptp)

        bt = font.render('BACK',1,BLACK,WHITE)
        btp = bt.get_rect()
        btp.left = 20
        btp.bottom = height - 20
        if btp.collidepoint(pygame.mouse.get_pos()):
            a,b,c=pygame.mouse.get_pressed()
            if a:
                breakout = True
        screen.blit(bt,btp)

        if breakout:
            break
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == QUIT:
                save()
                pygame.display.quit()
                quit()

def Shop():
    global player, cash
    breakout = False
    while True:
        screen.fill((100,100,100))
        screen.blit(cashico,cashrect)
        try:
            cfont = pygame.font.SysFont(None, 50)
        except:
            cfont = pygame.font.Font(None,50)
        ct = cfont.render(str(cash),1,(0,180,0))
        ctp = ct.get_rect()
        ctp.centery = cashrect.centery
        ctp.left = cashrect.right
        screen.blit(ct,ctp)
        lt = cfont.render("LEVEL " + str(player.level),1,(0,180,0))
        ltp = lt.get_rect()
        ltp.centery = ctp.centery
        ltp.right = width-10
        screen.blit(lt,ltp)
        font = pygame.font.Font(None, 90)
        st = font.render("SHOP",1,GREEN)
        stp = st.get_rect()
        stp.centerx = width/2
        stp.centery = 50
        y = 100
        for i in weapons:
            y, cash = i.shopdraw(screen,y,width,height,player,cash)
        font = pygame.font.Font(None, 40)
        bt = font.render("BACK",1,BLACK,WHITE)
        btp = bt.get_rect()
        btp.right = width -15
        btp.bottom = height - 15
        screen.blit(st,stp)
        screen.blit(bt,btp)
        pygame.display.flip()

        a,b,c = pygame.mouse.get_pressed()
        if a:
            if btp.collidepoint(pygame.mouse.get_pos()):
                breakout = True
        if breakout:
            break
        for event in pygame.event.get():
            if event.type == QUIT:
                save()
                pygame.display.quit()
                quit()

def save(data = []):
    global player,weapon,xp,cash
    weapon = weapons.index(player.weapon)
    purchases = []
    dlvls = []
    for i in weapons:
        purchases.append(i.purchased)
        dlvls.append(i.dlvl)
    f = open("Save.pickle",'w')
    datlist = [weapon,cash,player.rank,player.level, player.headnum,purchases,dlvls,player.name]
    if data:
        for i,x in enumerate(data):
            try:
                datlist[i] = x
            except:
                pass
    pickle.dump(datlist,f)
    f.close()
if data:
    save(data)
    f = open("Save.pickle",'r')
    data = pickle.load(f)
    f.close()
    weapon, lcash, rank, level, headnum, purchases, dlvls, name = data
    data = None
    reset()

Menu()
pygame.display.quit()
