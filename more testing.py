import pygame
from cube import Cube

class Snake(object):

    def __init__(self, pos, color):
        self.pos = pos
        self.body = []
        self.turns = {}
        self.color = color
        self.head = Cube(self.pos, 0, 0, 10, self.color)
        self.body.append(self.head)
        self.dirnx = 50
        self.dirny = 100


    def test(self):
        currentpos = tuple(self.head.pos)
        self.head.pos = [1,1]
        self.turns[currentpos] = [self.dirnx, self.dirny]
        print(self.head.pos)
        print(self.turns[currentpos])

testyBoi = Snake([1,1],(0,0,0))

testyBoi.test()
