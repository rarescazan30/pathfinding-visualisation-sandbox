# main.py

import pygame
import random
import re       
import easygui  
from graphical_interface.constants import *
from graphical_interface.spot import Spot
from graphical_interface.button import Button
from algorithms.bfs import bfs
from events import handle_events
from grid import draw, make_grid, get_clicked_pos

# --- Copied functions (all correct) ---
def get_matrix_input_popup():
    msg = "Paste your matrix (0=path, 1=wall, 2=start, 3=end):"
    title = "Load Labyrinth Matrix"
    return easygui.codebox(msg, title, "") 

def parse_and_load_matrix(matrix_text, width):
    if not matrix_text: 
        return None, None, None, None, "Load operation cancelled."
    lines = matrix_text.strip().split('\n')
    rows = len(lines)
    if not (10 <= rows <= 60):
        return None, None, None, None, "Matrix must be between 10x10 and 60x60."
    parsed_matrix = []
    start_count = 0
    end_count = 0
    for r, line in enumerate(lines):
        cleaned_line = line.strip()
        if not re.fullmatch(r"^[0-3](\s[0-3])*$", cleaned_line):
            if cleaned_line == "":
                 return None, None, None, None, f"Empty line found in matrix."
            return None, None, None, None, f"Invalid characters in row {r+1}."
        cols = cleaned_line.split(' ')
        if len(cols) != rows:
            return None, None, None, None, "Matrix is not square."
        start_count += cols.count('2')
        end_count += cols.count('3')
        parsed_matrix.append(cols)
    if start_count != 1:
        return None, None, None, None, "Matrix must have exactly one start (2)."
    if end_count != 1:
        return None, None, None, None, "Matrix must have exactly one end (3)."
    grid_rows_with_border = rows + 2 
    new_grid = make_grid(grid_rows_with_border, width)
    new_start = None
    new_end = None
    for r in range(rows):
        for c in range(rows):
            spot = new_grid[r + 1][c + 1] 
            val = parsed_matrix[r][c]
            if val == '1':
                spot.mark_barrier()
            elif val == '2':
                spot.mark_start()
                new_start = spot
            elif val == '3':
                spot.mark_end()
                new_end = spot
    return new_grid, grid_rows_with_border, new_start, new_end, None
# --- End of copied functions ---


def main(win, width):
    current_rows = 40
    grid = make_grid(current_rows, GRID_WIDTH)
    currrent_square_colour = RED
    start_node = None
    end_node = None
    grid_lines_visible = True
    drawing_mode = "maker"
    error_message = None

    pygame.font.init()
    button_font = pygame.font.SysFont("Arial", 24)
    small_font = pygame.font.SysFont("Arial", 30, bold=True) 

    # --- Button setup (unchanged) ---
    button_x = GRID_X_OFFSET + GRID_WIDTH + 50
    find_path_button = Button(x=button_x, y=100, width=200, height=50, text="Find Path", font=button_font, base_color=GREEN, hovering_color=BLUE)
    toggle_grid_button = Button(x=button_x, y=180, width=200, height=50, text="Toggle Grid", font=button_font, base_color=PURPLE, hovering_color=ORANGE)
    toggle_mode_button = Button(x=button_x, y=260, width=200, height=50, text="Switch to Eraser", font=button_font, base_color=(200, 50, 50), hovering_color=(250, 100, 100))
    decrease_button = Button(x=button_x, y=380, width=50, height=50, text="-", font=small_font, base_color=GREY, hovering_color=(190, 190, 190))
    increase_button = Button(x=button_x + 150, y=380, width=50, height=50, text="+", font=small_font, base_color=GREY, hovering_color=(190, 190, 190))
    left_button_x = 60
    load_matrix_button = Button(x=left_button_x, y=320, width=200, height=50, text="Load Labyrinth", font=button_font, base_color=BLUE, hovering_color=GREEN)
    save_matrix_button = Button(x=left_button_x, y=390, width=200, height=50, text="Save Matrix", font=button_font, base_color=BLUE, hovering_color=GREEN)
    buttons = [find_path_button, toggle_grid_button, toggle_mode_button, decrease_button, increase_button, load_matrix_button, save_matrix_button]
    # --- End of button setup ---

    run = True
    while run:
        draw(
            win, grid, current_rows, GRID_WIDTH, buttons, 
            grid_lines_visible, error_message
        )
        
        events = pygame.event.get()
        
        result = handle_events(
            events, grid, current_rows, start_node, end_node, win, GRID_WIDTH,
            currrent_square_colour, buttons, grid_lines_visible, drawing_mode,
            error_message
        )
        
        (run, start_node, end_node, currrent_square_colour, 
         grid, grid_lines_visible, drawing_mode, current_rows, error_message) = result

        if drawing_mode == "get_matrix":
            pygame.display.iconify()
            pygame.key.set_repeat(0, 0)
            
            matrix_text = get_matrix_input_popup()
            
            # Clear stale mouse events from the queue
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
            
            # --- THIS IS THE FIX ---
            # Set a new mode to indicate we need one click
            # to reset the mouse state.
            drawing_mode = "just_loaded"
            # --- END OF FIX ---

    pygame.quit()

if __name__ == "__main__":
    WIN = pygame.display.set_mode((TOTAL_WIDTH, TOTAL_HEIGHT))
    pygame.display.set_caption("Pathfinding Visualisation Sandbox")
    pygame.key.set_repeat(500, 50) 
    main(WIN, GRID_WIDTH)

