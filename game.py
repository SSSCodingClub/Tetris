from mimetypes import init
from typing import Tuple
from setup import *
#tetrominoes fun



class Block:
    side_length: int = 30

    def __init__(self, pos: Tuple, colour:Tuple):
        self.position: pygame.Vector2 = pygame.Vector2(pos)
        self.colour =  colour
        self.falling = True

    def check_y(self, block_list): # Note for later, add type annotation
        if self.position.y + self.side_length >= SCREEN_HEIGHT:
            # self.position.y = SCREEN_HEIGHT - self.side_length
            return False
        for block in block_list:
            if block is not self:
                if self.get_rect(dy = self.side_length).colliderect(block.get_rect()):
                    # self.position.y = block.position.y - self.side_length
                    return False
        return True

    def check_x(self, direction, block_list):
        if direction > 0: # 1 for right
            if self.position.x + self.side_length >= SCREEN_WIDTH:
                # self.position.x = SCREEN_WIDTH - self.side_length
                return False
        else: # -1 for left
            if self.position.x <= 0:
                # self.position.x = 0
                return False

        for block in block_list:
            if block is not self:
                if self.get_rect(dx = self.side_length * direction).colliderect(block.get_rect()):
                    # self.position.x = block.position.x - self.side_length
                    return False
        return True

    def get_rect(self, dx=0, dy=0):
        return pygame.Rect(self.position + pygame.Vector2(dx, dy), (self.side_length, self.side_length))

    def draw(self, surf: pygame.Surface):
        pygame.draw.rect(surf, self.colour, self.get_rect())


class BlockManager:

    def __init__(self):
        self.blocks: list[Block] = []

        # self.add_block(Block((Block.side_length, Block.side_length * 5), Colour.RED))

    def add_block(self, block):
        self.blocks.append(block)

        def get_y(block: Block):
            return block.position.y

        self.blocks.sort(reverse=True, key=get_y)

    def update(self, delta: int):
        layer = []
        prev_y = None
        for i,block in enumerate(self.blocks[::-1]):
            if not block.falling:
                print(block)
                if prev_y is None or prev_y != block.position.y:
                    layer = []
                    print("Next layer")
                prev_y = block.position.y

                layer.append(block)

                if len(layer) >= 5: # 10 x 20 is size of playing field
                    print('remove!')
                    for b in layer:
                        if b in self.blocks:
                            del self.blocks[self.blocks.index(b)]

                    # for b in self.blocks[::i]:
                    #     b.position.y += Block.side_length
                

            

    def draw(self, surf: pygame.Surface):
        for block in self.blocks:
            block.draw(surf)


class Tetrominoe:
    gravity_time: int = 250

    shape: list[Tuple] = [(1,1), (0,1),  (0,0), (1,0)]

    colours = [Colour.RED, Colour.PURPLE, Colour.BLUE, Colour.AQUA, Colour.ORANGE, Colour.YELLOW, Colour.GREEN]

    def __init__(self, bm: BlockManager) -> None:
        self.blocks = []

        colour = random.choice(self.colours)

        for coords in self.shape:
            x,y = coords
            self.blocks.append(Block((x * Block.side_length, y * Block.side_length), colour))

        self.other_blocks = bm.blocks.copy()

        for b in self.blocks:
            bm.add_block(b)
        
        self.time: int = 0
        self.has_fallen: bool = False

        self.bm = bm

    def update(self, delta: int) -> None:
        self.move(delta)
        if self.has_fallen:
            self.__init__(self.bm)

    def move(self, delta) -> None:
        for event in pygame.event.get(pygame.KEYDOWN):
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    can_move = True
                    for block in self.blocks:
                        if not block.check_x(-1, self.other_blocks):
                            can_move = False
                    if can_move:
                        for block in self.blocks:
                            block.position.x -= block.side_length
                elif event.key == pygame.K_d:
                    can_move = True
                    for block in self.blocks:
                        if not block.check_x(1, self.other_blocks):
                            can_move = False
                    if can_move:
                        for block in self.blocks:
                            block.position.x += block.side_length

        self.time += delta
        if self.time >= self.gravity_time:
            self.time -= self.gravity_time
            can_move = True
            for block in self.blocks:
                if not block.check_y(self.other_blocks):
                    can_move = False
            if can_move:
                for block in self.blocks:
                    block.position.y += block.side_length
            else:
                self.has_fallen = True
                for block in self.blocks:
                    block.falling = False

    def rotate(self):
        ...

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
