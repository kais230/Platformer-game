import pygame
import time
from os import listdir
from os.path import isfile, join
from spritesheet import load_sprite_sheets
from health_bar import HealthBar


class Player(pygame.sprite.Sprite, HealthBar):
    COLOR =(255,0,0)
    GRAVITY= 1
    SPRITES= load_sprite_sheets("MainCharacters", "MaskDude", 32, 32, True)
    ANIMATION_DELAY=3

    def __init__(self,x,y,width,height):
        super().__init__()
        self.rect = pygame.Rect( x,y, width,height)
        self.x_vel = 0
        self.y_vel = 0
        self.mask = None
        self.direction = "left"
        self.animation_count = 0
        self.fall_count = 0
        self.hit = False
        self.hit_count = 0
        self.jump_count = 0
        self.hp = 100


    def jump(self):
        self.y_vel = -self.GRAVITY * 8
        if self.hit == False:
            self.animation_count = 0
        self.jump_count += 1
        if self.jump_count == 1:
            self.fall_count = 0

    def make_hit(self):
        self.hit = True
        self.hit_count = 0

    def move(self, dx, dy):
        self.rect.x += dx
        self.rect.y += dy

    def move_left(self,vel):
        self.x_vel += -vel
        if self.direction != "left":
            self.direction = "left"
            self.animation_count = 0

    def move_right(self,vel):
        self.x_vel += vel
        if self.direction != "right":
            self.direction = "right"
            self.animation_count = 0

    def loop(self,fps, dt):
        self.y_vel += min(1, (self.fall_count /fps) * self.GRAVITY ) #realistic gravity implementation
        self.move(self.x_vel, self.y_vel)

        if self.hit:
            # Adjust health reduction to make it frame rate independent
            health_reduction_per_frame = 100 / 2  # 2 seconds for hit animation
            if self.hit_count == 0:
                self.hp -= health_reduction_per_frame *dt

            self.hit_count += 1
        if self.hit_count > fps * 2:
            self.hit = False
            self.hit_count = 0

        self.fall_count += 1
        self.update_sprite()

    def landed(self):
        self.fall_count = 0
        self.y_vel = 0
        self.jump_count = 0

    def hit_head(self):
        self.count = 0
        self.y_vel *= -1

    def update_sprite(self):
        sprite_sheet = "idle"
        if self.hit:
            #pass
            sprite_sheet = "hit4"
        elif self.y_vel < 0:
            if self.jump_count == 1:
                sprite_sheet = "jump"
            elif self.jump_count == 2:
                sprite_sheet = "double_jump"
        elif self.y_vel > self.GRAVITY * 2:
            sprite_sheet = "fall"
        elif self.x_vel != 0:
            sprite_sheet = "run"

        sprite_sheet_name= sprite_sheet + "_" + self.direction
        sprites = self.SPRITES[sprite_sheet_name]
        sprite_index = self.animation_count // self.ANIMATION_DELAY % len(sprites)
        self.sprite = sprites[sprite_index]
        self.animation_count += 1
        self.update()

    def update(self):
        self.rect = self.sprite.get_rect(topleft=(self.rect.x, self.rect.y))

        self.mask = pygame.mask.from_surface(self.sprite) #pixel perfect collision




    def draw(self, win,offset_x, offset_y):
        win.blit(self.sprite, (self.rect.x - offset_x, self.rect.y - offset_y))

