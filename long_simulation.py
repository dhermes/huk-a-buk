import argparse
import random
import time

import deck
import game_play
from player_types import RandomPlayer


RESULTS_FILE_TMP = 'data/results-%d-%d%s.bindata'
DEFAULT_SHUFFLER = 'default_shuffler'
SEPARATOR = '|'
STATUS_UPDATE = 5 * 10**4
SERIALIZED_OUTCOMES = {
    # Tuples of (is_dealer, won_bid, tricks)
    (True, 0, 0): chr(0),
    (True, 0, 1): chr(1),
    (True, 0, 2): chr(2),
    (True, 0, 3): chr(3),
    (True, 0, 4): chr(4),
    (True, 0, 5): chr(5),
    (True, 2, 0): chr(6),
    (True, 2, 1): chr(7),
    (True, 2, 2): chr(8),
    (True, 2, 3): chr(9),
    (True, 2, 4): chr(10),
    (True, 2, 5): chr(11),
    (True, 3, 0): chr(12),
    (True, 3, 1): chr(13),
    (True, 3, 2): chr(14),
    (True, 3, 3): chr(15),
    (True, 3, 4): chr(16),
    (True, 3, 5): chr(17),
    (True, 4, 0): chr(18),
    (True, 4, 1): chr(19),
    (True, 4, 2): chr(20),
    (True, 4, 3): chr(21),
    (True, 4, 4): chr(22),
    (True, 4, 5): chr(23),
    (True, 5, 0): chr(24),
    (True, 5, 1): chr(25),
    (True, 5, 2): chr(26),
    (True, 5, 3): chr(27),
    (True, 5, 4): chr(28),
    (True, 5, 5): chr(29),
    (False, 0, 0): chr(30),
    (False, 0, 1): chr(31),
    (False, 0, 2): chr(32),
    (False, 0, 3): chr(33),
    (False, 0, 4): chr(34),
    (False, 0, 5): chr(35),
    (False, 2, 0): chr(36),
    (False, 2, 1): chr(37),
    (False, 2, 2): chr(38),
    (False, 2, 3): chr(39),
    (False, 2, 4): chr(40),
    (False, 2, 5): chr(41),
    (False, 3, 0): chr(42),
    (False, 3, 1): chr(43),
    (False, 3, 2): chr(44),
    (False, 3, 3): chr(45),
    (False, 3, 4): chr(46),
    (False, 3, 5): chr(47),
    (False, 4, 0): chr(48),
    (False, 4, 1): chr(49),
    (False, 4, 2): chr(50),
    (False, 4, 3): chr(51),
    (False, 4, 4): chr(52),
    (False, 4, 5): chr(53),
    (False, 5, 0): chr(54),
    (False, 5, 1): chr(55),
    (False, 5, 2): chr(56),
    (False, 5, 3): chr(57),
    (False, 5, 4): chr(58),
    (False, 5, 5): chr(59),
}
DESERIALIZED_OUTCOMES = {val: key for key, val in SERIALIZED_OUTCOMES.items()}


if SEPARATOR in deck.CARD_DESERIALIZE or SEPARATOR in DESERIALIZED_OUTCOMES:
    raise ValueError('Separator can not be used.')


def default_shuffler(deck):
    deck.shuffle()
    return deck


def ace_queen_shuffler(deck):
    deck.shuffle()
    # Pick a player to give A,Q of Hearts to.
    player_with_aq = random.randint(0, 4)
    # Put Ace of Hearts in position `player_with_aq` so that person gets it.
    ace_hearts, = [i for i, card in enumerate(deck.cards)
                   if card.suit == 'H' and card.value == 'A']
    if ace_hearts != player_with_aq:
        deck.cards[player_with_aq], deck.cards[ace_hearts] = (
            deck.cards[ace_hearts], deck.cards[player_with_aq])

    # Put Queen of Hearts in position (`player_with_aq` + 5) so that person
    # gets it as their second card.
    queen_hearts, = [i for i, card in enumerate(deck.cards)
                     if card.suit == 'H' and card.value == 'Q']
    if queen_hearts != player_with_aq + 5:
        deck.cards[player_with_aq + 5], deck.cards[queen_hearts] = (
            deck.cards[queen_hearts], deck.cards[player_with_aq + 5])

    return deck


def simulate(num_players=4, shuffler=default_shuffler):
    curr_deck = shuffler(deck.random_deck())
    players = [RandomPlayer() for _ in xrange(num_players)]
    game = game_play.Game(curr_deck, players)
    game.play()

    hand_vals = [game.trump]
    for hand in game.hands:
        hand_vals.extend([card.serialize() for card in hand.played_cards])
        key = (hand.is_dealer, hand.won_bid, hand.tricks)
        hand_vals.append(SERIALIZED_OUTCOMES[key])

    return ''.join(hand_vals)


def long_simulate(n, shuffler=default_shuffler):
    print 'Simulating {:,} games'.format(n)

    start = time.time()
    shuffler_str = ''
    if shuffler.__name__ != DEFAULT_SHUFFLER:
        shuffler_str = '-%s' % (shuffler.__name__,)

    results_file = RESULTS_FILE_TMP % (time.time(), n, shuffler_str)
    print 'Saving in %s.' % (results_file,)
    with open(results_file, 'wb') as fh:
        # Write the first so that separator only appears before.
        # Assumes n > 0.
        fh.write(simulate(shuffler=shuffler))
        for i in xrange(2, n + 1):
            fh.write(SEPARATOR)
            fh.write(simulate(shuffler=shuffler))

            if i % STATUS_UPDATE == 0:
                message = '{:,} iterations: {} seconds'.format(
                    i, time.time() - start)
                print message


if __name__ == '__main__':
    shuffle_funcs = {
        DEFAULT_SHUFFLER: default_shuffler,
        'ace_queen_shuffler': ace_queen_shuffler,
    }
    parser = argparse.ArgumentParser(description='Simulation Huk-A-Buk.')
    parser.add_argument('--num-games', dest='num_games', type=int,
                        required=True, help='Number of games to simulate.')
    parser.add_argument('--shuffler', dest='shuffler',
                        choices=tuple(shuffle_funcs.keys()),
                        default=DEFAULT_SHUFFLER,
                        help='Shuffler to use for simulation.')
    args = parser.parse_args()

    shuffler = shuffle_funcs[args.shuffler]
    long_simulate(args.num_games, shuffler=shuffler)
