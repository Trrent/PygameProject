from Player import player
from Platform import Platform
from Enemy import Enemy
from Main import *
from Camera import Camera
from spriteGroups import all_sprites, buttons


def start_screen():
    # bg = pygame.transform.scale(load_image('fon.jpg'), (WIDTH, HEIGHT))
    startBtnImage = load_image('start_btn.png')
    startBtnPressedImage = load_image('start_btn_pressed.png')
    exitBtnImage = load_image('exit_btn.png')
    exitBtnPressedImage = load_image('exit_btn_pressed.png')
    Button(760, 200, level_screen, startBtnImage, active_image=startBtnPressedImage)
    Button(960, 200, terminate, exitBtnImage, active_image=exitBtnPressedImage)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
        buttons.update()
        buttons.draw(screen)
        pygame.display.flip()
        clock.tick(FPS)


def level_screen():
    # bg = pygame.transform.scale(load_image('fon.jpg'), (WIDTH, HEIGHT))
    buttons.empty()
    screen.fill((0, 0, 0))
    levelBtnImage = load_image('level1_btn.png')
    levelBtnPressedImage = load_image('level1_btn_pressed.png')
    Button(450, 300, lambda lvl = 1: start(lvl), levelBtnImage, active_image=levelBtnPressedImage)
    Button(600, 300, lambda lvl = 2: start(lvl), levelBtnImage, active_image=levelBtnPressedImage)
    Button(750, 300, lambda lvl = 3: start(lvl), levelBtnImage, active_image=levelBtnPressedImage)
    Button(900, 300, lambda lvl = 4: start(lvl), levelBtnImage, active_image=levelBtnPressedImage)
    Button(1050, 300, lambda lvl = 5: start(lvl), levelBtnImage, active_image=levelBtnPressedImage)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
        buttons.update()
        buttons.draw(screen)
        pygame.display.flip()
        clock.tick(FPS)


def death_screen():
    pass


def start(level):
    camera = Camera()
    player.rect.x, player.rect.y = load_level(level)
    while True:
        screen.fill((0, 0, 0))
        all_sprites.draw(screen)
        all_sprites.update()
        camera.update(player)
        for sprite in all_sprites:
            camera.apply(sprite)
        if player.hp <= 0:
            death_screen()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:
                    player.jump()
                if event.key == pygame.K_d:
                    player.move("RIGHT")
                if event.key == pygame.K_a:
                    player.move("LEFT")
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_d and player.vx > 0:
                    player.stop()
                if event.key == pygame.K_a and player.vx < 0:
                    player.stop()
        pygame.display.flip()
        clock.tick(FPS)


if __name__ == '__main__':
    pygame.display.set_caption('Revenge underground')
    start_screen()
