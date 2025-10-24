import pygame
import random
from graphical_interface.constants import *
from graphical_interface.spot import Spot
from algorithms.bfs import bfs
from grid import draw, make_grid, get_clicked_pos


def add_colors(color1, color2):
    result = []
    for c1, c2 in zip(color1, color2):
        if c1 + c2 > 255: # first case to avoid going over 255
            new_colour = c1 - c2 + random.randint(-10,10) # randomness
            if new_colour < 0:
                new_colour = 0
            elif new_colour > 255:
                new_colour = 255    
        else:
            new_colour = c1 + c2 + random.randint(-10,10) # randomness
            if new_colour < 0:
                new_colour = 0
            elif new_colour > 255:
                new_colour = 255
        # we do not want new colour same as game colours or old colours
        while new_colour in {RED, GREEN, BLUE, YELLOW, WHITE, BLACK, PURPLE, ORANGE, GREY, TURQUOISE, c1 + c2, c1 - c2}:
            new_colour = new_colour + random.randint(-10,10)
            if new_colour < 0:
                new_colour = 0
            elif new_colour > 255:
                new_colour = 255 
        
        result.append(new_colour)
    return tuple(result)


def handle_events(grid, ROWS, start_node, end_node, win, width, cur_square_color):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return False, start_node, end_node, grid, cur_square_color # user wants to quit, function returns false, program in main's while loop stops

        # handles mouse clicks
        if event.type == pygame.MOUSEBUTTONDOWN or pygame.mouse.get_pressed()[0] or pygame.mouse.get_pressed()[2]:
            pos = pygame.mouse.get_pos()
            row, col = get_clicked_pos(pos, ROWS, width)
            spot = grid[row][col]
        
            if event.type == pygame.MOUSEBUTTONDOWN:
                if not start_node and spot != end_node:
                    start_node = spot
                    start_node.mark_start()
                elif not end_node and spot != start_node:
                    end_node = spot
                    end_node.mark_end()
            elif pygame.mouse.get_pressed()[0]:
                if spot != start_node and spot != end_node:
                    spot.mark_barrier()
            elif pygame.mouse.get_pressed()[2]:
                spot.reset()
                if spot == start_node:
                    start_node = None
                if spot == end_node:
                    end_node = None


        # handles keyboard inputs
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and start_node and end_node:
                algorithm_generator = bfs(
                    lambda: draw(win, grid, ROWS, width),
                    grid, start_node, end_node, cur_square_color
                )
                for _ in algorithm_generator:
                    pass
                cur_square_color = add_colors(cur_square_color, (10, 10, 10))
            
            if event.key == pygame.K_c:
                start_node = None
                end_node = None
                grid = make_grid(ROWS, width)

    return True, start_node, end_node, cur_square_color