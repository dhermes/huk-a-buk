import random


CARD_VALUES = (2, 3, 4, 5, 6, 7, 8, 9, 10, 'J', 'Q', 'K', 'A')
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
        # # To test:
        # deck = random_deck()
        # for card in deck.cards:
        #     print card.pretty
        return u'%s%s' % (self.value, CARD_SUITS[self.suit])


class Deck(object):

    def __init__(self):
        self.current_index = 0
        self.cards = []
        for value in CARD_VALUES:
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
