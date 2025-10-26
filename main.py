# main.py

import pygame
import random
from graphical_interface.constants import *
from graphical_interface.spot import Spot
from graphical_interface.button import Button
from algorithms.bfs import bfs
from events import handle_events
from grid import draw, make_grid, get_clicked_pos

def main(win, width):
    ROWS = 40
    grid = make_grid(ROWS, GRID_WIDTH)
    
    currrent_square_colour = RED
    start_node = None
    end_node = None
    
    grid_lines_visible = True
    
    # --- NEW STATE VARIABLE ---
    drawing_mode = "maker" # Can be "maker" or "eraser"

    pygame.font.init()
    button_font = pygame.font.SysFont("Arial", 24)

    button_x = GRID_X_OFFSET + GRID_WIDTH + 50
    
    find_path_button = Button(
        x=button_x, y=100, width=200, height=50,
        text="Find Path", font=button_font,
        base_color=GREEN, hovering_color=BLUE
    )
    toggle_grid_button = Button(
        x=button_x, y=180, width=200, height=50,
        text="Toggle Grid", font=button_font,
        base_color=PURPLE, hovering_color=ORANGE
    )
    # --- NEW BUTTON INSTANCE ---
    toggle_mode_button = Button(
        x=button_x, y=260, width=200, height=50,
        text="Switch to Eraser", font=button_font, # Initial text
        base_color=(200, 50, 50), hovering_color=(250, 100, 100) # Reddish colors
    )
    
    # --- ADD NEW BUTTON TO THE LIST ---
    buttons = [find_path_button, toggle_grid_button, toggle_mode_button]

    run = True
    while run:
        draw(win, grid, ROWS, GRID_WIDTH, buttons, grid_lines_visible)
        
        # --- PASS AND RECEIVE THE NEW STATE ---
        result = handle_events(
            grid, ROWS, start_node, end_node, win, GRID_WIDTH,
            currrent_square_colour, buttons, grid_lines_visible, drawing_mode
        )
        
        run, start_node, end_node, currrent_square_colour, grid, grid_lines_visible, drawing_mode = result

    pygame.quit()

if __name__ == "__main__":
    WIN = pygame.display.set_mode((TOTAL_WIDTH, TOTAL_HEIGHT))
    pygame.display.set_caption("Pathfinding Visualisation Sandbox")
    main(WIN, GRID_WIDTH)