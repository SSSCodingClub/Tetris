import pygame
pygame.init()

GRID_LENGTH, GRID_HEIGHT = 12, 21
SCREEN_WIDTH, SCREEN_HEIGHT = 30 * GRID_LENGTH, 30 * GRID_HEIGHT
dimensions: tuple = (SCREEN_WIDTH, SCREEN_HEIGHT)
screen: pygame.Surface = pygame.display.set_mode(dimensions)

pygame.display.set_caption("Tetris")
# icon = pygame.image.load("logo.png")
# icon = pygame.transform.scale(icon, (32, 32))
# pygame.display.set_icon(icon)

# clock = pygame.time.Clock()
# fps = 60

#
# class Colour:
#     BLACK = (0, 0, 0)
#     WHITE = (255, 255, 255)
#     GRAY = (127, 127, 127)
#     DARK_GRAY = (40, 40, 40)
#     LIGHT_GRAY = (225, 225, 225)
#     RED = (204, 0, 0)
