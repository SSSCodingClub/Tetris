from setup import *
from game import Game
from screens import Title, GameOver

delta: int = 1000 / fps
is_running: bool = True

scenes = {
    "Title": Title,
    "Game": Game,
    "GameOver": GameOver
}

scene = Title()

while is_running:
    if pygame.event.peek(pygame.QUIT):
        is_running = False

    scene.update(delta)
    scene.draw(screen)

    if scene.next_scene is not None:
        if scene.next_scene == "GameOver" and isinstance(scene, Game):
            scene = scenes[scene.next_scene](scene.score)
        else:
            scene = scenes[scene.next_scene]()

    pygame.display.update()
    delta = clock.tick(fps)

pygame.quit()
