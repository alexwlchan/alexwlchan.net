---
layout: page
title: Projects
---

For my day job, I help to build digital services at <a href="https://wellcomecollection.org/">Wellcome Collection</a>, to help people discover and use the collections.
My particular interest is in digital preservation, and I enjoy the future-proofing that involves.
Sometimes it's designing a storage repository that doesn't rely on the continued existence of a given software stack, sometimes it's writing code with enough comments to make sense to future developers.

Outside work, I try to do stuff that's fun, stuff that doesn't have any practical purpose.
If it's colourful, pretty, or whimsical, I'm there.
That could be [software](#fun-stuff), or [short stories](https://archiveofourown.org/users/alexwlchan/pseuds/alexwlchan), or [stitching](https://twitter.com/alexwlchan/status/1375920499717464071).
I used to contribute to open-source Python projects, but I've mostly stopped – these days, I try to minimise the free time I spend coding.

I love sharing what I've learnt.
I've had some great teaching, and my blog posts and conference talks are how I pay that favour forward.
There are hundreds of posts on this site, quite a few others elsewhere, and you may have seen me speaking at events like [PyCon UK](https://2019.pyconuk.org) and [Monki Gras](https://monkigras.com).

This page lists some of my projects, so you can get an idea of what I've been up to:

- [Wellcome Collection](#wellcome-collection)
- [Writing](#writing)
- [Talks and workshops](#talks-and-workshops)
- [Conference organisation](#conference-organisation)
- [Personal tools](#personal-tools)
- [Open-source software](#open-source-software)
- [Fun stuff](#fun-stuff)

**Interested in anything on this page? Want to know more? [Get in touch](/#contact)!**



<style>
  dt:not(:first-child) {
    margin-top: 20px;
  }

  dd {
    margin-left: 20px;
  }

  /* Styles for lists that have an image hovering out to the right.
   * When the screen is narrow, the image moves to be inline with the text.
   */

  .illustrated_list .illustrated_item:not(:last-child) {
    margin-bottom: 1em;
  }

  .illustrated_list {
    padding-left: 0;
  }

  .illustrated_item {
    display: grid;
    grid-column-gap: 1em;
    grid-template-columns: auto auto;
  }

  /* Vertically centre the text that appears alongside the image */
  .illustrated_item dl {
    margin-top:    auto;
    margin-bottom: auto;
  }

  .illustrated_item a:hover img {
    opacity: 0.65;
  }

  /*
    On desktop browsers, the image appears off to the right.  We use
    max-height instead of height so it maintains the correct aspect
    ratio on small screens.

    On mobile browsers, the image appears vertically inline with the text.
  */
  .illustrated_item a img {
    max-height: 150px;
    border-radius: 3px;
  }

  @media screen and (min-width: 500px) {
    .illustrated_item {
      height: 150px;
    }
  }

  @media screen and (max-width: 500px) {
    .illustrated_item {
      grid-template-columns: auto;
    }

    .illustrated_item .img_wrapper {
      background-opacity: 0;
    }

    .fun_image {
      margin-top: 1em;

      /* This ensures that the background colour doesn't span the full width
       * of the page on a small device.
       */
      margin-left:  auto;
      margin-right: auto;
    }
  }

  #howlongismydata:hover {
    background: rgba(255, 71, 255, 0.2);
  }

  #howlongismydata img {
    border: 0.5px solid #ff47ff;
  }

  #rainbowhearts:hover, #rainbowvalknuts:hover {
    background: rgba(34, 34, 34, 0.3);
  }

  #rainbowhearts img, #rainbowvalknuts img {
    border: 0.5px solid #222;
  }

  #booktracker:hover {
    background: rgba(157.30927835051543,65.30927835051551,141.04123711340196, 0.3);
  }

  #booktracker img {
    border: 0.5px solid rgb(157.30927835051543,65.30927835051551,141.04123711340196);
  }

  #kempisbot:hover {
    background: rgba(85, 172, 238, 0.3);
  }

  #kempisbot img {
    border: 0.5px solid rgba(85, 172, 238, 0.7);
  }

  #finduntaggedtumblrposts:hover {
    background: rgba(43, 99, 151, 0.3);
  }

  #finduntaggedtumblrposts img {
    border: 0.5px solid rgba(43, 99, 151, 0.5);
  }

  #ukstationsmap:hover {
    background: rgba(0, 194, 52, 0.4);
  }

  #ukstationsmap img {
    border: 0.5px solid #333;
  }

  #specktre:hover, #happybackgrounds:hover {
    background: none;
  }

  #happybackgrounds img {
    border: 0.5px solid #c24401;
  }
