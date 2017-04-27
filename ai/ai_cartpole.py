''' AI wrapper for the game cartpole '''

import copy
import gym
from .base_ai import BaseAI
from agents.cartpole_agent import CartPoleDQNAgent


class AICartPole(BaseAI):
    ''' AI wrapper for the game cartpole '''

    def __init__(self, config, mode_learn=True):
        super().__init__(config)

        self.env = None
        self.agent = None

    def learn(self):
        ''' episodically learns the game of cartpole '''
        self.env = gym.make('CartPole-v0')

        self.agent = CartPoleDQNAgent(self.config, 4, 2)
        self.agent.build_model()

        episodes = self.config['Episodes']
        render_environment = self.config['RenderEnvironment']

        for episode in range(episodes):
            # Reset environment
            state = self.env.reset()
            game_end = False
            time_step = 0
            action_space = [i for i in range(self.env.action_space.n)]

            while not game_end:
                # Renders environment
                if render_environment:
                    self.env.render()

                action, _ = self.agent.act(state, action_space)
                next_state, reward, game_end, _ = self.env.step(action)

                self.agent.remember(state, action, next_state, reward, game_end)
                state = copy.deepcopy(next_state)

                time_step += 1

                if game_end:
                    print('Episode {:d} finished after {:d} timesteps'.format(
                        episode, time_step))

                self.agent.learn()

    def move(self):
        pass
