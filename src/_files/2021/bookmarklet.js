var sourcePath = document.querySelector("meta[name=page-source-path]").attributes["content"].value;

/* I run the site on http://localhost:5757 when working locally, so that's
 * the URL I want to switch to for the dev preview. */
if (document.location.href.startsWith("https://alexwlchan.net/")) {
  var altEnvironment = "local dev preview";
  var altUrl = document.location.href.replace("https://alexwlchan.net/", "http://localhost:5757/");
} else {
  var altEnvironment = "live version";
  var altUrl = document.location.href.replace("http://localhost:5757/", "https://alexwlchan.net/");
}

/* Are we running on iOS? I don't have a local checkout of the repo on iOS
 * and I don't run the localhost version of the site, so adding those links
 * isn't useful.  On iOS, the only link I want is to the GitHub source, so I
 * can do quick edits in the browser.
 *
 * See https://stackoverflow.com/q/9038625/1558022 */
var iOS = [
    'iPad Simulator',
    'iPhone Simulator',
    'iPod Simulator',
    'iPad',
    'iPhone',
    'iPod'
].includes(navigator.platform) || (navigator.userAgent.includes("Mac") && "ontouchend" in document);

if (iOS) {
  document.querySelector("body").innerHTML = `
    <article style="padding-bottom: 8px; padding-top: 8px;">
      Edit this page:&nbsp;
      <ul class="dot_list" style="display: inline-block; margin: 0;">
        <li><a href="https://github.com/alexwlchan/alexwlchan.net/blob/live/src/${sourcePath}">on GitHub</a></li>
      </ul>
    </article>
    ` + document.querySelector("body").innerHTML;
} else {
  /* The link to open in my text editor uses a txmt:// URL, which is the URL
   * scheme for opening files in TextMate, my editor of choice. */
  document.querySelector("body").innerHTML = `
    <article style="padding-bottom: 8px; padding-top: 8px;">
      Edit this page:&nbsp;
      <ul class="dot_list" style="display: inline-block; margin: 0;">
        <li><a href="https://github.com/alexwlchan/alexwlchan.net/blob/live/src/${sourcePath}">on GitHub</a></li>
        <li><a href="txmt://open?url=file://~/repos/alexwlchan.net/src/${sourcePath}">in TextMate</a></li>
      </ul>
      &nbsp;/&nbsp;
      See the <a href="${altUrl}">${altEnvironment}</a> of this page
    </article>
    ` + document.querySelector("body").innerHTML;
}
