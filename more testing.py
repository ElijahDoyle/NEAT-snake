import pygame
from snake import Snake
from cube import Cube
from randomSnack import randomSnack
from drawGrid import drawGrid
from snakeSense import *

pygame.init()
fps = 10
clock = pygame.time.Clock()
rows = 15
width = 510
height = 510
player = Snake([69, 35], (255, 255, 255), width // rows)
snack = Cube(randomSnack(rows, player, width // rows), 0, 0, width // rows - 1, color=(255, 0, 0))
screen = pygame.display.set_mode((width, height))
#senses = snakeSenses(player, snack, width, width // rows, screen)

running = True
while running:

    screen.fill((0, 0, 0))
    if player.body[0].pos == snack.pos:
         player.addCube()
         snack = Cube(randomSnack(rows, player, width // rows), 0, 0, width // rows - 1, color=(255, 0, 0))
    snack.draw(screen)
    player.move()
    player.draw(screen)
   # senses.snakeVision()
   # senses.drawVision()
    pygame.display.update()
    print(player.body)
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