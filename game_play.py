from deck import CARD_SUITS


CARDS_PER_HAND = 5
SEPARATOR = '=' * 60
DEBUG = False


def print_method(value):
    if DEBUG:
        print(value)


def reorder_for_hand(hands, hand, make_last=False):
    matching_indices = [i for i, curr_hand in enumerate(hands)
                        if curr_hand is hand]
    if len(matching_indices) != 1:
        raise ValueError('Not exactly one matching hand.')

    if make_last:
        index = matching_indices[0] + 1
    else:
        index = matching_indices[0]

    return hands[index:] + hands[:index]


class Game(object):

    def __init__(self, deck, players):
        self.hands = []
        for i, player in enumerate(players):
            hand_name = chr(i + 65)
            self.hands.append(PlayerHand(self, deck, player,
                                         hand_name=hand_name))

        # Make the last hand the dealer.
        self.hands[-1].is_dealer = True

        for _ in xrange(CARDS_PER_HAND):
            for hand in self.hands:
                hand.take_from_dealer()

    def play(self):
        self.get_bids()
        self.draw_cards()
        self.play_tricks()

    def get_bids(self):
        self.winning_bid = 1  # Maximum non-bid.
        winning_index = None

        for index, hand in enumerate(self.hands):
            curr_bid, trump = hand.bid(self.winning_bid)
            if curr_bid is not None:
                print_method('Player %s bids %d.' % (hand, curr_bid))
                if not curr_bid > self.winning_bid:
                    raise ValueError('Bids can only increase.')
                self.winning_bid = curr_bid
                self.trump = trump
                winning_index = index
            else:
                print_method('Player %s does not bid.' % (hand,))

        self.winning_bidder = self.hands[winning_index]
        self.winning_bidder.won_bid = self.winning_bid
        # Re-order so that the winning bidder is last.
        self.hands = reorder_for_hand(self.hands, self.winning_bidder,
                                      make_last=True)
        message = ('%s won bid with %d tricks. Trump is %s.' % (
            self.winning_bidder, self.winning_bid, CARD_SUITS[self.trump]))
        print_method(message)

    def draw_cards(self):
        print_method(SEPARATOR)
        hands_after_draw = []
        for hand in self.hands:
            cards_drawn = hand.draw(self.winning_bid)
            if cards_drawn is not None:
                hands_after_draw.append(hand)
                print_method('Hand %s takes %d cards.' % (hand.pretty,
                                                          cards_drawn))
            elif hand is self.winning_bidder:
                raise ValueError('Winning bidder must not fold')
            else:
                print_method('Hand %s folds.' % (hand.pretty,))
        self.hands = hands_after_draw

        # Re-order so that the winning bidder plays first.
        self.hands = reorder_for_hand(self.hands, self.winning_bidder,
                                      make_last=False)

    def play_tricks(self):
        print_method(SEPARATOR)
        for i in xrange(5):
            print_method('Trick %d:' % (i + 1,))
            self.play_trick()
            print_method(SEPARATOR)

        for hand in self.hands:
            if hand.won_bid != 0:
                print_method('%s finished with %d tricks after bidding %d.' % (
                    hand, hand.tricks, hand.won_bid))
            else:
                print_method('%s finished with %d tricks.' % (hand,
                                                              hand.tricks))

    def play_trick(self):
        cards_out = []
        for hand in self.hands:
            card_played = hand.play(self.trump, cards_out)
            print_method('Hand %s played %s.' % (hand, card_played.pretty))

        best_card = cards_out[0]
        lead_suit = cards_out[0].suit
        winning_index = 0
        for i, card in enumerate(cards_out[1:]):
            if card.is_better(best_card, self.trump, lead_suit):
                winning_index = i + 1
                best_card = card

        winning_hand = self.hands[winning_index]
        winning_hand.tricks += 1
        # Re-order so that the winning bidder is last.
        self.hands = reorder_for_hand(self.hands, winning_hand,
                                      make_last=False)
        print_method('%s wins.' % (winning_hand,))


class PlayerHand(object):

    def __init__(self, game, deck, player, hand_name=None):
        self.game = game
        self.hand_name = hand_name
        self.deck = deck
        self.player = player
        self.is_dealer = False
        self.won_bid = 0
        # Set the cards.
        self.played_cards = []
        self.unplayed_cards = []
        self.tricks = 0

    def __str__(self):
        return 'PlayerHand(%r)' % (self.hand_name,)

    @property
    def pretty(self):
        played_pretty_str = ','.join(card.pretty for card in self.played_cards)
        unplayed_pretty_str = ','.join(card.pretty
                                       for card in self.unplayed_cards)
        if played_pretty_str:
            if unplayed_pretty_str:
                return 'PlayerHand(%r, played=%s, unplayed=%s)' % (
                    self.hand_name, played_pretty_str, unplayed_pretty_str)
            else:
                return 'PlayerHand(%r, played=%s)' % (self.hand_name,
                                                      played_pretty_str)
        else:
            return 'PlayerHand(%r, unplayed=%s)' % (self.hand_name,
                                                    unplayed_pretty_str)


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
        card_played = self.player.play_card(self, trump, cards_out)
        cards_out.append(card_played)
        return card_played
