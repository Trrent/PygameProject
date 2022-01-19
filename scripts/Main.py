import sys
import pytmx
from Parameters import *
import pygame
from Platform import Platform
from spriteGroups import buttons, all_sprites
from pathlib import Path

screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
clock = pygame.time.Clock()
PATH_HEAD = Path(__file__).parent.parent
PATH_DATA = Path(PATH_HEAD, 'data')


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


def load_sound(name):
    filename = Path(PATH_DATA, 'sounds', name)
    if not filename.is_file():
        print(f"Файл '{name}' не найден")
        terminate()
    return pygame.mixer.Sound(filename)


def load_music(name, music):
    filename = Path(PATH_DATA, 'sounds', name)
    if not filename.is_file():
        print(f"Файл '{name}' не найден")
        terminate()
    music.load(filename)
    music.set_volume(0.1)
    return music


def load_level(level):
    filename = Path(PATH_DATA, 'levels', f"{level}.tmx")
    if not filename.is_file():
        print(f"Файл '{level}.tmx' не найден")
        terminate()
    map = pytmx.load_pygame(filename)
    h, w = map.height, map.width
    tileW, tileH = map.tilewidth, map.tileheight
    x, y = None, None
    for y in range(h):
        for x in range(w):
            image = map.get_tile_image(x, y, 0)
            if image:
                Platform(x * tileW, y * tileH, image)
    return 2 * tileW, 9 * tileH  # координаты игрока, на всех уровнях спавнится в одном месте


def load_font(font_size, font_type='Comic_CAT.otf'):  # Создание шрифта для текста
    font_path = Path(PATH_DATA, 'fonts', font_type)
    return pygame.font.Font(font_path, font_size)


def printText(message, pos_x, pos_y, font_size=30, color='black', surface=screen):  # Вывод текста
    font = load_font(font_size=font_size)
    string_rendered = font.render(message, True, pygame.Color(color))
    intro_rect = string_rendered.get_rect()
    intro_rect.top = pos_y
    intro_rect.x = pos_x
    surface.blit(string_rendered, intro_rect)


sound1 = load_sound('b1.mp3')
sound1.set_volume(0.2)


class Button(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y, action, inactive_image, active_image=None, group=buttons, locked=False):
        super().__init__(group)
        self.image = inactive_image.copy()
        self.active_image = active_image
        self.action = action
        self.locked = locked
        self.inactive_image = inactive_image

        self.locker = load_image('lock.png')
        if locked:
            self.image.blit(self.locker, (0, 0))

        self.rect = self.image.get_rect()
        self.rect.x = pos_x
        self.rect.y = pos_y

    def is_pressed(self):
        mouse = pygame.mouse.get_pos()
        if not self.locked:
            click = pygame.mouse.get_pressed()
            if self.rect.collidepoint(mouse):
                if click[0]:
                    sound1.play()
                    return True
            return False

    def update(self):
        if not self.locked:
            self.image = self.inactive_image
            mouse = pygame.mouse.get_pos()
            if self.rect.collidepoint(mouse):
                if self.active_image is not None:
                    self.image = self.active_image
            else:
                self.image = self.inactive_image


def terminate():
    pygame.quit()
    sys.exit()
