import pygame, math
from pygame.locals import *
from random import randint as rand
import PlatformAI as PAI

class player():
    def __init__(self, x, y, width = 30, height = 50):
        self.rect = pygame.Rect(x, y, width, height)
        self.rect.top = y
        self.rect.left = x
        self.vel = [0,0]
        self.maxvel = 16
        self.maxjump = 36
        self.var = True
        self.health = 100
        self.healthtime = 0
        self.htime = 60
        self.kills = 0
        self.deaths = 0
        self.alive = True
        self.skulls = pygame.image.load("Images/red-skull.png")
        self.skulls = pygame.transform.scale(self.skulls, (45,45))
        self.skullsurf = pygame.Surface((45,45), SRCALPHA , 32)
        self.skullsurf.blit(self.skulls,(0,0))
        self.skullsurf = self.skullsurf.convert_alpha()
        self.deadtimer = 0
        self.zone = None
        self.awareness = 0
        self.weapon = None
        self.firetime = 2
        self.curstreak = 0
        self.killstreak = 0
        self.clip = 0
        self.reloading = False
        self.rank = 0
        self.level = 1
        self.headnum = 1
        self.headimg = pygame.image.load("Images/front" + str(self.headnum) + ".png")
        self.sideimg = pygame.image.load("Images/side" + str(self.headnum) + ".png")
        self.grenades = []
        self.gvar = False
        self.grenum = 1
        self.grenmax = 3
        self.name = 'Player'
        self.invintime = 30
    def set_head(self):
        self.headimg = pygame.image.load("Images/front" + str(self.headnum) + ".png")
        self.sideimg = pygame.image.load("Images/side" + str(self.headnum) + ".png")
    def reset(self, x, y):
        self.rect = pygame.Rect(x, y, 30, 50)
        self.rect.top = y
        self.rect.left = x
        self.vel = [0,0]
        self.maxvel = 16
        self.maxjump = 36
        self.var = True
        self.health = 100
        self.healthtime = 0
        self.kills = 0
        self.deaths = 0
        self.alive = True
        self.deadtimer = 0
        self.zone = None
        self.awareness = 0
        self.firetime = 2
        self.curstreak = 0
        self.killstreak = 0
        self.reloading = False
        self.grenades = []
        self.grenum = self.grenmax
        self.invintime = 30
    def draw(self, screen, color, walls, xscroll, yscroll, spawnpoints, enemies, truescreen):
        key = pygame.key.get_pressed()
        if (self.clip <=0 or key[K_r]) and not self.reloading and self.clip < self.weapon.magsize:
            self.firetime = self.weapon.reloadtime
            self.reloading = True
        if self.curstreak > self.killstreak:
            self.killstreak = self.curstreak
        self.firetime -=1
        if self.firetime <= 0:
            self.firetime = 0
            if self.reloading:
                self.reloading = False
                self.clip = self.weapon.magsize
        if self.alive:
            if self.invintime>0:
                self.invintime-=1
            if self.health <100:
                self.healthtime -= 1
                if self.healthtime <= 0:
                    self.health += .5
                    if self.health >100:
                        self.health = 100
            onBlock = False
            self.head = pygame.Rect(self.rect.left + 3, self.rect.top,self.rect.width-6,self.rect.height/3)
            self.body = pygame.Rect(self.rect.left,self.rect.top + self.rect.height/3,self.rect.width,self.rect.height*2/3)
            pygame.draw.rect(screen,color,self.body)
            if self.invintime:
                pygame.draw.rect(screen,(180,180,255),self.rect,(self.invintime/10)+1)
            mx,my = pygame.mouse.get_pos()
            mx += xscroll
            my += yscroll
            th = math.atan2(my-self.rect.centery,mx-self.rect.centerx)
            img = self.weapon.image
            imw, imh = img.get_size()
            vv = imh/22.0
            img = pygame.transform.scale(img,(int(imw/vv),int(imh/vv)))
            shift = -12
            if (th<math.pi/2 and th>math.pi*-.5) or (th>math.pi*3/2 and th < math.pi*5/2):
                img =pygame.transform.flip(img,False,True)
                shift = 12
            img = pygame.transform.rotate(img, math.degrees(th))
            img = pygame.transform.flip(img,False, True)
            imrec = img.get_rect()
            imrec.centerx = self.rect.centerx + shift
            imrec.centery = self.rect.centery

            if key[K_f] and self.gvar and self.grenum > 0:
                self.grenum -= 1
                self.grenades.append(grenade(th,self,mx,my))
                self.gvar = False
            elif not key[K_f] and not self.gvar:
                self.gvar = True
            hrect = self.head
            if self.headnum == 8:
                hrect.width += 8
                hrect.left -= 4
            if (math.degrees(th) > -70 and math.degrees(th) < 70) or (math.degrees(th) > 290 and math.degrees(th) < 430):
                screen.blit(pygame.transform.scale(self.sideimg,(self.head.width,self.head.height)),hrect)
            elif (math.degrees(th) > 110 and math.degrees(th) < 250) or (math.degrees(th) < -110 and math.degrees(th) > -250):
                himg = pygame.transform.flip(self.sideimg,True,False)
                screen.blit(pygame.transform.scale(himg,(self.head.width,self.head.height)),hrect)
            else:
                screen.blit(pygame.transform.scale(self.headimg,(self.head.width,self.head.height)),hrect)

            screen.blit(img,imrec)

            if self.health <100:
                pygame.draw.rect(screen,(0,255,0),(self.rect.left, self.rect.top - 10, self.health * .3, 4))
            self.vel[1] += 4
            self.rect.y += self.vel[1]
            if self.rect.bottom > 1200:
                self.rect.bottom = 1180
                self.vel[1] = -1
            for i in walls:
                if self.rect.colliderect(i.rect):
                    if self.vel[1]>0:
                        self.rect.bottom=i.rect.top
                    elif self.vel[1]<0:
                        self.rect.top = i.rect.bottom
                    self.vel[1]=0
                if self.rect.bottom == i.rect.top and self.rect.left<i.rect.right and self.rect.right>i.rect.left:
                    onBlock = True
            self.rect.x += self.vel[0]
            for i in walls:
                if self.rect.colliderect(i.rect):
                    if self.vel[0]>0:
                        self.rect.right=i.rect.left
                    elif self.vel[0]<0:
                        self.rect.left = i.rect.right
                    self.vel[0]=0
            k = pygame.key.get_pressed()
            if k[K_RIGHT] or k[K_d]:
                self.vel[0] += 5
                if self.vel[0] > self.maxvel:
                    self.vel[0] = self.maxvel
            if k[K_LEFT] or k[K_a]:
                self.vel[0] -=5
                if self.vel[0] < (-1*self.maxvel):
                    self.vel[0] = (-1*self.maxvel)

            if not k[K_LEFT] and not k[K_RIGHT] and not k[K_a] and not k[K_d]:
                self.vel[0] /= 4.0
                if self.vel[0] < 1 and self.vel[0]>-1:
                    self.vel[0] = 0

            if onBlock:
                if k[K_UP] or k[K_w] or k[K_SPACE]:
                    self.vel[1] = -self.maxjump

            if k[K_s] or k[K_DOWN]:
                if self.rect.height==50:
                    self.rect.y+=25
                self.rect.height=25
                self.maxvel=7
                self.maxjump = 28
            else:
                if self.rect.height == 25:
                    self.rect.y -=25
                self.rect.height=50
                self.maxvel=16
                self.maxjump = 36

            if pygame.mouse.get_pressed()[0] and not self.var and self.firetime<=0:
                if not self.weapon.Class == "Full-Auto":
                    self.var = True
                x,y = pygame.mouse.get_pos()
                x += xscroll
                y += yscroll
                self.clip -= 1
                self.firetime = self.weapon.firerate
                if self.zone:
                    if not self.weapon.Class == "Sniper":
                        for e in enemies:
                            e.targets[self.zone] += 9
                            if self.weapon.Class == "Shotgun":
                                e.targets[self.zone] += 4
                ret = [bullet(self.rect.centerx,self.rect.centery,x,y,self)]
                if self.weapon.Class == "Shotgun":
                    for i in range(0,5):
                        ret.append(bullet(self.rect.centerx,self.rect.centery,x,y,self))
                return ret

            if self.var and not pygame.mouse.get_pressed()[0]:
                self.var = False

            poss = None
            for i in PAI.floors:
                if self.rect.bottom <= i.height and self.rect.right > i.left and self.rect.left < i.right:
                    if poss:
                        if i.height < PAI.floors[poss].height:
                            poss = PAI.floors.index(i)
                    else:
                        poss = PAI.floors.index(i)

            self.zone = poss

        else:
            if self.curstreak:
                self.curstreak = 0
            self.rect.y -= 1
            screen.blit(self.skullsurf, self.rect)
            self.deadtimer -= 1
            if self.deadtimer <=0:
                self.rect.x, self.rect.y = spawnpoints[rand(0, len(spawnpoints) - 1)]
                self.health = 100
                self.clip = self.weapon.magsize
                self.grenum = self.grenmax
                self.vel = [0,0]
                return True
        poplist = []

        for gren in self.grenades:
            gv = gren.draw(walls, screen, enemies, self)
            if gv:
                poplist.append(gren)

        for i in poplist:
            self.grenades.remove(i)

