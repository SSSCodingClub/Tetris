from setup import *


# tetrominoes fun
class Block:
    side_length: int = 30

    def __init__(self, pos):
        self.position: pygame.Vector2 = pygame.Vector2(pos)

    def update(self):
        self.position.y += self.side_length

    def draw(self, surf: pygame.Surface):
        r = pygame.Rect(self.position.x, self.position.y, self.side_length, self.side_length)
        pygame.draw.rect(surf, (255, 0, 0), r)
