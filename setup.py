import pygame
import time
import random
import math


pygame.init()

GRID_LENGTH, GRID_HEIGHT = 12, 21
SCREEN_WIDTH, SCREEN_HEIGHT = 30 * GRID_LENGTH, 30 * GRID_HEIGHT

#Tuple
dimensions = (SCREEN_WIDTH, SCREEN_HEIGHT)

#Display screen
screen = pygame.display.set_mode(dimensions)
screen_center = pygame.Vector2(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)

#Screen name
pygame.display.set_caption("Tetris")

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

COMMAND_EXIT = 0
COMMAND_START = 1
COMMAND_GAME_OVER = 2
