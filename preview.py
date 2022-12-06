from tetromino import Tetromino
from block import Block


class Preview:

    def __init__(self):
        self.tetromino = Tetromino([], []) # empty for now

    def update(self, tetromino):
        other_blocks = tetromino.other_blocks[:] # copy the other blocks list
        # list comphrension 
        blocks = [Block(block.position, block.colour) for block in tetromino.blocks] 

        for block in tetromino.blocks: # remove the actual blocks of the falling tetromino
            other_blocks.remove(block)

        # new tetromino each frame
        self.tetromino = Tetromino(other_blocks, blocks)

        while not self.tetromino.has_fallen: # has_fallen set to False when it cannot move anymore
            self.tetromino.move_down()

    def draw(self, screen):
        for block in self.tetromino.blocks:
            block.draw(screen, filled=False)