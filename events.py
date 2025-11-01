# events.py

import pygame
import random
import pyperclip
import re
# Removed easygui, it's not called from here
from graphical_interface.constants import *
from graphical_interface.spot import Spot
# --- Import all algorithms ---
from algorithms.bfs import bfs
from algorithms.dfs import dfs
from algorithms.best_first_search import greedyBestFirstSearch
# ---
from grid import draw, make_grid, get_clicked_pos

# --- REMOVED: get_matrix_input_popup() ---
# --- REMOVED: parse_and_load_matrix() ---

# --- Helper function to generate matrix string (UNCHANGED) ---
def generate_matrix_string(grid):
    matrix = []
    for row in grid:
        row_str = []
        for spot in row:
            if spot.is_start:
                row_str.append("2")
            elif spot.is_end:
                row_str.append("3")
            elif spot.is_wall:
                row_str.append("1")
            else:
                row_str.append("0")
        matrix.append(" ".join(row_str))
    return "\n".join(matrix)

def add_colors(color1, color2):
    # THIS FUNCTION IS UNCHANGED
    result = []
    for c1, c2 in zip(color1, color2):
        if c1 + c2 > 255:
            new_colour = c1 - c2 + random.randint(-10,10)
            if new_colour < 0: new_colour = 0
            elif new_colour > 255: new_colour = 255 	
        else:
            new_colour = c1 + c2 + random.randint(-10,10)
            if new_colour < 0: new_colour = 0
            elif new_colour > 255: new_colour = 255
        while new_colour in {RED, GREEN, BLUE, YELLOW, WHITE, BLACK, PURPLE, ORANGE, GREY, TURQUOISE, c1 + c2, c1 - c2}:
            new_colour = new_colour + random.randint(-10,10)
            if new_colour < 0: new_colour = 0
            elif new_colour > 255: new_colour = 255 
        result.append(new_colour)
    return tuple(result)

