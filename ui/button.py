import pygame
from ui.constants import *
from managers.texture_manager import TEXTURE_NAMES, TEXTURE_CATEGORIES

class Button:
    def __init__(self, x, y, width, height, text, font, base_color, hovering_color):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.font = font
        self.base_color = base_color
        self.hovering_color = hovering_color
        self.current_color = base_color
        self.text_color = (255, 255, 255)

    def draw(self, win):
        pygame.draw.rect(win, self.current_color, self.rect, border_radius=12)
        text_surface = self.font.render(self.text, True, self.text_color)
        text_rect = text_surface.get_rect(center=self.rect.center)
        win.blit(text_surface, text_rect)

    def check_for_hover(self, mouse_pos):
        self.current_color = self.hovering_color if self.rect.collidepoint(mouse_pos) else self.base_color

    def is_clicked(self, event):
        return event.type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(event.pos)

    def update_text(self, new_text):
        self.text = new_text


class ImageButton(Button):
    def __init__(self, x, y, width, height, base_color, hovering_color, image, category, index):
        super().__init__(x, y, width, height, "", None, base_color, hovering_color)
        self.image = image
        self.scaled_image = pygame.transform.scale(self.image, (width - 8, height - 8))
        self.category = category
        self.index = index
        self.is_selected = False

    def draw(self, win):
        pygame.draw.rect(win, self.current_color, self.rect, border_radius=8)
        if self.is_selected:
            pygame.draw.rect(win, ORANGE, self.rect, 4, border_radius=8)
        img_rect = self.scaled_image.get_rect(center=self.rect.center)
        win.blit(self.scaled_image, img_rect)

    def check_for_hover(self, mouse_pos, active_index):
        super().check_for_hover(mouse_pos)
        self.is_selected = self.index == active_index


class RaceTimerButton(Button):
    def __init__(self, x, y, width, height):
        super().__init__(x, y, width, height, "", None, GREY, GREY)
        self.text = "Time: 0.0s"
        self.text_color = BLACK
        self.font = pygame.font.SysFont("Arial", 28, bold=True)
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def update_time(self, elapsed_ms: int):
        seconds = elapsed_ms // 1000
        tenths = (elapsed_ms % 1000) // 100
        self.text = f"Time: {seconds}.{tenths}s"

    def draw(self, win):
        label_surface = self.font.render(self.text, True, self.text_color)
        label_rect = label_surface.get_rect(center=self.rect.center)
        win.blit(label_surface, label_rect)


