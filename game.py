from typing import Tuple
from setup import *
#tetrominoes fun



class Block:
    side_length: int = 30

    def __init__(self, pos: Tuple):
        self.position: pygame.Vector2 = pygame.Vector2(pos)

    def move_y(self, block_list): # Note for later, add type annotation
        if self.position.y + self.side_length >= SCREEN_HEIGHT:
            self.position.y = SCREEN_HEIGHT - self.side_length
            return
        for block in block_list:
            if block is not self:
                if self.get_rect(dy = self.side_length).colliderect(block.get_rect()):
                    self.position.y = block.position.y - self.side_length
                    return
        self.position.y += Block.side_length

    def get_rect(self, dx=0, dy=0):
        return pygame.Rect(self.position + pygame.Vector2(dx, dy), (self.side_length, self.side_length))

    def draw(self, surf: pygame.Surface):
        pygame.draw.rect(surf, Colour.RED, self.get_rect())


class BlockManager:
    gravity_time: int = 250
    falling: Block = None

    def __init__(self):
        self.blocks: list[Block] = []
        self.time: int = 0

    def add_block(self, block):
        self.blocks.append(block)

    def update(self, delta: int):
        self.time += delta
        if self.time >= self.gravity_time:
            self.time -= self.gravity_time
            for block in self.blocks:
                block.move_y(self.blocks)


    def draw(self, surf: pygame.Surface):
        for block in self.blocks:
            block.draw(surf)


class Tetrominoe:
    shape: list[Tuple] = [(1,1), (0,1),  (0,0), (1,0)]

    def __init__(self, bm: BlockManager) -> None:
        self.blocks = []
        for coords in self.shape:
            x,y = coords
            self.blocks.append(Block((x * Block.side_length, y * Block.side_length)))

        self.other_blocks = bm.blocks

        for b in self.blocks:
            bm.add_block(b)

    def update(self, delta: int) -> None:
        for event in pygame.event.get(pygame.KEYDOWN):
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    for block in self.blocks:
                        block.position.x -= block.side_length
                elif event.key == pygame.K_d:
                    for block in self.blocks:
                        block.position.x += block.side_length

    def draw(self, surf: pygame.Surface) -> None:
        ...
class Game:

    def __init__(self):
        self.bm: BlockManager = BlockManager()
        self.t: Tetrominoe = Tetrominoe(self.bm)

    def update(self, delta: int):
        self.bm.update(delta)
        self.t.update(delta)


    def draw(self, surf: pygame.Surface):
        surf.fill(Colour.BLACK)
        self.bm.draw(surf)
