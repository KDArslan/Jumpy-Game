import pygame as pg
from os import path

# define some colors (R, G, B)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
LIGHTGREY = (100, 100, 100)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# constants
TITLE = "Jumpy Game"
HEIGHT = 600
WIDTH = 900
ACC = 0.8
SLOWING = -0.14
FPS = 60

#loading images
game_folder = path.dirname(__file__)
img_folder = path.join(game_folder, "img")

    #background sky
sky_img = pg.image.load(path.join(img_folder, "sky.jpg"))
sky_img = pg.transform.scale(sky_img, (900, 900))

    #player images
player_img_stand = pg.image.load(path.join(img_folder, "player_img_down.png"))
player_img_stand = pg.transform.scale(player_img_stand, (40, 40))
player_img_left = pg.image.load(path.join(img_folder, "player_img_left.png"))
player_img_left = pg.transform.scale(player_img_left, (40, 40))
player_img_right = pg.image.load(path.join(img_folder, "player_img_right.png"))
player_img_right = pg.transform.scale(player_img_right, (40, 40))
