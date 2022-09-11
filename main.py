from setup import *
from game import Game

delta: int = 1000/fps
is_running: bool = True


scene: Game = Game()

while is_running:
    if pygame.event.peek(pygame.QUIT):
        is_running = False

    scene.update(delta)
    scene.draw(screen)

    pygame.display.update()
    delta = clock.tick(fps)

pygame.quit()
