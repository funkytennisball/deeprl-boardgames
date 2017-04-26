''' AI wrapper for the game 2048 '''

import time

from games.game2048.game2048 import Game2048
from agents.game2048_dqnagent import Game2048DQNAgent
from .base_ai import BaseAI


class AI2048(BaseAI):
    ''' AI wrapper for the game 2048 '''

    def __init__(self, config, mode_learn=True):
        super().__init__(config)

        self.env = None
        self.agent = Game2048DQNAgent(self.config, 16, 4, mode_learn)

    def load(self):
        ''' loads previously learnt data '''
        self.agent.agent_load(self.get_model_filename())

    def play(self, game_env):
        ''' setups game environment for play '''
        self.env = game_env

    def move(self):
        ''' determines a move given a 2048 board '''
        available_moves = [move.value for move in self.env.available_moves()]
        _, target = self.agent.act(self.env.board, available_moves)

        available_moves = self.env.available_moves()
        sel_move = None
        max_val = None

        for _, move in enumerate(available_moves):
            pos = move.value

            if max_val is None or target[pos] > max_val:
                max_val = target[pos]
                sel_move = move

        return sel_move

    def learn(self):
        ''' initiate ai learning '''
        self.env = Game2048()
        self.agent.build_model()

        state, game_state = self.env.reset()
        batch_count = 0
        games = 0
        sum_score = 0
        max_tile = 0
        generation_count = self.config['Generation']

        for i in range(self.config['Episodes']):
            while game_state != Game2048.GameState.ENDED:
                available_moves = [
                    move.value for move in self.env.available_moves()]
                action, target = self.agent.act(state, available_moves)
                game_action = Game2048.Action(action)

                next_state, game_state, add_score = self.env.step(game_action)

                if game_state == Game2048.GameState.ENDED:
                    self.agent.remember(state, target, action,
                                        next_state, self.env.game_score, game_state)
                else:
                    self.agent.remember(state, target, action,
                                        next_state, add_score, game_state)
                state = next_state
                batch_count += 1

            if game_state == Game2048.GameState.ENDED:
                if (games - 1) % generation_count == 0:
                    print('Generation: ' + str((games - 1) / generation_count) + '. Score attained: ' +
                          str(sum_score / generation_count) + ' Max Tile: ' + str(max_tile))

                    sum_score = 0
                    max_tile = 0

                games += 1
                sum_score += self.env.game_score
                max_tile = max(max_tile, self.env.get_max_tile())
                state, game_state = self.env.reset()

                self.agent.learn()
            batch_count = 0

        self.agent.agent_save(self.get_model_filename())
