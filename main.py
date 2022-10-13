from setup import *
from game import Game
from screens import Title, GameOver, Pause

delta: int = 1000 / fps
is_running: bool = True

scenes = {
    "Title": Title,
    "Game": Game,
    "GameOver": GameOver,
    "Pause": Pause
}

scene = Title()

pause = Pause()

while is_running:
    if pygame.event.peek(pygame.QUIT):
        is_running = False

    if not (isinstance(scene, Game) and scene.tm.paused):
        scene.update(delta)
        scene.draw(screen)
    else:
        if pause.update(delta):
            scene.tm.paused = False
        pause.draw(screen)

    if scene.next_scene is not None:
        if scene.next_scene == "GameOver" and isinstance(scene, Game):
            scene = scenes[scene.next_scene](scene.score)
        else:
            scene = scenes[scene.next_scene]()

    pygame.display.update()
    delta = clock.tick(fps)

pygame.quit()
