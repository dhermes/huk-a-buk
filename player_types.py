import random

from game_play import CARDS_PER_HAND


class RandomPlayer(object):

    RANDOM_BIDS = tuple(range(2, CARDS_PER_HAND + 1))

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

    def make_bid(self, unused_hand):
        return random.choice(self.RANDOM_BIDS)

    def play_card(self, hand, unused_trump, unused_cards_out):
        card_to_play = random.choice(hand.unplayed_cards)
        hand.unplayed_cards.remove(card_to_play)
        hand.played_cards.append(card_to_play)
        return card_to_play
