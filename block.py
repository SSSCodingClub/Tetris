import pygame.draw

from setup import *
from effects import  LineClear, HardDrop, BlockHit


class Block:
    side_length: int = 30
    bezel = 2

    def __init__(self, pos: Tuple, colour: Tuple):
        self.position: pygame.Vector2 = pygame.Vector2(pos)
        self.colour = colour
        self.outline_colour = (max(self.colour[0] - 25, 0), max(self.colour[1] - 25, 0), max(self.colour[2] - 25, 0))
        self.falling = True
        self.is_controlled = False

    def is_colliding(self, block_list):
        if (not (self.side_length <= self.position.x <= SCREEN_WIDTH - self.side_length * 2 and
                 0 <= self.position.y <= SCREEN_HEIGHT - self.side_length * 2)):  # to account for block + wall
            return True
        for block in block_list:
            if block.is_controlled:
                continue

            if block is not self:
                if self.get_rect(dy=self.side_length).colliderect(block.get_rect()):
                    return False
        # for block in block_list:
        #     if block is self or block.falling:
        #         continue
        #     if block.get_rect().colliderect(self.get_rect()):
        #         return True
        return False

    def check_y(self, block_list,is_tetromino_controlled=False):  # Note for later, add type annotation
        if self.position.y + self.side_length >= SCREEN_HEIGHT - Block.side_length:
             return False, False
        if is_tetromino_controlled:
            still_falling = False
            for block in block_list:
                if block.is_controlled:
                    continue

                if block is not self:
                    if self.get_rect(dy=self.side_length).colliderect(block.get_rect()):
                        # self.position.y = block.position.y - self.side_length
                        if block.falling:
                            still_falling = True
                        return False, still_falling
        else:
            for block in block_list:
                if block.falling:
                    continue
                if block is not self:
                    if self.get_rect(dy=self.side_length).colliderect(block.get_rect()):
                        # self.position.y = block.position.y - self.side_length
                        return False, False

        return True, False

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
            if block is self or block.falling:
                continue
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

    def __init__(self, effects):
        self.blocks: list[Block] = []
        self.falling_bits = []
        self.effects = effects
        self.grid = [[None for i in range(12)] for i in range(21)]

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
            if not i.falling and i in self.falling_bits:
                self.falling_bits.remove(i)
                del i
        # print('---------------------------------------------', len(self.blocks))
        self.sort_blocks()
        self.grid = [[None for i in range(12)] for i in range(21)]
        for block in self.blocks:
            if not block.falling:
                self.grid[int(block.position.y / Block.side_length)][int(block.position.x / Block.side_length)] = block

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
        for n, layer in enumerate(self.grid):
            x_counts = 0
            for i in layer:
                if isinstance(i, Block):
                    x_counts += 1
            if x_counts >= 10:
                for i in layer:
                    if isinstance(i, Block):
                        if i in self.blocks:
                            self.blocks.remove(i)
                self.grid[n] = [None for _ in range(12)]
                score_to_be_added += 1
                Tetrominoe.gravity_time = max(100, Tetrominoe.gravity_time - 10)
                self.effects.append(LineClear((0,(n+1)*30),Tetrominoe.gravity_time,self.effects))
                # print_grid()
        if score_to_be_added > 0:
            self.detect_tetrominoes(self.grid)
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

    def draw(self, surf: pygame.Surface):
        for block in self.blocks:
            block.draw(surf)


