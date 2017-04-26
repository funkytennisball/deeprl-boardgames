""" DQN Agent for the 2048 Game """

from keras.models import Sequential
from keras.layers import Dense
from keras.optimizers import Adam
from keras.layers.advanced_activations import LeakyReLU

import numpy as np

from .base_agent import BaseAgent
from games.game2048.game2048 import Game2048


class Game2048DQNAgent(BaseAgent):
    """ DQN Agent for the 2048 Game """

    def __init__(self, config, input_dim, output_dim, mode_learn=True):
        super().__init__(config, input_dim, output_dim, mode_learn)

    def build_model(self):
        """ Builds ANN """
        self.model = Sequential()
        self.model.add(
            Dense(16, input_dim=self.input_dim, activation='linear'))
        self.model.add(LeakyReLU(alpha=.001))
        self.model.add(Dense(16, activation='linear'))
        self.model.add(LeakyReLU(alpha=.001))
        self.model.add(Dense(16, activation='linear'))
        self.model.add(LeakyReLU(alpha=.001))
        self.model.add(Dense(self.output_dim, activation='linear'))
        self.model.add(LeakyReLU(alpha=.001))
        self.model.compile(loss='mse', optimizer=Adam(
            lr=self.config['LearningRate']))

    def act(self, state, available_moves):
        max_val = max(state)
        conv_state = [val / max_val for val in state]

        return super().act(conv_state, available_moves)

    def remember(self, state, cur_scores, action, next_state, score, game_state):
        curstate_max = max(state)
        nextstate_max = max(next_state)

        conv_curstate = [val / curstate_max for val in state]
        conv_nextstate = [val / nextstate_max for val in next_state]

        super().remember(conv_curstate, cur_scores, action,
                         conv_nextstate, score, game_state)

    def get_reward(self, score, game_state):
        if game_state == Game2048.GameState.ENDED:
            return score/1024
        else:
            return score/512

    def compute_target(self, reward, game_state, input_next_state):
        if game_state != Game2048.GameState.ENDED:
            return reward + self.gamma * \
                np.amax(self.model.predict(input_next_state)[0])
        else:
            return reward
