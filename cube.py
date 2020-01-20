import pygame

class Cube(object):
    def __init__(self, pos, dirnx, dirny, sideLength, color, layer=1):
        self.pos = pos
        self.dirnx = dirnx
        self.dirny = dirny
        self.sideLength = sideLength
        self.color = color
        self.layer = layer

    def move(self, dirnx, dirny):
        self.dirnx = dirnx
        self.dirny = dirny
        xMagnitude = int((self.dirnx * self.sideLength))
        yMagnitude = int((self.dirny * self.sideLength))
        self.pos = [self.pos[0] + xMagnitude, self.pos[1] + yMagnitude]



    def draw(self, window):
        self.pos = tuple(self.pos)
        pygame.draw.rect(window, self.color, [self.pos[0], self.pos[1], self.sideLength, self.sideLength], 0)





