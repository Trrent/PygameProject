import pygame
from Main import all_sprites, platforms, enemies
from Player import player


class Enemy(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y, image):
        super().__init__(all_sprites, enemies)
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = pos_x 
        self.rect.y = pos_y
        self.mask = pygame.mask.from_surface(self.image)
        self.vx, self.vy = 0, 0 # скорость по x и по y
        self.grounded = False
    
    def behaviour(self):
        # TODO Искусственный интеллект врагов
        x, y = self.rect.x, self.rect.y
        px, py = player.rect.x, player.rect.y
    
    def update(self):
        self.behaviour() # Поведение 
        self.rect.x += self.vx
        self.rect.y += self.vy
        collides = pygame.sprite.spritecollide(self, platforms, False)
        for p in collides: 
            if self.vx > 0:
                self.rect.right = p.rect.left
            if self.vx < 0:
                self.rect.left = p.rect.right
            if self.vy > 0:
                self.rect.bottom = p.rect.top
                self.grounded = True
                self.vy = 0
            if self.vy < 0:
                self.rect.top = p.rect.bottom
                self.vy = 0
        if not self.grounded: # применяем ускорение свободного падения
            self.vy += 49 / 60 # 5g / 60
