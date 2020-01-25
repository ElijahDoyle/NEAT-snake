import pygame
from snake4NN import Snake
from cube import Cube
from randomSnack import randomSnack
from drawGrid import drawGrid
import os
import neat
from snakeSense import *

def changeSnake(startingCam):
    snakeCam = startingCam
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                snakeCam -= 1
            if event.key == pygame.K_RIGHT:
                snakeCam += 1
    return snakeCam

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
    delayTime = 20
    clock = pygame.time.Clock()



    for i, snake in enumerate(snakeList):
        snack = Cube(randomSnack(rows, snake, width // rows), 0, 0, width // rows - 1, color=(255, 0, 0), layer=i)
        snacks.append(snack)

    screen = pygame.display.set_mode((width, height))

    running = True
    generationBirth = pygame.time.get_ticks()
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                running = False
        timefromBirth = pygame.time.get_ticks() - generationBirth
        screen.fill((0, 0, 0))
        #drawGrid(rows, rows, width, height, width // rows, screen)
        for i, snake in enumerate(snakeList):

            if snake.body[0].pos == snacks[i].pos:
                ge[i].fitness += len(snake.body) * 2.5
                ge[i].fitness -= 1/snake.numberOfTurns
                snake.addCube()
                snake.initialSnackDistance = -1
                newSnack = Cube(randomSnack(rows, snake, width // rows), 0, 0, width // rows - 1, color=(255, 0, 0), layer=i)
                snacks[i] = newSnack
                snake.numberOfTurns += 55
            if snack.layer == 1:
                snack.draw(screen)

            snakeInputs = snakeSenses(snake, snacks[i], width, width // rows, screen, rows)
            inputs = snakeInputs.snakeVision()
            if snakeInputs.snackInSight:
                for dist in (snakeInputs.distancesToSnack):
                    if dist != 0:
                        if snake.initialSnackDistance == -1:
                            snake.initialSnackDistance = dist

                        else:
                            if snake.initialSnackDistance - dist > 0:
                                ge[i].fitness += .2
                                #ge[i].fitness += (snake.initialSnackDistance - dist) * 1.5
                            elif snake.initialSnackDistance - dist < 0:
                                ge[i].fitness -= .2
                            snake.initialSnackDistance = dist
            else:
                pass



            outputs = nets[i].activate(inputs)
            snake.move(outputs)


            dead = False
            for x in range(len(snake.body)):
                if snake.body[x].pos in list(map(lambda z: z.pos, snake.body[x + 1:])) and not dead:
                    dead = True
                    ge[i].fitness -= 1
                    ge.pop(i)
                    nets.pop(i)
                    snakeList.pop(i)
                    snacks.pop(i)
                    #print(str(i) + "has died")
                    break

            if snake.head.pos[0] < 0 or snake.head.pos[0] > width or snake.head.pos[1] < 0 or snake.head.pos[1] > width and not dead:
                ge[i].fitness -= 0
                ge.pop(i)
                nets.pop(i)
                snakeList.pop(i)
                snacks.pop(i)
               # print(str(i) + "has died")

            elif snake.numberOfTurns <= 0:
                ge[i].fitness -= 0
                ge.pop(i)
                nets.pop(i)
                snakeList.pop(i)
                snacks.pop(i)
                dead = True
            else:
                ge[i].fitness += 0.05
        bestSnake = 0
        if len(snakeList) > 0:
            fitnessess = []
            for genome in (ge):
                fitnessess.append(genome.fitness)
            bestSnake = fitnessess.index(max(fitnessess))
            '''bodyLengths = []
            for snake in snakeList:
                bodyLengths.append(len(snake.body))
            bestSnake = bodyLengths.index(max(bodyLengths))'''
            snacks[bestSnake].draw(screen)
            snakeList[bestSnake].draw(screen)
            bestVision = snakeSenses(snakeList[bestSnake], snacks[bestSnake], width, width // rows, screen, rows)
            bestVision.snakeVision()
            bestVision.drawVision()
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
    configu_path = os.path.join(local_dir, 'Config-HW')
    run(configu_path)