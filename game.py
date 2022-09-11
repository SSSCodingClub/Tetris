from typing import Tuple
from setup import *


# tetrominoes fun
class Block:
    side_length: int = 40

    def __init__(self, pos: Tuple):
        self.position: pygame.Vector2 = pygame.Vector2(pos)

    def update(self, delta: int):
        pass

    def move_y(self, block_list):  # Note for later, add type annotation
        print('b')
        if self.position.y + self.side_length < SCREEN_HEIGHT:
            print('a')
            return
        for block in block_list:
            if block is not self:
                if self.get_rect(dy=self.side_length).colliderect(block.get_rect()):
                    print('hi')
                    return

        self.position.y += self.side_length

    def get_rect(self, dx=0, dy=0):
        return pygame.Rect(self.position + pygame.Vector2(dx, dy), (self.side_length, self.side_length))

    def draw(self, surf: pygame.Surface):
        pygame.draw.rect(surf, Colour.RED, self.get_rect())


class BlockManager:
    gravity_time: int = 1500
    falling: Block = None

    def __init__(self):
        self.blocks: list[Block] = [Block((0, 0)),
                                    Block((0, 80))]
        self.time: int = 0

    def update(self, delta: int):
        self.time += delta

        if self.time >= self.gravity_time:
            for block in self.blocks:
                block.move_y(self.blocks)

    def draw(self, surf: pygame.Surface):
        for block in self.blocks:
            block.draw(surf)


class Game:

    def __init__(self):
        self.bm: BlockManager = BlockManager()

    def update(self, delta: int):
        self.bm.update(delta)

    def draw(self, surf: pygame.Surface):
        surf.fill(Colour.BLACK)
        self.bm.draw(surf)
