(function() {
  if (navigator.doNotTrack == 1) {
    console.log("You have Do Not Track enabled, so I don't record any analytics.");
  } else {
    var doc = document, enc = encodeURIComponent, img = new Image;
    img.src = "/analytics/a.gif?url=" + enc(doc.location.href) + "&ref=" + enc(doc.referrer) + "&t=" + enc(doc.title);
  }
})()