</style>


## Wellcome Collection

I've been a software developer at <a href="https://wellcomecollection.org/">Wellcome Collection</a> since 2017, which is a museum and library exploring health and human experience.
I help to build digital services that present and preserve the collections, making them more accessible and discoverable.
All of our work is in public GitHub repositories and available under an MIT licence.
The projects I've worked on include:

<dl>
  <dt><a href="https://github.com/wellcomecollection/storage-service">Storage service</a></dt>
  <dd>
    The storage service is the preservation repository for Wellcome’s digital collections.
    It uploads files to cloud storage providers like Amazon S3 and Azure Blob, and ensures the integrity and correctness of the files.
    I was part of the team that built the original storage service, and I handle ongoing maintenance and debugging.
    Recently I’ve been working on documentation and a demo, so that other institutions can try running the storage service.
  </dd>

  <dt><a href="https://developers.wellcomecollection.org/catalogue">Catalogue API</a></dt>
  <dd>
    The Catalogue API provides a unified search for the museum and library collections.
    I’m one of the developers who works on the Catalogue API and its associated infrastructure.
  </dd>

  <dt><a href="https://stacks.wellcomecollection.org">Stacks development blog</a></dt>
  <dd>
    I’ve written a number of articles for the development blog, explaining key pieces of work and sharing what we’ve learnt.
    See a list of <a href="/elsewhere#stacks-development-blog-for-wellcome-collection">articles I’ve written</a>.
  </dd>

  <dt><a href="https://wellcome.org/news/our-trans-inclusion-policy-latest-step-making-wellcome-more-inclusive">Trans inclusion policy</a></dt>
  <dd>
    I helped write Wellcome’s trans inclusion policy and guidance, which provides advice for trans staff and their managers and colleagues.
  </dd>
</dl>



## Writing

<dl>
  <dt><a href="https://alexwlchan.net/posts/" aria-label="alex w l chan dot net" aria-braillelabel="alexwlchan.net">alexwlchan.net</a></dt>
  <dd>
    This site started as a place where I could practice my writing; I’ve since written over 300 posts.
    There’s no consistent theme – I have a lot of posts about programming, but plenty for non-programmers as well.
  </dd>

  <dt><a href="https://www.lastweekinaws.com/blog/">Last Week in AWS</a></dt>
  <dd>
    Last Week in AWS is a publication that talks about news from the world of AWS and cloud computing.
    I’m a guest writer for their AWS blog, and you can see a list of <a href="/elsewhere#last-week-in-aws">articles I’ve written</a>.
  </dd>

  <dt><a href="https://stacks.wellcomecollection.org/">Wellcome Collection development blog</a></dt>
  <dd>
    The development blog describes work that’s been happening at Wellcome Collection.
    Sometimes I write about projects my team has been working on, and you can see a list of <a href="/elsewhere#stacks-development-blog-for-wellcome-collection">articles I’ve written</a>.
  </dd>

  <dt><a href="https://archiveofourown.org/users/alexwlchan/pseuds/alexwlchan">Fiction on AO3</a></dt>
  <dd>
    I’ve written a small amount of fiction, which is posted on AO3.
    This is light-hearted writing and something I’d like to do more of.
  </dd>
</dl>



## Talks and workshops

<figure style="width: 350px; display: inline-block; float: right; margin-left: 1em;">
  {%
    picture
    filename="pyconuk-speaking.jpg"
    visible_width="350px"
    parent="/images/projects"
    alt="A person in a green top standing at a podium, in front of a large screen with the words “duplicate bugs”."
  %}
  <figcaption>
    Espousing the benefits of sans I/O programming at PyCon UK 2019.
    The coordination of my slides, jumper and eyeshadow is entirely deliberate.
    Image courtesy <a href="https://www.flickr.com/photos/184390836@N04/48726548731/">Mark Hawkins</a>.
  </figcaption>
</figure>

I've given talks and workshops at a number of conferences.
If you'd like me to speak at your event, [get in touch](/#contact) for details.

These are a few of my favourites:

