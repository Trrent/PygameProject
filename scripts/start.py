from Player import player
from Platform import Platform
from Enemy import Enemy
from Main import *


while True:
    screen.fill((0, 0, 0))
    all_sprites.draw(screen)
    all_sprites.update()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    pygame.display.flip()
    clock.tick(FPS)