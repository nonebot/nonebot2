navigator.serviceWorker.getRegistrations().then(function (e) {
  for (
    var r, i = e, t = Array.isArray(i), a = 0, i = t ? i : i[Symbol.iterator]();
    ;

  ) {
    if (t) {
      if (a >= i.length) break;
      r = i[a++];
    } else {
      if ((a = i.next()).done) break;
      r = a.value;
    }
    r.unregister();
  }
});
