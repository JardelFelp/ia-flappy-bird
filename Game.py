import pygame
import os
import neat

from Bird import Bird
from Pipe import Pipe
from Floor import Floor


# Initialize fonts
def get_font():
    pygame.font.init()
    return pygame.font.SysFont('arial', 35)


class Game:
    BACKGROUND_IMAGE = pygame.transform.scale2x(pygame.image.load(os.path.join('images', 'bg.png')))
    SCORE_FONT = get_font()
    SCREEN_WIDTH = 500
    SCREEN_HEIGHT = 800

    def __init__(self):
        # Check if is the IA Playing
        self.ia_playing = False
        self.score = 0
        # Screen Elements
        self.birds = []
        self.pipes = []
        self.floor = []
        # IA
        self.genomes = None
        self.config = None
        self.generation = 0
        self.genomes_list = []
        self.networks = []
        # Screem
        self.screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))

    def _print_score_and_generation(self):
        # Add Score in The Screen
        score_text = self.SCORE_FONT.render(f"Score: {self.score}", 1, (255, 255, 255))
        self.screen.blit(score_text, (self.SCREEN_WIDTH - 10 - score_text.get_width(), 10))

        # Add Generation in The Screen
        if self.ia_playing:
            generation_text = self.SCORE_FONT.render(f"Generation: {self.generation}", 1, (255, 255, 255))
            self.screen.blit(generation_text, (10, 10))

    def generate_screen(self):
        # Create Background Image
        self.screen.blit(self.BACKGROUND_IMAGE, (0, 0))

        # Add Elements on Screen
        for bird in self.birds:
            bird.print(self.screen)

        for pipe in self.pipes:
            pipe.print(self.screen)

        self.floor.print(self.screen)

        # Update Texts
        self._print_score_and_generation()

        # Update Display
        pygame.display.update()

    def _generate_ia_variables(self):
        for _, genome in self.genomes:
            network = neat.nn.FeedForwardNetwork.create(genome, self.config)
            self.networks.append(network)
            genome.fitness = 0
            self.genomes_list.append(genome)
            self.birds.append(Bird(230, 350))

    def _check_events(self):
        # User Interactions
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE and not self.ia_playing:
                for bird in self.birds:
                    bird.jump()

    def _get_next_pipe_index(self):
        pipe_index = 0

        if len(self.birds) > 0:
            if len(self.pipes) > 1 and self.birds[0].x > (self.pipes[0].x + self.pipes[0].TOP_PIPE.get_width()):
                pipe_index = 1
            else:
                pipe_index = 0

        return pipe_index

    def _move_bird(self, pipe_index):
        for index, bird in enumerate(self.birds):
            bird.move()

            if self.ia_playing:
                # Increment Fitness
                self.genomes_list[index].fitness += 0.1
                output = self.networks[index].activate((
                    bird.x,
                    abs(bird.y - self.pipes[pipe_index].height),
                    abs(bird.y - self.pipes[pipe_index].bottom_position)
                ))

                if output[0] >= 0.5:
                    bird.jump()

    def _create_and_delete_pipes(self):
        create_pipe = False
        removed_pipes = []

        # Check Collision and Change Pipe List
        for pipe in self.pipes:
            for index, bird in enumerate(self.birds):
                if pipe.has_collision(bird):
                    self.birds.pop(index)
                    if self.ia_playing:
                        self.genomes_list[index].fitness -= 1
                        self.genomes_list.pop(index)
                        self.networks.pop(index)

                if not pipe.bird_has_passed and bird.x > pipe.x:
                    create_pipe = True
                    pipe.bird_has_passed = True

                if (pipe.x + pipe.TOP_PIPE.get_width()) < 0:
                    removed_pipes.append(pipe)

            pipe.move()

        # Create Pipe if is Necessary
        if create_pipe:
            self.score += 1
            self.pipes.append(Pipe(600))

            for genome in self.genomes_list:
                genome.fitness += 5

        # Remove Pipe if is Necessary
        for index, pipe in enumerate(removed_pipes):
            if index < len(self.pipes):
                self.pipes.pop(index)

        for index, bird in enumerate(self.birds):
            # Floor Collision
            if (bird.y + bird.image.get_height()) > self.floor.y or bird.y < 0:
                self.birds.pop(index)

                if self.ia_playing:
                    # genomes_list[index].fitness -= 1
                    self.genomes_list.pop(index)
                    self.networks.pop(index)

        self.generate_screen()

    def main(self, genomes, config):
        self.genomes = genomes
        self.config = config

        self.ia_playing = self.genomes is not None and self.config is not None
        self.generation += 1

        if self.ia_playing:
            self._generate_ia_variables()
        else:
            self.birds = [Bird(230, 350)]

        self.floor = Floor(730)
        self.pipes = [Pipe(700)]
        score = 0

        # Assistant Variable
        frames_per_second = pygame.time.Clock()
        executing = True

        while executing:
            frames_per_second.tick(30)

            # Check events to Quit and Jump
            self._check_events()

            pipe_index = self._get_next_pipe_index()

            if len(self.birds) == 0 and self.ia_playing:
                break

            # Move Birds
            self._move_bird(pipe_index)

            self.floor.move()

            # Create and delete pipes
            self._create_and_delete_pipes()
