import pygame


def drawGrid(columns, rows, width, height, spaceBetween, surface):

    x = 0
    y = 0
    for c in range(0, columns):
        x += spaceBetween
        pygame.draw.line(surface, (255,255,255), (x,0), (x, height), 1)

    for r in range(0, rows):
        y += spaceBetween
        pygame.draw.line(surface, (255,255,255), (0,y), (width, y), 1)

