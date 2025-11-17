import re
import pygame
import pygame_textinput
import pygame.scrap

import easygui
from grid import make_grid
from graphical_interface.spot import Spot
from graphical_interface.constants import *


""""

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
        error_font = pygame.font.SysFont("Arial", 18, bold=True)
        error_surface = error_font.render(error_message, True, (200, 0, 0))
        error_rect = error_surface.get_rect(center=(SIDE_MENU_WIDTH // 2, 480))
        win.blit(error_surface, error_rect)

    pygame.display.update()


"""
def draw_for_load_window(win, text_surface, input_rect, paste_btn_rect, done_btn_rect):
    width, height = win.get_width(), win.get_height()
    win.fill(WHITE)

    box_w, box_h = 600, 300
    box_x = (width - box_w) // 2
    box_y = (height - box_h) // 2

    # panel first
    pygame.draw.rect(win, GREY, (box_x, box_y, box_w, box_h))

    # input area and its text
    pygame.draw.rect(win, WHITE, input_rect)
    win.blit(text_surface, (input_rect.x + 5, input_rect.y + 5))

    



    mouse_pos = pygame.mouse.get_pos()
    color_done = RED if done_btn_rect.collidepoint(mouse_pos) else GREEN
    color_paste = RED if paste_btn_rect.collidepoint(mouse_pos) else GREEN
    pygame.draw.rect(win, color_paste, paste_btn_rect, border_radius=12)
    pygame.draw.rect(win, color_done, done_btn_rect, border_radius=12)
    btn_font = pygame.font.SysFont("Arial", 14, bold=True)
    btn_text = btn_font.render("   Click to paste your matrix!\n(0=path, 1=wall, 2=start, 3=end)", True, WHITE)
    btn_text_done = btn_font.render("Done", True, WHITE)
    win.blit(btn_text, btn_text.get_rect(center=paste_btn_rect.center))
    win.blit(btn_text_done, btn_text_done.get_rect(center=done_btn_rect.center))

    pygame.display.update()


# we want to see the text nicely displayed on our page
def wrap_text(s: str) -> str:
    s = s.replace("\r", "").strip("\x00")
    wrapped = []
    for line in s.split("\n"):
        while len(line) > 90:
            wrapped.append(line[:90])
            line = line[90:]
        wrapped.append(line)
    return "\n".join(wrapped)

def start_load_window(win):
    # clipboard
    pygame.scrap.init()
    
    textinput = pygame_textinput.TextInputVisualizer(font_color=BLACK, cursor_color=BLACK)
    
    w, h = win.get_width(), win.get_height()
    box_center_x = w // 2
    box_center_y = h // 2
    
    # input box
    input_rect = pygame.Rect(10, 150, w - 200, h)
    
    paste_btn_rect = pygame.Rect(10, 10, 300, 60)

    done_btn_rect = pygame.Rect(w - 260, 10, 250, 60)

    run_load = True

    return_textvalue = ""
    while run_load:
        events = pygame.event.get()
        textinput.update(events)
        return_textvalue = textinput.value
        textinput.value = wrap_text(textinput.value)
        
        draw_for_load_window(win, textinput.surface, input_rect, paste_btn_rect, done_btn_rect)

        for event in events:
            if event.type == pygame.QUIT:
                return return_textvalue
            
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                if paste_btn_rect.collidepoint(event.pos):
                    # we get clipboard content
                    content = pygame.scrap.get(pygame.SCRAP_TEXT)
                    if content:
                        if isinstance(content, bytes):
                            text = content.decode("utf-8", errors="ignore")
                        else:
                            text = str(content)
                        # we want to show the text in the input box so we wrap
                        textinput.value += text
                        return_textvalue += text
                        textinput.value = wrap_text(textinput.value)

                if done_btn_rect.collidepoint(event.pos):
                    return return_textvalue
                    

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return return_textvalue
                if event.key == pygame.K_RETURN:
                    return return_textvalue
  
    return return_textvalue


def parse_and_load_matrix(matrix_text, width):
    if not matrix_text: 
        return None, None, None, None, "Load operation cancelled."
    lines = matrix_text.strip().split('\n')
    rows = len(lines)
    if not (10 <= rows <= 60):
        return None, None, None, None, "Invalid matrix."
    parsed_matrix = []
    start_count = 0
    end_count = 0
    for r, line in enumerate(lines):
        cleaned_line = line.strip()
        # regex to match only 0,1,2,3 separated by spaces
        if not re.fullmatch(r"^[0-3](\s[0-3])*$", cleaned_line):
            if cleaned_line == "":
                 return None, None, None, None, f"Empty line found in matrix."
            return None, None, None, None, f"Invalid characters in row {r+1}."
        cols = cleaned_line.split(' ')
        if len(cols) != rows:
            return None, None, None, None, "Matrix is not square."
        # we get the number of starts and ends on each row
        start_count += cols.count('2')
        end_count += cols.count('3')
        parsed_matrix.append(cols)
    if start_count != 1:
        return None, None, None, None, "Matrix must have exactly one start (2)."
    if end_count != 1:
        return None, None, None, None, "Matrix must have exactly one end (3)."
    grid_rows_with_border = rows + 2 
    new_grid = make_grid(grid_rows_with_border, width)
    new_start = None
    new_end = None
    for r in range(rows):
        for c in range(rows):
            spot = new_grid[r + 1][c + 1] 
            val = parsed_matrix[r][c]
            if val == '1':
                spot.mark_barrier()
            elif val == '2':
                spot.mark_start()
                new_start = spot
            elif val == '3':
                spot.mark_end()
                new_end = spot
    return new_grid, grid_rows_with_border, new_start, new_end, None