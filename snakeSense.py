import math
import pygame

class Slope(object):
    __slots__ = ('run', 'rise')
    def __init__(self, run: int, rise: int):
        self.rise = rise
        self.run = run

class snakeSenses():
    def __init__(self, snake, snack, width, interval, surface, rows):
        self.snake = snake
        self.snack = snack
        self.width = width
        self.interval = interval
        self.surface = surface
        self.color = (0, 0, 255)
        self.snackColor = (0,255,100)
        self.snackInSight = False
        self.rows = rows
        self.VISION_8 = (
            #   0 up             1 diagRightUp
            Slope(0, -1), Slope(1, -1),
            #   2 Right          3 diagRightDown
            Slope(1, 0), Slope(1, 1),
            #  4 Down           5 diagLeftDown
            Slope(0, 1), Slope(-1, 1),
            #  6 Left           7 diagLeftUP
            Slope(-1, 0), Slope(-1, -1),
        )
        # creates empty lists   Each will have 8 values (1 for each direction)
        self.distancesToWall = []
        self.distancesToSnack = []  # if the value is 0, then it has not been detected
        self.distancesToSelf = []  # if the value is 0 then it has not been detected
        self.wallPositions = []

    def distanceBetween(self, pos1, pos2):
        dist = math.sqrt((pos1[0] - pos2[0]) ** 2 + (pos1[1] - pos2[1]) ** 2)
        return dist

    def snakeVision(self):
        # the snake will be able to see in 8 directions, and determine the distance from an apple, its own body and a wall
        # creates empty lists   Each will have 8 values (1 for each direction)
        self.distancesToWall = []
        self.distancesToSnack = []  # if the value is 0, then it has not been detected
        self.distancesToSelf = []  # if the value is 0 then it has not been detected
        self.wallPositions = []
        self.snackDirection = 9

        for i, slope in enumerate(self.VISION_8):
            currentPos = list(self.snake.head.pos)
            snackDetected = False
            bodyDetected = False
            outsideOfWall = False
            intervalxDist = self.interval * slope.run
            intervalyDist = self.interval * slope.rise

            while not outsideOfWall:

                currentPos[0] += intervalxDist
                currentPos[1] += intervalyDist

                if currentPos == list(self.snack.pos):
                    snackDetected = True
                    self.snackInSight = True
                    sdist = self.distanceBetween(self.snake.head.pos, self.snack.pos)
                    sdist = sdist / self.interval
                    sdist = sdist/(self.rows - 2)
                    self.distancesToSnack.append(sdist)


                for bodyPiece in self.snake.body:
                    if not bodyDetected:
                        if currentPos == list(bodyPiece.pos):
                            bodyDetected = True
                            dist = self.distanceBetween(self.snake.head.pos, bodyPiece.pos)
                            dist = dist / self.interval
                            # puts the value between 0 & 1
                            dist = dist/(self.rows - 1)
                            self.distancesToSelf.append(dist)
                            bodyDetected = True

                if currentPos[0] < 0 or currentPos[0] > self.width or currentPos[1] < 0 or currentPos[1] > self.width:
                    wallDist = self.distanceBetween(currentPos, self.snake.head.pos) / self.interval
                    wallDist = wallDist/ (self.rows - 1)
                    self.distancesToWall.append(wallDist)
                    posOfWall = currentPos
                    self.wallPositions.append(posOfWall)
                    outsideOfWall = True

            if not snackDetected:
                sndist = 0
                self.distancesToSnack.append(sndist)
            if not bodyDetected:
                bdDist = 0
                self.distancesToSelf.append(bdDist)
        if self.snake.dirnx == 1:
            right = 1
        else:
            right = 0
        if self.snake.dirnx == -1:
            left = 1
        else:
            left = 0
        if self.snake.dirny == -1:
            up = 1
        else:
            up = 0
        if self.snake.dirny == 1:
            down = 1
        else:
            down = 0
        inputs = self.distancesToWall + self.distancesToSelf + self.distancesToSnack + [left, right, up, down]
        inputs = tuple(inputs)
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

        headPosition = [self.snake.head.pos[0] + self.interval // 2, self.snake.head.pos[1] + self.interval // 2]

        allZero = True
        for i, dist in enumerate(self.distancesToSnack):
            if dist != 0:
                self.snackDirection = i
                allZero = False

        if allZero:
            self.snackInSight = False

        for i, slope in enumerate(VISION_8):
            wallPos = self.wallPositions[i]
            wallPos = [wallPos[0] + self.interval // 2, wallPos[1] + self.interval // 2]
            if i == self.snackDirection and self.snackInSight:

                pygame.draw.line(self.surface, self.snackColor, headPosition, wallPos, 2)
            else:
                pygame.draw.line(self.surface, self.color, headPosition, wallPos, 2)