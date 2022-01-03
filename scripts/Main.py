import sys
import os
import pygame
from Platform import Platform
from pathlib import Path

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

def load_font(font_type='Comic_CAT.otf', font_size=30):  # Создание шрифта для текста
    font_path = Path(Path(__file__).parent.parent, 'data', font_type)
    return pygame.font.Font(font_path, font_size)


def printText(message, pos_x, pos_y):  # Вывод текста
    font = load_font(font_size=40)
    string_rendered = font.render(message, True, pygame.Color('black'))
    intro_rect = string_rendered.get_rect()
    text_coord = pos_y + 10
    intro_rect.top = text_coord
    intro_rect.x = pos_x + 10
    text_coord += intro_rect.height
    screen.blit(string_rendered, intro_rect)


class Button:
    def __init__(self, width, height, inactive_color, active_color):
        self.width = width
        self.height = height
        self.inactive_color = inactive_color
        self.active_color = active_color

    def draw(self, pos_x, pos_y, message, action=None):
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        if pos_x < mouse[0] < pos_x + self.width and pos_y < mouse[1] < pos_y + self.height:
            pygame.draw.rect(screen, self.active_color, (pos_x, pos_y, self.width, self.height))

            if click[0] == 1 and action is not None:
                action()

        else:
            pygame.draw.rect(screen, self.inactive_color, (pos_x, pos_y, self.width, self.height))
        printText(message, pos_x, pos_y)


def terminate():
    pygame.quit()
    sys.exit()
