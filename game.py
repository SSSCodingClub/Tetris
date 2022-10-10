from setup import *
from block import Block
from tetromino import Tetromino

class Game:

    def __init__(self):
        self.tetromino = Tetromino()
    
    def update(self, delta):
        self.tetromino.update(delta)

    def draw(self, screen):
        for block in self.tetromino.blocks:
            block.draw(screen)