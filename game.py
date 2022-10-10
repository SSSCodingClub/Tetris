from setup import *
from block import Block, BlockManager, Tetrominoe, TetrominoeManager

class Walls:
    colour = Colour.DARK_GRAY

    def __init__(self):
        self.blocks = []
        for i in range(GRID_HEIGHT):
            self.blocks.append(Block((0,i * Block.side_length),self.colour))
            self.blocks.append(Block((SCREEN_WIDTH-Block.side_length,i * Block.side_length),self.colour))
        for i in range(1,GRID_WIDTH):
            self.blocks.append(Block((i * Block.side_length,SCREEN_HEIGHT-Block.side_length),self.colour))

    def draw(self, surf):
        for block in self.blocks:
            block.draw(surf)

class Game:

    def __init__(self):
        self.next_scene = None
        self.bm: BlockManager = BlockManager()
        self.tm: TetrominoeManager = TetrominoeManager(self.bm)

        self.score = 0

        self.walls = Walls()

    def update(self, delta: int):
        if self.tm.update(delta):
            self.next_scene = "GameOver"
        self.score += self.bm.update(delta)

        # print(self.score)

    def draw(self, surf: pygame.Surface):
        surf.fill(Colour.GRAY)
        self.walls.draw(surf)
        # pygame.draw.rect(surf, Colour.GRAY, pygame.Rect(Block.side_length, 0, SCREEN_WIDTH - 2 * Block.side_length,
        #                                                 SCREEN_HEIGHT - Block.side_length))
        self.bm.draw(surf)
