import pygame
from Physics import Point
from spriteGroups import all_sprites, platforms


class Platform(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y, image):
        super().__init__(all_sprites, platforms)
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = pos_x 
        self.rect.y = pos_y
        self.mask = pygame.mask.from_surface(self.image)
        self.pos = Point(pos_x, pos_y) # заглушка