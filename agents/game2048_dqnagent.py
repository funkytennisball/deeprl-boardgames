""" DQN Agent for the 2048 Game """

from keras.models import Sequential
from keras.layers import Dense
from keras.optimizers import Adam

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
        self.model.add(Dense(512, input_dim=self.input_dim, activation='sigmoid'))
        self.model.add(Dense(128, activation='sigmoid'))
        self.model.add(Dense(16, activation='sigmoid'))
        self.model.add(Dense(self.output_dim, activation='sigmoid'))

        self.model.compile(loss='mse', optimizer=Adam(
            lr=self.config['LearningRate']))

    def get_reward(self, score, game_state):
        if game_state == Game2048.GameState.ENDED:
            return -1
        else:
            return score

    def compute_target(self, reward, game_state, input_next_state):
        if game_state != Game2048.GameState.ENDED:
            return reward + self.gamma * \
                np.amax(self.model.predict(input_next_state)[0])
        else:
            return reward

