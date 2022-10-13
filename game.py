from setup import *
from block import Block, BlockManager, Tetrominoe, TetrominoeManager
from effects import  LineClear,BlockHit

class Walls:
    colour = Colour.DARK_GRAY

    def __init__(self):
        self.blocks = []
        for i in range(GRID_HEIGHT):
            self.blocks.append(Block((0, i * Block.side_length), self.colour))
            self.blocks.append(Block((SCREEN_WIDTH - Block.side_length, i * Block.side_length), self.colour))
        for i in range(1, GRID_WIDTH):
            self.blocks.append(Block((i * Block.side_length, SCREEN_HEIGHT - Block.side_length), self.colour))

    def draw(self, surf):
        for block in self.blocks:
            block.draw(surf)


class Game:

    def __init__(self):
        self.effects = []
        # self.effects.append()
        self.next_scene = None
        self.bm: BlockManager = BlockManager(self.effects)
        self.tm: TetrominoeManager = TetrominoeManager(self.bm, self.effects)

        self.score = 0

        self.walls = Walls()

    def update(self, delta: int):

        for effect in self.effects:
            effect.update(delta)
        if self.tm.update(delta):
            self.next_scene = "GameOver"

        # if self.tm.paused:
        #     self.next_scene = "Pause"

        self.score += self.bm.update(delta)


        # print(self.score)

    def draw(self, surf: pygame.Surface):
        surf.fill(Colour.GRAY)
        self.walls.draw(surf)
        # pygame.draw.rect(surf, Colour.GRAY, pygame.Rect(Block.side_length, 0, SCREEN_WIDTH - 2 * Block.side_length,
        #                                                 SCREEN_HEIGHT - Block.side_length))
        self.tm.draw(surf)
        self.bm.draw(surf)
        for effect in self.effects:
            effect.draw(surf)
