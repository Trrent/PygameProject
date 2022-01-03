from Player import player
from Platform import Platform
from Enemy import Enemy
from Main import *
from Camera import Camera
from spriteGroups import all_sprites

def start_screen():
    pass

def death_screen():
    pass

def start():
    camera = Camera()
    player.rect.x, player.rect.y = load_level(0)
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
        clock.tick(60)

if __name__ == '__main__':
    pygame.display.set_caption('Revenge underground')
    start()