<dl>
  <dt><a href="{% post_url 2019/2019-01-31-monki-gras-the-curb-cut-effect %}">The Curb Cut Effect</a></dt>
  <dd>
    A collection of stories about the “curb cut effect”: the idea that making something better for disabled people can make it better for everyone.
  </dd>

  <dt><a href="/a-plumbers-guide-to-git/">A Plumber’s Guide to Git</a></dt>
  <dd>
    This is a two-hour workshop about the inner workings of Git (the “plumbing” commands).
    The goal is to give participants a better understanding of Git’s internal data structures, so they can be more confident and capable Git users.
    My notes are available online.
  </dd>

  <dt><a href="https://www.youtube.com/watch?t=47m10s&v=hGI95LWVeuk">A robot stole my job!</a></dt>
  <dd>
    A fun lightning talk about the unexpected consequences of build automation.
  </dd>

  <dt><a href="{% post_url 2018/2018-09-24-assume-worst-intent %}">Assume worst intent</a></dt>
  <dd>
    If you’re designing services, it’s important to think about how they might be misused to hurt people.
    If you don’t think about this upfront, your users will find out the hard way.
  </dd>

  <dt><a href="{% post_url 2019/2019-10-14-sans-io-programming %}">Sans I/O programming patterns: what, why, and how</a></dt>
  <dd>
    I make my case for an approach to programming that gives you code which is dramatically simpler and easier to test.
  </dd>
</dl>

