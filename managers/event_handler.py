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

def check_user_victory(grid, start_node, end_node):
    """
    Performs a quick BFS to see if the User Path connects Start to End.
    Allows DIAGONAL connections.
    """
    if not start_node or not end_node:
        return False

    queue = deque([start_node])
    visited = {start_node}

    while queue:
        current = queue.popleft()
        
        # Check all 8 neighbors (Orthogonal + Diagonal)
        directions = [
            (0, 1), (0, -1), (1, 0), (-1, 0),
            (1, 1), (1, -1), (-1, 1), (-1, -1)
        ]

        for dr, dc in directions:
            r, c = current.row + dr, current.col + dc
            
            if 0 <= r < len(grid) and 0 <= c < len(grid[0]):
                neighbor = grid[r][c]
                
                # Victory Condition
                if neighbor == end_node:
                    return True
                
                # Traverse User Paths
                if neighbor.is_user_path and neighbor not in visited:
                    visited.add(neighbor)
                    queue.append(neighbor)
    
    return False

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



def handle_events(run, events, grid, ROWS, start_node, end_node, win, width, cur_square_color, buttons, grid_lines_visible, drawing_mode, error_message, current_algorithm, algorithm_generator, texture_manager, race_mode, race_timer, race_timer_button, show_secret_message, input_blocked):
    # unpack buttons for easier access
    # Găsim butoanele după text, e mai sigur decât despachetarea fixă
    win_triggered = False
    find_path_button = next(b for b in buttons if b.text == "Find Path")
    toggle_grid_button = next(b for b in buttons if b.text == "Toggle Grid")
    toggle_mode_button = next(b for b in buttons if "Eraser" in b.text or "Maker" in b.text)
    decrease_button = next(b for b in buttons if b.text == "-")
    increase_button = next(b for b in buttons if b.text == "+")
    
    presets_button = next(b for b in buttons if b.text == "Presets")
    
    load_mac_button = next(b for b in buttons if b.text == "Load (Mac)")
    load_win_button = next(b for b in buttons if b.text == "Load (Win)")
    
    save_matrix_button = next(b for b in buttons if b.text == "Save")
    bfs_button = next(b for b in buttons if b.text == "BFS")
    dfs_button = next(b for b in buttons if b.text == "DFS")
    gbfs_button = next(b for b in buttons if b.text == "GBFS")
    astar_button = next(b for b in buttons if b.text == "A*")
    race_mode_button = next(b for b in buttons if "Race Mode" in b.text)
    
    # reset all to inactive color
    bfs_button.base_color = PURPLE
    dfs_button.base_color = PURPLE
    gbfs_button.base_color = PURPLE
    astar_button.base_color = PURPLE
    
    if current_algorithm == "bfs":
        bfs_button.base_color = GREEN
    elif current_algorithm == "dfs":
        dfs_button.base_color = GREEN
    elif current_algorithm == "gbfs":
        gbfs_button.base_color = GREEN
    elif current_algorithm == "astar":
        astar_button.base_color = GREEN

    mouse_pos = pygame.mouse.get_pos()
    
    for button in buttons:
        if isinstance(button, ImageButton):
            active_index = texture_manager.active_texture_index.get(button.category, -1)
            button.check_for_hover(mouse_pos, active_index)
        else:
            button.check_for_hover(mouse_pos)

    for event in events:
        if event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.KEYDOWN:
            error_message = None

        if event.type == pygame.QUIT:
            run = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            for button in buttons:
                if isinstance(button, ImageButton) and button.is_clicked(event):
                    texture_manager.set_active_texture_index(button.category, button.index)
                    break 

        if presets_button.is_clicked(event):
            drawing_mode = "choose_preset"
            break

        if find_path_button.is_clicked(event) or (event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE):
            if start_node and end_node: # and algorithm_generator["running"] == False
                for row in grid:
                    for spot in row:
                        spot.clear_visualization()
                
                # --- Modificare Texturi ---
                # draw_lambda trebuie să captureze și texture_manager
                draw_lambda = lambda: draw(win, grid, ROWS, width, buttons, grid_lines_visible, error_message, texture_manager, race_mode, race_timer, race_timer_button, show_secret_message)
                # --- Sfârșit Modificare ---
                
                if current_algorithm == "bfs":
                    algorithm_generator["generator"] = bfs(draw_lambda, grid, start_node, end_node, cur_square_color)
                elif current_algorithm == "dfs":
                    algorithm_generator["generator"] = dfs(draw_lambda, grid, start_node, end_node, cur_square_color)
                elif current_algorithm == "gbfs":
                    algorithm_generator["generator"] = greedyBestFirstSearch(draw_lambda, grid, start_node, end_node, cur_square_color)
                elif current_algorithm == "astar":
                    algorithm_generator["generator"] = astar(draw_lambda, grid, start_node, end_node, cur_square_color)
                
                algorithm_generator["running"] = True
                algorithm_generator["last_step_time"] = pygame.time.get_ticks()
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
        
        
        if race_mode_button.is_clicked(event):
            if race_mode == False:
                for r in grid:
                    for s in r:
                        s.clear_visualization()
                        algorithm_generator["running"] = False
                race_mode = True
                race_mode_button.update_text("Race Mode: ON")
                race_mode_button.base_color = BUTTON_RED
                race_mode_button.hovering_color = HOVER_BUTTON_RED
                race_timer["start_time"] = pygame.time.get_ticks()
                
            else:
                race_mode = False
                race_mode_button.update_text("Race Mode: OFF")
                race_mode_button.base_color = GREEN
                race_mode_button.hovering_color = BLUE
                race_timer["running"] = False
                race_timer["elapsed_ms"] = 0


        if save_matrix_button.is_clicked(event):
            internal_grid = [row[1:-1] for row in grid[1:-1]]
            matrix_str = generate_matrix_string(internal_grid)
            pyperclip.copy(matrix_str)
            print("Matrix copied to clipboard!") 

        if load_mac_button.is_clicked(event):
            drawing_mode = "get_matrix_mac" 
            break 

        if load_win_button.is_clicked(event):
            drawing_mode = "get_matrix_win" 
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

        if astar_button.is_clicked(event):
            current_algorithm = "astar"
            print("Algorithm set to A*")
        
        grid_changed = False

        if toggle_grid_button.is_clicked(event) or (event.type == pygame.KEYDOWN and event.key == pygame.K_g):
                grid_lines_visible = not grid_lines_visible
                
        global last_update  
        
        if decrease_button.is_clicked(event) or increase_button.is_clicked(event):
            algorithm_generator["running"] = False
            algorithm_generator["generator"] = None
            algorithm_generator["last_step_time"] = 0
            first_pressed_time = pygame.time.get_ticks()
            
            initial_rows = ROWS 

            while pygame.mouse.get_pressed()[0]:
                current_time = pygame.time.get_ticks()
                time_held = current_time - first_pressed_time
                update_speed_value = max(70, 250 - (time_held / 10))
                
                if current_time - last_update > update_speed_value:
                    if decrease_button.is_clicked(event):
                        # --- FIX: Limite corecte pentru 60x60 (ROWS=62) ---
                        if ROWS > 12:
                            if ROWS > 62: # Dacă e The Judge (102), sărim la 62
                                ROWS = 62
                            else:
                                ROWS -= 1
                            grid_changed = True
                        
                    elif increase_button.is_clicked(event):
                        if ROWS < 62: # Limităm manualul la 62 (pentru 60x60 usable)
                            ROWS += 1
                            grid_changed = True
                        # --- SFÂRȘIT FIX ---
                        
                    last_update = current_time
                
                if grid_changed and ROWS != initial_rows:
                    start_node = None
                    end_node = None
                    grid = make_grid(ROWS, width) 
                    
                    gap = GRID_WIDTH // ROWS
                    texture_manager.update_scaled_textures(gap)
                    # Pasăm texture_manager la draw
                    draw(win, grid, ROWS, width, buttons, grid_lines_visible, error_message, texture_manager, race_mode, race_timer_button, show_secret_message)
                    # --- Sfârșit Modificare ---
                    
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


        # handle our drawing and erasing on the map
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
                        # race_timer["elapsed_ms"] = 0
                        
                        # Trigger Algorithm Automatically
                        if start_node and end_node and algorithm_generator["running"] == False:
                            for r in grid:
                                for s in r:
                                    s.clear_visualization()
                            
                            # Define lambda with new 'race_started=True'
                            draw_lambda = lambda: draw(win, grid, ROWS, width, buttons, grid_lines_visible, error_message, texture_manager, race_mode, race_timer_button, show_secret_message, True)
                            
                            if current_algorithm == "bfs":
                                algorithm_generator["generator"] = bfs(draw_lambda, grid, start_node, end_node, cur_square_color)
                            elif current_algorithm == "dfs":
                                algorithm_generator["generator"] = dfs(draw_lambda, grid, start_node, end_node, cur_square_color)
                            elif current_algorithm == "gbfs":
                                algorithm_generator["generator"] = greedyBestFirstSearch(draw_lambda, grid, start_node, end_node, cur_square_color)
                            elif current_algorithm == "astar":
                                algorithm_generator["generator"] = astar(draw_lambda, grid, start_node, end_node, cur_square_color)

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
                                # --- DRAWING LOGIC (Click) ---
                                if race_mode:
                                    if not spot.is_wall:
                                        spot.mark_user_path()
                                        # Victory Check
                                        if check_user_victory(grid, start_node, end_node):
                                            print("USER WINS! (Click)")
                                            race_timer["running"] = False
                                            algorithm_generator["running"] = False
                                            
                                            race_mode = False
                                            win_triggered = True
                                            
                                            race_mode_button.update_text("Race Mode: OFF")
                                            race_mode_button.base_color = GREEN
                                            race_mode_button.hovering_color = BLUE
                                            for row in grid:
                                                for s in row:
                                                    s.clear_visualization()
                                else:
                                    spot.mark_barrier()
                                # -----------------------------

                        elif pygame.mouse.get_pressed()[0]: 
                            if not spot.is_start and not spot.is_end:
                                if race_mode:
                                    if not spot.is_wall:
                                        spot.mark_user_path()

                                        if race_timer["running"] and check_user_victory(grid, start_node, end_node):
                                            print("USER WINS! (Drag)")
                                            race_timer["running"] = False
                                            algorithm_generator["running"] = False
                                            
                                            
                                            race_mode = False
                                            win_triggered = True
                                            
                                            
                                            race_mode_button.update_text("Race Mode: OFF")
                                            race_mode_button.base_color = GREEN
                                            race_mode_button.hovering_color = BLUE
                                            for row in grid:
                                                for s in row:
                                                    s.clear_visualization()
                                else:
                                    spot.mark_barrier()
                    elif drawing_mode == "eraser":
                        is_border_wall = row == 0 or row == ROWS - 1 or col == 0 or col == ROWS - 1
                        if spot.is_wall == True and not is_border_wall:
                            spot.reset()
        
        # Dacă utilizatorul a ridicat click-ul și eram în modul 'just_loaded',
        # acum e sigur să trecem în 'maker'.
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
        
        # with c you reset the map

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

    # Logica de rulare a algoritmului a fost mutată în main.py
    
    return run, start_node, end_node, cur_square_color, grid, grid_lines_visible, drawing_mode, ROWS, error_message, current_algorithm, race_mode, win_triggered