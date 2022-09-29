import pygame
import random
import os

PIPE_IMAGE = pygame.transform.scale2x(pygame.image.load(os.path.join('images', 'pipe.png')))


class Pipe:
    DISTANCE = 200
    VELOCITY = 5

    def __init__(self, x, difficulty):
        self.x = x
        self.height = 0
        self.top_position = 0
        self.bottom_position = 0
        # Pipe Images
        self.BOTTOM_PIPE = PIPE_IMAGE
        self.TOP_PIPE = pygame.transform.flip(PIPE_IMAGE, False, True)
        # Controller Props
        self.bird_has_passed = False
        self.difficulty = difficulty
        self.direction = -1 if random.randrange(0, 1) == 0 else 1

        # Call set_height Function
        self.set_height()

    def _get_distance(self):
        if self.difficulty == "MEDIUM":
            return self.DISTANCE - 25
        else:
            return self.DISTANCE

    def set_height(self):
        self.height = random.randrange(50, 450)
        self.top_position = self.height - self.TOP_PIPE.get_height()
        self.bottom_position = self.height + self._get_distance()

    def move(self):
        # The Screen move from Right to Left
        self.x -= self.VELOCITY

        if self.difficulty == "HARD":
            self.top_position += (1 * self.direction)
            self.bottom_position += (1 * self.direction)

            if self.bottom_position >= 450:
                self.direction = -1
            elif (self.top_position + self.TOP_PIPE.get_height()) <= 50:
                self.direction = +1

    def print(self, screen):
        screen.blit(self.TOP_PIPE, (self.x, self.top_position))
        screen.blit(self.BOTTOM_PIPE, (self.x, self.bottom_position))

    def has_collision(self, bird):
        # Create Masks
        bird_mask = bird.get_mask()
        pipe_top_mask = pygame.mask.from_surface(self.TOP_PIPE)
        pipe_bottom_mask = pygame.mask.from_surface(self.BOTTOM_PIPE)

        # Get distance of the bird with the pipes
        distance_top = (round(self.x - bird.x), round(self.top_position - bird.y))
        distance_bottom = (round(self.x - bird.x), round(self.bottom_position - bird.y))

        # Check Collision
        pipe_top_has_collision = bird_mask.overlap(pipe_top_mask, distance_top)
        pipe_bottom_has_collision = bird_mask.overlap(pipe_bottom_mask, distance_bottom)

        return pipe_top_has_collision or pipe_bottom_has_collision
