import pygame, Player, Enemies, pickle
from Player import weapon as weap
from random import randint as rand
import random as rander
from pygame.locals import *


global xp, cash, weapon
try:
    f = open("Save.pickle",'r')
    data = pickle.load(f)
    f.close()
    weapon, cash, rank, level, purchases, dlvls = data
except:
    print 'No readable save'
    weapon = 0
    cash = 0
    rank = 0
    level = 1
    cash = 0
    purchases = None
    dlvls = None

pygame.init()

cashico = pygame.image.load("Cash.png")
cashico = pygame.transform.scale(cashico,(70,70))
cashrect = cashico.get_rect()
cashrect.left = 5
cashrect.top = 0

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

screen = pygame.display.set_mode((width,height))
background=pygame.Surface((bwidth,bheight))
background=background.convert()
background.fill(BLACK)

weapons = [weap("Semi-Auto",15,200,8, 0,8,"USP","USP.png",1,5,0),weap("Full-Auto",8,130,25,3,15,"M27","Machine Gun.png",5,3,80),weap("Shotgun",10,85,5,6,15,"Sawed-Off Shotgun","Sawed-Off.png",10,2,100),weap("Sniper",55,500,5,20,35,"Intervention","Intervention.png",15,15,200)]
if purchases:
    for i,x in enumerate(purchases):
        weapons[i].purchased = x
else:
    weapons[0].purchased = True

if dlvls:
    for i,x in enumerate(dlvls):
        weapons[i].dlvl = x
        weapons[i].damage += weapons[i].dinc * (weapons[i].dlvl - 1)

global player
player = Player.player(100, height - 200)
if weapons[weapon].purchased:
    player.weapon = weapons[weapon]
else:
    player.weapon = weapons[0]
player.rank = rank
player.level = level

def main(enenum, reqkills):
    global player, xp, cash
    player.reset(100, height - 200)
    player.clip = player.weapon.magsize
    breakout = False
    clock = pygame.time.Clock()
    xscroll=0
    yscroll=0
    walls=Map1
    bullets = []
    enemies = []
    ennum = enenum
    reqkills = reqkills
    victory = False
    kvar = False
    if ennum < len(spawnpoints):
        sps = rander.sample(range(0,len(spawnpoints)-1),ennum)
    else:
        sps = range(0,len(spawnpoints))
        n = ennum - len(spawnpoints)
        sps += rander.sample(range(0,len(spawnpoints)-1),n)

    for i in sps:
        sx,sy = spawnpoints[i]
        enemies.append(Enemies.Enemy(sx,sy,100))

    while len(enemies)<ennum:
        sx, sy = spawnpoints[rand(0, len(spawnpoints) - 1)]
        enemies.append(Enemies.Enemy(sx, sy, 100))
    while True:
        k = pygame.key.get_pressed()
        if k[K_g]:
            print player.zone, player.awareness

        clock.tick(100)
        background.fill(BLACK)
        for i in walls:
            i.draw()

        poplist = []
        for e in enemies:
            bpoplist = []
            for b in e.bullets:
                for i in range(0,10):
                    if i<6:
                        show = False
                    else:
                        show = True
                    a = b.draw(background,WHITE,walls,player,show)
                    if a:
                        bpoplist.append(b)
                        b.draw(background,WHITE,walls,player,True)
                        break
            for i in bpoplist:
                e.bullets.remove(i)
            if e.alive:
                if e.cview(player,walls) and player.zone:
                    for ee in enemies:
                        ee.targets[player.zone] += 2
                e.draw(background,walls,WHITE,player,xscroll,yscroll)
            elif not e.alive:
                e.deadtimer = e.deadtimer - 1
                e.rect.y -= 1
                background.blit(e.skullsurf, e.rect)
                if e.deadtimer <=0:
                    e.alive = True
                    e.health = 100
                    sx, sy = spawnpoints[rand(0, len(spawnpoints) - 1)]
                    e.rect = pygame.Rect(sx, sy, 30, 50)
            if e.health<=0:
                poplist.append(e)
        for i in poplist:
            if i.alive:
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
        kst = font.render("KILLSTREAK: " +str(player.killstreak),1,YELLOW)
        kstp = kst.get_rect()
        kstp.left = 15
        kstp.top = dtp.bottom + 5
        screen.blit(kst,kstp)

        minimap = background.copy()
        minimap = pygame.transform.scale(minimap,(150,100))
        minimap.set_alpha(150)
        screen.blit(minimap,(width - minimap.get_width() - 10, 20))

        for i in range(0,player.weapon.magsize):
            ccolor = (255,255,255)
            if i >= player.clip:
                ccolor = (120,120,120)
            pygame.draw.rect(screen,ccolor,((900-(15*(i+1))),(600 - 30),8,20))

        pygame.display.flip()

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
            screen.blit(pt,ptp)
            pygame.display.flip()
            while True:
                key = pygame.key.get_pressed()
                if not kvar and (key[K_ESCAPE] or key[K_p]):
                    break
                if kvar and not key[K_ESCAPE] and not key[K_p]:
                    kvar = False
                for event in pygame.event.get():
                    if event.type == QUIT:
                        save()
                        pygame.display.quit()
                        quit()
            kvar = True

        if player.kills >= reqkills:
            victory = True
            breakout = True
        elif player.deaths >= reqkills:
            victory = False
            breakout = True

        for event in pygame.event.get():
            if event.type == QUIT:
                save()
                breakout = True

        if breakout:
            break
    timer = 80
    nxp = player.kills
    if victory:
        text = "VICTORY!"
        color = GREEN
        multip = 2
    else:
        text = "DEFEAT"
        color = YELLOW
        multip = 1

    player.rank += player.kills * multip
    player.rank += player.killstreak * multip
    cash += player.kills * multip
    cash += player.killstreak * multip
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
        kt = font.render("KILLS: " + str(player.kills), 1, RED)
        ktp = kt.get_rect()
        ktp.centerx = width/2
        ktp.centery = height*3/5 + 10
        dt = font.render("DEATHS: " + str(player.deaths),1, WHITE)
        dtp = dt.get_rect()
        dtp.centerx = width/2
        dtp.top = ktp.bottom + 10
        fadesurf.blit(kt,ktp)
        fadesurf.blit(dt,dtp)
        fadesurf.blit(got,gotr)
        fadesurf.set_alpha(timer*20)
        screen.blit(fadesurf,(0,0))
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == QUIT:
                save()
                pygame.display.quit()
                quit()

