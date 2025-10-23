import pygame
import math
from queue import PriorityQueue
from constants import * 

pygame.init()

WIN = pygame.display.set_mode((WIDTH, WIDTH))
pygame.display.set_caption("Pathfinding Visualisation Sandbox")




run = True
fill_colour = RED

try:
    FONT = pygame.font.Font('BitcountGridSingle-VariableFont_CRSV,ELSH,ELXP,slnt,wght.ttf', 40)
except pygame.error:
    # in case font not installed/found
    print("Error loading custom font. Falling back to monospace.")
    FONT = pygame.font.SysFont('monospace', 30)

current_message = "Press a key to start"


while run:
    WIN.fill(fill_colour)
    #check for quit
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
          run = False
        if event.type == pygame.KEYDOWN:
            fill_colour = TURQUOISE
            current_message = "You pressed a key!"
            pygame.display.set_caption(current_message)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            current_message = "You pressed mouse button!"
            fill_colour = ORANGE   
            pygame.display.set_caption(current_message)
    text_surface = FONT.render(current_message, True, BLACK) # render text surface
    text_rect = text_surface.get_rect(center=(WIDTH // 2, 50)) # made square where text will be
    WIN.blit(text_surface, text_rect) # draw text onto surface   
    
           
    
    pygame.display.update()
    

pygame.quit()