from setup import *

class GameOver:
    bold_font = pygame.font.Font("font/Silkscreen-Bold.ttf", 40)
    subtitle_font = pygame.font.Font("font/Silkscreen-Regular.ttf", 12)
    subtitle_font2 = pygame.font.Font("font/Silkscreen-Regular.ttf", 20)

    # render the text GAMEOVER!
    title = bold_font.render("GAMEOVER!", True, RED)
    subtitle = subtitle_font.render("Press any key to continue...", True, LIGHT_GRAY)

    # This will have all the text
    game_over_card = pygame.Surface(dimensions, pygame.SRCALPHA)
    # gives alpha value for pixel individually

    # darkness 
    dark = pygame.Surface(dimensions)
    dark.fill(DARK_GRAY)
    # 0 is transparent and 255 is opaque
    dark.set_alpha(125) # Transparency RGBA <- alpha 
    
    def __init__(self, score):
        self.score = score # so we can display it
        self.score_text = self.subtitle_font2.render(f"Score:{self.score}", True, LIGHT_GRAY)

        self.time = 0 # track how far we are into the animation

        self.background = None # store the screen as the game ends
    
    def update(self, delta):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return COMMAND_EXIT
            # condition to check if player wants to play again
            if self.time > 4500 and (event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN):
                return COMMAND_START # restart the game
        
        if self.time < 10000:
            self.time += delta # delta is the time in between frames
        
    def draw(self, screen):
        if self.background is None:
            self.background = screen.copy() 
            # since we set it the screen, it won't be none anymore

        self.game_over_card.fill((0,0,0,0)) # transparent background for the text
        self.game_over_card.blit(self.title, self.title.get_rect(center = pygame.Vector2(SCREEN_WIDTH/2, SCREEN_HEIGHT/3)))
        self.game_over_card.blit(self.score_text, self.score_text.get_rect(center = pygame.Vector2(SCREEN_WIDTH/2, SCREEN_HEIGHT * 0.425)))
        
        display_subtitle = pygame.transform.scale(self.subtitle, 
        (self.subtitle.get_width() * (0.15 * math.sin(time.time() * 2) + 1.15),
        self.subtitle.get_height() * (0.15 * math.sin(time.time() * 2) + 1.15))
        )
        
        self.game_over_card.blit(display_subtitle, display_subtitle.get_rect(center=screen_center))

        screen.blit(self.background, self.background.get_rect(center=screen_center))

        self.dark.set_alpha(min(125, pow(0.99, -0.2 * self.time)))
        self.game_over_card.set_alpha(min(255, pow(0.99, -0.2 * (self.time - 1000))))

        screen.blit(self.dark, self.dark.get_rect(center=screen_center))
        screen.blit(self.game_over_card, self.game_over_card.get_rect(center = screen_center))