def create_buttons(button_font, small_font, texture_manager):
    all_buttons = []

    # Calculate menu positions
    RIGHT_MENU_START_X = GRID_X_OFFSET + GRID_WIDTH
    RIGHT_MENU_WIDTH = SIDE_MENU_WIDTH
    current_y = 20

    btn_width_large = 200
    btn_x_large = RIGHT_MENU_START_X + (RIGHT_MENU_WIDTH - btn_width_large) // 2

    # Main action buttons
    find_path_button = Button(btn_x_large, current_y, btn_width_large, 50, "Find Path", button_font, GREEN, BLUE)
    all_buttons.append(find_path_button)
    current_y += 70

    race_mode_button = Button(btn_x_large, current_y, btn_width_large, 50, "Race Mode: OFF", button_font, GREEN, BLUE)
    all_buttons.append(race_mode_button)
    current_y += 70

    toggle_grid_button = Button(btn_x_large, current_y, btn_width_large, 50, "Toggle Grid", button_font, PURPLE, GREEN)
    all_buttons.append(toggle_grid_button)
    current_y += 70

    toggle_mode_button = Button(btn_x_large, current_y, btn_width_large, 50, "Switch to Eraser", button_font, BUTTON_RED, HOVER_BUTTON_RED)
    all_buttons.append(toggle_mode_button)
    current_y += 70

    # +/- buttons
    current_y += 30
    btn_width_small = 50
    gap_between_small = 100
    total_width_small = btn_width_small * 2 + gap_between_small
    btn_x_decrease = RIGHT_MENU_START_X + (RIGHT_MENU_WIDTH - total_width_small) // 2
    btn_x_increase = btn_x_decrease + btn_width_small + gap_between_small

    decrease_button = Button(btn_x_decrease, current_y, btn_width_small, 50, "-", small_font, GREY, (190, 190, 190))
    all_buttons.append(decrease_button)
    increase_button = Button(btn_x_increase, current_y, btn_width_small, 50, "+", small_font, GREY, (190, 190, 190))
    all_buttons.append(increase_button)
    current_y += 70

    # Presets button
    presets_button = Button(btn_x_large, current_y, btn_width_large, 50, "Presets", button_font, ORANGE, YELLOW)
    presets_button.text_color = BLACK
    all_buttons.append(presets_button)
    current_y += 70

    # Load/Save buttons
    padding = 10
    btn_width_load = (RIGHT_MENU_WIDTH - padding * 3) // 2
    btn_x_load_mac = RIGHT_MENU_START_X + padding
    btn_x_load_win = btn_x_load_mac + btn_width_load + padding
    load_font = pygame.font.SysFont("Arial", 20, bold=True)

    load_mac_button = Button(btn_x_load_mac, current_y, btn_width_load, 50, "Load (Mac)", load_font, BLUE, GREEN)
    all_buttons.append(load_mac_button)
    load_win_button = Button(btn_x_load_win, current_y, btn_width_load, 50, "Load (Win)", load_font, BLUE, GREEN)
    all_buttons.append(load_win_button)
    current_y += 60

    save_matrix_button = Button(btn_x_large, current_y, btn_width_large, 50, "Save", button_font, BLUE, GREEN)
    all_buttons.append(save_matrix_button)
    current_y += 70

    # Algorithm buttons (4 per row)
    btn_width_algo = (RIGHT_MENU_WIDTH - padding * 5) // 4
    algo_font = pygame.font.SysFont("Arial", 16, bold=True)

    x_positions_algo = [RIGHT_MENU_START_X + padding + i * (btn_width_algo + padding) for i in range(4)]
    algo_texts = ["BFS", "DFS", "GBFS", "A*"]

    for x_pos, text in zip(x_positions_algo, algo_texts):
        all_buttons.append(Button(x_pos, current_y, btn_width_algo, 50, text, algo_font, PURPLE, GREEN))

    # Texture buttons (Left Menu)
    texture_btn_width = 60
    texture_btn_height = 60
    h_padding = (SIDE_MENU_WIDTH - 3 * texture_btn_width) // 4
    start_y = 20
    y_gap = texture_btn_height + 15
    x_positions_tex = [h_padding, h_padding * 2 + texture_btn_width, h_padding * 3 + 2 * texture_btn_width]
    label_font = pygame.font.SysFont("Arial", 16, bold=True)
    current_y_tex = start_y

    for category in TEXTURE_CATEGORIES:
        label_text = TEXTURE_NAMES.get(category, category.capitalize())
        label_btn = Button(0, current_y_tex, SIDE_MENU_WIDTH, 20, label_text, label_font, GREY, GREY)
        label_btn.text_color = BLACK
        all_buttons.append(label_btn)
        current_y_tex += 25

        for i in range(3):
            try:
                img = texture_manager.get_original_texture(category, i)
                img_btn = ImageButton(x_positions_tex[i], current_y_tex, texture_btn_width, texture_btn_height, GREY, BLUE, img, category, i)
                all_buttons.append(img_btn)
            except IndexError:
                pass  # ignore missing texture

        current_y_tex += y_gap

    # Race timer button
    timer_x = RIGHT_MENU_START_X + 10
    timer_y = 650
    timer_width = RIGHT_MENU_WIDTH - 20
    timer_height = 40
    race_timer_button = RaceTimerButton(timer_x, timer_y, timer_width, timer_height)

    return all_buttons, race_timer_button
