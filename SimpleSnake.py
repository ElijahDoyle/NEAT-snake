import pygame
from cube import Cube
import math
from randomSnack import randomSnack
import neat
import os


def distanceBetween( pos1, pos2):
    dist = math.sqrt((pos1[0] - pos2[0]) ** 2 + (pos1[1] - pos2[1]) ** 2)
    return dist


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
        self.movesLeft = 60
        self.colliding = False
        #self.body.append(
            #Cube((self.pos[0] - self.interval, self.pos[1]), self.dirnx, self.dirny, self.sidelength, self.color))

    def move(self, NNoutputs):
        currentpos = tuple(self.head.pos)
        self.movesLeft -= 1
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
        upSafe = 1
        downSafe = 1
        leftSafe = 1
        rightSafe = 1
        snackUp = 0
        snackDown = 0
        snackLeft = 0
        snackRight = 0
        currentPos = self.snake.head.pos
        #print("front: " + str(self.snake.body[0].pos), ",  head: " + str(self.snake.head.pos))
        '''xDiff = currentPos[0] - self.snack.pos[0]
        yDiff = currentPos[1] - self.snack.pos[1]
        snackAngle = math.atan2(yDiff,xDiff)
        normalizedAngle = (snackAngle - 0) * (1 - 0) / (2 * math.pi)'''

        if self.snack.pos[0] > currentPos[0]:
            snackRight = 1
        elif self.snack.pos[0] < currentPos[0]:
            snackLeft = 1
        if self.snack.pos[1] > currentPos[1]:
            snackDown = 1
        elif self.snack.pos[1] < currentPos[1]:
            snackUp = 1

        for i, c in enumerate(self.snake.body):
            p = tuple(c.pos)
            if currentPos[0] + self.interval == p[0]:
                rightSafe = 0
            if currentPos[0] - self.interval == p[0]:
                leftSafe = 0
            if currentPos[1] + self.interval == p[1]:
                downSafe = 0
            if currentPos[1] - self.interval == p[1]:
                upSafe = 0

        if currentPos[0] + self.interval > self.width:
            rightSafe = 0
        if currentPos[0] - self.interval < 0:
            leftSafe = 0
        if currentPos[1] + self.interval > self.width:
            downSafe = 0
        if currentPos[1] - self.interval < 0:
            upSafe = 0
        return (rightSafe, leftSafe, upSafe, downSafe, snackRight, snackLeft, snackUp, snackDown)

def eval_genomes(genomes, config):
    rows = 15
    width = 510
    height = 510
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
        snakeList.append(Snake([35, 35], (255, 255, 255), width // rows))

    pygame.init()
    fps = 20
    delayTime = 20
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
                ge[i].fitness += 15
                snake.movesLeft += 60
                #ge[i].fitness -= 1/snake.numberOfTurns
                snake.addCube()
                newSnack = Cube(randomSnack(rows, snake, width // rows), 0, 0, width // rows - 1, color=(255, 0, 0), layer=i)
                snacks[i] = newSnack
            if snack.layer == 1:
                snack.draw(screen)

            snakeInputs = snakeSenses(snake, snacks[i], width, width // rows, screen, rows)
            inputs = snakeInputs.see()
            outputs = nets[i].activate(inputs)
            distFromSnack = distanceBetween(snacks[i].pos, snake.body[0].pos)
            snake.move(outputs)
            newDistFromSnack = distanceBetween(snacks[i].pos, snake.body[0].pos)

            if distFromSnack - newDistFromSnack > 0:
                ge[i].fitness += .5

            else:
                ge[i].fitness -= .6


            if snake.colliding:
                ge[i].fitness -= 0
                ge.pop(i)
                nets.pop(i)
                snakeList.pop(i)
                snacks.pop(i)

            elif snake.head.pos[0] < 0 or snake.head.pos[0] > width or snake.head.pos[1] < 0 or snake.head.pos[1] > width:
                ge[i].fitness -= 0
                ge.pop(i)
                nets.pop(i)
                snakeList.pop(i)
                snacks.pop(i)

            elif ge[i].fitness < 0:
                ge.pop(i)
                nets.pop(i)
                snakeList.pop(i)
                snacks.pop(i)
            elif snake.movesLeft <= 0:
                ge.pop(i)
                nets.pop(i)
                snakeList.pop(i)
                snacks.pop(i)
            else:
                pass
                #ge[i].fitness += 0.01



        if len(snakeList) > 0:
            '''bodyLengths = []
            for snake in snakeList:
                bodyLengths.append(len(snake.body))
            bestSnake = bodyLengths.index(max(bodyLengths))'''
            fitnessess = []
            for genome in (ge):
                fitnessess.append(genome.fitness)
            bestSnake = fitnessess.index(max(fitnessess))
            snacks[bestSnake].draw(screen)
            snakeList[bestSnake].draw(screen)
            sight = snakeSenses(snakeList[bestSnake], snacks[bestSnake], width, width // rows, screen, rows)


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
    winner = popu.run(eval_genomes, 200)

if __name__ == '__main__':
    local_dir = os.path.dirname(__file__)
    configu_path = os.path.join(local_dir, 'simpleSnake-Config')
    run(configu_path)