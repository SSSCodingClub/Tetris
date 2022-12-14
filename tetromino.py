from setup import *
from block import Block
from particles import BlockFall


class Tetromino:
    gravity_time = 250

    
    def __init__(self, global_blocks, blocks, effects=None):
        self.blocks = blocks

        self.other_blocks = global_blocks
        
        self.time = 0
        self.has_fallen = False

        self.effect_list = effects


    def update(self, delta):
        self.time += delta

        if self.time >= self.gravity_time:
            self.move_down()
            self.time = 0
            return True
        return False

    def move_down(self):
        can_move = True
        for block in self.blocks:
            if not block.can_move_down(self.other_blocks, self.blocks):
                can_move = False

        if can_move:
            for block in self.blocks:
                block.move_down()
                block.has_fallen = False

            self.has_fallen = False
        else:
            self.has_fallen = True
            for block in self.blocks:
                block.has_fallen = True
                if self.effect_list is not None:
                    self.effect_list.append(BlockFall(block, 250, 3))
            
    


        