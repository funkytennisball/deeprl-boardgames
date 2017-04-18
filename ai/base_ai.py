''' Base class for all game AIs '''

from abc import ABC, abstractmethod


class BaseAI(ABC):
    ''' AI base classes '''

    def __init__(self, config):
        self.config = config

    def get_model_filename(self):
        """ gets the file name of the saved model file """
        return 'data/' + self.config['SaveFile']

    @abstractmethod
    def play(self):
        ''' base method for play. Used to play defined game with AI '''
        pass

    @abstractmethod
    def learn(self):
        ''' base method for ai to learn a defined game '''
        pass
