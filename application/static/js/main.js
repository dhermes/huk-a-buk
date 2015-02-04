var hukABukApp = hukABukApp || {};

hukABukApp.mainSigninCallback = function(authResult) {
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
