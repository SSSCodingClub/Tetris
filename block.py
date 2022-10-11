from setup import *

class Block:
    side_length = 30

    def __init__(self, position, colour):
        self.position = pygame.Vector2(position)
        self.colour = colour
        self.has_fallen = False

    def can_move_down(self, collision_blocks):
        #Going down means y value increases
        if self.position.y + self.side_length >= SCREEN_HEIGHT:
            self.has_fallen = True
            return False
        # Check if collide with blocks going down
        for block in collision_blocks:
            if (self.position.x < block.position.x + block.side_length and
                self.position.x + self.side_length > block.position.x and
                self.position.y + self.side_length < block.position.y + block.side_length and
                self.position.y + self.side_length * 2 > block.position.y):# AABB Collision
                self.has_fallen = True
                return False
        return True
    
    def can_move_left(self, collision_blocks):
        if self.position.x <= 0:
            return False
        for block in collision_blocks:
            if (self.position.x - self.side_length < block.position.x + block.side_length and
                self.position.x > block.position.x and
                self.position.y < block.position.y + block.side_length and
                self.position.y + self.side_length > block.position.y):# AABB Collision
                return False
        return True

    def can_move_right(self, collision_blocks):
        if self.position.x + self.side_length >= SCREEN_WIDTH:
            return False
        for block in collision_blocks:
            if (self.position.x + self.side_length < block.position.x + block.side_length and
                self.position.x + self.side_length * 2 > block.position.x and
                self.position.y < block.position.y + block.side_length and
                self.position.y + self.side_length > block.position.y):# AABB Collision
                return False
        return True

    def move_down(self):
        self.position.y += self.side_length
      
    def draw(self, screen):
        rect = pygame.Rect(self.position.x, self.position.y, self.side_length, self.side_length)
        pygame.draw.rect(screen, self.colour, rect)
