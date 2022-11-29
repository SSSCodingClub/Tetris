from setup import *
from playable_tetromino import PlayableTetromino
from tetromino import Tetromino
from block import Block


class BackgroundTetrominos:
    gravity_time = Tetromino.gravity_time
    shapes = PlayableTetromino.shapes
    colours = PlayableTetromino.colours

    def __init__(self):
        self.tetrominos = []
        for i in range(4):
            self.add_shape()
        
        self.time = 0
    
    def update(self, delta):
        self.time += delta
        for tetromino in self.tetrominos:
            if self.time >= self.gravity_time:
                for block in tetromino.blocks: 
                    block.position.y += Block.side_length

            is_below = True
            for block in tetromino.blocks:
                if block.position.y < SCREEN_HEIGHT:
                    is_below = False
            
            if is_below:
                self.tetrominos.remove(tetromino)
                self.add_shape()
        if self.time >= self.gravity_time:
            self.time = 0

    def draw(self, screen):
        for tetromino in self.tetrominos:
            for block in tetromino.blocks:
                block.draw(screen)


    def add_shape(self):
        blocks = []
        colour = random.choice(self.colours)
        shape = random.choice(list(self.shapes.keys()))
        dx, dy = random.randint(1, 9), random.randint(-GRID_HEIGHT * 2, -1)

        for coords in self.shapes[shape]:
            x, y = coords
            blocks.append(Block(((x + dx) * Block.side_length, (y + dy) * Block.side_length), colour))

        self.tetrominos.append(Tetromino([], blocks))


class Start:
    bold_font = pygame.font.Font("font/Silkscreen-Bold.ttf", 75)
    title = bold_font.render("TETRIS", True, YELLOW)

    regular_font = pygame.font.Font("font/Silkscreen-Regular.ttf", 15)
    subtitle = regular_font.render("Press any button to play!", True, LIGHT_GRAY)


    def __init__(self):
        self.background_tetrominos = BackgroundTetrominos()

    def update(self, delta):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return COMMAND_EXIT
            if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                return COMMAND_START

        self.background_tetrominos.update(delta)

    def draw(self, screen):
        screen.fill(DARK_GRAY)

        self.background_tetrominos.draw(screen)

        screen.blit(self.title, self.title.get_rect(center = (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 3)))
        
        display_subtitle = pygame.transform.scale(self.subtitle, (
            self.subtitle.get_width() * (0.15 * math.sin(time.time() * 2) + 1.15),
            self.subtitle.get_height() * (0.15 * math.sin(time.time() * 2) + 1.15)
            ))
        
        screen.blit(display_subtitle, display_subtitle.get_rect(center = screen_center))
