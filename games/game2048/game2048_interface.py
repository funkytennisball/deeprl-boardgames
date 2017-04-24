""" simple(ugly and unituitive) interface for the 2048 game """

from .game2048 import Game2048


class Game2048Interface:
    """ main class for the interface """

    def __init__(self):
        self.game = Game2048()

    def play(self):
        """ plays the game of 2048 until it ends """

        while self.game.game_state != Game2048.GameState.ENDED:
            self.print_board()

            try:
                move = input('Move (w/a/s/d):')

                if move == 'w':
                    self.game.step(Game2048.Action.UP)
                elif move == 'a':
                    self.game.step(Game2048.Action.LEFT)
                elif move == 's':
                    self.game.step(Game2048.Action.DOWN)
                elif move == 'd':
                    self.game.step(Game2048.Action.RIGHT)
            except ValueError:
                print('input valid value (w/a/s/d)')

    def print_board(self):
        """ prints the board of the 2048 game on the console """

        scoreboard = 'GameScore: ' + str(self.game.game_score)
        board_str = str(self.game)

        print(scoreboard + '\n' + board_str)
