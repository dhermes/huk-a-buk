CARDS_PER_HAND = 5


class Game(object):

    def __init__(self, deck, players):
        self.deck = deck
        self.players = players

        self.hands = []
        for player in players:
            self.hands.append(PlayerHand(self.deck, player))

        for _ in xrange(CARDS_PER_HAND):
            for hand in self.hands:
                hand.take_from_dealer()


class PlayerHand(object):

    def __init__(self, deck, player):
        self.deck = deck
        self.player = player
        # Set the cards.
        self.played_cards = []
        self.unplayed_cards = []

    def take_from_dealer(self):
        card = self.deck.draw_card()
        self.unplayed_cards.append(card)
        if len(self.unplayed_cards) > CARDS_PER_HAND:
            raise ValueError('Too many cards')

    def bid(self):
        return self.player.make_bid(self)

    def draw(self):
        """Determines if hand will play and draws if in.

        - Returns None if the player is folding.
        - Returns the number of cards played if playing.
        - If playing, updates "unplayed_cards".
        """
        return self.player.draw_cards(self)

    def play(self, trump, cards_out):
        return self.player.play_card(self, trump, cards_out)
