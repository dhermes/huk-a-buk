from deck import random_deck
from player import Game
from player import RandomPlayer


def simulate(num_players=4):
    curr_deck = random_deck()
    players = [RandomPlayer() for _ in xrange(num_players)]
    game = Game(curr_deck, players)
    return game
