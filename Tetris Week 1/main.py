from setup import *
from game import Game

is_running = True

scene = Game()

while is_running:
    screen.fill((0, 0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            is_running = False

    scene.update()
    scene.draw(screen)

    pygame.display.update()

pygame.quit()
