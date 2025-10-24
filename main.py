import pygame
import random
from graphical_interface.constants import *
from graphical_interface.spot import Spot
from algorithms.bfs import bfs
from events import handle_events
from grid import draw, make_grid, get_clicked_pos

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
        run, start_node, end_node, currrent_square_colour = handle_events(grid, ROWS, start_node, end_node, win, width, currrent_square_colour)
    pygame.quit()

if __name__ == "__main__":
    WIN = pygame.display.set_mode((WIDTH, WIDTH))
    pygame.display.set_caption("Pathfinding Visualisation Sandbox")
    main(WIN, WIDTH)