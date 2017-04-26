""" simple(ugly and unituitive) interface for the 2048 game """

import sys
import os
import time
from .game2048 import Game2048


class Game2048Interface:
    """ main class for the interface """

    def __init__(self, ai_player=None, refresh_rate=0.2):
        self.game = Game2048()
        self.os_windows = os.name == 'nt'

        self.ai_player = ai_player
        self.refresh_rate = refresh_rate

        if self.ai_player:
            ai_player.play(self.game)

    def play(self):
        """ plays the game of 2048 until it ends """

        while self.game.game_state != Game2048.GameState.ENDED:
            self.clear_layout()
            self.print_board()

            if self.ai_player:
                time.sleep(self.refresh_rate)
                selected_move = self.ai_player.move()
            else:
                try:
                    move = input('Move (w/a/s/d):')

                    if move == 'w':
                        selected_move = Game2048.Action.UP
                    elif move == 'a':
                        selected_move = Game2048.Action.LEFT
                    elif move == 's':
                        selected_move = Game2048.Action.DOWN
                    elif move == 'd':
                        selected_move = Game2048.Action.RIGHT
                except ValueError:
                    print('input valid value (w/a/s/d)')

            self.game.step(selected_move)

    def clear_layout(self):
        """ clears the game layout """
        if self.os_windows:
            os.system('cls')
        else:
            os.system('clear')

    def print_board(self):
        """ prints the board of the 2048 game on the console """

        scoreboard = 'GameScore: ' + str(self.game.game_score)
        board_str = str(self.game)

        sys.stdout.write(scoreboard + '\n' + board_str)
