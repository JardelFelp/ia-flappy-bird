import pygame
import os

BIRD_IMAGES = (
    pygame.transform.scale2x(pygame.image.load(os.path.join('images', 'bird1.png'))),
    pygame.transform.scale2x(pygame.image.load(os.path.join('images', 'bird2.png'))),
    pygame.transform.scale2x(pygame.image.load(os.path.join('images', 'bird3.png'))),
)


class Bird:
    IMAGES = BIRD_IMAGES
    # Rotations Animations
    MAX_ROTATION = 25
    ROTATION_VELOCITY = 20
    ANIMATION_TIME = 5

    def __init__(self, x, y):
        # Start position
        self.x = x
        self.y = y
        # Dynamic values
        self.angle = 0
        self.velocity = 0
        self.height = y
        # Assistant values
        self.time = 0
        self.image_count = 0
        self.image = self.IMAGES[0]

    def jump(self):
        self.velocity = -10.5
        self.time = 0
        self.height = self.y

    def move(self):
        # Calculate Movement
        self.time += 1
        movement = 1.5 * (self.time**2) + self.velocity * self.time

        # Restrict Movement
        if movement > 16:
            movement = 16
        elif movement < 0:
            movement -= 2

        self.y += movement

        # Set Bird Angle
        if movement < 0 or self.y < (self.height + 50):
            if self.angle < self.MAX_ROTATION:
                self.angle = self.MAX_ROTATION
        else:
            if self.angle > -90:
                self.angle -= self.ROTATION_VELOCITY

    def print(self, screen):
        # Set Bird Image
        self.image_count += 1

        # Bird Animation
        if self.image_count < self.ANIMATION_TIME:
            self.image = self.IMAGES[0]
        elif self.image_count < (self.ANIMATION_TIME * 2):
            self.image = self.IMAGES[1]
        elif self.image_count < (self.ANIMATION_TIME * 3):
            self.image = self.IMAGES[2]
        elif self.image_count < (self.ANIMATION_TIME * 4):
            self.image = self.IMAGES[1]
        elif self.image_count >= ((self.ANIMATION_TIME * 4) + 1):
            self.image = self.IMAGES[0]
            self.image_count = 0
        # Birt Fall
        if self.angle <= -80:
            self.image = self.IMAGES[0]
            # Next image is IMAGES[2]
            self.image_count = self.ANIMATION_TIME * 2

        # Print Bird Image
        rotation_image = pygame.transform.rotate(self.image, self.angle)
        center_position = self.image.get_rect(topleft=(self.x, self.y)).center
        bird_scope = rotation_image.get_rect(center=center_position)

        # Print bird using reference bird rectangle top left
        screen.blit(rotation_image, bird_scope.topleft)

    def get_mask(self):
        return pygame.mask.from_surface(self.image)
