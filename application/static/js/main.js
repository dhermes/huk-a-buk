var hukABukApp = hukABukApp || {};

hukABukApp.addGame = function(gameId, numPlayers, tableElt) {
  var row = document.createElement('tr');

  var idElt = document.createElement('td');
  idElt.innerHTML = gameId;

  var numPlayersElt = document.createElement('td');
  if (numPlayers === 1) {
    numPlayersElt.innerHTML = numPlayers + ' player';
  } else {
    numPlayersElt.innerHTML = numPlayers + ' players';
  }

  row.appendChild(idElt);
  row.appendChild(numPlayersElt);

  tableElt.appendChild(row);
}

hukABukApp.getGames = function() {
  var gamesElt = document.getElementById('games');
  if (!gamesElt) {
    console.log('No games element found on page.');
    return;
  }
  var tableElts = gamesElt.getElementsByTagName('table');
  if (tableElts.length !== 1) {
    console.log('Expected 1 table elements.');
    return;
  }
  var tableElt = tableElts[0];

  gapi.client.hukabuk.game.list({}).execute(function(resp) {
    // TODO(djh): Check for resp.error.
    var game;
    for (var i = 0; i < resp.games.length; i++) {
      game = resp.games[i];
      hukABukApp.addGame(game.id, game.players.length, tableElt);
    }
  });
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
