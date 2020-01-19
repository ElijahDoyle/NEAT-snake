import pygame
from cube import Cube
from drawGrid import drawGrid
from snake import Snake
from randomSnack import randomSnack



def test():
    pygame.init()
    fps = 10
    clock = pygame.time.Clock()
    rows = 15
    width = 510
    height = 510
    tSnake = Snake([0, 0], (255, 255, 255), width // rows)
    snack = Cube(randomSnack(rows, tSnake, width//rows), 0, 0, width//rows, color=(255,0,0))
    screen = pygame.display.set_mode((width, height))


    running = True
    while running:

        screen.fill((0,0,0))
        drawGrid(rows, rows, width, height, width//rows, screen)
        if tSnake.body[0].pos == snack.pos:
            tSnake.addCube()
            snack = Cube(randomSnack(rows, tSnake, width//rows), 0, 0, width//rows, color=(255, 0, 0))
        snack.draw(screen)
        tSnake.move()
        tSnake.draw(screen)
        pygame.display.update()
        for x in range(len(tSnake.body)):
            if tSnake.body[x].pos in list(map(lambda z: z.pos, tSnake.body[x + 1:])):
                print('Score: ', len(tSnake.body))
                pygame.time.delay(1000)
                tSnake.reset((0, 0))
                break
        if tSnake.head.pos[0] < 0 or tSnake.head.pos[0] > width or tSnake.head.pos[1] < 0 or tSnake.head.pos[1] > width:
            pygame.time.delay(1000)
            tSnake.reset((0,0))
        pygame.time.delay(50)
        clock.tick(fps)

test()