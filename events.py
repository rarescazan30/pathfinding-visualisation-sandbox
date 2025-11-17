import pygame
import random
import pyperclip
import re

from graphical_interface.constants import *
from graphical_interface.spot import Spot

from algorithms.bfs import bfs
from algorithms.dfs import dfs
from algorithms.best_first_search import greedyBestFirstSearch

from grid import draw, make_grid, get_clicked_pos

last_update = 0  # Global variable to track last update time for continuous increase

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


# function to add two colors with randomness and constraints
# we use this to change the color of the path after each run
def add_colors(color1, color2):
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



def handle_events(run, events, grid, ROWS, start_node, end_node, win, width, cur_square_color, buttons, grid_lines_visible, drawing_mode, error_message, current_algorithm, algorithm_generator):
    # unpack buttons for easier access
    (find_path_button, toggle_grid_button, toggle_mode_button, 
     decrease_button, increase_button, 
     load_matrix_button, save_matrix_button,
     bfs_button, dfs_button, gbfs_button) = buttons
    
    # reset all to inactive color
    bfs_button.base_color = PURPLE
    dfs_button.base_color = PURPLE
    gbfs_button.base_color = PURPLE
    
    if current_algorithm == "bfs":
        bfs_button.base_color = GREEN
    elif current_algorithm == "dfs":
        dfs_button.base_color = GREEN
    elif current_algorithm == "gbfs":
        gbfs_button.base_color = GREEN
    
    mouse_pos = pygame.mouse.get_pos()
    
    for button in buttons:
        button.check_for_hover(mouse_pos)

    for event in events:
        # clear error message on any interaction
        if event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.KEYDOWN:
            error_message = None

        if event.type == pygame.QUIT:
            run = False

        
        if toggle_grid_button.is_clicked(event) or (event.type == pygame.KEYDOWN and event.key == pygame.K_g):
                grid_lines_visible = not grid_lines_visible



        # clear former visualization when finding path
        if find_path_button.is_clicked(event) or (event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE):
            if start_node and end_node and algorithm_generator["running"] == False:
                for row in grid:
                    for spot in row:
                        spot.clear_visualization()
                
                
                # instead of calling draw with all those arguments, we create a lambda function that captures the current state
                draw_lambda = lambda: draw(win, grid, ROWS, width, buttons, grid_lines_visible, error_message)
                if current_algorithm == "bfs":
                    algorithm_generator["generator"] = bfs(draw_lambda, grid, start_node, end_node, cur_square_color)
                elif current_algorithm == "dfs":
                    algorithm_generator["generator"] = dfs(draw_lambda, grid, start_node, end_node, cur_square_color)
                elif current_algorithm == "gbfs":
                    algorithm_generator["generator"] = greedyBestFirstSearch(draw_lambda, grid, start_node, end_node, cur_square_color)
                algorithm_generator["running"] = True
                algorithm_generator["last_step_time"] = pygame.time.get_ticks()
                # we get those yields from the each algorithm which we run step by step
                
                cur_square_color = add_colors(cur_square_color, (10, 10, 10))
                pygame.event.clear(pygame.KEYDOWN) 

        
        if toggle_mode_button.is_clicked(event):
            if drawing_mode == "maker":
                drawing_mode = "eraser"
                toggle_mode_button.update_text("Switch to Maker")
                toggle_mode_button.base_color = GREEN
                toggle_mode_button.hovering_color = BLUE
            else:
                drawing_mode = "maker"
                toggle_mode_button.update_text("Switch to Eraser")
                toggle_mode_button.base_color = BUTTON_RED
                toggle_mode_button.hovering_color = HOVER_BUTTON_RED

        if save_matrix_button.is_clicked(event):
            internal_grid = [row[1:-1] for row in grid[1:-1]]
            matrix_str = generate_matrix_string(internal_grid)
            pyperclip.copy(matrix_str)
            print("Matrix copied to clipboard!") 

        if load_matrix_button.is_clicked(event):
            drawing_mode = "get_matrix"
            # we don't want to handle other events while loading a new matrix
            break 
        
        if bfs_button.is_clicked(event):
            current_algorithm = "bfs"
            print("Algorithm set to BFS")
        
        if dfs_button.is_clicked(event):
            current_algorithm = "dfs"
            print("Algorithm set to DFS")
            
        if gbfs_button.is_clicked(event):
            current_algorithm = "gbfs"
            print("Algorithm set to Greedy Best-First")
        
        grid_changed = False
        pygame.init()  # we use this to get the time for our continuous increase/decrease
        global last_update  # use global variable to track last update time
        
        if decrease_button.is_clicked(event) or increase_button.is_clicked(event):
            # we stop the algorithm!
            algorithm_generator["running"] = False
            algorithm_generator["generator"] = None
            algorithm_generator["last_step_time"] = 0
            first_pressed_time = pygame.time.get_ticks()
            # we want to decrease/increase WHILE the button is pressed
            while pygame.mouse.get_pressed()[0]:
                current_time = pygame.time.get_ticks()
                time_held = current_time - first_pressed_time
                # for decreasing faster when held down longer
                update_speed_value = max(70, 250 - (time_held / 10))
                if current_time - last_update > update_speed_value:
                    if decrease_button.is_clicked(event):
                        if ROWS > 12:
                            ROWS -= 1
                            grid_changed = True
                    elif increase_button.is_clicked(event):
                        if ROWS < 62:
                            ROWS += 1
                            grid_changed = True
                    last_update = current_time
                # update visually (grid and number)
                if grid_changed:
                    start_node = None
                    end_node = None
                    grid = make_grid(ROWS, width)  # Update the grid with the new rows value
                    draw(win, grid, ROWS, width, buttons, grid_lines_visible, error_message)  # redraw everything
                
                # allow pygame to process other events, really important to avoid freezing!
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        exit()

        # handle our drawing and erasing on the map
        if pygame.mouse.get_pressed()[0] or (event.type == pygame.MOUSEBUTTONDOWN and event.button == 1):
            pos = pygame.mouse.get_pos()
            row, col = get_clicked_pos(pos, ROWS, width)
            if row is not None:
                spot = grid[row][col]
                
                if drawing_mode == "just_loaded":
                    drawing_mode = "maker"
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
                    elif pygame.mouse.get_pressed()[0]: # for continuous drawing
                        if not spot.is_start and not spot.is_end:
                            spot.mark_barrier()

                elif drawing_mode == "eraser":
                    is_border_wall = row == 0 or row == ROWS - 1 or col == 0 or col == ROWS - 1
                    if spot.is_wall and not is_border_wall:
                        spot.reset()
                
                # !!! CHANGE I MADE: removed just_loaded mode handling from here and added it above, view line 193. PLEASE CHECK FUNCTIONALITY HERE ON LINUX!

                # elif drawing_mode == "just_loaded":
                #     if event.type == pygame.MOUSEBUTTONDOWN:
                #         drawing_mode = "maker" 
                #         if not start_node and not spot.is_end:
                #             start_node = spot
                #             start_node.mark_start()
                #         elif not end_node and not spot.is_start:
                #             end_node = spot
                #             end_node.mark_end()
                #         elif not spot.is_start and not spot.is_end:
                #             spot.mark_barrier()

        # you can delete start and end with right click
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
        
        # with c you reset the map
        if event.type == pygame.KEYDOWN and event.key == pygame.K_c:
            start_node = None
            end_node = None
            grid = make_grid(ROWS, width)
            algorithm_generator["running"] = False
            algorithm_generator["generator"] = None
            algorithm_generator["last_step_time"] = 0

    # if the grid size changed, we need to reset start and end nodes
    # last condition of if is about how fast the steps update, this will be changed depending on difficulty.
    current_ticks = pygame.time.get_ticks()
    if algorithm_generator["running"] and algorithm_generator["generator"] and current_ticks - algorithm_generator["last_step_time"] >= algorithm_generator["step_interval_ms"]:
        print("Algorithm step")
        try:
            next(algorithm_generator["generator"])
        except StopIteration:
            algorithm_generator["running"] = False
            algorithm_generator["generator"] = None
        algorithm_generator["last_step_time"] = current_ticks

    return run, start_node, end_node, cur_square_color, grid, grid_lines_visible, drawing_mode, ROWS, error_message, current_algorithm