class bullet():
    def __init__(self, x, y, tx, ty, player):
        self.x = x
        self.y = y
        theta = math.atan2(ty-y,tx-x)
        if player.rect.height >=50:
            theta += rand(-20,20)/float(player.weapon.accuracy)
        else:
            theta += rand(-20,20)/(float(player.weapon.accuracy)*1.5)
        self.vel = [math.cos(theta),math.sin(theta)]

    def draw(self,background,color,walls,enemies,show,player,hvar):
        dead = False
        self.x += 4 * self.vel[0]
        self.y += 4 * self.vel[1]
        if show:
            pygame.draw.circle(background,color,(int(self.x),int(self.y)),1)

        if hvar:
            for enemy in enemies:
                if enemy.head.collidepoint((int(self.x),int(self.y))) or enemy.body.collidepoint((int(self.x),int(self.y))):
                    if enemy.alive and enemy.health > 0:
                        dead = True
                        if (enemy.headshot and enemy.head.collidepoint((int(self.x), int(self.y)))) or not enemy.headshot:
                            enemy.health -= player.weapon.damage
                            if enemy.head.collidepoint((int(self.x),int(self.y))):
                                enemy.health -= player.weapon.damage
                            enemy.healthtime = enemy.htime
                            if enemy.health <= 0:
                                enemy.deaths += 1
                                enemy.deadtimer = 70
                                enemy.alive = False
                                player.kills += 1
                                player.curstreak += 1
                            break

            for wall in walls:
                if wall.rect.collidepoint((int(self.x),int(self.y))):
                    dead = True

        return dead

