import pygame

from graphical_interface.constants import *

class Button:
    def __init__(self, x, y, width, height, text, font, base_color, hovering_color):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.font = font
        self.base_color = base_color
        self.hovering_color = hovering_color
        self.current_color = base_color
        self.text_color = (255, 255, 255)  # TODO: set customizable text color

    def create_buttons(button_font, small_font):
        button_x = GRID_X_OFFSET + GRID_WIDTH + 50
        find_path_button = Button(
            x=button_x, y=100, width=200, height=50,
            text="Find Path", font=button_font,
            base_color=GREEN, hovering_color=BLUE)
        toggle_grid_button = Button(
            x=button_x, y=180, width=200, height=50,
            text="Toggle Grid", font=button_font,
            base_color=PURPLE, hovering_color=GREEN)
        toggle_mode_button = Button(
            x=button_x, y=260, width=200, height=50,
            text="Switch to Eraser", font=button_font,
            base_color=BUTTON_RED, hovering_color=HOVER_BUTTON_RED)
        decrease_button = Button(
            x=button_x, y=380, width=50, height=50,
            text="-", font=small_font,
            base_color=GREY, hovering_color=(190, 190, 190))
        increase_button = Button(
            x=button_x + 150, y=380, width=50, height=50,
            text="+", font=small_font,
            base_color=GREY, hovering_color=(190, 190, 190))
        
        left_button_x = 60
        
        load_matrix_button = Button(
            x=left_button_x, y=100, width=200, height=50, 
            text="Load Labyrinth", font=button_font, 
            base_color=BLUE, hovering_color=GREEN
        )
        save_matrix_button = Button(
            x=left_button_x, y=170, width=200, height=50, 
            text="Save Labyrinth", font=button_font, 
            base_color=BLUE, hovering_color=GREEN
        )
        bfs_button = Button(
            x=left_button_x, y=260, width=200, height=50,
            text="BFS (Default)", font=button_font,
            base_color=PURPLE, hovering_color=GREEN
        )
        dfs_button = Button(
            x=left_button_x, y=330, width=200, height=50,
            text="DFS", font=button_font,
            base_color=PURPLE, hovering_color=GREEN
        )
        gbfs_button = Button(
            x=left_button_x, y=400, width=200, height=50,
            text="Greedy Best-First", font=button_font,
            base_color=PURPLE, hovering_color=GREEN
        )
        return [
            find_path_button, toggle_grid_button, toggle_mode_button, 
            decrease_button, increase_button,
            load_matrix_button, save_matrix_button,
            bfs_button, dfs_button, gbfs_button
        ]

    def draw(self, win):
        # Draw the button rectangle
        pygame.draw.rect(win, self.current_color, self.rect, border_radius=12)
        
        # Render and center the text
        text_surface = self.font.render(self.text, True, (255, 255, 255))
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
        """Updates the text displayed on the button."""
        self.text = new_text
        