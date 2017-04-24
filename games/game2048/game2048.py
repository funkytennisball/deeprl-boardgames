""" Implementation for a 2048 game """

import random
from enum import Enum


class Game2048:
    """ base class for a 2048 game """

    class GameState(Enum):
        """ Game State of the 2048 game """
        ONGOING = 0
        ENDED = 1
        STALL = 2

    class Action(Enum):
        """ Actions representing keyboard actions """
        LEFT = 0
        UP = 1      # pylint: disable=C0103
        RIGHT = 2
        DOWN = 3

    def __init__(self):
        # Parameters
        self.start_tiles = 2
        self.board_size = 16
        self.col_size = 4
        self.gen_four_prob = 0.1

        # Objects
        self.board = []
        self.game_state = None
        self.game_score = 0

        # Initialization
        self.reset()

    def __str__(self):
        board_str = ''
        for i in range(self.col_size):
            board_str += str(self.board[i * 4]) + '\t' + \
                str(self.board[i * 4 + 1]) + '\t' + \
                str(self.board[i * 4 + 2]) + '\t' + \
                str(self.board[i * 4 + 3]) + '\n'

        return board_str

    def reset(self):
        """ resets the 2048 game state """
        self.game_state = Game2048.GameState.ONGOING
        self.board = [0 for i in range(self.board_size)]
        self.game_score = 0

        for _ in range(2):
            self.add_random_tile()

        return self.board, self.game_state

    def add_random_tile(self):
        """ adds a random tile on the game board with a probability of 0.9 for 2, 0.1 for 4 """
        available_tiles = self.get_available_tiles()

        if len(available_tiles) > 0:
            chosen_tile = random.choice(available_tiles)
            tile_val = 4 if random.random() < self.gen_four_prob else 2

            self.board[chosen_tile] = tile_val

    def step(self, move):
        """ process a movement from the user """
        if self.game_state == Game2048.GameState.ENDED:
            return

        grid = self.get_grid()

        next_grid, step_score = Game2048.process_move(grid, move)
        next_board = []

        for _, row in enumerate(next_grid):
            next_board = next_board + row

        if self.board != next_board:
            self.board = next_board
            self.game_score += step_score

            self.add_random_tile()
            self.check_game_status()
        else:
            self.game_state = Game2048.GameState.STALL

        return next_board, self.game_state, step_score

    def get_grid(self):
        """ Gets game board in grid format """
        return [[self.board[i * 4], self.board[i * 4 + 1],
                 self.board[i * 4 + 2], self.board[i * 4 + 3]]
                for i in range(self.col_size)]

    def get_max_tile(self):
        """ Gets maximum tile attained from game """
        return max(self.board)

    def check_game_status(self):
        """ checks if the game has ended """
        if self.no_moves_available():
            self.game_state = Game2048.GameState.ENDED
        else:
            self.game_state = Game2048.GameState.ONGOING

    def available_moves(self):
        """ returns all available moves """

        available_moves = []

        grid = self.get_grid()
        for move in Game2048.Action:
            next_grid, _ = Game2048.process_move(grid, move)
            if grid != next_grid:
                available_moves.append(move)

        return available_moves

    def no_moves_available(self):
        """ check if no moves are available to be executed """

        # check availability of zero tiles
        if self.get_available_tiles():
            return False

        # check if able to move horizontally
        for i in range(4):
            if self.board[4 * i] == self.board[4 * i + 1] or \
                    self.board[4 * i + 1] == self.board[4 * i + 2] or \
                    self.board[4 * i + 2] == self.board[4 * i + 3]:
                return False

        for i in range(3):
            if self.board[4 * i] == self.board[4 * i + 4] or \
                    self.board[4 * i + 1] == self.board[4 * i + 5] or \
                    self.board[4 * i + 2] == self.board[4 * i + 6] or \
                    self.board[4 * i + 3] == self.board[4 * i + 7]:
                return False

        return True

    def get_available_tiles(self):
        """ returns all the possible moves """
        return [tile for tile, val in enumerate(self.board) if val == 0]

    @staticmethod
    def process_move(grid, move):
        """ returns a grid if a particular move is applied """
        res = []

        if move == Game2048.Action.LEFT or move == Game2048.Action.RIGHT:
            res = [Game2048.process_row(row, move) for row in grid]

        elif move == Game2048.Action.UP or move == Game2048.Action.DOWN:
            flipped_grid = [[grid[j][i]
                             for j in range(len(grid))] for i in range(len(grid))]
            temp_grid = [Game2048.process_row(
                flipped_grid[i], move) for i in range(len(grid))]

            # flip grid back
            res = [([temp_grid[j][0][i] for j in range(len(grid))],
                    temp_grid[i][1]) for i in range(len(grid))]

        next_row = [val[0] for _, val in enumerate(res)]
        add_score = sum(val[1] for val in res)

        return next_row, add_score

    @staticmethod
    def process_row(row, move):
        """ processes row of 2048 """
        next_row = [0 for i in range(len(row))]
        if move == Game2048.Action.LEFT or move == Game2048.Action.UP:
            orientation = 1
        elif move == Game2048.Action.RIGHT or move == Game2048.Action.DOWN:
            orientation = -1

        movement = 0
        last_node = 0
        cur_score = 0

        for pos, _ in enumerate(row):
            accessor = int((-3 * orientation + 3) / 2)
            node = int(row[pos * orientation + accessor])
            if node == 0:
                movement += 1
            else:
                if last_node == node:
                    new_node = node * 2
                    next_row[(pos - movement - 1) *
                             orientation + accessor] = new_node
                    cur_score += new_node

                    last_node = 0
                    movement += 1
                else:
                    next_row[(pos - movement) * orientation + accessor] = node
                    last_node = node

        return next_row, cur_score
