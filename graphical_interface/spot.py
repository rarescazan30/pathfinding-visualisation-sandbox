import pygame
from .constants import * 

class Spot:
    def __init__(self, row, col, width, total_rows):
        self.row = row
        self.col = col # coloana
        self.width = width
        self.x = row * width
        self.y = col * width
        self.colour = WHITE # colour of the spot
        self.neighbors = [] # list of neighboring spots
        self.total_rows = total_rows

        # proprieties for compatibility with backend algorithms

        self.is_start = False
        self.is_finish = False

        self.is_visited = False
        self.parent = None
        self.is_wall = False

    def get_pos(self):
        return self.row, self.col
    def is_closed(self):
        return self.colour == RED
    def is_open(self):
        return self.colour == GREEN
    def is_barrier(self):
        return self.colour == BLACK
    def is_start(self):
        return self.colour == ORANGE
    def is_end(self):
        return self.colour == TURQUOISE

    def mark_start(self):
        self.colour = ORANGE
        self.is_wall = False
        self.is_visited = False
        self.is_start = True
        self.is_end = False
    def mark_closed(self):
        self.colour = RED
        self.is_wall = False
        self.is_visited = True
    def mark_open(self):
        self.colour = GREEN
        self.is_wall = False
        self.is_visited = False
    def mark_barrier(self):
        self.colour = BLACK
        self.is_wall = True
        self.is_visited = False
        self.is_start = False
        self.is_end = False
    def mark_end(self):
        self.colour = TURQUOISE
        self.is_wall = False
        self.is_visited =  False
        self.is_end = True
        self.is_start = False
    def mark_path(self):
        self.colour = PURPLE
        self.is_wall = False
        self.is_visited = True

    def reset(self):
        self.colour = WHITE
        self.is_visited = False
        self.parent = None
        self.is_wall = False
        self.is_end = False
        self.is_start = False

    # metohod to draw rectangle on main window        
    def draw(self, win):
        pygame.draw.rect(win, self.colour, (self.x, self.y, self.width, self.width))

        
