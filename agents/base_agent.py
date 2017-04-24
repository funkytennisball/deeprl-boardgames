""" Base implementation for a DQN Agent """

from abc import ABC, abstractmethod

import random
from collections import deque

from keras.models import load_model

import numpy as np


class BaseAgent(ABC):
    """ DQN agent, wrapper for keras """

    def __init__(self, config, input_dim, output_dim, mode_learn=True):
        self.config = config
        self.model = None
        self.input_dim = input_dim
        self.output_dim = output_dim
        self.mode_learn = mode_learn

        self.memory = deque(maxlen=self.config['MemoryMaxSize'])
        self.gamma = self.config['DiscountRate']

    def remember(self, state, cur_scores, action, next_state, score, game_state):
        """ Stores given state, action, next_state, game_state pair in the memory """
        self.memory.append(
            (state, cur_scores, action, next_state, score, game_state))

    def act(self, state):
        """ DQN agent will decide on the action given a particular state """
        input_state = np.array([state])
        act_values = self.model.predict(input_state)[0]

        return np.argmax(act_values), act_values

    def learn(self):
        """ Learns given states in memory set """
        batch_size = min(len(self.memory), self.config['BatchSize'])
        X = np.zeros((batch_size, self.input_dim))  # pylint: disable=C0103
        Y = np.zeros((batch_size, self.output_dim))  # pylint: disable=C0103

        sample = random.sample(self.memory, batch_size)

        for i, (state, target, action, next_state, score, game_state) in enumerate(sample):
            input_state = np.array([state])
            input_next_state = np.array([next_state])

            reward = self.get_reward(score, game_state)
            target[action] = self.compute_target(reward, game_state, input_next_state)

            X[i], Y[i] = input_state, target

        self.model.fit(X, Y, batch_size=batch_size, epochs=1, verbose=0)

    @abstractmethod
    def compute_target(self, reward, game_state, input_next_state):
        pass

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
