from re import X
from typing import Any
import pygame
import random


from pygame.locals import (
    RLEACCEL,
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    KEYDOWN,
    K_SPACE,
    QUIT,
)
pygame.font.init()
font = pygame.font.Font("valorax.ttf", 30)
font2 = pygame.font.Font("valorax.ttf", 18)
bg_image = pygame.image.load('background-black.png')
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
ENEMY_HEIGHT = 60
ENEMY_WIDTH = 60
ENEMY_ROW = 5
ENEMY_COLUMN = 8


def enemySpawn():
    for i in range(ENEMY_COLUMN):
        for j in range(ENEMY_ROW):
            px = i*(ENEMY_WIDTH+5)+5
            py = j*(ENEMY_HEIGHT+5)+5
            if j in [0,]:
                enemy = Enemy_white(px,py)
            if j == 1:
                enemy = Enemy_grey(px,py)
            if j == 2:
                enemy = Enemy_blue(px,py)
            if j == 3:
                enemy = Enemy_green(px,py)
            if j == 4:
                enemy = Enemy_red(px,py)
            enemies.add(enemy)

def draw_text(text,font,text_col,x,y):
    image = font.render(text,True,text_col)
    win.blit(image,(x,y))


class Player(pygame.sprite.Sprite):
    def __init__(self,):
        super(Player, self).__init__()
        self.surf = pygame.image.load("pixel_ship_yellow_small.png").convert()
        self.surf.set_colorkey((0,0,0), RLEACCEL)
        self.rect = self.surf.get_rect()
        self.rect.move_ip( 5, SCREEN_HEIGHT-50)
        self.bullet_x = 45/2+5
        self.bullet_y = SCREEN_HEIGHT- 61
        self.speed = 7
        
        
    
    def update(self, pressed_keys):
        if pressed_keys[K_LEFT]:
            self.rect.move_ip(-self.speed, 0)
            self.bullet_x -= self.speed
        if pressed_keys[K_RIGHT]:
            self.rect.move_ip(self.speed, 0)
            self.bullet_x += self.speed
        if self.rect.left < 0:
            self.rect.left = 0
        elif self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        if self.rect.top <= 0:
            self.rect.top = 0
        elif self.rect.bottom >= SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT

class Bullet(pygame.sprite.Sprite):
    def __init__(self,x,y):
        super().__init__()
        self.x = x
        self.y = y 
        self.surf = pygame.Surface([6,6])
        self.rect = self.surf.get_rect()
        self.rect.move_ip(x,y)
        pygame.draw.circle(self.surf, (200,200,200), (3,3),3)
        
    
    def update(self):
        self.y -= 5
        self.rect.move_ip(0,-5)
        if self.y < 0:
            self.kill() 
        
        
class EnemyBullet(pygame.sprite.Sprite):
    def __init__(self,x,y):
        super().__init__()
        self.x = x
        self.y = y 
        self.surf = pygame.Surface([6,6])
        self.rect = self.surf.get_rect()
        self.rect.move_ip(x,y)
        pygame.draw.circle(self.surf, (255,0,0), (3,3),3)
        self.maxMove = SCREEN_HEIGHT
        
    
    def update(self):
        self.y += 8
        self.rect.move_ip(0,+8)
        if self.y > self.maxMove:
            self.kill()

    
class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super(Enemy, self).__init__()
        self.surf = pygame.Surface((ENEMY_HEIGHT,ENEMY_WIDTH))
        self.surf.fill((255, 255, 255))
        self.rect = self.surf.get_rect()
        self.rect.move_ip(x,y)
        self.speed = 5
        self.moveCount = 0
        self.maxMove = (SCREEN_WIDTH - ((ENEMY_COLUMN * (ENEMY_WIDTH + 5) )+5)) / self.speed
        self.bullet_x = ENEMY_WIDTH/2 + x
        self.bullet_y = ENEMY_HEIGHT + y
        self.original_x = x
        self.original_y = y
        self.isAttacking = False
        self.x = x
        self.y = y
        self.isBackToHome = False
        self.speed_2 = 8

    
    def update(self):
        if self.isBackToHome:
            mx = self.original_x - self.x
            my = self.original_y - self.y
            if mx > self.speed_2:
                mx = self.speed_2
            if my > self.speed_2:
                my = self.speed_2
            self.rect.move_ip(mx,my)
            self.x += mx
            self.y += my
            if (self.x == self.original_x) and (self.y == self.original_y):
                self.isBackToHome = False
        if self.isAttacking == True:
            self.rect.move_ip(0,abs(self.speed)) 
            self.y += abs(self.speed)
            if self.y > SCREEN_HEIGHT:
               self.rect.move_ip((0-self.x),(0-self.y)) 
               self.isBackToHome = True
               self.x = 0
               self.y = 0
               self.isAttacking = False 
        else:
            self.rect.move_ip(self.speed,0)
            self.x += self.speed
     
        self.moveCount += 1
        self.original_x += self.speed
        self.bullet_x = self.x + 30
        self.bullet_y = self.y + 60
            
        if self.moveCount > self.maxMove:
            self.speed *= -1
            self.moveCount = 0
            
        


