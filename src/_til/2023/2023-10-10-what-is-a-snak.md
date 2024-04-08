---
layout: til
date: 2023-10-10 15:42:27 +0000
title: Why the term "snak" keeps appearing in the Wikidata API
tags:
  - wikimedia-commons
  - naming-things
---
This is one of those terms I kept seeing in API responses and documentation, but it wasn't immediately obvious to me what it means.
I found an explanation in the [Wikibase/DataModel](https://www.mediawiki.org/wiki/Wikibase/DataModel#Overview_of_the_data_model) docs:

> For lack of a better name, any such basic assertion that one can make in Wikidata is called a **Snak** (which is small, but more than a byte). This term will not be relevant for using Wikidata (editors will not encounter it), but it is relevant for developers to avoid confusion with Statements or other claims.
