/* Re-use Google namespace. */
var google = google || {};
google.config = google.config || {};

var hukABukApp = hukABukApp || {};

hukABukApp.SUITS = {
    'H': '\u2665',
    'S': '\u2660',
    'C': '\u2663',
    'D': '\u2666'
}
hukABukApp.RANKS = {
    1: '2',
    2: '3',
    3: '4',
    4: '5',
    5: '6',
    6: '7',
    7: '8',
    8: '9',
    9: '10',
    10: 'J',
    11: 'Q',
    12: 'K',
    13: 'A'
}

/**
 * Client ID of the application (from the APIs Console).
 * @type {string}
 */
hukABukApp.CLIENT_ID = google.config.CLIENT_ID;

/**
 * Scopes used by the application.
 * @type {string}
 */
hukABukApp.SCOPES =
    'https://www.googleapis.com/auth/userinfo.email ' +
    'https://www.googleapis.com/auth/plus.login';

/**
 * Parses email from the claim set of a JWT ID token.
 *
 * NOTE: We are not validating the ID token since from a trusted source.
 *       We are simply parsed the value from the JWT.
 *
 * See http://www.tbray.org/ongoing/When/201x/2013/04/04/ID-Tokens
 * or
 * http://openid.net/specs/openid-connect-messages-1_0.html#StandardClaims
 * for more info.
 *
 * @param {string} idToken A base64 JWT containing a user ID token.
 * @return {string} The email parsed from the claim set, else undefined
 *                  if one can't be parsed.
 */
hukABukApp.getEmailFromIDToken = function(idToken) {
  if (typeof idToken !== 'string') {
    return;
  }

  var segments = idToken.split('.');
  if (segments.length !== 3) {
    return;
  }

  try {
    var claimSet = JSON.parse(atob(segments[1]));
  } catch (e) {
    return;
  }

  if (claimSet.email && typeof claimSet.email === 'string') {
    return claimSet.email;
  }
}

hukABukApp.addCard = function(tdElt, suit, rank) {
    var sp = document.createElement('span');
    var colorClass;
    if (suit === 'H' || suit === 'D') {
        colorClass = "red";
    } else if (suit === 'C' || suit === 'S') {
        colorClass = "black";
    } else {
        console.log('Unexpected suit.');
        return;
    }

    if (!(rank in hukABukApp.RANKS)) {
        console.log('Unexpected rank.');
        return;
    }

    sp.innerHTML = hukABukApp.SUITS[suit] + hukABukApp.RANKS[rank];
    sp.classList.add(colorClass);
    tdElt.appendChild(sp);
}

hukABukApp.queryCards = function() {
    var cardElt = document.getElementById('cards');
    if (!cardElt) {
        console.log('No cards element found on page.');
        return;
    }
    var tdElts = cardElt.getElementsByTagName('td');
    if (tdElts.length !== 5) {
        console.log('Expected 5 TD elements.');
        return;
    }

    // Fake a response.
    hukABukApp.addCard(tdElts[0], 'H', 1);
    hukABukApp.addCard(tdElts[1], 'S', 6);
    hukABukApp.addCard(tdElts[2], 'C', 9);
    hukABukApp.addCard(tdElts[3], 'D', 12);
    hukABukApp.addCard(tdElts[4], 'H', 13);
}

/**
 * Handles the Google+ Sign In response.
 *
 * Success calls hukABukApp.init. Failure makes the Sign-In
 * button visible.
 *
 * @param {Object} authResult The contents returned from the Google+
 *                            Sign In attempt.
 */
hukABukApp.signinCallback = function(authResult) {
  var tokenEmail = hukABukApp.getEmailFromIDToken(
      authResult.id_token);
  if (authResult.access_token && tokenEmail) {
    document.getElementById('warning').classList.add('hidden');
    document.getElementById('cards').classList.remove('hidden');
    document.getElementById('userLabel').innerHTML = tokenEmail;

    document.getElementById('signinButtonContainer').classList.remove(
        'visible');
    document.getElementById('signedInStatus').classList.add('visible');

    hukABukApp.queryCards();
  } else {
    document.getElementById('warning').classList.remove('hidden');
    document.getElementById('cards').classList.add('hidden');

    document.getElementById('signinButtonContainer').classList.add('visible');
    document.getElementById('signedInStatus').classList.remove('visible');

    if (!authResult.error) {
      console.log('Unexpected result');
      console.log(authResult);
    } else if (authResult.error !== 'immediate_failed') {
      console.log('Unexpected error occured: ' + authResult.error);
    } else {
      console.log('Immediate mode failed, user needs to click Sign In.');
    }
  }
};

/**
 * Renders the Google+ Sign-in button using auth parameters.
 */
hukABukApp.renderHukABuk = function() {
  gapi.signin.render('signinButton', {
    'callback': hukABukApp.signinCallback,
    'clientid': hukABukApp.CLIENT_ID,
    'cookiepolicy': 'single_host_origin',
    'requestvisibleactions': 'http://schemas.google.com/AddActivity',
    'scope': hukABukApp.SCOPES
  });
};
// A quirk of the JSONP callback of the plusone client makes it so
// our callback must exist as an element in window.
window['hukABukApp.renderHukABuk'] = hukABukApp.renderHukABuk;

// Recommended code to load Google+ JS library.
(function() {
  var newScriptElement = document.createElement('script');
  newScriptElement.type = 'text/javascript';
  newScriptElement.async = true;
  newScriptElement.src = 'https://apis.google.com/js/client:plusone.js' +
                         '?onload=hukABukApp.renderHukABuk';
  var firstScriptElement = document.getElementsByTagName('script')[0];
  firstScriptElement.parentNode.insertBefore(newScriptElement,
                                             firstScriptElement);
})();