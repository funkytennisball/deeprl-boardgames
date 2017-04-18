"""
DQN learning for tic tac toe
"""

import yaml

from ai import AI

if __name__ == "__main__":
    # Load the YAML config file
    CONFIG_FILE = 'config.yml'
    with open(CONFIG_FILE, 'r') as ymlfile:
        CONFIG = yaml.load(ymlfile)

    if CONFIG:
        AI_GAME = AI(CONFIG)
        AI_GAME.learn()
