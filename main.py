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


# helper functions

def update_win_loss_messages(win_start, loss_start):
    now = pygame.time.get_ticks()

    show_win = win_start > 0 and now - win_start < 5000
    if not show_win:
        win_start = 0

    show_loss = loss_start > 0 and now - loss_start < 5000
    if not show_loss:
        loss_start = 0

    return show_win, show_loss, win_start, loss_start



def update_race_timer(race_mode, race_timer, race_button):
    if not race_mode:
        return race_timer
    if race_timer["running"]:
        race_timer["elapsed_ms"] = pygame.time.get_ticks() - race_timer["start_time"]
        race_button.update_time(race_timer["elapsed_ms"])
    else:
        race_timer["elapsed_ms"] = 0
    return race_timer


def advance_algorithm_step(algorithm_generator, race_mode, race_timer, buttons):
    now = pygame.time.get_ticks()
    loss_trigger = None

    if not algorithm_generator["running"]:
        return race_mode, race_timer, None

    gen = algorithm_generator["generator"]
    if not gen:
        return race_mode, race_timer, None

    if now - algorithm_generator["last_step_time"] < algorithm_generator["step_interval_ms"]:
        return race_mode, race_timer, None

    try:
        next(gen)
    except StopIteration:
        if race_mode and race_timer["running"]:
            race_timer["running"] = False
            race_mode = False
            loss_trigger = pygame.time.get_ticks()
            for btn in buttons:
                if "Race Mode" in btn.text:
                    btn.update_text("Race Mode: OFF")
                    btn.base_color = GREEN
                    btn.hovering_color = BLUE
                    break

    algorithm_generator["last_step_time"] = now
    return race_mode, race_timer, loss_trigger


def load_matrix_and_update_state(matrix_text, GRID_WIDTH, texture_manager):
    if not matrix_text:
        return None, None, None, None, "Load operation cancelled."

    grid, rows, start, end, err = parse_and_load_matrix(matrix_text, GRID_WIDTH)
    if err:
        return None, None, None, None, err

    gap = GRID_WIDTH // rows
    texture_manager.update_scaled_textures(gap)

    return grid, rows, start, end, None


def handle_matrix_mode(drawing_mode, win, GRID_WIDTH, texture_manager):
    if drawing_mode == "choose_preset":
        result = start_preset_chooser(win)
        pygame.event.clear()
        if not result:
            return True, None, None, None, None, None, False
        matrix_text, is_secret = result
        # new_grid, new_rows, new_start, new_end, err_msg
        g, r, s, e, err = load_matrix_and_update_state(matrix_text, GRID_WIDTH, texture_manager)
        return True, g, r, s, e, err, is_secret

    if drawing_mode == "get_matrix_mac":
        matrix_text = start_load_window(win, use_pyperclip=True)
        pygame.event.clear()
        g, r, s, e, err = load_matrix_and_update_state(matrix_text, GRID_WIDTH, texture_manager)
        return True, g, r, s, e, err, False

    if drawing_mode == "get_matrix_win":
        pygame.display.iconify()
        matrix_text = get_matrix_input_popup()
        pygame.display.set_mode((TOTAL_WIDTH, TOTAL_HEIGHT))
        pygame.event.clear()
        g, r, s, e, err = load_matrix_and_update_state(matrix_text, GRID_WIDTH, texture_manager)
        return True, g, r, s, e, err, False

    return False, None, None, None, None, None, False


def main(win, width):
    # check if textures loaded
    if not os.path.isdir('assets/textures'):
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
    
    buttons, race_timer_button = create_buttons(button_font, small_font, texture_manager)

    algorithm_generator = {
            "generator": None,
            "running": False,
            "step_interval_ms": 40, # controls how fast algorithm updates visually
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
        # loss message 5 seconds; user can't draw new walls
        show_win_message, show_loss_message, win_start_time, loss_start_time = \
            update_win_loss_messages(win_start_time, loss_start_time)

        previous_rows = current_rows

        events = pygame.event.get()
        
        input_blocked = show_win_message or show_loss_message

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
        
        if current_rows != previous_rows:
            show_secret_message = False

        race_timer = update_race_timer(race_mode, race_timer, race_timer_button)

        race_mode, race_timer, loss_trigger = advance_algorithm_step(
            algorithm_generator, race_mode, race_timer, buttons
        )
        if loss_trigger:
            loss_start_time = loss_trigger
        # new_grid, new_rows, new_start, new_end, err_msg
        apply_matrix, g, r, s, e, err, secret = \
            handle_matrix_mode(drawing_mode, win, GRID_WIDTH, texture_manager)

        if apply_matrix:
            if g is not None:
                grid, current_rows, start_node, end_node = g, r, s, e
                show_secret_message = secret
                error_message = err
            else:
                error_message = err
            drawing_mode = "just_loaded"
            pygame.event.clear()

        draw(
            win, grid, current_rows, GRID_WIDTH, buttons, 
            grid_lines_visible, error_message, texture_manager, race_mode, race_timer_button,
            show_secret_message, race_timer["running"], show_win_message, show_loss_message
        )

        clock.tick(60) 

    pygame.quit()


if __name__ == "__main__":
    WIN = pygame.display.set_mode((TOTAL_WIDTH, TOTAL_HEIGHT))
    pygame.display.set_caption("Pathfinding Visualisation Sandbox")
    
    main(WIN, GRID_WIDTH)
