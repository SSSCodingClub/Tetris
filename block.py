import pygame.draw

from setup import *


class Block:
    side_length: int = 30
    bezel = 2

    def __init__(self, pos: Tuple, colour: Tuple):
        self.position: pygame.Vector2 = pygame.Vector2(pos)
        self.colour = colour
        self.outline_colour = (max(self.colour[0] - 25, 0), max(self.colour[1] - 25, 0), max(self.colour[2] - 25, 0))
        self.falling = True

    def check_y(self, block_list):  # Note for later, add type annotation
        if self.position.y + self.side_length >= SCREEN_HEIGHT - Block.side_length:
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
            if self.position.x + self.side_length >= SCREEN_WIDTH - Block.side_length:
                # self.position.x = SCREEN_WIDTH - self.side_length
                return False
        else:  # -1 for left
            if self.position.x <= Block.side_length:  # this is the wall at the sides
                # self.position.x = 0
                return False

        for block in block_list:
            if block is not self:
                if self.get_rect(dx=self.side_length * direction).colliderect(block.get_rect()):
                    # self.position.x = block.position.x - self.side_length
                    return False
        return True

    def get_rect(self, dx=0, dy=0, side=side_length):
        return pygame.Rect(self.position + pygame.Vector2(dx, dy), (side, side))
        # return pygame.Rect(self.position + pygame.Vector2(dx, dy), (self.side_length, self.side_length))

    def draw(self, surf: pygame.Surface, wireframe=False):
        if wireframe:
            # output = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
            pygame.draw.rect(surf, self.colour, self.get_rect(), self.bezel)
            # pygame.draw.rect(surf, Colour.GRAY,
            #                  self.get_rect(self.bezel, self.bezel, self.side_length - 2 * self.bezel))
            # output.set_alpha(128)
            # surf.blit(output,(0,0))
        else:
            pygame.draw.rect(surf, self.colour, self.get_rect())
            pygame.draw.rect(surf, self.outline_colour, self.get_rect(), self.bezel)
            # pygame.draw.rect(surf, self.colour,
            #                  self.get_rect(dx=self.bezel, dy=self.bezel, side=self.side_length - 2 * self.bezel))


class BlockManager:

    def __init__(self):
        self.blocks: list[Block] = []
        self.falling_bits = []

        # self.add_block(Block((Block.side_length, Block.side_length * 5), Colour.RED))

    def add_block(self, block):
        self.blocks.append(block)

        self.sort_blocks()

    def sort_blocks(self):  # sorts blocks from greatest y to least y
        def get_y(block: Block):
            return block.position.y

        self.blocks.sort(reverse=True, key=get_y)

    def update(self, delta: int):

        for i in self.falling_bits:
            i.update(delta)
            if not i.falling:
                self.falling_bits.remove(i)
        # print('---------------------------------------------', len(self.blocks))
        self.sort_blocks()
        grid = [[None for i in range(12)] for i in range(21)]
        for block in self.blocks:
            if not block.falling:
                grid[int(block.position.y / Block.side_length)][int(block.position.x / Block.side_length)] = block

        # def print_grid():
        #
        #     for i in grid:
        #         for j in i:
        #             if isinstance(j, Block):
        #                 print("x", end=" ")
        #             else:
        #                 print(" ", end=" ")
        #         print()

        # print('-----------------')
        score_to_be_added = 0
        for n, layer in enumerate(grid):
            x_counts = 0
            for i in layer:
                if isinstance(i, Block):
                    x_counts += 1
            if x_counts >= 10:
                for i in layer:
                    if isinstance(i, Block):
                        if i in self.blocks:
                            self.blocks.remove(i)
                grid[n] = [None for _ in range(12)]
                score_to_be_added += 1
                # print_grid()
                self.detect_tetrominoes(grid)
                # counter = 0
                # # move all blocks before down
                # for m, l in enumerate(grid[n::]):
                #     for k, j in enumerate(l):
                #         if isinstance(j, Block): # maybe make check so that it doesnt go out
                #             counter += 1
                # #             j.position.y += Block.side_length
                # #             grid[m][k + 1] = j
                # #             grid[m][k] = None
                # print(counter)

        # for i in grid:
        #     for j in i:
        #         if isinstance(j, Block):
        #             print("x", end=" ")
        #         else:
        #             print(" ", end=" ")
        #     print()
        return score_to_be_added

    def detect_tetrominoes(self, l):
        grid = l[:]
        seen = set()

        # def print_grid(g):
        #
        #     for i in g:
        #         for j in i:
        #             if j == 'x':
        #                 print("b", end=" ")
        #             elif isinstance(j, Block):
        #                 print('o', end=' ')
        #             else:
        #                 print(" ", end=" ")
        #         print()
        # temp = []
        def dfs(x, y, current_t):
            if grid[y][x] in seen:
                return
            else:
                seen.add(grid[y][x])

            if x + 1 < 12 and isinstance(grid[y][x + 1], Block):
                current_t.append(grid[y][x + 1])
                # seen.add(grid[y][x+1])
                # temp.append((y,x+1))
                dfs(x + 1, y, current_t)
            if x - 1 > 0 and isinstance(grid[y][x - 1], Block):
                current_t.append(grid[y][x - 1])
                # seen.add(grid[y][x-1])
                # temp.append((y,x-1))
                dfs(x - 1, y, current_t)
            if y + 1 < 20 and isinstance(grid[y + 1][x], Block):
                current_t.append(grid[y + 1][x])
                # seen.add(grid[y+1][x])
                # temp.append((y+1,x))
                dfs(x, y + 1, current_t)
            if y - 1 > 0 and isinstance(grid[y - 1][x], Block):
                current_t.append(grid[y - 1][x])
                # seen.add(grid[y-1][x])
                # temp.append((y-1,x))
                dfs(x, y - 1, current_t)

        print()
        for y, layer in enumerate(grid):
            for x, i in enumerate(layer):
                if isinstance(i, Block) and i not in seen:
                    current_tetrominoe = [i]
                    # temp = []
                    dfs(x, y, current_tetrominoe)
                    # g = grid[:]
                    # for a,b in temp:
                    #     g[a][b] = 'x'
                    # print_grid(g)

                    self.falling_bits.append(Tetrominoe(self, current_tetrominoe))
                    print('a')

    def draw(self, surf: pygame.Surface):
        for block in self.blocks:
            block.draw(surf)


