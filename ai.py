""" Core AI Logic """

from games.tictactoe.tictactoe import Tictactoe, GameState, PlayerType
from agents.dqnagent import DQNAgent

class AI:
    """ AI Class """

    def __init__(self, config):
        self.config = config

        self.env = Tictactoe()
        self.agent = DQNAgent(self.config)
        self.game_stats = AI.init_game_stats()

    def play(self):
        """ play against learnt AI """
        self.agent.mode_learn = False
        self.agent.agent_load(self.get_model_filename())

        state, game_state = self.env.reset()

        while game_state == GameState.ONGOING:
            action, _ = self.agent.act(state)
            next_state, game_state = self.env.step(action, PlayerType.HUMAN)

            state = next_state
            print(game_state)

        print(self.env.to_printable())

    def learn(self):
        """ initiate ai learning """
        self.agent.build_model()

        for i in range(self.config['Episodes']):
            state, game_state = self.env.reset()

            while game_state == GameState.ONGOING:
                action, cur_scores = self.agent.act(state)
                next_state, game_state = self.env.step(action)
                self.agent.remember(state, cur_scores, action, next_state, game_state)

                state = next_state

            self.game_stats[game_state] += 1

            if (i + 1) % self.config['BatchSize'] == 0:
                self.agent.learn()

                print(self.game_stats)
                self.game_stats = AI.init_game_stats()

        self.agent.agent_save(self.get_model_filename())

    def get_model_filename(self):
        """ gets the file name of the saved model file """
        return 'data/' + self.config['SaveFile']

    @staticmethod
    def init_game_stats():
        """ resets the game statistics """
        return {
            GameState.DRAW: 0,
            GameState.LOSE: 0,
            GameState.WIN: 0,
        }
