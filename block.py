from setup import *

class Block:
    side_length = 30

    def __init__(self, position, colour):
        self.position = pygame.Vector2(position)
        self.colour = colour

    def can_move_down(self):
        #Going down means y value increases
        if self.position.y + self.side_length >= SCREEN_HEIGHT:
            return False
        else:
            return True
    
    def can_move_left(self):
        if self.position.x <= 0:
            return False
        else:
            return True

    def can_move_right(self):
        if self.position.x + self.side_length >= SCREEN_WIDTH:
            return False
        else:
            return True

    def move_down(self):
        self.position.y += self.side_length
      
    def draw(self, screen):
        rect = pygame.Rect(self.position.x, self.position.y, self.side_length, self.side_length)
        pygame.draw.rect(screen, self.colour, rect)
