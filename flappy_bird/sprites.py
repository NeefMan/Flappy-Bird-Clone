import pygame
import json
import time

class SpriteSheet:
    def __init__(self, main, sheet_file, meta_data):
        # References to external objects
        self.main = main
        self.settings = self.main.settings
        self.screen = self.main.screen
        self.screen_rect = self.screen.get_rect()
        
        # Files and related data
        self.image = pygame.image.load(sheet_file).convert_alpha()
        self.meta_data = meta_data
        self.f_name = sheet_file.split(".png")[0].split("images/")[1]
        
        # Frame data
        self.frames = {}
        self.frame = None
        self.total = 0
        self.current_frame = 0
        self.frameDuration = 0
        self.current_action = None
        
        # Position and screen-related logic
        self.x_pos, self.y_pos = self.screen_rect.center

        #Frame start and end times
        self.start = time.time()
        
        self.get_frame_rects()
    
    def get_frame_rects(self):
        with open(self.meta_data, "r") as f:
            data = json.load(f)

        frame_tags = data["meta"]["frameTags"]

        for tag in frame_tags:
            tempDic = {}
            for j, i in enumerate(range(tag["from"], tag["to"] + 1)):
                frame_name = f"{self.f_name} {i}.aseprite"
                frame = data["frames"][frame_name]["frame"]
                duration = data["frames"][frame_name]["duration"]
                tempDic[j] = {"frame": self.image.subsurface(pygame.Rect(
                    frame["x"],
                    frame["y"],
                    frame["w"],
                    frame["h"]
                )),
                "duration": duration
                }
            tempDic["total"] = len(tempDic) - 1
            self.frames[tag["name"]] = tempDic

    def display_sheet(self, rotation=0):        
        self.frame = self.frames[self.current_action][self.current_frame]["frame"]
        
        self.main.screen.blit(
            pygame.transform.rotate(self.frame, rotation),
            (self.x_pos, self.y_pos),
        )
    
    def increaseFrame(self):
        if (time.time() - self.start)*1000 >= self.frames[self.current_action][self.current_frame]["duration"]:
            self.current_frame += 1
            self.start = time.time()

class Bird(SpriteSheet):
    def __init__(self, main, sheet_file, meta_data):
        super().__init__(main, sheet_file, meta_data)
        self.current_action = "animation"
        self.default_pos = (self.main.settings.screen_width//2-100, self.main.settings.screen_height//2-100)
        self.x_pos, self.y_pos = self.default_pos
        self.jump_bool = False
        self.cur_vel = self.settings.gravity
        self.rotation = 0
        self.bird_collision_rect = None
        self.x_vals = {num for num in range(self.settings.screen_width//2-120, self.settings.screen_width//2-100+100)}
        self.update_collision_rect()

        # values for get_rotation() function
        self.up_count = 0
        self.down_count = 0
        self.initial_y_pos = self.y_pos
    
    def update_collision_rect(self):
        self.bird_collision_rect = pygame.Rect(0,0,60,66)
        bird_rect = self.frames[self.current_action][self.current_frame]["frame"].get_rect()
        bird_rect.x, bird_rect.y = self.x_pos, self.y_pos
        self.bird_collision_rect.center = bird_rect.center
        self.bird_collision_rect.x += 10
        self.bird_collision_rect.y += 17

    def manage_sheet(self):
        if self.y_pos < -100:
            self.main.sounds.hit_floor.play()
            self.main.die()
        self.update_collision_rect()
        self.get_rotation()
        self.display_sheet(self.rotation)
        # If current frame is last frame, reset animation to frame 0
        self.total = self.frames[self.current_action]["total"]
        
        if self.current_frame >= self.total:
            self.current_frame = 0
        
        self.increaseFrame()
        
        # Simulate gravity, reset pos if sprite goes off screen
        if self.y_pos + 79 < self.screen_rect.bottom:
            self.y_pos += self.main.settings.gravity
        else:
            self.x_pos, self.y_pos = self.default_pos
        
        self.jump()
    
    def get_rotation(self):
        if self.cur_vel <= 0:
            self.initial_y_pos = self.y_pos
        if self.cur_vel <= 0 and self.rotation < 30:
            self.rotation += 10
        if self.cur_vel > 0 and self.rotation > -70:
            self.up_count = 0
            if self.y_pos - self.initial_y_pos >= 80:
                self.rotation -= 5

    def jump(self):
        if self.jump_bool:
            self.cur_vel = self.settings.jump_vel
            self.jump_bool = False

        if self.cur_vel < self.settings.gravity:
            self.cur_vel += (self.settings.gravity)*0.50

        self.y_pos += self.cur_vel
        self.rect = pygame.rect.Rect(
            self.x_pos,
            self.y_pos,
            100,
            self.image.get_height()
        )
    
    def reset(self):
        self.x_pos, self.y_pos = self.default_pos
        self.rotation = 0
        self.current_frame = 0