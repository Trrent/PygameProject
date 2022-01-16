import sys
import os
from Parameters import *
import pygame
from Platform import Platform
from spriteGroups import buttons, all_sprites
from pathlib import Path


screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
clock = pygame.time.Clock()
PATH_HEAD = Path(__file__).parent.parent
PATH_DATA = Path(PATH_HEAD, 'data')


# levels = [
#     [
#         "#########################################################################################################################",
#         "..................######################.............##########................############......................########",
#         "#######..............................................###############.........######.....................#################",
#         "@.................######################.................................................................................",
#         "#######################################################################################.....#############################"
# ]]

def load_image(name, colorkey=None):
    filename = Path(PATH_DATA, 'sprites', name)
    if not filename.is_file():
        print(f"Файл с изображением '{name}' не найден")
        terminate()
    image = pygame.image.load(filename)
    if colorkey is not None:
        image = image.convert()
    if colorkey == -1:
        colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


def load_level(level, group):
    filename = Path(PATH_DATA, 'levels', f"level_{level}.txt")
    if not filename.is_file():
        print(f"Файл 'level_{level}.txt' не найден")
        terminate()
    with open(filename, 'r') as mapFile:
        levelMap = [line.strip() for line in mapFile]
    px, py = None, None
    x, y = None, None
    for y in range(len(levelMap)):
        for x in range(len(levelMap[y])):
            if levelMap[y][x] == '#':
                Platform(50 * x, 50 * y + 300, load_image("grass.png"))
            elif levelMap[y][x] == '@':
                px, py = 50 * x, 50 * y + 300
    return px, py


def load_font(font_size, font_type='Comic_CAT.otf'):  # Создание шрифта для текста
    font_path = Path(PATH_DATA, 'fonts', font_type)
    return pygame.font.Font(font_path, font_size)


def printText(message, pos_x, pos_y, font_size=30, color='black'):  # Вывод текста
    font = load_font(font_size=font_size)
    string_rendered = font.render(message, True, pygame.Color(color))
    intro_rect = string_rendered.get_rect()
    intro_rect.top = pos_y
    intro_rect.x = pos_x
    screen.blit(string_rendered, intro_rect)


class Button(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y, action, inactive_image, active_image=None, group=buttons, width=0, height=0):
        super().__init__(group)
        self.image = inactive_image
        self.active_image = active_image
        self.action = action
        self.inactive_image = inactive_image
        self.rect = self.image.get_rect()
        self.rect.x = pos_x
        self.rect.y = pos_y

    def is_pressed(self):
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        if self.rect.collidepoint(mouse):
            if click[0]:
                return True
        return False

    def update(self):
        mouse = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse):
            if self.active_image is not None:
                self.image = self.active_image
        else:
            self.image = self.inactive_image


class HealthBar(pygame.sprite.Sprite):
    def __init__(self, player, group=all_sprites):
        super().__init__(group)
        self.player = player
        self.image = pygame.transform.scale(load_image('hp_bar.png'), (102, 40))
        self.rect = self.image.get_rect()

        self.rect.x = -300
        self.rect.y = 30

    def update(self):
        pass


def terminate():
    pygame.quit()
    sys.exit()
