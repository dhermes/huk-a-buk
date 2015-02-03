package hukabuk

import (
	"errors"
	"net/http"

	"github.com/GoogleCloudPlatform/go-endpoints/endpoints"
)

var (
	scopes    = []string{endpoints.EmailScope}
	clientIds = []string{ClientID, endpoints.APIExplorerClientID}
	// in case we'll want to use Huk-A-Buk API from an Android app
	audiences = []string{ClientID}
)

type EmptyRequest struct {
}

// Huk-A-Buk API service
type HukABukApi struct {
}

func (hapi *HukABukApi) GetCards(r *http.Request,
	req *EmptyRequest, resp *Hand) error {

	c := NewContext(r)
	u, err := getCurrentUser(c) // Not Used
	if err != nil {
		return err
	}
	c.Infof("%v", u)

	return GetOrCreateHand(c, u, resp)
}

// getCurrentUser retrieves a user associated with the request.
// If there's no user (e.g. no auth info present in the request) returns
// an "unauthorized" error.
func getCurrentUser(c Context) (*userLocal, error) {
	u, err := CurrentUser(c, scopes, audiences, clientIds)
	if err != nil {
		return nil, err
	}
	if u == nil {
		return nil, errors.New("Unauthorized: Please, sign in.")
	}
	c.Debugf("Current user: %#v", u)
	return u, nil
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

	return rpcService, nil
}

func init() {
	if _, err := RegisterService(); err != nil {
		panic(err.Error())
	}
	endpoints.HandleHTTP()
}
