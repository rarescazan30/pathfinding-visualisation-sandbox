import random
import re

import easygui
import pygame

from algorithms.bfs import bfs
from algorithms.dfs import dfs
from algorithms.best_first_search import greedyBestFirstSearch
from events import handle_events
from grid import draw, get_clicked_pos, make_grid
from graphical_interface.button import Button
from graphical_interface.spot import Spot
# since we are using many constants, import all
# this could be bad practice (hard to debug), but:
# they are distinctly named to ease debug (all uppercase)
from graphical_interface.constants import *
from initialize_matrix import get_matrix_input_popup, parse_and_load_matrix


def main(win, width):
    current_rows = 40
    grid = make_grid(current_rows, GRID_WIDTH)
    currrent_square_colour = RED
    start_node = None
    end_node = None
    grid_lines_visible = True
    drawing_mode = "maker"
    error_message = None
    
    current_algorithm = "bfs" # default to BFS

    pygame.font.init()
    button_font = pygame.font.SysFont("Arial", 24)
    small_font = pygame.font.SysFont("Arial", 30, bold=True) 

    buttons = Button.create_buttons(button_font, small_font)

    run = True
    while run:
        draw(
            win, grid, current_rows, GRID_WIDTH, buttons, 
            grid_lines_visible, error_message
        )
        
        events = pygame.event.get()
        

        # handle events is a function that deals with all events
        # and returns the updated values of all relevant variables
        result = handle_events(
            events, grid, current_rows, start_node, end_node, win, GRID_WIDTH,
            currrent_square_colour, buttons, grid_lines_visible, drawing_mode,
            error_message, current_algorithm
        )
        # unpack all returned values
        (run, start_node, end_node, currrent_square_colour, 
         grid, grid_lines_visible, drawing_mode, current_rows, 
         error_message, current_algorithm) = result


        if drawing_mode == "get_matrix":
            # this will minimize the pygame window to avoid overlapping
            pygame.display.iconify()
            # disable key repeat to avoid input issues
            pygame.key.set_repeat(0, 0)
            
            matrix_text = get_matrix_input_popup()
            
            pygame.event.clear(pygame.MOUSEBUTTONDOWN)
            pygame.event.clear(pygame.MOUSEBUTTONUP)
            
            pygame.key.set_repeat(500, 50) 
            pygame.display.set_mode((TOTAL_WIDTH, TOTAL_HEIGHT))
            
            if matrix_text:
                (new_grid, new_rows, new_start, new_end, err_msg) = \
                    parse_and_load_matrix(matrix_text, GRID_WIDTH)
                
                if err_msg:
                    error_message = err_msg
                else:
                    grid = new_grid
                    current_rows = new_rows
                    start_node = new_start
                    end_node = new_end
                    error_message = None
            else:
                error_message = "Load operation cancelled."
            
            drawing_mode = "just_loaded"

    pygame.quit()

if __name__ == "__main__":
    WIN = pygame.display.set_mode((TOTAL_WIDTH, TOTAL_HEIGHT))
    pygame.display.set_caption("Pathfinding Visualisation Sandbox")
    pygame.key.set_repeat(500, 50) 
    main(WIN, GRID_WIDTH)

