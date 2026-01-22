---
layout: til
date: 2023-11-30 00:27:25 +01:00
title: Why I prefer XML to JSON in the Wikimedia Commons APIs
summary: |
  The XML-to-JSON conversion leads to some inconsistent behaviour, especially in corner cases of the API.
tags:
  - wikimedia commons
---
The Wikimedia APIs I've used can return results in three formats: HTML, JSON, and XML.
Initially I was using the JSON APIs because JSON is easy, it's familiar, there are built-in methods for it my HTTP client libraries.

It seems like at least some of the APIs are doing an automated XML-to-JSON translation, which has inconsistent results in certain corner cases.
This is why I'm gradually leaning towards the XML APIs, which seem to be more consistent in how they behave.

This is a useful example of automated XML-to-JSON risks in general.

## The `languagesearch` API

First let's go ahead and use then [Languagesearch API](https://www.mediawiki.org/wiki/API:Languagesearch) to find a list of languages which match the query "english":

```console
$ curl 'https://en.wikipedia.org/w/api.php?action=languagesearch&search=english&format=json' | jq .
{
  "languagesearch": {
    "en": "english",
    "en-us": "english sa america",
    "en-au": "english sa australia",
    …
  }
}

$ curl 'https://en.wikipedia.org/w/api.php?action=languagesearch&search=english&format=xml' | xmllint --format -
<?xml version="1.0"?>
<api>
  <
    languagesearch
    en="english"
    en-us="english sa america"
    en-au="english sa australia"
    …
  />
</api>
```

The JSON contains an object which maps language ID to name; the XML uses language IDs as attributes and names as values.

Now let's try that query again, with a query that won't return any results;

```console
$ curl 'https://en.wikipedia.org/w/api.php?action=languagesearch&search=doesnotexist&format=json' | jq .
{
  "languagesearch": []
}

$ curl 'https://en.wikipedia.org/w/api.php?action=languagesearch&search=doesnotexist&format=xml' | xmllint --format -
<?xml version="1.0"?>
<api>
  <languagesearch/>
</api>
```

Notice that the structure of the JSON response has changed slightly -- where previously it returned an object, now it returns an array.
Meanwhile the XML response looks just as before, just without any attributes.

This broke my JSON-using code, because I was assuming the `languagesearch` value would always be a mapping, and that worked until I tested the empty case.