If you want to see all of my talks, I have [a complete list](/elsewhere#talks-and-workshops).



## Conference organisation

<dl>
  <dt><a href="https://2020.pyconuk.org/">PyCon UK</a></dt>
  <dd>
    I helped to organise PyCon UK from 2016 to 2022.
    PyCon UK is a community conference celebrating the use of Python in the UK.
    I worn many hats in this role, including organising the schedule, maintaining the website, and helping at the reception desk.
  </dd>

  <dt><a href="https://alexwlchan.net/ideas-for-inclusive-events/">Ideas for inclusive events</a></dt>
  <dd>
    This is my ideas and suggestions for running inclusive, accessible events.
    It’s important for events to welcome as wide a range of people as possible.
    This is based on my experience both organising and attending in-person tech events, but these ideas aren’t tech specific.
  </dd>
</dl>



## Personal tools

These are tools I’ve written that make my life easier.
Usually they solve a very specific problem and I don’t expect anybody else to use them directly, but I publish the source code and my notes in case they’re a useful source of ideas.

<dl>
  <dt><a href="https://github.com/alexwlchan/docstore">docstore</a></dt>
  <dd>
    A tool for organising my scanned documents and reference files with keyword tagging.
    There’s a CLI to store files, and a web app to search for previously-stored files.
  </dd>

  <dt><a href="https://github.com/alexwlchan/dominant_colours" aria-label="dominant colours">dominant_colours</a></dt>
  <dd>
    A command-line tool to find the dominant colours in an image.
    It prints a palette of colours in your terminal.
  </dd>

  <dt><a href="https://github.com/alexwlchan/safari.rs" aria-label="safari dot rs" aria-braillelabel="safari.rs">safari.rs</a></dt>
  <dd>
    A command-line tool for getting data from Safari, like the URL of the frontmost window or the number of open tabs.
    I also use it for a text expansion macro: I can type <code>;furl</code> in any app, and it gets replaced by the frontmost URL (with tracking parameters automatically removed).
  </dd>

  <dt><a href="https://github.com/alexwlchan/highlight-twitter-alt-text">highlight-twitter-alt-text</a></dt>
  <dd>
    A collection of CSS and JavaScript snippets I use to show alt text in my Twitter timeline (or highlight its absence).
  </dd>

  <dt><a href="https://github.com/wellcomecollection/ingest-inspector">ingest-inspector</a></dt>
  <dd>
    This is a tool for looking up ingests in the Wellcome storage service.
    I love this as an example of solving one problem and solving it well – the ingests are also available in a Kibana instance, but a dedicated viewer means I can design it to make it as easy as possible to understand ingests.
  </dd>

  <dt><a href="https://github.com/alexwlchan/ao3">ao3-python</a></dt>
  <dd>
    Since AO3 doesn’t have an official API, I wrote a small Python library that provides a scripted interface to AO3 data by scraping the page HTML.
  </dd>
</dl>



## Open-source software

I've writen dozens of small patches for open-source software, mostly fixing typos or small bugs.
I'm not currently taking an active maintainer role in anything, but these are a few projects where I've made larger contributions in the past:

<dl>
  <dt><a href="https://github.com/loris-imageserver/loris">Loris</a> </dt>
  <dd>
    Loris is a <a href="http://iiif.io/api/image/2.0/"><abbr aria-label="triple eye F" aria-braillelabel="IIIF">IIIF</abbr> Image API server</a>, written in Python by Jon Stroop.
    While Loris was in use at Wellcome, I was one of two Loris maintainers.
    I’m particularly pleased with the <a href="https://github.com/loris-imageserver/loris/blob/development/loris/jp2_extractor.py">revised JPEG 2000 parser</a> I wrote.
    (Wellcome stopped using Loris in 2021.)
  </dd>
  <dt><a href="https://github.com/urllib3/urllib3" aria-label="url lib 3">urllib3</a></dt>
  <dd role="text">
    <span class="visually-hidden">url lib 3</span><span aria-hidden="true">urllib3</span> is an HTTP client for Python.
    In 2017, I did a significant amount of work on the test suite: migrating it from <span class="visually-hidden">nose tests</span><span aria-hidden="true">nosetests</span> to py.test, and cleaning up file descriptor leaks.
  </dd>
  <dt><a href="https://github.com/pyca/pyopenssl/">PyOpenSSL</a></dt>
  <dd>
    PyOpenSSL is a Python wrapper around the OpenSSL library.
    In 2016, I helped them migrate their test suite from unittest to py.test-style.
  </dd>
  <dt><a href="https://github.com/HypothesisWorks/hypothesis/">Hypothesis</a></dt>
  <dd>
    Hypothesis is a property-based testing library in Python, written by David MacIver.
    I was the second maintainer on the project, mostly working on the CI and build system.
  </dd>

  <dt><a href="https://nrich.maths.org/mathmoApp/#/mathmo">Mathmo</a></dt>
  <dd>
    Mathmo is a tool that generates maths exercises for A-level students, developed as part of the <a href="https://nrich.maths.org" aria-label="n rich project" aria-braillelabel="NRICH Project">NRICH Project</a>.
    As part of a summer job, I did some work to refactor the codebase and add several new types of question.
  </dd>
</dl>



## Fun stuff

{% comment %}
  All images should have the same ratio, so they look consistent.

  Currently 503x444, which is an admittedly arbitrary choice.
{% endcomment %}

<ul class="illustrated_list">
  <li class="illustrated_item">
    <dl>
      <dt>
        <a href="https://howlongismydata.glitch.me">How long is my data?</a>
      </dt>
      <dd role="text">
        Measure data in the shelving space you’d need if you stored it as a series of <span class="visually-hidden">3&frac12; inch</span><span aria-hidden="true">3&frac12;&Prime;</span> floppy disks.
      </dd>
    </dl>
    <a href="https://howlongismydata.glitch.me" id="howlongismydata" class="fun_image">
      <img src="/images/projects/howlongismydata.png" alt="A white page with two rows of pink floppy disks and a title 'How long is my data?'">
    </a>
  </li>

  <li class="illustrated_item">
    <dl>
      <dt>
        <a href="http://rainbow-hearts.glitch.me/">Rainbow hearts</a>
      </dt>
      <dd>
        Create pairs of interlocking hearts in a variety of Pride flags.
        They use some SVG masking techniques I wrote about <a href="{% post_url 2021/2021-03-12-inner-outer-strokes-svg %}">in a blog post</a>.
      </dd>
    </dl>
    <a href="http://rainbow-hearts.glitch.me/" id="rainbowhearts" class="fun_image">
      <img src="/images/projects/rainbowhearts.png" alt="A grey web page with white and green text, with a large illustration of two interlocking hearts in rainbow and purple/black/grey/white colours. These are the colours of the rainbow pride flag and the asexual pride flag.">
    </a>
  </li>

  <li class="illustrated_item">
    <dl>
      <dt>
        <a href="https://books.alexwlchan.net/">my book tracker</a>
      </dt>
      <dd>
        This is a site where I track the books I’m reading, and try to write a few paragraphs about why I did or didn’t like each book.
      </dd>
    </dl>
    <a href="https://books.alexwlchan.net/" id="booktracker" class="fun_image">
      <img src="/images/projects/booktracker.png" alt="A web page with a purple header, a purple-ish book cover in the top-right, and text on the page titled 'The Galaxy, and the Ground Within'.">
    </a>
  </li>

  <li class="illustrated_item">
    <dl>
      <dt>
        <a href="https://twitter.com/KempisBot">KempisBot</a>
      </dt>
      <dd>
        Turning the fifteenth-century book <em>The Imitation of Christ</em> into a Twitter thread.
        This was my friend Jay’s idea.
        You can read his post about <a href="https://jayhulme.com/blog/kempisbot">why we did it</a>, and my post about <a href="{% post_url 2021/2021-01-31-kempisbot %}">how we did it</a>.
      </dd>
    </dl>
    <a href="https://twitter.com/KempisBot" id="kempisbot" class="fun_image">
      <img src="/images/projects/kempisbot.png" alt="The Twitter page for KempisBot, with a header image showing an old manuscript with handwritten pages and the profile image an illustration of Thomas Kempis.">
    </a>
  </li>

  <li class="illustrated_item">
    <dl>
      <dt>
        <a href="https://rainbow-valknuts.glitch.me/">Rainbow valknuts</a>
      </dt>
      <dd>
        Create sets of interlocking Valknuts in a variety of Pride flags.
        This is based on an idea by <a href="https://twitter.com/KlezmerGryphon/status/1173897515843735553">@KlezmerGryphon</a>, and it uses some code I wrote for <a href="{% post_url 2019/2019-09-23-triangular-coordinates-in-svg %}">drawing in triangular coordinates</a>.
      </dd>
    </dl>
    <a href="https://rainbow-valknuts.glitch.me/" id="rainbowvalknuts" class="fun_image">
      <img src="/images/projects/rainbowvalknuts.png" alt="A dark-background web page with three interlocking triangles (a Valknut) in various stripes for different pride flags, and the caption 'Your cowardly bigotry is an affront to the Allfather'.">
    </a>
  </li>

  <li class="illustrated_item">
    <dl>
      <dt>
        <a href="https://finduntaggedtumblrposts.com/">Find Untagged Tumblr Posts</a>
      </dt>
      <dd>
        I made this for a friend who was trying to be more consistent about tagging posts on her Tumblr, and was struggling to find posts she’d never tagged.
      </dd>
    </dl>
    <a href="https://finduntaggedtumblrposts.com/" id="finduntaggedtumblrposts" class="fun_image">
      <img src="/images/projects/finduntaggedtumblrposts.png" alt="A web page with a blue header titled 'Find Untagged Tumblr Posts', a large text box for somebody to put in a URL, and a large blue button labelled 'Get my untagged posts!'.">
    </a>
  </li>

  <li class="illustrated_item">
    <dl>
      <dt>
        <a href="http://uk-stations-map.glitch.me">UK stations map</a>
      </dt>
      <dd>
        An interactive map that lets you plot the railway stations you’ve visited in the UK and Ireland.
      </dd>
    </dl>
    <a href="http://uk-stations-map.glitch.me" id="ukstationsmap" class="fun_image">
      <img src="/images/projects/ukstationsmap.png" alt="A greyscale map of the UK and Ireland with green dots overlaid at various points, representing the position of railway stations.">
    </a>
  </li>

  <li class="illustrated_item">
    <dl>
      <dt>
        <a href="https://github.com/alexwlchan/specktre">specktre</a>
      </dt>
      <dd>
        Create simple geometric wallpapers from regular tilings of the plane.
        I’ve written <a href="{% post_url 2016/2016-10-21-tiling-the-plane-with-pillow %}">blog</a> <a href="{% post_url 2016/2016-10-22-wallpapers-with-pillow %}">posts</a> about how this works.
      </dd>
    </dl>
    <a href="https://github.com/alexwlchan/specktre" id="specktre" class="fun_image">
      <img src="/images/projects/specktre.png" alt="Three wallpapers. From left-to-right: blue hexagons, red squares, yellow triangles. Each wallpaper has tiling shapes in slightly different shades of the main colour.">
    </a>
  </li>

  <li class="illustrated_item">
    <dl>
      <dt>
        <a href="https://marquee-rocket.glitch.me" aria-label="marquee rocket">&lt;marquee&gt; rocket</a>
      </dt>
      <dd>
        <span role="text">Controlling a tiny rocket using nothing but the <span aria-hidden="true">&lt;</span>marquee<span aria-hidden="true">&gt;</span> tag.
        This came from</span> <a href="https://twitter.com/seldo/status/1461848209769197573">a tweet by Laurie Voss</a> about people building web apps with a minimal set of tags.
      </dd>
    </dl>
    <a href="https://github.com/alexwlchan/happybackgrounds" id="happybackgrounds" class="fun_image">
      <img src="/images/projects/marqueerocket.png" alt="A black background with simple buttons for up/down/left/right direction controls, and some play/pause/faster/slower speed controls. There's also an emoji rocket moving around on the black background.">
    </a>
  </li>

  <li class="illustrated_item">
    <dl>
      <dt>
        <a href="https://github.com/alexwlchan/happybackgrounds">happybackgrounds</a>
      </dt>
      <dd>
        Create simple wallpapers and background images using Font Awesome icons on solid colour background.
      </dd>
    </dl>
    <a href="https://github.com/alexwlchan/happybackgrounds" id="happybackgrounds" class="fun_image">
      <img src="/images/projects/happybackgrounds.png" alt="An orange background with small rockets overlaid at various points at angles, meant to invoke imagery of Mars.">
    </a>
  </li>
</ul>
