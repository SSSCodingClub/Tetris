import pygame

from setup import *


class Grid:
    width = 10
    height = 20

    cell_length = 40

    def __init__(self):
        self.grid = [[None for _ in range(self.height)] for _ in range(self.width)]

    def update(self, blocks):
        for block in blocks:
            x, y = block.grid_pos
            self.grid[int(x)][int(y)] = block

    def draw(self, surf):
        pass


class Block:
    length = Grid.cell_length

    def __init__(self, pos):
        self.grid_pos = pygame.Vector2(pos)
        self.display_pos = pygame.Vector2(self.grid_pos.x * Grid.cell_length,
                                          self.grid_pos.y * Grid.cell_length)
        self.velocity = pygame.Vector2(0, 0)
        self.initial_pos = pygame.Vector2(pos)

    def update(self, delta, gravity, blocks):
        self.velocity.y = gravity * delta
        next_display_pos, next_grid_pos = self.get_move(display_offset=self.velocity)
        for block in blocks:
            if block is self:
                continue
            if block.get_rect().colliderect(self.get_rect(next_display_pos)):
                if self.velocity.y > 0:
                    self.display_pos.y = block.display_pos.y - self.length
                    self.grid_pos.y = block.grid_pos.y - 1
                return

        self.move(next_display_pos, next_grid_pos)

    def get_move(self, grid_offset=pygame.Vector2(0, 0), display_offset=pygame.Vector2(0, 0)):
        d = pygame.Vector2(min((Grid.width - 1) * Grid.cell_length - self.length,
                               max(0, int(self.display_pos.x + display_offset.x))),
                           min((Grid.height - 1) * Grid.cell_length - self.length,
                               max(0, int(self.display_pos.y + display_offset.y))))
        g = pygame.Vector2(min(Grid.width - 1, max(0, int(self.display_pos.x // Grid.cell_length))),
                           min(Grid.height - 1, max(0, int(self.display_pos.y // Grid.cell_length))))
        return d, g

    def move(self, d,g):
        self.display_pos = d
        self.grid_pos = g

    def get_rect(self, pos=None):
        if pos is None:
            pos = self.display_pos
        return pygame.Rect(pos, (self.length, self.length))

    def draw(self, surf):
        r = pygame.Rect(self.grid_pos.x * self.length,
                        self.grid_pos.y * self.length,
                        self.length,
                        self.length)
        pygame.draw.rect(surf, Colour.RED, r)


class BlockManager:

    def __init__(self):
        self.blocks = []
        self.gravity = 0.25

    def add(self, block):
        self.blocks.append(block)

        def get_y(block):
            return block.grid_pos.y

        self.blocks.sort(key=get_y, reverse=True)  # we do this so that things are checked from bottom to top

    def next_level(self):
        self.gravity += 1

    def update(self, delta):
        for block in self.blocks:
            block.update(delta, self.gravity, self.blocks)

    def draw(self, surf):
        for block in self.blocks:
            block.draw(surf)


class Tetrione:
    shapes = [
        [[0, 0], [0, 1], [1, 0], [1, 1]],
    ]

    def __init__(self, blockmanager):
        self.shape = choice(self.shapes)
        self.blockmanager = blockmanager
        for coords in self.shape:
            self.blockmanager.add(Block(coords))
        self.prev_mouse_pos = pygame.mouse.get_pos()

    def update(self, delta):
        offset = pygame.Vector2(pygame.mouse.get_pos()[0] - self.prev_mouse_pos[0], 0)
        self.prev_mouse_pos = pygame.mouse.get_pos()

        for block in self.blockmanager.blocks:
            # print(block.initial_pos)
            # block.display_pos.x = block.initial_pos.x * block.length + ceil(pygame.mouse.get_pos()[0])
            a,b = block.get_move(display_offset=offset)
            print(a,b)
            block.move(a,b)


class TetrioneManager:

    def __init__(self, blockmanager):
        self.tetrione = None
        self.blockmanager = blockmanager

    def add(self):
        self.tetrione = Tetrione(self.blockmanager)

    def update(self, delta):
        self.tetrione.update(delta)


class Game:

    def __init__(self):
        self.grid = Grid()
        self.block_manager = BlockManager()
        self.tetrione_manager = TetrioneManager(self.block_manager)

        # self.block_manager.add(Block((0, 0)))

        # Tetrione(self.block_manager)
        self.tetrione_manager.add()

    def update(self, delta):
        self.block_manager.update(delta)
        self.grid.update(self.block_manager.blocks)
        self.tetrione_manager.update(delta)

    def draw(self, surf):
        surf.fill(Colour.BLACK)

        self.grid.draw(surf)
        self.block_manager.draw(surf)
