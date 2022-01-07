import pygame

# from Player import Player, HealthBar
from Platform import Platform
# from Enemy import Enemy
from Main import *
from Camera import Camera
from spriteGroups import all_sprites, buttons, platforms, enemies

retryBtnImage = load_image('retry_btn.png')
retryBtnPressedImage = load_image('retry_btn_pressed.png')
homeBtnImage = load_image('home_btn.png')
homeBtnPressedImage = load_image('home_btn_pressed.png')
startBtnImage = load_image('start_btn.png')
startBtnPressedImage = load_image('start_btn_pressed.png')
exitBtnImage = load_image('exit_btn.png')
exitBtnPressedImage = load_image('exit_btn_pressed.png')
levelBtnImage = load_image('level1_btn.png')
levelBtnPressedImage = load_image('level1_btn_pressed.png')
pauseBtnImage = load_image('pause_btn.png')
pauseBtnPressedImage = load_image('pause_btn_pressed.png')


class StartScreen:
    def __init__(self):
        self.bg = pygame.transform.scale(load_image('bg.jpg'), (WIDTH, HEIGHT))
        self.buttons = pygame.sprite.Group()
        self.levelScreen = LevelScreen()
        Button(760, 200, self.levelScreen.show, startBtnImage, active_image=startBtnPressedImage, group=self.buttons)
        Button(960, 200, terminate, exitBtnImage, active_image=exitBtnPressedImage, group=self.buttons)

    def show(self):
        while True:
            self.buttons.update()
            self.buttons.draw(self.bg)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    terminate()
            for b in self.buttons:
                if b.is_pressed():
                    return b.action()
            screen.blit(self.bg, (0, 0))
            pygame.display.flip()
            clock.tick(FPS)


class LevelScreen:
    def __init__(self):
        self.bg = pygame.transform.scale(load_image('bg.jpg'), (WIDTH, HEIGHT))
        self.buttons = pygame.sprite.Group()

        Button(450, 300, 1, levelBtnImage, active_image=levelBtnPressedImage, group=self.buttons)
        Button(600, 300, 2, levelBtnImage, active_image=levelBtnPressedImage, group=self.buttons)
        Button(750, 300, 3, levelBtnImage, active_image=levelBtnPressedImage, group=self.buttons)
        Button(900, 300, 4, levelBtnImage, active_image=levelBtnPressedImage, group=self.buttons)
        Button(1050, 300, 5, levelBtnImage, active_image=levelBtnPressedImage, group=self.buttons)

    def show(self):
        while True:
            self.buttons.update()
            self.buttons.draw(self.bg)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    terminate()
            for b in self.buttons:
                if b.is_pressed():
                    level = StartLevel(b.action)
                    return level.run()
            screen.blit(self.bg, (0, 0))
            pygame.display.flip()
            clock.tick(FPS)


class StartLevel:
    def __init__(self, level):
        self.image = pygame.Surface((WIDTH, HEIGHT))
        self.camera = Camera()
        self.platforms = pygame.sprite.Group()
        self.all_sprites = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        self.buttons = pygame.sprite.Group()
        self.ui = pygame.sprite.Group()
        self.pauseScreen = PauseScreen(level)
        self.deathScreen = DeathScreen(level)
        self.level = level
        px, py = load_level(level, [self.all_sprites, self.platforms])
        self.player = Player(px, py, load_image("player.png"), self)
        self.hpBar = HealthBar(self.player, group=self.ui)
        Button(1700, 40, self.pauseScreen.show, pauseBtnImage,
               active_image=pauseBtnPressedImage, group=[self.buttons, self.ui])

    def run(self):
        while True:
            self.image.fill((0, 50, 0))
            self.all_sprites.draw(self.image)
            self.all_sprites.update()
            self.ui.draw(self.image)
            self.ui.update()
            for b in self.buttons:
                if b.is_pressed():
                    b.action()
            self.camera.update(self.player)
            for sprite in self.all_sprites:
                self.camera.apply(sprite)
            if self.player.hp <= 0:
                return self.deathScreen.show()
            if self.player.rect.top > HEIGHT:
                self.player.hp = 0

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    terminate()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_w or event.key == pygame.K_SPACE:
                        self.player.jump()
                    if event.key == pygame.K_d:
                        self.player.move("RIGHT")
                    if event.key == pygame.K_a:
                        self.player.move("LEFT")
                    if event.key == pygame.K_ESCAPE:
                        self.pauseScreen.show()
                elif event.type == pygame.KEYUP:
                    if event.key == pygame.K_d and self.player.vx > 0:
                        self.player.stop()
                    if event.key == pygame.K_a and self.player.vx < 0:
                        self.player.stop()
            screen.blit(self.image, (0, 0))
            pygame.display.flip()
            clock.tick(FPS)


