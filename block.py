from setup import *


class Block:
    side_length = 30
    bezel = 3

    def __init__(self, position, colour):
        self.position = pygame.Vector2(position)
        self.colour = colour
        self.outline_colour = (max(self.colour[0] - 25, 0), max(self.colour[1] - 25, 0), max(self.colour[2] - 25, 0))
        self.has_fallen = False

    def is_colliding(self, position, collision_blocks):
        if not (Block.side_length <= position.x <= SCREEN_WIDTH - Block.side_length * 2 and
                0 <= position.y <= SCREEN_HEIGHT - Block.side_length * 2):
            return True
        for block in collision_blocks:
            if (position.x < block.position.x + block.side_length and
                position.x + self.side_length > block.position.x and
                position.y < block.position.y + block.side_length and
                position.y + self.side_length > block.position.y):# AABB Collision
                return True
        return False

    def can_move_down(self, collision_blocks):
        #Going down means y value increases
        if self.position.y + self.side_length >= SCREEN_HEIGHT - Block.side_length:
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
        if self.position.x <= Block.side_length:
            return False
        for block in collision_blocks:
            if (self.position.x - self.side_length < block.position.x + block.side_length and
                self.position.x > block.position.x and
                self.position.y < block.position.y + block.side_length and
                self.position.y + self.side_length > block.position.y):# AABB Collision
                return False
        return True

    def can_move_right(self, collision_blocks):
        if self.position.x + self.side_length >= SCREEN_WIDTH - Block.side_length:
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
        pygame.draw.rect(screen, self.outline_colour, rect, width = self.bezel)
