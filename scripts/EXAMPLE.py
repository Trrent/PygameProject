import pygame

from Main import *
from Physics import Point, RIGHT, LEFT, UP, DOWN, distance
from characters import ExampleController

hero = ExampleController(Point(width // 2, height // 3), load_image("creature.png"), jump_height=150)
all_sprites.add(hero)
print("НачПоз: ", hero.pos)
while True:
    screen.fill((0, 0, 0))
    all_sprites.draw(screen)
    all_sprites.update()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and hero.grounded:
                hero.jumped = True
            if event.key == pygame.K_LEFT:
                hero.move(LEFT * hero.vel)
            if event.key == pygame.K_RIGHT:
                hero.move(RIGHT * hero.vel)
    pygame.display.flip()
    clock.tick(FPS)
    if hero.pos.pg_y >= height - 150:
        hero.grounded = True
    else:
        hero.grounded = False

    if 0 < distance(Point(0, hero.pos.pg_y), Point(0, height - 150)) <= 1:
        hero.move_to(Point(hero.pos.x, height - 150), immediately=True)