class Tetrominoe:
    gravity_time: int = 400
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

    # Data from https://tetris.wiki/Super_Rotation_System#Wall_Kicks
    # J, L, S, T, Z Tetromino Wall Kick Data
    wall_kicks = {
        "0-1": ((0, 0), (-1, 0), (-1, -1), (0, +2), (-1, +2)),
        "3-0": ((0, 0), (+1, 0), (+1, +1), (0, -2), (+1, -2)),
        "1-2": ((0, 0), (+1, 0), (+1, +1), (0, -2), (+1, -2)),
        "2-3": ((0, 0), (-1, 0), (-1, -1), (0, +2), (-1, +2)),
        # "2-L": ((0, 0), (+1, 0), (+1, -1), (0, +2), (+1, +2)),
        # "L-2": ((0, 0), (-1, 0), (-1, +1), (0, -2), (-1, -2)),
        # "L-0": ((0, 0), (-1, 0), (-1, +1), (0, -2), (-1, -2)),
        # "0-L": ((0, 0), (+1, 0), (+1, -1), (0, +2), (+1, +2))
    }
    # I Tetromino Wall Kick Data
    I_wall_kicks = {
        "0-1": ((0, 0), (-2, 0), (+1, 0), (-2, +1), (+1, -2)),
        "3-0": ((0, 0), (+2, 0), (-1, 0), (+2, -1), (-1, +2)),
        "1-2": ((0, 0), (-1, 0), (+2, 0), (-1, -2), (+2, +1)),
        "2-3": ((0, 0), (+1, 0), (-2, 0), (+1, +2), (-2, -1)),
        # "2-L": ((0, 0), (+2, 0), (-1, 0), (+2, -1), (-1, +2)),
        # "L-2": ((0, 0), (-2, 0), (+1, 0), (-2, +1), (+1, -2)),
        # "L-0": ((0, 0), (+1, 0), (-2, 0), (+1, +2), (-2, -1)),
        # "0-L": ((0, 0), (-1, 0), (+2, 0), (-1, -2), (+2, +1))
    }

    colours = [Colour.RED, Colour.PURPLE, Colour.BLUE, Colour.AQUA, Colour.ORANGE, Colour.YELLOW, Colour.GREEN]

    # def draw(self, surf):
    #     print(self.rotation_center, self.blocks[0].position)
    #     r = pygame.Rect(self.rotation_center, (Block.side_length, Block.side_length))
    #     pygame.draw.rect(surf,(255,255,255),r)
    effects = []
    def __init__(self, bm: BlockManager, blocks=None) -> None:
        self.effects_added = False
        if blocks is None:
            self.blocks = []

            colour = random.choice(self.colours)
            self.shape = random.choice(list(self.shapes.keys()))
            # self.shape = "T"
            for coords in self.shapes[self.shape]:
                x, y = coords
                self.blocks.append(Block(((x + 5) * Block.side_length, y * Block.side_length), colour))

            self.rotation_center = pygame.Vector2(((self.rotation_centers[self.shape][0] + 5) * Block.side_length,
                                                   self.rotation_centers[self.shape][1] * Block.side_length))

            for b in self.blocks:
                b.is_controlled = True
                bm.add_block(b)

            def get_y(block: Block):
                return block.position.y

            self.blocks.sort(reverse=True, key=get_y)

            self.just_spawned = True
            self.is_controlled = True
        else:
            self.blocks = list(dict.fromkeys(blocks.copy()))
            for block in self.blocks:
                block.falling = True
                block.is_controlled = False
            # self.blocks = blocks[:]

            self.rotation_center = pygame.Vector2(0, 0)

            def get_y(block: Block):
                return block.position.y

            self.blocks.sort(reverse=True, key=get_y)
            self.just_spawned = False
            self.is_controlled = False

        self.hard_dropped = False

        self.time: int = 0
        self.falling: bool = True

        self.bm = bm

        self.speed_modifier = 1

    def update(self, delta: int) -> bool:
        if self.falling:
            temp = self.move(delta)
            if not self.effects_added:
                for block in self.blocks:
                    if not block.check_y(self.bm.blocks)[0]:
                        self.effects.append(BlockHit(block,250,3,self.effects))
                        self.effects_added = True

            return temp

    def move(self, delta) -> bool:

        self.time += delta * self.speed_modifier
        # print(self.time, self.gravity_time)
        if self.time >= self.gravity_time:
            self.time = 0
            can_move = True
            for block in self.blocks:
                check_y,still_falling = block.check_y(self.bm.blocks, self.is_controlled)
                if not check_y:
                    can_move = False
            if can_move:
                self.just_spawned = False
                for block in self.blocks:
                    block.position.y += block.side_length

                self.rotation_center.y += Block.side_length
            else:
                if self.just_spawned:
                    return True
                if not still_falling:
                    self.falling = False
                    for block in self.blocks:
                        block.falling = False
                        # block.is_controlled = False
                # self.bm.falling_bits.clear()
                # self.bm.detect_tetrominoes(self.bm.grid)



        return False


