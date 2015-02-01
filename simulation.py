from deck import random_deck
import game_play
from player_types import RandomPlayer


game_play.DEBUG = True


def simulate(num_players=4):
    curr_deck = random_deck()
    players = [RandomPlayer() for _ in xrange(num_players)]
    game = game_play.Game(curr_deck, players)
    game.play()


if __name__ == '__main__':
    simulate()
