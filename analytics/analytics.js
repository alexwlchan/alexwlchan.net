(function() {
  if (navigator.doNotTrack == 1) {
    console.log("Do Not Track is enabled; don't run analytics 🙈");
  } else {
    var doc = document; enc = encodeURIComponent; img = new Image;
    img.src = "%s/a.gif?url=" + enc(doc.location.href) + "&ref=" + enc(doc.referrer) + "&t=" enc(doc.title);
  }
})()
