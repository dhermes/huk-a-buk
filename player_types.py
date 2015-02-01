import random

from deck import CARD_SUITS
from game_play import CARDS_PER_HAND


class RandomPlayer(object):

    MINIMUM_BID = 2
    TRUMP_CHOICES = tuple(CARD_SUITS.keys())
    RANDOM_BIDS = tuple(range(MINIMUM_BID, CARDS_PER_HAND + 1))

    def draw_cards(self, hand, unused_winning_bid):
        # `randint` is inclusive
        if hand.won_bid != 0:
            # Winner can't fold.
            num_to_draw = random.randint(0, CARDS_PER_HAND)
        else:
            # 6-9 fold, so 40% of hands will fold.
            num_to_draw = random.randint(0, 2 * CARDS_PER_HAND - 1)

        if num_to_draw > CARDS_PER_HAND:
            return None

        # Keep a random subset of cards.
        # random.sample "Chooses k unique random elements"
        hand.unplayed_cards = random.sample(
            hand.unplayed_cards, CARDS_PER_HAND - num_to_draw)

        for _ in xrange(num_to_draw):
            hand.unplayed_cards.append(hand.deck.draw_card())

        return num_to_draw

    def make_bid(self, hand, max_bid):
        trump = random.choice(self.TRUMP_CHOICES)
        if hand.is_dealer and max_bid < self.MINIMUM_BID:
            return self.MINIMUM_BID, trump

        bid_val = random.choice(self.RANDOM_BIDS)
        if bid_val > max_bid:
            return bid_val, trump
        else:
            return None, None

    def play_card(self, hand, unused_trump, unused_cards_out):
        card_to_play = random.choice(hand.unplayed_cards)
        hand.unplayed_cards.remove(card_to_play)
        hand.played_cards.append(card_to_play)
        return card_to_play
