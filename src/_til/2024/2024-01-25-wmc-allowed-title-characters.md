---
layout: til
date: 2024-01-25 12:34:09 +0000
title: What characters are allowed in titles on Wikimedia Commons?
tags:
  - wikimedia-commons
---
When you upload a file to Wikimedia Commons with the Upload Wizard, you sometimes get an error about invalid titles:

<img src="/images/2024/wiki-commons-title.png" class="screenshot" style="width: 529px;" alt="An error message: 'This title is invalid. Make sure to remove characters like square brackets, colons, slashes, comparison operators, pipes and curly brackets.'">

I've seen the other title validation by watching the Network tab in the Safari developer tools, but I don't see the page making any network requests before it rejects this title.

Instead, it's inspecting the [`wgIllegalFileChars` setting](https://www.mediawiki.org/wiki/Manual:$wgIllegalFileChars).

## Debugging steps

In the Sources tab of the Safari developer tools, I did a global search (⇧⌘F) for the text in the error.
There were two results: once in the HTML of the page where it was appearing, once in a list of error message translations.
It's the English translation for the error `mwe-upwiz-error-title-invalid`.

<img src="/images/2024/wmc-inspector-search-1.png" class="screenshot" style="width: 668px;">

Then I did a search for the ID in the translation file, where I see that you can get this error if an exception is thrown while constructing the title.
I made a guess that the `makeTitleInFileNS` function might be interesting:

<img src="/images/2024/wmc-inspector-search-2.png" class="screenshot" style="width: 668px;">

I did another search to find the definition of the function, where I see that it looks for characters defined by a config setting:

<img src="/images/2024/wmc-inspector-search-3.png" class="screenshot" style="width: 668px;">

And doing one more search, I can find the value of the config setting:

<img src="/images/2024/wmc-inspector-search-4.png" class="screenshot" style="width: 668px;">

Looking up the name of that config setting (`wgIllegalFileChars`) led me to a page in the [MediaWiki documentation](https://www.mediawiki.org/wiki/Manual:$wgIllegalFileChars) which describes the behaviour in more detail.

Looking back, I'm not sure I quite followed the right path.
I don't think `makeTitleInFileNS` throws an exception; instead, it sets the title to `null` if it contains illegal characters.
There's another place you can get the `mwe-upwiz-error-title-invalid` error if the title is empty, but it's less obvious what's setting the title in this context:

<img src="/images/2024/wmc-inspector-search-5.png" class="screenshot" style="width: 668px;">

