''' AI wrapper for the game 2048 '''

from games.game2048.game2048 import Game2048
from agents.game2048_dqnagent import Game2048DQNAgent
from .base_ai import BaseAI


class AI2048(BaseAI):
    ''' AI wrapper for the game 2048 '''

    def __init__(self, config):
        super().__init__(config)

        self.env = Game2048()
        self.agent = Game2048DQNAgent(self.config, 16, 4)

    def play(self):
        ''' play against learnt ai '''
        pass

    def learn(self):
        ''' initiate ai learning '''
        self.agent.build_model()

        state, game_state = self.env.reset()
        batch_count = 0
        games = 0

        for i in range(self.config['Episodes']):
            while game_state != Game2048.GameState.ENDED and batch_count < self.config['BatchSize']:
                action, target = self.agent.act(state)

                # print(target)

                game_action = Game2048.Action(action)

                next_state, game_state, add_score = self.env.step(game_action)

                self.agent.remember(state, target, action,
                                    next_state, add_score, game_state)

                if game_state == Game2048.GameState.STALL:
                    available_moves = self.env.available_moves()
                    sel_move = None
                    max_val = None

                    for _, move in enumerate(available_moves):
                        pos = move.value

                        if max_val is None or target[pos] > max_val:
                            max_val = target[pos]
                            sel_move = move

                    next_state, game_state, add_score = self.env.step(sel_move)

                    self.agent.remember(state, target, action,
                                        next_state, add_score, game_state)

                state = next_state
                batch_count += 1

            if game_state == Game2048.GameState.ENDED:
                print('Game: ' + str(games) + '. Score attained: ' + str(self.env.game_score) + 'Max Tile: ' + str(self.env.get_max_tile()))

                games += 1
                state, game_state = self.env.reset()

            self.agent.learn()
            batch_count = 0

        self.agent.agent_save(self.get_model_filename())
