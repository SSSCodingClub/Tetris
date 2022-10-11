from setup import *
from block import Tetrominoe, Block


class FakeTetrominoes:
    gravity_time = Tetrominoe.gravity_time
    shapes = Tetrominoe.shapes
    colours = Tetrominoe.colours

    def __init__(self):
        self.blocks = []
        for i in range(4):
            self.add_shape()

        self.time = 0
        self.remove_counter = 0

    def add_shape(self):
        colour = random.choice(self.colours)
        shape = random.choice(list(self.shapes.keys()))
        dx, dy = random.randint(1, 9), random.randint(-GRID_HEIGHT * 2, -1)
        for coords in self.shapes[shape]:
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


class GameOver:
    bold_font = pygame.font.Font("font/Silkscreen-Bold.ttf", 40)
    regular_font = pygame.font.Font("font/Silkscreen-Regular.ttf", 12)
    regular_font2 = pygame.font.Font("font/Silkscreen-Regular.ttf", 20)
    title = bold_font.render("GameOver!", True, Colour.RED)
    subtitle = regular_font.render("Press any key to continue...", True, Colour.LIGHT_GRAY)

    gameovercard = pygame.Surface(dimensions)
    dark = pygame.Surface(dimensions)
    dark.fill(Colour.DARK_GRAY)
    dark.set_alpha(125)

    def __init__(self, score):
        self.score = score
        self.score_text = self.regular_font2.render(f"Score:{self.score}", True, Colour.LIGHT_GRAY)
        self.next_scene = None
        self.saved_bg = False
        self.bg = None
        self.time = 0

    def update(self, delta):
        if self.time < 10000:
            self.time += delta

        for event in pygame.event.get():
            if self.time > 4500 and (event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN):
                self.next_scene = "Game"

    def draw(self, surf):
        if not self.saved_bg:
            self.bg = surf.copy()
            self.saved_bg = True

        self.gameovercard.blit(self.bg, self.bg.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)))

        # surf.blit(self.gameovercard, self.gameovercard.get_rect(center=(SCREEN_WIDTH/2,SCREEN_HEIGHT/2)))
        self.gameovercard.blit(self.dark, self.dark.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)))

        self.gameovercard.blit(self.title, self.title.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 3)))

        self.gameovercard.blit(self.score_text,
                               self.score_text.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT * 0.425)))

        display_subtitle = pygame.transform.scale(self.subtitle, (
            self.subtitle.get_width() * (0.15 * math.sin(time.time() * 2) + 1.15),
            self.subtitle.get_height() * (0.15 * math.sin(time.time() * 2) + 1.15)))
        self.gameovercard.blit(display_subtitle,
                               display_subtitle.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)))

        self.gameovercard.set_alpha(min(255, pow(0.99, -0.1 * (self.time - 1250))))

        surf.blit(self.gameovercard, self.gameovercard.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)))

class Pause:
    dark = pygame.Surface(dimensions)
    dark.fill(Colour.DARK_GRAY)
    dark.set_alpha(25)
    regular_font = pygame.font.Font("font/Silkscreen-Regular.ttf", 20)
    text = regular_font.render("Paused",True,Colour.WHITE)

    def __init__(self):
        self.copied_bg = False
        self.bg = None
        self.unpaused = False

    def update(self, delta):
        self.unpaused = False
        mixer.music.set_volume(0)
        for event in pygame.event.get((pygame.KEYDOWN, pygame.MOUSEBUTTONDOWN)):
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.copied_bg = False
                    mixer.music.set_volume(0.25)

                    self.unpaused = True
                    return True
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self.copied_bg = False
                self.unpaused = True
                mixer.music.set_volume(0.25)

                return True
        return False


    def draw(self, surf):
        if not self.unpaused:
            if not self.copied_bg:
                self.bg = surf.copy()
                self.copied_bg = True
            surf.blit(self.bg, (0,0))
            surf.blit(self.dark,(0,0))
            surf.blit(self.text,self.text.get_rect(center=(SCREEN_WIDTH/2,SCREEN_HEIGHT/3)))
