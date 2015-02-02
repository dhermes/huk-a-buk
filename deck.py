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
CARD_SERIALIZE = {
    ('H', 2): chr(0),
    ('H', 3): chr(1),
    ('H', 4): chr(2),
    ('H', 5): chr(3),
    ('H', 6): chr(4),
    ('H', 7): chr(5),
    ('H', 8): chr(6),
    ('H', 9): chr(7),
    ('H', 10): chr(8),
    ('H', 'J'): chr(9),
    ('H', 'Q'): chr(10),
    ('H', 'K'): chr(11),
    ('H', 'A'): chr(12),
    ('S', 2): chr(13),
    ('S', 3): chr(14),
    ('S', 4): chr(15),
    ('S', 5): chr(16),
    ('S', 6): chr(17),
    ('S', 7): chr(18),
    ('S', 8): chr(19),
    ('S', 9): chr(20),
    ('S', 10): chr(21),
    ('S', 'J'): chr(22),
    ('S', 'Q'): chr(23),
    ('S', 'K'): chr(24),
    ('S', 'A'): chr(25),
    ('C', 2): chr(26),
    ('C', 3): chr(27),
    ('C', 4): chr(28),
    ('C', 5): chr(29),
    ('C', 6): chr(30),
    ('C', 7): chr(31),
    ('C', 8): chr(32),
    ('C', 9): chr(33),
    ('C', 10): chr(34),
    ('C', 'J'): chr(35),
    ('C', 'Q'): chr(36),
    ('C', 'K'): chr(37),
    ('C', 'A'): chr(38),
    ('D', 2): chr(39),
    ('D', 3): chr(40),
    ('D', 4): chr(41),
    ('D', 5): chr(42),
    ('D', 6): chr(43),
    ('D', 7): chr(44),
    ('D', 8): chr(45),
    ('D', 9): chr(46),
    ('D', 10): chr(47),
    ('D', 'J'): chr(48),
    ('D', 'Q'): chr(49),
    ('D', 'K'): chr(50),
    ('D', 'A'): chr(51),
}
CARD_DESERIALIZE = {val: key for key, val in CARD_SERIALIZE.items()}


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

    def serialize(self):
        return CARD_SERIALIZE[(self.suit, self.value)]

    @classmethod
    def deserialize(cls, char):
        return cls(*CARD_DESERIALIZE[char])


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
