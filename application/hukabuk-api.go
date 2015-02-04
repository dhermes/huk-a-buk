package hukabuk

import (
	"net/http"

	"github.com/GoogleCloudPlatform/go-endpoints/endpoints"
)

var (
	scopes    = []string{endpoints.EmailScope}
	clientIds = []string{ClientID, endpoints.APIExplorerClientID}
	// in case we'll want to use Huk-A-Buk API from an Android app
	audiences = []string{ClientID}
)

// getCurrentUser retrieves a user associated with the request.
// If there's no user (e.g. no auth info present in the request) returns
// an "unauthorized" error.
func getCurrentUser(c Context) (*userLocal, error) {
	u, err := CurrentUser(c, scopes, audiences, clientIds)
	if err != nil || u == nil {
		return nil, endpoints.NewUnauthorizedError("Request not authorized.")
	}
	c.Debugf("Current user: %#v", u)
	return u, nil
}

type EmptyAPIStruct struct {
}

// Huk-A-Buk API service
type HukABukApi struct {
}

type GameIDRequest struct {
	GameId int64 `json:"game,string"`
}

func (hapi *HukABukApi) GetCards(r *http.Request,
	req *GameIDRequest, resp *Hand) error {
	c := NewContext(r)
	c.Infof("req: %v", req)
	u, err := getCurrentUser(c)
	if err != nil {
		return err
	}

	var hand *Hand
	hand, err = GetHand(c, u, req.GameId)
	if err == nil {
		resp.Ranks = hand.Ranks
		resp.Suits = hand.Suits
		resp.Created = hand.Created
	}
	return err
}

type GetGameRequest struct {
	// H/T to: http://stackoverflow.com/a/21152548/1068170
	GameId *int64 `json:"id,string,omitempty"`
}

func (hapi *HukABukApi) GetGame(r *http.Request,
	req *GetGameRequest, resp *Game) error {
	c := NewContext(r)
	u, err := getCurrentUser(c)
	if err != nil {
		return err
	}
	if req.GameId == nil {
		return endpoints.NewBadRequestError("Game id is required.")
	}
	c.Infof("User %v unused until GetGame gets authenticated.", u)
	return GetGame(c, *req.GameId, resp)
}

type NewGameRequest struct {
	Players []string `json:"players"`
}

func (hapi *HukABukApi) NewGame(r *http.Request,
	req *NewGameRequest, resp *Game) error {
	c := NewContext(r)
	u, err := getCurrentUser(c)
	if err != nil {
		return err
	}
	return NewGame(c, u, req.Players, resp)
}

func (hapi *HukABukApi) GetGames(r *http.Request,
	req *EmptyAPIStruct, resp *GetGamesResponse) error {
	c := NewContext(r)
	u, err := getCurrentUser(c)
	if err != nil {
		return err
	}
	return GetGames(c, u, resp)
}

func (hapi *HukABukApi) StartGame(r *http.Request,
	req *GameIDRequest, resp *EmptyAPIStruct) error {
	c := NewContext(r)
	u, err := getCurrentUser(c)
	if err != nil {
		return err
	}
	game := &Game{}
	err = GetGame(c, req.GameId, game)
	if err != nil {
		return err
	}
	userInGame := false
	for _, player := range game.Players {
		if u.GooglePlusID == player {
			userInGame = true
			break
		}
	}
	if !userInGame {
		return endpoints.NewForbiddenError("User not in game.")
	}

	return StartGame(c, game)
}

// RegisterService exposes HukABukApi methods as API endpoints.
//
// The registration/initialization during startup is not performed here.
func RegisterService() (*endpoints.RPCService, error) {
	api := &HukABukApi{}
	rpcService, err := endpoints.RegisterService(
		api,
		"hukabuk",
		"v1beta",
		"Huk-A-Buk API",
		true,
	)
	if err != nil {
		return nil, err
	}

	info := rpcService.MethodByName("GetCards").Info()
	info.Path, info.HTTPMethod, info.Name = "cards", "GET", "cards.list"
	info.Scopes, info.ClientIds, info.Audiences = scopes, clientIds, audiences

	info = rpcService.MethodByName("GetGame").Info()
	info.Path, info.HTTPMethod, info.Name = "game", "GET", "game.get"
	info.Scopes, info.ClientIds, info.Audiences = scopes, clientIds, audiences

	info = rpcService.MethodByName("NewGame").Info()
	info.Path, info.HTTPMethod, info.Name = "game/new", "POST", "game.newgame"
	info.Scopes, info.ClientIds, info.Audiences = scopes, clientIds, audiences

	info = rpcService.MethodByName("GetGames").Info()
	info.Path, info.HTTPMethod, info.Name = "games", "GET", "game.list"
	info.Scopes, info.ClientIds, info.Audiences = scopes, clientIds, audiences

	info = rpcService.MethodByName("StartGame").Info()
	info.Path, info.HTTPMethod, info.Name = "games/{game}/start", "POST", "game.start"
	info.Scopes, info.ClientIds, info.Audiences = scopes, clientIds, audiences

	return rpcService, nil
}

func init() {
	if _, err := RegisterService(); err != nil {
		panic(err.Error())
	}
	endpoints.HandleHTTP()
}
