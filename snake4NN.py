import pygame
from cube import Cube

class Snake(object):
    body = []
    turns = {}

    def __init__(self, pos, color, sidelength):
        self.pos = list(pos)
        self.color = color
        self.interval = sidelength
        self.sidelength = sidelength
        self.dirnx = 1
        self.dirny = 0
        self.head = Cube(self.pos, self.dirnx, self.dirny, self.sidelength, self.color)
        self.body.append(self.head)

    def move(self, NNoutputs):
        bestValue = NNoutputs.index(max(NNoutputs))
        currentpos = tuple(self.head.pos)

        if NNoutputs[0]:
            self.dirnx = -1
            self.dirny = 0
            self.turns[currentpos] = [self.dirnx, self.dirny]

        elif NNoutputs[1]:
            self.dirnx = 1
            self.dirny = 0
            self.turns[currentpos] = [self.dirnx, self.dirny]

        elif NNoutputs[2]:
            self.dirnx = 0
            self.dirny = -1
            self.turns[currentpos] = [self.dirnx, self.dirny]

        elif NNoutputs[3]:
            self.dirnx = 0
            self.dirny = 1
            self.turns[currentpos] = [self.dirnx, self.dirny]

        for i, c in enumerate(self.body):
            p = tuple(c.pos)
            if p in self.turns:
                turn = self.turns[p]
                c.move(turn[0], turn[1]) # turn[0] and turn[0] act as dirnx and dirny and the interval is how mch it will move
                if i == len(self.body) - 1:  # if its the last cube, it removes the turn from the dictionary
                    self.turns.pop(p)
            else:
                c.move(c.dirnx, c.dirny)

    def draw(self, surface):
        for cube in self.body:
            cube.draw(surface)

    def reset(self, pos):
        self.turns = {}
        self.color = (255,255,255)
        self.dirnx = 1
        self.dirny = 0
        self.head = Cube(pos, self.dirnx, self.dirny, self.sidelength, self.color)
        self.body = []
        self.body.append(self.head)

    def addCube(self):
        tail = self.body[-1]
        dx, dy = tail.dirnx, tail.dirny

        if dx == 1 and dy == 0:
            self.body.append(Cube((tail.pos[0] - self.interval, tail.pos[1]), dx, dy, self.sidelength, self.color))
        elif dx == -1 and dy == 0:
            self.body.append(Cube((tail.pos[0] + self.interval, tail.pos[1]), dx, dy, self.sidelength, self.color))
        elif dx == 0 and dy == 1:
            self.body.append(Cube((tail.pos[0], tail.pos[1] - self.interval), dx, dy, self.sidelength, self.color))
        elif dx == 0 and dy == -1:
            self.body.append(Cube((tail.pos[0], tail.pos[1] + self.interval), dx, dy, self.sidelength, self.color))

