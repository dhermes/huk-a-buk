var hukABukApp = hukABukApp || {};

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

  gapi.client.hukabuk.cards.list({}).execute(function(resp) {
    var suits = atob(resp.suits);
    var ranks = atob(resp.ranks);
    for (var i = 0; i < 5; i++) {
      hukABukApp.addCard(tdElts[i], suits[i], ranks[i]);
    }
  });
}

hukABukApp.gameSigninCallback = function(authResult) {
  if (hukABukApp.baseSigninCallback(authResult)) {
    document.getElementById('cards').classList.remove('hidden');
    var apiRoot = '//' + window.location.host + '/_ah/api';
    gapi.client.load('hukabuk', 'v1beta', hukABukApp.queryCards, apiRoot);
  } else {
    document.getElementById('cards').classList.add('hidden');
  }
};

// Callback with no arguments.
hukABukApp.renderGame = function() {
  hukABukApp.renderSigninButton(hukABukApp.gameSigninCallback);
};
// A quirk of the JSONP callback of the plusone client makes it so
// our callback must exist as an element in window.
window['hukABukApp.renderGame'] = hukABukApp.renderGame;

hukABukApp.loadGoogle('hukABukApp.renderGame');
