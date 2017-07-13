import pygame

class Flare:

    def __init__(self, pos, radius, velocity, temp):
        self.pos = pos
        self.radius = radius
        self.velocity = velocity
        self.temp = temp
        self.colCore = (255,250,250)
        self.colEdge = (192,192,255)
        self.edge = 2
        self.alive = True
        self.decayRate = -1
        
    def draw(self,surface,origin):
        if self.alive == True:
            (ox,oy) = origin
            (px,py) = self.pos
            r = self.radius-self.edge
            if r > self.edge:
                pygame.draw.circle(surface, self.colCore, (ox+px,oy+py), int(r), 0)
                pygame.draw.circle(surface, self.colEdge, (ox+px,oy+py), int(r)+self.edge, self.edge)
            elif self.radius > 0:
                pygame.draw.circle(surface, self.colCore, (ox+px,oy+py), int(self.radius), 0)
        
    def tick(self):
        if self.alive == True:
            self.radius = self.radius+self.decayRate
            self.decayRate = self.decayRate-0.1
            if self.radius <= 0:
                self.alive = False
