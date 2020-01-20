import pygame
from snake4NN import Snake
from cube import Cube
from randomSnack import randomSnack
from drawGrid import drawGrid
import os
import neat
from snakeSense import *


def eval_genomes(genomes, config):
    rows = 15
    width = 510
    height = 510

    #time for neat stuff
    nets = []
    ge = []
    snakes = []
    snacks = []
    for genome_id, genome in genomes:
        genome.fitness = 0
        net = neat.nn.FeedForwardNetwork.create(genome, config)
        nets.append(net)
        ge.append(genome)
        snake = Snake([35, 35], (255, 255, 255), width // rows)
        snakes.append(snake)





    pygame.init()
    fps = 10
    clock = pygame.time.Clock()

    for i, snake in enumerate(snakes):
        snack = Cube(randomSnack(rows, snake, width // rows), 0, 0, width // rows - 1, color=(255, 0, 0), layer=i)
        snacks.append(snack)

    screen = pygame.display.set_mode((width, height))

    running = True
    while running:

        screen.fill((0, 0, 0))
        drawGrid(rows, rows, width, height, width // rows, screen)
        for i, snake in enumerate(snakes):

            if snake.body[0].pos == snacks[i].pos:
                ge[i].fitness += 5
                snake.addCube()
                newSnack = Cube(randomSnack(rows, snake, width // rows), 0, 0, width // rows - 1, color=(255, 0, 0), layer=i)
                snacks[i] = newSnack
            if snack.layer == 1:
                snack.draw(screen)
            snakeInputs = snakeSenses(snake, snacks[i], width, width // rows, screen)
            inputs = snakeInputs.snakeVision()
            outputs = nets[i].activate(inputs)

            snake.move(outputs)


            for x in range(len(snake.body)):
                if snake.body[x].pos in list(map(lambda z: z.pos, snake.body[x + 1:])):
                    ge[i].fitness -= 5
                    ge.pop(i)
                    nets.pop(i)
                    snakes.pop(i)
                    snacks.pop(i)
                    break
            if snake.head.pos[0] < 0 or snake.head.pos[0] > width or snake.head.pos[1] < 0 or snake.head.pos[1] > width:
                ge[i].fitness -= 5
                ge.pop(i)
                nets.pop(i)
                snakes.pop(i)
                snacks.pop(i)

        snakes[1].draw(screen)
        ge[i].fitness += .1
        pygame.display.update()
        pygame.time.delay(50)
        clock.tick(fps)

def run(config_path):
    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, neat.DefaultStagnation,
                         config_path)
    popu = neat.Population(config)
    stats = neat.StatisticsReporter()
    popu.add_reporter(stats)
    popu.add_reporter(neat.StdOutReporter(True))
    winner = popu.run(eval_genomes, 50)

if __name__ == '__main__':
    local_dir = os.path.dirname(__file__)
    configu_path = os.path.join(local_dir, 'Config-HW')
    run(configu_path)