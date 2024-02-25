import pygame

class HealthBar():
    def __init__(self, x, y, w, h, max_hp):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.hp = max_hp
        self.max_hp = max_hp

    def draw(self, window):
        ratio = self.hp / self.max_hp
        pygame.draw.rect(window, "red", (self.x, self. y, self.w, self.h))
        pygame.draw.rect(window, "green", (self.x, self.y, self.w * ratio, self.h))



