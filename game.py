from mimetypes import init
from typing import Tuple
from setup import *


class Block:
    side_length: int = 30

    def __init__(self, pos: Tuple, colour: Tuple):
        self.position: pygame.Vector2 = pygame.Vector2(pos)
        self.colour = colour
        self.falling = True

    def check_y(self, block_list):  # Note for later, add type annotation
        if self.position.y + self.side_length >= SCREEN_HEIGHT:
            # self.position.y = SCREEN_HEIGHT - self.side_length
            return False
        for block in block_list:
            if block is not self:
                if self.get_rect(dy=self.side_length).colliderect(block.get_rect()):
                    # self.position.y = block.position.y - self.side_length
                    return False
        return True

    def check_x(self, direction, block_list):
        if direction > 0:  # 1 for right
            if self.position.x + self.side_length >= SCREEN_WIDTH:
                # self.position.x = SCREEN_WIDTH - self.side_length
                return False
        else:  # -1 for left
            if self.position.x <= 0:
                # self.position.x = 0
                return False

        for block in block_list:
            if block is not self:
                if self.get_rect(dx=self.side_length * direction).colliderect(block.get_rect()):
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

        self.sort_blocks()

    def sort_blocks(self):  # sorts blocks from greatest y to least y
        def get_y(block: Block):
            return block.position.y

        self.blocks.sort(reverse=True, key=get_y)

    def update(self, delta: int):
        # print('---------------------------------------------', len(self.blocks))
        self.sort_blocks()
        grid = [[None for i in range(12)] for i in range(21)]
        for block in self.blocks:
            if not block.falling:
                grid[int(block.position.y / Block.side_length)][int(block.position.x / Block.side_length)] = block

        score_to_be_added = 0
        for n, layer in enumerate(grid):
            x_counts = 0
            for i in layer:
                if isinstance(i, Block):
                    x_counts += 1
            if x_counts >= 12:
                for i in layer:
                    if isinstance(i, Block):
                        if i in self.blocks:
                            self.blocks.remove(i)
                grid[n] = [None for _ in range(12)]
                score_to_be_added += 1


        # for i in grid:
        #     for j in i:
        #         if isinstance(j, Block):
        #             print("x", end=" ")
        #         else:
        #             print(" ", end=" ")
        #     print()
        return score_to_be_added

    def draw(self, surf: pygame.Surface):
        for block in self.blocks:
            block.draw(surf)


class Tetrominoe:
    gravity_time: int = 250

    shape: list[Tuple] = [(1, 1), (0, 1), (0, 0), (1, 0)]

    colours = [Colour.RED, Colour.PURPLE, Colour.BLUE, Colour.AQUA, Colour.ORANGE, Colour.YELLOW, Colour.GREEN]

    def __init__(self, bm: BlockManager) -> None:
        self.blocks = []

        colour = random.choice(self.colours)

        for coords in self.shape:
            x, y = coords
            self.blocks.append(Block(((x + 5) * Block.side_length, y * Block.side_length), colour))

        self.other_blocks = bm.blocks.copy()

        for b in self.blocks:
            bm.add_block(b)

        self.time: int = 0
        self.falling: bool = True

        self.bm = bm

        self.speed_modifier = 1
        self.just_spawned = True

    def update(self, delta: int) -> bool:
        if self.falling:
            return self.move(delta)

    def move(self, delta) -> bool:
        for event in pygame.event.get((pygame.KEYDOWN, pygame.KEYUP)):
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
            #     elif event.key == pygame.K_s:
            #         self.speed_modifier = 5
            # if event.type == pygame.KEYUP:
            #     if event.key == pygame.K_s:
            #         self.speed_modifier = 1

        self.time += delta * self.speed_modifier
        if self.time >= self.gravity_time:
            self.time -= self.gravity_time
            can_move = True
            for block in self.blocks:
                if not block.check_y(self.other_blocks):
                    can_move = False
            if can_move:
                self.just_spawned = False
                for block in self.blocks:
                    block.position.y += block.side_length
            else:
                if self.just_spawned:
                    return True

                self.falling = False
                for block in self.blocks:
                    block.falling = False
        return False

    def rotate(self):
        ...


class TetrominoeManager:
    delay_time = 500

    def __init__(self, block_manager):
        self.t: Tetrominoe = Tetrominoe(block_manager)
        self.bm = block_manager
        self.delay = 0

    def update(self, delta: int):
        if pygame.key.get_pressed()[pygame.K_s]:
            self.t.speed_modifier = 5
        else:
            self.t.speed_modifier = 1

        if self.t.update(delta):  # if collides with block after just spawning
            print('you lose!')

        if not self.t.falling:
            if self.delay >= self.delay_time:
                self.reset_tetrominoe()
                self.delay = 0

            self.delay += delta

    def reset_tetrominoe(self):
        self.t = Tetrominoe(self.bm)


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
        self.bm.draw(surf)
