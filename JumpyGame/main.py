import pygame as pg
from pygame.locals import *
import sys
import random
from settings import*
from mechanics import*


class Game():
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()

    def start_screen(self):
        base_plat.surf = pg.Surface((WIDTH, 20))        #create a base platform
        base_plat.surf.fill((RED))
        base_plat.rect = base_plat.surf.get_rect(center = (WIDTH/2, HEIGHT - 10))
        base_plat.point = False

        for x in range(random.randint(8,9)):    #create start set-up of random platforms
            collide = True
        while collide:
            rando = random.randrange(1,101)
            if rando < 50:
                plat  = Bouncy_Platform()
            else:
                plat = Platform()
            collide = check(plat, platforms)
        platforms.add(plat)
        if rando < 50:
            bouncy_platforms.add(plat)

    def run(self):
        self.playing = True
        while self.playing:
            self.clock.tick(FPS)
            self.events()
            self.updates()
            pg.display.update()

    def events(self):
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

    def updates(self):
        plat_create()
        player.scroll()
        if player.rect.top > HEIGHT:        #Game Over --> create screen
            player.kill()
            #end_font = pg.font.SysFont("lucidasans", 100)
            #end_screen = end_font.render("Game Over", False, RED, BLACK)
            #screen.blit(end_screen, (WIDTH/2 - 200, 200))
            pg.display.update()

        if player.rect.top < HEIGHT:
            player.auto_scroll()
        pg.display.update()

    def blits(self):
        style = pg.font.SysFont("lucidasans", 20)
        high_score = style.render(str(player.score), True, (RED))
        self.screen.blit(sky_img, (0 , 0))
        self.screen.blit(high_score, (WIDTH/2, 10))

        for entity in platforms:
            self.screen.blit(entity.surf, entity.rect)
            entity.move()
        self.screen.blit(player.image, player.rect)
        player.move()

    def game_over(self):
        player.kill()
        end_font = pg.font.SysFont("lucidasans", 100)
        end_screen = end_font.render("Game Over", False, RED)
        self.screen.blit(end_screen, (WIDTH/2 - 200, 200))
        pg.display.flip()

game = Game()
while True:
    game.start_screen()
    game.blits()
    game.run()
