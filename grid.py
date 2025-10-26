
import pygame
from graphical_interface.spot import Spot
from graphical_interface.constants import *
from algorithms.bfs import bfs

def draw(win, grid, rows, width, buttons, grid_lines_visible):
    win.fill(WHITE)

    # Draw side menus (simple colored rectangles for now)
    # Left Menu
    pygame.draw.rect(win, GREY, (0, 0, SIDE_MENU_WIDTH, TOTAL_HEIGHT))
    # Right Menu
    pygame.draw.rect(win, GREY, (GRID_X_OFFSET + GRID_WIDTH, 0, SIDE_MENU_WIDTH, TOTAL_HEIGHT))

    for row in grid:
        for spot in row:
            spot.draw(win)

    # Draw grid lines IF they are visible
    if grid_lines_visible:
        gap = width // rows
        for i in range(rows + 1):
            # Horizontal lines
            pygame.draw.line(win, BLACK, (GRID_X_OFFSET, GRID_Y_OFFSET + i * gap), (GRID_X_OFFSET + width, GRID_Y_OFFSET + i * gap))
            # Vertical lines
            pygame.draw.line(win, BLACK, (GRID_X_OFFSET + i * gap, GRID_Y_OFFSET), (GRID_X_OFFSET + i * gap, GRID_Y_OFFSET + width))
    
    # Draw all buttons
    for button in buttons:
        button.draw(win)

    pygame.display.update()


def make_grid(rows, width):
    grid = []
    gap = width // rows
    for i in range(rows):
        grid.append([])
        for j in range(rows):
            spot = Spot(i, j, gap, rows)
            if i == 0 or i == rows - 1 or j == 0 or j == rows - 1:
                spot.mark_barrier()
            grid[i].append(spot)
    return grid

def get_clicked_pos(pos, rows, width):
    gap = width // rows
    x, y = pos

    # Subtract the offset to get coordinates relative to the grid
    relative_y = y - GRID_Y_OFFSET
    relative_x = x - GRID_X_OFFSET
    
    row = relative_y // gap
    col = relative_x // gap

    # Check if the click was outside the grid boundaries
    if not (0 <= row < rows and 0 <= col < rows):
        return None, None # Return None if click is outside

    return row, col
