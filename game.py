from setup import *
from block import Block
from tetromino import Tetromino
from playable_tetromino import PlayableTetromino
from walls import Walls


class Game:

    def __init__(self):
        self.global_blocks = []
        self.cycle = self.get_cycle()
        self.counter = 0
        self.tetromino = PlayableTetromino(self.global_blocks, self.cycle[0])

        self.walls = Walls()

        self.score = 0

        self.tetrominos_list = []

    
    def update(self, delta):
        for i, t in enumerate(self.tetrominos_list):
            t.update(delta)
            if t.has_fallen:
                del self.tetrominos_list[i]



        self.tetromino.update(delta)
        if self.tetromino.has_fallen:
            self.counter += 1
            self.tetromino = PlayableTetromino(self.global_blocks, self.cycle[self.counter % len(self.cycle)])

        grid = [[None for i in range(GRID_LENGTH)] for i in range(GRID_HEIGHT)]


        for block in self.global_blocks:
            grid[int(block.position.y // Block.side_length)][int(block.position.x // Block.side_length)] = block


        cleared_line = False

        for r, row in enumerate(grid):
            block_counter = 0
            for val in row:
                if isinstance(val, Block):
                    block_counter += 1
            
            if block_counter >= GRID_LENGTH - 2:
                print("Line Clear!")
                self.score += 1

                for block in row:
                    if block in self.global_blocks:
                        self.global_blocks.remove(block)
                
                grid[r] = [None for i in range(GRID_LENGTH)]
                cleared_line = True
        
        if cleared_line:
            self.detect_tetrominos(grid)
        
        # # printing out the grid do not need to copy
        # print()
        # for row in grid:
        #     print(*row)
        # print()

    def detect_tetrominos(self, grid):
        seen = set()

        # Depth First Search
        def DFS(x, y, current_tetromino):
            if grid[y][x] in seen:
                # we have already seen this
                return
            else:
                seen.add(grid[y][x])
                current_tetromino.append(grid[y][x])
            
            # check to the right 
            if x + 1 < GRID_LENGTH - 1 and isinstance(grid[y][x + 1], Block):
                DFS(x + 1, y, current_tetromino)
            
            # check to the left
            if x - 1 > 0 and isinstance(grid[y][x - 1], Block):
                DFS(x - 1, y, current_tetromino)
            
            # Check above
            if y + 1 < GRID_HEIGHT - 1 and isinstance(grid[y - 1][x], Block):
                DFS(x, y - 1, current_tetromino)

            # Check Below
            if y - 1 > 0 and isinstance(grid[y + 1][x], Block):
                DFS(x, y + 1, current_tetromino)
            
        for y, row in enumerate(grid):
            for x, val in enumerate(row):
                if isinstance(val, Block) and val not in seen:
                    current_tetromino = []
                    DFS(x, y, current_tetromino)
                    self.tetrominos_list.append(Tetromino(self.global_blocks, current_tetromino))
        
            
            
            

    def draw(self, screen):
        for block in self.global_blocks:
            block.draw(screen)
        self.walls.draw(screen)


    def get_cycle(self):
        choices = list(PlayableTetromino.shapes.keys()) # gives us this ["O", "I", "J", "L", "S", "T", "Z"]
        cycle = []
        for i in range(len(choices)):
            choice = random.choice(choices)
            choices.remove(choice)
            cycle.append(choice)
        return cycle