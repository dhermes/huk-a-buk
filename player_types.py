import random

from game_play import CARDS_PER_HAND


class RandomPlayer(object):

    MINIMUM_BID = 2
    RANDOM_BIDS = tuple(range(MINIMUM_BID, CARDS_PER_HAND + 1))

    def draw_cards(self, hand):
        num_to_draw = random.randint(0, 6)  # `randint` is inclusive
        if num_to_draw == 6:
            return None

        # Keep a random subset of cards.
        # random.sample "Chooses k unique random elements"
        hand.unplayed_cards = random.sample(
            hand.unplayed_cards, CARDS_PER_HAND - num_to_draw)

        for _ in num_to_draw:
            hand.unplayed_cards.append(hand.deck.draw_card())

        return num_to_draw

    def make_bid(self, hand, max_bid):
        if hand.is_dealer and max_bid < self.MINIMUM_BID:
            return self.MINIMUM_BID

        bid_val = random.choice(self.RANDOM_BIDS)
        if bid_val > max_bid:
            return bid_val

    def play_card(self, hand, unused_trump, unused_cards_out):
        card_to_play = random.choice(hand.unplayed_cards)
        hand.unplayed_cards.remove(card_to_play)
        hand.played_cards.append(card_to_play)
        return card_to_play
