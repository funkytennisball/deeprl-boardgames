""" plays the game of 2048 as a human player """

from games.game2048.game2048_interface import Game2048Interface

if __name__ == "__main__":
    INTERFACE = Game2048Interface()
    INTERFACE.play()
