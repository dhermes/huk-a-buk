import random

from deck import CARD_SUITS
from game_play import CARDS_PER_HAND


ASSUMPTIONS = {
    'non_win_fold': 0.4,  # 40% chance of folding given non-winning bid.
    'bids': {
         5:  1,  #      Pr(5) = 1/100
         4:  2,  #      Pr(4) = 2/100
         3: 24,  #      Pr(3) = 24/100
         2: 48,  #      Pr(2) = 48/100
        -1: 25,  # Pr(No Bid) = 25/100
    },
}


class RandomPlayer(object):

    MINIMUM_BID = 2

    def __init__(self, random_bids=None):
        if random_bids is None:
            random_bids = (( 5,) * ASSUMPTIONS['bids'][5] +
                           ( 4,) * ASSUMPTIONS['bids'][4] +
                           ( 3,) * ASSUMPTIONS['bids'][3] +
                           ( 2,) * ASSUMPTIONS['bids'][2] +
                           (-1,) * ASSUMPTIONS['bids'][-1])

        self.random_bids = random_bids

    def draw_cards(self, hand, unused_winning_bid):
        trump = hand.game.trump
        trump_cards = [card for card in hand.unplayed_cards
                       if card.suit == trump]
        non_trump_cards = [card for card in hand.unplayed_cards
                           if card.suit != trump]
        cards_to_ditch = len(non_trump_cards)

        # `randint` is inclusive
        if hand.won_bid != 0:
            # Winner can't fold.
            num_to_draw = random.randint(0, cards_to_ditch)
        else:
            # Fold 40% of the time.
            if random.random() < ASSUMPTIONS['non_win_fold']:
                num_to_draw = CARDS_PER_HAND + 1
            else:
                num_to_draw = random.randint(0, cards_to_ditch)

        if num_to_draw > CARDS_PER_HAND:
            return None

        # Keep a random subset of cards.
        # random.sample "Chooses k unique random elements"
        hand.unplayed_cards = trump_cards + random.sample(
            non_trump_cards, cards_to_ditch - num_to_draw)

        for _ in xrange(num_to_draw):
            hand.unplayed_cards.append(hand.deck.draw_card())

        return num_to_draw

    def make_bid(self, hand, max_bid):
        hand_suits = [card.suit for card in hand.unplayed_cards]
        trump = random.choice(hand_suits)
        if hand.is_dealer and max_bid < self.MINIMUM_BID:
            return self.MINIMUM_BID, trump

        bid_val = random.choice(self.random_bids)
        if bid_val > max_bid:
            return bid_val, trump
        else:
            return None, None

    def play_card(self, hand, trump, cards_out):
        # Winning bidder must lead first hand with trump.
        if hand.won_bid != 0 and len(hand.unplayed_cards) == CARDS_PER_HAND:
            matching_cards = [card for card in hand.unplayed_cards
                              if card.suit == trump]
            if len(matching_cards) == 0:
                raise ValueError('Winning bid has no trump. What the hell!')
            card_to_play = random.choice(matching_cards)
        elif cards_out:
            matching_cards = [card for card in hand.unplayed_cards
                              if card.suit == cards_out[0].suit]
            # Follow suit if you can.
            if matching_cards:
                card_to_play = random.choice(matching_cards)
            else:
                card_to_play = random.choice(hand.unplayed_cards)
        else:
            card_to_play = random.choice(hand.unplayed_cards)

        hand.unplayed_cards.remove(card_to_play)
        hand.played_cards.append(card_to_play)
        return card_to_play
