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

type EmptyRequest struct {
}

type CardListResponse struct {
	Items []*Card `json:"items"`
}

// Huk-A-Buk API service
type HukABukApi struct {
}

func (hapi *HukABukApi) GetCards(r *http.Request,
	req *EmptyRequest, resp *CardListResponse) error {

	resp.Items = []*Card{}

	c, err := NewCard('H', '2')
	resp.Items = append(resp.Items, c)

	c, err = NewCard('S', '7')
	resp.Items = append(resp.Items, c)

	c, err = NewCard('C', 'T')
	resp.Items = append(resp.Items, c)

	c, err = NewCard('D', 'K')
	resp.Items = append(resp.Items, c)

	c, err = NewCard('H', 'A')
	resp.Items = append(resp.Items, c)

	return err
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
