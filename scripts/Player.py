import pygame
from Main import all_sprites, platforms, load_image


class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y, image):
        super().__init__(all_sprites)
        self.image = image # картинку потом приделаем
        self.rect = self.image.get_rect()
        self.rect.x = pos_x 
        self.rect.y = pos_y
        self.mask = pygame.mask.from_surface(self.image)
        self.vx, self.vy = 0, 0 # скорость по x и по y
        self.grounded = False
    
    def move(self, direction):
        if not self.grounded:
            return
        if direction == "RIGHT":
            self.vx += 20
            if self.vx > 100:
                self.vx = 100 # максимальная скорость героя
        if direction == "LEFT":
            self.vx -= 20
            if self.vx < -100:
                self.vx = -100
    
    def jump(self):
        if self.grounded:
            self.vy -= 100
            self.grounded = False
    
    def update(self):
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
        

