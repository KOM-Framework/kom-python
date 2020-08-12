(function() {
 if (window.httpRequestsListenerStarted) return;
 window.httpRequestsListenerStarted = true;
 var oldOpen = XMLHttpRequest.prototype.open;
 window.openHTTPs = 0;
 var listener = function() {
  if (this.readyState == 4) {
   window.openHTTPs--;
   this.removeEventListener('readystatechange', listener);
  }
 };
 XMLHttpRequest.prototype.open = function(method, url, async, user, pass) {
  window.openHTTPs++;
  this.addEventListener('readystatechange', listener);
  oldOpen.call(this, method, url, async, user, pass);
 };
})();