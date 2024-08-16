import pygame
class Ui:
    def __init__(self, main):
        self.main = main
    
    def check_click_in_range(self, rect, event):
        x, y = event.pos
        if (x in range(rect.left, rect.right) and 
        y in range(rect.top, rect.bottom)):
            return True
        return False
    
    def display_score(self, source, starting_pos, scale_2x=False):
        cur_pos = starting_pos
        for digit in str(source):
            image = pygame.image.load(f"images/numbers/{digit}.png")
            if scale_2x:
                image = pygame.transform.scale2x(image)
            image_rect = image.get_rect()
            image_rect.midleft = cur_pos
            cur_pos = image_rect.midright
            self.main.screen.blit(image, image_rect)