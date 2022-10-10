from setup import *
from block import Block, BlockManager, Tetrominoe, TetrominoeManager

class Game:

    def __init__(self):
        self.bm: BlockManager = BlockManager()
        self.tm: TetrominoeManager = TetrominoeManager(self.bm)

        self.score = 0

    def update(self, delta: int):
        self.tm.update(delta)
        self.score += self.bm.update(delta)

        # print(self.score)

    def draw(self, surf: pygame.Surface):
        surf.fill(Colour.BLACK)
        pygame.draw.rect(surf, Colour.GRAY, pygame.Rect(Block.side_length, 0, SCREEN_WIDTH - 2 * Block.side_length,
                                                        SCREEN_HEIGHT - Block.side_length))
        self.bm.draw(surf)
