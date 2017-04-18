""" simple(ugly and unituitive) interface for the 2048 game """

from .game2048 import Game2048

class Game2048Interface:
    """ main class for the interface """

    def __init__(self):
        self.game = Game2048()

    def play(self):
        """ plays the game of 2048 until it ends """

        while self.game.game_state == Game2048.GameState.ONGOING:
            self.print_board()

            try:
                move = input('Move (w/a/s/d):')

                if move == 'w':
                    self.game.player_action(Game2048.Action.UP)
                elif move == 'a':
                    self.game.player_action(Game2048.Action.LEFT)
                elif move == 's':
                    self.game.player_action(Game2048.Action.DOWN)
                elif move == 'd':
                    self.game.player_action(Game2048.Action.RIGHT)
            except ValueError:
                print('input valid value (w/a/s/d)')

    def print_board(self):
        """ prints the board of the 2048 game on the console """

        board_str = ''
        for i in range(self.game.col_size):
            board_str += str(self.game.board[i*4]) + '\t' + \
                         str(self.game.board[i*4 + 1]) + '\t' + \
                         str(self.game.board[i*4 + 2]) + '\t' + \
                         str(self.game.board[i*4 + 3]) + '\n'

        print(board_str)
