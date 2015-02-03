package hukabuk

import (
	"errors"
	"fmt"
)

var (
	suits = map[byte]bool{
		'H': true,
		'S': true,
		'C': true,
		'D': true,
	}
	ranks = map[byte]uint8{ // Use 0 as empty key
		'2': 1,
		'3': 2,
		'4': 3,
		'5': 4,
		'6': 5,
		'7': 6,
		'8': 7,
		'9': 8,
		'T': 9,
		'J': 10,
		'Q': 11,
		'K': 12,
		'A': 13,
	}
)

type Card struct {
	Suit byte `json:"suit" endpoints:"required"`
	Rank byte `json:"rank" endpoints:"required"`
}

// Make a new Card. Verifies that the suit and rank are among
// the acceptable values (single bytes) where 'T', 'J', 'Q', 'K', 'A'
// are used for ranks outside of 2-9 and 'H' -> Heart, 'S' -> Spades,
// 'C' -> Clubs and 'D' -> Diamonds for suits.
func NewCard(suit byte, rank byte) (*Card, error) {
	card := &Card{}

	if !suits[suit] {
		return nil, errors.New(fmt.Sprintf("Invalid suit: %q.", suit))
	}
	card.Suit = suit

	if ranks[rank] == 0 {
		return nil, errors.New(fmt.Sprintf("Invalid rank: %q.", rank))
	}
	card.Rank = rank
	return card, nil
}

// IsBetter compares a card to another during a hand of Huk-A-Buk. In
// addition to the cards themselves, the trump for the hand and the
// suit led on the current trick must be incorporated. In the case that
// both cards don't match the trump or the lead suit, no comparison
// between the two is relevant.
func (card *Card) IsBetter(other *Card, trump byte, lead byte) bool {
	if card.Suit == other.Suit {
		return ranks[card.Rank] > ranks[other.Rank]
	}

	// If the suits are different, then at most 1 is trump and at
	// most 1 is the lead suit.
	// Trump has higher precedence than lead (which may also be trump).
	if card.Suit == trump {
		return true
	} else if other.Suit == trump {
		return false
	}

	if card.Suit == lead {
		return true
	} else if other.Suit == lead {
		return false
	}

	// If neither card is one of the relevant suits, their comparison
	// is irrelevant.
	return false
}
