CARDS_PER_HAND = 5


class Game(object):

    def __init__(self, deck, players):
        self.hands = []
        for player in players:
            self.hands.append(PlayerHand(deck, player))

        # Make the last hand the dealer.
        self.hands[-1].is_dealer = True

        for _ in xrange(CARDS_PER_HAND):
            for hand in self.hands:
                hand.take_from_dealer()

    def play(self):
        self.get_bids()

    def get_bids(self):
        self.winning_bid = 1  # Maximum non-bid.
        self.winning_bidder = None

        for hand in self.hands:
            curr_bid = hand.bid(self.winning_bid)
            if curr_bid is not None:
                if not curr_bid > self.winning_bid:
                    raise ValueError('Bids can only increase.')
                self.winning_bid = curr_bid
                self.winning_bidder = hand


class PlayerHand(object):

    def __init__(self, deck, player):
        self.deck = deck
        self.player = player
        self.is_dealer = False
        # Set the cards.
        self.played_cards = []
        self.unplayed_cards = []

    def take_from_dealer(self):
        card = self.deck.draw_card()
        self.unplayed_cards.append(card)
        if len(self.unplayed_cards) > CARDS_PER_HAND:
            raise ValueError('Too many cards')

    def bid(self, max_bid):
        return self.player.make_bid(self, max_bid)

    def draw(self):
        """Determines if hand will play and draws if in.

        - Returns None if the player is folding.
        - Returns the number of cards played if playing.
        - If playing, updates "unplayed_cards".
        """
        return self.player.draw_cards(self)

    def play(self, trump, cards_out):
        return self.player.play_card(self, trump, cards_out)
