---
layout: til
date: 2023-10-16 16:45:35 +00:00
title: Find files that use a particular SDC field
tags:
  - wikimedia commons
  - sparql
---
## Using Special:MediaSearch

You can do structured data queries using [Special:MediaSearch](https://www.mediawiki.org/wiki/Help:MediaSearch#Statements_and_structured_data).
Here are a couple of examples:

*   To find uses of a particular statement:

    *   Videos with property P1651 (YouTube video ID): <https://commons.wikimedia.org/wiki/Special:MediaSearch?type=video&search=haswbstatement%3AP1651>
    *   Images with property P12120 (Flickr photo ID): <https://commons.wikimedia.org/wiki/Special:MediaSearch?type=image&search=haswbstatement%3AP12120>

*   To find a statement with a particular value:

    *   Images with P7482=Q66458942 (source of file is original creation by uploader): <https://commons.wikimedia.org/wiki/Special:MediaSearch?search=haswbstatement%3AP7482%3DQ66458942&type=image>

## Using the Commons Query Service

You can run SPARQL queries with the [Commons Query Service](https://commons.wikimedia.org/wiki/Commons:SPARQL_query_service).
I'm not super experienced with SPARQL, but I'll use this as a place to gather queries I've been able to get working.

*   This is a query that finds files which have a P7482=Q74228490, P137=Q420747, and one of two Flickr URLs in the P973 field.

    ```sparql
    SELECT ?item ?described_url WHERE {
      ?item wdt:P7482 wd:Q74228490 .       # P7482 (source of file) = Q74228490 (file available on the internet)
      ?item p:P7482 ?statement .
      ?statement pq:P137 wd:Q103204.       # P137 (operator) = Q420747 (National Library of Finland)
      ?statement pq:P973 ?described_url.
      VALUES (?described_url) { (<https://www.flickr.com/photos/sunrise/29916169/>) (<https://www.flickr.com/photos/sunrise/29916169>) }
    } LIMIT 1
    ```

    [Link to query in WCQS](https://commons-query.wikimedia.org/#SELECT%20%3Fitem%20%3Fdescribed_url%20WHERE%20%7B%0A%20%20%3Fitem%20wdt%3AP7482%20wd%3AQ74228490%20.%20%20%20%20%20%20%20%23%20P7482%20%28source%20of%20file%29%20%3D%20Q74228490%20%28file%20available%20on%20the%20internet%29%0A%20%20%3Fitem%20p%3AP7482%20%3Fstatement%20.%0A%20%20%3Fstatement%20pq%3AP137%20wd%3AQ103204.%20%20%20%20%20%20%20%23%20P137%20%28operator%29%20%3D%20Q420747%20%28National%20Library%20of%20Finland%29%0A%20%20%3Fstatement%20pq%3AP973%20%3Fdescribed_url.%0A%20%20VALUES%20%28%3Fdescribed_url%29%20%7B%20%28%3Chttps%3A%2F%2Fwww.flickr.com%2Fphotos%2Fsunrise%2F29916169%2F%3E%29%20%28%3Chttps%3A%2F%2Fwww.flickr.com%2Fphotos%2Fsunrise%2F29916169%3E%29%20%7D%0A%7D%20LIMIT%201), which returns a single result.

*   This is a query that finds users with a particular value in the Flickr User ID field:

    ```sparql
    SELECT ?image WHERE {
      # P170 (creator) / P3267 (Flickr user ID) = specified ID
      ?file p:P170 ?creator .
      ?creator pq:P3267 "52498302@N08" .

      # Retrieve the image URL to display as a link
      ?file schema:url ?image .
    }
    ```

    [Link to query in WCQS](https://commons-query.wikimedia.org/#SELECT%20%3Fimage%20WHERE%20%7B%0A%20%20%23%20P170%20%28creator%29%20%2F%20P3267%20%28Flickr%20user%20ID%29%20%3D%20specified%20ID%0A%20%20%3Ffile%20p%3AP170%20%3Fcreator%20.%0A%20%20%3Fcreator%20pq%3AP3267%20%2252498302%40N08%22%20.%0A%20%20%0A%20%20%23%20Retrieve%20the%20image%20URL%20to%20display%20as%20a%20link%0A%20%20%3Ffile%20schema%3Aurl%20%3Fimage%20.%0A%7D%0A)
