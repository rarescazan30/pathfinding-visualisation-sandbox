
import pygame
from graphical_interface.spot import Spot
from graphical_interface.constants import *


def draw(win, grid, rows, width, buttons, grid_lines_visible, error_message):
    win.fill(WHITE)

    # draw side menus
    pygame.draw.rect(win, GREY, (0, 0, SIDE_MENU_WIDTH, TOTAL_HEIGHT))
    pygame.draw.rect(win, GREY, (GRID_X_OFFSET + GRID_WIDTH, 0, SIDE_MENU_WIDTH, TOTAL_HEIGHT))

    # grid frame
    pygame.draw.rect(win, BLACK, (GRID_X_OFFSET, GRID_Y_OFFSET, GRID_WIDTH, GRID_HEIGHT))

    # padding for variable size of grid
    gap = width // rows
    actual_grid_size = gap * rows
    padding = (width - actual_grid_size) // 2

    # draw the grid size text
    font = pygame.font.SysFont("Arial", 22)
    usable_size = rows - 2
    size_text = font.render(f"{usable_size}x{usable_size} Grid", True, BLACK)
    button_x_right_menu = GRID_X_OFFSET + GRID_WIDTH + 50
    text_center_x = button_x_right_menu + 100
    text_rect = size_text.get_rect(center=(text_center_x, 350))
    win.blit(size_text, text_rect)

    for row in grid:
        for spot in row:
            spot.draw(win, padding, padding)


    if grid_lines_visible:
        for i in range(rows + 1):
            # horizontal and vertical lines
            pygame.draw.line(
                win, BLACK, (GRID_X_OFFSET + padding, GRID_Y_OFFSET + padding + i * gap),
                (GRID_X_OFFSET + padding + actual_grid_size, GRID_Y_OFFSET + padding + i * gap))
            pygame.draw.line(
                win, BLACK, (GRID_X_OFFSET + padding + i * gap, GRID_Y_OFFSET + padding),
                  (GRID_X_OFFSET + padding + i * gap, GRID_Y_OFFSET + padding + actual_grid_size))
    
    # draw the ui buttons
    for button in buttons:
        button.draw(win)

    # draw the error message
    if error_message:
        error_font = pygame.font.SysFont("Arial", 35, bold=True)
        error_surface = error_font.render(error_message, True, BUTTON_RED)
        error_rect = error_surface.get_rect(center=(SIDE_MENU_WIDTH // 2, 500))
        win.blit(error_surface, error_rect)

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
    actual_grid_size = gap * rows
    padding = (width - actual_grid_size) // 2
    
    x, y = pos
    # account for padding
    relative_x = x - GRID_X_OFFSET - padding
    relative_y = y - GRID_Y_OFFSET - padding
    
    row = relative_y // gap
    col = relative_x // gap

    if not (0 <= row < rows and 0 <= col < rows):
        return None, None

    return row, col
