import pygame
import sys
from settings import Settings
from sprites import SpriteSheet, Bird
from obstacles import Pipe
from ground import Ground
from sound_class import Sound
from ui import Ui
from button import Button
import random
import time
import json
import os

class Main:
    def __init__(self):
        pygame.init()
        self.clock = pygame.time.Clock()
        self.settings = Settings()
        self.screen = pygame.display.set_mode(self.settings.screen_size)
        pygame.display.set_caption("Flappy Bird")
        pygame.display.set_icon(pygame.image.load("images/flappy.ico"))
        self.ui = Ui(self)
        self.bird = Bird(self, "images/flappy_bird.png", "json/flappy_bird.json")
        self.background = pygame.image.load("images/background.png")
        self.sounds = Sound(self)
        
        self.pipes = pygame.sprite.Group()

        self.floor_tiles = pygame.sprite.Group()

        self.play_button = Button(self, 175, 625, 150, 50, self.settings.colors["yellow"])
        self.play_button_text = "Play"
        self.score_text_box = Button(self, 175, 450, 150, 150, self.settings.colors["yellow"])
        
        self.score = 0
        self.final_score = 0
        self.high_score = 0
        self.game_running = False
        self.get_high_score()

    def run(self):  
        while True:
            self.update_screen()
            self.handle_events()
            if self.game_running:
                self.pipes.update()
                self.floor_tiles.update()
                self.clock.tick(self.settings.fps)
            
    def update_screen(self): 
        self.screen.fill(self.settings.colors["bg_color"])
        self.screen.blit(pygame.transform.scale2x(self.background), (0,0))
        if self.game_running:
            self.update_game_screen()
        if not self.game_running:
            self.update_menu_display()
        pygame.display.flip() 
    
    def update_game_screen(self):
        self.bird.manage_sheet()
        self.pipes.draw(self.screen)
        self.floor_tiles.draw(self.screen)
        self.ui.display_score(self.score, (0,150), True)

    def update_menu_display(self):
        self.bird.display_sheet()
        self.screen.blit(pygame.image.load("images/ground.png"), (0,700))
        self.play_button.draw_button()
        self.play_button.display_text(self.play_button_text, 20, pos_by_rect=True)
        self.display_scores()

    def display_scores(self):
        self.score_text_box.draw_button()
        self.score_text_box.display_text("Score:", 20, manual_pos=(220,445))
        self.ui.display_score(self.final_score, (220, 492))
        self.score_text_box.display_text("Your Best:", 20, manual_pos=(200, 515))
        self.ui.display_score(self.high_score, (220, 565))

    def get_high_score(self):
        appdata_folder = os.getenv('APPDATA')
        app_folder = os.path.join(appdata_folder, 'Flappy Bird', 'Save Data')
        os.makedirs(app_folder, exist_ok=True)
        json_path = os.path.join(app_folder, 'data.json')
        
        try: 
            with open(json_path, "r") as f:
                data = json.load(f)
                self.high_score = data["high_score"]
                if self.final_score > data["high_score"]:
                    self.high_score = self.final_score
                    with open(json_path, "w") as new_file:
                        data["high_score"] = self.final_score
                        json.dump(data, new_file)
        except:
            with open(json_path, "w") as f:
                data = {"high_score": self.final_score}
                json.dump(data, f)
                self.high_score = self.final_score

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and self.game_running:
                    self.bird.jump_bool = True
                    self.settings.cur_jump_vel = self.settings.jump_vel
                    self.sounds.flap.play()
                if event.key == pygame.K_ESCAPE:
                    sys.exit()
            if not self.game_running:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        if self.play_button.click_in_range(event):
                            self.play_button.color = self.settings.colors["dark_yellow"]
                if event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 1:
                        self.play_button.color = self.settings.colors["yellow"]
                        if self.play_button.click_in_range(event):
                            self.reset_game()
                            self.game_running = True
                            self.play_button_text = "Play Again"
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.reset_game()
                        self.game_running = True
                        self.play_button_text = "Play Again"
    
    def create_top_pipe(self, y):
        screen_rect = self.screen.get_rect()
        # Initialize top pipe
        x = screen_rect.right
        top_pipe = Pipe(self, "images/top_pipe.png", x, y, True)
        self.pipes.add(top_pipe)

    def create_bottom_pipe(self, y):
        screen_rect = self.screen.get_rect()
        # Initialize bottom pipe
        x = screen_rect.right
        bottom_pipe = Pipe(self, "images/bottom_pipe.png", x, y, False)
        self.pipes.add(bottom_pipe)
    
    def check_collision(self, obj1, obj2):
        if ((obj1.right in range(obj2.left, obj2.right)and
            obj1.top in range(obj2.top, obj2.bottom)) or
            (obj1.right in range(obj2.left, obj2.right)and
            obj1.bottom in range(obj2.top, obj2.bottom)) or
            (obj1.left in range(obj2.left, obj2.right)and
            obj1.top in range(obj2.top, obj2.bottom)) or
            (obj1.left in range(obj2.left, obj2.right)and
            obj1.bottom in range(obj2.top, obj2.bottom))):
            if self.bird.y_pos > 600:
                self.sounds.hit_floor.play()
                self.die()
            else:
                self.sounds.death.play()
                self.die()
            

    def die(self):
        time.sleep(0.8)
        self.game_running = False
        self.bird.reset()
        self.reset_game() 

    def reset_game(self):
        self.bird.reset()
        # Reset pipes
        for pipe in self.pipes.copy():
            self.pipes.remove(pipe)
        self.initialize_pipes()
        self.initialize_ground()
        self.final_score = self.score
        self.get_high_score()
        self.score = 0
        pygame.event.clear()

    
    def initialize_pipes(self):
        num = random.randint(200, 500)
        self.create_top_pipe(num-620)
        self.create_bottom_pipe(num+120)

    def initialize_ground(self):
        new_floor = Ground(self, "images/ground.png", 0)
        self.floor_tiles.add(new_floor)
        new_floor = Ground(self, "images/ground.png", self.screen.get_rect().right)
        self.floor_tiles.add(new_floor)

if __name__ == "__main__":
    main = Main()
    main.run()