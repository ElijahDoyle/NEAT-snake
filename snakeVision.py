import pygame
from snake4NN import Snake
from cube import Cube
from randomSnack import randomSnack
from drawGrid import drawGrid
import os
import neat
import math

class Slope(object):
    __slots__ = ('rise', 'run')
    def __init__(self, rise: int, run: int):
        self.rise = rise
        self.run = run
def distanceBetween(pos1,pos2):
     dist = math.sqrt((pos1[0] - pos2[0])**2 + (pos1[1] - pos2[1])**2)
     return dist


def snakeVision(snake, snack, width, interval):
    # the snake will be able to see in 8 directions, and determine the distance from an apple, its own body and a wall
    currentPos = list(snake.head.pos)

    #creats empty lists   Each will have 8 values (1 for each direction)
    distancesToWall=[]
    distancesToSnack=[] # if the value is 0, then it has not been detected
    distancesToSelf=[] # if the value is 0 then it has not been detected

    VISION_8 = (
        #   up              diagRightUp
        Slope(0, -1), Slope(1, -1),
        #   Right           diagRightDown
        Slope(1, 0), Slope(1, -1),
        #   Down            diagLeftDown
        Slope(0, 1), Slope(-1, 1),
        #   Left            diagLeftUP
        Slope(-1, 0), Slope(-1, -1),
    )

    for i, slope in enumerate(VISION_8):
        snackDetected = False
        bodyDetected = False
        outsideOfWall = False
        intervalxDist = interval * slope.x
        intervalyDIst = interval * slope.y
        wallPositions

        while not outsideOfWall:
            currentPos[0] += intervalxDist
            currentPos[1] += intervalyDIst
            if currentPos == snack.pos:
                snackDetected = True
                sdist = distanceBetween(currentPos, snack.pos)
                sdist = sdist//interval
                distancesToSnack.append(sdist)
            for bodyPiece in snake.body and not bodyDetected:
                if currentPos == snake.body.pos:
                    bodyDetected = True
                    dist = distanceBetween(currentPos,snake.body.pos)
                    dist = dist // interval
                    # puts the value between 0 & 1
                    distancesToSelf.append(dist)
                    break
            if currentPos[0] < 0 or currentPos[0] > width or currentPos[1] < 0 or currentPos[1] > width:
                wallDist = distanceBetween(currentPos, snake.body.pos)

                distancesToWall.append(wallDist // interval)
                outsideOfWall = True
        if not snackDetected:
            sndist = 0
            distancesToSnack.append(sndist)
        if not bodyDetected:
            bdDist = 0
            distancesToSnack.append(bdDist)
    inputs = [distancesToWall, distancesToSelf, distancesToSnack]
    return inputs



def drawVision(snake, snack, width, interval, surface):
    VISION_8 = (
        #   up              diagRightUp
        Slope(0, -1), Slope(1, -1),
        #   Right           diagRightDown
        Slope(1, 0), Slope(1, -1),
        #   Down            diagLeftDown
        Slope(0, 1), Slope(-1, 1),
        #   Left            diagLeftUP
        Slope(-1, 0), Slope(-1, -1),
    )

    currentPos = [snake.head.pos[0] + interval//2, snake.head.pos[1] + interval//2]
    vision = snakeVision(snake, snack, width, interval)
    distToWall = vision[2]

    for i, slope in enumerate(VISION_8):
        xDist = slope.run * distToWall[i] * interval
        yDist = slope.rise * distToWall[i] * interval
        wallPos = (currentPos[0] + (distToWall[distance] * interval), currentPos[1] + (distToWall[distance] * interval))
        pygame.draw.line(surface,(0,255,155), currentPos, wallPos)

