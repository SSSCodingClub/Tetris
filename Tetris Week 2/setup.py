import pygame
import random
pygame.init()

SCREEN_WIDTH, SCREEN_HEIGHT = 30 * 12, 30 * 21
dimensions: tuple = (SCREEN_WIDTH, SCREEN_HEIGHT)
screen: pygame.Surface = pygame.display.set_mode(dimensions)


pygame.display.set_caption("Tetris")
# icon = pygame.image.load("logo.ico")
# icon = pygame.transform.scale(icon, (32, 32))
# pygame.display.set_icon(icon)

clock = pygame.time.Clock()
fps = 60


class Colour:
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    GRAY = (127, 127, 127)
    DARK_GRAY = (40, 40, 40)
    LIGHT_GRAY = (225, 225, 225)
    RED = (255, 17, 0)
    PURPLE = (157, 0, 255)
    BLUE = (0, 21, 255)
    AQUA = (0, 225, 255)
    ORANGE = (255, 136, 0)
    YELLOW = (255, 225, 0)
    GREEN = (0, 255, 17)