# --- Updated function signature ---
def handle_events(events, grid, ROWS, start_node, end_node, win, width, cur_square_color, buttons, grid_lines_visible, drawing_mode, error_message, current_algorithm):
    
    # --- Unpack all buttons, including new ones ---
    (find_path_button, toggle_grid_button, toggle_mode_button, 
     decrease_button, increase_button, 
     load_matrix_button, save_matrix_button,
     bfs_button, dfs_button, gbfs_button) = buttons
    
    # --- FIX #1: Update algorithm button colors ---
    # We set their base color *before* checking for hovers.
    # Reset all to inactive color
    bfs_button.base_color = ORANGE
    dfs_button.base_color = ORANGE
    gbfs_button.base_color = ORANGE
    
    # Set the active one to a different color (e.g., GREEN)
    if current_algorithm == "bfs":
        bfs_button.base_color = GREEN
    elif current_algorithm == "dfs":
        dfs_button.base_color = GREEN
    elif current_algorithm == "gbfs":
        gbfs_button.base_color = GREEN
    # --- End of Fix #1 ---
    
    mouse_pos = pygame.mouse.get_pos()
    for button in buttons:
        button.check_for_hover(mouse_pos)

    for event in events:
        # --- FIX #2: Clear error message only on a new action ---
        # This stops mouse movement from clearing the error.
        if event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.KEYDOWN:
            error_message = None
        # --- End of Fix #2 ---

        if event.type == pygame.QUIT:
            # --- Add new state to return tuple ---
            return False, start_node, end_node, cur_square_color, grid, grid_lines_visible, drawing_mode, ROWS, error_message, current_algorithm

        # --- Button Click Logic ---
        if find_path_button.is_clicked(event):
            if start_node and end_node:
                for row in grid:
                    for spot in row:
                        spot.clear_visualization()
                
                # --- NEW: Use current_algorithm to decide ---
                draw_lambda = lambda: draw(win, grid, ROWS, width, buttons, grid_lines_visible, error_message)
                
                if current_algorithm == "bfs":
                    algorithm_generator = bfs(draw_lambda, grid, start_node, end_node, cur_square_color)
                elif current_algorithm == "dfs":
                    algorithm_generator = dfs(draw_lambda, grid, start_node, end_node, cur_square_color)
                elif current_algorithm == "gbfs":
                    algorithm_generator = greedyBestFirstSearch(draw_lambda, grid, start_node, end_node, cur_square_color)

                for _ in algorithm_generator: pass
                cur_square_color = add_colors(cur_square_color, (10, 10, 10))
                pygame.event.clear(pygame.KEYDOWN) 

        if toggle_grid_button.is_clicked(event):
            grid_lines_visible = not grid_lines_visible

        if toggle_mode_button.is_clicked(event):
            if drawing_mode == "maker":
                drawing_mode = "eraser"
                toggle_mode_button.update_text("Switch to Maker")
            else:
                drawing_mode = "maker"
                toggle_mode_button.update_text("Switch to Eraser")

        if save_matrix_button.is_clicked(event):
            internal_grid = [row[1:-1] for row in grid[1:-1]]
            matrix_str = generate_matrix_string(internal_grid)
            pyperclip.copy(matrix_str)
            print("Matrix copied to clipboard!") 

        if load_matrix_button.is_clicked(event):
            drawing_mode = "get_matrix"
            break 
        
        # --- NEW: Handle Algorithm Button Clicks ---
        if bfs_button.is_clicked(event):
            current_algorithm = "bfs"
            print("Algorithm set to BFS") # For debugging
        
        if dfs_button.is_clicked(event):
            current_algorithm = "dfs"
            print("Algorithm set to DFS")
            
        if gbfs_button.is_clicked(event):
            current_algorithm = "gbfs"
            print("Algorithm set to Greedy Best-First")
        # ---
        
        # --- Grid Size Buttons (unchanged) ---
        grid_changed = False
        if decrease_button.is_clicked(event):
            if ROWS > 12:
                ROWS -= 1
                grid_changed = True
        
        if increase_button.is_clicked(event):
            if ROWS < 62:
                ROWS += 1
                grid_changed = True
        
        if grid_changed:
            start_node = None
            end_node = None
            grid = make_grid(ROWS, width)
            continue

        # --- MOUSE CLICK LOGIC (unchanged) ---
        if pygame.mouse.get_pressed()[0] or (event.type == pygame.MOUSEBUTTONDOWN and event.button == 1):
            pos = pygame.mouse.get_pos()
            row, col = get_clicked_pos(pos, ROWS, width)
            if row is not None:
                spot = grid[row][col]
                
                if drawing_mode == "maker":
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if not start_node and not spot.is_end:
                            start_node = spot
                            start_node.mark_start()
                        elif not end_node and not spot.is_start:
                            end_node = spot
                            end_node.mark_end()
                        elif not spot.is_start and not spot.is_end:
                            spot.mark_barrier()
                    elif pygame.mouse.get_pressed()[0]: 
                        if not spot.is_start and not spot.is_end:
                            spot.mark_barrier()

                elif drawing_mode == "eraser":
                    is_border_wall = row == 0 or row == ROWS - 1 or col == 0 or col == ROWS - 1
                    if spot.is_wall and not is_border_wall:
                        spot.reset()
                
                elif drawing_mode == "just_loaded":
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        drawing_mode = "maker" 
                        if not start_node and not spot.is_end:
                            start_node = spot
                            start_node.mark_start()
                        elif not end_node and not spot.is_start:
                            end_node = spot
                            end_node.mark_end()
                        elif not spot.is_start and not spot.is_end:
                            spot.mark_barrier()

        # Right-Click Logic (unchanged)
        if pygame.mouse.get_pressed()[2]:
            pos = pygame.mouse.get_pos()
            row, col = get_clicked_pos(pos, ROWS, width)
            if row is not None:
                spot = grid[row][col]
                if spot.is_start:
                    start_node = None
                    spot.reset()
                elif spot.is_end:
                    end_node = None
                    spot.reset()
        
        # --- KEYBOARD LOGIC ---
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and start_node and end_node:
                for row in grid:
                    for spot in row:
                        spot.clear_visualization()
                
                # --- NEW: Use current_algorithm to decide ---
                draw_lambda = lambda: draw(win, grid, ROWS, width, buttons, grid_lines_visible, error_message)

                if current_algorithm == "bfs":
                    algorithm_generator = bfs(draw_lambda, grid, start_node, end_node, cur_square_color)
                elif current_algorithm == "dfs":
                    algorithm_generator = dfs(draw_lambda, grid, start_node, end_node, cur_square_color)
                elif current_algorithm == "gbfs":
                    algorithm_generator = greedyBestFirstSearch(draw_lambda, grid, start_node, end_node, cur_square_color)

                for _ in algorithm_generator: pass
                cur_square_color = add_colors(cur_square_color, (10, 10, 10))
                pygame.event.clear(pygame.KEYDOWN)

            if event.key == pygame.K_c:
                start_node = None
                end_node = None
                grid = make_grid(ROWS, width)

    # --- Add new state to return tuple ---
    return True, start_node, end_node, cur_square_color, grid, grid_lines_visible, drawing_mode, ROWS, error_message, current_algorithm