class wall():
    def __init__(self, x, y, width, height, color=GREEN):
        self.rect = pygame.Rect(x, y, width, height)
        self.rect.left = x
        self.rect.top = bheight-y
        self.color = color

    def draw(self):
        pygame.draw.rect(background,self.color,self.rect)

Map1 = [wall(0,20,bwidth,20),wall(0,bheight,20,bheight),wall(0,bheight,bwidth,20),wall(bwidth-20,bheight,20,bheight),wall(300,140,300,30),wall(900,140,300,30),wall(1500,140,300,30),wall(0,260,300,30),wall(600,260,300,30),wall(1200,260,300,30),wall(885,260,30,150),wall(1185,260,30,290),wall(1000,360,100,100,BLUE),wall(800,480,500,30),wall(1035,bheight,30,750),wall(600,610,20,260),wall(520,360,180,20),wall(520,610,180,20),wall(1480,610,20,260),wall(1400,360,180,20),wall(1400,610,180,20),wall(1580,480,220,30),wall(300,480,220,30)]
spawnpoints = [(390,670),(900,670),(900,1130),(1030,1010),(1030,790),(1170,670),(1650,670),(1630,1010),(1340,1130),(430,1130)]

def Menu():
    try:
        bfont = pygame.font.SysFont('silom',80)
        cfont = pygame.font.SysFont('georgia', 40)
        lfont = pygame.font.SysFont('arialblack', 70)
    except:
        bfont = pygame.font.Font(None, 80)
        cfont = pygame.font.Font(None, 50)
        lfont = pygame.font.Font(None, 80)
    breakout = False
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
        ptp.centery = height/3
        st = bfont.render("SHOP",1,(255,255,0))
        stp = st.get_rect()
        stp.centerx = width/2
        stp.centery = height *2/3
        pos = pygame.mouse.get_pos()
        if ptp.collidepoint(pos):
            pygame.draw.rect(screen,BLUE,ptp)
            a,b,c = pygame.mouse.get_pressed()
            if a:
                Setup()
        if stp.collidepoint(pos):
            pygame.draw.rect(screen,BLUE,stp)
            a,b,c = pygame.mouse.get_pressed()
            if a:
                Shop()
        screen.blit(pt,ptp)
        screen.blit(st,stp)
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == QUIT:
                save()
                breakout = True

        if breakout:
            break

def Setup():
    breakout = False
    enemies = 2
    kills = 10
    cvar = True
    while True:
        a,b,c = pygame.mouse.get_pressed()
        if not a:
            cvar = False
        screen.fill((60,0,0))
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
        if pltp.collidepoint(pygame.mouse.get_pos()):
            a,b,c = pygame.mouse.get_pressed()
            if a and not cvar:
                enemies +=1
                if enemies > 12:
                    enemies = 12
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
                    enemies = 100
                cvar = True
        if mtp2.collidepoint(pygame.mouse.get_pos()):
            a,b,c = pygame.mouse.get_pressed()
            if a and not cvar:
                kills -= 5
                cvar = True
                if kills <5:
                    kills = 5

        pt = font.render('PLAY',1,YELLOW)
        ptp = pt.get_rect()
        ptp.right = width - 20
        ptp.bottom = height - 20
        if ptp.collidepoint(pygame.mouse.get_pos()):
            pygame.draw.rect(screen,BLUE,ptp)
            a,b,c=pygame.mouse.get_pressed()
            if a:
                main(enemies, kills)
                breakout = True
        screen.blit(pt,ptp)

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
        screen.fill(BLACK)
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

def save():
    global player,weapon,xp,cash
    weapon = weapons.index(player.weapon)
    purchases = []
    dlvls = []
    for i in weapons:
        purchases.append(i.purchased)
        dlvls.append(i.dlvl)
    f = open("Save.pickle",'w')
    pickle.dump([weapon,cash,player.rank,player.level,purchases,dlvls],f)
    f.close()

Menu()
pygame.display.quit()
