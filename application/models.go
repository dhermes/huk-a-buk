package hukabuk

import (
	"appengine"
	"appengine/datastore"

	"github.com/GoogleCloudPlatform/go-endpoints/endpoints"
)

type Game struct {
	// Id is just the Key Id, but we keep it around for responses.
	Id      int64    `json:"id" datastore:"-"`
	Deck    Deck     `json:"-"`
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

type GetGamesResponse struct {
	// H/T to: http://stackoverflow.com/a/21152548/1068170
	Games []Game `json:"games"`
}

func GetGames(c appengine.Context, u *userLocal, resp *GetGamesResponse) error {
	gameId := int64(5865619656278016)
	game := &Game{}
	err := GetGame(c, gameId, game)
	if err == nil {
		resp.Games = []Game{*game}
		return nil
	} else {
		return err
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
