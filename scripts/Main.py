import sys
import os
import pygame
from Platform import Platform


screen = pygame.display.set_mode((1920, 1020), pygame.RESIZABLE)
clock = pygame.time.Clock()

levels = [
    [
        "#########################################################################################################################",
        "..................######################.............##########................############......................########",
        "#######..............................................###############.........######.....................#################",
        "@.................######################.................................................................................",
        "#######################################################################################.....#############################"
]]

def load_image(name, colorkey=None):
    fullname = os.path.join('sprites', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    if colorkey is not None:
        image = image.convert()
    if colorkey == -1:
        colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image

def load_level(level):
    px, py = None, None
    x, y = None, None
    levelMap = levels[level]
    for y in range(len(levelMap)):
        for x in range(len(levelMap[y])):
            if levelMap[y][x] == '#':
                Platform(50 * x, 50 * y, load_image("grass.png"))
            elif levelMap[y][x] == '@':
                px, py = 50 * x, 50 * y
    return px, py
