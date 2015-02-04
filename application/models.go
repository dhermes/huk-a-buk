package hukabuk

import (
	"appengine"
	"appengine/datastore"

	"github.com/GoogleCloudPlatform/go-endpoints/endpoints"
)

type Game struct {
	Id   string `json:"id" endpoints:"required" datastore"-"`
	Deck Deck   `json:"deck" endpoints:"required"`
}

func GetGame(c appengine.Context, gameId string, game *Game) error {
	key := datastore.NewKey(c, "Game", gameId, 0, nil)
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
