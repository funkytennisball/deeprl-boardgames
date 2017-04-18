""" Base implementation for a DQN Agent """

from abc import ABC, abstractmethod

import random
from collections import deque

from keras.models import Sequential, load_model
from keras.layers import Dense
from keras.optimizers import Adam

import numpy as np

from games.tictactoe.tictactoe import GameState

class BaseAgent(ABC):
    """ DQN agent, wrapper for keras """

    def __init__(self, config, input_dim, mode_learn=True):
        self.config = config
        self.model = None
        self.input_dim = input_dim
        self.mode_learn = mode_learn

        self.memory = deque(maxlen=self.config['MemoryMaxSize'])
        self.gamma = self.config['DiscountRate']

    def remember(self, state, cur_scores, action, next_state, score, game_state, game_end):
        """ Stores given state, action, next_state, game_state pair in the memory """
        self.memory.append((state, cur_scores, action, next_state, score, game_state, game_end))

    def act(self, state):
        """ DQN agent will decide on the action given a particular state """
        input_state = state.reshape(-1, self.input_dim).copy()
        act_values = self.model.predict(input_state)[0]

        return np.argmax(act_values), act_values

    def learn(self):
        """ Learns given states in memory set """
        batch_size = min(len(self.memory), self.config['BatchSize'])
        X = np.zeros((batch_size, self.input_dim))  # pylint: disable=C0103
        Y = np.zeros((batch_size, self.input_dim))  # pylint: disable=C0103

        sample = random.sample(self.memory, batch_size)

        for i, (state, target, action, next_state, score, game_state, game_end) in enumerate(sample):
            input_state = state.reshape(-1, self.input_dim).copy()
            input_next_state = next_state.reshape(-1, self.input_dim).copy()

            reward = self.get_reward(score, game_state)

            if game_end:
                target[action] = reward + self.gamma * \
                                 np.amax(self.model.predict(input_next_state)[0])
            else:
                target[action] = reward

            X[i], Y[i] = input_state, target

        self.model.fit(X, Y, batch_size=batch_size, epochs=1, verbose=0)

    @abstractmethod
    def get_reward(self, score, game_state):
        pass

    @abstractmethod
    def build_model(self):
        """ Builds ANN """
        pass

    def agent_save(self, file):
        """ Saves learned NN into given file """
        self.model.save(file)

    def agent_load(self, file):
        """ Loads NN from a given file """
        self.model = load_model(file)