class TetrominoeManager:
    delay_time = 500

    def __init__(self, block_manager, effects):
        Tetrominoe.gravity_time = 400
        self.t: Tetrominoe = Tetrominoe(block_manager)
        self.preview = Preview(self.t.blocks)
        self.effects = effects
        self.bm = block_manager
        self.delay = 0
        self.rotations = 0

        self.paused = False
        self.left_move_ticker = 0
        self.left_moves = 0
        self.right_move_ticker = 0
        self.right_moves = 0
        self.rotational_move_ticker = 0
        self.rotational_moves = 0

    def update(self, delta: int):

        if self.t.just_spawned:
            collided = False
            for block in self.t.blocks:
                if block.is_colliding(self.t.bm.blocks) or not block.check_y(self.t.bm.blocks, True)[0]:
                    collided = True
            if collided:
                self.t.falling = False
                for block in self.t.blocks:
                    block.falling = False
                return True

        self.paused = False
        pressed = pygame.key.get_pressed()
        if not self.t.hard_dropped:
            if pressed[pygame.K_s] or pressed[pygame.K_DOWN]:
                self.t.speed_modifier = 5
            else:
                self.t.speed_modifier = 1

            moved_left = pressed[pygame.K_a] or pressed[pygame.K_LEFT]
            moved_right = pressed[pygame.K_d] or pressed[pygame.K_RIGHT]

            if moved_left and not moved_right:
                self.left_move_ticker += delta
                if self.left_moves == 0 or self.left_move_ticker > 210 and self.t.falling:
                    moved_sideways = True
                    self.left_move_ticker = 0
                    self.left_moves += 1
                    can_move = True
                    for block in self.t.blocks:
                        if not block.check_x(-1, self.t.bm.blocks):
                            can_move = False
                    if can_move:
                        for block in self.t.blocks:
                            block.position.x -= block.side_length
                        self.t.rotation_center.x -= Block.side_length
            else:
                self.left_move_ticker = 0
                self.left_moves = 0

            if moved_right and not moved_left:

                self.right_move_ticker += delta
                if self.right_moves == 0 or self.right_move_ticker > 210 and self.t.falling:
                    moved_sideways = True
                    self.right_move_ticker = 0
                    self.right_moves += 1
                    can_move = True
                    for block in self.t.blocks:
                        if not block.check_x(1, self.t.bm.blocks):
                            can_move = False
                    if can_move:
                        for block in self.t.blocks:
                            block.position.x += block.side_length
                        self.t.rotation_center.x += Block.side_length
            else:
                self.right_move_ticker = 0
                self.right_moves = 0

            if pressed[pygame.K_w] or pressed[pygame.K_UP] or pressed[pygame.K_r]:
                self.rotational_move_ticker += delta
                if self.rotational_moves == 0 or self.rotational_move_ticker > 275 and self.t.falling:
                    self.rotational_move_ticker = 0
                    self.rotational_moves += 1
                    self.rotate_tetrominoe(1)
            else:
                self.rotational_move_ticker = 0
                self.rotational_moves = 0




        if self.t.falling:


            for event in pygame.event.get((pygame.KEYDOWN, pygame.KEYUP)):
                if event.type == pygame.KEYDOWN:
                    # if event.key == pygame.K_a or event.key == pygame.K_LEFT:
                    #     can_move = True
                    #     for block in self.t.blocks:
                    #         if not block.check_x(-1, self.t.bm.blocks):
                    #             can_move = False
                    #     if can_move:
                    #         for block in self.t.blocks:
                    #             block.position.x -= block.side_length
                    #         self.t.rotation_center.x -= Block.side_length
                    #         moved_sideways = True
                    # elif event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                    #     can_move = True
                    #     for block in self.t.blocks:
                    #         if not block.check_x(1, self.t.bm.blocks):
                    #             can_move = False
                    #     if can_move:
                    #         for block in self.t.blocks:
                    #             block.position.x += block.side_length
                    #         self.t.rotation_center.x += Block.side_length
                    #         moved_sideways = True
                    # elif event.key == pygame.K_r or event.key == pygame.K_w or event.key == pygame.K_UP:
                    #     self.rotate_tetrominoe(1)
                    if event.key == pygame.K_SPACE:
                        self.t.hard_dropped = True
                        self.t.just_spawned = False
                        self.t.falling = True
                        for block, new in zip(self.t.blocks, self.preview.blocks):
                            block.position = new.position
                            block.falling = True
                            if not self.t.effects_added:
                                self.effects.append(BlockHit(block,250,3,self.effects))
                        self.t.effects_added = True
                        self.t.rotation_center.y += 30 * self.preview.moves_down
                        # self.effects.append(HardDrop2(self.t.blocks,self.effects))
                    elif event.key == pygame.K_ESCAPE:
                        self.paused = True
        else:
            for event in pygame.event.get(pygame.KEYDOWN):
                if event.key == pygame.K_ESCAPE:
                    self.paused = True
                    # elif event.key == pygame.K_q: # world is not ready for counter clockwise rotations
                    #     self.rotate_tetrominoe(-1)
                #     elif event.key == pygame.K_s:
                #         self.speed_modifier = 5
                # if event.type == pygame.KEYUP:
                #     if event.key == pygame.K_s:
                #         self.speed_modifier = 1


        if self.t.update(delta):  # if collides with block after just spawning
            return True

        self.preview.update(self.t.blocks, self.bm.blocks)
        for e in self.t.effects:
            if e not in self.effects:
                self.effects.append(e)
                self.effects[-1].effects = self.effects
        if not self.t.falling:
            if self.delay >= self.delay_time:
                self.reset_tetrominoe()
                self.delay = 0

            self.delay += delta
        return False

    def reset_tetrominoe(self):
        for block in self.t.blocks:
            block.is_controlled = False
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
        # rotate_c
        # 7 4 1
        # 8 5 2
        # 9 6 3
        # rotate_cc
        # 3 6 9
        # 2 5 8
        # 1 4 7
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

        def rotate_c(g):
            output = deepcopy(grid)
            for i in range(len(g[0])):
                for j in range(len(g)):
                    output[i][j] = g[j][i]
                output[i].reverse()
            return output

        def rotate_cc(g):
            output = deepcopy(grid)
            for i in range(len(g[0])):
                for j in range(len(g)):
                    output[i][j] = g[j][i]
            output.reverse()
            return output

        rotated_grid = deepcopy(grid)

        self.rotations += direction
        self.rotations %= 4
        if direction > 0:
            for i in range(self.rotations):
                rotated_grid = rotate_c(rotated_grid)
        elif direction < 0:
            for i in range(self.rotations):
                rotated_grid = rotate_cc(rotated_grid)

        # print_grid(rotated_grid)

        rotated_positions = []
        for y, layer in enumerate(rotated_grid):
            for x, val in enumerate(layer):
                if val == 1:
                    rotated_positions.append((self.t.rotation_center.x + x * Block.side_length,
                                              self.t.rotation_center.y + y * Block.side_length))

        # Wall kicks
        # DANGER! now entering nerd territory. https://tetris.wiki/Super_Rotation_System#Wall_Kicks

        temp = []
        for block in self.t.blocks:
            temp.append(block.position)
        # otherblocks = deepcopy(self.t.other_blocks)
        rotated = False
        if self.t.shape != "I":
            wall_kick_data = Tetrominoe.wall_kicks[f'{(self.rotations - 1) % 4}-{self.rotations}']
        else:
            wall_kick_data = Tetrominoe.I_wall_kicks[f'{(self.rotations - 1) % 4}-{self.rotations}']

        for x, y in wall_kick_data:
            for pos, block in zip(rotated_positions, self.t.blocks):
                # print(block.position, pos)
                block.position = pygame.Vector2(pos) + pygame.Vector2(x * Block.side_length, y * Block.side_length)

            can_move = True
            for block in self.t.blocks:
                if block.is_colliding(self.t.bm.blocks):
                    can_move = False
            if can_move:
                rotated = True
                for block in self.t.blocks:
                    block.falling = True
                self.t.falling = True
                break
        if not rotated:
            for block, t in zip(self.t.blocks, temp):
                block.position = t
        # if rotated:
        #     def get_y(b):
        #         return b.position.y
        #     temp.sort(key=get_y, reverse=True)
        #     self.t.blocks = deepcopy(temp)

    def draw(self, surf):
        if self.t.falling:
            self.preview.draw(surf)
        # self.t.draw(surf)


