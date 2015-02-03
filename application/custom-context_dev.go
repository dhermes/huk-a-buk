// This implementation of Context interface uses tokeninfo API to validate
// bearer token.
//
// It is intended to be used only on dev server.

package hukabuk

import (
	"encoding/json"
	"errors"
	"fmt"
	"io/ioutil"
	"net/http"
	"strings"
	"sync"

	"appengine"
)

const tokeninfoEndpointURL = "https://www.googleapis.com/oauth2/v2/tokeninfo"

type tokeninfo struct {
	IssuedTo      string `json:"issued_to"`
	Audience      string `json:"audience"`
	UserID        string `json:"user_id"` // Equivalent of `Subject`
	Scope         string `json:"scope"`
	ExpiresIn     int    `json:"expires_in"`
	Email         string `json:"email"`
	VerifiedEmail bool   `json:"verified_email"`
	AccessType    string `json:"access_type"`
	// ErrorDescription is populated when an error occurs. Usually, the response
	// either contains only ErrorDescription or the fields above
	ErrorDescription string `json:"error_description"`
}

// A context that uses tokeninfo API to validate bearer token
type cachingTokeninfoContext struct {
	appengine.Context
	r *http.Request
	// map keys as scopes
	responseCache map[string]*[]byte
	// mutex for oauthResponseCache
	sync.Mutex
}

func populateTokenInfoResponse(c *cachingTokeninfoContext, token string, scope string) error {
	// Only one scope should be cached at once, so we just destroy the cache
	c.responseCache = map[string]*[]byte{}

	// Construct the URL to get the token.
	url := tokeninfoEndpointURL + "?access_token=" + token
	c.Debugf("Fetching token info from %q", url)
	resp, err := newHTTPClient(c).Get(url)
	if err != nil {
		return err
	}
	// Make sure to close if the request did not fail.
	defer resp.Body.Close()

	c.Debugf("Tokeninfo replied with %s", resp.Status)
	if resp.StatusCode != http.StatusOK {
		errMsg := fmt.Sprintf("Error fetching tokeninfo (status %d)", resp.StatusCode)
		return errors.New(errMsg)
	}

	var content []byte
	content, err = ioutil.ReadAll(resp.Body)
	if err != nil {
		return err

	}

	c.responseCache[scope] = &content
	return nil
}

func getTokenInfoResponse(c *cachingTokeninfoContext, token string, scope string) (*[]byte, error) {
	res, ok := c.responseCache[scope]

	if !ok {
		c.Lock()
		defer c.Unlock()
		if err := populateTokenInfoResponse(c, token, scope); err != nil {
			return nil, err
		}
		res = c.responseCache[scope]
	}

	return res, nil
}

// fetchTokeninfo retrieves token info from tokeninfoEndpointURL  (tokeninfo API)
func fetchTokeninfo(c *cachingTokeninfoContext, token string, scope string) (*tokeninfo, error) {
	responseBody, err := getTokenInfoResponse(c, token, scope)
	if err != nil {
		return nil, err
	}

	ti := &tokeninfo{}
	if err = json.Unmarshal(*responseBody, ti); err != nil {
		return nil, err
	}

	switch {
	case ti.ExpiresIn <= 0:
		return nil, errors.New("Token is expired")
	case !ti.VerifiedEmail:
		return nil, fmt.Errorf("Unverified email %q", ti.Email)
	case ti.Email == "":
		return nil, fmt.Errorf("Invalid email address")
	}

	return ti, err
}

// getScopedTokeninfo validates fetched token by matching tokeinfo.Scope
// with scope arg.
func getScopedTokeninfo(c *cachingTokeninfoContext, scope string) (*tokeninfo, error) {
	token := getToken(c.HTTPRequest())
	if token == "" {
		return nil, errors.New("No token found")
	}
	ti, err := fetchTokeninfo(c, token, scope)
	if err != nil {
		return nil, err
	}
	for _, s := range strings.Split(ti.Scope, " ") {
		if s == scope {
			return ti, nil
		}
	}
	return nil, fmt.Errorf("No scope matches: expected one of %q, got %q",
		ti.Scope, scope)
}

func newTokenCachingContext(c appengine.Context, r *http.Request) Context {
	return &cachingTokeninfoContext{c, r, map[string]*[]byte{}, sync.Mutex{}}
}

func (c *cachingTokeninfoContext) HTTPRequest() *http.Request {
	// WAS: c.Request().(*http.Request)
	return c.r
}

// Namespace returns a replacement context that operates within the given namespace.
func (c *cachingTokeninfoContext) Namespace(name string) (Context, error) {
	nc, err := appengine.Namespace(c, name)
	if err != nil {
		return nil, err
	}
	return newTokenCachingContext(nc, c.r), nil
}

// CurrentOAuthClientID returns a clientID associated with the scope.
func (c *cachingTokeninfoContext) CurrentOAuthClientID(scope string) (string, error) {
	ti, err := getScopedTokeninfo(c, scope)
	if err != nil {
		return "", err
	}
	return ti.IssuedTo, nil
}

// CurrentOAuthUser returns a user associated with the request in context.
func (c *cachingTokeninfoContext) CurrentOAuthUser(scope string) (*userLocal, error) {
	ti, err := getScopedTokeninfo(c, scope)
	if err != nil {
		return nil, err
	}
	return &userLocal{
		Email:        ti.Email,
		GooglePlusID: ti.UserID,
	}, nil
}

// cachingTokeninfoContextFactory creates a new cachingTokeninfoContext from r.
// To be used as auth.go/ContextFactory.
func cachingTokeninfoContextFactory(r *http.Request) Context {
	return newTokenCachingContext(appengine.NewContext(r), r)
}
