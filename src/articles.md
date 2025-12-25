---
layout: page
title: Articles
nav_section: articles
---

<style type="x-text/scss">
  @use "components/article_cards";

  .alinks + .acards {
    margin-top: 2em;
  }

  #articles {
    margin-top: 2.5em;
  }
</style>

{#
  The logic here is quite fiddly and took a lot of thought.  It may also be
  implementing a bad design.

  Here's the basic idea: I want to intersperse these two types:

  * featured articles (shown as cards)
  * regular articles (shown as links)

  I also want to maintain a vague semblance of chronological order, but it doesn't
  have to be strict.  In particular I would rather make it look nice than make the
  sorting completely accurate (because I make no guarantees that this is date sort).

  Showing a single card on its own looks a bit odd (maybe I should redesign the
  cards to be horizontal, but that's a bigger piece of work).

  Here's the rough idea:

  * go through the list of articles, and build a running list of featured/unfeatured
    articles that haven't been shown yet
  * whenever you have enough featured articles to show (i.e. 2), check how many
    unfeatured articles are waiting to be shown

    - if ≥3, show those first
    - if <3, keep them and wait for a later opportunity to display them
  * at the end, display anything not yet displayed
#}

{% set ns = namespace(featured_posts=[], remaining_posts=[]) %}

{% set add_article_order = true %}

<div id="articles" data-card-count="2">
{% for this_article in site.articles|sort(attribute="date")|reverse %}
  {% if this_article.is_excluded_from_index %}
    {% continue %}
  {% endif %}

  {% if this_article.is_featured %}
    {% set ns.featured_posts = ns.featured_posts + [this_article] %}
  {% else %}
    {% set ns.remaining_posts = ns.remaining_posts + [this_article] %}
  {% endif %}

  {% if ns.featured_posts|count != 2 %}
    {% continue %}
  {% endif %}

  {%- with articles = ns.featured_posts -%}
    {%- include "partials/article_cards.html" %}
  {%- endwith -%}
  {% set ns.featured_posts = [] %}

  {% if ns.remaining_posts|count >= 3 %}
    {%- with articles = ns.remaining_posts -%}
      {%- include "partials/article_links.html" %}
    {% endwith %}
    {% set ns.remaining_posts = [] %}
  {% endif %}
{% endfor %}

{#
  At the end, display anything not yet displayed
#}

{%- with articles = ns.featured_posts -%}
  {%- include "partials/article_cards.html" %}
{%- endwith -%}

{%- with articles = ns.remaining_posts -%}
  {%- include "partials/article_links.html" %}
{% endwith %}
</div>

<script>
  function arrangeCards() {
    console.debug("Calling arrangeCards()");

    /* https://stackoverflow.com/a/11744120/1558022 */
    const width = window.innerWidth || document.documentElement.clientWidth ||
    document.body.clientWidth;

    const cardCount = width < 1000 ? 2 : 3;
    console.debug(`Based on window width, show ${cardCount} cards in a row`);

    if (Number(document.querySelector("#articles").getAttribute("data-card-count")) === cardCount) {
      console.debug("This is the same as the existing layout; do nothing");
      return;
    }

    console.debug("This is different to the existing layout; do nothing");

   /* First reconstruct the "site.posts" array based on the HTML already
    * on the page.  We're going to just shuffle the HTML elements around;
    * not rearrange the whole thing. */
   const allFeaturedPosts = [...document.querySelectorAll('.acards > li')]
     .map(function(elem) {
       return {
         'elem': elem,
         'type': 'featured',
         'order': Number(elem.getAttribute('data-o'))
       };
     });
   const allRemainingPosts = [...document.querySelectorAll('.alinks > li')]
     .map(function(elem) {
       return {
         'elem': elem,
         'type': 'remaining',
         'order': Number(elem.getAttribute('data-o'))
       };
     });

   const posts = allFeaturedPosts.concat(allRemainingPosts)
     .sort((a, b) => b.order - a.order);

   /* Now re-implement the sorting logic. */
   const container = document.createElement("div");
   container.setAttribute("id", "articles");

   var featuredPosts = [];
   var remainingPosts = [];

   posts.forEach(function(thisArticle) {
     // note: why am I not using an elif here?
     // to satisfy `minify_html`
     // see https://github.com/wilsonzlin/minify-html/issues/242
     if (thisArticle.type === 'featured') {
       featuredPosts.push(thisArticle);
     }

     if (thisArticle.type !== 'featured') {
       remainingPosts.push(thisArticle);
     }

     if (featuredPosts.length !== cardCount) {
       return;
     }

     var articleCards = document.createElement("ul");
     articleCards.setAttribute('class', 'acards');
     featuredPosts.forEach(p => articleCards.appendChild(p.elem));
     container.appendChild(articleCards);
     featuredPosts = [];

     /* If we display three cards horizontally, we want at least five links
      * between them.
      *
      * If we display two cards horizontally, we only need three links
      * between a row of cards.
      */
     const linksBetweenCards = cardCount === 3 ? 5 : 3;

     if (remainingPosts.length >= linksBetweenCards) {
       var articleLinks = document.createElement("ul");
       articleLinks.setAttribute('class', 'alinks');
       remainingPosts.forEach(p => articleLinks.appendChild(p.elem));
       container.appendChild(articleLinks);
       remainingPosts = [];
     }
   });

   if (featuredPosts.length > 0) {
     var articleCards = document.createElement("ul");
     articleCards.setAttribute('class', 'acards');
     featuredPosts.forEach(p => articleCards.appendChild(p.elem));
     container.appendChild(articleCards);
   }

   if (remainingPosts.length > 0) {
     var articleLinks = document.createElement("ul");
     articleLinks.setAttribute('class', 'alinks');
     remainingPosts.forEach(p => articleLinks.appendChild(p.elem));
     container.appendChild(articleLinks);
   }

   document.querySelector('#articles').replaceWith(container);
   document.querySelector('#articles').setAttribute("data-card-count", cardCount);
  }

  window.addEventListener("DOMContentLoaded", arrangeCards);
  window.addEventListener("resize", arrangeCards);
</script>
