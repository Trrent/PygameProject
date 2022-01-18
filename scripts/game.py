import pygame
import Physics
from pygame.sprite import spritecollide
from Main import *
from Camera import Camera
from spriteGroups import all_sprites, platforms, enemies

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
backBtnImage = load_image('back_btn.png')
backBtnPressedImage = load_image('back_btn_pressed.png')
mixer = pygame.mixer.music


class StartScreen:
    def __init__(self):
        self.bg = pygame.transform.scale(load_image('Background/bg1.jpg'), (WIDTH, HEIGHT))
        self.buttons = pygame.sprite.Group()
        self.levelScreen = LevelScreen()
        Button(WIDTH // 2 - 150, HEIGHT // 2 - 300, self.levelScreen.show, startBtnImage, active_image=startBtnPressedImage, group=self.buttons)
        Button(WIDTH // 2 + 50, HEIGHT // 2 - 300, terminate, exitBtnImage, active_image=exitBtnPressedImage, group=self.buttons)

    def show(self, playMusic=True):
        if playMusic:
            music = load_music(f'menu.mp3', mixer)
            music.play(-1)
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
        self.bg = pygame.transform.scale(load_image('Background/bg1.jpg'), (WIDTH, HEIGHT))
        self.buttons = pygame.sprite.Group()

        Button(WIDTH // 2 - 350, HEIGHT // 2 - 100, 1, levelBtnImage, active_image=levelBtnPressedImage, group=self.buttons)
        Button(WIDTH // 2 - 200, HEIGHT // 2 - 100, 2, levelBtnImage, active_image=levelBtnPressedImage, group=self.buttons)
        Button(WIDTH // 2 - 50, HEIGHT // 2 - 100, 3, levelBtnImage, active_image=levelBtnPressedImage, group=self.buttons)
        Button(50, 50, 0, backBtnImage, active_image=backBtnPressedImage, group=self.buttons)

    def show(self):
        while True:
            self.buttons.update()
            self.buttons.draw(self.bg)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    terminate()
            for b in self.buttons:
                if b.is_pressed():
                    if b.action == 0:
                        return start_screen.show(playMusic=False)
                    else:
                        level = StartLevel(b.action)
                        return level.run()
            screen.blit(self.bg, (0, 0))
            pygame.display.flip()
            clock.tick(FPS)


class StartLevel:
    def __init__(self, level):
        self.image = pygame.Surface((WIDTH, HEIGHT))
        self.bg = pygame.transform.scale(load_image(f"Background/Background{level}.png"), (WIDTH, HEIGHT))
        self.camera = Camera()
        self.buttons = pygame.sprite.Group()
        self.ui = pygame.sprite.Group()
        self.pauseScreen = PauseScreen(self)
        self.deathScreen = DeathScreen(self)
        self.level = level
        all_sprites.empty()
        platforms.empty()
        enemies.empty()
        px, py = load_level(level)
        self.player = Player(px, py)
        self.playerGlobalX = px # насколько player удалён от координаты x = 0
        self.playerGlobalY = py # насколько player удалён от координаты y = 0
        self.camera.update(self.player)
        for sprite in all_sprites:
            self.camera.apply(sprite)
        self.player.end_pos = Physics.Point(self.player.rect.x, self.player.rect.x)
        self.hpBar = HealthBar(self.player, group=self.ui)
        Button(WIDTH - WIDTH // 10, HEIGHT // 20, self.pauseScreen.show, pauseBtnImage,
               active_image=pauseBtnPressedImage, group=[self.buttons, self.ui])
        music = load_music(f'{level}.mp3', mixer)
        music.play(-1)

    def run(self):
        iterations = 0
        while True:
            self.image.blit(self.bg, (0, 0))
            all_sprites.draw(self.image)
            all_sprites.update()
            self.ui.draw(self.image)
            self.ui.update()

            if iterations == 5:
                self.player.updateFrame()
                iterations = 0

            for b in self.buttons:
                if b.is_pressed():
                    b.action()
            self.camera.update(self.player)
            self.playerGlobalX -= self.camera.dx
            self.playerGlobalY -= self.camera.dy
            for sprite in all_sprites:
                self.camera.apply(sprite)
            if self.player.hp <= 0:
                return self.deathScreen.show()
            if self.playerGlobalX >= 23000:
                self.pauseScreen.show()
                # нужен экран окончания уровня с возможностью перехода на следующий
            if self.playerGlobalY > HEIGHT * 1.1:
                self.player.hp = 0

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    terminate()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_w or event.key == pygame.K_SPACE:
                        self.player.jump()
                        self.player.jumped = True
                    if event.key == pygame.K_d:
                        self.player.move("RIGHT")
                    if event.key == pygame.K_a:
                        self.player.move("LEFT")
                    if event.key == pygame.K_ESCAPE:
                        self.pauseScreen.show()
                    if event.key == pygame.K_k:
                        self.player.attack()
                elif event.type == pygame.KEYUP:
                    if event.key == pygame.K_d and self.player.vx > 0:
                        self.player.stop()
                    if event.key == pygame.K_a and self.player.vx < 0:
                        self.player.stop()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        self.player.attack()
            iterations += 1
            screen.blit(self.image, (0, 0))
            pygame.display.flip()
            clock.tick(FPS)


class DeathScreen:
    def __init__(self, lvl):
        self.image = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        self.image.fill((255, 255, 255, 128))
        self.buttons = pygame.sprite.Group()
        self.level = lvl
        Button(WIDTH // 2 - 150, HEIGHT // 2 - 100, self.retryAction, retryBtnImage, active_image=retryBtnPressedImage, group=self.buttons)
        Button(WIDTH // 2 + 50, HEIGHT // 2 - 100, start_screen.show, homeBtnImage, active_image=homeBtnPressedImage, group=self.buttons)

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
        level = StartLevel(self.level.level)
        del self.level
        level.run()


class PauseScreen:
    def __init__(self, lvl):
        self.image = pygame.Surface((WIDTH // 2, HEIGHT // 2), pygame.SRCALPHA)
        width, height = WIDTH // 2, HEIGHT // 2
        self.image.fill((255, 255, 255, 200))
        self.buttons = pygame.sprite.Group()
        self.level = lvl
        Button(width - 200, height - 50, None, startBtnImage, active_image=startBtnPressedImage, group=self.buttons)
        Button(width - 50, height - 50, self.retryAction, retryBtnImage, active_image=retryBtnPressedImage, group=self.buttons)
        Button(width + 100, height - 50, start_screen.show, homeBtnImage, active_image=homeBtnPressedImage, group=self.buttons)

    def show(self):
        mixer.pause()
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
                    return mixer.unpause()
            pygame.display.flip()
            clock.tick(FPS)

    def retryAction(self):
        level = StartLevel(self.level.level)
        del self.level
        level.run()


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


class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(all_sprites)
        self.frames = {'Attack1Right': (4, 1, []), 'Attack1Left': (4, 1, []), 'Attack': (4, 1, []),
                       'DeathRight': (9, 1, []), 'FallRight': (6, 1, []),  'FallLeft': (6, 1, []),
                       'HitRight': (3, 1, []), 'IdleRight': (6, 1, []), 'IdleLeft': (6, 1, []),
                       'JumpRight': (6, 1, []),  'JumpLeft': (6, 1, []), 'RunRight': (8, 1, []), 'RunLeft': (8, 1, [])}
        self.cut_sheet()
        self.direction = True
        self.current_frames = self.frames['FallRight'][2]
        self.cur_frame = 0
        self.image = self.current_frames[self.cur_frame]
        self.rect = self.image.get_rect()
        self.rect.x = pos_x
        self.rect.y = pos_y
        self.mask = pygame.mask.from_surface(self.image)
        self.vx, self.vy = 0, 0  # скорость по x и по y
        self.grounded = False
        self.hp = 100
        self.damage = 20
        self.attacking = False

    def cut_sheet(self):
        for name, (columns, rows, frames) in self.frames.items():
            sheet = load_image(f"Hero/{name}.png")
            self.rect = pygame.Rect(0, 0, sheet.get_width() // columns, sheet.get_height() // rows)
            for j in range(rows):
                for i in range(columns):
                    frame_location = (self.rect.w * i, self.rect.h * j)
                    frames.append(sheet.subsurface(pygame.Rect(frame_location, self.rect.size)))

    def move(self, direction):
        if direction == "RIGHT":
            self.vx = 5
            self.direction = True
        if direction == "LEFT":
            self.vx = -5
            self.direction = False

    def jump(self):
        if self.grounded:
            self.vy -= 15
            self.grounded = False
            self.changeFrames('JumpRight' if self.direction else 'JumpLeft')

    def attack(self):
        if self.attacking:
            return
        self.rect.x += 110
        if pygame.sprite.spritecollideany(self, platforms):
            self.rect.x -= 110
            return
        self.rect.x -= 110
        self.attacking = True
        for sprite in spritecollide(self, enemies, False):
            sprite.health -= self.damage

    def changeFrames(self, key):
        if self.frames[key][2] != self.current_frames:
            self.current_frames = self.frames[key][2]
            self.cur_frame = 0

    def updateFrame(self):
        self.cur_frame = (self.cur_frame + 1) % len(self.current_frames)
        if self.cur_frame == 0 and self.attacking:
            self.attacking = False
        self.image = self.current_frames[self.cur_frame]

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
        if self.attacking:
            self.changeFrames('Attack')
        elif self.vy == 0 and self.vx == 0:
            self.changeFrames('IdleRight' if self.direction else 'IdleLeft')
        elif self.vy == 0 and self.vx != 0:
            self.changeFrames('RunRight' if self.direction else 'RunLeft')
        self.checkGrounded()
        if not self.grounded:
            self.vy += 0.81  # 5g / 60
            self.changeFrames('FallRight' if self.direction else 'FallLeft')

    def checkGrounded(self):
        self.rect.y += 1
        self.grounded = pygame.sprite.spritecollideany(self, platforms)
        self.rect.y -= 1

    def stop(self):
        self.vx = 0
        self.changeFrames('IdleRight' if self.direction else 'IdleLeft')


if __name__ == '__main__':
    pygame.display.set_caption('Knight Adventures')
    start_screen = StartScreen()
    start_screen.show()