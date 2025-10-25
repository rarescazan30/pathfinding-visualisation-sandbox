import pygame
import shared
from .constants import * 

START_IMAGE = pygame.image.load('graphical_interface/start_crate.png')
PATH_IMAGE = pygame.image.load('graphical_interface/path.png')
PATH_BARRIER = pygame.image.load('graphical_interface/barrier.png')

class Spot:
    def __init__(self, row, col, width, total_rows):
        self.row = row
        self.col = col # coloana
        self.width = width
        self.x = row * width
        self.y = col * width
        self.image = None # we want to add images instead of some plain square spots
        self.colour = WHITE # colour of the spot
        self.neighbors = [] # list of neighboring spots
        self.total_rows = total_rows
        self.start_image = pygame.transform.scale(START_IMAGE, (width, width))
        self.path_image = pygame.transform.scale(PATH_IMAGE, (width, width))
        self.barrier_image = pygame.transform.scale(PATH_BARRIER, (width, width))
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
        self.image = self.start_image
        self.colour = WHITE
        self.is_wall = False
        self.is_visited = False
        self.is_start = True
        self.is_end = False
    def mark_closed(self, colour):
        self.colour = colour
        self.is_wall = False
        self.is_visited = True
    def mark_open(self):
        self.colour = GREEN
        self.is_wall = False
        self.is_visited = False
    def mark_barrier(self):
        self.image = self.barrier_image
        self.colour = shared.cur_square_color
        self.is_wall = True
        self.is_visited = False
        self.is_start = False
        self.is_end = False
    def mark_outer_barrier(self):
        self.image = self.barrier_image
        self.colour = BLACK
        self.is_wall = True
        self.is_visited = False
        self.is_start = False
        self.is_end = False
    
    def mark_end(self):
        self.image = self.start_image
        self.colour = RED
        self.is_wall = False
        self.is_visited =  False
        self.is_end = True
        self.is_start = False
    def mark_path(self):
        self.image = self.path_image
        self.colour = shared.cur_square_color
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
        if self.image:
            win.blit(self.image, (self.x, self.y))
        
            

        
