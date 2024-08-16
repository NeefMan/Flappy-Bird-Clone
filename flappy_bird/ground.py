import pygame
from pygame.sprite import Sprite

class Ground(Sprite):
    def __init__(self, main, image, x):
        super().__init__()
        self.main = main
        self.image = pygame.image.load(image)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = 700

    def update(self):
        self.rect.x -= self.main.settings.scroll_speed
        if self.rect.right <= 5:
            for tile in self.main.floor_tiles.copy():
                self.main.floor_tiles.remove(tile)
            self.main.initialize_ground()
        
        self.main.check_collision(pygame.rect.Rect(
            self.main.bird.x_pos,
            self.main.bird.y_pos,
            100,
            self.main.bird.image.get_height()
        ),
        self.rect)