class Preview:

    def __init__(self, blocks):
        self.blocks = deepcopy(blocks)
        self.moves_down = 0

    def check_y(self, b, block_list):  # Note for later, add type annotation
        if b.position.y + b.side_length >= SCREEN_HEIGHT - b.side_length:
            # self.position.y = SCREEN_HEIGHT - self.side_length
            return False
        for block in block_list:
            if block.is_controlled:
                continue
            else:
                if b.get_rect(dy=Block.side_length).colliderect(block.get_rect()):
                    # self.position.y = block.position.y - self.side_length
                    return False
        return True

    def update(self, blocks, otherblocks):
        self.moves_down = 0

        self.blocks = deepcopy(blocks)
        positions = {(b.position.x, b.position.y): b for b in self.blocks}
        other_blocks = deepcopy(otherblocks)
        positions2 = {(b.position.x, b.position.y): b for b in other_blocks}
        self.blocks = []
        for i in positions.keys():
            if i in positions2:
                self.blocks.append(positions2[i])
        if len(self.blocks) > 0:
            while True:
                can_move = True
                for block in self.blocks:
                    if not self.check_y(block, other_blocks):
                        can_move = False
                if can_move:
                    for block in self.blocks:
                        block.position.y += block.side_length
                    self.moves_down += 1

                else:
                    break

    def draw(self, surf):
        for block in self.blocks:
            block.draw(surf, wireframe=True)
