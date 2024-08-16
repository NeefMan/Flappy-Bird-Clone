import pygame

class Button:
    def __init__(self, main, x, y, width, height, color, centered=False):
        self.main = main
        self.button_rect = pygame.Rect(x, y, width, height)
        if centered:
            self.button_rect.center = self.main.screen.get_rect().center
        self.color = color
    
    def draw_button(self):
        pygame.draw.rect(self.main.screen, self.color, self.button_rect)
    
    def click_in_range(self, event):
        x, y = event.pos
        if (x in range(self.button_rect.left, self.button_rect.right) and 
        y in range(self.button_rect.top, self.button_rect.bottom)):
            return True
        return False

    def display_text(self, text, size, manual_pos=None, pos_by_rect=False):
        font = pygame.font.SysFont("comicsansms", int(size))
        rendered_text = font.render(text, 1, self.main.settings.colors["black"])
        width, height = rendered_text.get_size()
    
        if manual_pos:
            x, y = manual_pos
            self.main.screen.blit(rendered_text, pygame.Rect(x,y,width,height))

        if pos_by_rect:
            rect_x, rect_y = self.button_rect.center
            x = rect_x - (width//2)
            y = rect_y - (height//2)
            self.main.screen.blit(rendered_text, pygame.Rect(x,y,width,height))