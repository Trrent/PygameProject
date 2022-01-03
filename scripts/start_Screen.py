from Main import *


def start_screen():
    button = Button(100, 50, (50, 50, 50), (150, 150, 150))

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
        button.draw(100, 100, 'Exit', terminate)
        pygame.display.flip()
        clock.tick(FPS)




