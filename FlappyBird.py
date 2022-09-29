import pygame
import os
import random

from Bird import Bird
from Pipe import Pipe
from Floor import Floor

# Screen sizes
SCREEN_WIDTH = 500
SCREEN_HEIGHT = 800

# Import game images
BACKGROUND_IMAGE = pygame.transform.scale2x(pygame.image.load(os.path.join('images', 'bg.png')))

# Initialize fonts
pygame.font.init()
SCORE_FONT = pygame.font.SysFont('arial', 50)


def print_screen(screen, birds, pipes, floor, score):
    # Create Background Image
    screen.blit(BACKGROUND_IMAGE, (0, 0))

    # Add Elements on Screen
    for bird in birds:
        bird.print(screen)

    for pipe in pipes:
        pipe.print(screen)

    floor.print(screen)

    # Add Score in The Screen
    text = SCORE_FONT.render(f"Score: { score }", 1, (255, 255, 255))
    screen.blit(text, (SCREEN_WIDTH - 10 - text.get_width(), 10))

    # Update Display
    pygame.display.update()


def main():
    # Create Elements
    birds = [Bird(230, 350)]
    floor = Floor(730)
    pipes = [Pipe(700)]
    # Create Screen
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    # Create Score
    score = 0
    # Create FPS Timer
    frames_per_second = pygame.time.Clock()
    # Assistant Variable
    executing = True

    while executing:
        frames_per_second.tick(30)

        # User Interactions
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                executing = False
                pygame.quit()
                quit()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                for bird in birds:
                    bird.jump()

        # Move Elements
        for bird in birds:
            bird.move()

        if len(birds) > 0:
            floor.move()

        create_pipe = False
        removed_pipes = []

        # Check Collision and Change Pipe List
        for pipe in pipes:
            for index, bird in enumerate(birds):
                if pipe.has_collision(bird):
                    birds.pop(index)
                if not pipe.bird_has_passed and bird.x > pipe.x:
                    create_pipe = True
                    pipe.bird_has_passed = True

                pipe.move()

                if (pipe.x + pipe.TOP_PIPE.get_width()) < 0:
                    removed_pipes.append(pipe)

        # Create Pipe if is Necessary
        if create_pipe:
            score += 1
            pipes.append(Pipe(600))

        # Remove Pipe if is Necessary
        for pipe in removed_pipes:
            pipes.remove(pipe)

        for index, bird in enumerate(birds):
            # Floor Collision
            if (bird.y + bird.image.get_height()) > floor.y or bird.y < 0:
                birds.pop(index)

        print_screen(screen, birds, pipes, floor, score)


if __name__ == "__main__":
    main()
