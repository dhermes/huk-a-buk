package hukabuk

import (
	"fmt"
	"net/http"
)

func init() {
	http.HandleFunc("/", handler)
}

func handler(w http.ResponseWriter, r *http.Request) {
	c1 := &Card{Suit: 'H', Rank: '2'}
	c2 := &Card{Suit: 'H', Rank: '5'}
	if c1.IsBetter(c2, 'S', 'D') {
		fmt.Fprint(w, "Card 1 is better.\n")
	} else {
		fmt.Fprint(w, "Card 1 is not better.\n")
	}
	fmt.Fprint(w, "Yay for Huk-A-Buk!")
}
