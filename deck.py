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
    # Tuples of (from_original_hand, suit, value)
    (True, 'H', 2): chr(0),
    (True, 'H', 3): chr(1),
    (True, 'H', 4): chr(2),
    (True, 'H', 5): chr(3),
    (True, 'H', 6): chr(4),
    (True, 'H', 7): chr(5),
    (True, 'H', 8): chr(6),
    (True, 'H', 9): chr(7),
    (True, 'H', 10): chr(8),
    (True, 'H', 'J'): chr(9),
    (True, 'H', 'Q'): chr(10),
    (True, 'H', 'K'): chr(11),
    (True, 'H', 'A'): chr(12),
    (True, 'S', 2): chr(13),
    (True, 'S', 3): chr(14),
    (True, 'S', 4): chr(15),
    (True, 'S', 5): chr(16),
    (True, 'S', 6): chr(17),
    (True, 'S', 7): chr(18),
    (True, 'S', 8): chr(19),
    (True, 'S', 9): chr(20),
    (True, 'S', 10): chr(21),
    (True, 'S', 'J'): chr(22),
    (True, 'S', 'Q'): chr(23),
    (True, 'S', 'K'): chr(24),
    (True, 'S', 'A'): chr(25),
    (True, 'C', 2): chr(26),
    (True, 'C', 3): chr(27),
    (True, 'C', 4): chr(28),
    (True, 'C', 5): chr(29),
    (True, 'C', 6): chr(30),
    (True, 'C', 7): chr(31),
    (True, 'C', 8): chr(32),
    (True, 'C', 9): chr(33),
    (True, 'C', 10): chr(34),
    (True, 'C', 'J'): chr(35),
    (True, 'C', 'Q'): chr(36),
    (True, 'C', 'K'): chr(37),
    (True, 'C', 'A'): chr(38),
    (True, 'D', 2): chr(39),
    (True, 'D', 3): chr(40),
    (True, 'D', 4): chr(41),
    (True, 'D', 5): chr(42),
    (True, 'D', 6): chr(43),
    (True, 'D', 7): chr(44),
    (True, 'D', 8): chr(45),
    (True, 'D', 9): chr(46),
    (True, 'D', 10): chr(47),
    (True, 'D', 'J'): chr(48),
    (True, 'D', 'Q'): chr(49),
    (True, 'D', 'K'): chr(50),
    (True, 'D', 'A'): chr(51),
    (False, 'H', 2): chr(52),
    (False, 'H', 3): chr(53),
    (False, 'H', 4): chr(54),
    (False, 'H', 5): chr(55),
    (False, 'H', 6): chr(56),
    (False, 'H', 7): chr(57),
    (False, 'H', 8): chr(58),
    (False, 'H', 9): chr(59),
    (False, 'H', 10): chr(60),
    (False, 'H', 'J'): chr(61),
    (False, 'H', 'Q'): chr(62),
    (False, 'H', 'K'): chr(63),
    (False, 'H', 'A'): chr(64),
    (False, 'S', 2): chr(65),
    (False, 'S', 3): chr(66),
    (False, 'S', 4): chr(67),
    (False, 'S', 5): chr(68),
    (False, 'S', 6): chr(69),
    (False, 'S', 7): chr(70),
    (False, 'S', 8): chr(71),
    (False, 'S', 9): chr(72),
    (False, 'S', 10): chr(73),
    (False, 'S', 'J'): chr(74),
    (False, 'S', 'Q'): chr(75),
    (False, 'S', 'K'): chr(76),
    (False, 'S', 'A'): chr(77),
    (False, 'C', 2): chr(78),
    (False, 'C', 3): chr(79),
    (False, 'C', 4): chr(80),
    (False, 'C', 5): chr(81),
    (False, 'C', 6): chr(82),
    (False, 'C', 7): chr(83),
    (False, 'C', 8): chr(84),
    (False, 'C', 9): chr(85),
    (False, 'C', 10): chr(86),
    (False, 'C', 'J'): chr(87),
    (False, 'C', 'Q'): chr(88),
    (False, 'C', 'K'): chr(89),
    (False, 'C', 'A'): chr(90),
    (False, 'D', 2): chr(91),
    (False, 'D', 3): chr(92),
    (False, 'D', 4): chr(93),
    (False, 'D', 5): chr(94),
    (False, 'D', 6): chr(95),
    (False, 'D', 7): chr(96),
    (False, 'D', 8): chr(97),
    (False, 'D', 9): chr(98),
    (False, 'D', 10): chr(99),
    (False, 'D', 'J'): chr(100),
    (False, 'D', 'Q'): chr(101),
    (False, 'D', 'K'): chr(102),
    (False, 'D', 'A'): chr(103),
}
CARD_DESERIALIZE = {val: key for key, val in CARD_SERIALIZE.items()}


class Card(object):

    def __init__(self, suit, value, from_original_hand=True):
        self.suit = suit
        self.value = value
        self.from_original_hand = from_original_hand
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
        return CARD_SERIALIZE[(self.from_original_hand, self.suit, self.value)]

    @classmethod
    def deserialize(cls, char):
        from_original_hand, suit, value = CARD_DESERIALIZE[char]
        return cls(suit, value, from_original_hand=from_original_hand)


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
