
import pygame
from graphical_interface.spot import Spot
from graphical_interface.constants import *
from algorithms.bfs import bfs

def draw(win, grid, rows, width):
    win.fill(WHITE) # Fill the whole screen with a white background
    
    # draw each spot on grid
    for row in grid:
        for spot in row:
            spot.draw(win) # Call the draw method for each spot

    #Draw grid lines
    # gap = width // rows
    # for i in range(rows):
    #     pygame.draw.line(win, GREY, (0, i * gap), (width, i * gap))
    #     for j in range(rows):
    #         pygame.draw.line(win, GREY, (j * gap, 0), (j * gap, width))

    pygame.display.flip()


def make_grid(rows, width):
    grid = []
    gap = width // rows
    for i in range(rows):
        grid.append([])
        for j in range(rows):
            spot = Spot(i, j, gap, rows)
            if i == 0 or i == rows - 1 or j == 0 or j == rows - 1:
                spot.mark_outer_barrier()
            grid[i].append(spot)
    return grid

def get_clicked_pos(pos, rows, width):
    gap = width // rows
    y, x = pos
    row = y // gap
    col = x // gap
    if row >= rows:
        row = rows - 1
    if col >= rows:
        col = rows - 1
    return row, col
