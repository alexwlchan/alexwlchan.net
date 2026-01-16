---
layout: til
title: What is the `author_name` in the list of tags on a Flickr photo?
summary: |
  When you call the `flickr.photos.getInfo` API, each tag is attributed to an author. The `author_name` is their username, not their realname.
date: 2024-10-24 10:00:15 +01:00
tags:
  - flickr
---
When you look up a photo with the `flickr.photos.getInfo` API, you get a list of tags on the photo, including the NSID and "authorname" of the Flickr member who added the tag.

Here's an example (emphasis mine):

<pre><code>&lt;rsp stat="ok"&gt;
  &lt;photo id="2179931434"…&gt;
    …
    &lt;tags&gt;
      &lt;
        tag id="8602872-2179931434-6656"
        <strong>author="7745644@N04"</strong>
        <strong>authorname="allenellisdewitt"</strong>
        raw="farming" machine_tag="0"&gt;farming&lt;/tag&gt;
    &lt;/tags&gt;
  &lt;/photo&gt;
&lt;/rsp&gt;</code></pre>

A Flickr member can have two names: a `username` and a `realname`.
Which is it?

We can confirm that it's the `username` with the `flickr.people.getInfo` API.

<pre><code>&lt;rsp stat="ok"&gt;
  &lt;person <strong>id="7745644@N04"</strong> …&gt;
    <strong>&lt;username&gt;allenellisdewitt&lt;/username&gt;</strong>
    <strong>&lt;realname&gt;Allen DeWitt&lt;/realname&gt;</strong>
    …
  &lt;/person&gt;
&lt;/rsp&gt;</code></pre>
