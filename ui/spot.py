import pygame
from .constants import *

class Spot:
    def __init__(self, row, col, width, total_rows):
        self.row = row
        self.col = col
        self.width = width
        self.x = col * width
        self.y = row * width
        self.colour = WHITE
        self.neighbors = []
        self.total_rows = total_rows

        self.is_start = False
        self.is_end = False
        self.is_wall = False
        self.is_user_path = False
        self.is_visited = False
        self.parent = None

    def get_pos(self):
        return self.row, self.col
    
    def is_closed(self):
        return self.colour == RED
    
    def is_open(self):
        return self.colour == GREEN

    def is_barrier(self):
        return self.is_wall
    
    def is_start_node(self):
        return self.is_start
    
    def is_end_node(self):
        return self.is_end

    def clear_visualization(self):
        if not (self.is_start or self.is_end or self.is_wall):
            self.colour = WHITE
            self.parent = None
            self.is_visited = False
            self.is_user_path = False

    def mark_start(self):
        self.colour = ORANGE
        self.is_start = True
        self.is_wall = False

    def mark_closed(self, colour):
        if not self.is_user_path:
            self.colour = colour
            self.is_visited = True

    def mark_open(self):
        if not self.is_user_path:
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
        self.is_visited = True
        
    def mark_user_path(self):
        if not (self.is_start or self.is_end):
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
        final_x = self.x + GRID_X_OFFSET + padding_x
        final_y = self.y + GRID_Y_OFFSET + padding_y
        
        category = 'background'
        if self.is_start:
            category = 'start'
        elif self.is_end:
            category = 'end'
        elif self.is_wall:
            category = 'wall'
        elif self.colour == PURPLE:
            category = 'path'
        elif self.colour == GREEN:
            category = 'search'
        elif self.is_visited:
            category = 'margin_of_search'

        if self.is_start:
            category = 'start'
        elif self.is_end:
            category = 'end'
        elif self.colour == PURPLE:
            category = 'path'

        # draw texture
        try:
            texture = texture_manager.get_active_texture(category)
            win.blit(texture, (final_x, final_y))
        except Exception as e:
            # fallback if texture fails
            pygame.draw.rect(win, self.colour, (final_x, final_y, self.width, self.width))
