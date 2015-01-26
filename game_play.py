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
        self.draw_cards()
        self.play_hands()

    def get_bids(self):
        self.winning_bid = 1  # Maximum non-bid.
        winning_index = None

        for index, hand in enumerate(self.hands):
            curr_bid, trump = hand.bid(self.winning_bid)
            if curr_bid is not None:
                if not curr_bid > self.winning_bid:
                    raise ValueError('Bids can only increase.')
                self.winning_bid = curr_bid
                self.trump = trump
                winning_index = index

        self.winning_bidder = self.hands[winning_index]
        self.winning_bidder.won_bid = True
        # Re-order so that the winning bidder is last.
        new_beginning = self.hands[winning_index + 1:]
        truncated_front = self.hands[:winning_index + 1]
        self.hands = new_beginning + truncated_front

    def draw_cards(self):
        hands_after_draw = []
        for hand in self.hands:
            cards_drawn = hand.draw(self.winning_bid)
            if cards_drawn is not None:
                hands_after_draw.append(hand)
            elif hand is self.winning_bidder:
                raise ValueError('Winning bidder must not fold')
        self.hands = hands_after_draw

    def play_hands(self):
        for _ in xrange(5):
            self.play_hand()

    def play_hand(self):
        pass


class PlayerHand(object):

    def __init__(self, deck, player):
        self.deck = deck
        self.player = player
        self.is_dealer = False
        self.won_bid = False
        # Set the cards.
        self.played_cards = []
        self.unplayed_cards = []

    def __unicode__(self):
        all_cards = self.played_cards + self.unplayed_cards
        pretty_str = ', '.join(card.pretty for card in all_cards)
        return 'PlayerHand(%s)' % (pretty_str,)

    def take_from_dealer(self):
        card = self.deck.draw_card()
        self.unplayed_cards.append(card)
        if len(self.unplayed_cards) > CARDS_PER_HAND:
            raise ValueError('Too many cards')

    def bid(self, max_bid):
        return self.player.make_bid(self, max_bid)

    def draw(self, winning_bid):
        """Determines if hand will play and draws if in.

        - Returns None if the player is folding.
        - Returns the number of cards played if playing.
        - If playing, updates "unplayed_cards".
        """
        return self.player.draw_cards(self, winning_bid)

    def play(self, trump, cards_out):
        return self.player.play_card(self, trump, cards_out)
