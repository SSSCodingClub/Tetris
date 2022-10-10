from setup import *
from game import Game
from screens import Title

delta: int = 1000 / fps
is_running: bool = True

scenes = {
    "Title": Title,
    "Game": Game
}

scene = Title()

while is_running:
    if pygame.event.peek(pygame.QUIT):
        is_running = False

    scene.update(delta)
    scene.draw(screen)

    if scene.next_scene is not None:
        scene = scenes[scene.next_scene]()

    pygame.display.update()
    delta = clock.tick(fps)

pygame.quit()
