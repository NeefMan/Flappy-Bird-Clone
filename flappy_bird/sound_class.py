import pygame

class Sound:
    def __init__(self, main):
        self.main = main
        self.flap = pygame.mixer.Sound("sounds/flap2.wav")
        self.flap.set_volume(0.8)
        self.death = pygame.mixer.Sound("sounds/death.wav")
        self.death.set_volume(0.6)
        self.hit_floor = pygame.mixer.Sound("sounds/hit_floor.wav")