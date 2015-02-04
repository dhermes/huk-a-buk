package hukabuk

import (
	"appengine"
	"appengine/datastore"

	"github.com/GoogleCloudPlatform/go-endpoints/endpoints"
)

type Game struct {
	Id      int64    `json:"id" endpoints:"required" datastore:"-"`
	Deck    Deck     `json:"deck" endpoints:"required"`
	Players []string `json:"players"`
}

func GetGame(c appengine.Context, gameId int64, game *Game) error {
	key := datastore.NewKey(c, "Game", "", gameId, nil)
	err := datastore.Get(c, key, game)
	if err == nil {
		game.Id = gameId
		return nil
	} else {
		// TODO(djh): Distinguish between a "good" error (key does not exist)
		//            and a "bad" one (request failure).
		c.Debugf("GetGame err: %v", err)
		return endpoints.NewNotFoundError("Game not found.")
	}
}

func StartGame(c appengine.Context, u *userLocal, game *Game) error {
	key := datastore.NewIncompleteKey(c, "Game", nil)
	game.Players = append(game.Players, u.GooglePlusID)
	game.Deck = Deck{}
	game.Deck.Shuffle()

	newKey, err := datastore.Put(c, key, game)
	if err != nil {
		c.Infof("error failure: %v", err)
		return endpoints.NewBadRequestError("Creating game failed.")
	}
	game.Id = newKey.IntID()
	c.Infof("newKey.IntID(): %v, key.IntID(): %v", game.Id, key.IntID())
	return nil
}
