import re
import pygame
import pygame_textinput
import pygame.scrap 
import pyperclip    

import easygui
from grid import make_grid
from graphical_interface.spot import Spot
from graphical_interface.constants import *

# --- ADAUGAT DIN NOU (PENTRU WINDOWS) ---
def get_matrix_input_popup():
    """
    Varianta originală cu EasyGUI pentru Windows/Linux.
    Deschide o fereastră nativă de sistem.
    """
    msg = "Paste your matrix (0=path, 1=wall, 2=start, 3=end):"
    title = "Load Labyrinth Matrix"
    return easygui.codebox(msg, title, "") 
# --- SFÂRȘIT ---

def draw_for_load_window(win, text_input_value, input_rect, paste_btn_rect, done_btn_rect, font_object):
    width, height = win.get_width(), win.get_height()
    win.fill(WHITE)

    box_w, box_h = 600, 300
    box_x = (width - box_w) // 2
    box_y = (height - box_h) // 2

    # panel first
    pygame.draw.rect(win, GREY, (box_x, box_y, box_w, box_h))

    # input area
    pygame.draw.rect(win, WHITE, input_rect)

    # Creăm suprafața de afișare AICI, pe baza textului wrap-uit
    wrapped_text = wrap_text(text_input_value)
    
    # pygame-textinput nu randează multi-linie implicit,
    # așa că o facem noi manual.
    lines = wrapped_text.split('\n')
    y_offset = input_rect.y + 5
    x_pos = input_rect.x + 5
    
    for line in lines:
        text_surface = font_object.render(line, True, BLACK)
        win.blit(text_surface, (x_pos, y_offset))
        y_offset += font_object.get_linesize() # Mutăm la linia următoare


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

# Aceasta este acum STRICT varianta pentru MAC/Custom UI
def start_load_window(win, use_pyperclip=True):
    
    textinput = pygame_textinput.TextInputVisualizer(font_color=BLACK, cursor_color=BLACK)
    
    w, h = win.get_width(), win.get_height()
    
    # input box
    input_rect = pygame.Rect(10, 150, w - 200, h)
    
    paste_btn_rect = pygame.Rect(10, 10, 300, 60)
    done_btn_rect = pygame.Rect(w - 260, 10, 250, 60)

    run_load = True

    while run_load:
        events = pygame.event.get()
        textinput.update(events)
        
        draw_for_load_window(
            win, textinput.value, input_rect, 
            paste_btn_rect, done_btn_rect, 
            textinput.font_object
        )

        for event in events:
            if event.type == pygame.QUIT:
                return textinput.value
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                if paste_btn_rect.collidepoint(event.pos):
                    text_to_paste = ""
                    
                    # Folosim pyperclip (pentru Mac)
                    try:
                        text_to_paste = pyperclip.paste()
                        print("Used pyperclip")
                    except Exception as e:
                        print(f"Error pyperclip: {e}")
                    
                    if text_to_paste:
                        textinput.value += text_to_paste

                if done_btn_rect.collidepoint(event.pos):
                    return textinput.value
                    
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return textinput.value
                if event.key == pygame.K_RETURN:
                    return textinput.value
 
    return textinput.value


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