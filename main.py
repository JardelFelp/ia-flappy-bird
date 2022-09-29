import os
import neat

from Game import Game

ia_playing = True


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

    population.run(Game().main, 50)


if __name__ == "__main__":
    if ia_playing:
        path = os.path.dirname(__file__)
        execute_ia(os.path.join(path, 'config', 'config.txt'))
    else:
        Game().main(None, None)
