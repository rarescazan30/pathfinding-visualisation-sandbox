import pygame
from graphical_interface.constants import *
from graphical_interface.button import Button
from presets import PRESET_LABYRINTHS

# --- MODIFICARE: Mapare Nume ---
PRESET_CONFIG = {
    10: ["Small & simple", "Left & right", "Dual choice", "Snakey"],
    20: ["Thin walls", "Needles", "Counting", "Classic 1"],
    30: ["Zig Zag", "Rawr", "Meow", "Classic 2"],
    40: ["Classic 3", "Impossible", "67", "SECRET"],
    50: ["Classic 4", "Happiness", "Capitalism", "Classic 5"],
    60: ["Classic 6", "Abstract", "Sorry", "Moonlight"],
    100: ["The Judge"]
}
# --- SFÂRȘIT MODIFICARE ---

def draw_preset_window(win, buttons, back_button):
    win.fill(WHITE)
    
    title_font = pygame.font.SysFont("Arial", 30, bold=True)
    title_text = title_font.render("Alege un Labirint Predefinit", True, BLACK)
    title_rect = title_text.get_rect(center=(TOTAL_WIDTH // 2, 50))
    win.blit(title_text, title_rect)
    
    instr_font = pygame.font.SysFont("Arial", 18)
    instr_text = instr_font.render("Selectează o dimensiune și o variantă:", True, GREY)
    instr_rect = instr_text.get_rect(center=(TOTAL_WIDTH // 2, 90))
    win.blit(instr_text, instr_rect)

    for btn in buttons:
        btn.draw(win)
        
    back_button.draw(win)

    pygame.display.update()

def start_preset_chooser(win):
    """
    Deschide bucla pentru fereastra de selecție.
    Returnează un tuplu (matrix_str, is_secret_preset) sau None.
    """
    run_chooser = True
    clock = pygame.time.Clock()
    
    preset_buttons = []
    button_font = pygame.font.SysFont("Arial", 14, bold=True) # Font puțin mai mic pentru nume lungi
    
    start_y = 130
    btn_width = 120
    btn_height = 40
    margin_x = 20
    
    # Centrare orizontală
    total_row_width = 80 + 4 * (btn_width + margin_x)
    start_x = (TOTAL_WIDTH - total_row_width) // 2

    sorted_sizes = sorted(PRESET_LABYRINTHS.keys())
    
    current_y_offset = 0

    for i, size in enumerate(sorted_sizes):
        variants = PRESET_LABYRINTHS[size]
        names = PRESET_CONFIG.get(size, [f"Var {k+1}" for k in range(len(variants))])
        
        row_y = start_y + current_y_offset
        
        # --- MODIFICARE: Tratament Special pentru 100x100 (The Judge) ---
        if size == 100:
            # Nu desenăm eticheta de rând, doar un buton mare centrat jos
            # Mai lăsăm un pic de spațiu
            row_y += 20 
            
            judge_btn_width = 200
            judge_x = (TOTAL_WIDTH - judge_btn_width) // 2
            
            matrix_str = variants[0]
            is_valid = len(matrix_str.strip()) > 10
            
            # Culoare Auriu (Gold)
            GOLD_COLOR = (218, 165, 32)
            HOVER_GOLD = (255, 215, 0)
            
            color = GOLD_COLOR if is_valid else GREY
            hover = HOVER_GOLD if is_valid else GREY
            
            p_btn = Button(
                x=judge_x, y=row_y, width=judge_btn_width, height=50,
                text="The Judge", font=pygame.font.SysFont("Arial", 20, bold=True),
                base_color=color, hovering_color=hover
            )
            p_btn.matrix_data = matrix_str
            p_btn.is_selectable = is_valid
            p_btn.is_secret = False # The Judge nu e SECRET-ul de github, e doar boss level
            
            preset_buttons.append(p_btn)
            continue # Sărim peste logica standard pentru 100
        # --- SFÂRȘIT MODIFICARE ---

        # Eticheta rândului standard
        label_btn = Button(
            x=start_x, y=row_y, width=80, height=btn_height,
            text=f"{size}x{size}", font=pygame.font.SysFont("Arial", 16, bold=True),
            base_color=WHITE, hovering_color=WHITE
        )
        label_btn.text_color = BLACK 
        preset_buttons.append(label_btn) 
        
        for v_idx, matrix_str in enumerate(variants):
            btn_x = start_x + 100 + v_idx * (btn_width + margin_x)
            
            is_valid = len(matrix_str.strip()) > 10
            
            # --- MODIFICARE: Logică pentru culori și nume ---
            btn_name = names[v_idx] if v_idx < len(names) else f"Var {v_idx+1}"
            
            # Default colors
            color = GREEN if is_valid else GREY
            hover = BLUE if is_valid else GREY
            text_col = WHITE
            is_secret = False

            # SECRET button (40x40, varianta 4 -> index 3)
            if size == 40 and v_idx == 3:
                color = (255, 69, 0) # Red-Orange (Striking)
                hover = (255, 99, 71) # Tomato
                is_secret = True # Acesta declanșează mesajul
            
            p_btn = Button(
                x=btn_x, y=row_y, width=btn_width, height=btn_height,
                text=btn_name, font=button_font,
                base_color=color, hovering_color=hover
            )
            p_btn.text_color = text_col
            p_btn.matrix_data = matrix_str 
            p_btn.is_selectable = is_valid
            p_btn.is_secret = is_secret
            
            preset_buttons.append(p_btn)
            # --- SFÂRȘIT MODIFICARE ---

        current_y_offset += (btn_height + 20) # Spațiere verticală

    back_btn = Button(
        x=20, y=20, width=100, height=40,
        text="< Back", font=button_font,
        base_color=BUTTON_RED, hovering_color=HOVER_BUTTON_RED
    )

    while run_chooser:
        draw_preset_window(win, preset_buttons, back_btn)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return None
            
            if back_btn.is_clicked(event):
                return None
                
            if event.type == pygame.MOUSEBUTTONDOWN:
                for btn in preset_buttons:
                    if hasattr(btn, 'is_selectable') and btn.is_selectable:
                        if btn.is_clicked(event):
                            # Returnăm tuplul (data, is_secret)
                            return (btn.matrix_data, getattr(btn, 'is_secret', False))
                            
        clock.tick(60)
        
    return None
