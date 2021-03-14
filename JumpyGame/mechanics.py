import pygame as pg
from pygame.locals import *
import sys
import random
from settings import*

vec = pg.math.Vector2               #2-dimensional vector for movement

class Player(pg.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = player_img_stand
        self.rect = self.image.get_rect()
        self.pos = vec((WIDTH/2, 580))
        self.vel = vec(0,0)
        self.acc = vec(0,0)
        self.jumping = False
        self.score = 0

    def move(self):             #dynamic movevemt using vectors
        self.acc = vec(0,0.55)
        speedy_hits = pg.sprite.spritecollide(self, speedy_platforms, False)
        key = pg.key.get_pressed()
        if key[K_LEFT] or key[K_a]:
            self.image = player_img_left
            if speedy_hits:
                self.acc.x = -ACC - 0.8
            else:
                self.acc.x = -ACC
        if key[K_RIGHT] or key[K_d]:
            self.image = player_img_right
            if speedy_hits:
                self.acc.x = ACC + 0.8
            else:
                self.acc.x = ACC
        self.acc.x += self.vel.x * SLOWING
        self.vel += self.acc
        self.pos += self.vel + 0.55 * self.acc
        self.rect.midbottom = self.pos

        if self.pos.x > WIDTH:      #teleport to other side when leaving screen
            self.pos.x = 0
        if self.pos.x < 0:
            self.pos.x = WIDTH

    def jump(self):                 #jumping; max height dependent on platform type
        hits = pg.sprite.spritecollide(self, platforms, False)
        bouncy_hits = pg.sprite.spritecollide(self, bouncy_platforms, False)
        if bouncy_hits and not self.jumping:
            self.jumping = True
            self.vel.y = -20
            return
        elif hits and not self.jumping:
           self.jumping = True
           self.vel.y = -15

    def stop_jump(self):            #allows jumps to be shortened
        if self.jumping:
            if self.vel.y < -2:
                self.vel.y = -2

    def update(self):               #updates the player class
        hits = pg.sprite.spritecollide(self, platforms, False)
        if self.vel.y > 0 and hits:
            if self.pos.y < hits[0].rect.bottom:
                if hits[0].point > 0:
                    hits[0].point -= 100        #points in steps of 100
                    self.score += 100
                self.pos.y = hits[0].rect.top +1
                self.vel.y = 0
                self.jumping = False

    #"camera" movement
    def scroll(self):               #moves "camera" up at certain height
        if self.rect.top <= HEIGHT/3:       #follow player on screen
            self.pos.y += abs(self.vel.y)
            for plat in platforms:
                plat.rect.y += abs(self.vel.y)
                if plat.rect.top >= HEIGHT:     #remove platforms off screen
                    plat.kill()

    def auto_scroll(self):          #continually moves "camera" up
        if player.score < 1500:       #increase scroll speed after point thresholds
            SPEED = 1
        elif player.score >= 1500 and player.score < 3000:
            SPEED = 1.5
        else:
            SPEED = 2
        if pg.sprite.spritecollide(self, base_group, False):        #only start after leaving base_plat
            return
        else:
            self.pos.y += SPEED           #scroll speed
            for plat in platforms:
                plat.rect.y += SPEED
                if plat.rect.top >= HEIGHT:     #remove platforms off screen
                    plat.kill()

class Platform(pg.sprite.Sprite):
    def __init__(self):             #initializes platform and gives parameters for randomized platform size
        super().__init__()
        if player.score < 500:
            min = 70
            max = 120
        elif player.score >= 500 and player.score < 1000:
            min = 60
            max = 100
        elif player.score >= 1000 and player.score < 2000:
            min = 50
            max = 85
        else:
            min = 40
            max = 70
        self.surf = pg.Surface((random.randint(min, max), 10))
        self.surf.fill(LIGHTGREY)
        self.rect = self.surf.get_rect(center = (random.randint(0,WIDTH-25), random.randint(0, HEIGHT-10)))
        self.point = 100                #points awarded for landing on this platform type

class Bouncy_Platform(Platform):
    def __init__(self):
        super().__init__()
        self.surf.fill(WHITE)
        self.point = 200

class Speedy_Platform(Platform):
    def __init__(self):
        super().__init__()
        if player.score < 500:
            speedy_min = 90
            speedy_max = 140
        elif player.score >= 500 and player.score < 1000:
            speedy_min = 80
            speedy_max = 120
        elif player.score >= 1000 and player.score < 2000:
            speedy_min = 70
            speedy_max = 100
        else:
            speedy_min = 55
            speedy_max = 85
        self.surf = pg.Surface((random.randint(speedy_min, speedy_max), 10))
        self.surf.fill(BLUE)
        self.point = 300

def check(Platform, all_plat):  #checks for colission/proximity of platforms
    if pg.sprite.spritecollideany(Platform, all_plat):
        return True
    else:
        for plat in all_plat:
            if plat == Platform:
                continue
            if (abs(Platform.rect.top - plat.rect.bottom) < 50) and (abs(Platform.rect.bottom - plat.rect.top) < 50):
                return True
            else:
                collide = False

def plat_create():          #seta the odds for each platform types and creates them in a semi-random location on the screen if the check is passed
    while len(platforms) < 10:
        plat_width = random.randrange(50,100)
        rando = random.randrange(0,100)
        if rando < 40:
            p = Platform()
        elif rando < 70:
            p  = Bouncy_Platform()
        else:
            plat_width = random.randrange(80,130)
            p = Speedy_Platform()

        collide = True
        while collide:
             p.rect.center = (random.randrange(0 + plat_width//2, WIDTH - plat_width//2), random.randrange(-50, 0))
             collide = check(p, platforms)
        platforms.add(p)
        if rando >39 and rando < 70:
            bouncy_platforms.add(p)
        if rando > 69:
            speedy_platforms.add(p)

#creates sprite groups and player object 
player = Player()
platforms = pg.sprite.Group()
base_group = pg.sprite.Group()
bouncy_platforms = pg.sprite.Group()
speedy_platforms = pg.sprite.Group()
