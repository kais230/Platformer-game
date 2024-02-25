import pygame
from spritesheet import load_sprite_sheets, get_block


class Object(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, name=None):
        super().__init__()
        self.rect = pygame.Rect(x, y, width, height)
        self.image = pygame.Surface((width, height), pygame.SRCALPHA)
        self.width = width
        self.height = height
        self.name = name
        self.counter_c = 0

    def draw(self, win, offset_x, offset_y):
        win.blit(self.image, (self.rect.x - offset_x, self.rect.y - offset_y))


class Block(Object):
    def __init__(self, x, y, size):
        super().__init__(x, y, size, size)
        block = get_block(size, 96, 64)
        self.image.blit(block, (0, 0))
        self.mask = pygame.mask.from_surface(self.image)


class GoldBlock(Object):
    def __init__(self, x, y, size):
        super().__init__(x, y, size, size)
        block = get_block(size, 288, 128)
        self.image.blit(block, (0, 0))
        self.mask = pygame.mask.from_surface(self.image)


class Portal(Object):
    def __init__(self, x, y, size, block_name):
        super().__init__(x, y, size, size, block_name)
        block = get_block(size, 0, 128)
        self.image.blit(block, (0, 0))
        self.mask = pygame.mask.from_surface(self.image)


class Trap(Object):
    ANIMATION_DELAY = 3

    def __init__(self, x, y, width, height, trap_name):
        super().__init__(x, y, width, height, trap_name)
        self.fire = load_sprite_sheets("Traps", trap_name, width, height)
        self.image = self.fire["off"][0]
        self.mask = pygame.mask.from_surface(self.image)
        self.animation_count = 0
        self.animation_name = "off"
        self.hit_player = False

    def on(self):
        self.animation_name = "on"

    def off(self):
        self.animation_name = "off"

    def loop(self):

        sprites = self.fire[self.animation_name]
        sprite_index = self.animation_count // self.ANIMATION_DELAY % len(sprites)
        self.image = sprites[sprite_index]
        self.animation_count += 1
        self.rect = self.image.get_rect(topleft=(self.rect.x, self.rect.y))
        self.mask = pygame.mask.from_surface(self.image)  # pixel perfect collision

        if self.animation_count // self.ANIMATION_DELAY > len(sprites):
            self.animation_count = 0


