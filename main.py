import random
import re
import os # Necesar pentru a verifica existența folderului de assets

import easygui
import pygame

from algorithms.bfs import bfs
from algorithms.dfs import dfs
from algorithms.best_first_search import greedyBestFirstSearch
from events import handle_events
from grid import draw, get_clicked_pos, make_grid
# --- MODIFICARE ---
# Am adăugat 'create_buttons' la import
from graphical_interface.button import Button, ImageButton, RaceTimerButton, create_buttons
# --- SFÂRȘIT MODIFICARE ---
from graphical_interface.spot import Spot
from graphical_interface.constants import *
from initialize_matrix import parse_and_load_matrix, start_load_window
from texture_manager import TextureManager # Importăm noul manager

def main(win, width):
    
    # Verificăm dacă folderul de assets există
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
    
    current_algorithm = "bfs" # default to BFS

    pygame.font.init()
    button_font = pygame.font.SysFont("Arial", 24)
    small_font = pygame.font.SysFont("Arial", 30, bold=True) 
    
    # --- Modificări pentru Texturi ---
    # 1. Inițializăm managerul (încarcă imaginile originale)
    texture_manager = TextureManager()
    
    # 2. Creăm grila
    grid = make_grid(current_rows, GRID_WIDTH)
    
    # 3. Calculăm gap-ul inițial și actualizăm texturile scalate
    gap = GRID_WIDTH // current_rows
    texture_manager.update_scaled_textures(gap)
    
    # 4. Pasăm managerul de texturi la funcția de creare a butoanelor
    # --- MODIFICARE ---
    # Am eliminat 'Button.' din apel
    buttons, race_timer_button = create_buttons(button_font, small_font, texture_manager)
    # --- SFÂRȘIT MODIFICARE ---
    # --- Sfârșitul modificărilor pentru texturi ---

    algorithm_generator = {
            "generator": None,
            "running": False,
            "step_interval_ms": 25,
            "last_step_time": 0,
        }
    run = True
    race_mode = False
    race_timer = {
        "running": False,
        "start_time": 0,
        "elapsed_ms": 0
    }
    
    clock = pygame.time.Clock() # Adăugăm un ceas pentru a controla FPS-ul
    
    while run:
        # Pasăm și managerul de texturi funcției 'draw'
        draw(
            win, grid, current_rows, GRID_WIDTH, buttons, 
            grid_lines_visible, error_message, texture_manager, race_mode, race_timer_button
        )
        
        events = pygame.event.get()
        

        

        result = handle_events(
            run, events, grid, current_rows, start_node, end_node, win, GRID_WIDTH,
            currrent_square_colour, buttons, grid_lines_visible, drawing_mode,
            error_message, current_algorithm, algorithm_generator,
            texture_manager, race_mode, race_timer
        )
        # unpack all returned values
        (run, start_node, end_node, currrent_square_colour, 
         grid, grid_lines_visible, drawing_mode, current_rows, 
         error_message, current_algorithm, race_mode) = result
        
        if race_mode:
            if race_timer["running"]:
                # Calculate time (Use 'start_time' to match your initialization)
                race_timer["elapsed_ms"] = pygame.time.get_ticks() - race_timer["start_time"]
                # Update the button visual text
                race_timer_button.update_time(race_timer["elapsed_ms"])
            else:
                # Reset to 0.0s if race is ON but hasn't started yet
                race_timer["elapsed_ms"] = 0

        # Logica pentru rularea algoritmului (mutată din events.py pentru claritate)
        current_ticks = pygame.time.get_ticks()
        if algorithm_generator["running"] and algorithm_generator["generator"] and \
           current_ticks - algorithm_generator["last_step_time"] >= algorithm_generator["step_interval_ms"]:
            
            try:
                next(algorithm_generator["generator"])
            except StopIteration:
                algorithm_generator["running"] = False
                algorithm_generator["generator"] = None
                if race_mode and race_timer["running"]:
                    race_timer["running"] = False
            algorithm_generator["last_step_time"] = current_ticks


        if drawing_mode == "get_matrix":
            
            matrix_text = start_load_window(win)
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
                    # --- Modificare Texturi ---
                    # Recalculăm texturile scalate pentru noua mărime a grilei
                    gap = GRID_WIDTH // current_rows
                    texture_manager.update_scaled_textures(gap)
                    # --- Sfârșit Modificare ---
            
            drawing_mode = "just_loaded"
        
        clock.tick(60) # Limităm la 60 FPS

    pygame.quit()

if __name__ == "__main__":
    WIN = pygame.display.set_mode((TOTAL_WIDTH, TOTAL_HEIGHT))
    pygame.display.set_caption("Pathfinding Visualisation Sandbox")
    
    main(WIN, GRID_WIDTH)