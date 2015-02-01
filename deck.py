import random


CARD_VALUES = {
    2: 2,
    3: 3,
    4: 4,
    5: 5,
    6: 6,
    7: 7,
    8: 8,
    9: 9,
    10: 10,
    'J': 11,
    'Q': 12,
    'K': 13,
    'A': 14,
}
CARD_SUITS = {
    'H': u'\u2665',
    'S': u'\u2660',
    'C': u'\u2663',
    'D': u'\u2666',
}


class Card(object):

    def __init__(self, suit, value):
        self.suit = suit
        self.value = value
        self._validate()

    def _validate(self):
        if self.value not in CARD_VALUES:
            raise ValueError('Bad card value', self.value)
        if self.suit not in CARD_SUITS:
            raise ValueError('Bad card suit', self.suit)

    @property
    def pretty(self):
        return u'%2s%s' % (self.value, CARD_SUITS[self.suit])

    def is_better(self, other_card, trump, lead_suit):
        if self.suit == other_card.suit:
            return CARD_VALUES[self.value] > CARD_VALUES[other_card.value]

        # If the suits are different, then at most 1 is trump and at
        # most 1 is the lead suit.
        if self.suit == trump:
            return True
        elif other_card.suit == trump:
            return False

        if self.suit == lead_suit:
            return True
        elif other_card.suit == lead_suit:
            return False

        # If neither card is one of the relevant suits, their comparison
        # is irrelevant, but `self` is certainly not `is_better`.
        return False


class Deck(object):

    def __init__(self):
        self.current_index = 0
        self.cards = []
        for value in CARD_VALUES.keys():
            for suit in CARD_SUITS.keys():
                new_card = Card(suit, value)
                self.cards.append(new_card)

    def shuffle(self):
        random.shuffle(self.cards)
        self.current_index = 0

    def draw_card(self):
        result = self.cards[self.current_index]
        self.current_index += 1
        return result


def random_deck():
    deck = Deck()
    deck.shuffle()
    return deck
