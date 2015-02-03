// This implementation of Context interface uses tokeninfo API to validate
// bearer token.
//
// It is intended to be used only on dev server.

package hukabuk

import (
	"encoding/json"
	"errors"
	"fmt"
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
	tokeninfoCache map[string]*tokeninfo
	// mutex for tokeninfoCache
	sync.Mutex
}

// fetchTokeninfo retrieves token info from tokeninfoEndpointURL  (tokeninfo API)
func fetchTokeninfo(c *cachingTokeninfoContext, token string) (*tokeninfo, error) {
	url := tokeninfoEndpointURL + "?access_token=" + token
	c.Debugf("Fetching token info from %q", url)
	resp, err := newHTTPClient(c).Get(url)
	if err != nil {
		return nil, err
	}
	defer resp.Body.Close()
	c.Debugf("Tokeninfo replied with %s", resp.Status)

	ti := &tokeninfo{}
	if err = json.NewDecoder(resp.Body).Decode(ti); err != nil {
		return nil, err
	}
	if resp.StatusCode != http.StatusOK {
		errMsg := fmt.Sprintf("Error fetching tokeninfo (status %d)", resp.StatusCode)
		if ti.ErrorDescription != "" {
			errMsg += ": " + ti.ErrorDescription
		}
		return nil, errors.New(errMsg)
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

func populateTokenInfo(c *cachingTokeninfoContext, scope string) error {
	// Only one scope should be cached at once, so we just destroy the cache
	c.tokeninfoCache = map[string]*tokeninfo{}

	token := getToken(c.HTTPRequest())
	if token == "" {
		return errors.New("No token found")
	}
	ti, err := fetchTokeninfo(c, token)
	if err != nil {
		return err
	}
	for _, s := range strings.Split(ti.Scope, " ") {
		if s == scope {
			c.tokeninfoCache[scope] = ti
			return nil
		}
	}
	return fmt.Errorf("No scope matches: expected one of %q, got %q",
		ti.Scope, scope)
}

// getScopedTokeninfo validates fetched token by matching tokeninfo.Scope
// with scope arg.
func getScopedTokeninfo(c *cachingTokeninfoContext, scope string) (*tokeninfo, error) {
	ti, ok := c.tokeninfoCache[scope]

	if !ok {
		c.Lock()
		defer c.Unlock()
		if err := populateTokenInfo(c, scope); err != nil {
			return nil, err
		}
		ti = c.tokeninfoCache[scope]
	}

	return ti, nil
}

func newTokenCachingContext(c appengine.Context, r *http.Request) Context {
	return &cachingTokeninfoContext{c, r, map[string]*tokeninfo{}, sync.Mutex{}}
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
