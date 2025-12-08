import pygame
from graphical_interface.spot import Spot
from graphical_interface.constants import *


def draw_race_timer(win, elapsed_ms):
    font = pygame.font.SysFont("Arial", 28, bold=True)
    seconds = elapsed_ms // 1000
    millis = (elapsed_ms % 1000) // 10
    text_surface = font.render(f"Time: {seconds}.{millis:02}s", True, BLACK)
    x = GRID_X_OFFSET + GRID_WIDTH + (SIDE_MENU_WIDTH // 2)
    y = 120  # under the Race Mode button
    rect = text_surface.get_rect(center=(x, y))
    win.blit(text_surface, rect)

def draw(win, grid, rows, width, buttons, grid_lines_visible, error_message, texture_manager, race_mode, race_timer_button, show_secret_message):
    # Am adăugat texture_manager ca parametru
    
    win.fill(WHITE)

    # draw side menus
    pygame.draw.rect(win, GREY, (0, 0, SIDE_MENU_WIDTH, TOTAL_HEIGHT))
    pygame.draw.rect(win, GREY, (GRID_X_OFFSET + GRID_WIDTH, 0, SIDE_MENU_WIDTH, TOTAL_HEIGHT))

    # grid frame
    pygame.draw.rect(win, BLACK, (GRID_X_OFFSET, GRID_Y_OFFSET, GRID_WIDTH, GRID_HEIGHT))

    gap = width // rows
    actual_grid_size = gap * rows
    padding = (width - actual_grid_size) // 2

    font = pygame.font.SysFont("Arial", 22)
    usable_size = rows - 2
    size_text = font.render(f"{usable_size}x{usable_size} Grid", True, BLACK)
    button_x_right_menu = GRID_X_OFFSET + GRID_WIDTH + 50
    text_center_x = button_x_right_menu + 100 
    text_rect = size_text.get_rect(center=(text_center_x, 345)) 
    win.blit(size_text, text_rect)

    for row in grid:
        for spot in row:
            spot.draw(win, padding, padding, texture_manager)

    if grid_lines_visible:
        for i in range(rows + 1):
            pygame.draw.line(
                win, BLACK, (GRID_X_OFFSET + padding, GRID_Y_OFFSET + padding + i * gap),
                (GRID_X_OFFSET + padding + actual_grid_size, GRID_Y_OFFSET + padding + i * gap))
            pygame.draw.line(
                win, BLACK, (GRID_X_OFFSET + padding + i * gap, GRID_Y_OFFSET + padding),
                  (GRID_X_OFFSET + padding + i * gap, GRID_Y_OFFSET + padding + actual_grid_size))
    
    # --- FIX 2: Înlocuit emoji cu asteriscuri ---
    if show_secret_message:
        msg_font = pygame.font.SysFont("Arial", 20, bold=True)
        # Am șters emoji-urile ⭐ și am pus *
        msg_text = msg_font.render("* If you like our project please give us a star! *", True, (255, 215, 0)) 
        
        msg_bg_surface = pygame.Surface((GRID_WIDTH, 40))
        msg_bg_surface.set_alpha(180) 
        msg_bg_surface.fill((0, 0, 0))
        
        win.blit(msg_bg_surface, (GRID_X_OFFSET, GRID_Y_OFFSET)) 
        
        text_rect = msg_text.get_rect(center=(GRID_X_OFFSET + GRID_WIDTH // 2, GRID_Y_OFFSET + 20))
        win.blit(msg_text, text_rect)
    # --- SFÂRȘIT FIX ---

    for button in buttons:
        button.draw(win)
    if race_mode:
        race_timer_button.draw(win)
    # draw the error message
    if error_message:
        error_font = pygame.font.SysFont("Arial", 20, bold=True)
        error_surface = error_font.render(error_message, True, BUTTON_RED)
        error_rect = error_surface.get_rect(center=(SIDE_MENU_WIDTH // 2, TOTAL_HEIGHT - 30))
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
    relative_x = x - GRID_X_OFFSET - padding
    relative_y = y - GRID_Y_OFFSET - padding
    
    row = relative_y // gap
    col = relative_x // gap

    if not (0 <= row < rows and 0 <= col < rows):
        return None, None

    return row, col