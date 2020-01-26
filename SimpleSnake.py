import pygame
from cube import Cube
import math
from randomSnack import randomSnack
import neat
import os

class Snake(object):

    def __init__(self, pos, color, sidelength):
        self.pos = list(pos)
        self.color = color
        self.interval = sidelength
        self.sidelength = sidelength
        self.dirnx = 1
        self.dirny = 0
        self.head = Cube(self.pos, self.dirnx, self.dirny, self.sidelength, self.color)
        self.body = [self.head]
        self.body.append(Cube((self.pos[0] - self.interval, self.pos[1]), self.dirnx, self.dirny, self.sidelength, self.color))
        self.turns = {}
        self.numberOfTurns = 50
        self.initialSnackDistance = -1
        self.colliding = False
        #self.body.append(
            #Cube((self.pos[0] - self.interval, self.pos[1]), self.dirnx, self.dirny, self.sidelength, self.color))

    def move(self, NNoutputs):
        currentpos = tuple(self.head.pos)
        self.numberOfTurns -= 1
        # left
        if NNoutputs[0] == max(NNoutputs):
            self.dirnx = 1
            self.dirny = 0
            self.turns[currentpos] = [self.dirnx, self.dirny]
        # right
        elif NNoutputs[1] == max(NNoutputs):
            self.dirnx = -1
            self.dirny = 0
            self.turns[currentpos] = [self.dirnx, self.dirny]

        elif NNoutputs[2] == max(NNoutputs):
            self.dirnx = 0
            self.dirny = -1
            self.turns[currentpos] = [self.dirnx, self.dirny]

        elif NNoutputs[3] == max(NNoutputs):
            self.dirnx = 0
            self.dirny = 1
            self.turns[currentpos] = [self.dirnx, self.dirny]

        for i, c in enumerate(self.body):
            p = tuple(c.pos)
            if (self.body[0].pos[0], self.body[0].pos[1]) == p and i != 0:
                self.colliding = True

            if p in self.turns:
                turn = self.turns[p]
                c.move(turn[0],
                       turn[1])  # turn[0] and turn[0] act as dirnx and dirny and the interval is how mch it will move
                if i == len(self.body) - 1:  # if its the last cube, it removes the turn from the dictionary
                    self.turns.pop(p)
            else:
                c.move(c.dirnx, c.dirny)

    def draw(self, surface):
        for cube in self.body:
            cube.draw(surface)

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


    def distanceBetween(self, pos1, pos2):
        dist = math.sqrt((pos1[0] - pos2[0]) ** 2 + (pos1[1] - pos2[1]) ** 2)
        return dist

    def see(self):
        upSafe = 0
        downSafe = 0
        leftSafe = 0
        rightSafe = 0
        currentPos = self.snake.head.pos
        xDiff = currentPos[0] - self.snack.pos[0]
        yDiff = currentPos[1] - self.snack.pos[1]
        snackAngle = math.atan2(yDiff,xDiff)
        normalizedAngle = (snackAngle - 0) * (1 - 0) / (2 * math.pi)

        for i, c in enumerate(self.snake.body):
            p = tuple(c.pos)
            if currentPos[0] + self.interval == p:
                rightSafe = 1
            if currentPos[0] - self.interval == p:
                leftSafe = 1
            if currentPos[1] + self.interval == p:
                downSafe = 1
            if currentPos[1] - self.interval == p:
                upSafe = 1

        if currentPos[0] + self.interval > self.width:
            rightSafe = 1
        if currentPos[0] - self.interval < 0:
            leftSafe = 1
        if currentPos[1] + self.interval > self.width:
            downSafe = 1
        if currentPos[1] - self.interval < 0:
            upSafe = 1
        return (rightSafe, leftSafe, upSafe, downSafe, normalizedAngle)

def eval_genomes(genomes, config):
    rows = 10
    width = 500
    height = 500
    shownSnake = 0
    #time for neat stuff
    nets = []
    ge = []
    snakeList = []
    snacks = []
    for genome_id, genome in genomes:
        genome.fitness = 0
        net = neat.nn.FeedForwardNetwork.create(genome, config)
        nets.append(net)
        ge.append(genome)
        snakeList.append(Snake([201, 201], (255, 255, 255), width // rows))

    pygame.init()
    fps = 15
    delayTime = 100
    clock = pygame.time.Clock()



    for i, snake in enumerate(snakeList):
        snack = Cube(randomSnack(rows, snake, width // rows), 0, 0, width // rows - 1, color=(255, 0, 0), layer=i)
        snacks.append(snack)

    screen = pygame.display.set_mode((width, height))
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                running = False

        screen.fill((0, 0, 0))

        for i, snake in enumerate(snakeList):

            if snake.body[0].pos == snacks[i].pos:
                ge[i].fitness += 7
                #ge[i].fitness -= 1/snake.numberOfTurns
                snake.addCube()
                newSnack = Cube(randomSnack(rows, snake, width // rows), 0, 0, width // rows - 1, color=(255, 0, 0), layer=i)
                snacks[i] = newSnack
                snake.numberOfTurns += 55
            if snack.layer == 1:
                snack.draw(screen)

            snakeInputs = snakeSenses(snake, snacks[i], width, width // rows, screen, rows)
            inputs = snakeInputs.see()
            outputs = nets[i].activate(inputs)
            snake.move(outputs)

            if snake.colliding:
                ge[i].fitness -= 1
                ge.pop(i)
                nets.pop(i)
                snakeList.pop(i)
                snacks.pop(i)

            elif snake.head.pos[0] < 0 or snake.head.pos[0] > width or snake.head.pos[1] < 0 or snake.head.pos[1] > width:
                ge[i].fitness -= 1
                ge.pop(i)
                nets.pop(i)
                snakeList.pop(i)
                snacks.pop(i)

            elif snake.numberOfTurns <= 0:
                ge[i].fitness -= -2
                ge.pop(i)
                nets.pop(i)
                snakeList.pop(i)
                snacks.pop(i)
            else:
                ge[i].fitness += 0.1


        if len(snakeList) > 0:
            fitnessess = []
            for genome in (ge):
                fitnessess.append(genome.fitness)
            bestSnake = fitnessess.index(max(fitnessess))
            snacks[bestSnake].draw(screen)
            snakeList[bestSnake].draw(screen)

        else:
            running = False
        pygame.display.update()
        pygame.time.delay(delayTime)
        clock.tick(fps)

def run(config_path):
    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, neat.DefaultStagnation,
                         config_path)
    popu = neat.Population(config)
    stats = neat.StatisticsReporter()
    popu.add_reporter(stats)
    popu.add_reporter(neat.StdOutReporter(True))
    winner = popu.run(eval_genomes, 100)

if __name__ == '__main__':
    local_dir = os.path.dirname(__file__)
    configu_path = os.path.join(local_dir, 'simpleSnake-Config')
    run(configu_path)