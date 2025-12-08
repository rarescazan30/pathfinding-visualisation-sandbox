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
        if self.rect.collidepoint(mouse_pos):
            self.current_color = self.hovering_color
        else:
            self.current_color = self.base_color

    def is_clicked(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(event.pos):
            return True
        return False
    
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
        if self.index == active_index:
            self.is_selected = True
        else:
            self.is_selected = False

class RaceTimerButton(Button):
    def __init__(self, x, y, width, height):
        super().__init__(x, y, width, height, "", None, base_color=GREY, hovering_color=GREY)
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
    
    RIGHT_MENU_START_X = GRID_X_OFFSET + GRID_WIDTH
    RIGHT_MENU_WIDTH = SIDE_MENU_WIDTH
    current_y = 20
    
    # --- Standard Buttons ---
    btn_width_large = 200
    btn_x_large = RIGHT_MENU_START_X + (RIGHT_MENU_WIDTH - btn_width_large) // 2
    
    find_path_button = Button(
        x=btn_x_large, y=current_y, width=btn_width_large, height=50,
        text="Find Path", font=button_font,
        base_color=GREEN, hovering_color=BLUE)
    all_buttons.append(find_path_button)
    current_y += 70 
    
    race_mode_button = Button(
        x=btn_x_large, y=current_y, width=btn_width_large, height=50,
        text="Race Mode: OFF", font=button_font,
        base_color=GREEN, hovering_color=BLUE)
    all_buttons.append(race_mode_button)
    current_y += 70
    
    toggle_grid_button = Button(
        x=btn_x_large, y=current_y, width=btn_width_large, height=50,
        text="Toggle Grid", font=button_font,
        base_color=PURPLE, hovering_color=GREEN)
    all_buttons.append(toggle_grid_button)
    current_y += 70
    
    toggle_mode_button = Button(
        x=btn_x_large, y=current_y, width=btn_width_large, height=50,
        text="Switch to Eraser", font=button_font,
        base_color=BUTTON_RED, hovering_color=HOVER_BUTTON_RED)
    all_buttons.append(toggle_mode_button)
    current_y += 70 
    
    # --- +/- Buttons ---
    current_y += 30 
    
    btn_width_small = 50
    gap_between_small = 100 
    total_width_small = btn_width_small * 2 + gap_between_small
    btn_x_decrease = RIGHT_MENU_START_X + (RIGHT_MENU_WIDTH - total_width_small) // 2
    btn_x_increase = btn_x_decrease + btn_width_small + gap_between_small
    
    decrease_button = Button(
        x=btn_x_decrease, y=current_y, width=btn_width_small, height=50,
        text="-", font=small_font,
        base_color=GREY, hovering_color=(190, 190, 190))
    all_buttons.append(decrease_button)
    
    increase_button = Button(
        x=btn_x_increase, y=current_y, width=btn_width_small, height=50,
        text="+", font=small_font,
        base_color=GREY, hovering_color=(190, 190, 190))
    all_buttons.append(increase_button)
    current_y += 70 

     # --- Presets Button ---
    btn_width_large = 200 
    btn_x_large = RIGHT_MENU_START_X + (RIGHT_MENU_WIDTH - btn_width_large) // 2
    
    presets_button = Button(
        x=btn_x_large, y=current_y, width=btn_width_large, height=50,
        text="Presets", font=button_font,
        base_color=ORANGE, hovering_color=YELLOW 
    )
    presets_button.text_color = BLACK 
    all_buttons.append(presets_button)
    
    current_y += 70
    
    # --- Load/Save Buttons ---
    padding = 10
    btn_width_load = (RIGHT_MENU_WIDTH - (padding * 3)) // 2 
    btn_x_load_mac = RIGHT_MENU_START_X + padding
    btn_x_load_win = btn_x_load_mac + btn_width_load + padding
    
    load_font = pygame.font.SysFont("Arial", 20, bold=True)

    load_mac_button = Button(
        x=btn_x_load_mac, y=current_y, width=btn_width_load, height=50, 
        text="Load (Mac)", font=load_font, 
        base_color=BLUE, hovering_color=GREEN
    )
    all_buttons.append(load_mac_button)
    
    load_win_button = Button(
        x=btn_x_load_win, y=current_y, width=btn_width_load, height=50, 
        text="Load (Win)", font=load_font, 
        base_color=BLUE, hovering_color=GREEN
    )
    all_buttons.append(load_win_button)
    
    current_y += 60 
    
    save_matrix_button = Button(
        x=btn_x_large, y=current_y, width=btn_width_large, height=50, 
        text="Save", font=button_font, 
        base_color=BLUE, hovering_color=GREEN
    )
    all_buttons.append(save_matrix_button)
    current_y += 70 
    
    # --- Algo Buttons (4 per row) ---
    btn_width_algo = (RIGHT_MENU_WIDTH - (padding * 5)) // 4 
    algo_font = pygame.font.SysFont("Arial", 16, bold=True) 
    
    btn_x_bfs = RIGHT_MENU_START_X + padding
    btn_x_dfs = btn_x_bfs + btn_width_algo + padding
    btn_x_gbfs = btn_x_dfs + btn_width_algo + padding
    btn_x_astar = btn_x_gbfs + btn_width_algo + padding
    
    bfs_button = Button(
        x=btn_x_bfs, y=current_y, width=btn_width_algo, height=50,
        text="BFS", font=algo_font, 
        base_color=PURPLE, hovering_color=GREEN
    )
    all_buttons.append(bfs_button)

    dfs_button = Button(
        x=btn_x_dfs, y=current_y, width=btn_width_algo, height=50,
        text="DFS", font=algo_font,
        base_color=PURPLE, hovering_color=GREEN
    )
    all_buttons.append(dfs_button)

    gbfs_button = Button(
        x=btn_x_gbfs, y=current_y, width=btn_width_algo, height=50,
        text="GBFS", font=algo_font, 
        base_color=PURPLE, hovering_color=GREEN
    )
    all_buttons.append(gbfs_button)

    astar_button = Button(
        x=btn_x_astar, y=current_y, width=btn_width_algo, height=50,
        text="A*", font=algo_font, 
        base_color=PURPLE, hovering_color=GREEN
    )
    all_buttons.append(astar_button)
    
    # --- Texture Buttons (Left Menu) ---
    texture_btn_width = 60
    texture_btn_height = 60 
    h_padding = (SIDE_MENU_WIDTH - (3 * texture_btn_width)) // 4 
    
    start_y = 20
    y_gap = texture_btn_height + 15
    
    x_positions = [
        h_padding,
        h_padding * 2 + texture_btn_width,
        h_padding * 3 + (2 * texture_btn_width)
    ]
    
    label_font = pygame.font.SysFont("Arial", 16, bold=True)
    
    current_y_tex = start_y

    for category in TEXTURE_CATEGORIES:
        label_text = TEXTURE_NAMES.get(category, category.capitalize())
        label_btn = Button(
            x=0, y=current_y_tex, width=SIDE_MENU_WIDTH, height=20,
            text=label_text, font=label_font,
            base_color=GREY, hovering_color=GREY
        )
        label_btn.text_color = BLACK
        all_buttons.append(label_btn)
        
        current_y_tex += 25 

        for i in range(3):
            try:
                img = texture_manager.get_original_texture(category, i)
                img_btn = ImageButton(
                    x=x_positions[i], y=current_y_tex, 
                    width=texture_btn_width, height=texture_btn_height,
                    base_color=GREY, hovering_color=BLUE,
                    image=img,
                    category=category,
                    index=i
                )
                all_buttons.append(img_btn)
            except IndexError:
                print(f"Nu s-a putut crea butonul pentru {category}_{i+1}")
                
        current_y_tex += y_gap 

    timer_x = RIGHT_MENU_START_X + 10
    timer_y = 650
    timer_width = RIGHT_MENU_WIDTH - 20
    timer_height = 40
    
    race_timer_button = RaceTimerButton(timer_x, timer_y, timer_width, timer_height)

    return all_buttons, race_timer_button