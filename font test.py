import pygame
from pygame.locals import *

pygame.init()

lis = pygame.font.get_fonts()
print len(lis)

screen = pygame.display.set_mode((800,900))
background=pygame.Surface((200,900))
background=background.convert()
background.fill((0,0,0))

rem = ['brushscriptmt', 'gb18030bitmap', 'webdings','applebraille','kokonor','wingdings2','wingdings3']
for i in rem:
    lis.remove(i)
lis.append(None)

while True:
    screen.blit(background,(0,0))
    p = 0
    for f in lis:
        font = pygame.font.SysFont(f,30)
        t = font.render(str(f),1,(255,255,255))
        tp = t.get_rect()
        tp.left = 10
        tp.top = p
        screen.blit(t,tp)
        font = pygame.font.SysFont(f,20,False,True)
        t = font.render(str(f),1,(255,255,255))
        tp = t.get_rect()
        tp.left = 300
        tp.top = p
        p = tp.bottom
        screen.blit(t,tp)
    pygame.display.flip()
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.display.quit()
            break