class Tetrominoe:
    gravity_time: int = 250
    # https://tetris.fandom.com/wiki/Tetromino refer to this for names
    shapes: dict = {
        "O": ((1, 1), (0, 1), (0, 0), (1, 0)),
        "I": ((-1, 0), (0, 0), (1, 0), (2, 0)),
        "J": ((0, 1), (-1, 1), (1, 1), (-1, 0)),
        "L": ((0, 1), (-1, 1), (1, 1), (1, 0)),
        "S": ((-1, 1), (0, 1), (0, 0), (1, 0)),
        "T": ((-1, 1), (0, 1), (1, 1), (0, 0)),
        "Z": ((0, 1), (1, 1), (-1, 0), (0, 0))
    }

    rotation_centers = {
        "O": (0, 0),  # does not appear to rotate
        "I": (-1, -1),
        "J": (-1, 0),
        "L": (-1, 0),
        "S": (-1, 0),
        "T": (-1, 0),
        "Z": (-1, 0)

    }

    colours = [Colour.RED, Colour.PURPLE, Colour.BLUE, Colour.AQUA, Colour.ORANGE, Colour.YELLOW, Colour.GREEN]

    # def draw(self, surf):
    #     print(self.rotation_center, self.blocks[0].position)
    #     r = pygame.Rect(self.rotation_center, (Block.side_length, Block.side_length))
    #     pygame.draw.rect(surf,(255,255,255),r)

    def __init__(self, bm: BlockManager, blocks=None) -> None:
        if blocks is None:
            self.blocks = []

            colour = random.choice(self.colours)
            self.shape = random.choice(list(self.shapes.keys()))
            # self.shape = "I"
            for coords in self.shapes[self.shape]:
                x, y = coords
                self.blocks.append(Block(((x + 5) * Block.side_length, y * Block.side_length), colour))

            self.rotation_center = pygame.Vector2(((self.rotation_centers[self.shape][0] + 5) * Block.side_length,
                                                   self.rotation_centers[self.shape][1] * Block.side_length))

            self.other_blocks = bm.blocks.copy()

            for b in self.blocks:
                bm.add_block(b)

            self.just_spawned = True
        else:
            self.blocks = list(dict.fromkeys(blocks.copy()))

            # self.blocks = blocks[:]

            self.rotation_center = pygame.Vector2(0, 0)

            def get_y(block: Block):
                return block.position.y

            self.blocks.sort(reverse=True, key=get_y)
            self.other_blocks = []
            # if bm is not None:
            for b in bm.blocks:
                if b not in self.blocks:
                    self.other_blocks.append(b)
            self.just_spawned = False

        self.time: int = 0
        self.falling: bool = True

        self.bm = bm

        self.speed_modifier = 1

    def update(self, delta: int) -> bool:
        if self.falling:
            return self.move(delta)

    def move(self, delta) -> bool:

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
                self.rotation_center.y += Block.side_length
            else:
                if self.just_spawned:
                    return True

                self.falling = False
                for block in self.blocks:
                    block.falling = False
        return False


