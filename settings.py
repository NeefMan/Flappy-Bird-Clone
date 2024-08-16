import pygame
class Settings:
    def __init__(self):
        self.screen_width = 500
        self.screen_height = 800
        self.screen_size = (self.screen_width, self.screen_height)
        self.fps = 1000
        self.clock = pygame.time.Clock()
        self.gravity = 3.5
        self.jump_vel = -25
        self.scroll_speed = 3.75

        # Colors
        self.colors = {
            "bg_color": (190,190,190),
            "yellow": (250,218,94),
            "dark_yellow": (220,188,64),
            "red": (250,0,0),
            "black": (0,0,0),
        }