import pygame
from pygame.sprite import Sprite
import time

class Pipe(Sprite):
    def __init__(self, main, image, x, y, top_pipe):
        super().__init__()
        self.main = main
        self.image = pygame.image.load(image)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.top_pipe = top_pipe
        self.pipe_created = False
        self.can_score = True
    
    def update(self):
        self.rect.x -= self.main.settings.scroll_speed

        if self.rect.x <= self.main.bird.x_pos-100 and self.top_pipe and not self.pipe_created:
            self.main.initialize_pipes()
            self.pipe_created = True

        if self.rect.right <= 0:
            self.main.pipes.remove(self)

        if self.top_pipe and self.can_score and self.rect.right < self.main.bird.x_pos:
            self.main.score += 1
            self.can_score = False
        
        """if self.rect.x in self.main.bird.x_vals:"""
        self.main.check_collision(self.main.bird.bird_collision_rect, self.rect)
            