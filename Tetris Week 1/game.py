from setup import *
from block import Block


class Game:

    def __init__(self):

        self.block = Block((0,0))
        self.time = 0

    def update(self):

        self.time += 1
        if self.time % 256 == 0:
            self.block.update()

    def draw(self, surf: pygame.Surface):
        self.block.draw(surf)