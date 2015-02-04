var hukABukApp = hukABukApp || {};

hukABukApp.getGames = function() {
};

hukABukApp.mainSigninCallback = function(authResult) {
  if (hukABukApp.baseSigninCallback(authResult)) {
    document.getElementById('games').classList.remove('hidden');
    var apiRoot = '//' + window.location.host + '/_ah/api';
    gapi.client.load('hukabuk', 'v1beta', hukABukApp.getGames, apiRoot);
  } else {
    document.getElementById('games').classList.add('hidden');
  }

  var tokenEmail = hukABukApp.baseSigninCallback(authResult);
};

// Callback with no arguments.
hukABukApp.renderMain = function() {
  hukABukApp.renderSigninButton(hukABukApp.mainSigninCallback);
};
// A quirk of the JSONP callback of the plusone client makes it so
// our callback must exist as an element in window.
window['hukABukApp.renderMain'] = hukABukApp.renderMain;

hukABukApp.loadGoogle('hukABukApp.renderMain');
