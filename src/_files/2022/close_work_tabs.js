#!/usr/bin/env osascript -l JavaScript
// A script to close ephemeral Safari tabs.
//
// This is a script I run at the end of each working day, to close
// Safari tabs I've opened that can be safely closed.
//
// See https://alexwlchan.net/2022/02/safari-tabs/

safari = Application("Safari Technology Preview");

// Generates all the window/tab/URLs in Safari.
//
// This runs in reverse window/tab index order: that is, windows are returned
// bottom to top, and tabs from right to left.
function* tabGenerator() {
  window_count = safari.windows.length;

  for (window_index = window_count - 1; window_index >= 0; window_index--) {
    this_window = safari.windows[window_index];

    tab_count = this_window.tabs.length;

    for (tab_index = tab_count - 1; tab_index >= 0; tab_index--) {
      tab = this_window.tabs[tab_index];
      yield [window_index, tab_index, tab.url()];
    }
  }
}

function isSafeToClose(url) {

  // Sometimes we get a `null` as the URL of a tab; I'm not sure why,
  // so leave this tab open.
  if (url === null) { return false; }

  return (
    url.startsWith("https://zoom.us/") ||
    url.startsWith("https://trustnet.wellcome.org/") ||
    url.startsWith("https://search.wellcomelibrary.org") ||
    url.startsWith("https://logging.wellcomecollection.org") ||
    url.startsWith("https://console.aws.amazon.com/") ||
    url.startsWith("https://us-east-1.signin.aws.amazon.com/") ||
    url.startsWith("https://eu-west-1.console.aws.amazon.com/") ||
    url.startsWith("https://github.com/wellcomecollection/") ||
    url.startsWith("https://github.com/search?type=Code&q=org:wellcomecollection") ||
    url.startsWith("https://buildkite.com/orgs/wellcomecollection/") ||
    url.startsWith("http://localhost:3000/") ||
    url.startsWith("https://api.wellcomecollection.org/") ||
    url.startsWith("https://www-stage.wellcomecollection.org/")
  );
}

for (const [window_index, tab_index, url] of tabGenerator()) {
  if (isSafeToClose(url)) {
    console.log(url);
    safari.windows[window_index].tabs[tab_index].close();
  }
}
