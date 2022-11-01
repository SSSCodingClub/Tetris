from setup import *
from block import Block
from tetromino import Tetromino
from walls import Walls



class Game:

    def __init__(self):
        self.global_blocks = []
        self.cycle = self.get_cycle()
        self.counter = 0
        self.tetromino = Tetromino(self.global_blocks, self.cycle[0])

        self.walls = Walls()

        self.score = 0

    
    def update(self, delta):
        self.tetromino.update(delta)
        if self.tetromino.has_fallen:
            self.counter += 1
            self.tetromino = Tetromino(self.global_blocks, self.cycle[self.counter % len(self.cycle)])

        grid = [[None for i in range(GRID_LENGTH)][:] for i in range(GRID_HEIGHT)]


        for block in self.global_blocks:
            grid[int(block.position.y // Block.side_length)][int(block.position.x // Block.side_length)] = block


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
                
                grid[r] = [None for i in range(GRID_LENGTH)][:]
        
        # # printing out the grid do not need to copy
        # print()
        # for row in grid:
        #     print(*row)
        # print()

    def draw(self, screen):
        for block in self.global_blocks:
            block.draw(screen)
        self.walls.draw(screen)


    def get_cycle(self):
        choices = list(Tetromino.shapes.keys()) # gives us this ["O", "I", "J", "L", "S", "T", "Z"]
        cycle = []
        for i in range(len(choices)):
            choice = random.choice(choices)
            choices.remove(choice)
            cycle.append(choice)
        return cycle