import random


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
