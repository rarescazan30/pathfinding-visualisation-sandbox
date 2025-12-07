import random
import re
import os 
import easygui
import pygame

from algorithms.bfs import bfs
from algorithms.dfs import dfs
from algorithms.best_first_search import greedyBestFirstSearch
from events import handle_events
from grid import draw, get_clicked_pos, make_grid
from graphical_interface.button import Button, ImageButton, create_buttons
from graphical_interface.spot import Spot
from graphical_interface.constants import *
# --- MODIFICARE: Am adus înapoi get_matrix_input_popup ---
from initialize_matrix import parse_and_load_matrix, start_load_window, get_matrix_input_popup
# --- SFÂRȘIT MODIFICARE ---
from texture_manager import TextureManager 

def main(win, width):
    
    if not os.path.isdir('assets/textures'):
        print("EROARE: Folderul 'assets/textures' nu a fost găsit.")
        print("Te rog asigură-te că ai 21 de imagini în 'assets/textures'")
        pygame.quit()
        return

    current_rows = 40
    
    currrent_square_colour = RED
    start_node = None
    end_node = None
    grid_lines_visible = True
    drawing_mode = "maker"
    error_message = None
    
    current_algorithm = "bfs" 

    pygame.font.init()
    button_font = pygame.font.SysFont("Arial", 24)
    small_font = pygame.font.SysFont("Arial", 30, bold=True) 
    
    texture_manager = TextureManager()
    
    grid = make_grid(current_rows, GRID_WIDTH)
    
    gap = GRID_WIDTH // current_rows
    texture_manager.update_scaled_textures(gap)
    
    buttons = create_buttons(button_font, small_font, texture_manager)

    algorithm_generator = {
            "generator": None,
            "running": False,
            "step_interval_ms": 25,
            "last_step_time": 0,
        }
    run = True
    race_mode = False
    
    clock = pygame.time.Clock() 
    
    while run:
        draw(
            win, grid, current_rows, GRID_WIDTH, buttons, 
            grid_lines_visible, error_message, texture_manager
        )
        
        events = pygame.event.get()
        
        result = handle_events(
            run, events, grid, current_rows, start_node, end_node, win, GRID_WIDTH,
            currrent_square_colour, buttons, grid_lines_visible, drawing_mode,
            error_message, current_algorithm, algorithm_generator, race_mode,
            texture_manager 
        )
        (run, start_node, end_node, currrent_square_colour, 
         grid, grid_lines_visible, drawing_mode, current_rows, 
         error_message, current_algorithm, race_mode) = result
        

        current_ticks = pygame.time.get_ticks()
        if algorithm_generator["running"] and algorithm_generator["generator"] and \
           current_ticks - algorithm_generator["last_step_time"] >= algorithm_generator["step_interval_ms"]:
            
            try:
                next(algorithm_generator["generator"])
            except StopIteration:
                algorithm_generator["running"] = False
                algorithm_generator["generator"] = None
            algorithm_generator["last_step_time"] = current_ticks


        # --- MODIFICARE: Separare clară între Mac și Windows ---
        if drawing_mode == "get_matrix_mac":
            # Varianta Custom UI (pentru Mac)
            matrix_text = start_load_window(win, use_pyperclip=True)
            
            if matrix_text is not None:
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
                    gap = GRID_WIDTH // current_rows
                    texture_manager.update_scaled_textures(gap)
            drawing_mode = "just_loaded"

        elif drawing_mode == "get_matrix_win":
            # Varianta EasyGUI Originală (pentru Windows/Linux)
            
            # Minimizăm pentru a evita probleme de focus
            pygame.display.iconify()
            
            matrix_text = get_matrix_input_popup()
            
            # Curățăm evenimentele și restaurăm
            pygame.event.clear(pygame.MOUSEBUTTONDOWN)
            pygame.event.clear(pygame.MOUSEBUTTONUP)
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
                    gap = GRID_WIDTH // current_rows
                    texture_manager.update_scaled_textures(gap)
            else:
                error_message = "Load operation cancelled."
            
            drawing_mode = "just_loaded"
        # --- SFÂRȘIT MODIFICARE ---
        
        clock.tick(60) 

    pygame.quit()

if __name__ == "__main__":
    WIN = pygame.display.set_mode((TOTAL_WIDTH, TOTAL_HEIGHT))
    pygame.display.set_caption("Pathfinding Visualisation Sandbox")
    
    main(WIN, GRID_WIDTH)