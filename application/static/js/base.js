var hukABukApp = hukABukApp || {};

hukABukApp.SUITS = {
    'H': '\u2665',
    'S': '\u2660',
    'C': '\u2663',
    'D': '\u2666'
}
hukABukApp.RANKS = {
    '2': '2',
    '3': '3',
    '4': '4',
    '5': '5',
    '6': '6',
    '7': '7',
    '8': '8',
    '9': '9',
    'T': '10',
    'J': 'J',
    'Q': 'Q',
    'K': 'K',
    'A': 'A'
}

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

hukABukApp.baseSigninCallback = function(authResult) {
  var tokenEmail = hukABukApp.getEmailFromIDToken(
      authResult.id_token);
  if (authResult.access_token && tokenEmail) {
    // BEGIN: Hack to make sure ID tokens are sent in request.
    var token = gapi.auth.getToken();
    token.access_token = token.id_token;
    gapi.auth.setToken(token);
    //   END: Hack to make sure ID tokens are sent in request.
    document.getElementById('warning').classList.add('hidden');

    document.getElementById('signinButtonContainer').classList.remove(
        'visible');
    document.getElementById('signedInTopLeft').classList.add('visible');
    document.getElementById('userLabel').innerHTML = tokenEmail;

    return true;
  } else {
    document.getElementById('warning').classList.remove('hidden');

    document.getElementById('signinButtonContainer').classList.add('visible');
    document.getElementById('signedInTopLeft').classList.remove('visible');

    if (!authResult.error) {
      console.log('Unexpected result');
      console.log(authResult);
    } else if (authResult.error !== 'immediate_failed') {
      console.log('Unexpected error occured: ' + authResult.error);
    } else {
      console.log('Immediate mode failed, user needs to click Sign In.');
    }
    return false;
  }
};

hukABukApp.renderSigninButton = function(callback) {
  gapi.signin.render('signinButton', {
    'callback': callback,
    'clientid': hukABukApp.CLIENT_ID,
    'cookiepolicy': 'single_host_origin',
    'requestvisibleactions': 'http://schemas.google.com/AddActivity',
    'scope': hukABukApp.SCOPES
  });
};

// Recommended code to load Google+ JS library.
hukABukApp.loadGoogle = function(onloadStr) {
  var newScriptElement = document.createElement('script');
  newScriptElement.type = 'text/javascript';
  newScriptElement.async = true;
  newScriptElement.src = 'https://apis.google.com/js/client:plusone.js' +
                         '?onload=' + onloadStr;
  var firstScriptElement = document.getElementsByTagName('script')[0];
  firstScriptElement.parentNode.insertBefore(newScriptElement,
                                             firstScriptElement);
}
