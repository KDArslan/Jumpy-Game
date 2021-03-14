import pygame as pg
import sys
import random
from settings import*
from mechanics import*

pg.init()
screen = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption(TITLE)
clock = pg.time.Clock()

def start_screen():           #sets up initial level layout/ start screen
    base_plat = Platform()      #create a base platform
    base_group.add(base_plat)
    platforms.add(base_plat)
    base_plat.surf = pg.Surface((WIDTH, 20))
    base_plat.surf.fill((RED))
    base_plat.rect = base_plat.surf.get_rect(center = (WIDTH/2, HEIGHT - 10))
    base_plat.point = False

    for x in range(random.randint(9, 10)):    #create start set-up of random platforms
        collide = True
        while collide:
            rando = random.randrange(0,100)
            if rando < 40:
                plat  = Platform()
            elif rando < 70:
                plat = Bouncy_Platform()
            else:
                plat = Speedy_Platform()
            collide = check(plat, platforms)
        platforms.add(plat)
        if rando < 70:
            bouncy_platforms.add(plat)
        elif rando >= 70:
            speedy_platforms.add(plat)

def blits():            #blitting onto the screen
    style = pg.font.SysFont("lucidasans", 20)
    high_score = style.render(str(player.score), True, (RED))
    screen.blit(sky_img, (0 , 0))
    screen.blit(high_score, (WIDTH/2, 10))

    for platform in platforms:
        screen.blit(platform.surf, platform.rect)
    screen.blit(player.image, player.rect)
    player.move()

def game_over():            #game over events when player falls off screen
    player.kill()
    pg.mixer.music.stop()
    end_font = pg.font.SysFont("comicsansms", 100)
    end_screen = end_font.render("Game Over", False, BLACK)
    screen.blit(end_screen, (WIDTH/2 - 200, 200))
    pg.display.flip()

pg.mixer.music.load('bounce.mp3')
pg.mixer.music.play(-1)
start_screen()
run = True
while run:                  #game loop to run the game and its mechanics
    clock.tick(FPS)
    player.update()
    key = pg.key.get_pressed()
    if key[K_ESCAPE]:
        event.type = QUIT
    for event in pg.event.get():
        if event.type == QUIT:
            pg.quit()
            sys.exit()
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_SPACE:
                player.jump()
        if event.type == pg.KEYUP:
            if event.key == pg.K_SPACE:
                player.stop_jump()

    if player.rect.top < HEIGHT:
        player.auto_scroll()

    player.scroll()
    plat_create()
    blits()

    if player.rect.top > HEIGHT:
        game_over()
    else:
        pg.display.update()
