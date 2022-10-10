from setup import *
from game import Game

game = Game()

is_running = True

previous_time = time.time()


while is_running:
    delta_time = time.time() - previous_time
    previous_time = time.time()
    #RGB
    screen.fill((0, 0, 0))
    
    #Event listener
    for event in pygame.event.get(pygame.QUIT):
        if event.type == pygame.QUIT:
            is_running = False

    game.update(delta_time * 1000) # 1000 ms in 1 sec
    game.draw(screen)

    pygame.display.update()

pygame.quit()