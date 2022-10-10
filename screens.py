from setup import *
from block import Tetrominoe, Block


class FakeTetrominoes:
    gravity_time = Tetrominoe.gravity_time
    shapes = Tetrominoe.shapes
    colours = Tetrominoe.colours

    def __init__(self):
        self.blocks = []
        for i in range(3):
            self.add_shape()

        self.time = 0
        self.remove_counter = 0

    def add_shape(self):
        colour = random.choice(self.colours)
        self.shape = random.choice(list(self.shapes.keys()))
        dx, dy = random.randint(1, 10), random.randint(-GRID_HEIGHT, -1)
        for coords in self.shapes[self.shape]:
            x, y = coords
            self.blocks.append(Block(((x + dx) * Block.side_length, (y + dy) * Block.side_length), colour))

    def update(self, delta):
        self.time += delta
        if self.time >= self.gravity_time:
            self.time = 0
            for block in self.blocks:
                block.position.y += block.side_length

        for block in self.blocks:
            if block.position.y >= SCREEN_HEIGHT:
                self.blocks.remove(block)
                self.remove_counter += 1
                if self.remove_counter % 4 == 0:
                    self.remove_counter = 0
                    self.add_shape()

    def draw(self, surf):
        for block in self.blocks:
            block.draw(surf)


class Title:
    bold_font = pygame.font.Font("font/Silkscreen-Bold.ttf", 75)
    regular_font = pygame.font.Font("font/Silkscreen-Regular.ttf", 15)
    title = bold_font.render("Tetris", True, Colour.YELLOW)
    subtitle = regular_font.render("Press any button to play!", True, Colour.LIGHT_GRAY)

    def __init__(self):
        self.next_scene = None
        self.t = FakeTetrominoes()

    def update(self, delta):
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                self.next_scene = "Game"
        self.t.update(delta)

    def draw(self, surf):
        surf.fill(Colour.DARK_GRAY)

        self.t.draw(surf)

        surf.blit(self.title, self.title.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 3)))

        display_subtitle = pygame.transform.scale(self.subtitle, (
            self.subtitle.get_width() * (0.15 * math.sin(time.time() * 2) + 1.15),
            self.subtitle.get_height() * (0.15 * math.sin(time.time() * 2) + 1.15)))
        surf.blit(display_subtitle, display_subtitle.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)))
