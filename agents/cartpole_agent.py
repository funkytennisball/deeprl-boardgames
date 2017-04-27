''' DQN Agent for the 2048 Game '''

from keras.models import Sequential
from keras.layers import Dense
from keras.optimizers import RMSprop

import numpy as np

from .base_agent import BaseAgent


class CartPoleDQNAgent(BaseAgent):
    ''' DQN Agent for the 2048 Game '''

    def __init__(self, config, input_dim, output_dim, mode_learn=True):
        super().__init__(config, input_dim, output_dim, mode_learn)

    def build_model(self):
        ''' Builds ANN '''
        self.model = Sequential()
        self.model.add(
            Dense(20, input_dim=self.input_dim, activation='tanh'))
        self.model.add(Dense(20, activation='tanh'))
        self.model.add(Dense(self.output_dim, activation='linear'))
        self.model.compile(loss='mse', optimizer=RMSprop(
            lr=self.config['LearningRate']))

    def get_reward(self, score, _):
        return score

    def compute_target(self, reward, game_end, input_next_state):
        if not game_end:
            return reward + self.discount_rate * \
                np.amax(self.model.predict(input_next_state)[0])
        else:
            return reward
