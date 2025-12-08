import pygame
from ui.constants import *
from ui.button import Button
from config.presets import PRESET_LABYRINTHS


PRESET_CONFIG = {
    10: ["Small & simple", "Left & right", "Dual choice", "Snakey"],
    20: ["Thin walls", "Needles", "Counting", "Classic 1"],
    30: ["Zig Zag", "Rawr", "Meow", "Classic 2"],
    40: ["Classic 3", "Impossible", "67", "SECRET"],
    50: ["Classic 4", "Happiness", "Capitalism", "Classic 5"],
    60: ["Classic 6", "Abstract", "Sorry", "Moonlight"],
    100: ["The Judge"]
}

# Window for selecting preset labyrinths
def draw_preset_window(win, buttons, back_button):
    win.fill(WHITE)

    title_font = pygame.font.SysFont("Arial", 30, bold=True)
    title_text = title_font.render("Choose a premade labyrinth", True, BLACK)
    win.blit(title_text, title_text.get_rect(center=(TOTAL_WIDTH // 2, 50)))

    instr_font = pygame.font.SysFont("Arial", 18)
    instr_text = instr_font.render("Select an option", True, GREY)
    win.blit(instr_text, instr_text.get_rect(center=(TOTAL_WIDTH // 2, 90)))

    for btn in buttons:
        btn.draw(win)

    back_button.draw(win)
    pygame.display.update()


def create_label_button(x, y, size, height):
    btn = Button(
        x=x, y=y, width=80, height=height,
        text=f"{size}x{size}", font=pygame.font.SysFont("Arial", 16, bold=True),
        base_color=WHITE, hovering_color=WHITE
    )
    btn.text_color = BLACK
    return btn


def create_standard_variant_button(x, y, name, matrix_str, font, valid, secret=False):
    base = GREEN if valid else GREY
    hover = BLUE if valid else GREY

    if secret:
        base = (255, 69, 0)
        hover = (255, 99, 71)

    btn = Button(
        x=x, y=y, width=120, height=40,
        text=name, font=font,
        base_color=base, hovering_color=hover
    )
    btn.text_color = WHITE
    btn.matrix_data = matrix_str
    btn.is_selectable = valid
    btn.is_secret = secret
    return btn


def create_judge_button(x, y, matrix_str):
    GOLD = (218, 165, 32)
    HOVER_GOLD = (255, 215, 0)
    valid = len(matrix_str.strip()) > 10

    btn = Button(
        x=x, y=y, width=200, height=50,
        text="The Judge", font=pygame.font.SysFont("Arial", 20, bold=True),
        base_color=GOLD if valid else GREY,
        hovering_color=HOVER_GOLD if valid else GREY
    )
    btn.matrix_data = matrix_str
    btn.is_selectable = valid
    btn.is_secret = False
    return btn


def add_preset_row(buttons, size, variants, names, start_x, y, font):
    # Special 100x100 row
    if size == 100:
        judge_x = (TOTAL_WIDTH - 200) // 2
        buttons.append(create_judge_button(judge_x, y + 20, variants[0]))
        return

    buttons.append(create_label_button(start_x, y, size, 40))

    for idx, matrix_str in enumerate(variants):
        valid = len(matrix_str.strip()) > 10
        name = names[idx] if idx < len(names) else f"Var {idx+1}"
        is_secret = (size == 40 and idx == 3)

        btn_x = start_x + 100 + idx * (120 + 20)
        btn = create_standard_variant_button(
            btn_x, y, name, matrix_str, font, valid, secret=is_secret
        )
        buttons.append(btn)



def start_preset_chooser(win):
    clock = pygame.time.Clock()
    button_font = pygame.font.SysFont("Arial", 14, bold=True)

    start_y = 130
    row_spacing = 60

    sizes = sorted(PRESET_LABYRINTHS.keys())
    buttons = []

    total_row_width = 80 + 4 * (120 + 20)
    start_x = (TOTAL_WIDTH - total_row_width) // 2

    y_offset = 0

    for size in sizes:
        variants = PRESET_LABYRINTHS[size]
        names = PRESET_CONFIG.get(size, [f"Var {i+1}" for i in range(len(variants))])

        row_y = start_y + y_offset
        add_preset_row(buttons, size, variants, names, start_x, row_y, button_font)
        y_offset += row_spacing

    back_btn = Button(
        x=20, y=20, width=100, height=40,
        text="< Back", font=button_font,
        base_color=BUTTON_RED, hovering_color=HOVER_BUTTON_RED
    )

    while True:
        draw_preset_window(win, buttons, back_btn)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return None

            if back_btn.is_clicked(event):
                return None

            if event.type == pygame.MOUSEBUTTONDOWN:
                for btn in buttons:
                    if getattr(btn, "is_selectable", False) and btn.is_clicked(event):
                        return (btn.matrix_data, btn.is_secret)

        clock.tick(60)
