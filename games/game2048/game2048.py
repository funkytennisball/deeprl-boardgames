""" Implementation for a 2048 game """

import random
from enum import Enum


class Game2048:
    """ base class for a 2048 game """

    class GameState(Enum):
        """ Game State of the 2048 game """
        ONGOING = 0
        ENDED = 1

    class Action(Enum):
        """ Actions representing keyboard actions """
        LEFT = 1
        UP = 2      # pylint: disable=C0103
        RIGHT = 3
        DOWN = 4

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

    def reset(self):
        """ resets the 2048 game state """
        self.game_state = Game2048.GameState.ONGOING
        self.board = [0 for i in range(self.board_size)]
        self.game_score = 0

        for _ in range(2):
            self.add_random_tile()

        return self.game_state, self.board

    def add_random_tile(self):
        """ adds a random tile on the game board with a probability of 0.9 for 2, 0.1 for 4 """
        available_tiles = self.get_available_tiles()

        if len(available_tiles) > 0:
            chosen_tile = random.choice(available_tiles)
            tile_val = 4 if random.random() < self.gen_four_prob else 2

            self.board[chosen_tile] = tile_val

    def step(self, move):
        """ process a movement from the user """
        if self.game_state != Game2048.GameState.ONGOING:
            return

        grid = [[self.board[i * 4], self.board[i * 4 + 1],
                 self.board[i * 4 + 2], self.board[i * 4 + 3]]
                for i in range(self.col_size)]

        next_grid, step_score = Game2048.process_move(grid, move)
        next_board = []

        for _, row in enumerate(next_grid):
            next_board = next_board + row

        if self.board != next_board:
            self.board = next_board

            self.add_random_tile()
            self.check_game_status()

        return self.board, self.game_state, step_score

    def check_game_status(self):
        """ checks if the game has ended """
        if len(self.get_available_tiles()) == 0:
            self.game_state = Game2048.GameState.ENDED
        else:
            self.game_state = Game2048.GameState.ONGOING

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
            next_grid = [Game2048.process_row(
                flipped_grid[i], move) for i in range(len(grid))]
            res = [[next_grid[j][i]
                    for j in range(len(grid))] for i in range(len(grid))]

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
