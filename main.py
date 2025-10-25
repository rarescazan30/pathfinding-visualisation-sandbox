import pygame
import random
import shared
from graphical_interface.constants import *
from graphical_interface.spot import Spot
from algorithms.bfs import bfs
from events import handle_events
from grid import draw, make_grid, get_clicked_pos

shared.cur_square_color = RED 

def main(win, width):
    ROWS = 40
    grid = make_grid(ROWS, width)
    currrent_square_colour = RED
    start_node = None
    end_node = None

    my_modifier = (0, 0, 0)

    run = True
    while run:
        draw(win, grid, ROWS, width)
        run, start_node, end_node, shared.cur_square_color = handle_events(grid, ROWS, start_node, end_node, win, width, shared.cur_square_color)
    pygame.quit()

if __name__ == "__main__":
    WIN = pygame.display.set_mode((WIDTH, WIDTH))
    pygame.display.set_caption("Pathfinding Visualisation Sandbox")
    main(WIN, WIDTH)