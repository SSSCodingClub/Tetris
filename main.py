from setup import *
from game import Game
from start import Start
from game_over import GameOver

scene = Start()

is_running = True

previous_time = time.time()


while is_running:
    delta_time = time.time() - previous_time
    previous_time = time.time()

    status = scene.update(delta_time * 1000) # 1000 ms in 1 sec
    if status == COMMAND_EXIT:
        is_running = False
    elif status == COMMAND_START:
        scene = Game()
    elif status == COMMAND_GAME_OVER:
        scene = GameOver(scene.score)

    scene.draw(screen)

    pygame.display.update()

pygame.quit()