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
    
    def __init__(self, global_blocks):
        self.shape = random.choice(list(self.shapes.values()))
        self.colour = random.choice(self.colours)
        self.blocks = []
        for x,y in self.shape:
            self.blocks.append(Block(((6 + x) * Block.side_length, y * Block.side_length), self.colour))
        
        self.other_blocks = global_blocks[:] # global_blocks.copy

        for b in self.blocks:
            global_blocks.append(b)


        self.time = 0
        self.has_fallen = False



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
                            
                elif event.key == pygame.K_a:
                    can_move = True
                    for block in self.blocks:
                        if not block.can_move_left(self.other_blocks):
                            can_move = False
                    if can_move:
                        for block in self.blocks:
                            block.position.x -= block.side_length

                elif event.key == pygame.K_s:
                    print("speed up!!!")
                    can_move = True
                    for block in self.blocks:
                        if not block.can_move_down(self.other_blocks):
                            can_move = False
                        if block.has_fallen: # == True:
                            self.has_fallen = True
                    if can_move:
                        for block in self.blocks:
                            block.move_down()
                elif event.key == pygame.K_r:
                    print("rotate")

        if self.time >= self.gravity_time:
            can_move = True
            for block in self.blocks:
                if not block.can_move_down(self.other_blocks):
                    can_move = False
                if block.has_fallen: # == True:
                    self.has_fallen = True
            if can_move:
                for block in self.blocks:
                    block.move_down()
            self.time = 0