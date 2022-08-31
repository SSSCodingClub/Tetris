import pygame

from setup import *


class Grid:
    width = 10
    height = 20

    cell_length = 30

    def draw(self, surf):
        pass


class Block:
    length = Grid.cell_length

    def __init__(self, pos):
        self.position = pygame.Vector2(pos)
        self.initial_position = pygame.Vector2(pos)
        self.falling = True
        self.collided_x = False

    def sort_list(self, direction, lis):
        def get_y(b):
            return b.position.y
        def get_x(b):
            return b.position.x

        match direction:
            case 'up':
                lis.sort(key=get_y)
            case 'down':
                lis.sort(key=get_y, reverse=True)
            case 'right':
                lis.sort(key=get_x)
            case 'left':
                lis.sort(key=get_x, reverse=True)
        return lis

    def update(self, x_offset, gravity, blocks):
        next_position = pygame.Vector2(min(Grid.width - 1, max(0, self.position.x + x_offset)),
                                       min(Grid.height - 1, max(0, self.position.y + gravity)))

        self.check_x(x_offset,blocks,next_position)
        self.check_y(gravity,blocks,next_position)



    def check_x(self, x_offset, blocks, next_position):
        if x_offset > 0:
            blocks = self.sort_list('left', blocks)
        elif x_offset < 0:
            blocks = self.sort_list('right', blocks)

        if x_offset != 0:
            temp = []
            for i in blocks:
                temp.append(i.position.x)
            print(temp)

        if self.position.x == Grid.width - 1:
            self.collided_x = True
        else:
            self.collided_x = False

        for block in blocks:
            if block is not self and block.position == next_position:
                return
        self.position.x = next_position.x

    def check_y(self, gravity, blocks, next_position):
        if gravity >= 0:
            blocks = self.sort_list('down', blocks)
        else:
            blocks = self.sort_list('up', blocks)

        for block in blocks:
            if block is not self and block.position == next_position:
                return
        self.position.y = next_position.y
    def draw(self, surf):
        r = pygame.Rect((self.position.x * self.length, self.position.y * self.length), (self.length, self.length))
        pygame.draw.rect(surf, Colour.RED, r)


class BlockManager:
    gravity = 1

    def __init__(self):
        self.blocks = []
        self.falling_blocks = []

        self.time_to_move = 500
        self.gravity_time = 0

    def add(self, block):
        self.blocks.append(block)
        self.falling_blocks.append(block)

        def get_y(b):
            return b.position.y

        self.blocks.sort(key=get_y, reverse=True)  # we do this so that things are checked from bottom to top

    def update(self, delta):
        self.gravity_time += delta

        if self.gravity_time >= self.time_to_move:
            gravity_modifier = 1
            self.gravity_time -= self.time_to_move
        else:
            gravity_modifier = 0

        x_offset = 0
        pressed = pygame.key.get_pressed()
        if pressed[pygame.K_a or pygame.K_LEFT]:
            x_offset = max(x_offset-1, -1)
        if pressed[pygame.K_d or pygame.K_RIGHT]:
            x_offset = min(x_offset + 1, 1)

        x_offset_modifier = 1
        for block in self.blocks:
            block.update(x_offset * x_offset_modifier, self.gravity * gravity_modifier, self.blocks)
            if block.collided_x:
                x_offset_modifier = 0

        # print()
    def draw(self, surf):
        for block in self.blocks:
            block.draw(surf)


class Tetrominoe:
    shapes = [
        [[0, 0], [0, 1], [1, 0], [1, 1]],
    ]

    def __init__(self, block_manager):
        self.shape = choice(self.shapes)
        self.block_manager = block_manager
        for coords in self.shape:
            self.block_manager.add(Block(coords))
        self.prev_mouse_pos = pygame.mouse.get_pos()

    def update(self, delta):
        pass


class TetrominoeManager:

    def __init__(self, block_manager):
        self.tetrominoe = None
        self.block_manager = block_manager

    def add(self):
        self.tetrominoe = Tetrominoe(self.block_manager)

    def update(self, delta):
        self.tetrominoe.update(delta)


class Game:

    def __init__(self):
        self.grid = Grid()
        self.block_manager = BlockManager()
        self.tetrominoe_manager = TetrominoeManager(self.block_manager)

        self.tetrominoe_manager.add()

    def update(self, delta):
        self.block_manager.update(delta)
        self.tetrominoe_manager.update(delta)

    def draw(self, surf):
        surf.fill(Colour.BLACK)

        self.grid.draw(surf)
        self.block_manager.draw(surf)
