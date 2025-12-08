import pygame
from ui.spot import Spot
from ui.constants import *



def make_grid(rows, width):
    grid = []
    gap = width // rows
    for i in range(rows):
        grid.append([])
        for j in range(rows):
            spot = Spot(i, j, gap, rows)
            # Set the outer boundary as barriers automatically
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

# Draws the floating timer during Race Mode
def draw_race_timer(win, elapsed_ms):
    font = pygame.font.SysFont("Arial", 28, bold=True)
    seconds = elapsed_ms // 1000
    millis = (elapsed_ms % 1000) // 10
    text_surface = font.render(f"Time: {seconds}.{millis:02}s", True, BLACK)
    
    x = GRID_X_OFFSET + GRID_WIDTH + (SIDE_MENU_WIDTH // 2)
    y = 120  
    rect = text_surface.get_rect(center=(x, y))
    win.blit(text_surface, rect)

# Draws the Green Victory Popup
def draw_win_message(win, time_text):
    font_title = pygame.font.SysFont("Verdana", 50, bold=True)
    font_time = pygame.font.SysFont("Verdana", 30, bold=True)
    
    text_title = font_title.render("YOU WON!", True, WHITE)
    text_time = font_time.render(time_text, True, WHITE)
    
    center_x = GRID_X_OFFSET + GRID_WIDTH // 2
    center_y = GRID_Y_OFFSET + GRID_HEIGHT // 2
    
    rect_title = text_title.get_rect(midbottom=(center_x, center_y - 5))
    rect_time = text_time.get_rect(midtop=(center_x, center_y + 5))
    
    content_rect = rect_title.union(rect_time)
    bg_rect = content_rect.inflate(80, 50)
    
    pygame.draw.rect(win, GREEN, bg_rect, border_radius=20)
    pygame.draw.rect(win, YELLOW, bg_rect, 6, border_radius=20)
    
    win.blit(text_title, rect_title)
    win.blit(text_time, rect_time)

# Draws the Red Defeat Popup
def draw_loss_message(win, time_text):
    font_title = pygame.font.SysFont("Verdana", 50, bold=True)
    font_time = pygame.font.SysFont("Verdana", 30, bold=True)
    
    text_title = font_title.render("YOU LOST!", True, WHITE)
    text_time = font_time.render(time_text, True, WHITE)

    center_x = GRID_X_OFFSET + GRID_WIDTH // 2
    center_y = GRID_Y_OFFSET + GRID_HEIGHT // 2
    
    rect_title = text_title.get_rect(midbottom=(center_x, center_y - 5))
    rect_time = text_time.get_rect(midtop=(center_x, center_y + 5))
    
    content_rect = rect_title.union(rect_time)
    bg_rect = content_rect.inflate(80, 50)
    
    pygame.draw.rect(win, BUTTON_RED, bg_rect, border_radius=20)
    pygame.draw.rect(win, (150, 50, 50), bg_rect, 6, border_radius=20)
    
    win.blit(text_title, rect_title)
    win.blit(text_time, rect_time)

# Draws the transparent overlay prompting user to start the race
def draw_race_start_prompt(win):
    font = pygame.font.SysFont("Verdana", 30, bold=True)
    text = font.render("Click on the grid to Start Race!", True, WHITE)
    
    text_rect = text.get_rect(center=(GRID_X_OFFSET + GRID_WIDTH // 2, GRID_Y_OFFSET + GRID_HEIGHT // 2))
    bg_rect = text_rect.inflate(60, 40)
    
    # Transparent so user can see grid
    transparent_surface = pygame.Surface(bg_rect.size, pygame.SRCALPHA)
    pygame.draw.rect(transparent_surface, (0, 0, 0, 90), transparent_surface.get_rect(), border_radius=15)
    
    win.blit(transparent_surface, bg_rect.topleft)
    win.blit(text, text_rect)

# Draws the banner at the top of the grid
def draw_secret_message_banner(win):
    msg_font = pygame.font.SysFont("Arial", 20, bold=True)
    msg_text = msg_font.render("* If you like our project please give us a star! *", True, (255, 215, 0)) 
    
    msg_bg_surface = pygame.Surface((GRID_WIDTH, 40))
    msg_bg_surface.set_alpha(180) 
    msg_bg_surface.fill((0, 0, 0))
    
    win.blit(msg_bg_surface, (GRID_X_OFFSET, GRID_Y_OFFSET)) 
    
    text_rect = msg_text.get_rect(center=(GRID_X_OFFSET + GRID_WIDTH // 2, GRID_Y_OFFSET + 20))
    win.blit(msg_text, text_rect)


def draw(win, grid, rows, width, buttons, grid_lines_visible, error_message, texture_manager, race_mode, race_timer_button, show_secret_message, race_started=False, show_win_message=False, show_loss_message=False):
    win.fill(WHITE)

    # Static Layout Elements
    pygame.draw.rect(win, GREY, (0, 0, SIDE_MENU_WIDTH, TOTAL_HEIGHT))
    pygame.draw.rect(win, GREY, (GRID_X_OFFSET + GRID_WIDTH, 0, SIDE_MENU_WIDTH, TOTAL_HEIGHT))
    pygame.draw.rect(win, BLACK, (GRID_X_OFFSET, GRID_Y_OFFSET, GRID_WIDTH, GRID_HEIGHT))

    # Grid Size Indicator (Right Menu)
    gap = width // rows
    actual_grid_size = gap * rows
    padding = (width - actual_grid_size) // 2

    font = pygame.font.SysFont("Arial", 22)
    usable_size = rows - 2
    size_text = font.render(f"{usable_size}x{usable_size}", True, BLACK)
    
    button_x_right_menu = GRID_X_OFFSET + GRID_WIDTH + 50
    text_center_x = button_x_right_menu + 90
    text_rect = size_text.get_rect(center=(text_center_x, 355)) 
    win.blit(size_text, text_rect)

    # Spots
    for row in grid:
        for spot in row:
            spot.draw(win, padding, padding, texture_manager)

    # Grid Lines
    if grid_lines_visible:
        for i in range(rows + 1):
            pygame.draw.line(
                win, BLACK, (GRID_X_OFFSET + padding, GRID_Y_OFFSET + padding + i * gap),
                (GRID_X_OFFSET + padding + actual_grid_size, GRID_Y_OFFSET + padding + i * gap))
            pygame.draw.line(
                win, BLACK, (GRID_X_OFFSET + padding + i * gap, GRID_Y_OFFSET + padding),
                  (GRID_X_OFFSET + padding + i * gap, GRID_Y_OFFSET + padding + actual_grid_size))
    
    if show_secret_message:
        draw_secret_message_banner(win)

    for button in buttons:
        button.draw(win)
        
    if race_mode:
        race_timer_button.draw(win)
    
    # Overlays (Win/Loss/Start)
    if show_win_message:
        draw_win_message(win, race_timer_button.text)
    
    if show_loss_message:
        draw_loss_message(win, race_timer_button.text)

    if race_mode and not race_started:
        draw_race_start_prompt(win)
    
    if error_message:
        error_font = pygame.font.SysFont("Arial", 20, bold=True)
        error_surface = error_font.render(error_message, True, BUTTON_RED)
        error_rect = error_surface.get_rect(center=(SIDE_MENU_WIDTH // 2, TOTAL_HEIGHT - 30))
        win.blit(error_surface, error_rect)
        
    pygame.display.update()