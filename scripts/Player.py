import pygame
from spriteGroups import all_sprites, platforms
from Main import load_image


class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y, image):
        super().__init__(all_sprites)
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = pos_x
        self.rect.y = pos_y
        self.mask = pygame.mask.from_surface(self.image)
        self.vx, self.vy = 0, 0  # скорость по x и по y
        self.grounded = False
        self.hp = 100

    def move(self, direction):
        if direction == "RIGHT":
            self.vx = 3
        if direction == "LEFT":
            self.vx = -3

    def jump(self):
        if self.grounded:
            self.vy -= 10
            self.grounded = False

    def update(self):
        self.rect.y += self.vy
        collides = pygame.sprite.spritecollide(self, platforms, False)
        for p in collides:
            if self.vy > 0 and self.vy != 0.81:
                self.rect.bottom = p.rect.top
                self.grounded = True
            if self.vy < 0:
                self.rect.top = p.rect.bottom
            self.vy = 0
        self.rect.x += self.vx
        collides = pygame.sprite.spritecollide(self, platforms, False)
        for p in collides:
            if self.vx > 0:
                self.rect.right = p.rect.left
            if self.vx < 0:
                self.rect.left = p.rect.right
            self.vx = 0
        self.checkGrounded()
        if not self.grounded:
            self.vy += 0.81  # 5g / 60

    def checkGrounded(self):
        self.rect.y += 1
        self.grounded = pygame.sprite.spritecollideany(self, platforms)
        self.rect.y -= 1

    def stop(self):
        self.vx = 0


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


# player = Player(100, 100, load_image("player.png"))
# hpBar = HealthBar(player)