class Enemy_red(Enemy):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.surf = pygame.image.load("red.png").convert()
        self.surf.set_colorkey((0,0,0), RLEACCEL)
        self.score = 10
       

class Enemy_green(Enemy):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.surf = pygame.image.load("green.png").convert()
        self.surf.set_colorkey((0,0,0), RLEACCEL)
        self.score = 25
        

class Enemy_blue(Enemy):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.surf = pygame.image.load("blue.png").convert()
        self.surf.set_colorkey((0,0,0), RLEACCEL)
        self.score = 50

class Enemy_grey(Enemy):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.surf = pygame.image.load("grey.png").convert()
        self.surf.set_colorkey((0,0,0), RLEACCEL)
        self.score = 80

class Enemy_white(Enemy):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.surf = pygame.image.load("black.png").convert()
        self.surf.set_colorkey((0,0,0), RLEACCEL)
        self.score = 100


pygame.init()
clock = pygame.time.Clock()

win = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

player = Player()
enemies = pygame.sprite.Group()
bullets = pygame.sprite.Group()
enemy_bullets = pygame.sprite.Group()


enemySpawn()


ADDBULLET = pygame.USEREVENT + 1
pygame.time.set_timer(ADDBULLET, 750)
maxEnemyBullet = 2

ENEMYATTACK = pygame.USEREVENT + 2
pygame.time.set_timer(ENEMYATTACK,1000)
maxAttacking = 2

running = True
lifeCount = 3
maxBullet = 4
myScore = 0
gameOver= False
while running:
    clock.tick(30)
    

    for event in pygame.event.get():
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                running = False
        elif event.type == QUIT:
            running = False
        if event.type == KEYDOWN:
            if event.key == K_SPACE:
                if maxBullet > bullets.__len__() and not gameOver:
                    bullet = Bullet(player.bullet_x,player.bullet_y)
                    bullets.add(bullet)
        if event.type == ADDBULLET:
            if maxEnemyBullet > enemy_bullets.__len__() and not gameOver:
                if enemies.__len__() > 1:
                    r = random.randint(0,enemies.__len__()-1)
                else:
                    r = 0
                e =pygame.sprite.Group.sprites(enemies)[r]
                eb = EnemyBullet(e.bullet_x, e.bullet_y)
                enemy_bullets.add(eb)
                
                    
                    
        if event.type == ENEMYATTACK and not gameOver:
            attackCount = 0
            for e in enemies:
                if e.isAttacking:
                    attackCount+=1
            if attackCount < maxAttacking:
                r = random.randint(1,enemies.__len__())
                pygame.sprite.Group.sprites(enemies)[r-1].isAttacking = True

    pressed_keys = pygame.key.get_pressed()
    player.update(pressed_keys)
    
    win.blit(bg_image,(0,0))
    
    for e in enemies:
        win.blit(e.surf,e.rect)
    enemies.update()

    for b in bullets:
        win.blit(b.surf,b.rect)
    bullets.update()

    for eb in enemy_bullets:
        win.blit(eb.surf, eb.rect)
    enemy_bullets.update()
    
    isHit = pygame.sprite.spritecollideany(player, enemies)
    
    if isHit != None:
        lifeCount -= 1
        isHit.isBackToHome = True
    
    if  pygame.sprite.spritecollide(player, enemy_bullets,True):
        lifeCount -= 1
    enemyDict = pygame.sprite.groupcollide(enemies, bullets,False,True)
    
    for e in enemyDict:
        myScore += e.score
        e.kill()
    
    if enemies.__len__() == 0:
        enemySpawn()        
        maxAttacking += 2
        maxEnemyBullet += 2
        maxBullet += 2
        
    if lifeCount > 0:
        win.blit(player.surf,player.rect)
    else:   
        gameOver = True
        lifeCount = 0
        draw_text(('Game over!'),font,(255,255,255), 270,350 )

    draw_text((f"lives: {lifeCount}, Score: {myScore}"),font2,(255,255,255),20,550) 
    pygame.display.flip()