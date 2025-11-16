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
    
    # --- NEW: State for selected algorithm ---
    current_algorithm = "bfs" # Default to BFS

    pygame.font.init()
    button_font = pygame.font.SysFont("Arial", 24)
    small_font = pygame.font.SysFont("Arial", 30, bold=True) 

    # --- Right Menu Buttons (unchanged) ---
    button_x = GRID_X_OFFSET + GRID_WIDTH + 50
    find_path_button = Button(x=button_x, y=100, width=200, height=50, text="Find Path", font=button_font, base_color=GREEN, hovering_color=BLUE)
    toggle_grid_button = Button(x=button_x, y=180, width=200, height=50, text="Toggle Grid", font=button_font, base_color=PURPLE, hovering_color=ORANGE)
    toggle_mode_button = Button(x=button_x, y=260, width=200, height=50, text="Switch to Eraser", font=button_font, base_color=(200, 50, 50), hovering_color=(250, 100, 100))
    decrease_button = Button(x=button_x, y=380, width=50, height=50, text="-", font=small_font, base_color=GREY, hovering_color=(190, 190, 190))
    increase_button = Button(x=button_x + 150, y=380, width=50, height=50, text="+", font=small_font, base_color=GREY, hovering_color=(190, 190, 190))
    
    # --- Left Menu Buttons (Layout Updated) ---
    left_button_x = 60 # Center them in the left menu
    
    # Moved Up
    load_matrix_button = Button(
        x=left_button_x, y=100, width=200, height=50, 
        text="Load Labyrinth", font=button_font, 
        base_color=BLUE, hovering_color=GREEN
    )
    # Moved Up
    save_matrix_button = Button(
        x=left_button_x, y=170, width=200, height=50, 
        text="Save Matrix", font=button_font, 
        base_color=BLUE, hovering_color=GREEN
    )

    # --- NEW: Algorithm Buttons ---
    bfs_button = Button(
        x=left_button_x, y=260, width=200, height=50,
        text="BFS (Default)", font=button_font,
        base_color=ORANGE, hovering_color=YELLOW
    )
    dfs_button = Button(
        x=left_button_x, y=330, width=200, height=50,
        text="DFS", font=button_font,
        base_color=ORANGE, hovering_color=YELLOW
    )
    gbfs_button = Button(
        x=left_button_x, y=400, width=200, height=50,
        text="Greedy Best-First", font=button_font,
        base_color=ORANGE, hovering_color=YELLOW
    )
    # Note: We could add logic to show which button is "active"
    # but for now, this sets up the functionality.

    buttons = [
        find_path_button, toggle_grid_button, toggle_mode_button, 
        decrease_button, increase_button,
        load_matrix_button, save_matrix_button,
        bfs_button, dfs_button, gbfs_button # <-- Add new buttons
    ]

    run = True
    while run:
        draw(
            win, grid, current_rows, GRID_WIDTH, buttons, 
            grid_lines_visible, error_message
        )
        
        events = pygame.event.get()
        
        # --- PASS and RECEIVE the new algorithm state ---
        result = handle_events(
            events, grid, current_rows, start_node, end_node, win, GRID_WIDTH,
            currrent_square_colour, buttons, grid_lines_visible, drawing_mode,
            error_message, current_algorithm # <-- Pass state in
        )
        
        (run, start_node, end_node, currrent_square_colour, 
         grid, grid_lines_visible, drawing_mode, current_rows, 
         error_message, current_algorithm) = result # <-- Unpack state
        # ---

        if drawing_mode == "get_matrix":
            pygame.display.iconify()
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

