import pygame
from graphical_interface.constants import *
# Avem nevoie de TEXTURE_NAMES din noul manager
from texture_manager import TEXTURE_NAMES, TEXTURE_CATEGORIES

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
        # desenează dreptunghiul butonului
        pygame.draw.rect(win, self.current_color, self.rect, border_radius=12)
        
        # randează și centrează textul
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
        # actualizează textul afișat pe buton
        self.text = new_text

# --- Clasă Nouă pentru Butoanele cu Texturi ---

class ImageButton(Button):
    def __init__(self, x, y, width, height, base_color, hovering_color, image, category, index):
        """
        Un buton care afișează o imagine în loc de text.
        'image' este imaginea originală (nescalată).
        """
        # Folosim un text gol pentru clasa părinte
        super().__init__(x, y, width, height, "", None, base_color, hovering_color)
        
        self.image = image
        # Scalăm imaginea pentru a se potrivi butonului, lăsând un mic chenar
        self.scaled_image = pygame.transform.scale(self.image, (width - 8, height - 8))
        
        # Stocăm informațiile necesare pentru a ști ce textură setăm
        self.category = category
        self.index = index
        
        # Stare pentru a arăta dacă e selectat
        self.is_selected = False

    def draw(self, win):
        """
        Desenează butonul. Afișează un chenar evidențiat dacă este selectat.
        """
        # Culoarea de bază
        pygame.draw.rect(win, self.current_color, self.rect, border_radius=8)
        
        # Chenar de selecție
        if self.is_selected:
            pygame.draw.rect(win, ORANGE, self.rect, 4, border_radius=8) # Chenar portocaliu de 4px

        # Centrarea imaginii
        img_rect = self.scaled_image.get_rect(center=self.rect.center)
        win.blit(self.scaled_image, img_rect)

    def check_for_hover(self, mouse_pos, active_index):
        """
        Suprascriem check_for_hover pentru a gestiona și starea de selecție.
        """
        super().check_for_hover(mouse_pos)
        
        # Verificăm dacă acest buton corespunde indexului activ
        if self.index == active_index:
            self.is_selected = True
        else:
            self.is_selected = False

    # is_clicked este moștenit și funcționează perfect

# --- SFÂRȘIT CLASĂ NOUĂ ---


