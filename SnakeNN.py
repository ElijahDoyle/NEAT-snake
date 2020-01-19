import pygame
from snake4NN import Snake
from cube import Cube
from randomSnack import randomSnack
from drawGrid import drawGrid
import os
import neat


def snakeSense(snake, snack, width, interval)
    # the snake will be able to see in 8 directions, and determine the distance from an apple, its own body and a wall
    #the snake's forwards vision
    distFromWallUP = snake.pos[1]
    distFromWallDown = width//snake.pos[1]
    distFromWallLeft = snake.pos[0]
    distFromWallRight = width//snake.pos[0]
    

def eval_genomes(genomes, config):
    #time for neat stuff
    for genome_id, genome in genomes:
        genome.fitness = 0
        net = neat.nn.FeedForwardNetwork.create(genome, config)


    pygame.init()
    fps = 10
    clock = pygame.time.Clock()
    rows = 15
    width = 510
    height = 510
    player = Snake([1, 1], (255, 255, 255), width // rows)
    snack = Cube(randomSnack(rows, player, width // rows), 0, 0, width // rows - 1, color=(255, 0, 0))
    screen = pygame.display.set_mode((width, height))

    running = True
    while running:

        screen.fill((0, 0, 0))
        drawGrid(rows, rows, width, height, width // rows, screen)
        if player.body[0].pos == snack.pos:
            player.addCube()
            snack = Cube(randomSnack(rows, player, width // rows), 0, 0, width // rows - 1, color=(255, 0, 0))
        snack.draw(screen)

        player.move()
        player.draw(screen)
        pygame.display.update()
        for x in range(len(player.body)):
            if player.body[x].pos in list(map(lambda z: z.pos, player.body[x + 1:])):
                print('Score: ', len(player.body))
                pygame.time.delay(1000)
                player.reset((1, 1))
                break
        if player.head.pos[0] < 0 or player.head.pos[0] > width or player.head.pos[1] < 0 or player.head.pos[1] > width:
            pygame.time.delay(1000)
            player.reset((1, 1))
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
    config_path = os.path.join(local_dir, 'Config-HW')
    run(config_path)