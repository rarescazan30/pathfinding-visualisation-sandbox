import pygame
from .constants import *

class Spot:
    def __init__(self, row, col, width, total_rows):
        self.row = row
        self.col = col
        self.width = width
        self.x = col * width
        self.y = row * width
        self.colour = WHITE # Culoarea este încă folosită pentru logică!
        self.neighbors = []
        self.total_rows = total_rows
        self.is_start = False
        self.is_end = False
        self.is_wall = False
        self.is_user_path = False # for race mode!
        self.is_visited = False # Folosim asta pentru 'margin_of_search'
        self.parent = None

    def get_pos(self):
        return self.row, self.col
    
    def is_closed(self):
        # Logica rămâne bazată pe culoare
        return self.colour == RED
    
    def is_open(self):
        return self.colour == GREEN

    def is_barrier(self):
        return self.is_wall
    
    def is_start_node(self): # Am redenumit-o pentru a evita conflictul
        return self.is_start
    
    def is_end_node(self): # Am redenumit-o pentru a evita conflictul
        return self.is_end

    def clear_visualization(self):
        if not self.is_start and not self.is_end and not self.is_wall:
            self.colour = WHITE
            self.parent = None
            self.is_visited = False
            self.is_user_path = False

    def mark_start(self):
        self.colour = ORANGE
        self.is_start = True
        self.is_wall = False

    def mark_closed(self, colour):
        if self.is_user_path:
            return
        self.colour = colour
        self.is_visited = True

    def mark_open(self):
        if self.is_user_path:
            return
        self.colour = GREEN

    def mark_barrier(self):
        self.colour = BLACK
        self.is_wall = True

    def mark_end(self):
        self.colour = TURQUOISE
        self.is_end = True
        self.is_wall = False

    def mark_path(self):
        self.colour = PURPLE
        self.is_visited = True # O cale este și vizitată
        
    def mark_user_path(self):
        # Only used when USER draws in Race Mode
        if self.is_start or self.is_end:
            return
        self.colour = PURPLE
        self.is_user_path = True
        self.is_wall = False
        self.is_visited = True
    
    def reset(self):
        self.colour = WHITE
        self.is_visited = False
        self.parent = None
        self.is_wall = False
        self.is_end = False
        self.is_start = False
        self.is_user_path = False

    def draw(self, win, padding_x, padding_y, texture_manager):
        # Am adăugat texture_manager ca parametru
        
        final_x = self.x + GRID_X_OFFSET + padding_x
        final_y = self.y + GRID_Y_OFFSET + padding_y
        
        # --- Logică Nouă pentru Texturi ---
        
        # 1. Stabilim ce categorie de textură să folosim
        # Categoriile tale: 'start', 'end', 'path', 'background', 'search', 'margin_of_search', 'wall'
        
        category = 'background' # Default (fundal gol)
        
        if self.is_start:
            category = 'start'
        elif self.is_end:
            category = 'end'
        elif self.is_wall:
            category = 'wall'
        elif self.colour == PURPLE: # Calea finală
            category = 'path'
        elif self.colour == GREEN: # Noduri deschise (în curs de căutare)
            category = 'search'
        elif self.is_visited: # Noduri închise (deja vizitate)
            # Ne asigurăm că nu e start, end, sau path, care sunt și ele "visited"
            category = 'margin_of_search'
            
        # Cazuri speciale pentru a nu suprascrie start/end/path
        if self.is_start:
            category = 'start'
        elif self.is_end:
            category = 'end'
        elif self.colour == PURPLE:
            category = 'path'


        # 2. Obținem textura corectă (deja scalată) de la manager
        try:
            texture_to_draw = texture_manager.get_active_texture(category)
        except Exception as e:
            # Fallback în caz de eroare (de ex. la prima randare)
            print(f"Eroare la get_active_texture pentru {category}: {e}")
            pygame.draw.rect(win, self.colour, (final_x, final_y, self.width, self.width))
            return

        # 3. Desenăm textura
        win.blit(texture_to_draw, (final_x, final_y))
        
        # --- Sfârșit Logică Nouă ---
        
        # Am înlocuit linia de mai jos:
        # pygame.draw.rect(win, self.colour, (final_x, final_y, self.width, self.width))