# --- MODIFICARE ---
# Am scos '@staticmethod' și am de-indentat funcția.
# Acum este o funcție normală în acest fișier, nu o metodă a unei clase.
def create_buttons(button_font, small_font, texture_manager):
    """
    Pasăm 'texture_manager' pentru a crea butoanele-imagine.
    """
    
    all_buttons = []
    
    # --- MODIFICARE: Butoanele din Dreapta (Reorganizate) ---
    
    # Folosim o logică mai robustă pentru poziționare
    RIGHT_MENU_START_X = GRID_X_OFFSET + GRID_WIDTH
    RIGHT_MENU_WIDTH = SIDE_MENU_WIDTH # 280px
    
    current_y = 20 # Începem de mai sus
    
    # --- Butoane principale (Lățime 200px) ---
    btn_width_large = 200
    btn_x_large = RIGHT_MENU_START_X + (RIGHT_MENU_WIDTH - btn_width_large) // 2
    
    find_path_button = Button(
        x=btn_x_large, y=current_y, width=btn_width_large, height=50,
        text="Find Path", font=button_font,
        base_color=GREEN, hovering_color=BLUE)
    all_buttons.append(find_path_button)
    current_y += 70 # 50 înălțime + 20 gap (era 60)
    
    race_mode_button = Button(
        x=btn_x_large, y=current_y, width=btn_width_large, height=50,
        text="Race Mode: OFF", font=button_font,
        base_color=GREEN, hovering_color=BLUE)
    all_buttons.append(race_mode_button)
    current_y += 70 # (era 60)
    
    toggle_grid_button = Button(
        x=btn_x_large, y=current_y, width=btn_width_large, height=50,
        text="Toggle Grid", font=button_font,
        base_color=PURPLE, hovering_color=GREEN)
    all_buttons.append(toggle_grid_button)
    current_y += 70 # (era 60)
    
    toggle_mode_button = Button(
        x=btn_x_large, y=current_y, width=btn_width_large, height=50,
        text="Switch to Eraser", font=button_font,
        base_color=BUTTON_RED, hovering_color=HOVER_BUTTON_RED)
    all_buttons.append(toggle_mode_button)
    current_y += 70 # Am terminat cu butoanele principale (era 60)
    
    
    # --- Butoanele +/- și Textul Grilei ---
    # Textul va veni primul
    current_y += 30 # Spațiu pentru text (rămâne 30)
    
    # Acum butoanele +/-
    btn_width_small = 50
    gap_between_small = 100 # Spațiu mare între ele
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
    current_y += 70 # 50 înălțime + 20 gap (rămâne 70)
    

    # --- Butoane Load/Save (2 pe rând) ---
    padding = 10
    btn_width_medium = (RIGHT_MENU_WIDTH - (padding * 3)) // 2 # ~125px
    btn_x_load = RIGHT_MENU_START_X + padding
    btn_x_save = btn_x_load + btn_width_medium + padding
    
    load_matrix_button = Button(
        x=btn_x_load, y=current_y, width=btn_width_medium, height=50, 
        text="Load", font=button_font, 
        base_color=BLUE, hovering_color=GREEN
    )
    all_buttons.append(load_matrix_button)
    
    save_matrix_button = Button(
        x=btn_x_save, y=current_y, width=btn_width_medium, height=50, 
        text="Save", font=button_font, 
        base_color=BLUE, hovering_color=GREEN
    )
    all_buttons.append(save_matrix_button)
    current_y += 70 # 50 înălțime + 20 gap (era 60)
    
    
    # --- Butoane Algoritmi (3 pe rând) ---
    btn_width_algo = (RIGHT_MENU_WIDTH - (padding * 4)) // 3 # ~80px
    algo_font = pygame.font.SysFont("Arial", 18, bold=True) # Font mai mic
    
    btn_x_bfs = RIGHT_MENU_START_X + padding
    btn_x_dfs = btn_x_bfs + btn_width_algo + padding
    btn_x_gbfs = btn_x_dfs + btn_width_algo + padding
    
    bfs_button = Button(
        x=btn_x_bfs, y=current_y, width=btn_width_algo, height=50,
        text="BFS", font=algo_font, # Text mai scurt
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
        text="GBFS", font=algo_font, # Text mai scurt
        base_color=PURPLE, hovering_color=GREEN
    )
    all_buttons.append(gbfs_button)
    
    # --- SFÂRȘIT MODIFICARE ---


    # --- Butoanele din Stânga ---
    
    # 1. Butoanele pentru Texturi
    texture_btn_width = 60
    texture_btn_height = 60 # Le facem pătrate
    h_padding = (SIDE_MENU_WIDTH - (3 * texture_btn_width)) // 4 # Pading orizontal dinamic
    
    start_y = 20
    y_gap = texture_btn_height + 15
    
    x_positions = [
        h_padding,
        h_padding * 2 + texture_btn_width,
        h_padding * 3 + (2 * texture_btn_width)
    ]
    
    # Font mic pentru etichetele texturilor
    label_font = pygame.font.SysFont("Arial", 16, bold=True)
    
    current_y = start_y

    for category in TEXTURE_CATEGORIES:
        # Adăugăm eticheta pentru rând
        label_text = TEXTURE_NAMES.get(category, category.capitalize())
        label_surface = label_font.render(label_text, True, BLACK)
        # Salvăm eticheta ca un buton "fals" (doar pentru desenare)
        # O facem un buton normal, dar nu o adăugăm la logica de click
        label_btn = Button(
            x=0, y=current_y, width=SIDE_MENU_WIDTH, height=20,
            text=label_text, font=label_font,
            base_color=GREY, hovering_color=GREY
        )
        # Suprascriem textul și culoarea
        label_btn.text_color = BLACK
        all_buttons.append(label_btn)
        
        current_y += 25 # Spațiu pentru etichetă

        # Creăm cele 3 butoane-imagine
        for i in range(3):
            try:
                img = texture_manager.get_original_texture(category, i)
                img_btn = ImageButton(
                    x=x_positions[i], y=current_y, 
                    width=texture_btn_width, height=texture_btn_height,
                    base_color=GREY, hovering_color=BLUE,
                    image=img,
                    category=category,
                    index=i
                )
                all_buttons.append(img_btn)
            except IndexError:
                # Se întâmplă dacă o textură lipsește
                print(f"Nu s-a putut crea butonul pentru {category}_{i+1}")
                
        current_y += y_gap # Trecem la următorul rând de texturi

    # 2. Butoanele de Acțiune (mutate mai jos)
    # --- MODIFICARE: Am șters butoanele de acțiune de aici ---
    # action_btn_width = 200
    # ...
    # all_buttons.extend([
    #     load_matrix_button, save_matrix_button,
    #     bfs_button, dfs_button, gbfs_button
    # ])
    # --- SFÂRȘIT MODIFICARE ---

    return all_buttons
# --- SFÂRȘIT MODIFICARE ---