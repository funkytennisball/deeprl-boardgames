""" DQN Agent for the 2048 Game """

from keras.models import Sequential
from keras.layers import Dense
from keras.optimizers import Adam

import numpy as np

from .base_agent import BaseAgent
from games.game2048.game2048 import Game2048

class Game2048DQNAgent(BaseAgent):
    """ DQN Agent for the 2048 Game """

    def __init__(self, config, input_dim, mode_learn=True):
        super().__init__(config, input_dim, mode_learn)

    def build_model(self):
        """ Builds ANN """
        self.model = Sequential()
        self.model.add(Dense(16, input_dim=self.input_dim, activation='relu'))
        self.model.add(Dense(16, activation='relu'))
        self.model.add(Dense(16, activation='relu'))
        self.model.add(Dense(4, activation='relu'))

        self.model.compile(loss='mse', optimizer=Adam(
            lr=self.config['LearningRate']))

    def act(self, state):
        action, act_values = super().act(state)
        return Game2048.Action(action), act_values

    def get_reward(self, score, game_state):
        if game_state == Game2048.GameState.ENDED:
            return score * (-1)
        else:
            return score

    def compute_target(self, reward, game_state, input_next_state):
        if game_state == Game2048.GameState.ENDED:
            return reward + self.gamma * \
                np.amax(self.model.predict(input_next_state)[0])
        else:
            return reward

