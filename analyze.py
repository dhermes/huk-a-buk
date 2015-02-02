import argparse
import glob
import json
import os

import deck
from long_simulation import DESERIALIZED_OUTCOMES
from long_simulation import SEPARATOR


class DoNothingAnalyzer(object):

    def __call__(self, game_result):
        pass

    def post_result(self):
        pass


class AceQueenAnalyzer(object):

    def __init__(self):
        self.counts = {}

    def __call__(self, game_result):
        trump = game_result[0]
        # Unpack since we expect a single match.
        winning_bidder, = [hand for hand in game_result[1:]
                           if hand[6] != 0]

        # Last 3 are: is_dealer, won_bid, tricks
        key = tuple(winning_bidder[5:])

        # First 5 are: cards
        trump_dealt = set([card.value for card in winning_bidder[:5]
                           if card.suit == trump and card.from_original_hand])
        if trump_dealt == set(('A', 'Q')):
            self.counts[key] = self.counts.get(key, 0) + 1

    def post_result(self):
        results_by_bid = {
            2: {},
            3: {},
            4: {},
            5: {},
        }

        for key, val in self.counts.iteritems():
            _, won_bid, tricks = key
            curr_tricks = results_by_bid[won_bid]
            curr_tricks[tricks] = curr_tricks.get(tricks, 0) + 1

        print json.dumps(results_by_bid, indent=2, sort_keys=True)


def pick_filename():
    files = glob.glob('data/*.bindata')
    for i, filename in enumerate(files):
        print '%d: %s' % (i, filename)

    file_chosen = None
    while file_chosen is None:
        try:
            choice = raw_input('Which file? ')
            file_chosen = files[int(choice)]
        except (TypeError, ValueError, KeyError):
            pass

    return file_chosen


def read_game(file_handle, total_bytes):
    result = []
    separator_found = False
    while not separator_found:
        if file_handle.tell() >= total_bytes:
            break

        char = file_handle.read(1)
        if char == SEPARATOR:
            separator_found = True
        else:
            result.append(char)
    return ''.join(result)


def parse_game_line(game_line):
    num_players, remainder = divmod(len(game_line), 6)
    if remainder != 1:
        raise ValueError('Expected 6 characters per hand.')

    trump = game_line[0]
    game_line = game_line[1:]
    game_result = [trump]

    for index in range(num_players):
        cards = [deck.Card.deserialize(game_line[6 * index + i])
                 for i in xrange(5)]
        cards.extend(DESERIALIZED_OUTCOMES[game_line[6 * index + 5]])
        game_result.append(cards)

    return game_result


def read_simulation(results_file, analyze_func):
    # os.fstat(fh.fileno()).st_size
    fh = open(results_file, 'rb')
    total_bytes = os.fstat(fh.fileno()).st_size

    try:
        while fh.tell() < total_bytes:
            game_line = read_game(fh, total_bytes)
            game_result = parse_game_line(game_line)
            analyze_func(game_result)
    finally:
        fh.close()


if __name__ == '__main__':
    analyze_funcs = {
        'do_nothing_analyze': DoNothingAnalyzer,
        'analyze_ace_queen': AceQueenAnalyzer,
    }
    parser = argparse.ArgumentParser(
        description='Analyze simulated Huk-A-Buk games.',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('--filename', dest='filename',
                        help='Filename containing simulated data.')
    parser.add_argument('--analyze-func', dest='analyze_func',
                        choices=tuple(analyze_funcs.keys()),
                        default='do_nothing_analyze',
                        help='Function used to analyze simulated data.')
    args = parser.parse_args()
    filename = args.filename or pick_filename()

    analyzer = analyze_funcs[args.analyze_func]()
    read_simulation(filename, analyzer)
    analyzer.post_result()
