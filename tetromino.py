from setup import *
from block import Block


class Tetromino:
    gravity_time = 250
    shapes = {
        "O": ((1, 1), (0, 1), (0, 0), (1, 0)),
        "I": ((-1, 0), (0, 0), (1, 0), (2, 0)),
        "J": ((0, 1), (-1, 1), (1, 1), (-1, 0)),
        "L": ((0, 1), (-1, 1), (1, 1), (1, 0)),
        "S": ((-1, 1), (0, 1), (0, 0), (1, 0)),
        "T": ((-1, 1), (0, 1), (1, 1), (0, 0)),
        "Z": ((0, 1), (1, 1), (-1, 0), (0, 0))
    }
    colours = [ 
                RED,
                PURPLE, 
                BLUE, 
                AQUA, 
                ORANGE, 
                YELLOW, 
                GREEN
    ]

    # Data from https://tetris.wiki/Super_Rotation_System#Wall_Kicks
    # J, L, S, T, Z Tetromino Wall Kick Data
    wall_kick_tests = {
        "0-1": ((0, 0), (-1, 0), (-1, -1), (0, +2), (-1, +2)),
        "1-0": ((0, 0), (+1, 0), (+1, +1), (0, -2), (+1, -2)),
        "1-2": ((0, 0), (+1, 0), (+1, +1), (0, -2), (+1, -2)),
        "2-1": ((0, 0), (-1, 0), (-1, -1), (0, +2), (-1, +2)),
        "2-3": ((0, 0), (+1, 0), (+1, -1), (0, +2), (+1, +2)),
        "3-2": ((0, 0), (-1, 0), (-1, +1), (0, -2), (-1, -2)),
        "3-0": ((0, 0), (-1, 0), (-1, +1), (0, -2), (-1, -2)),
        "0-3": ((0, 0), (+1, 0), (+1, -1), (0, +2), (+1, +2))
    }
    # I Tetromino Wall Kick Data
    I_wall_kick_tests = {
        "0-1": ((0, 0), (-2, 0), (+1, 0), (-2, +1), (+1, -2)),
        "1-0": ((0, 0), (+2, 0), (-1, 0), (+2, -1), (-1, +2)),
        "1-2": ((0, 0), (-1, 0), (+2, 0), (-1, -2), (+2, +1)),
        "2-1": ((0, 0), (+1, 0), (-2, 0), (+1, +2), (-2, -1)),
        "2-3": ((0, 0), (+2, 0), (-1, 0), (+2, -1), (-1, +2)),
        "3-2": ((0, 0), (-2, 0), (+1, 0), (-2, +1), (+1, -2)),
        "3-0": ((0, 0), (+1, 0), (-2, 0), (+1, +2), (-2, -1)),
        "0-3": ((0, 0), (-1, 0), (+2, 0), (-1, -2), (+2, +1))
    }

    
    def __init__(self, global_blocks):
        # self.shape = random.choice(list(self.shapes.keys()))
        self.shape = "I"
        self.colour = random.choice(self.colours)
        self.blocks = []
        for x,y in self.shapes[self.shape]:
            self.blocks.append(Block(((6 + x) * Block.side_length, y * Block.side_length), self.colour))
        
        self.other_blocks = global_blocks[:] # global_blocks.copy

        for b in self.blocks:
            global_blocks.append(b)


        self.time = 0
        self.has_fallen = False

        self.rotations = 0
        self.rotation_center = pygame.Vector2((-1 + 6) * Block.side_length, -1 * Block.side_length)



    def update(self, delta):
        self.time += delta

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_d:
                    can_move = True
                    for block in self.blocks:
                        if not block.can_move_right(self.other_blocks):
                            can_move = False
                    if can_move:
                        for block in self.blocks:
                            block.position.x += block.side_length
                        self.rotation_center.x += Block.side_length
                            
                elif event.key == pygame.K_a:
                    can_move = True
                    for block in self.blocks:
                        if not block.can_move_left(self.other_blocks):
                            can_move = False
                    if can_move:
                        for block in self.blocks:
                            block.position.x -= block.side_length
                        self.rotation_center.x -= Block.side_length

                elif event.key == pygame.K_s:
                    self.move_down()
                elif event.key == pygame.K_r:
                    self.rotate()

        if self.time >= self.gravity_time:
            self.move_down()
            self.time = 0  

    
    def move_down(self):
        can_move = True
        for block in self.blocks:
            if not block.can_move_down(self.other_blocks):
                can_move = False
            if block.has_fallen: # == True:
                self.has_fallen = True
        if can_move:
            for block in self.blocks:
                block.move_down()
            self.rotation_center.y += Block.side_length
    

    def rotate(self): # rotate the tetromino
        if self.shape == "O":
            return
        
        grid = []
        if self.shape != "I":
            grid_length = 3
            n = 0
        else:
            grid_length = 4
            n = 1

        for row in range(grid_length):
            grid.append([])
            for val in range(grid_length):
                grid[-1].append(0)
        
        for x,y in self.shapes[self.shape]:
            grid[y + n][x + 1] = 1 # representing a block

        def rotate_clockwise():
            temp = []
            for r in grid:
                temp.append([])
                for v in r:
                    temp[-1].append(v)

            for i in range(len(grid[0])):
                for j in range(len(grid)):
                    grid[i][j] = temp[j][i]
                grid[i].reverse()
            
        rotations = (self.rotations + 1) % 4

        for rotation in range(rotations):
            rotate_clockwise()
        
        new_block_positions = []
        for y, row in enumerate(grid):
            for x, val in enumerate(row):
                if val == 1:
                    new_block_positions.append((self.rotation_center.x + x * Block.side_length,
                                                self.rotation_center.y + y * Block.side_length))


        if self.shape != "I":
            test_cases = self.wall_kick_tests[f'{(rotations - 1) % 4}-{rotations}']
        else:
            test_cases = self.I_wall_kick_tests[f'{(rotations - 1) % 4}-{rotations}']


        for test_x,test_y in test_cases:
            rotated = True
            for block,position in zip(self.blocks, new_block_positions):
                if block.is_colliding(pygame.Vector2(position) + 
                    pygame.Vector2(test_x * Block.side_length,test_y * Block.side_length), self.other_blocks):
                    rotated = False
            
            if rotated:
                for block,position in zip(self.blocks, new_block_positions): 
                    block.position = pygame.Vector2(position) + pygame.Vector2(test_x * Block.side_length,test_y * Block.side_length)
                self.rotation_center += pygame.Vector2(test_x * Block.side_length,test_y * Block.side_length)
                self.rotations = rotations
                break
        