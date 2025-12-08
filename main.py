import random
import re
import os 
import easygui
import pygame

from algorithms.bfs import bfs
from algorithms.dfs import dfs
from algorithms.best_first_search import greedyBestFirstSearch
from managers.event_handler import handle_events
from core.grid import draw, get_clicked_pos, make_grid
from ui.button import Button, ImageButton, RaceTimerButton, create_buttons
from ui.spot import Spot
from ui.constants import *
from core.matrix_utils import parse_and_load_matrix, start_load_window, get_matrix_input_popup
from managers.texture_manager import TextureManager 
from ui.preset_chooser import start_preset_chooser

def main(win, width):
    if not os.path.isdir('assets/textures'):
        print("EROARE: Folderul 'assets/textures' nu a fost găsit.")
        print("Te rog asigură-te că ai 21 de imagini în 'assets/textures'")
        pygame.quit()
        return

    current_rows = 20
    
    currrent_square_colour = RED
    start_node = None
    end_node = None
    grid_lines_visible = False
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
    
    # 4. Pasăm managerul de texturi la funcția de creare a butoanelor
    # --- MODIFICARE ---
    # Am eliminat 'Button.' din apel
    buttons, race_timer_button = create_buttons(button_font, small_font, texture_manager)
    # --- SFÂRȘIT MODIFICARE ---
    # --- Sfârșitul modificărilor pentru texturi ---

    algorithm_generator = {
            "generator": None,
            "running": False,
            "step_interval_ms": 2,
            "last_step_time": 0,
        }
    run = True
    race_mode = False
    race_timer = {
        "running": False,
        "start_time": 0,
        "elapsed_ms": 0
    }
    
    show_secret_message = False
    win_start_time = 0
    loss_start_time = 0
    clock = pygame.time.Clock() 
    
    while run:
        show_win_message = False
        show_loss_message= False
        # ca sa nu spameze
        if win_start_time > 0:
            if pygame.time.get_ticks() - win_start_time < 5000:
                show_win_message = True
            else:
                win_start_time = 0
        if loss_start_time > 0:
            if pygame.time.get_ticks() - loss_start_time < 5000:
                show_loss_message = True
            else:
                loss_start_time = 0
        
        
        previous_rows = current_rows

        events = pygame.event.get()
        
        input_blocked = show_win_message or show_loss_message # no walls when loss/win is shown

        result = handle_events(
            run, events, grid, current_rows, start_node, end_node, win, GRID_WIDTH,
            currrent_square_colour, buttons, grid_lines_visible, drawing_mode,
            error_message, current_algorithm, algorithm_generator,
            texture_manager, race_mode, race_timer, race_timer_button, show_secret_message, input_blocked
        )
        (run, start_node, end_node, currrent_square_colour, 
         grid, grid_lines_visible, drawing_mode, current_rows, 
         error_message, current_algorithm, race_mode, win_triggered) = result
        
        if win_triggered:
            win_start_time = pygame.time.get_ticks()
        
        if race_mode:
            if race_timer["running"]:
                # Calculate time (Use 'start_time' to match your initialization)
                race_timer["elapsed_ms"] = pygame.time.get_ticks() - race_timer["start_time"]
                # Update the button visual text
                race_timer_button.update_time(race_timer["elapsed_ms"])
            else:
                # Reset to 0.0s if race is ON but hasn't started yet
                race_timer["elapsed_ms"] = 0
        if current_rows != previous_rows:
             show_secret_message = False

        current_ticks = pygame.time.get_ticks()
        if algorithm_generator["running"] and algorithm_generator["generator"] and \
           current_ticks - algorithm_generator["last_step_time"] >= algorithm_generator["step_interval_ms"]:
            
            try:
                next(algorithm_generator["generator"])
            except StopIteration:
                if race_mode and race_timer["running"]:
                    print("USER LOST! Algorithm finished first.")
                    race_timer["running"] = False
                    race_mode = False
                    loss_start_time = pygame.time.get_ticks()
                    show_loss_message = True
                    
                    # Update the button visually to OFF
                    # We look for the button in the list to update it
                    for btn in buttons:
                        if "Race Mode" in btn.text:
                            btn.update_text("Race Mode: OFF")
                            btn.base_color = GREEN
                            btn.hovering_color = BLUE
                            break
            algorithm_generator["last_step_time"] = current_ticks

        draw(
            win, grid, current_rows, GRID_WIDTH, buttons, 
            grid_lines_visible, error_message, texture_manager, race_mode, race_timer_button,
            show_secret_message, race_timer["running"], show_win_message, show_loss_message
        )

        if drawing_mode == "choose_preset":
            result = start_preset_chooser(win)
            
            pygame.event.clear()
            
            matrix_text = None
            is_secret = False
            
            if result:
                matrix_text, is_secret = result
            
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
                    
                    show_secret_message = is_secret
            
            # --- FIX: Setăm modul "just_loaded" și așteptăm ridicarea click-ului ---
            drawing_mode = "just_loaded"
            pygame.event.clear() # Curățăm orice click rezidual

        if drawing_mode == "get_matrix_mac":
            matrix_text = start_load_window(win, use_pyperclip=True)
            
            pygame.event.clear()
            
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
                    show_secret_message = False 
            
            drawing_mode = "just_loaded"
            pygame.event.clear()

        elif drawing_mode == "get_matrix_win":
            pygame.display.iconify()
            matrix_text = get_matrix_input_popup()
            
            pygame.display.set_mode((TOTAL_WIDTH, TOTAL_HEIGHT))
            
            pygame.event.clear()
            
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
                    show_secret_message = False 
            else:
                error_message = "Load operation cancelled."
            
            drawing_mode = "just_loaded"
            pygame.event.clear() # Încă o curățare pentru siguranță
        
        clock.tick(60) 

    pygame.quit()

if __name__ == "__main__":
    WIN = pygame.display.set_mode((TOTAL_WIDTH, TOTAL_HEIGHT))
    pygame.display.set_caption("Pathfinding Visualisation Sandbox")
    
    main(WIN, GRID_WIDTH)