class grenade():
    def __init__(self, theta, player, mx, my):
        v = math.fabs(math.hypot(player.rect.centerx - mx, player.rect.centery - my))
        v = 8*math.log1p(v)+1

        self.vel = [v*math.cos(theta),v*math.sin(theta)]
        self.pos = [player.rect.centerx, player.rect.centery]
        self.acc = [0, 4]
        self.timer = 30
        self.rad = 5
    def draw(self, walls, screen, enemies, player):
        if self.timer >3:
            self.timer -=1
            for i in range(0,5):
                self.vel[1] += self.acc[1]/5.0
                self.pos[1] += self.vel[1]/5.0
                for wall in walls:
                    if self.vel[1] > 0:
                        if wall.rect.collidepoint((int(self.pos[0]),int(self.pos[1])+self.rad)):
                            self.vel[1] *= -3/4.5
                            self.pos[1] = wall.rect.top - self.rad
                    elif self.vel[1] <0:
                        if wall.rect.collidepoint((int(self.pos[0]),int(self.pos[1])-self.rad)):
                            self.vel[1] *= -3/4.0
                            self.pos[1] = wall.rect.bottom + self.rad
                self.pos[0] += self.vel[0]/5.0
                for wall in walls:
                    if self.vel[0] > 0:
                        if wall.rect.collidepoint((int(self.pos[0]) + self.rad, int(self.pos[1]))):
                            self.vel[0] *= -3/5.0
                            self.pos[0] = wall.rect.left - self.rad
                    elif self.vel[0] < 0:
                        if wall.rect.collidepoint((int(self.pos[0]) - self.rad, int(self.pos[1]))):
                            self.vel[0] *= -3/5.0
                            self.pos[0] = wall.rect.right + self.rad
                    if self.pos[1] + self.rad == wall.rect.top:
                        self.vel[0] *= 7/8.0
                if self.vel[0] < 1 and self.vel[0] > -1 and self.vel[0] != 0:
                    self.vel[0] = 0

            pygame.draw.circle(screen, (0,150,0),(int(self.pos[0]),int(int(self.pos[1]))),self.rad)
            return False
        elif self.timer == 3 or self.timer == 0:
            self.timer -= 1
            pygame.draw.circle(screen,(255,255,100),(int(self.pos[0]),int(self.pos[1])),20)
        elif self.timer == 2:
            self.timer -= 1
            pygame.draw.rect(screen,(255,150,0),(int(self.pos[0])-35,int(self.pos[1])-35,70,70))
            pygame.draw.circle(screen,(255,255,0),(int(self.pos[0]),int(self.pos[1])),50)
        elif self.timer == 1:
            self.timer -= 1
            pygame.draw.circle(screen,(255,165,0),(int(self.pos[0]),int(self.pos[1])),100)
            pygame.draw.circle(screen,(255,0,0),(int(self.pos[0]),int(self.pos[1])),70)
            pygame.draw.circle(screen,(255,255,90),(int(self.pos[0]),int(self.pos[1])),30)
            pygame.draw.circle(screen,(255,255,255),(int(self.pos[0]),int(self.pos[1])),10)
            for e in enemies:
                hit = False
                if e.alive and e.rect.colliderect(pygame.Rect(self.pos[0]-100,self.pos[1]-100,200,200)):
                    for x in (e.rect.left,e.rect.right):
                        for y in (e.rect.top,e.rect.bottom):
                            if math.hypot(self.pos[0]-x,self.pos[1]-y) < 100:
                                hit = True
                if hit:
                    damage = 1.5*(22*((100/(math.hypot(self.pos[0]-e.rect.centerx,self.pos[1]-e.rect.centery)+10))**2))
                    e.health -= damage
                    e.healthtime = e.htime
                    if e.health <= 0 and e.alive:
                        e.deadtimer = 70
                        e.alive = False
                        e.deaths += 1
                        player.kills += 1
                        player.curstreak += 1

        else:
            return True



