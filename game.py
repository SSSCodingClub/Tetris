from setup import *
from block import Block
from tetromino import Tetromino

class Game:

    def __init__(self):
        self.global_blocks = [Block((0, SCREEN_HEIGHT - 30), RED),Block((180, SCREEN_HEIGHT - 30), RED),Block((180, SCREEN_HEIGHT - 60), RED),Block((180, SCREEN_HEIGHT - 90), RED),Block((180, SCREEN_HEIGHT - 150), RED)]
        self.tetromino = Tetromino(self.global_blocks)
    
    def update(self, delta):
        self.tetromino.update(delta)
        if self.tetromino.has_fallen:
            self.tetromino = Tetromino(self.global_blocks)

    def draw(self, screen):
        for block in self.global_blocks:
            block.draw(screen)
