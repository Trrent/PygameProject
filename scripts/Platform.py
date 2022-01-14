import pygame
from spriteGroups import all_sprites, platforms


class Platform(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y, image, group):
        super().__init__(group)
        self.image = pygame.transform.scale(image, (40, 40))
        self.rect = self.image.get_rect()
        self.rect.x = pos_x 
        self.rect.y = pos_y
        self.mask = pygame.mask.from_surface(self.image)