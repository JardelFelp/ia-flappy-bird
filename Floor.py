import pygame
import os

FLOOR_IMAGE = pygame.transform.scale2x(pygame.image.load(os.path.join('images', 'base.png')))


class Floor:
    VELOCITY = 5
    WIDTH = FLOOR_IMAGE.get_width()
    IMAGE = FLOOR_IMAGE

    def __init__(self, y):
        self.y = y
        self.x1 = 0
        self.x2 = self.WIDTH

    def move(self):
        # Create a infinite animation
        self.x1 -= self.VELOCITY
        self.x2 -= self.VELOCITY

        if (self.x1 + self.WIDTH) <= 0:
            self.x1 = self.x2 + self.WIDTH

        if (self.x2 + self.WIDTH) <= 0:
            self.x2 = self.x1 + self.WIDTH

    def print(self, screen):
        screen.blit(self.IMAGE, (self.x1, self.y))
        screen.blit(self.IMAGE, (self.x2, self.y))
