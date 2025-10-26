# events.py

import pygame
import random
from graphical_interface.constants import *
from graphical_interface.spot import Spot
from algorithms.bfs import bfs
from grid import draw, make_grid, get_clicked_pos

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


def handle_events(grid, ROWS, start_node, end_node, win, width, cur_square_color, buttons, grid_lines_visible, drawing_mode):
    find_path_button, toggle_grid_button, toggle_mode_button = buttons
    
    mouse_pos = pygame.mouse.get_pos()
    for button in buttons:
        button.check_for_hover(mouse_pos)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return False, start_node, end_node, cur_square_color, grid, grid_lines_visible, drawing_mode

        # Button click logic is unchanged
        if find_path_button.is_clicked(event):
            if start_node and end_node:
                for row in grid:
                    for spot in row: spot.clear_visualization()
                algorithm_generator = bfs(lambda: draw(win, grid, ROWS, width, buttons, grid_lines_visible), grid, start_node, end_node, cur_square_color)
                for _ in algorithm_generator: pass
                cur_square_color = add_colors(cur_square_color, (10, 10, 10))
        if toggle_grid_button.is_clicked(event):
            grid_lines_visible = not grid_lines_visible
        if toggle_mode_button.is_clicked(event):
            if drawing_mode == "maker":
                drawing_mode = "eraser"
                toggle_mode_button.update_text("Switch to Maker")
            else:
                drawing_mode = "maker"
                toggle_mode_button.update_text("Switch to Eraser")

        # LEFT-CLICK LOGIC
        if pygame.mouse.get_pressed()[0] or (event.type == pygame.MOUSEBUTTONDOWN and event.button == 1):
            pos = pygame.mouse.get_pos()
            row, col = get_clicked_pos(pos, ROWS, width)
            if row is not None:
                spot = grid[row][col]
                if drawing_mode == "maker":
                    # This logic for placing nodes and walls is unchanged
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
                
                # !!! THIS IS THE FIRST PART OF THE FIX !!!
                # The eraser can ONLY delete a spot if it is a barrier AND nothing else.
                # This prevents it from erasing the path, start, or end nodes.
                elif drawing_mode == "eraser":
                    is_border_wall = row == 0 or row == ROWS - 1 or col == 0 or col == ROWS - 1
                    if spot.is_barrier and not spot.is_start and not spot.is_end and not is_border_wall:
                        spot.reset()

        # RIGHT-CLICK LOGIC
        if pygame.mouse.get_pressed()[2]:
            pos = pygame.mouse.get_pos()
            row, col = get_clicked_pos(pos, ROWS, width)
            if row is not None:
                spot = grid[row][col]
                
                # !!! THIS IS THE SECOND PART OF THE FIX !!!
                # Right-click ONLY affects start and end nodes. It can no longer
                # erase walls or path visualizations.
                if spot.is_start:
                    start_node = None
                    spot.reset()
                elif spot.is_end:
                    end_node = None
                    spot.reset()
        
        # Keyboard logic is unchanged
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and start_node and end_node:
                for row in grid:
                    for spot in row: spot.clear_visualization()
                algorithm_generator = bfs(lambda: draw(win, grid, ROWS, width, buttons, grid_lines_visible), grid, start_node, end_node, cur_square_color)
                for _ in algorithm_generator: pass
                cur_square_color = add_colors(cur_square_color, (10, 10, 10))
            if event.key == pygame.K_c:
                start_node = None
                end_node = None
                grid = make_grid(ROWS, width)

    return True, start_node, end_node, cur_square_color, grid, grid_lines_visible, drawing_mode