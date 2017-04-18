"""
Starting point

Usage:
-c 'config.yml' (config file path)
-g 'tictactoe' (select games: tictactoe/2048)
-m 'play' (select modes: play/learn)
"""

import sys
import getopt

from ai.ai2048 import AI2048


def program_quit():
    """ exists program and provides instructions """
    print('Run Instructions:')
    print('run.py '
          '-g <game [tictactoe|2048]> '
          '-m <mode [play|learn]> '
          '-c <config_file[default=config.yml]> ')
    sys.exit(2)


def program_action(config_file, game, play_mode):
    ''' invoke ai '''
    if game == '2048':
        ai_2048 = AI2048(config_file)
        if play_mode == 'play':
            ai_2048.play()
        elif play_mode == 'learn':
            ai_2048.learn()
        else:
            program_quit()
    else:
        program_quit()


def main(argv):
    """ parses argument list from user """
    config_file = 'config.yml'
    game = None
    play_mode = None

    try:
        opts, _ = getopt.getopt(argv, 'hc:g:m:')
    except getopt.GetoptError:
        program_quit()

    for opt, arg in opts:
        if opt == '-h':
            program_quit()
        elif opt == '-c':
            config_file = arg
        elif opt == '-g':
            game = arg
        elif opt == '-m':
            play_mode = arg

    if config_file is None or game is None or play_mode is None:
        program_quit()

    program_action(config_file, game, play_mode)


if __name__ == "__main__":
    main(sys.argv[1:])
