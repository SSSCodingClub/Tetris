import random

import pygame

from setup import *


class Particle:
    gravity =600

    def __init__(self, pos, vel, colour):
        self.position = pygame.Vector2(pos)
        self.velocity = pygame.Vector2(vel)
        self.acceleration = pygame.Vector2(0,self.gravity)
        self.side = random.randint(5,12)
        self.r = pygame.Rect(self.position, (self.side,self.side))
        self.colour = colour
        self.outline_colour = (max(self.colour[0] - 100, 0), max(self.colour[1] - 100, 0), max(self.colour[2] - 100, 0))
    def update(self,delta):
        self.position.x += self.velocity.x * delta/1000
        self.position.y += self.velocity.y * delta/1000
        self.velocity.x += self.acceleration.x * delta/1000
        self.velocity.y += self.acceleration.y * delta/1000
        self.r = pygame.Rect(self.position, (self.side, self.side))

        # print(delta)

    def draw(self,surf):
        pygame.draw.rect(surf,self.colour,self.r)
        pygame.draw.rect(surf,self.outline_colour,self.r,2)

class BlockHit:

    def __init__(self, block, intensity, amount, effect_list):
        self.effects = effect_list
        self.position = pygame.Vector2(block.position)
        self.time = 0
        self.amount = amount
        self.particles = [Particle(self.position + pygame.Vector2(random.random() * 15 - 15/2, 30), (intensity * random.random() - intensity/2,intensity * random.random()-intensity * 0.9), block.colour) for _ in range(self.amount)]
        sounds["place"].play()

    def update(self, delta):
        self.time += delta
        for e in self.particles:
            e.update(delta)
        if self.time >= 10000:
            if self in self.effects:
                self.effects.remove(self)

    def draw(self, surf):
        for e in self.particles:
            e.draw(surf)

class LineClear:
    min_time = 600

    def __init__(self, position, time_allowed, effect_list):
        self.position = pygame.Vector2(position)
        self.blocks = [pygame.Vector2((1+i) * 30, self.position.y) for i in range(GRID_WIDTH-2)]
        self.time = 0
        self.max_time = time_allowed
        self.effect_list = effect_list
        self.display = []
        sounds["line_break"].play()

    def update(self, delta):
        self.display = []
        for x,i in enumerate(self.blocks):#[:round(self.min_time/(self.time+1))]
            s = pow(0.99, self.time - 20) * 50
            self.display.append(pygame.Rect(x * 30 + 30+15-s/2, self.position.y-30+15-s/2,s,s))
            # temp = pygame.Surface((s,s))
            # pygame.draw.rect(temp,Colour.WHITE,pygame.Rect(0,0,s,s))#,border_radius=4
            # temp2=pygame.transform.rotate(temp,30)
            # self.display.append(temp2.copy())
            # del temp

        if self.time >= self.min_time:
            self.effect_list.remove(self)

        self.time += delta

    def draw(self, surf):
        for i,r in enumerate(self.display):
            # surf.blit(r,r.get_rect(center=(i * 30 + 15+30, self.position.y + 15 - 30)))
            pygame.draw.rect(surf,Colour.WHITE,r,border_radius=4)


class HardDrop:
    n=5 # number of squares the trail follows
    trail = []
    for i in range(n*6):
        t = pygame.Surface((30, 5))
        t.fill(Colour.WHITE)
        t.set_alpha(int(100 - (i+1) * 100/(n*6)))
        trail.append(t)
    trail2 =[]
    for i in range(n*6):
        t = pygame.Surface((60, 30))
        t.fill(Colour.WHITE)
        t.set_alpha(int(100 - (i+1) * 100/(n*6)))
        trail2.append(t)

    def __init__(self, blocks, effect_list):
        self.effects =effect_list
        self.time = 0
        self.blocks = []
        self.left = None
        self.middle = None
        self.right = None
        for b in blocks:
            self.blocks.append(b.position)
            if self.left is None or (b.position.x < self.left.position.x or (b.position.x == self.left.position.x and b.position.y <= self.left.position.y)):
                self.left = b
            if self.right is None or (b.position.x > self.right.position.x or (b.position.x == self.right.position.x and b.position.y <= self.right.position.y)):
                self.right = b

        if self.right.position.x > self.left.position.x + 30:
            self.middle= None
            m = pygame.Vector2(self.left.position.x + 30, SCREEN_HEIGHT)
            for b in blocks:
                if (self.middle is None and b.position.x == m.x and b.position.y < m.y) or (self.middle is not None and b.position.y < self.middle.position.y and b.position.x == self.middle.position.x):
                    self.middle = b
            # if self.minposx is None or b.position.x < self.minposx:
            #     self.minposx = b.position.x
            # if self.maxposx is None or b.position.x > self.maxposx:
            #     self.maxposx = b.position.x
            # if self.minposy is None or b.position.y < self.minposy:
            #     self.minposy = b.position.y
            # if self.maxposy is None or b.position.y > self.maxposy:
            #     self.maxposy = b.position.y



    def update(self, delta):
        self.time += delta
        if self.time > 500:
            self.effects.remove(self)

    def draw(self,surf):
        for i,j in enumerate(self.trail):
            surf.blit(j,j.get_rect(bottomleft=(self.left.position.x,self.left.position.y - i * 5)))
            if self.right.position.x > self.left.position.x:
                surf.blit(j,j.get_rect(bottomleft=(self.right.position.x,self.right.position.y - i * 5)))
            if self.right.position.x - (self.left.position.x+30) == 30:
                surf.blit(j,j.get_rect(bottomleft=(self.left.position.x+30,self.middle.position.y - i * 5)))


        if self.right.position.x - (self.left.position.x+30) > 30:
            for i,j in enumerate(self.trail2):
                surf.blit(j,j.get_rect(bottomleft=(self.left.position.x+30,self.middle.position.y - i * 5)))


        # l_trail = pygame.Surface((30, (self.n) * 30))
        # l_trail.fill(Colour.WHITE)
        # l_trail.set_alpha(70)
        # surf.blit(l_trail,l_trail.get_rect(bottomleft=(self.left.position.x,self.left.position.y)))
        #
        # if self.right.position.x - (self.left.position.x+30) > 0:
        #     m_trail = pygame.Surface((self.right.position.x - (self.left.position.x + 30), (self.n) * 30))
        #     m_trail.fill(Colour.WHITE)
        #     m_trail.set_alpha(70)
        #     surf.blit(m_trail,m_trail.get_rect(bottomleft=(self.left.position.x+30,self.middle.position.y)))
        #
        # if self.right.position.x > self.left.position.x:
        #     r_trail = pygame.Surface((30, (self.n) * 30))
        #     r_trail.fill(Colour.WHITE)
        #     r_trail.set_alpha(70)
        #     surf.blit(r_trail,r_trail.get_rect(bottomleft=(self.right.position.x,self.right.position.y)))
        # pygame.draw.line(surf,Colour.WHITE,(self.left.position.x,self.left.position.y),(self.left.position.x, self.left.position.y - (self.n) * 30))
        # pygame.draw.line(surf,Colour.WHITE,(self.right.position.x+30,self.right.position.y),(self.right.position.x+30, self.right.position.y - (self.n) * 30))