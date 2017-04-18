""" DQN Agent for the 2048 Game """

import random

from keras.models import Sequential
from keras.layers import Dense
from keras.optimizers import Adam

import numpy as np

from .base_agent import BaseAgent


class Game2048DQNAgent(BaseAgent):
    """ DQN Agent for the 2048 Game """

    def __init__(self, config, input_dim, mode_learn):
        super().__init__(self, config, input_dim, mode_learn)

    def build_model(self):
        """ Builds ANN """
        self.model = Sequential()
        self.model.add(Dense(16, input_dim=self.input_dim, activation='relu'))
        self.model.add(Dense(16, activation='relu'))
        self.model.add(Dense(16, activation='relu'))
        self.model.add(Dense(16, activation='relu'))

        self.model.compile(loss='mse', optimizer=Adam(
            lr=self.config['LearningRate']))

    def get_reward(self, score, game_state):
        pass