class DeathScreen:
    def __init__(self, lvl):
        self.image = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        self.image.fill((255, 255, 255, 128))
        self.buttons = pygame.sprite.Group()
        self.level = lvl
        Button(760, 400, self.retryAction, retryBtnImage, active_image=retryBtnPressedImage, group=self.buttons)
        Button(960, 400, start_screen.show, homeBtnImage, active_image=homeBtnPressedImage, group=self.buttons)

    def show(self):
        screen.blit(self.image, (0, 0))
        while True:
            self.buttons.update()
            self.buttons.draw(screen)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    terminate()
            for b in self.buttons:
                if b.is_pressed():
                    return b.action()
            pygame.display.flip()
            clock.tick(FPS)

    def retryAction(self):
        level = StartLevel(self.level)
        level.run()


class PauseScreen:
    def __init__(self, lvl):
        self.image = pygame.Surface((WIDTH // 2, HEIGHT // 2), pygame.SRCALPHA)
        self.image.fill((255, 255, 255, 200))
        self.buttons = pygame.sprite.Group()
        self.level = lvl
        Button(750, 450, None, startBtnImage, active_image=startBtnPressedImage, group=self.buttons)
        Button(900, 450, self.retryAction, retryBtnImage, active_image=retryBtnPressedImage, group=self.buttons)
        Button(1050, 450, start_screen.show, homeBtnImage, active_image=homeBtnPressedImage, group=self.buttons)

    def show(self):
        screen.blit(self.image, (WIDTH // 4, HEIGHT // 4))
        while True:
            self.buttons.update()
            self.buttons.draw(screen)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    terminate()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        return
            for b in self.buttons:
                if b.is_pressed():
                    if b.action is not None:
                        return b.action()
                    return
            pygame.display.flip()
            clock.tick(FPS)

    def retryAction(self):
        level = StartLevel(self.level)
        level.run()


class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y, image, level):
        super().__init__(level.all_sprites)
        self.parent = level
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
        collides = pygame.sprite.spritecollide(self, self.parent.platforms, False)
        for p in collides:
            if self.vy > 0 and self.vy != 0.81:
                self.rect.bottom = p.rect.top
                self.grounded = True
            if self.vy < 0:
                self.rect.top = p.rect.bottom
            self.vy = 0
        self.rect.x += self.vx
        collides = pygame.sprite.spritecollide(self, self.parent.platforms, False)
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
        self.grounded = pygame.sprite.spritecollideany(self, self.parent.platforms)
        self.rect.y -= 1

    def stop(self):
        self.vx = 0


class HealthBar(pygame.sprite.Sprite):
    def __init__(self, player, group):
        super().__init__(group)
        self.player = player
        # self.image = pygame.transform.scale(load_image('hp_bar.png'), (302, 120))
        self.image = pygame.Surface((315, 100))
        self.rect = self.image.get_rect()

        self.rect.x = 50
        self.rect.y = 30

    def update(self):
        self.image.fill((0, 0, 0))
        pygame.draw.line(self.image, pygame.Color('red'), (15, 50), (int(300 * self.player.hp / 100), 50), width=50)


if __name__ == '__main__':
    pygame.display.set_caption('Revenge underground')
    start_screen = StartScreen()
    start_screen.show()