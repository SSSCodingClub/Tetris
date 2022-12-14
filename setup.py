import pygame
import time
import random
import math


pygame.init()
# pygame.mixer.init() called in the previous line

GRID_LENGTH, GRID_HEIGHT = 12, 21
SCREEN_WIDTH, SCREEN_HEIGHT = 30 * GRID_LENGTH, 30 * GRID_HEIGHT

#Tuple
dimensions = (SCREEN_WIDTH, SCREEN_HEIGHT)

screen_center = pygame.Vector2(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)

#Screen name
pygame.display.set_caption("Tetris")

icon = pygame.transform.scale(pygame.image.load("logo.png"), (32,32))
pygame.display.set_icon(icon)

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

# Sounds
sounds = {
    "game_over": pygame.mixer.Sound("sounds/game_over.wav"),
    "line_clear": pygame.mixer.Sound("sounds/line_clear.wav"),
    "move": pygame.mixer.Sound("sounds/move.wav"),
    "fall": pygame.mixer.Sound("sounds/fall.wav"),
    "rotate": pygame.mixer.Sound("sounds/rotate.wav")
}

sounds["line_clear"].set_volume(0.35)
sounds["fall"].set_volume(0.1)
sounds["move"].set_volume(0.33)
sounds["rotate"].set_volume(0.33)

# Music
pygame.mixer.music.load("sounds/TetrisTheme.wav")
pygame.mixer.music.set_volume(0.10)
pygame.mixer.music.play(-1) # Infinitely loops