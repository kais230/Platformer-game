import pygame
from spritesheet import load_sprite_sheets


class Enemy(pygame.sprite.Sprite):
    SPRITES = load_sprite_sheets("MainCharacters", "PinkMan", 32, 32, True)
    ANIMATION_DELAY = 3

    def __init__(self, x, y, width, height, move_area_left, move_area_right):
        super().__init__()
        self.rect = pygame.Rect(x, y, width, height)
        self.animation_count = 0
        self.sprite = None
        self.image = pygame.Surface((width, height), pygame.SRCALPHA)
        self.moving_right = True
        self.move_area_left = move_area_left
        self.move_area_right = move_area_right

    def update_sprite(self):
        sprite_sheet_name = "idle" + "_" + ("right" if self.moving_right else "left")
        sprites = self.SPRITES[sprite_sheet_name]
        sprite_index = self.animation_count // self.ANIMATION_DELAY % len(sprites)
        self.sprite = sprites[sprite_index]
        self.image.blit(self.sprite, (0, 0))
        self.animation_count += 1
        self.update()

    def draw(self, window, offset_x, offset_y):
        window.blit(self.sprite, (self.rect.x - offset_x, self.rect.y- offset_y))

    def move(self):
        if self.moving_right:
            self.rect.x += 5  # movement speed
            if self.rect.right >= self.move_area_right:
                self.moving_right = False
        else:
            self.rect.x -= 5  # movement speed
            if self.rect.left <= self.move_area_left:
                self.moving_right = True

