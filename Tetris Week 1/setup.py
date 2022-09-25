import pygame


pygame.init()

GRID_LENGTH, GRID_HEIGHT = 12, 21
SCREEN_WIDTH, SCREEN_HEIGHT = 30 * GRID_LENGTH, 30 * GRID_HEIGHT
dimensions = (SCREEN_WIDTH, SCREEN_HEIGHT)

screen = pygame.display.set_mode(dimensions)

pygame.display.set_caption("Tetris")
