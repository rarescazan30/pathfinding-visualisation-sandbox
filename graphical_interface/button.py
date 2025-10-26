import pygame

class Button:
    def __init__(self, x, y, width, height, text, font, base_color, hovering_color):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.font = font
        self.base_color = base_color
        self.hovering_color = hovering_color
        self.current_color = base_color

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
        