---
layout: post
date: 2021-03-29T10:48:12.797Z
title: Building Wellcome Collection's new unified catalogue search
summary: Collaboration between our digital and collections teams helped to build a single search box for all of our catalogues.
tags:
  - wellcome collection
  - search
canonical_url: https://stacks.wellcomecollection.org/building-our-new-unified-collections-search-ed399c412b01
colors:
  index_light: "#63605f"
  index_dark:  "#d4d2cc"
---
*I wrote this article while I was working at Wellcome Collection. It was originally published [on their Stacks blog](https://stacks.wellcomecollection.org/building-our-new-unified-collections-search-ed399c412b01) under a CC BY 4.0 license, and is reposted here in accordance with that license.*

<p>One of the key features of the new Wellcome Collection website is our <a href="https://wellcomecollection.org/collections">unified collections search</a>.</p>

{%
  picture
  filename="1*yylbOkcv7M-D5CcYOt2u3w.png"
  width="750"
  class="screenshot"
  alt="A search box labelled “Search the catalogue” with two tabs: “Library catalogue” and “Images”. To the right is a green button labelled “Search”. The search is for “suez canal” and shows two search results."
%}

<p>On the old Wellcome Library and Wellcome Images websites, we had different search tools for different types of records. Each tool would present a different view of the data, and you had to work out which tool would find the information you needed.</p><p>We had one tool that would search all our catalogues, but it lost a lot of the structure from the underlying data. We had other tools that would preserve the structure and detail, but only included a subset of the catalogue. Yet another tool would search our image collections. Our new search no longer forces you to choose: <strong>a single search box searches everything, and with all the detail and functionality our users expect.</strong></p><p>This has been a significant technical challenge, with input from teams across Wellcome Collection. In this post, I’m going to explain how we built this feature.</p>

---

<h2>Why did we have different search boxes?</h2>

<figure>
  {%
    picture
    filename="1*NlNlV_i2hio5htAGADHvIw.png"
    width="750"
    class="screenshot"
    alt="Screenshot of the “Which search tool should I use?” page from the old Library website."
  %}
  <figcaption>You won’t find this page on our new website.</figcaption>
</figure>

<p>Like many institutions, our collections data is split across multiple systems — including Calm for our archives, <a href="https://www.iii.com/products/sierra-ils/">Sierra</a> for our library catalogue, an image asset catalogue called Miro, and our <a href="/2020/archival-storage-service/">cloud storage</a> for digitised material. Each system is designed to store a particular kind of data, and there’s no one-size-fits-all system that could record all our collections in the level of detail we want.</p><p>The different search boxes were for searching different systems, and a user had to know how and where we might have recorded something. The different systems are important to our collections team, but we didn’t want online visitors to have to worry about this distinction.</p>

---

<h2>How our unified search works</h2><h3>Create a read-only copy of every source catalogue</h3><p>Our catalogue data is split across different systems, and each of those systems has its own API for accessing the data. The first step is to build some services that use those APIs to read data out of each system.</p>

{%
  picture
  filename="1*ze-zPsDn5J7EanZ_JwlzvQ.png"
  width="500"
  alt="A diagram showing arrows from three APIs on the left to three databases on the right. Each API/database pair has a different brown/cream-coloured shape."
%}

<p>To minimise load on the source systems, we read the data out once, and then we save it to a database that we manage (one database per source). As records are edited or created, we update the copy in our own database — and that’s what we use for the website search.</p><p>This gives us a copy of the data that we can query or transform extremely quickly, without slowing down or affecting the source systems.</p><p>We call these services <em>“adapters”</em>. Like an electrical plug, these adapters provide a common interface — in this case, for getting data from our source systems. The adapters handle all the complexity of talking to the source system APIs, and all our other services can read from the managed databases, regardless of the original source system.</p><p>As much as possible, we store an exact copy of the data as we received it from the original system. At this stage, we try not to do any processing or transformation.</p><p>This is a read-only copy of the data. We’re not trying to replace or supplant the source systems as the canonical copy of our catalogue. Doing so would be massively disruptive, and add very little value to this process.</p><p>Right now, our adapters only pull in catalogue records, but this approach would allow us to bring in other types of data that don’t traditionally live in a catalogue — things like OCR for our digitised items, <a href="https://stacks.wellcomecollection.org/tei-for-manuscript-description-at-wellcome-collection-a2b8f52524e2">TEI descriptions of manuscripts</a>, or the output from <a href="https://stacks.wellcomecollection.org/a-new-kind-of-image-search-5870c2cdadcb">our machine learning models</a>.</p>

<h3>Transform each record into a common model</h3>

<p>All of our source catalogues store data in a different way — for example, our archives catalogue uses <a href="https://en.wikipedia.org/wiki/ISAD(G)">ISAD(G)</a>, whereas our library catalogue uses <a href="https://en.wikipedia.org/wiki/MARC_standards">MARC</a>.</p><p>We could build a unified search by searching every catalogue individually, and then combining the results — but putting the results in a sensible order would be very tricky.</p>

{%
  picture
  filename="1*_X5vD-np5M3K4NtAo_8qdw.png"
  width="500"
  alt="The brown shapes from the previous diagram being transformed into green circles."
%}

<p>Instead, we transform each of the source records into a common model — so we can store and search them as one big collection. This common model is called a <a href="https://developers.wellcomecollection.org/catalogue/v2/models/work">“Work”</a>, and we’ve designed it so that it can store all the data we want to present publicly.</p><p>Using a new model — rather than using one of the models from the source records — allows us to keep all the structure of the source catalogues. Among other things, it preserves the hierarchy and relationships between works in our archives catalogue. The combined search on our old website squashed ISAD(G) into MARC, which lost a lot of this structure and made archives harder to navigate. Our new model has no such restrictions.</p><p>We have a different transformation process for each source catalogue, based on how it structures its data. For example, the “title” on a Work created from our Calm catalogue comes from the “Title” field, whereas a Work from our Sierra catalogue uses MARC field 245. These processes are very Wellcome-specific, and they come from lots of conversations between our collections and digital teams. We tweak the transformation on a regular basis, to try to improve the quality of data on a Work.</p>

<h3>Combine works that refer to the “same” thing</h3><p>Sometimes we have multiple source records that describe the same object, and we want to combine them into a single Work.</p>

{%
  picture
  filename="1*UcfhxyQ2WkPINF-AkBvHvA.png"
  width="500"
  alt=""
%}

<p>For example, we might have a library book that we’ve digitised. This would have (at least) two records: one in the library catalogue, one in our cloud storage. We want to combine these together, so that if somebody comes to the page for the library catalogue record, they’ll see the digitised copy of the book on the same page.</p><p>We look for matching identifiers in the source records, and if we find any, we try to merge the resulting Works into a single Work (and redirect the others to this new Work). The merging process combines the data from all the individual Works according to a set of rules which are designed as a close collaboration between our digital team and collections staff. As the original records get updated, we update these merges, combining or splitting Works to reflect the latest data in the underlying catalogue.</p>

### Add a new identifier

<p>All of our catalogue systems use different identifier schemes. One system might use UUIDs, another an auto-incrementing integer, another a human-written reference number. We didn’t want to rely on any of these schemes — we wanted something that would look consistent, and which was independent of those systems. If we replace one of our catalogue systems, we want our IDs and our website URLs to keep working.</p><p>When we were deciding how to identify works, we came up with a couple of desirable properties:</p><ul><li><em>Identifiers should be URL safe. </em>Each Work has a page at /works/{id}, so we want an ID that you can put in a URL.</li><li><em>Identifiers should be short.</em> This is what I call the “post-it note test”: could somebody scribble down an ID on a post-it note, and still read it later?</li><li><em>No ambiguous characters</em>. Similar-looking characters like o/O/0 or l/I cause all manner of confusion, and we’d prefer not to use them.</li></ul>

{%
  picture
  filename="1*HBBGURDF4ce5jqi7IzcHNQ.png"
  width="500"
  alt=""
%}

<p>We generate our own “canonical” identifiers, which look like <em>jn3aavyr</em> or <em>xwkfdhhz</em>. Even with ambiguous characters removed, that gives us nearly a trillion identifiers, which is plenty.</p><p>We always generate exactly one canonical identifier for each source identifier — they are meant to augment the existing source identifiers, not replace them.</p>

### Put the works in a search index

<p>We put every work in the same search index — regardless of source system. By running queries against that index, we can search records from across all of our catalogues, and get a single set of results.</p>

{%
  picture
  filename="1*O5oZzA-gzWzMfbwbl8o5Pw.png"
  width="500"
  alt=""
%}

<p>We have a publicly available <a href="https://developers.wellcomecollection.org/catalogue">Catalogue API</a> that anybody can use to search our collections, and we use the same API for the search on our website. This API is making queries directly against the search index, and includes filters and aggregations to help people narrow down what they’re looking for.</p><p>Over time, we can tweak the queries, which we hope will improve the quality of search results. For example, we can adjust the importance of certain fields, change how the data is analysed, or vary the amount of fuzziness allowed when matching a word.</p>

<h2>Putting it all together</h2>

<p>This is a fairly standard <a href="https://en.wikipedia.org/wiki/Extract,_transform,_load">ETL pipeline</a>. We <strong>extract</strong> data from our catalogue systems, we <strong>transform</strong> it into our common Work model, and we <strong>load</strong> it into a search index.</p><p>This system is pretty flexible, and will allow us to add more sources in future. These could be entirely new catalogues, or data to enrich our existing works.</p><p>The hard part is, as ever, understanding the context. We can extract and load the data pretty easily, but we can only write the transformation process when we know what the data means. What is this field used for? How is this sort of record catalogued? How do our collections team think about this data? And so on.</p><p><strong>Building our unified collections search has been an iterative, collaborative process.</strong> There are lots of conversations between our digital and collections teams, trying to get us all to a common understanding of how our catalogues work. We use that understanding to design and implement the transformation process — and in turn, we have more conversations when people can see the output. We’re continually tweaking and improving how this pipeline works.</p><p><em>Thanks to Ashley Ray, Christy Henshaw, Jamie Parkinson, Lalita Kaplish and Tom Scott for their help reviewing drafts of this post.</em></p>
