---
layout: til
date: 2023-12-08 20:58:33 +0000
title: Go between M-IDs and filenames on Wikimedia Commons
tags:
  - wikimedia-commons
---
Every file on Wikimedia Commons has two identifiers:

*   A filename, e.g. `File:Herestraat Groningen.JPG`.
    This always starts with `File:` because these are pages in the [File namespace][namespaces]
*   A numeric identifier, e.g. `M128`.
    This is a unique dientifier for each file on Commons, similar to Q IDs for entities on Wikidata.

The APIs for searching/updating Wikimedia Commons typically accept both forms; sometimes it's convenient to go between the two.

1.  To go from filename to numeric ID, you can use the [Query API][query] and do a search with the `titles` parameter.
    The M ID is included in the response.

    For example:

    ```console
    $ curl 'https://commons.wikimedia.org/w/api.php?action=query&format=xml&titles=File:Herestraat%20Groningen.JPG'
    <?xml version="1.0"?>
    <api batchcomplete="">
      <query>
        <pages>
          <page _idx="128" pageid="128" ns="6" title="File:Herestraat Groningen.JPG"/>
        </pages>
      </query>
    </api>
    ```

2.  To go from numeric ID to filename, go to `https://commons.wikimedia.org/?curid=[ID]`.

    For example, <https://commons.wikimedia.org/?curid=128>.

    Alternatively, you can use the Query API with the `pageids` parameter.
    For example:

    ```console
    $ curl 'https://commons.wikimedia.org/w/api.php?action=query&format=xml&pageids=128'
    <?xml version="1.0"?>
    <api batchcomplete="">
      <query>
        <pages>
          <page _idx="128" pageid="128" ns="6" title="File:Herestraat Groningen.JPG"/>
        </pages>
      </query>
    </api>
    ```

[query]: https://www.mediawiki.org/wiki/API:Query
[namespaces]: https://commons.wikimedia.org/wiki/Help:Namespaces