class TetrominoeManager:
    delay_time = 500

    def __init__(self, block_manager):
        self.t: Tetrominoe = Tetrominoe(block_manager)
        self.preview = Preview(self.t.blocks)

        self.bm = block_manager
        self.delay = 0
        self.rotations = 0

    def update(self, delta: int):
        if pygame.key.get_pressed()[pygame.K_s]:
            self.t.speed_modifier = 5
        else:
            self.t.speed_modifier = 1
        if self.t.falling:
            for event in pygame.event.get((pygame.KEYDOWN, pygame.KEYUP)):
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_a:
                        can_move = True
                        for block in self.t.blocks:
                            if not block.check_x(-1, self.t.other_blocks):
                                can_move = False
                        if can_move:
                            for block in self.t.blocks:
                                block.position.x -= block.side_length
                            self.t.rotation_center.x -= Block.side_length
                    elif event.key == pygame.K_d:
                        can_move = True
                        for block in self.t.blocks:
                            if not block.check_x(1, self.t.other_blocks):
                                can_move = False
                        if can_move:
                            for block in self.t.blocks:
                                block.position.x += block.side_length
                            self.t.rotation_center.x += Block.side_length

                    elif event.key == pygame.K_r:
                        self.rotate_tetrominoe(1)
                #     elif event.key == pygame.K_s:
                #         self.speed_modifier = 5
                # if event.type == pygame.KEYUP:
                #     if event.key == pygame.K_s:
                #         self.speed_modifier = 1
        if self.t.update(delta):  # if collides with block after just spawning
            return True

        self.preview.update(self.t.blocks, self.t.other_blocks)

        if not self.t.falling:
            if self.delay >= self.delay_time:
                self.reset_tetrominoe()
                self.delay = 0

            self.delay += delta
        return False

    def reset_tetrominoe(self):
        self.t = Tetrominoe(self.bm)
        self.preview = Preview(self.t.blocks)
        self.rotations = 0

    def rotate_tetrominoe(self, direction):
        def print_grid(g):

            for i in g:
                for j in i:
                    if j == 1:
                        print("x", end=" ")
                    else:
                        print("_", end=" ")
                print()

        # refer to https://tetris.wiki/Super_Rotation_System
        # 1 2 3
        # 4 5 6
        # 7 8 9
        # rotate
        # 7 4 1
        # 8 5 2
        # 9 6 3
        if self.t.shape == "O":
            return
        elif self.t.shape != "I":
            grid = [[0, 0, 0],
                    [0, 0, 0],
                    [0, 0, 0]]  # 0 for no block, 1 for block

            for x, y in self.t.shapes[self.t.shape]:
                grid[y][x + 1] = 1
        else:
            grid = [[0, 0, 0, 0],
                    [0, 0, 0, 0],
                    [0, 0, 0, 0],
                    [0, 0, 0, 0]]  # 0 for no block, 1 for block
            for x, y in self.t.shapes[self.t.shape]:
                grid[y + 1][x + 1] = 1

        def rotate(g):
            output = deepcopy(grid)
            for i in range(len(g[0])):
                for j in range(len(g)):
                    output[i][j] = g[j][i]
                output[i].reverse()
            return output

        rotated_grid = deepcopy(grid)

        self.rotations += 1
        self.rotations %= 4
        if direction > 0:
            for i in range(self.rotations):
                rotated_grid = rotate(rotated_grid)

        # print_grid(rotated_grid)

        rotated_positions = []
        for y, layer in enumerate(rotated_grid):
            for x, val in enumerate(layer):
                if val == 1:
                    rotated_positions.append((self.t.rotation_center.x + x * Block.side_length,
                                              self.t.rotation_center.y + y * Block.side_length))

        for pos, block in zip(rotated_positions, self.t.blocks):
            # print(block.position, pos)
            block.position = pygame.Vector2(pos)

    def draw(self, surf):
        if self.t.falling:
            self.preview.draw(surf)
        # self.t.draw(surf)


class Preview:

    def __init__(self, blocks):
        self.blocks = deepcopy(blocks)

    def check_y(self, block, block_list):  # Note for later, add type annotation
        if block in block_list:
            print('c')

        if block.position.y + block.side_length >= SCREEN_HEIGHT - Block.side_length:
            return False
        for b in block_list:
            if b is not self:
                if block.get_rect(dy=block.side_length).colliderect(b.get_rect()):
                    return False
        return True

    def update(self, blocks, otherblocks):
        self.blocks = deepcopy(blocks)
        other_blocks = deepcopy(otherblocks)
        while True:
            can_move = True
            for block in self.blocks:
                if not self.check_y(block, other_blocks):
                    can_move = False
            if can_move:
                for block in self.blocks:
                    block.position.y += block.side_length
            else:
                break

    def draw(self, surf):
        for block in self.blocks:
            block.draw(surf, wireframe=True)