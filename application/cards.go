package hukabuk

import (
	"math/rand"
	"time"

	"appengine"
	"appengine/datastore"
)

var (
	suitsList = []byte{'H', 'S', 'C', 'D'}
	ranks     = map[byte]uint8{
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
	Suit byte `json:"suit" endpoints:"required"`
	Rank byte `json:"rank" endpoints:"required"`
}

type Deck struct {
	CardBytes []byte `json:"cardBytes" datastore:"cardBytes"`
	currIndex int8
}

type Hand struct {
	Suits   []byte    `json:"suits"`
	Ranks   []byte    `json:"ranks"`
	Created time.Time `json:"created"`
	Email   string    `json:"-"`
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

func (deck *Deck) Shuffle() {
	deck.currIndex = 0
	numCards := 52
	// H/T to: http://stackoverflow.com/a/12321192/1068170
	source := rand.NewSource(time.Now().UTC().UnixNano())
	intPerm := rand.New(source).Perm(numCards)

	perm := make([]byte, numCards)
	for i, value := range intPerm {
		perm[i] = byte(value)
	}
	deck.CardBytes = perm
}

func (deck *Deck) NextCard() Card {
	var cardIndex int8
	if deck.CardBytes == nil {
		cardIndex = deck.currIndex
	} else {
		cardIndex = int8(deck.CardBytes[deck.currIndex])
	}
	deck.currIndex++
	return unshuffledDeck[cardIndex]
}

func GetHand(c appengine.Context, u *userLocal) (*Hand, error) {
	key := datastore.NewKey(c, "Hand", u.GooglePlusID, 0, nil)
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

	hand.Ranks = make([]byte, 5)
	hand.Suits = make([]byte, 5)
	for i := 0; i < 5; i++ {
		card := deck.NextCard()
		hand.Ranks[i] = card.Rank
		hand.Suits[i] = card.Suit
	}
	return nil
}

func GetOrCreateHand(c appengine.Context, u *userLocal, hand *Hand) error {
	existingHand, err := GetHand(c, u)
	if err == nil {
		hand.Ranks = existingHand.Ranks
		hand.Suits = existingHand.Suits
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

	key := datastore.NewKey(c, "Hand", u.GooglePlusID, 0, nil)
	_, err = datastore.Put(c, key, hand)
	return err
}
