import pygame, math
from pygame.locals import *
import PlatformAI as PAI
from random import randint as rand

class Enemy():
    def __init__(self,x,y,health):
        self.rect = pygame.Rect(x,y,30,50)
        self.health = health
        self.starthealth = health
        self.vel = [0,0]
        self.movelist = []
        self.hitwall = False
        self.move = True
        self.bullets = []
        self.timeit = 0
        self.alive = True
        self.pausetimer = 40
        self.deadtimer = 0
        self.curblock = 0
        self.skull = pygame.transform.scale(pygame.image.load("Images/white-skull.png"),(45,45))
        self.skullsurf = pygame.Surface((45,45), pygame.SRCALPHA, 32)
        self.skullsurf.blit(self.skull,(0,0))
        self.targets = []
        for i in range (0,len(PAI.floors)):
            self.targets.append(0)
        a = [math.pi, 0]
        self.curthet = a[rand(0,1)] + (rand(-3,3)/10.0)
        self.aimspeed = .2
        self.images = [pygame.image.load("Images/enemyfront.png"),pygame.image.load("Images/enemyright.png"),pygame.image.load("Images/enemyleft.png")]
        self.images[2] = pygame.transform.flip(self.images[2],True,False)

    def draw(self,background,walls,color,player,xscroll,yscroll):
        if self.alive:
            for i in range(0,len(self.targets)):
                if self.targets[i] < 0:
                    self.targets[i] = 0
                elif self.targets[i] > 0:
                    self.targets[i] -= 1

            if self.pausetimer>0:
                self.pausetimer-=1
                self.move=False
            else:
                self.move=True
            self.timeit += 1
            a = (self.rect.centerx - player.rect.centerx)**2
            b = (self.rect.centery - player.rect.centery)**2
            c = math.sqrt(a+b)

            if self.cview(player,walls) and c < 500:
                pthet = get_theta(self,player)
                if self.curthet < 0:
                    self.curthet += math.pi * 2
                if pthet < 0:
                    pthet += math.pi * 2
                acc = 1
                v = pthet - self.curthet
                if math.fabs(v) > math.pi/2:
                    acc = 3
                if v <= self.aimspeed and v >= (-1 * self.aimspeed):
                    self.curthet = pthet
                if pthet > self.curthet:
                    self.curthet += acc * self.aimspeed
                elif pthet < self.curthet:
                    self.curthet -= acc * self.aimspeed
                if self.curthet < 0:
                    self.curthet += 2*math.pi
                elif self.curthet > 2*math.pi:
                    self.curthet -= 2*math.pi
                if self.vel[0]!=0:
                    if (self.vel[0] > 0 and player.rect.centerx > self.rect.centerx) or (self.vel[0] < 0 and player.rect.centerx < self.rect.centerx):
                        if self.timeit > 8:
                            self.timeit = 0
                            self.bullets.append(ebullet(self,player))
                        self.move = False
                if self.timeit > 8:
                    self.timeit = 0
                    self.bullets.append(ebullet(self, player))
            else:
                if self.pausetimer<=0:
                    self.move = True
                if self.vel[0] > 0:
                    self.curthet = 0
                elif self.vel[0] < 0:
                    self.curthet = math.pi

            if self.health < self.starthealth and self.health > 0:
                pygame.draw.rect(background, (0,255,0), (self.rect.left, self.rect.top - 10, (self.health*self.rect.width)/self.starthealth, 4))

            onBlock = False
            self.head = pygame.Rect(self.rect.left + 3, self.rect.top,self.rect.width-6,self.rect.height/3)
            self.body = pygame.Rect(self.rect.left,self.rect.top + self.rect.height/3,self.rect.width,self.rect.height*2/3)

            if (math.degrees(self.curthet) > -70 and math.degrees(self.curthet) < 70) or (math.degrees(self.curthet) > 290 and math.degrees(self.curthet) < 430):
                background.blit(pygame.transform.scale(self.images[1],(self.head.width,self.head.height)),self.head)
            elif (math.degrees(self.curthet) > 110 and math.degrees(self.curthet) < 250) or (math.degrees(self.curthet) < -110 and math.degrees(self.curthet) > -250):
                background.blit(pygame.transform.scale(self.images[2],(self.head.width,self.head.height)),self.head)
            else:
                img = self.images[0]
                background.blit(pygame.transform.scale(img,(self.head.width,self.head.height)),self.head)

            pygame.draw.rect(background,color,self.body)
            pygame.draw.line(background, (255,0,0),(self.rect.centerx,self.rect.centery),(self.rect.centerx + (20 * math.cos(self.curthet)),self.rect.centery + (20 * (math.sin(self.curthet)))),3)
            self.curblock = None
            a = self.rect.centerx-player.rect.centerx
            b = self.rect.centery-player.rect.centery
            c = math.sqrt((a**2) + (b**2))

            self.vel[1] += 4
            self.rect.y += self.vel[1]
            for i in walls:
                if self.rect.colliderect(i.rect):
                    if self.vel[1]>0:
                        self.rect.bottom=i.rect.top
                    elif self.vel[1]<0:
                        self.rect.top = i.rect.bottom
                    self.vel[1]=0
                if self.rect.bottom == i.rect.top and self.rect.left<i.rect.right and self.rect.right>i.rect.left:
                    onBlock = True
            if self.move or not onBlock:
                self.rect.x += self.vel[0]
                for i in walls:
                    if self.rect.colliderect(i.rect):
                        if self.vel[0]>0:
                            self.rect.right=i.rect.left
                        elif self.vel[0]<0:
                            self.rect.left = i.rect.right
                        if self.vel[1] == 0:
                            self.vel[0] *= -1
                            self.hitwall = not self.hitwall
                if not self.curblock:
                    for i in range(0,len(PAI.floors)):
                        if self.on(i):
                            self.curblock = i
                            break
                if self.movelist == None:
                    self.movelist = []
                if len(self.movelist)>1:
                    if self.on(self.movelist[1]):
                        self.curblock = self.movelist.pop(0)
                    if self.on(self.movelist[0]):
                        if self.movelist[0] == self.curblock:
                            F=PAI.floors[self.movelist[1]]
                            if onBlock:
                                if F.height>self.rect.bottom:
                                    if self.curblock != None:
                                        if F.right>PAI.floors[self.curblock].right and not self.hitwall:
                                            self.vel[0]=16
                                        elif F.left<PAI.floors[self.curblock].left:
                                            self.vel[0]=-16
                                elif F.height<self.rect.bottom and self.curblock != None:
                                    dx = 16 * ((math.sqrt((35**2)+(2*(4)*(self.rect.bottom-F.height)))-35)/4)
                                    if F.left>PAI.floors[self.curblock].left+dx:
                                        tx = F.left-dx
                                        if tx > PAI.floors[self.curblock].left and tx < PAI.floors[self.curblock].right:
                                            if tx>self.rect.right:
                                                self.vel[0] = 16
                                                if self.rect.right>tx-35:
                                                    self.vel[1] = -35
                                            else:
                                                self.vel[0] = -16
                                        else:
                                            self.vel[0] = 16
                                            if self.rect.right>PAI.floors[self.curblock].right:
                                                self.vel[1] = -35
                                    else:
                                        tx = F.right + dx
                                        if tx > PAI.floors[self.curblock].left and tx < PAI.floors[self.curblock].right:
                                            if tx<self.rect.right:
                                                self.vel[0] = -16
                                                if self.rect.left<tx + 35:
                                                    self.vel[1] = -35
                                            else:
                                                self.vel[0] = 16
                                        else:
                                            self.vel[0] = -16
                                            if self.rect.left < PAI.floors[self.curblock].left:
                                                self.vel[1] = -35
                            else:
                                self.hitwall = False
                    elif onBlock:
                        if self.curblock != None and len(self.movelist) > 1:
                            self.movelist = PAI.Check(self.curblock, self.movelist[len(self.movelist)-1])
                        else:
                            self.movelist = []
                else:
                    if onBlock and not self.curblock:
                        for i in range(0, len(PAI.floors)):
                            if self.on(i):
                                self.curblock = i
                                break
                    if self.curblock and len(self.movelist)<=1:

                        tb = self.curblock
                        while tb == self.curblock:
                            tb = rand(0,18)
                        self.movelist = PAI.Check(self.curblock,tb)

                if not self.movelist and self.curblock == 0:
                    self.movelist = [0,2]

            if onBlock:
                for i in PAI.floors:
                    if self.rect.bottom == i.height and self.rect.right > i.left and self.rect.left < i.right:
                        self.curblock = PAI.floors.index(i)
                if self.curblock:
                    if not self.cview(player,walls):
                        self.targets[self.curblock] = 0
                    if max(self.targets):
                        testlist = PAI.Check(self.curblock, self.targets.index(max(self.targets)))
                        if testlist:
                            if (max(self.targets)/12) > len(testlist):
                                self.movelist = testlist

    def on(self, fl):
        F=PAI.floors[fl]
        if self.rect.bottom == F.height and self.rect.left<F.right and self.rect.right>F.left:
            return True
        else:
            return False

    def cview(self, player, walls):
        theta = math.atan2(player.rect.centery-self.rect.centery,player.rect.centerx-self.rect.centerx)
        self.tvel = [math.cos(theta), math.sin(theta)]
        self.tpos = [self.rect.centerx, self.rect.centery]
        breakout = False
        hit = False
        while True:
            self.tpos[0] += self.tvel[0]
            self.tpos[1] += self.tvel[1]
            for wall in walls:
                if wall.rect.collidepoint((self.tpos[0],self.tpos[1])):
                    breakout = True
                    break
            if player.rect.collidepoint((self.tpos[0],self.tpos[1])):
                hit = True
                break
            if breakout:
                break
        if hit and player.alive:
            return True
        else:
            return False

def get_theta(ene, pla):
    theta = math.atan2((pla.rect.centery)-ene.rect.centery,(pla.rect.centerx)-ene.rect.centerx)
    return theta

class ebullet():
    def __init__(self,ene,pla):
        self.pos = [ene.rect.centerx,ene.rect.centery]
        theta = ene.curthet +(rand(-10,10))/100.0
        self.vel = [math.cos(theta),math.sin(theta)]
    def draw(self, background, color, walls, player, show):
        dead = False
        self.pos[0] += 6 * self.vel[0]
        self.pos[1] += 6 * self.vel[1]
        if show:
            pygame.draw.circle(background,color,(int(self.pos[0]),int(self.pos[1])),3)

        if player.head.collidepoint(self.pos[0],self.pos[1]):
            dead = True
            player.health -= 2
            player.healthtimer = 0
        if player.body.collidepoint(self.pos[0],self.pos[1]):
            dead = True
            player.health -= 1
            player.healthtimer = 0

        for wall in walls:
            if wall.rect.collidepoint((int(self.pos[0]),int(self.pos[1]))):
                dead = True

        if dead:
            return True
