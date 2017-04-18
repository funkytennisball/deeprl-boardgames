''' AI wrapper for the game 2048 '''

from games.game2048.game2048 import Game2048
from agents.dqnagent import DQNAgent
from .base_ai import BaseAI


class AI2048(BaseAI):
    ''' AI wrapper for the game 2048 '''

    def __init__(self, config):
        super().__init__(config)

        self.env = Game2048()
        self.agent = DQNAgent(self.config)

    def play(self):
        ''' play against learnt ai '''
        pass

    def learn(self):
        ''' initiate ai learning '''
        self.agent.build_model()

        for i in range(self.config['Episodes']):
            state, game_state = self.env.reset()

            while game_state == Game2048.GameState.ONGOING:
                action, cur_scores = self.agent.act(state)
                next_state, game_state, add_score = self.env.step(action)
                self.agent.remember(state, cur_scores, action,
                                    next_state, add_score, game_state)

                state = next_state

            if (i + 1) % self.config['BatchSize'] == 0:
                self.agent.learn()

        self.agent.agent_save(self.get_model_filename())
