import pygame
import os
import neat

from Bird import Bird
from Pipe import Pipe
from Floor import Floor

# IA Variables
ia_playing = True
generation = 0

# Screen sizes
SCREEN_WIDTH = 500
SCREEN_HEIGHT = 800

# Import game images
BACKGROUND_IMAGE = pygame.transform.scale2x(pygame.image.load(os.path.join('images', 'bg.png')))

# Initialize fonts
pygame.font.init()
SCORE_FONT = pygame.font.SysFont('arial', 35)


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
    score_text = SCORE_FONT.render(f"Score: { score }", 1, (255, 255, 255))
    screen.blit(score_text, (SCREEN_WIDTH - 10 - score_text.get_width(), 10))

    # Add Generation in The Screen
    if ia_playing:
        generation_text = SCORE_FONT.render(f"Generation: {generation}", 1, (255, 255, 255))
        screen.blit(generation_text, (10, 10))

    # Update Display
    pygame.display.update()


# Fitness Function
def main(genomes, config):
    # Set generation as a Global Variable
    global generation
    generation += 1

    if ia_playing:
        networks = []
        genomes_list = []
        birds = []

        for _, genome in genomes:
            network = neat.nn.FeedForwardNetwork.create(genome, config)
            networks.append(network)
            genome.fitness = 0
            genomes_list.append(genome)
            birds.append(Bird(230, 350))
    else:
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
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE and not ia_playing:
                for bird in birds:
                    bird.jump()

        pipe_index = 0

        if len(birds) > 0:
            if len(pipes) > 1 and birds[0].x > (pipes[0].x + pipes[0].TOP_PIPE.get_width()):
                pipe_index = 1
            else:
                pipe_index = 0
        else:
            break

        # Move Elements
        for index, bird in enumerate(birds):
            bird.move()

            if ia_playing:
                # Increment Fitness
                genomes_list[index].fitness += 0.1
                output = networks[index].activate((
                    bird.x,
                    abs(bird.y - pipes[pipe_index].height),
                    abs(bird.y - pipes[pipe_index].bottom_position)
                ))

                if output[0] >= 0.5:
                    bird.jump()

        floor.move()

        create_pipe = False
        removed_pipes = []

        # Check Collision and Change Pipe List
        for pipe in pipes:
            for index, bird in enumerate(birds):
                if pipe.has_collision(bird):
                    birds.pop(index)
                    if ia_playing:
                        genomes_list[index].fitness -= 1
                        genomes_list.pop(index)
                        networks.pop(index)

                if not pipe.bird_has_passed and bird.x > pipe.x:
                    create_pipe = True
                    pipe.bird_has_passed = True

                if (pipe.x + pipe.TOP_PIPE.get_width()) < 0:
                    removed_pipes.append(pipe)

            pipe.move()

        # Create Pipe if is Necessary
        if create_pipe:
            score += 1
            pipes.append(Pipe(600))

            for genome in genomes_list:
                genome.fitness += 5

        # Remove Pipe if is Necessary
        for index, pipe in enumerate(removed_pipes):
            if index < len(pipes):
                pipes.pop(index)

        for index, bird in enumerate(birds):
            # Floor Collision
            if (bird.y + bird.image.get_height()) > floor.y or bird.y < 0:
                birds.pop(index)

                if ia_playing:
                    # genomes_list[index].fitness -= 1
                    genomes_list.pop(index)
                    networks.pop(index)

        print_screen(screen, birds, pipes, floor, score)


def execute_ia(config_path):
    config = neat.config.Config(
        neat.DefaultGenome,
        neat.DefaultReproduction,
        neat.DefaultSpeciesSet,
        neat.DefaultStagnation,
        config_path
    )

    population = neat.Population(config)

    population.add_reporter(neat.StdOutReporter(True))
    population.add_reporter(neat.StatisticsReporter())

    population.run(main, 50)


if __name__ == "__main__":
    if ia_playing:
        path = os.path.dirname(__file__)
        execute_ia(os.path.join(path, 'config', 'config.txt'))
    else:
        main(None, None)
