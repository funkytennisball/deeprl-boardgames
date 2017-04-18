""" DQN agent, wrapper for keras """

import random
from collections import deque

from keras.models import Sequential, load_model
from keras.layers import Dense
from keras.optimizers import Adam

import numpy as np

from games.tictactoe.tictactoe import GameState

class DQNAgent:
    """ DQN agent, wrapper for keras """

    def __init__(self, config, mode_learn=True):
        self.config = config
        self.model = None
        self.mode_learn = mode_learn

        self.gamma = self.config['DiscountRate']

        self.memory = deque(maxlen=self.config['MemoryMaxSize'])
        self.input_dim = self.config['InputDimension']

        self.epsilon = 1.0  # exploration rate
        self.e_decay = .99
        self.e_min = 0.05

    def build_model(self):
        """ Builds ANN """
        self.model = Sequential()
        self.model.add(Dense(9, input_dim=self.input_dim, activation='relu'))
        self.model.add(Dense(9, activation='relu'))
        self.model.add(Dense(9, activation='relu'))
        self.model.add(Dense(9, activation='relu'))

        self.model.compile(loss='mse', optimizer=Adam(lr=self.config['LearningRate']))

    def act(self, state):
        """ DQN agent will decide on the action given a particular state """
        input_state = state.reshape(-1, 9).copy()
        act_values = self.model.predict(input_state)[0]

        available_moves = DQNAgent.get_available_moves(state)
        available_scores = [act_values[move] for move in available_moves]

        move_index = np.argmax(available_scores)

        if random.random() <= self.epsilon and self.mode_learn:
            return random.choice(available_moves), act_values
        else:
            return available_moves[move_index], act_values

    def remember(self, state, cur_scores, action, next_state, game_state,):
        """ Stores given state, action, next_state, game_state pair in the memory """
        self.memory.append((state, cur_scores, action, next_state, game_state))

    def learn(self):
        """ Learns given states in memory set """
        batch_size = min(len(self.memory), self.config['BatchSize'])
        X = np.zeros((batch_size, self.input_dim))  # pylint: disable=C0103
        Y = np.zeros((batch_size, self.input_dim))  # pylint: disable=C0103

        sample = random.sample(self.memory, batch_size)

        for i, (state, target, action, next_state, game_state) in enumerate(sample):
            input_state = state.reshape(-1, 9).copy()
            input_next_state = next_state.reshape(-1, 9).copy()

            reward = DQNAgent.tictactoe_reward(game_state)

            if game_state == GameState.ONGOING:
                target[action] = reward + self.gamma * \
                                 np.amax(self.model.predict(input_next_state)[0])
            else:
                target[action] = reward

            X[i], Y[i] = input_state, target

        self.model.fit(X, Y, batch_size=batch_size, epochs=1, verbose=0)

        if self.epsilon > self.e_min and self.mode_learn:
            self.epsilon *= self.e_decay

    @staticmethod
    def get_available_moves(state):
        return [i for i, val in enumerate(state) if val == 0]

    def agent_save(self, file):
        self.model.save(file)

    def agent_load(self, file):
        self.model = load_model(file)

    @staticmethod
    def tictactoe_reward(game_state):
        """ returns the reward given for a given game state """
        if game_state == GameState.ONGOING:
            return 0
        elif game_state == GameState.WIN:
            return 1.0
        elif game_state == GameState.LOSE:
            return -1.0
        else:
            return 1.0
