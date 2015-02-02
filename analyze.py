import argparse
import glob
import os

import deck
from long_simulation import DESERIALIZED_OUTCOMES
from long_simulation import SEPARATOR


def do_nothing_analyze(game_result):
    pass


def pick_filename():
    files = glob.glob('*.bindata')
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
    parser = argparse.ArgumentParser(
        description='Analyze simulated Huk-A-Buk games.')
    parser.add_argument('--filename', dest='filename',
                        help='Filename containing simulated data.')
    args = parser.parse_args()
    filename = args.filename or pick_filename()
    read_simulation(filename, do_nothing_analyze)
