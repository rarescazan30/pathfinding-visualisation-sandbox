import pygame
import random
import pyperclip
import re
import time
from collections import deque

from ui.constants import *
from ui.spot import Spot
from ui.button import ImageButton 

from algorithms.bfs import bfs
from algorithms.dfs import dfs
from algorithms.best_first_search import greedyBestFirstSearch
from algorithms.astar import astar

from core.grid import draw, make_grid, get_clicked_pos

last_update = 0 

# Converts the grid into a string format (0 for empty, 1 for wall, 2 for start, 3 for end)
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

# Checks if user built path connected from start to end
# Takes corners into account
def check_user_victory(grid, start_node, end_node):
    if not start_node or not end_node:
        return False

    queue = deque([start_node])
    visited = {start_node}

    while queue:
        current = queue.popleft()
        
        directions = [
            (0, 1), (0, -1), (1, 0), (-1, 0),
            (1, 1), (1, -1), (-1, 1), (-1, -1)
        ]

        for dr, dc in directions:
            r, c = current.row + dr, current.col + dc
            
            if 0 <= r < len(grid) and 0 <= c < len(grid[0]):
                neighbor = grid[r][c]
                
                if neighbor == end_node:
                    return True
                
                if neighbor.is_user_path and neighbor not in visited:
                    visited.add(neighbor)
                    queue.append(neighbor)
    
    return False

# Changes color slightly for variation when running algorithm multiple times
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


def get_ui_buttons(buttons):
    ui = {}
    ui["find_path"] = next(b for b in buttons if b.text == "Find Path")
    ui["toggle_grid"] = next(b for b in buttons if b.text == "Toggle Grid")
    ui["toggle_mode"] = next(b for b in buttons if "Eraser" in b.text or "Maker" in b.text)
    ui["decrease"] = next(b for b in buttons if b.text == "-")
    ui["increase"] = next(b for b in buttons if b.text == "+")
    ui["presets"] = next(b for b in buttons if b.text == "Presets")
    ui["load_mac"] = next(b for b in buttons if b.text == "Load (Mac)")
    ui["load_win"] = next(b for b in buttons if b.text == "Load (Win)")
    ui["save"] = next(b for b in buttons if b.text == "Save")
    ui["bfs"] = next(b for b in buttons if b.text == "BFS")
    ui["dfs"] = next(b for b in buttons if b.text == "DFS")
    ui["gbfs"] = next(b for b in buttons if b.text == "GBFS")
    ui["astar"] = next(b for b in buttons if b.text == "A*")
    ui["race_mode"] = next(b for b in buttons if "Race Mode" in b.text)
    return ui

# Resets colors of all algorithm buttons and highlights the active one
def update_algorithm_button_visuals(ui_buttons, current_algorithm):
    ui_buttons["bfs"].base_color = PURPLE
    ui_buttons["dfs"].base_color = PURPLE
    ui_buttons["gbfs"].base_color = PURPLE
    ui_buttons["astar"].base_color = PURPLE
    
    if current_algorithm == "bfs":
        ui_buttons["bfs"].base_color = GREEN
    elif current_algorithm == "dfs":
        ui_buttons["dfs"].base_color = GREEN
    elif current_algorithm == "gbfs":
        ui_buttons["gbfs"].base_color = GREEN
    elif current_algorithm == "astar":
        ui_buttons["astar"].base_color = GREEN

def get_algorithm_generator(algo_name, draw_lambda, grid, start_node, end_node, cur_square_color):
    if algo_name == "bfs":
        return bfs(draw_lambda, grid, start_node, end_node, cur_square_color)
    elif algo_name == "dfs":
        return dfs(draw_lambda, grid, start_node, end_node, cur_square_color)
    elif algo_name == "gbfs":
        return greedyBestFirstSearch(draw_lambda, grid, start_node, end_node, cur_square_color)
    elif algo_name == "astar":
        return astar(draw_lambda, grid, start_node, end_node, cur_square_color)
    return None

