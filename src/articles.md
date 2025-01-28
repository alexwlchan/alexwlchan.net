---
layout: page
title: Articles
nav_section: articles
---

<style type="x-text/scss">
  @use "components/article_cards";

  .article_links + .article_cards {
    margin-top: 2em;
  }

  #articles {
    margin-top: 2.5em;
  }
</style>

{% comment %}
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
{% endcomment %}

{% assign featured_posts  = "" | split: ',' %}
{% assign remaining_posts = "" | split: ',' %}

{% assign add_data_metadata = true %}

<div id="articles">
{% for this_article in site.posts %}
  {% if this_article.index.exclude %}
    {% continue %}
  {% endif %}

  {% if this_article.index.feature %}
    {% assign featured_posts = featured_posts | push: this_article %}
  {% else %}
    {% assign remaining_posts = remaining_posts | push: this_article %}
  {% endif %}

  {% unless featured_posts.size == 2 %}
    {% continue %}
  {% endunless %}

  {%- include article_cards.html articles=featured_posts %}
  {% assign featured_posts = "" | split: ',' %}

  {% if remaining_posts.size >= 3 %}
  {%- include article_links.html articles=remaining_posts %}
  {% assign remaining_posts = "" | split: ',' %}
  {% endif %}
{% endfor %}

{% comment %}
  At the end, display anything not yet displayed
{% endcomment %}

{% include article_cards.html articles=featured_posts %}
{% include article_links.html articles=remaining_posts %}
</div>

<script>
  window.addEventListener("DOMContentLoaded", function() {
    /* https://stackoverflow.com/a/11744120/1558022 */
    const width  = window.innerWidth || document.documentElement.clientWidth ||
    document.body.clientWidth;

    if (width < 1000) {
      console.log(`Leaving article cards as 2-column layout (width=${width})`);
      return;
    }

    console.log(`Switching article cards to 3-column layout (width=${width})`);

    /* First reconstruct the "site.posts" array based on the HTML already
     * on the page.  We're going to just shuffle the HTML elements around;
     * not rearrange the whole thing. */
    const allFeaturedPosts = Array.from(document.querySelectorAll('.card'))
      .map(function(elem) {
        return {
          'elem': elem,
          'type': 'featured',
          'date': elem.getAttribute('data-date')
        };
      });
    const allRemainingPosts = Array.from(document.querySelectorAll('.article_links li'))
      .map(function(elem) {
        return {
          'elem': elem,
          'type': 'remaining',
          'date': elem.getAttribute('data-date')
        };
      });

    const posts = allFeaturedPosts.concat(allRemainingPosts)
      .sort((a, b) => a.date > b.date ? -1 : 1);

    /* Now re-implement the sorting logic. */
    const container = document.createElement("div");
    container.setAttribute("id", "articles");

    var featuredPosts = [];
    var remainingPosts = [];

    posts.forEach(function(thisArticle) {
      if (thisArticle.type === 'featured') {
        featuredPosts.push(thisArticle);
      } else {
        remainingPosts.push(thisArticle);
      }

      if (featuredPosts.length !== 3) {
        return;
      }

      var articleCards = document.createElement("ul");
      articleCards.setAttribute('class', 'plain_list article_cards');
      featuredPosts.forEach(p => articleCards.appendChild(p.elem));
      container.appendChild(articleCards);
      featuredPosts = [];

      if (remainingPosts.length >= 5) {
        var articleLinks = document.createElement("ul");
        articleLinks.setAttribute('class', 'plain_list article_links');
        remainingPosts.forEach(p => articleLinks.appendChild(p.elem));
        container.appendChild(articleLinks);
        remainingPosts = [];
      }
    });

    if (featuredPosts.length > 0) {
      var articleCards = document.createElement("ul");
      articleCards.setAttribute('class', 'plain_list article_cards');
      featuredPosts.forEach(p => articleCards.appendChild(p.elem));
      container.appendChild(articleCards);
    }

    if (remainingPosts.length > 0) {
      var articleLinks = document.createElement("ul");
      articleLinks.setAttribute('class', 'plain_list article_links');
      remainingPosts.forEach(p => articleLinks.appendChild(p.elem));
      container.appendChild(articleLinks);
    }

    document.querySelector('#articles').replaceWith(container);
  });
</script>
