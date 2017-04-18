""" Tic Tac Toe Class """

import random

from enum import Enum

import numpy as np

class GameState(Enum):
    """ Current state of a tic tac toe game """
    ONGOING = 0
    DRAW = 1
    WIN = 2
    LOSE = 3

class Cell(Enum):
    """ Cell Values of a tic tac toe game """
    EMPTY = 0
    O = 1   # pylint: disable=C0103
    X = -1   # pylint: disable=C0103

class PlayerType(Enum):
    """ Types of player facing against """
    RANDOM = 0
    HUMAN = 1

class Tictactoe:
    """ Environment for the game Tic Tac Toe """

    def __init__(self):
        self.layout = None
        self.game_state = GameState.ONGOING
        self.main_player = Cell.O.value
        self.next_player = Cell.X.value

        self.reset()

    def reset(self):
        """ resets the layout of the board """

        self.layout = np.full(9, Cell.EMPTY.value, dtype=int)
        self.game_state = GameState.ONGOING

        return self.layout.copy(), self.game_state

    def check_game_state(self):
        """ checks if the current game has ended """

        if (self.layout[0] == self.layout[1] == self.layout[2] != Cell.EMPTY.value) or \
           (self.layout[3] == self.layout[4] == self.layout[5] != Cell.EMPTY.value) or \
           (self.layout[6] == self.layout[7] == self.layout[8] != Cell.EMPTY.value) or \
           (self.layout[0] == self.layout[3] == self.layout[6] != Cell.EMPTY.value) or \
           (self.layout[1] == self.layout[4] == self.layout[7] != Cell.EMPTY.value) or \
           (self.layout[2] == self.layout[5] == self.layout[8] != Cell.EMPTY.value) or \
           (self.layout[0] == self.layout[4] == self.layout[8] != Cell.EMPTY.value) or \
           (self.layout[2] == self.layout[4] == self.layout[6] != Cell.EMPTY.value):
            return GameState.WIN

        available_moves = [pos for pos, cell in enumerate(self.layout) if cell == Cell.EMPTY.value]
        if len(available_moves) == 0:
            return GameState.DRAW

        return GameState.ONGOING

    def nextplayer_move(self, move_type):
        """ determines the next player's move based on the player type """
        if move_type == PlayerType.RANDOM:
            return self.random_move()
        else:
            return self.player_move()

    def player_move(self):
        """ player move """
        print(self.to_printable())

        available_moves = [pos for pos, cell in enumerate(self.layout) if cell == Cell.EMPTY.value]

        move = 0

        while True:
            try:
                move = int(input('Move:'))
                if 0 <= move <= 8 and (move in available_moves):
                    break
            except ValueError:
                print('input valid value from 0 to 8')

        return move

    def random_move(self):
        """ selects a random move given a state """

        available_moves = [pos for pos, cell in enumerate(self.layout) if cell == Cell.EMPTY.value]
        return random.choice(available_moves)

    def step(self, action, move_type=PlayerType.RANDOM):
        """ Simulates a step in a game of tictactoe

        # Arguments
            action: integer from 0 to 8

        # Returns
            next_state: subsequent state given an action
            game_state: current state of the game
        """

        if self.layout[action] != Cell.EMPTY.value:
            return self.layout.copy(), self.game_state

        self.layout[action] = self.main_player
        new_game_state = self.check_game_state()

        if new_game_state != GameState.ONGOING:
            self.game_state = new_game_state

            return self.layout.copy(), self.game_state
        else:
            nextplayer_action = self.nextplayer_move(move_type)

            self.layout[nextplayer_action] = self.next_player

            next_game_state = self.check_game_state()

            if next_game_state == GameState.WIN:
                self.game_state = GameState.LOSE
            elif next_game_state == GameState.DRAW:
                self.game_state = GameState.DRAW
            else:
                self.game_state = GameState.ONGOING

            return self.layout.copy(), self.game_state

    def to_printable(self):
        """ Converts gameboard to a printable string """
        printable = ''

        for i in range(9):
            if self.layout[i] == Cell.O.value:
                printable += 'O '
            elif self.layout[i] == Cell.X.value:
                printable += 'X '
            else:
                printable += '  '

            if (i+1)%3 == 0:
                printable += '\n'
            else:
                printable += '|'

        return printable
