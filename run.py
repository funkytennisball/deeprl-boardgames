"""
Starting point

Usage:
-c 'config.yml' (config file path)
-g 'tictactoe' (select games: tictactoe/2048)
-m 'play' (select modes: play/learn)
"""

import sys
import getopt

import yaml

from ai.ai2048 import AI2048
from ai.ai_cartpole import AICartPole
from games.game2048.game2048_interface import Game2048Interface

def program_quit():
    """ exists program and provides instructions """
    print('Run Instructions:')
    print('run.py '
          '-c <config_file[default=config.yml]> ')
    sys.exit(2)


def program_action(config):
    ''' invoke ai '''
    game = config['Game']
    play_mode = config['PlayMode']

    if game == '2048':
        if play_mode == 'aiplay':
            ai_2048 = AI2048(config, False)
            ai_2048.load()
            interface = Game2048Interface(ai_2048)
            interface.play()
        elif play_mode == 'play':
            interface = Game2048Interface()
            interface.play()
        elif play_mode == 'learn':
            ai_2048 = AI2048(config, True)
            ai_2048.learn()
        else:
            program_quit()
    elif game == 'cartpole':
        if play_mode == 'learn':
            ai_cartpole = AICartPole(config, True)
            ai_cartpole.learn()
    else:
        program_quit()


def main(argv):
    """ parses argument list from user """
    # Default config file
    config_file = 'config.yml'

    try:
        opts, _ = getopt.getopt(argv, 'h:c:')
    except getopt.GetoptError:
        program_quit()

    for opt, arg in opts:
        if opt == '-h':
            program_quit()
        elif opt == '-c':
            config_file = arg

    with open(config_file, 'r') as ymlfile:
        config = yaml.load(ymlfile)

        program_action(config)


if __name__ == "__main__":
    main(sys.argv[1:])
