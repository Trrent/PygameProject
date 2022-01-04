import pygame

from Main import *
from Physics import Point, RIGHT, LEFT, UP, DOWN, distance
from characters import ExampleEnemy

enemy = ExampleEnemy(Point(width // 2, height // 3), load_image("creature.png"), jump_height=150)
all_sprites.add(enemy)
print("НачПоз: ", enemy.pos)
while True:
    screen.fill((0, 0, 0))
    all_sprites.draw(screen)
    all_sprites.update()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and enemy.grounded:
                enemy.jumped = True
            if event.key == pygame.K_LEFT:
                enemy.move(LEFT * enemy.vel)
            if event.key == pygame.K_RIGHT:
                enemy.move(RIGHT * enemy.vel)
    pygame.display.flip()
    clock.tick(FPS)
    if enemy.pos.pg_y >= height - 150:
        enemy.grounded = True
    else:
        enemy.grounded = False

    if 0 < distance(Point(0, enemy.pos.pg_y), Point(0, height - 150)) <= 1:
        enemy.move_to(Point(enemy.pos.x, height - 150), immediately=True)
