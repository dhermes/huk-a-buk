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
	unshuffledDeck = map[int8]Card{
		0:  Card{Suit: 'H', Rank: '2'},
		1:  Card{Suit: 'H', Rank: '3'},
		2:  Card{Suit: 'H', Rank: '4'},
		3:  Card{Suit: 'H', Rank: '5'},
		4:  Card{Suit: 'H', Rank: '6'},
		5:  Card{Suit: 'H', Rank: '7'},
		6:  Card{Suit: 'H', Rank: '8'},
		7:  Card{Suit: 'H', Rank: '9'},
		8:  Card{Suit: 'H', Rank: 'T'},
		9:  Card{Suit: 'H', Rank: 'J'},
		10: Card{Suit: 'H', Rank: 'Q'},
		11: Card{Suit: 'H', Rank: 'K'},
		12: Card{Suit: 'H', Rank: 'A'},
		13: Card{Suit: 'S', Rank: '2'},
		14: Card{Suit: 'S', Rank: '3'},
		15: Card{Suit: 'S', Rank: '4'},
		16: Card{Suit: 'S', Rank: '5'},
		17: Card{Suit: 'S', Rank: '6'},
		18: Card{Suit: 'S', Rank: '7'},
		19: Card{Suit: 'S', Rank: '8'},
		20: Card{Suit: 'S', Rank: '9'},
		21: Card{Suit: 'S', Rank: 'T'},
		22: Card{Suit: 'S', Rank: 'J'},
		23: Card{Suit: 'S', Rank: 'Q'},
		24: Card{Suit: 'S', Rank: 'K'},
		25: Card{Suit: 'S', Rank: 'A'},
		26: Card{Suit: 'C', Rank: '2'},
		27: Card{Suit: 'C', Rank: '3'},
		28: Card{Suit: 'C', Rank: '4'},
		29: Card{Suit: 'C', Rank: '5'},
		30: Card{Suit: 'C', Rank: '6'},
		31: Card{Suit: 'C', Rank: '7'},
		32: Card{Suit: 'C', Rank: '8'},
		33: Card{Suit: 'C', Rank: '9'},
		34: Card{Suit: 'C', Rank: 'T'},
		35: Card{Suit: 'C', Rank: 'J'},
		36: Card{Suit: 'C', Rank: 'Q'},
		37: Card{Suit: 'C', Rank: 'K'},
		38: Card{Suit: 'C', Rank: 'A'},
		39: Card{Suit: 'D', Rank: '2'},
		40: Card{Suit: 'D', Rank: '3'},
		41: Card{Suit: 'D', Rank: '4'},
		42: Card{Suit: 'D', Rank: '5'},
		43: Card{Suit: 'D', Rank: '6'},
		44: Card{Suit: 'D', Rank: '7'},
		45: Card{Suit: 'D', Rank: '8'},
		46: Card{Suit: 'D', Rank: '9'},
		47: Card{Suit: 'D', Rank: 'T'},
		48: Card{Suit: 'D', Rank: 'J'},
		49: Card{Suit: 'D', Rank: 'Q'},
		50: Card{Suit: 'D', Rank: 'K'},
		51: Card{Suit: 'D', Rank: 'A'},
	}
)

type Card struct {
	// Use int8 instead of byte since App Engine needs it to be signed.
	Suit int8 `json:"suit" endpoints:"required"`
	Rank int8 `json:"rank" endpoints:"required"`
}

type Deck struct {
	cards     *[]int // TODO(djh): Would prefer to use int8.
	currIndex int8
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

func (deck *Deck) Shuffle() {
	deck.currIndex = 0
	perm := rand.Perm(52)
	deck.cards = &perm
}

func (deck *Deck) NextCard() Card {
	var cardIndex int8
	if deck.cards == nil {
		cardIndex = deck.currIndex
	} else {
		cardIndex = int8((*deck.cards)[deck.currIndex])
	}
	deck.currIndex++
	return unshuffledDeck[cardIndex]
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

func NewHand(hand *Hand, u *userLocal) error {
	hand.Created = time.Now().UTC()
	hand.Email = u.Email

	deck := &Deck{}
	deck.Shuffle()

	hand.Cards = make([]Card, 5)
	hand.Cards[0] = deck.NextCard()
	hand.Cards[1] = deck.NextCard()
	hand.Cards[2] = deck.NextCard()
	hand.Cards[3] = deck.NextCard()
	hand.Cards[4] = deck.NextCard()
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
