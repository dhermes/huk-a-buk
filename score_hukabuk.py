import json
import os
import time


DATA = {'turns': {}}


class Settings(object):
    FILENAME = None
    CURRENT_TURN = 0
    NAME_CHOICES = None


def set_filename():
    filename = raw_input('Set the filename? ').strip()
    if not filename:
        filename = str(int(time.time()))
    Settings.FILENAME = filename + '.json'


def save_game():
    with open(Settings.FILENAME, 'w') as fh:
        json.dump(DATA, fh)


def enter_names():
    names = {}
    while True:
        name = raw_input('Enter name: ')
        if name.strip() == '':
            break
        names[name] = -5
    DATA['names'] = names
    Settings.NAME_CHOICES = '\n'.join([
        '%d: %s' % (i, name)
        for i, name in enumerate(names.keys())
    ])
    save_game()


def game_over():
    game_over = raw_input('Is the game over? [y/n] ')
    return game_over.lower().strip() == 'y'


def get_bidder():
    actual_bidder = None
    while actual_bidder is None:
        print(Settings.NAME_CHOICES)
        bidder = raw_input('Who won the bid? ')
        try:
            bidder = int(bidder)
            actual_bidder = Settings.NAME_CHOICES[bidder]
        except:
            if bidder in Settings.NAME_CHOICES:
                actual_bidder = bidder

    return actual_bidder


def get_bid():
    actual_bid = None
    while actual_bid is None:
        bid = raw_input('Bid amount? ')
        try:
            bid = int(bid)
            if bid in (2, 3, 4, 5):
                actual_bid = bid
        except:
            pass

    return actual_bid


def get_points():
    result = {}
    print '=' * 60
    print 'Scores for turn %d:' % (Settings.CURRENT_TURN,)
    for name in DATA['names'].keys():
        msg = 'Score for %r: ' % (name,)
        actual_score = None
        while actual_score is None:
            score = raw_input(msg)
            try:
                score = int(score)
                if score in (-5, 0, 1, 2, 3, 4, 5):
                    actual_score = score
            except:
                pass

        result[name] = actual_score
        DATA['names'][name] += actual_score

    return result



def play_turn():
    turn = DATA['turns'].setdefault(Settings.CURRENT_TURN, {})
    turn['bidder'] = get_bidder()
    turn['bid'] = get_bid()
    turn['points'] = get_points()

    Settings.CURRENT_TURN += 1
    save_game()


def print_scores():
    print '=' * 60
    print 'Current scores:'
    print '-' * 60
    for name, score in DATA['names'].items():
        print '%r -> %d' % (name, score)
    print '=' * 60


def play_game():
    while not game_over():
        print_scores()
        play_turn()


def main():
    set_filename()
    enter_names()
    play_game()


if __name__ == '__main__':
    main()
