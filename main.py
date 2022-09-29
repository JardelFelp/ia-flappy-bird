import os
import neat

from Game import Game
from Menu import Menu


def execute_ia(config_path, difficulty):
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

    population.run(Game(difficulty).main, 50)


if __name__ == "__main__":
    menu = Menu()
    mode = menu.select_mode()
    difficulty = menu.select_difficulty()

    print(f"Mode: {mode} | Difficulty: {difficulty}")

    if mode == "IA":
        path = os.path.dirname(__file__)
        execute_ia(os.path.join(path, 'config', 'config.txt'), difficulty)
    else:
        Game(difficulty).main(None, None)