class weapon():
    def __init__(self,Class,damage,accuracy,magsize,firerate,reloadtime,name,image,reqlevel,dinc,cost):
        self.reloadtime = reloadtime
        self.firerate = firerate
        self.Class = Class
        self.name = name
        self.image = pygame.image.load(image)
        w = self.image.get_width()
        h = self.image.get_height()
        self.image = pygame.transform.scale(self.image,(w*45/h,45))
        self.damage = damage
        self.accuracy = accuracy
        self.magsize = magsize
        self.reqlevel = reqlevel
        self.var = False
        self.dlvl = 1
        self.dinc = dinc
        self.purchased = False
        self.cost = cost
        self.classlist = ["Semi-Auto","Full-Auto","Sniper","Shotgun"]
    def shopdraw(self,screen, y, width, height, player, cash):
        try:
            font = pygame.font.SysFont('andalemono',25)
        except:
            font = pygame.font.Font(None,35)
        pfont = pygame.font.Font(None,50)
        color = (255,255,255)
        if player.level < self.reqlevel and self.purchased:
            color = (100,100,100)
        nt = font.render(self.name + "    Class: " + self.Class,1,color)
        ntp = nt.get_rect()
        ntp.left = 25
        ntp.top = y
        font = pygame.font.Font(None,25)
        text = "DAMAGE: " + str(self.damage)
        if self.Class == "Shotgun":
            text += " x 5"
        dt = font.render(text, 1, (175,0,0))
        dtp = dt.get_rect()
        dtp.left = width/2
        dtp.top = ntp.bottom
        if self.purchased and self.dlvl <= 3:
            pt = pfont.render("+",1,(255,0,0))
            ptp = pt.get_rect()
            ptp.centery = dtp.centery - 3
            ptp.left = dtp.right + 5
            ptpc = pygame.Rect(ptp.left,ptp.top + 8,ptp.width,ptp.height-13)
            pygame.draw.rect(screen,(0,255,0),ptpc)
            screen.blit(pt,ptp)
            charge = self.dinc *10 *self.dlvl *(1 + self.classlist.index(self.Class))
            if ptpc.collidepoint(pygame.mouse.get_pos()):
                ct = font.render("$"+str(charge),1,(0,255,0))
                ctp = ct.get_rect()
                ctp.centery = ptpc.centery
                ctp.left = ptpc.right + 8
                screen.blit(ct,ctp)
            a,b,c = pygame.mouse.get_pressed()
            if a and not self.var:
                self.var = True
                if ptpc.collidepoint(pygame.mouse.get_pos()) and cash >= charge:
                    cash -= charge
                    self.damage += self.dinc
                    self.dlvl += 1
            if not a and self.var:
                self.var = False

        at = font.render("ACCURACY: " + str(round(100.0*(1-(20.0/self.accuracy)))) + "%",1,(175,0,0))
        atp = at.get_rect()
        atp.left = width/2
        atp.bottom = ntp.bottom + 45
        screen.blit(dt,dtp)
        screen.blit(at,atp)
        screen.blit(nt,ntp)
        rect = self.image.get_rect()
        rect.left = 25
        rect.top = ntp.bottom
        a,b,c = pygame.mouse.get_pressed()
        if a and rect.collidepoint(pygame.mouse.get_pos()) and not self.var and not self.purchased:
            self.var = True
            if cash >= self.cost:
                cash -= self.cost
                self.purchased = True
                player.weapon = self
        if a and rect.collidepoint(pygame.mouse.get_pos()) and self.purchased:
            player.weapon = self

        if not a and self.var:
            self.var = False

        if player.weapon == self:
            pygame.draw.rect(screen,(200,0,0),rect)
        screen.blit(self.image,(25,ntp.bottom))
        surf = pygame.Surface((rect.width,rect.height))
        surf.fill((0,0,0))
        surf.set_alpha(140)
        if player.level < self.reqlevel:
            screen.blit(surf,rect)
            rt = font.render("LEVEL " + str(self.reqlevel),1,(255,0,0))
            rtp = rt.get_rect()
            rtp.left = rect.right + 10
            rtp.centery = rect.centery
            screen.blit(rt,rtp)
        if self.purchased == False and player.level >= self.reqlevel:
            bt = font.render("$"+str(self.cost),1,(0,255,0))
            btp = bt.get_rect()
            btp.left = rect.right + 10
            btp.centery = rect.centery
            screen.blit(bt,btp)

        return ntp.bottom + 55, cash
