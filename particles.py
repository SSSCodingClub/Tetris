from setup import *

class Particle:
    gravity = 600

    def __init__(self, position, velocity, colour):
        self.position = pygame.Vector2(position)
        self.velocity = pygame.Vector2(velocity)
        self.acceleration = pygame.Vector2(0, self.gravity)
        self.colour = colour
        self.outline_color = (max(self.colour[0] - 100, 0), max(self.colour[1] - 100, 0), max(self.colour[2] - 100, 0))
        self.side_length = random.randint(5, 12)

    def update(self, delta):
        self.position += pygame.Vector2(self.velocity.x * delta / 1000, self.velocity.y * delta / 1000)
        self.velocity += pygame.Vector2(self.acceleration.x * delta / 1000, self.acceleration.y * delta / 1000)

    def is_out_of_bounds(self): # if off the screen, can't see them anymore
        if self.position.y >= SCREEN_HEIGHT: # below bottom of the screen
            return True
        return False

    def draw(self, screen):
        r = pygame.Rect(self.position, (self.side_length, self.side_length))
        pygame.draw.rect(screen, self.colour, r)
        pygame.draw.rect(screen, self.outline_color, r, 2) 


class BlockFall:

    def __init__(self, block, intensity, amount):
        self.position = pygame.Vector2(block.position)
        self.amount = amount
        self.particles = [Particle(self.position + pygame.Vector2(random.random() * 15 - 15 / 2, 30), 
                        (intensity * random.random() - intensity / 2, intensity * random.random() - intensity * 0.9),
                        block.colour) for i in range(self.amount)]

    def update(self, delta):
        for particle in self.particles:
            particle.update(delta)
            if particle.is_out_of_bounds():
                self.particles.remove(particle)

    def is_finished(self):
        if len(self.particles) == 0:
            return True
        return False

    def draw(self, screen):
        for particle in self.particles:
            particle.draw(screen)