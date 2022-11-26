from setup import *

class GameOver:

    def __init__(self):
        pass
    

    def update(self, delta):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return COMMAND_EXIT
                
    def draw(self, screen):
        screen.fill(BLUE)