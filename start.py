from setup import *


class Start:
    bold_font = pygame.font.Font("font/Silkscreen-Bold.ttf", 75)
    title = bold_font.render("TETRIS", True, YELLOW)

    regular_font = pygame.font.Font("font/Silkscreen-Regular.ttf", 15)
    subtitle = regular_font.render("Press any button to play!", True, LIGHT_GRAY)


    def __init__(self):
        pass

    def update(self, delta):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return COMMAND_EXIT
            if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                return COMMAND_START

    def draw(self, screen):
        screen.fill(DARK_GRAY)

        screen.blit(self.title, self.title.get_rect(center = (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 3)))
        
        display_subtitle = pygame.transform.scale(self.subtitle, (
            self.subtitle.get_width() * (0.15 * math.sin(time.time() * 2) + 1.15),
            self.subtitle.get_height() * (0.15 * math.sin(time.time() * 2) + 1.15)
            ))
        
        screen.blit(display_subtitle, display_subtitle.get_rect(center = (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)))
