package hukabuk

import (
	"errors"
	"fmt"
	"math/rand"
	"time"

	"appengine"
	"appengine/datastore"
)

var (
	suits = map[int8]bool{
		'H': true,
		'S': true,
		'C': true,
		'D': true,
	}
	suitsList = []int8{'H', 'S', 'C', 'D'}

	ranks = map[int8]uint8{ // Use 0 as empty key
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
	rankList = []int8{
		'2', '3', '4', '5',
		'6', '7', '8', '9',
		'T', 'J', 'Q', 'K', 'A',
	}
)

type Card struct {
	// Use int8 instead of byte since App Engine needs it to be signed.
	Suit int8 `json:"suit" endpoints:"required"`
	Rank int8 `json:"rank" endpoints:"required"`
}

type Hand struct {
	Cards   []Card    `json:"cards"`
	Created time.Time `json:"created"`
	Email   string    `json:"-"`
}

// Make a new Card. Verifies that the suit and rank are among
// the acceptable values (single bytes) where 'T', 'J', 'Q', 'K', 'A'
// are used for ranks outside of 2-9 and 'H' -> Heart, 'S' -> Spades,
// 'C' -> Clubs and 'D' -> Diamonds for suits.
func NewCard(suit int8, rank int8) (*Card, error) {
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
func (card *Card) IsBetter(other *Card, trump int8, lead int8) bool {
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

func GetHand(c appengine.Context, u *userLocal) (*Hand, error) {
	key := datastore.NewKey(c, "UserHand", u.GooglePlusID, 0, nil)
	hand := &Hand{}
	err := datastore.Get(c, key, hand)

	if err == nil {
		return hand, nil
	} else {
		// TODO(djh): Distinguish between a "good" error (key does not exist)
		//            and a "bad" one (request failure).
		c.Debugf("GetHand err: %v", err)
		return nil, err
	}
}

func randomCard() (*Card, error) {
	suit := suitsList[rand.Intn(len(suitsList))]
	rank := rankList[rand.Intn(len(rankList))]
	return NewCard(suit, rank)
}

func NewHand(hand *Hand, u *userLocal) error {
	hand.Created = time.Now().UTC()
	hand.Email = u.Email

	for i := 0; i < 5; i++ {
		card, err := randomCard()
		if err != nil {
			return err
		}
		hand.Cards = append(hand.Cards, *card)
	}
	return nil
}

func GetOrCreateHand(c appengine.Context, u *userLocal, hand *Hand) error {
	existingHand, err := GetHand(c, u)
	if err == nil {
		hand.Cards = existingHand.Cards
		hand.Created = existingHand.Created
		hand.Email = existingHand.Email
		return nil
	}

	// NOTE: This could be problematic since `hand` may be partially updated
	//       before a failure.
	err = NewHand(hand, u)
	if err != nil {
		return err
	}

	key := datastore.NewKey(c, "UserHand", u.GooglePlusID, 0, nil)
	_, err = datastore.Put(c, key, hand)
	return err
}
