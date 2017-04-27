""" Base implementation for a DQN Agent """

from abc import ABC, abstractmethod

import math
import random
import operator
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
        self.discount_rate = self.config['DiscountRate']
        self.batch_size = self.config['BatchSize']
        self.exploration_strategy = self.config['ExplorationStrategy']

        if self.exploration_strategy == 'softmax':
            assert self.config['ComputationalTemperature'] is not None
            self.temperature = self.config['ComputationalTemperature']
        elif self.exploration_strategy == 'egreedy':
            assert self.config['EpsilonMin'] is not None
            assert self.config['EpsilonDecay'] is not None

            self.epsilon = 1.0
            self.epsilon_min = self.config['EpsilonMin']
            self.epsilon_decay = self.config['EpsilonDecay']
        else:
            raise ValueError('Invalid strategy specified')

        self.learn_itr = 0
        self.epsilon = 1.0

    def remember(self, state, action, next_state, reward, game_state):
        """ Stores given state, action, next_state, game_state pair in the memory """
        self.memory.append(
            (state, action, next_state, reward, game_state))

    def act(self, state, available_moves):
        """ DQN agent will decide on the action given a particular state """
        input_state = np.array([state])
        act_values = self.model.predict(input_state)[0]

        if self.mode_learn:
            if self.exploration_strategy == 'softmax':
                return self._act_softmax(act_values, available_moves)
            elif self.exploration_strategy == 'egreedy':
                return self._act_egreedy(act_values, available_moves)
            else:
                raise ValueError('Invalid strategy specified')
        else:
            move, _ = max([(i, val) for i, val in enumerate(
                act_values) if i in available_moves], key=operator.itemgetter(1))
            return move, act_values

    def _act_softmax(self, act_values, available_moves):
        pow_act_values = [
            (i, math.exp(val / self.temperature)) for i, val in enumerate(act_values) if i in available_moves]
        sum_act_values = sum(act_value for (
            _, act_value) in pow_act_values)
        adj_act_values = [(move, act_value / sum_act_values)
                          for (move, act_value) in pow_act_values]

        rand_sel = random.random()
        cumulative = 0
        for (move, act_value) in adj_act_values:
            cumulative += act_value
            if rand_sel <= cumulative:
                return move, act_values

    def _act_egreedy(self, act_values, available_moves):
        if random.random() <= self.epsilon:
            return random.choice(available_moves), act_values

        return np.argmax(act_values), act_values

    def learn(self):
        """ Learns given states in memory set """
        if self.learn_itr < self.batch_size:
            self.learn_itr += 1
            return
        else:
            self.learn_itr = 0

        batch_size = min(len(self.memory), self.batch_size)
        sample = random.sample(self.memory, batch_size)

        X = np.zeros((batch_size, self.input_dim))  # pylint: disable=C0103
        Y = np.zeros((batch_size, self.output_dim))  # pylint: disable=C0103

        for i, (state, action, next_state, score, game_state) in enumerate(sample):
            input_state = np.array([state])
            input_next_state = np.array([next_state])

            target = self.model.predict(input_state)[0]
            reward = self.get_reward(score, game_state)

            target[action] = self.compute_target(
                reward, game_state, input_next_state)

            X[i], Y[i] = input_state, target

        self.model.fit(X, Y, batch_size=batch_size, epochs=1, verbose=0)

        if self.exploration_strategy == 'egreedy':
            if self.epsilon > self.epsilon_min:
                self.epsilon *= self.epsilon_decay

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
