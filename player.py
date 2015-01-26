import random


class PlayerHand(object):

    def __init__(self, deck, player):
        self.deck = deck
        self.player = player
        # Set the cards.
        self.played_cards = []
        self.unplayed_cards = [deck.draw_card() for _ in xrange(5)]

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

    RANDOM_BIDS = (2, 3, 4, 5)

    def draw_cards(self, hand):
        num_to_draw = random.randint(0, 6)  # `randint` is inclusive
        if num_to_draw == 6:
            return None

        # Keep a random subset of cards.
        # random.sample "Chooses k unique random elements"
        hand.unplayed_cards = random.sample(hand.unplayed_cards,
                                            5 - num_to_draw)
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
