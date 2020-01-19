import math
import pygame

class Slope(object):
    __slots__ = ('rise', 'run')
    def __init__(self, rise: int, run: int):
        self.rise = rise
        self.run = run

class snakeSense():
    def __init__(self, snake, snack, width, interval, surface):
        self.snake = snake
        self.snack = snack
        self.width = width
        self.interval = interval
        self.surface = surface
        self.VISION_8 = (
            #   up              diagRightUp
            Slope(0, -1), Slope(1, -1),
            #   Right           diagRightDown
            Slope(1, 0), Slope(1, -1),
            #   Down            diagLeftDown
            Slope(0, 1), Slope(-1, 1),
            #   Left            diagLeftUP
            Slope(-1, 0), Slope(-1, -1),
        )
        # creats empty lists   Each will have 8 values (1 for each direction)
        self.distancesToWall = []
        self.distancesToSnack = []  # if the value is 0, then it has not been detected
        self.distancesToSelf = []  # if the value is 0 then it has not been detected
        self.wallPositions = []

    def distanceBetween(self, pos1, pos2):
        dist = math.sqrt((pos1[0] - pos2[0]) ** 2 + (pos1[1] - pos2[1]) ** 2)
        return dist

    def snakeVision(self):
        # the snake will be able to see in 8 directions, and determine the distance from an apple, its own body and a wall
        currentPos = list(self.snake.head.pos)

        for i, slope in enumerate(self.VISION_8):
            snackDetected = False
            bodyDetected = False
            outsideOfWall = False
            intervalxDist = self.interval * slope.x
            intervalyDIst = self.interval * slope.y

            while not outsideOfWall:
                currentPos[0] += intervalxDist
                currentPos[1] += intervalyDIst
                if currentPos == self.snack.pos:
                    snackDetected = True
                    sdist = self.distanceBetween(currentPos, self.snack.pos)
                    sdist = sdist // self.interval
                    self.distancesToSnack.append(sdist)
                for bodyPiece in self.snake.body:
                    if currentPos == self.snake.body.pos:
                        bodyDetected = True
                        dist = self.distanceBetween(currentPos, self.snake.body.pos)
                        dist = dist // self.interval
                        # puts the value between 0 & 1
                        self.distancesToSelf.append(dist)
                        break
                if currentPos[0] < 0 or currentPos[0] > self.width or currentPos[1] < 0 or currentPos[1] > self.width:
                    wallDist = self.distanceBetween(currentPos, self.snake.body.pos)
                    self.distancesToWall.append(wallDist // self.interval)
                    self.wallPositions.append(currentPos)
                    outsideOfWall = True
            if not snackDetected:
                sndist = 0
                self.distancesToSnack.append(sndist)
            if not bodyDetected:
                bdDist = 0
                self.distancesToSnack.append(bdDist)
        inputs = [self.distancesToWall, self.distancesToSelf, self.distancesToSnack]
        return inputs

    def drawVision(self):
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

        currentPos = [self.snake.head.pos[0] + self.interval // 2, self.snake.head.pos[1] + self.interval // 2]

        for i in VISION_8:
            wallPos = self.wallPositions
            pygame.draw.line(self.surface, (0, 255, 155), currentPos, wallPos)