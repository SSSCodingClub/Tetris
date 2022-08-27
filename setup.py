import pygame
from random import choice
from math import ceil,floor
pygame.init()

SCREEN_WIDTH, SCREEN_HEIGHT = 30 * 12, 30 * 21
dimensions = (SCREEN_WIDTH, SCREEN_HEIGHT)

pygame.display.set_caption("Tetris")
# icon = pygame.image.load("logo.ico")
# icon = pygame.transform.scale(icon, (32, 32))
# pygame.display.set_icon(icon)

clock = pygame.time.Clock()
fps = 120


class Colour:
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    GRAY = (127, 127, 127)
    DARK_GRAY = (40, 40, 40)
    LIGHT_GRAY = (225, 225, 225)
    RED = (204, 0, 0)