def handle_events(run, events, grid, ROWS, start_node, end_node, win, width, cur_square_color, buttons, grid_lines_visible, drawing_mode, error_message, current_algorithm, algorithm_generator, texture_manager, race_mode, race_timer, race_timer_button, show_secret_message, input_blocked):
    
    ui = get_ui_buttons(buttons)
    win_triggered = False

    update_algorithm_button_visuals(ui, current_algorithm)

    mouse_pos = pygame.mouse.get_pos()
    for button in buttons:
        if isinstance(button, ImageButton):
            active_index = texture_manager.active_texture_index.get(button.category, -1)
            button.check_for_hover(mouse_pos, active_index)
        else:
            button.check_for_hover(mouse_pos)

    for event in events:
        # Reset error message on interaction (except Save button)
        if event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.KEYDOWN:
            error_message = None

        if event.type == pygame.QUIT:
            run = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            for button in buttons:
                if isinstance(button, ImageButton) and button.is_clicked(event):
                    texture_manager.set_active_texture_index(button.category, button.index)
                    break 


        if ui["presets"].is_clicked(event):
            drawing_mode = "choose_preset"
            break

        if ui["find_path"].is_clicked(event) or (event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE):
            if start_node and end_node:
                # Clear previous visualizers
                for row in grid:
                    for spot in row:
                        spot.clear_visualization()
                
                # Create lambda for drawing during algorithm steps
                draw_lambda = lambda: draw(win, grid, ROWS, width, buttons, grid_lines_visible, error_message, texture_manager, race_mode, race_timer, race_timer_button, show_secret_message)
                
                algorithm_generator["generator"] = get_algorithm_generator(current_algorithm, draw_lambda, grid, start_node, end_node, cur_square_color)
                
                algorithm_generator["running"] = True
                algorithm_generator["last_step_time"] = pygame.time.get_ticks()
                cur_square_color = add_colors(cur_square_color, (10, 10, 10))
                pygame.event.clear(pygame.KEYDOWN) 

        if ui["toggle_mode"].is_clicked(event):
            if drawing_mode == "maker":
                drawing_mode = "eraser"
                ui["toggle_mode"].update_text("Switch to Maker")
                ui["toggle_mode"].base_color = GREEN
                ui["toggle_mode"].hovering_color = BLUE
            else:
                drawing_mode = "maker"
                ui["toggle_mode"].update_text("Switch to Eraser")
                ui["toggle_mode"].base_color = BUTTON_RED
                ui["toggle_mode"].hovering_color = HOVER_BUTTON_RED
        
        if ui["race_mode"].is_clicked(event):
            if race_mode == False:
                for r in grid:
                    for s in r:
                        s.clear_visualization()
                        algorithm_generator["running"] = False
                race_mode = True
                ui["race_mode"].update_text("Race Mode: ON")
                ui["race_mode"].base_color = BUTTON_RED
                ui["race_mode"].hovering_color = HOVER_BUTTON_RED
                race_timer["start_time"] = pygame.time.get_ticks()
            else:
                race_mode = False
                ui["race_mode"].update_text("Race Mode: OFF")
                ui["race_mode"].base_color = GREEN
                ui["race_mode"].hovering_color = BLUE
                race_timer["running"] = False
                race_timer["elapsed_ms"] = 0

        if ui["save"].is_clicked(event):
            internal_grid = [row[1:-1] for row in grid[1:-1]]
            matrix_str = generate_matrix_string(internal_grid)
            pyperclip.copy(matrix_str)
            # We set the message here so it appears on screen
            error_message = "Map copied to clipboard!"

        if ui["load_mac"].is_clicked(event):
            drawing_mode = "get_matrix_mac" 
            break 

        if ui["load_win"].is_clicked(event):
            drawing_mode = "get_matrix_win" 
            break
        
        if ui["bfs"].is_clicked(event):
            current_algorithm = "bfs"
        
        if ui["dfs"].is_clicked(event):
            current_algorithm = "dfs"
            
        if ui["gbfs"].is_clicked(event):
            current_algorithm = "gbfs"

        if ui["astar"].is_clicked(event):
            current_algorithm = "astar"
        
        
        grid_changed = False

        if ui["toggle_grid"].is_clicked(event) or (event.type == pygame.KEYDOWN and event.key == pygame.K_g):
                grid_lines_visible = not grid_lines_visible
                
        global last_update  
        
        # Grid Resizing Logic (+ / -)
        if ui["decrease"].is_clicked(event) or ui["increase"].is_clicked(event):
            algorithm_generator["running"] = False
            algorithm_generator["generator"] = None
            algorithm_generator["last_step_time"] = 0
            first_pressed_time = pygame.time.get_ticks()
            
            initial_rows = ROWS 

            # Loop while mouse is held down to allow rapid resizing
            while pygame.mouse.get_pressed()[0]:
                current_time = pygame.time.get_ticks()
                time_held = current_time - first_pressed_time
                update_speed_value = max(70, 250 - (time_held / 10))
                
                if current_time - last_update > update_speed_value:
                    if ui["decrease"].is_clicked(event):
                        if ROWS > 12:
                            if ROWS > 62:
                                ROWS = 62
                            else:
                                ROWS -= 1
                            grid_changed = True
                        
                    elif ui["increase"].is_clicked(event):
                        if ROWS < 62:
                            ROWS += 1
                            grid_changed = True
                        
                    last_update = current_time
                
                # Re-generate grid if size changed
                if grid_changed and ROWS != initial_rows:
                    start_node = None
                    end_node = None
                    grid = make_grid(ROWS, width) 
                    
                    gap = GRID_WIDTH // ROWS
                    texture_manager.update_scaled_textures(gap)
                    
                    draw(win, grid, ROWS, width, buttons, grid_lines_visible, error_message, texture_manager, race_mode, race_timer_button, show_secret_message)
                    
                    initial_rows = ROWS 

                for e in pygame.event.get():
                    if e.type == pygame.QUIT:
                        pygame.quit()
                        exit()
                    if e.type == pygame.MOUSEBUTTONUP:
                        pygame.mouse.set_pos(pygame.mouse.get_pos()) 
                        break
                else: 
                    continue 
                break 

        
        # Check if user is clicking on the map (not on buttons)
        if not input_blocked and drawing_mode != "just_loaded" and (pygame.mouse.get_pressed()[0] or (event.type == pygame.MOUSEBUTTONDOWN and event.button == 1)):
            pos = pygame.mouse.get_pos()
            row, col = get_clicked_pos(pos, ROWS, width)
            if row is not None:
                clicked_on_button = False
                for button in buttons:
                    if button.rect.collidepoint(pos):
                        clicked_on_button = True
                        break
                
                if not clicked_on_button:
                    if race_mode and not race_timer["running"] and event.type == pygame.MOUSEBUTTONDOWN:
                        race_timer["running"] = True
                        race_timer["start_time"] = pygame.time.get_ticks()
                        
                        # Trigger Algorithm Automatically against user
                        if start_node and end_node and algorithm_generator["running"] == False:
                            for r in grid:
                                for s in r:
                                    s.clear_visualization()
                            
                            draw_lambda = lambda: draw(win, grid, ROWS, width, buttons, grid_lines_visible, error_message, texture_manager, race_mode, race_timer_button, show_secret_message, True)
                            
                            algorithm_generator["generator"] = get_algorithm_generator(current_algorithm, draw_lambda, grid, start_node, end_node, cur_square_color)

                            algorithm_generator["running"] = True
                            algorithm_generator["last_step_time"] = pygame.time.get_ticks()
                            cur_square_color = add_colors(cur_square_color, (10, 10, 10))
                    
                    
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
                                if race_mode:
                                    if not spot.is_wall:
                                        spot.mark_user_path()
                                        if check_user_victory(grid, start_node, end_node):
                                            race_timer["running"] = False
                                            algorithm_generator["running"] = False
                                            race_mode = False
                                            win_triggered = True
                                            
                                            ui["race_mode"].update_text("Race Mode: OFF")
                                            ui["race_mode"].base_color = GREEN
                                            ui["race_mode"].hovering_color = BLUE
                                            for row in grid:
                                                for s in row:
                                                    s.clear_visualization()
                                else:
                                    spot.mark_barrier()

                        elif pygame.mouse.get_pressed()[0]: 
                            if not spot.is_start and not spot.is_end:
                                if race_mode:
                                    if not spot.is_wall:
                                        spot.mark_user_path()
                                        if race_timer["running"] and check_user_victory(grid, start_node, end_node):
                                            race_timer["running"] = False
                                            algorithm_generator["running"] = False
                                            race_mode = False
                                            win_triggered = True
                                            
                                            ui["race_mode"].update_text("Race Mode: OFF")
                                            ui["race_mode"].base_color = GREEN
                                            ui["race_mode"].hovering_color = BLUE
                                            for row in grid:
                                                for s in row:
                                                    s.clear_visualization()
                                else:
                                    spot.mark_barrier()
                    elif drawing_mode == "eraser":
                        # Prevent erasing borders
                        is_border_wall = row == 0 or row == ROWS - 1 or col == 0 or col == ROWS - 1
                        if spot.is_wall == True and not is_border_wall:
                            spot.reset()
        
        if drawing_mode == "just_loaded" and event.type == pygame.MOUSEBUTTONUP:
             drawing_mode = "maker"


        if not input_blocked and pygame.mouse.get_pressed()[2]:
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
        
        # C key = Clear Map
        if event.type == pygame.KEYDOWN and event.key == pygame.K_c:
            start_node = None
            end_node = None
            grid = make_grid(ROWS, width)
            algorithm_generator["running"] = False
            algorithm_generator["generator"] = None
            algorithm_generator["last_step_time"] = 0
            
            if race_mode:
                race_timer["running"] = False
                race_timer["elapsed_ms"] = 0
                race_timer["start_time"] = pygame.time.get_ticks()

    
    return run, start_node, end_node, cur_square_color, grid, grid_lines_visible, drawing_mode, ROWS, error_message, current_algorithm, race_mode, win_triggered