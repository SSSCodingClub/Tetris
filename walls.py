from setup import *
from block import Block


class Walls:

    def __init__(self):
        self.blocks = []

        for i in range(GRID_HEIGHT):
            self.blocks.append(Block((0, i * Block.side_length), GRAY))
            self.blocks.append(Block((SCREEN_WIDTH - Block.side_length, i * Block.side_length), GRAY))
        
        for i in range(1, GRID_LENGTH - 1):
            self.blocks.append(Block((i * Block.side_length, SCREEN_HEIGHT - Block.side_length), GRAY))
            
    def draw(self, screen):
        for block in self.blocks:
            block.draw(screen)