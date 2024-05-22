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

    <div class="language-console highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="gp">$</span><span class="w"> </span>curl <span class="s1">'https://commons.wikimedia.org/w/api.php?action=query&amp;format=xml&amp;titles=File:Herestraat%20Groningen.JPG'</span>
<span class="go">&lt;?xml version="1.0"?&gt;</span>
<span class="go">&lt;api batchcomplete=""&gt;</span><span class="w">
</span><span class="go">  &lt;query&gt;</span><span class="w">
</span><span class="go">    &lt;pages&gt;</span><span class="w">
</span><span class="go">      &lt;page _idx="128" pageid="128" ns="6" title="File:Herestraat Groningen.JPG"/&gt;</span><span class="w">
</span><span class="go">    &lt;/pages&gt;</span><span class="w">
</span><span class="go">  &lt;/query&gt;</span><span class="w">
</span><span class="go">&lt;/api&gt;</span><span class="w">
</span></code></pre></div> </div>

2.  To go from numeric ID to filename, go to `https://commons.wikimedia.org/?curid=[ID]`.

    For example, <https://commons.wikimedia.org/?curid=128>.

    Alternatively, you can use the Query API with the `pageids` parameter.
    For example:

    <div class="language-console highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="gp">$</span><span class="w"> </span>curl <span class="s1">'https://commons.wikimedia.org/w/api.php?action=query&amp;format=xml&amp;pageids=128'</span>
<span class="go">&lt;?xml version="1.0"?&gt;</span><span class="w">
</span><span class="go">&lt;api batchcomplete=""&gt;</span><span class="w">
</span><span class="go">  &lt;query&gt;</span><span class="w">
</span><span class="go">    &lt;pages&gt;</span><span class="w">
</span><span class="go">      &lt;page _idx="128" pageid="128" ns="6" title="File:Herestraat Groningen.JPG"/&gt;</span><span class="w">
</span><span class="go">    &lt;/pages&gt;</span><span class="w">
</span><span class="go">  &lt;/query&gt;</span><span class="w">
</span><span class="go">&lt;/api&gt;</span><span class="w">
</span></code></pre></div> </div>

There's a Python implementation of this code [in Flickypedia], which includes some tests.

[query]: https://www.mediawiki.org/wiki/API:Query
[namespaces]: https://commons.wikimedia.org/wiki/Help:Namespaces
[in Flickypedia]: https://github.com/Flickr-Foundation/flickypedia/blob/11b6f675df851298b665940e9c378efdbd59de5d/src/flickypedia/apis/wikimedia/identifier_methods.py
