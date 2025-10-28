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
    # Reverted to a simple integer for grid size
    current_rows = 40
    grid = make_grid(current_rows, GRID_WIDTH)
    
    currrent_square_colour = RED
    start_node = None
    end_node = None
    
    grid_lines_visible = True
    drawing_mode = "maker"

    pygame.font.init()
    button_font = pygame.font.SysFont("Arial", 24)
    small_font = pygame.font.SysFont("Arial", 30, bold=True) 

    button_x = GRID_X_OFFSET + GRID_WIDTH + 50
    
    find_path_button = Button(x=button_x, y=100, width=200, height=50, text="Find Path", font=button_font, base_color=GREEN, hovering_color=BLUE)
    toggle_grid_button = Button(x=button_x, y=180, width=200, height=50, text="Toggle Grid", font=button_font, base_color=PURPLE, hovering_color=ORANGE)
    toggle_mode_button = Button(x=button_x, y=260, width=200, height=50, text="Switch to Eraser", font=button_font, base_color=(200, 50, 50), hovering_color=(250, 100, 100))
    decrease_button = Button(x=button_x, y=380, width=50, height=50, text="-", font=small_font, base_color=GREY, hovering_color=(190, 190, 190))
    increase_button = Button(x=button_x + 150, y=380, width=50, height=50, text="+", font=small_font, base_color=GREY, hovering_color=(190, 190, 190))
    
    buttons = [find_path_button, toggle_grid_button, toggle_mode_button, decrease_button, increase_button]

    run = True
    while run:
        draw(win, grid, current_rows, GRID_WIDTH, buttons, grid_lines_visible)
        
        # We no longer pass VALID_SIZES
        result = handle_events(
            grid, current_rows, start_node, end_node, win, GRID_WIDTH,
            currrent_square_colour, buttons, grid_lines_visible, drawing_mode
        )
        
        run, start_node, end_node, currrent_square_colour, grid, grid_lines_visible, drawing_mode, current_rows = result

    pygame.quit()

if __name__ == "__main__":
    WIN = pygame.display.set_mode((TOTAL_WIDTH, TOTAL_HEIGHT))
    pygame.display.set_caption("Pathfinding Visualisation Sandbox")
    main(WIN, GRID_WIDTH)